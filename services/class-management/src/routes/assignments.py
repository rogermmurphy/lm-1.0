"""
Assignment CRUD API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

from models import Assignment, AssignmentCreate, AssignmentUpdate
from config import settings
from lm_common.auth.jwt_utils import get_current_user

router = APIRouter(prefix="/assignments", tags=["assignments"])


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(settings.database_url, cursor_factory=RealDictCursor)


@router.post("", response_model=Assignment, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new assignment"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Verify class belongs to user
        cur.execute("""
            SELECT id FROM classes 
            WHERE id = %s AND user_id = %s
        """, (assignment_data.class_id, current_user["user_id"]))
        
        if not cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        cur.execute("""
            INSERT INTO assignments (
                class_id, user_id, title, type, description,
                due_date, status, priority
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            assignment_data.class_id,
            current_user["user_id"],
            assignment_data.title,
            assignment_data.type,
            assignment_data.description,
            assignment_data.due_date,
            assignment_data.status,
            assignment_data.priority
        ))
        
        new_assignment = cur.fetchone()
        conn.commit()
        return new_assignment
        
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()


@router.get("", response_model=List[Assignment])
async def list_assignments(
    class_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    """List assignments with optional filters"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        query = "SELECT * FROM assignments WHERE user_id = %s"
        params = [current_user["user_id"]]
        
        if class_id:
            query += " AND class_id = %s"
            params.append(class_id)
        
        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
        
        query += " ORDER BY due_date ASC"
        
        cur.execute(query, params)
        assignments = cur.fetchall()
        return assignments
        
    finally:
        cur.close()
        conn.close()


@router.get("/upcoming", response_model=List[Assignment])
async def get_upcoming_assignments(
    days: int = Query(7, ge=1, le=30),
    current_user: dict = Depends(get_current_user)
):
    """Get upcoming assignments within specified days"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM assignments 
            WHERE user_id = %s 
            AND due_date BETWEEN NOW() AND NOW() + INTERVAL '%s days'
            AND status != 'completed'
            ORDER BY due_date ASC
        """, (current_user["user_id"], days))
        
        assignments = cur.fetchall()
        return assignments
        
    finally:
        cur.close()
        conn.close()


@router.get("/{assignment_id}", response_model=Assignment)
async def get_assignment(
    assignment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific assignment"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT * FROM assignments 
            WHERE id = %s AND user_id = %s
        """, (assignment_id, current_user["user_id"]))
        
        assignment = cur.fetchone()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        return assignment
        
    finally:
        cur.close()
        conn.close()


@router.put("/{assignment_id}", response_model=Assignment)
async def update_assignment(
    assignment_id: int,
    assignment_update: AssignmentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update an assignment"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Check if assignment exists and belongs to user
        cur.execute("""
            SELECT id FROM assignments 
            WHERE id = %s AND user_id = %s
        """, (assignment_id, current_user["user_id"]))
        
        if not cur.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Build update query dynamically
        update_fields = []
        update_values = []
        
        for field, value in assignment_update.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            update_values.append(value)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_values.append(assignment_id)
        update_values.append(current_user["user_id"])
        
        query = f"""
            UPDATE assignments 
            SET {', '.join(update_fields)}
            WHERE id = %s AND user_id = %s
            RETURNING *
        """
        
        cur.execute(query, update_values)
        updated_assignment = cur.fetchone()
        conn.commit()
        
        return updated_assignment
        
    except psycopg2.Error as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()


@router.patch("/{assignment_id}/status", response_model=Assignment)
async def update_assignment_status(
    assignment_id: int,
    new_status: str = Query(..., pattern="^(pending|in-progress|completed|overdue)$"),
    current_user: dict = Depends(get_current_user)
):
    """Update assignment status"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE assignments 
            SET status = %s
            WHERE id = %s AND user_id = %s
            RETURNING *
        """, (new_status, assignment_id, current_user["user_id"]))
        
        updated_assignment = cur.fetchone()
        
        if not updated_assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        conn.commit()
        return updated_assignment
        
    finally:
        cur.close()
        conn.close()


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete an assignment"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            DELETE FROM assignments 
            WHERE id = %s AND user_id = %s
            RETURNING id
        """, (assignment_id, current_user["user_id"]))
        
        deleted = cur.fetchone()
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        conn.commit()
        
    finally:
        cur.close()
        conn.close()
