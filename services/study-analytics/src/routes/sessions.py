"""
Study session management routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import date
import psycopg2
from ..config import settings
from ..models import (
    SessionStart, SessionEnd, ActivityLog,
    SessionsListResponse, MessageResponse
)
from ..services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])

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

@router.post("/start")
async def start_session(
    session_data: SessionStart,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Start a new study session"""
    try:
        service = SessionService(conn)
        result = service.start_session(
            user_id=current_user["user_id"],
            class_id=session_data.class_id,
            session_type=session_data.session_type,
            focus_mode=session_data.focus_mode,
            location=session_data.location
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{session_id}/end")
async def end_session(
    session_id: int,
    session_data: SessionEnd,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """End an active study session"""
    try:
        service = SessionService(conn)
        result = service.end_session(
            session_id=session_id,
            user_id=current_user["user_id"],
            mood_rating=session_data.mood_rating,
            productivity_rating=session_data.productivity_rating,
            notes=session_data.notes
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{session_id}/activities")
async def log_activity(
    session_id: int,
    activity: ActivityLog,
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Log an activity within a session"""
    try:
        service = SessionService(conn)
        result = service.log_activity(
            session_id=session_id,
            user_id=current_user["user_id"],
            activity_type=activity.activity_type,
            content_type=activity.content_type,
            content_id=activity.content_id,
            items_completed=activity.items_completed,
            items_correct=activity.items_correct,
            duration_minutes=activity.duration_minutes,
            metadata=activity.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=SessionsListResponse)
async def list_sessions(
    class_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(50, le=100),
    current_user: dict = Depends(get_current_user),
    conn = Depends(get_db)
):
    """Get user's study sessions with filters"""
    try:
        service = SessionService(conn)
        result = service.list_sessions(
            user_id=current_user["user_id"],
            class_id=class_id,
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None,
            limit=limit
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
