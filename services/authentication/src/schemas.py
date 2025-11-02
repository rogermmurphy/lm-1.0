"""
Authentication Service - Request/Response Schemas
Pydantic models for API validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Request Schemas
class UserRegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(min_length=8, description="Password (min 8 characters)")
    username: Optional[str] = Field(None, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str


# Response Schemas
class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class UserResponse(BaseModel):
    """User data response"""
    id: int
    email: str
    username: Optional[str]
    full_name: Optional[str]
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
