"""
Leaderboards Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings

router = APIRouter(prefix="/leaderboards", tags=["leaderboards"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


@router.get("/global", response_model=List[dict])
async def get_global_leaderboard(limit: int = 10):
    """Get global leaderboard"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT up.user_id, up.total_points, up.level, up.streak_days,
                       u.username, u.email
                FROM user_points up
                JOIN users u ON up.user_id = u.id
                ORDER BY up.total_points DESC
                LIMIT %s
            """, (limit,))
            
            results = cur.fetchall()
            # Add rank
            for i, row in enumerate(results, 1):
                row['rank'] = i
            
            return [dict(row) for row in results]
    finally:
        conn.close()


@router.get("/class/{class_id}", response_model=List[dict])
async def get_class_leaderboard(class_id: int, limit: int = 10):
    """Get class-specific leaderboard"""
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT up.user_id, up.total_points, up.level, u.username
                FROM user_points up
                JOIN users u ON up.user_id = u.id
                JOIN class_enrollments ce ON u.id = ce.user_id
                WHERE ce.class_id = %s
                ORDER BY up.total_points DESC
                LIMIT %s
            """, (class_id, limit))
            
            results = cur.fetchall()
            for i, row in enumerate(results, 1):
                row['rank'] = i
            
            return [dict(row) for row in results]
    finally:
        conn.close()
