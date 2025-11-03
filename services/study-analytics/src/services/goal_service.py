"""
Goal management business logic
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date
from typing import Optional, Dict, Any
from decimal import Decimal

class GoalService:
    """Service for managing study goals"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def create_goal(self, user_id: int, class_id: Optional[int],
                   goal_type: str, goal_name: str, goal_description: Optional[str],
                   target_value: Decimal, unit: Optional[str],
                   start_date: date, target_date: date,
                   priority: str, is_recurring: bool,
                   recurrence_pattern: Optional[str],
                   reminder_enabled: bool) -> Dict[str, Any]:
        """Create a new study goal"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                INSERT INTO study_goals
                (user_id, class_id, goal_type, goal_name, goal_description,
                 target_value, unit, start_date, target_date, priority,
                 is_recurring, recurrence_pattern, reminder_enabled)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, status, current_value
            """, (user_id, class_id, goal_type, goal_name, goal_description,
                  target_value, unit, start_date, target_date, priority,
                  is_recurring, recurrence_pattern, reminder_enabled))
            
            result = cursor.fetchone()
            self.conn.commit()
            
            return {
                "goal_id": result['id'],
                "status": result['status'],
                "current_value": float(result['current_value']),
                "percentage_complete": 0,
                "message": "Goal created successfully"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to create goal: {str(e)}")
        finally:
            cursor.close()
    
    def list_goals(self, user_id: int, status: Optional[str],
                  class_id: Optional[int]) -> Dict[str, Any]:
        """Get user's study goals"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            query = "SELECT * FROM active_goals_with_progress WHERE user_id = %s"
            params = [user_id]
            
            if status:
                query = """
                    SELECT g.*, 
                           (g.current_value / g.target_value * 100) as percentage_complete,
                           (g.target_date - CURRENT_DATE) as days_remaining
                    FROM study_goals g
                    WHERE g.user_id = %s AND g.status = %s
                """
                params.append(status)
            
            if class_id:
                query += " AND class_id = %s"
                params.append(class_id)
            
            query += " ORDER BY priority DESC, target_date ASC"
            
            cursor.execute(query, params)
            goals = cursor.fetchall()
            
            # Calculate stats
            active_count = sum(1 for g in goals if g.get('status') == 'active')
            completed_count = sum(1 for g in goals if g.get('status') == 'completed')
            
            return {
                "goals": goals,
                "total_count": len(goals),
                "active_count": active_count,
                "completed_count": completed_count
            }
        finally:
            cursor.close()
    
    def update_goal(self, goal_id: int, user_id: int,
                   updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a study goal"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Build update query
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                if value is not None:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)
            
            if not set_clauses:
                raise Exception("No updates provided")
            
            set_clauses.append("updated_at = NOW()")
            params.extend([goal_id, user_id])
            
            query = f"""
                UPDATE study_goals
                SET {', '.join(set_clauses)}
                WHERE id = %s AND user_id = %s
                RETURNING id
            """
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            if not result:
                raise Exception("Goal not found")
            
            self.conn.commit()
            
            return {
                "goal_id": goal_id,
                "message": "Goal updated successfully"
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to update goal: {str(e)}")
        finally:
            cursor.close()
    
    def record_progress(self, goal_id: int, user_id: int,
                       progress_value: Decimal, notes: Optional[str]) -> Dict[str, Any]:
        """Record progress toward a goal"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            # Verify goal belongs to user
            cursor.execute("""
                SELECT id, target_value FROM study_goals
                WHERE id = %s AND user_id = %s
            """, (goal_id, user_id))
            
            goal = cursor.fetchone()
            if not goal:
                raise Exception("Goal not found")
            
            # Insert progress
            cursor.execute("""
                INSERT INTO goal_progress
                (goal_id, recorded_date, progress_value, notes)
                VALUES (%s, CURRENT_DATE, %s, %s)
                ON CONFLICT (goal_id, recorded_date)
                DO UPDATE SET progress_value = EXCLUDED.progress_value,
                             notes = EXCLUDED.notes
                RETURNING id, percentage_complete, milestone_reached, milestone_name
            """, (goal_id, progress_value, notes))
            
            result = cursor.fetchone()
            self.conn.commit()
            
            return {
                "goal_id": goal_id,
                "percentage_complete": float(result['percentage_complete']) if result['percentage_complete'] else 0,
                "milestone_reached": result['milestone_reached'],
                "milestone_name": result['milestone_name']
            }
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to record progress: {str(e)}")
        finally:
            cursor.close()
    
    def delete_goal(self, goal_id: int, user_id: int) -> Dict[str, Any]:
        """Delete a study goal"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                DELETE FROM study_goals
                WHERE id = %s AND user_id = %s
                RETURNING id
            """, (goal_id, user_id))
            
            result = cursor.fetchone()
            if not result:
                raise Exception("Goal not found")
            
            self.conn.commit()
            
            return {"message": "Goal deleted successfully"}
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to delete goal: {str(e)}")
        finally:
            cursor.close()
