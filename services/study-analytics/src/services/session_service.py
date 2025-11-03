"""
Session management business logic
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Optional, List, Dict, Any
import requests
from ..config import settings

class SessionService:
    """Service for managing study sessions"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def start_session(self, user_id: int, class_id: Optional[int], 
                     session_type: str, focus_mode: bool, 
                     location: Optional[str]) -> Dict[str, Any]:
        """Start a new study session"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                INSERT INTO study_sessions 
                (user_id, class_id, session_type, focus_mode, location)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, start_time
            """, (user_id, class_id, session_type, focus_mode, location))
            
            result = cursor.fetchone()
            self.conn.commit()
            
            return {
                "session_id": result['id'],
                "start_time": result['start_time'].isoformat(),
                "message": "Study session started"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to start session: {str(e)}")
        finally:
            cursor.close()
    
    def end_session(self, session_id: int, user_id: int,
                   mood_rating: Optional[int], productivity_rating: Optional[int],
                   notes: Optional[str]) -> Dict[str, Any]:
        """End an active study session"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Update session
            cursor.execute("""
                UPDATE study_sessions
                SET end_time = NOW(),
                    mood_rating = %s,
                    productivity_rating = %s,
                    notes = %s
                WHERE id = %s AND user_id = %s AND end_time IS NULL
                RETURNING id, duration_minutes
            """, (mood_rating, productivity_rating, notes, session_id, user_id))
            
            result = cursor.fetchone()
            if not result:
                raise Exception("Session not found or already ended")
            
            # Calculate points (0.5 points per minute)
            duration = result['duration_minutes'] or 0
            points = int(duration * 0.5)
            
            # Award points via gamification service
            if points > 0:
                self._award_points(user_id, points, "study_session", session_id)
            
            self.conn.commit()
            
            return {
                "session_id": session_id,
                "duration_minutes": duration,
                "points_earned": points,
                "message": "Study session ended"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to end session: {str(e)}")
        finally:
            cursor.close()
    
    def log_activity(self, session_id: int, user_id: int,
                    activity_type: str, content_type: Optional[str],
                    content_id: Optional[int], items_completed: int,
                    items_correct: Optional[int], duration_minutes: Optional[int],
                    metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Log an activity within a session"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Verify session belongs to user and is active
            cursor.execute("""
                SELECT id FROM study_sessions
                WHERE id = %s AND user_id = %s AND end_time IS NULL
            """, (session_id, user_id))
            
            if not cursor.fetchone():
                raise Exception("Session not found or already ended")
            
            # Calculate points for activity
            points = 0
            if items_correct is not None and items_correct > 0:
                points = items_correct  # 1 point per correct item
            
            # Insert activity
            cursor.execute("""
                INSERT INTO session_activities
                (session_id, activity_type, content_type, content_id,
                 items_completed, items_correct, duration_minutes, 
                 points_earned, metadata, end_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id, accuracy_percentage, points_earned
            """, (session_id, activity_type, content_type, content_id,
                  items_completed, items_correct, duration_minutes, points, metadata))
            
            result = cursor.fetchone()
            self.conn.commit()
            
            return {
                "activity_id": result['id'],
                "accuracy_percentage": float(result['accuracy_percentage']) if result['accuracy_percentage'] else None,
                "points_earned": result['points_earned'],
                "message": "Activity logged"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to log activity: {str(e)}")
        finally:
            cursor.close()
    
    def list_sessions(self, user_id: int, class_id: Optional[int],
                     start_date: Optional[str], end_date: Optional[str],
                     limit: int) -> Dict[str, Any]:
        """Get user's study sessions with filters"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Build query
            query = """
                SELECT s.*, c.name as class_name
                FROM study_sessions s
                LEFT JOIN classes c ON s.class_id = c.id
                WHERE s.user_id = %s
            """
            params = [user_id]
            
            if class_id:
                query += " AND s.class_id = %s"
                params.append(class_id)
            
            if start_date:
                query += " AND s.start_time >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND s.start_time <= %s"
                params.append(end_date)
            
            query += " ORDER BY s.start_time DESC LIMIT %s"
            params.append(limit)
            
            cursor.execute(query, params)
            sessions = cursor.fetchall()
            
            # Get total stats
            stats_query = """
                SELECT 
                    COUNT(*) as total_count,
                    COALESCE(SUM(duration_minutes), 0) as total_minutes,
                    COALESCE(AVG(duration_minutes), 0) as avg_duration
                FROM study_sessions
                WHERE user_id = %s AND end_time IS NOT NULL
            """
            stats_params = [user_id]
            
            if class_id:
                stats_query += " AND class_id = %s"
                stats_params.append(class_id)
            
            cursor.execute(stats_query, stats_params)
            stats = cursor.fetchone()
            
            return {
                "sessions": sessions,
                "total_count": stats['total_count'],
                "total_minutes": int(stats['total_minutes']),
                "avg_duration": int(stats['avg_duration']) if stats['avg_duration'] else None
            }
        finally:
            cursor.close()
    
    def _award_points(self, user_id: int, points: int, 
                     reason: str, reference_id: int):
        """Award points via gamification service"""
        try:
            response = requests.post(
                f"{settings.gamification_service_url}/api/gamification/points/award",
                json={
                    "user_id": user_id,
                    "points": points,
                    "reason": reason,
                    "reference_type": "study_session",
                    "reference_id": reference_id
                },
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            # Log error but don't fail the session end
            print(f"Warning: Failed to award points: {e}")
