"""
Study goal management routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import psycopg2
from ..config import settings
from ..models import (
    GoalCreate, GoalUpdate, GoalProgressRecord,
    GoalsListResponse, MessageResponse
)
from ..services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])

def get_db():
    """Database connection dependency"""
    conn = psycopg2.connect(settings.database_url)
    try:
        yield conn
    finally:
        conn.close()

def get_current_user():
    """Mock user for testing - replace with JWT auth"""
    return {"user_id": 7, "email": "testuser@test.com"}

@router.post("")
async def create_goal(
    goal_data: GoalCreate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Create a new study goal"""
    try:
        service = GoalService(conn)
        result = service.create_goal(
            user_id=current_user["user_id"],
            class_id=goal_data.class_id,
            goal_type=goal_data.goal_type,
            goal_name=goal_data.goal_name,
            goal_description=goal_data.goal_description,
            target_value=goal_data.target_value,
            unit=goal_data.unit,
            start_date=goal_data.start_date,
            target_date=goal_data.target_date,
            priority=goal_data.priority,
            is_recurring=goal_data.is_recurring,
            recurrence_pattern=goal_data.recurrence_pattern,
            reminder_enabled=goal_data.reminder_enabled
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=GoalsListResponse)
async def list_goals(
    status: Optional[str] = Query(None),
    class_id: Optional[int] = Query(None),
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Get user's study goals"""
    try:
        service = GoalService(conn)
        result = service.list_goals(
            user_id=current_user["user_id"],
            status=status,
            class_id=class_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{goal_id}")
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Update a study goal"""
    try:
        service = GoalService(conn)
        updates = goal_data.model_dump(exclude_unset=True)
        result = service.update_goal(
            goal_id=goal_id,
            user_id=current_user["user_id"],
            updates=updates
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{goal_id}/progress")
async def record_progress(
    goal_id: int,
    progress_data: GoalProgressRecord,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Record progress toward a goal"""
    try:
        service = GoalService(conn)
        result = service.record_progress(
            goal_id=goal_id,
            user_id=current_user["user_id"],
            progress_value=progress_data.progress_value,
            notes=progress_data.notes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Delete a study goal"""
    try:
        service = GoalService(conn)
        result = service.delete_goal(
            goal_id=goal_id,
            user_id=current_user["user_id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
