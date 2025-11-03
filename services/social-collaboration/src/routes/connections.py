"""
Classmate Connections Routes
"""
from fastapi import APIRouter, HTTPException, Header
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

from ..config import settings
from ..models import ConnectionCreate, ConnectionUpdate, Connection

router = APIRouter(prefix="/connections", tags=["connections"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


@router.post("", response_model=dict)
async def send_connection_request(
    connection: ConnectionCreate,
    authorization: Optional[str] = Header(None)
):
    """Send a connection request to another user"""
    # TODO: Extract user_id from JWT token
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO classmate_connections (user_id, classmate_user_id, status)
                VALUES (%s, %s, 'pending')
                RETURNING id, user_id, classmate_user_id, status, created_at, updated_at
            """, (user_id, connection.classmate_user_id))
            
            result = cur.fetchone()
            conn.commit()
            
            return {"message": "Connection request sent", "connection": dict(result)}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Connection already exists")
    finally:
        conn.close()


@router.get("", response_model=List[dict])
async def get_connections(
    status: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """Get user's connections"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if status:
                cur.execute("""
                    SELECT * FROM classmate_connections
                    WHERE (user_id = %s OR classmate_user_id = %s) AND status = %s
                    ORDER BY created_at DESC
                """, (user_id, user_id, status))
            else:
                cur.execute("""
                    SELECT * FROM classmate_connections
                    WHERE user_id = %s OR classmate_user_id = %s
                    ORDER BY created_at DESC
                """, (user_id, user_id))
            
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@router.put("/{connection_id}", response_model=dict)
async def update_connection(
    connection_id: int,
    update: ConnectionUpdate,
    authorization: Optional[str] = Header(None)
):
    """Update connection status (accept/reject/block)"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                UPDATE classmate_connections
                SET status = %s, updated_at = NOW()
                WHERE id = %s AND classmate_user_id = %s
                RETURNING id, user_id, classmate_user_id, status, created_at, updated_at
            """, (update.status, connection_id, user_id))
            
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Connection not found")
            
            conn.commit()
            return {"message": "Connection updated", "connection": dict(result)}
    finally:
        conn.close()


@router.delete("/{connection_id}")
async def delete_connection(
    connection_id: int,
    authorization: Optional[str] = Header(None)
):
    """Delete a connection"""
    user_id = 1  # Placeholder
    
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM classmate_connections
                WHERE id = %s AND (user_id = %s OR classmate_user_id = %s)
            """, (connection_id, user_id, user_id))
            
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Connection not found")
            
            conn.commit()
            return {"message": "Connection deleted"}
    finally:
        conn.close()
