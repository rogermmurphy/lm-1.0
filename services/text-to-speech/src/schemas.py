"""
Text-to-Speech Service - Request/Response Schemas
"""
from pydantic import BaseModel
from typing import Optional


class TTSGenerateRequest(BaseModel):
    """Request schema for TTS generation"""
    text: str
    voice: Optional[str] = None


class TTSGenerateResponse(BaseModel):
    """Response schema for TTS generation"""
    id: int
    audio_base64: str
    provider: str
    voice: str
