"""
Class CRUD API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

from ..models import Class, ClassCreate, ClassUpdate
from ..config import settings
# REMOVED: Auth not used in current system design (matches Chat, Flashcards, Groups pattern)
# from lm_common.auth.jwt_utils import get_current_user

router = APIRouter(prefix="/classes", tags=["classes"])


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)


@router.post("", response_model=Class, status_code=status.HTTP_201_CREATED)
async def create_class(
    class_data: ClassCreate
):
    """Create a new class"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO classes (
                user_id, name, teacher_name, period, color, 
                subject, current_grade, grade_percent
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            user_id,
            class_data.name,
            class_data.teacher_name,
            class_data.period,
            class_data.color,
            class_data.subject,
            class_data.current_grade,
            class_data.grade_percent
        ))
        
        new_class = cur.fetchone()
        conn.commit()
        return new_class
        
    except psycopg2.IntegrityError as e:
        conn.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A class with this name already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()


@router.get("", response_model=List[Class])
async def list_classes():
    """List all classes for the current user"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM classes 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        
        classes = cur.fetchall()
        return classes
        
    finally:
        cur.close()
        conn.close()


@router.get("/{class_id}", response_model=Class)
async def get_class(
    class_id: int
):
    """Get a specific class"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM classes 
            WHERE id = %s AND user_id = %s
        """, (class_id, user_id))
        
        class_data = cur.fetchone()
        
        if not class_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        return class_data
        
    finally:
        cur.close()
        conn.close()


@router.put("/{class_id}", response_model=Class)
async def update_class(
    class_id: int,
    class_update: ClassUpdate
):
    """Update a class"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Check if class exists and belongs to user
        cur.execute("""
            SELECT id FROM classes 
            WHERE id = %s AND user_id = %s
        """, (class_id, user_id))
        
        if not cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        for field, value in class_update.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            update_values.append(value)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_values.append(class_id)
        update_values.append(user_id)
        
        query = f"""
            UPDATE classes 
            SET {', '.join(update_fields)}
            WHERE id = %s AND user_id = %s
            RETURNING *
        """
        
        cur.execute(query, update_values)
        updated_class = cur.fetchone()
        conn.commit()
        
        return updated_class
        
    except psycopg2.IntegrityError as e:
        conn.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A class with this name already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: int
):
    """Delete a class"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            DELETE FROM classes 
            WHERE id = %s AND user_id = %s
            RETURNING id
        """, (class_id, user_id))
        
        deleted = cur.fetchone()
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        conn.commit()
        
    finally:
        cur.close()
        conn.close()


@router.get("/{class_id}/dashboard")
async def get_class_dashboard(
    class_id: int
):
    """Get class dashboard with related content"""
    # TODO: Get user_id from JWT token when auth is implemented
    user_id = 1
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Verify class ownership
        cur.execute("""
            SELECT * FROM classes 
            WHERE id = %s AND user_id = %s
        """, (class_id, user_id))
        
        class_data = cur.fetchone()
        
        if not class_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        # Get assignments count
        cur.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN status = 'overdue' THEN 1 ELSE 0 END) as overdue
            FROM assignments 
            WHERE class_id = %s
        """, (class_id,))
        
        assignment_stats = cur.fetchone()
        
        # Get recent assignments
        cur.execute("""
            SELECT * FROM assignments 
            WHERE class_id = %s 
            ORDER BY due_date ASC 
            LIMIT 5
        """, (class_id,))
        
        recent_assignments = cur.fetchall()
        
        # Get upcoming events
        cur.execute("""
            SELECT * FROM planner_events 
            WHERE class_id = %s AND start_time > NOW()
            ORDER BY start_time ASC 
            LIMIT 5
        """, (class_id,))
        
        upcoming_events = cur.fetchall()
        
        return {
            "class": class_data,
            "assignment_stats": assignment_stats,
            "recent_assignments": recent_assignments,
            "upcoming_events": upcoming_events
        }
        
    finally:
        cur.close()
        conn.close()
