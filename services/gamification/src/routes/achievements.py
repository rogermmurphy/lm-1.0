"""
Achievements Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..models import Achievement, AchievementCreate

router = APIRouter(prefix="/achievements", tags=["achievements"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


@router.get("", response_model=List[dict])
async def get_achievements(authorization: Optional[str] = Header(None)):
    """Get user's achievements"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM achievements
                WHERE user_id = %s
                ORDER BY earned_at DESC
            """, (user_id,))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.post("", response_model=dict)
async def award_achievement(
    achievement: AchievementCreate,
    authorization: Optional[str] = Header(None)
):
    """Award achievement to user"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO achievements 
                (user_id, achievement_type, achievement_name, achievement_description, points_awarded)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            """, (user_id, achievement.achievement_type, achievement.achievement_name,
                  achievement.achievement_description, achievement.points_awarded))
            
            result = cur.fetchone()
            conn.commit()
            
            return {"message": "Achievement awarded", "achievement": dict(result)}
    finally:
        conn.close()
