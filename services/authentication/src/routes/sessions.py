"""
Authentication Service - Session Management Routes
API endpoints for session management and monitoring
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from lm_common.database import get_db
from lm_common.auth.jwt_utils import verify_token

from ..models import User
from ..schemas import SessionResponse, MessageResponse
from ..services.session_manager import get_session_manager

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Get session manager instance
session_manager = get_session_manager()


@router.get("/active", response_model=List[SessionResponse])
async def get_active_sessions(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get all active sessions for the current user
    Requires authentication
    """
    # Get user from JWT token in Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    user_id = payload.get('sub')
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Get user's active sessions
    sessions = session_manager.get_user_sessions(int(user_id))
    
    return [
        SessionResponse(
            session_id=s['session_id'],
            user_id=s['user_id'],
            created_at=s['created_at'],
            expires_at=s['expires_at'],
            last_activity=s['last_activity'],
            device_info=s.get('device_info', {})
        )
        for s in sessions
    ]


@router.delete("/{session_id}", response_model=MessageResponse)
async def terminate_session(
    session_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Terminate a specific session
    Requires authentication - can only terminate own sessions
    """
    # Get user from JWT token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    user_id = payload.get('sub')
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Get session to verify ownership
    session_data = session_manager.get_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify user owns this session
    if session_data['user_id'] != int(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot terminate another user's session"
        )
    
    # Terminate session
    session_manager.terminate_session(session_id)
    
    return MessageResponse(message="Session terminated successfully")


@router.delete("/all", response_model=MessageResponse)
async def terminate_all_sessions(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Terminate all sessions for the current user
    Useful for "log out from all devices"
    """
    # Get user from JWT token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token = auth_header.split(' ')[1]
    payload = verify_token(token)
    user_id = payload.get('sub')
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Terminate all user sessions
    count = session_manager.terminate_all_user_sessions(int(user_id))
    
    return MessageResponse(
        message=f"Terminated {count} session(s)"
    )


@router.get("/validate/{session_id}", response_model=MessageResponse)
async def validate_session(session_id: str):
    """
    Validate if a session is active
    Public endpoint for session validation
    """
    is_valid = session_manager.validate_session(session_id)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or expired"
        )
    
    return MessageResponse(message="Session is valid")
