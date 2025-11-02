"""
Authentication Service - Auth Routes
API endpoints for authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib

from lm_common.database import get_db
from lm_common.auth import password_utils, jwt_utils
from lm_common.redis_client import get_redis_client

from ..models import User, RefreshToken
from ..schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenRefreshRequest,
    TokenResponse,
    UserResponse,
    MessageResponse
)
from ..config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - **email**: User email address
    - **password**: User password (min 8 characters, must meet strength requirements)
    - **username**: Optional username
    - **full_name**: Optional full name
    """
    # Validate email format
    is_valid_email, error = password_utils.validate_email(request.email)
    if not is_valid_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Validate password strength
    is_valid_password, error = password_utils.validate_password_strength(request.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists (if provided)
    if request.username:
        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
    
    # Hash password
    password_hash = password_utils.hash_password(request.password)
    
    # Create user
    new_user = User(
        email=request.email,
        password_hash=password_hash,
        username=request.username,
        full_name=request.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login and receive JWT tokens
    
    - **email**: User email
    - **password**: User password
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Verify password
    if not user.password_hash or not password_utils.verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    access_token = jwt_utils.create_access_token(
        user_id=user.id,
        email=user.email,
        secret_key=settings.JWT_SECRET_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    refresh_token = jwt_utils.create_refresh_token(
        user_id=user.id,
        secret_key=settings.JWT_SECRET_KEY,
        expires_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    # Store refresh token in database
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(db_refresh_token)
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    # Verify refresh token
    user_id = jwt_utils.verify_refresh_token(
        request.refresh_token,
        secret_key=settings.JWT_SECRET_KEY
    )
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # Check if token exists and is not revoked
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or revoked"
        )
    
    # Check if token is expired
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Generate new access token
    access_token = jwt_utils.create_access_token(
        user_id=user.id,
        email=user.email,
        secret_key=settings.JWT_SECRET_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=request.refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Logout by revoking refresh token
    
    - **refresh_token**: Refresh token to revoke
    """
    # Revoke refresh token
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).first()
    
    if db_token:
        db_token.revoked = True
        db_token.revoked_at = datetime.utcnow()
        db.commit()
    
    return MessageResponse(message="Logged out successfully")
