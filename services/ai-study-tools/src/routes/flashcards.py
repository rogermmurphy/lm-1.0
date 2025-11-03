"""
Flashcard routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import psycopg2
from datetime import datetime, timedelta

from ..models import (
    FlashcardDeckCreate, FlashcardCreate, FlashcardDeckResponse,
    FlashcardResponse, FlashcardReviewRequest, FlashcardReviewResponse
)
from ..services.ai_service import AIService
from ..config import settings

router = APIRouter(prefix="/flashcards", tags=["flashcards"])


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


@router.post("/decks", response_model=FlashcardDeckResponse)
async def create_deck(
    request: FlashcardDeckCreate,
    conn = Depends(get_db)
):
    """Create a new flashcard deck"""
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO flashcard_decks (class_id, user_id, title, description, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, created_at
        """, (
            request.class_id,
            request.user_id,
            request.title,
            request.description,
            datetime.now(),
            datetime.now()
        ))
        
        deck_id, created_at = cur.fetchone()
        conn.commit()
        cur.close()
        
        return FlashcardDeckResponse(
            id=deck_id,
            title=request.title,
            description=request.description,
            card_count=0,
            cards=[],
            created_at=created_at
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/decks/{deck_id}/generate")
async def generate_flashcards(
    deck_id: int,
    source_material_id: int,
    card_count: int = 10,
    conn = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Generate flashcards from source material"""
    try:
        cur = conn.cursor()
        
        # Get source content
        cur.execute("SELECT content FROM study_materials WHERE id = %s", (source_material_id,))
        result = cur.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Source material not found")
        
        source_content = result[0]
        
        # Generate flashcards using AI
        cards_data = ai_service.generate_flashcards(source_content, card_count)
        
        # Save flashcards
        for idx, card in enumerate(cards_data):
            cur.execute("""
                INSERT INTO flashcards (deck_id, front_text, back_text, order_index, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                deck_id,
                card['front_text'],
                card['back_text'],
                idx,
                datetime.now(),
                datetime.now()
            ))
        
        # Update deck card count
        cur.execute("""
            UPDATE flashcard_decks
            SET card_count = card_count + %s, updated_at = %s
            WHERE id = %s
        """, (len(cards_data), datetime.now(), deck_id))
        
        conn.commit()
        cur.close()
        
        return {"message": f"Generated {len(cards_data)} flashcards", "count": len(cards_data)}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decks/{deck_id}", response_model=FlashcardDeckResponse)
async def get_deck(deck_id: int, conn = Depends(get_db)):
    """Get a flashcard deck with all cards"""
    try:
        cur = conn.cursor()
        
        # Get deck
        cur.execute("""
            SELECT id, title, description, card_count, created_at
            FROM flashcard_decks
            WHERE id = %s
        """, (deck_id,))
        
        deck_row = cur.fetchone()
        if not deck_row:
            raise HTTPException(status_code=404, detail="Deck not found")
        
        # Get cards
        cur.execute("""
            SELECT id, front_text, back_text, order_index
            FROM flashcards
            WHERE deck_id = %s
            ORDER BY order_index
        """, (deck_id,))
        
        card_rows = cur.fetchall()
        cur.close()
        
        cards = [
            FlashcardResponse(
                id=row[0],
                front_text=row[1],
                back_text=row[2],
                order_index=row[3]
            )
            for row in card_rows
        ]
        
        return FlashcardDeckResponse(
            id=deck_row[0],
            title=deck_row[1],
            description=deck_row[2],
            card_count=deck_row[3],
            cards=cards,
            created_at=deck_row[4]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cards", response_model=FlashcardResponse)
async def create_card(
    request: FlashcardCreate,
    conn = Depends(get_db)
):
    """Create a single flashcard"""
    try:
        cur = conn.cursor()
        
        # Get current max order_index
        cur.execute("SELECT COALESCE(MAX(order_index), -1) FROM flashcards WHERE deck_id = %s", (request.deck_id,))
        max_index = cur.fetchone()[0]
        
        cur.execute("""
            INSERT INTO flashcards (deck_id, front_text, back_text, order_index, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, order_index
        """, (
            request.deck_id,
            request.front_text,
            request.back_text,
            max_index + 1,
            datetime.now(),
            datetime.now()
        ))
        
        card_id, order_index = cur.fetchone()
        
        # Update deck card count
        cur.execute("""
            UPDATE flashcard_decks
            SET card_count = card_count + 1, updated_at = %s
            WHERE id = %s
        """, (datetime.now(), request.deck_id))
        
        conn.commit()
        cur.close()
        
        return FlashcardResponse(
            id=card_id,
            front_text=request.front_text,
            back_text=request.back_text,
            order_index=order_index
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reviews", response_model=FlashcardReviewResponse)
async def review_card(
    request: FlashcardReviewRequest,
    conn = Depends(get_db)
):
    """Record a flashcard review (spaced repetition)"""
    try:
        cur = conn.cursor()
        
        # Get previous review if exists
        cur.execute("""
            SELECT interval_days, ease_factor
            FROM flashcard_reviews
            WHERE card_id = %s AND user_id = %s
            ORDER BY reviewed_at DESC
            LIMIT 1
        """, (request.card_id, request.user_id))
        
        prev_review = cur.fetchone()
        
        # Calculate new interval using SM-2 algorithm
        if prev_review:
            prev_interval, prev_ease = prev_review
        else:
            prev_interval, prev_ease = 1, 2.5
        
        # Update ease factor based on quality (0-5)
        new_ease = max(1.3, prev_ease + (0.1 - (5 - request.quality) * (0.08 + (5 - request.quality) * 0.02)))
        
        # Calculate new interval
        if request.quality < 3:
            new_interval = 1
        elif prev_interval == 1:
            new_interval = 6
        else:
            new_interval = int(prev_interval * new_ease)
        
        next_review = datetime.now() + timedelta(days=new_interval)
        
        # Save review
        cur.execute("""
            INSERT INTO flashcard_reviews (card_id, user_id, quality, next_review_date, interval_days, ease_factor, reviewed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            request.card_id,
            request.user_id,
            request.quality,
            next_review,
            new_interval,
            new_ease,
            datetime.now()
        ))
        
        review_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return FlashcardReviewResponse(
            id=review_id,
            next_review_date=next_review,
            interval_days=new_interval,
            ease_factor=new_ease
        )
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decks/user/{user_id}", response_model=List[FlashcardDeckResponse])
async def list_user_decks(user_id: int, conn = Depends(get_db)):
    """List all decks for a user"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, description, card_count, created_at
            FROM flashcard_decks
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        
        deck_rows = cur.fetchall()
        
        decks = []
        for deck_row in deck_rows:
            # Get cards for this deck
            cur.execute("""
                SELECT id, front_text, back_text, order_index
                FROM flashcards
                WHERE deck_id = %s
                ORDER BY order_index
            """, (deck_row[0],))
            
            card_rows = cur.fetchall()
            cards = [
                FlashcardResponse(
                    id=row[0],
                    front_text=row[1],
                    back_text=row[2],
                    order_index=row[3]
                )
                for row in card_rows
            ]
            
            decks.append(FlashcardDeckResponse(
                id=deck_row[0],
                title=deck_row[1],
                description=deck_row[2],
                card_count=deck_row[3],
                cards=cards,
                created_at=deck_row[4]
            ))
        
        cur.close()
        return decks
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
