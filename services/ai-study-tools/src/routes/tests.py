"""
Test generation routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import psycopg2
import json
from datetime import datetime

from ..models import TestGenerateRequest, TestResponse, TestQuestion, TestAttemptRequest, TestAttemptResponse
from ..services.ai_service import AIService
from ..config import settings

router = APIRouter(prefix="/tests", tags=["tests"])


def get_db():
    """Get database connection"""
    conn = psycopg2.connect(settings.database_url)
    try:
        yield conn
    finally:
        conn.close()


def get_ai_service():
    """Get AI service instance"""
    return AIService()


@router.post("/generate", response_model=TestResponse)
async def generate_test(
    request: TestGenerateRequest,
    conn = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Generate AI test from source materials"""
    try:
        cur = conn.cursor()
        
        # Get source content
        source_content = ""
        if request.source_material_ids:
            placeholders = ','.join(['%s'] * len(request.source_material_ids))
            cur.execute(f"""
                SELECT content FROM study_materials
                WHERE id IN ({placeholders})
            """, request.source_material_ids)
            materials = cur.fetchall()
            source_content = "\n\n".join([m[0] for m in materials])
        
        if not source_content:
            raise HTTPException(status_code=400, detail="No source materials provided")
        
        # Generate test using AI
        questions_data = ai_service.generate_test(
            source_content,
            request.difficulty.value,
            request.question_count
        )
        
        # Save test to database
        cur.execute("""
            INSERT INTO generated_tests (class_id, user_id, title, description, difficulty, question_count, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (
            request.class_id,
            request.user_id,
            request.title,
            request.description,
            request.difficulty.value,
            len(questions_data),
            datetime.now(),
            datetime.now()
        ))
        
        test_id, created_at = cur.fetchone()
        
        # Save questions
        questions = []
        for idx, q in enumerate(questions_data):
            cur.execute("""
                INSERT INTO test_questions (test_id, question_text, question_type, correct_answer, options, explanation, points, order_index, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                test_id,
                q['question_text'],
                q['question_type'],
                q.get('correct_answer'),
                json.dumps(q.get('options', [])),
                q.get('explanation'),
                q.get('points', 1),
                idx,
                datetime.now()
            ))
            
            questions.append(TestQuestion(**q))
        
        conn.commit()
        cur.close()
        
        return TestResponse(
            id=test_id,
            title=request.title,
            description=request.description,
            difficulty=request.difficulty,
            question_count=len(questions),
            questions=questions,
            created_at=created_at
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{test_id}", response_model=TestResponse)
async def get_test(test_id: int, conn = Depends(get_db)):
    """Get a specific test with questions"""
    try:
        cur = conn.cursor()
        
        # Get test
        cur.execute("""
            SELECT id, title, description, difficulty, question_count, created_at
            FROM generated_tests
            WHERE id = %s
        """, (test_id,))
        
        test_row = cur.fetchone()
        if not test_row:
            raise HTTPException(status_code=404, detail="Test not found")
        
        # Get questions
        cur.execute("""
            SELECT question_text, question_type, correct_answer, options, explanation, points
            FROM test_questions
            WHERE test_id = %s
            ORDER BY order_index
        """, (test_id,))
        
        question_rows = cur.fetchall()
        cur.close()
        
        questions = [
            TestQuestion(
                question_text=row[0],
                question_type=row[1],
                correct_answer=row[2],
                options=json.loads(row[3]) if row[3] else None,
                explanation=row[4],
                points=row[5]
            )
            for row in question_rows
        ]
        
        return TestResponse(
            id=test_row[0],
            title=test_row[1],
            description=test_row[2],
            difficulty=test_row[3],
            question_count=test_row[4],
            questions=questions,
            created_at=test_row[5]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attempts", response_model=TestAttemptResponse)
async def submit_test_attempt(
    request: TestAttemptRequest,
    conn = Depends(get_db)
):
    """Submit a test attempt and calculate score"""
    try:
        cur = conn.cursor()
        
        # Get correct answers
        cur.execute("""
            SELECT id, correct_answer, points
            FROM test_questions
            WHERE test_id = %s
            ORDER BY order_index
        """, (request.test_id,))
        
        questions = cur.fetchall()
        
        # Calculate score
        score = 0
        max_score = 0
        for q_id, correct, points in questions:
            max_score += points
            user_answer = request.answers.get(str(q_id))
            if user_answer and user_answer.lower() == correct.lower():
                score += points
        
        # Save attempt
        cur.execute("""
            INSERT INTO test_attempts (test_id, user_id, started_at, completed_at, score, max_score, answers)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, completed_at
        """, (
            request.test_id,
            request.user_id,
            datetime.now(),
            datetime.now(),
            score,
            max_score,
            json.dumps(request.answers)
        ))
        
        attempt_id, completed_at = cur.fetchone()
        conn.commit()
        cur.close()
        
        percentage = (score / max_score * 100) if max_score > 0 else 0
        
        return TestAttemptResponse(
            id=attempt_id,
            test_id=request.test_id,
            score=score,
            max_score=max_score,
            percentage=percentage,
            completed_at=completed_at
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
