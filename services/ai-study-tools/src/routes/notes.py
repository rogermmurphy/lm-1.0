"""
Notes generation routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import psycopg2
from datetime import datetime

from ..models import NoteGenerateRequest, NoteResponse
from ..services.ai_service import AIService
from ..config import settings

router = APIRouter(prefix="/notes", tags=["notes"])


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


@router.post("/generate", response_model=NoteResponse)
async def generate_notes(
    request: NoteGenerateRequest,
    conn = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Generate AI notes from source material"""
    try:
        cur = conn.cursor()
        
        # Get source content based on type
        source_content = ""
        if request.source_type == "recording":
            cur.execute("SELECT transcript FROM transcriptions WHERE id = %s", (request.source_id,))
            result = cur.fetchone()
            if result:
                source_content = result[0]
        elif request.source_type == "photo":
            cur.execute("SELECT extracted_text FROM photos WHERE id = %s", (request.source_id,))
            result = cur.fetchone()
            if result:
                source_content = result[0]
        elif request.source_type == "textbook":
            cur.execute("SELECT content FROM textbook_chunks WHERE textbook_id = %s ORDER BY chunk_index", (request.source_id,))
            chunks = cur.fetchall()
            source_content = "\n\n".join([chunk[0] for chunk in chunks])
        
        if not source_content:
            raise HTTPException(status_code=404, detail="Source content not found")
        
        # Generate notes using AI
        generated = ai_service.generate_notes(source_content, request.source_type.value)
        
        # Save to database
        cur.execute("""
            INSERT INTO study_materials (user_id, title, content, is_ai_generated, class_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (
            request.user_id,
            generated['title'],
            generated['content'],
            True,
            request.class_id,
            datetime.now()
        ))
        
        note_id, created_at = cur.fetchone()
        
        # Link to source
        cur.execute("""
            INSERT INTO note_sources (note_id, source_type, source_id)
            VALUES (%s, %s, %s)
        """, (note_id, request.source_type.value, request.source_id))
        
        conn.commit()
        cur.close()
        
        return NoteResponse(
            id=note_id,
            title=generated['title'],
            content=generated['content'],
            is_ai_generated=True,
            class_id=request.class_id,
            created_at=created_at
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int, conn = Depends(get_db)):
    """Get a specific note"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, content, is_ai_generated, class_id, created_at
            FROM study_materials
            WHERE id = %s
        """, (note_id,))
        
        result = cur.fetchone()
        cur.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return NoteResponse(
            id=result[0],
            title=result[1],
            content=result[2],
            is_ai_generated=result[3],
            class_id=result[4],
            created_at=result[5]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[NoteResponse])
async def list_notes(
    user_id: int,
    class_id: int = None,
    conn = Depends(get_db)
):
    """List all notes for a user"""
    try:
        cur = conn.cursor()
        
        if class_id:
            cur.execute("""
                SELECT id, title, content, is_ai_generated, class_id, created_at
                FROM study_materials
                WHERE user_id = %s AND class_id = %s
                ORDER BY created_at DESC
            """, (user_id, class_id))
        else:
            cur.execute("""
                SELECT id, title, content, is_ai_generated, class_id, created_at
                FROM study_materials
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
        
        results = cur.fetchall()
        cur.close()
        
        return [
            NoteResponse(
                id=row[0],
                title=row[1],
                content=row[2],
                is_ai_generated=row[3],
                class_id=row[4],
                created_at=row[5]
            )
            for row in results
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
