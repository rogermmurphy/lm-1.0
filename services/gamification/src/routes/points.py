"""
Points Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..models import PointAward

router = APIRouter(prefix="/points", tags=["points"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


@router.get("", response_model=dict)
async def get_user_points(authorization: Optional[str] = Header(None)):
    """Get user's points and level"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            
            if not result:
                return {
                    "user_id": user_id,
                    "total_points": 0,
                    "level": 1,
                    "streak_days": 0,
                    "last_activity_date": None
                }
            
            return dict(result)
    finally:
        conn.close()


@router.post("/award", response_model=dict)
async def award_points(
    award: PointAward,
    authorization: Optional[str] = Header(None)
):
    """Award points to user"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Call award_points function
            cur.execute(
                "SELECT award_points(%s, %s, %s, %s, %s)",
                (user_id, award.points, award.reason, award.reference_type, award.reference_id)
            )
            conn.commit()
            
            # Get updated points
            cur.execute("SELECT * FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            
            return {"message": "Points awarded", "user_points": dict(result)}
    finally:
        conn.close()


@router.get("/transactions", response_model=List[dict])
async def get_transactions(
    limit: int = 50,
    authorization: Optional[str] = Header(None)
):
    """Get point transaction history"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM point_transactions
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.post("/streak", response_model=dict)
async def update_streak(authorization: Optional[str] = Header(None)):
    """Update daily activity streak"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Call update_streak function
            cur.execute("SELECT update_streak(%s)", (user_id,))
            conn.commit()
            
            # Get updated streak
            cur.execute("SELECT streak_days FROM user_points WHERE user_id = %s", (user_id,))
            result = cur.fetchone()
            
            streak_days = result['streak_days'] if result else 0
            return {"message": "Streak updated", "streak_days": streak_days}
    finally:
        conn.close()
