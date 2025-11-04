import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..config import settings

class NotificationService:
    def __init__(self):
        self.db_url = settings.database_url
    
    def get_connection(self):
        return psycopg2.connect(self.db_url)
    
    def list_notifications(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """List notifications for a user"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, user_id, notification_type as type, title, message, reference_id as related_id, reference_type as related_type,
                           action_url, is_read, read_at, created_at
                    FROM notifications
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                """, (user_id, limit, offset))
                return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()
    
    def mark_as_read(self, user_id: int, notification_ids: List[int]) -> int:
        """Mark notifications as read"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE notifications
                    SET is_read = true, read_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND id = ANY(%s) AND is_read = false
                """, (user_id, notification_ids))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE notifications
                    SET is_read = true, read_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s AND is_read = false
                """, (user_id,))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()
    
    def delete_notification(self, user_id: int, notification_id: int) -> bool:
        """Delete a notification"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM notifications
                    WHERE id = %s AND user_id = %s
                """, (notification_id, user_id))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM notifications
                    WHERE user_id = %s AND is_read = false
                """, (user_id,))
                return cur.fetchone()[0]
        finally:
            conn.close()
    
    def get_preferences(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get notification preferences for a user"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT user_id, email_enabled, push_enabled,
                           assignment_notifications, grade_notifications,
                           message_notifications, social_notifications,
                           achievement_notifications, updated_at
                    FROM notification_preferences
                    WHERE user_id = %s
                """, (user_id,))
                result = cur.fetchone()
                if result:
                    return dict(result)
                
                # Create default preferences if none exist
                cur.execute("""
                    INSERT INTO notification_preferences (user_id)
                    VALUES (%s)
                    RETURNING user_id, email_enabled, push_enabled,
                              assignment_notifications, grade_notifications,
                              message_notifications, social_notifications,
                              achievement_notifications, updated_at
                """, (user_id,))
                conn.commit()
                return dict(cur.fetchone())
        finally:
            conn.close()
    
    def update_preferences(self, user_id: int, preferences: Dict[str, bool]) -> Dict[str, Any]:
        """Update notification preferences"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Ensure preferences exist
                cur.execute("""
                    INSERT INTO notification_preferences (user_id)
                    VALUES (%s)
                    ON CONFLICT (user_id) DO NOTHING
                """, (user_id,))
                
                # Update preferences
                cur.execute("""
                    UPDATE notification_preferences
                    SET email_enabled = COALESCE(%s, email_enabled),
                        push_enabled = COALESCE(%s, push_enabled),
                        assignment_notifications = COALESCE(%s, assignment_notifications),
                        grade_notifications = COALESCE(%s, grade_notifications),
                        message_notifications = COALESCE(%s, message_notifications),
                        social_notifications = COALESCE(%s, social_notifications),
                        achievement_notifications = COALESCE(%s, achievement_notifications),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = %s
                    RETURNING user_id, email_enabled, push_enabled,
                              assignment_notifications, grade_notifications,
                              message_notifications, social_notifications,
                              achievement_notifications, updated_at
                """, (
                    preferences.get('email_enabled'),
                    preferences.get('push_enabled'),
                    preferences.get('assignment_notifications'),
                    preferences.get('grade_notifications'),
                    preferences.get('message_notifications'),
                    preferences.get('social_notifications'),
                    preferences.get('achievement_notifications'),
                    user_id
                ))
                conn.commit()
                return dict(cur.fetchone())
        finally:
            conn.close()
    
    def create_notification(self, notification_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new notification"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    INSERT INTO notifications (user_id, notification_type, title, message, reference_id, reference_type, action_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, user_id, notification_type as type, title, message, reference_id as related_id, reference_type as related_type,
                              action_url, is_read, read_at, created_at
                """, (
                    notification_data['user_id'],
                    notification_data['type'],
                    notification_data['title'],
                    notification_data['message'],
                    notification_data.get('related_id'),
                    notification_data.get('related_type'),
                    notification_data.get('action_url')
                ))
                conn.commit()
                return dict(cur.fetchone())
        finally:
            conn.close()
