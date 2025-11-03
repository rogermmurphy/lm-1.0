"""
Content Sharing Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..models import SharedContentCreate, SharedContent

router = APIRouter(prefix="/sharing", tags=["sharing"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


@router.post("", response_model=dict)
async def share_content(
    share: SharedContentCreate,
    authorization: Optional[str] = Header(None)
):
    """Share content with another user"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO shared_content 
                (content_type, content_id, shared_by_user_id, shared_with_user_id, permissions)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, content_type, content_id, shared_by_user_id, shared_with_user_id, permissions, created_at
            """, (share.content_type, share.content_id, user_id, share.shared_with_user_id, share.permissions))
            
            result = cur.fetchone()
            conn.commit()
            
            return {"message": "Content shared successfully", "shared_content": dict(result)}
    finally:
        conn.close()


@router.get("/received", response_model=List[dict])
async def get_shared_with_me(
    content_type: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """Get content shared with me"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if content_type:
                cur.execute("""
                    SELECT * FROM shared_content
                    WHERE shared_with_user_id = %s AND content_type = %s
                    ORDER BY created_at DESC
                """, (user_id, content_type))
            else:
                cur.execute("""
                    SELECT * FROM shared_content
                    WHERE shared_with_user_id = %s
                    ORDER BY created_at DESC
                """, (user_id,))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.get("/sent", response_model=List[dict])
async def get_shared_by_me(
    authorization: Optional[str] = Header(None)
):
    """Get content I've shared"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM shared_content
                WHERE shared_by_user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.delete("/{share_id}")
async def revoke_share(
    share_id: int,
    authorization: Optional[str] = Header(None)
):
    """Revoke shared content"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM shared_content
                WHERE id = %s AND shared_by_user_id = %s
            """, (share_id, user_id))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Shared content not found")
            
            conn.commit()
            return {"message": "Share revoked"}
    finally:
        conn.close()
