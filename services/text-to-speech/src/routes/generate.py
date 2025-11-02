"""
Text-to-Speech Service - Generate Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os
import base64

from lm_common.database import get_db
from ..models import TTSAudioFile
from ..services.azure_rest_tts import AzureRestTTSService
from ..config import settings
from ..schemas import TTSGenerateRequest, TTSGenerateResponse

router = APIRouter(prefix="/tts", tags=["text-to-speech"])
tts_service = AzureRestTTSService()


@router.post("/generate", response_model=TTSGenerateResponse)
async def generate_speech(request: TTSGenerateRequest, db: Session = Depends(get_db)):
    """Generate speech from text using Azure TTS"""
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    output_file = os.path.join(settings.AUDIO_DIR, f"tts_{datetime.utcnow().timestamp()}.wav")
    
    success = tts_service.synthesize(request.text, output_file, request.voice)
    if not success:
        raise HTTPException(status_code=500, detail="TTS generation failed")
    
    # Read audio file and convert to base64
    with open(output_file, "rb") as f:
        audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Skip database write for now - users table not yet set up
    # TODO: Re-enable once authentication is fully integrated
    # audio_file = TTSAudioFile(
    #     user_id=1,
    #     text=request.text,
    #     voice=request.voice or settings.DEFAULT_VOICE,
    #     provider="azure",
    #     file_path=output_file,
    #     file_size=os.path.getsize(output_file)
    # )
    # db.add(audio_file)
    # db.commit()
    # db.refresh(audio_file)
    
    return TTSGenerateResponse(
        id=0,  # Temporary until database write is enabled
        audio_base64=audio_base64,
        provider="azure",
        voice=request.voice or settings.DEFAULT_VOICE
    )
