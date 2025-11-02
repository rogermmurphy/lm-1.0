"""
Speech-to-Text Service - Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TranscriptionJobResponse(BaseModel):
    """Transcription job response"""
    job_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TranscriptionResponse(BaseModel):
    """Transcription result response"""
    id: int
    job_id: int
    text: str
    confidence: Optional[float]
    language: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
