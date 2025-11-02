"""
Text-to-Speech Service - Generate Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import os

from lm_common.database import get_db
from ..models import TTSAudioFile
from ..services.azure_tts import AzureTTSService
from ..config import settings

router = APIRouter(prefix="/tts", tags=["text-to-speech"])
tts_service = AzureTTSService()


@router.post("/generate")
async def generate_speech(text: str, voice: str = None, db: Session = Depends(get_db)):
    """Generate speech from text using Azure TTS"""
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    output_file = os.path.join(settings.AUDIO_DIR, f"tts_{datetime.utcnow().timestamp()}.wav")
    
    success = tts_service.synthesize(text, output_file, voice)
    if not success:
        raise HTTPException(status_code=500, detail="TTS generation failed")
    
    audio_file = TTSAudioFile(
        user_id=1,
        text=text,
        voice=voice or settings.DEFAULT_VOICE,
        provider="azure",
        file_path=output_file,
        file_size=os.path.getsize(output_file)
    )
    db.add(audio_file)
    db.commit()
    
    return {"id": audio_file.id, "file_path": output_file, "provider": "azure"}
