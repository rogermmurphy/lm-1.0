import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
from datetime import datetime
from ..config import settings

class MessageService:
    def __init__(self):
        self.db_url = settings.database_url
    
    def get_connection(self):
        return psycopg2.connect(self.db_url)
    
    def send_message(self, sender_id: int, recipient_id: int, message: str) -> Dict[str, Any]:
        """Send a direct message"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO direct_messages (sender_id, recipient_id, message)
                    VALUES (%s, %s, %s)
                    RETURNING id, sender_id, recipient_id, message, is_read, read_at, created_at
                """, (sender_id, recipient_id, message))
                conn.commit()
                return dict(cur.fetchone())
        finally:
            conn.close()
    
    def get_conversations(self, user_id: int) -> List[Dict[str, Any]]:
        """Get list of conversations for a user"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        CASE 
                            WHEN user1_id = %s THEN user2_id 
                            ELSE user1_id 
                        END as other_user_id,
                        last_message_at,
                        message_count,
                        unread_count
                    FROM message_conversations
                    WHERE user1_id = %s OR user2_id = %s
                    ORDER BY last_message_at DESC
                """, (user_id, user_id, user_id))
                return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()
    
    def get_conversation(self, user_id: int, other_user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get messages in a conversation between two users"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, sender_id, recipient_id, message, is_read, read_at, created_at
                    FROM direct_messages
                    WHERE (sender_id = %s AND recipient_id = %s)
                       OR (sender_id = %s AND recipient_id = %s)
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (user_id, other_user_id, other_user_id, user_id, limit))
                messages = [dict(row) for row in cur.fetchall()]
                # Return in chronological order (oldest first)
                return list(reversed(messages))
        finally:
            conn.close()
    
    def mark_messages_as_read(self, user_id: int, message_ids: List[int]) -> int:
        """Mark messages as read"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE direct_messages
                    SET is_read = true, read_at = CURRENT_TIMESTAMP
                    WHERE recipient_id = %s AND id = ANY(%s) AND is_read = false
                """, (user_id, message_ids))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()
    
    def delete_message(self, user_id: int, message_id: int) -> bool:
        """Delete a message (only if sender)"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM direct_messages
                    WHERE id = %s AND sender_id = %s
                """, (message_id, user_id))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
