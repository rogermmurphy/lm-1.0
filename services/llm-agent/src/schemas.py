"""
LLM Agent Service - Request/Response Schemas
Pydantic models for API validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Request Schemas
class ChatMessageRequest(BaseModel):
    """Chat message request"""
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=5000)
    use_rag: bool = True


class StudyMaterialUploadRequest(BaseModel):
    """Study material upload request"""
    title: str = Field(min_length=1, max_length=500)
    content: str = Field(min_length=1)
    subject: Optional[str] = Field(None, max_length=100)


# Response Schemas
class ChatMessageResponse(BaseModel):
    """Chat message response"""
    conversation_id: int
    message_id: int
    response: str
    sources: Optional[List[str]] = None
    created_at: datetime


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: int
    title: Optional[str]
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StudyMaterialResponse(BaseModel):
    """Study material response"""
    id: int
    title: str
    subject: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MaterialsListResponse(BaseModel):
    """Materials list response with preview"""
    id: int
    title: str
    subject: Optional[str]
    content_preview: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
