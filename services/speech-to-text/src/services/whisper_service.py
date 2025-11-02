"""
Speech-to-Text Service - Whisper Service
Extracted from POC 09 transcription_engine.py - Validated
"""
import os
from faster_whisper import WhisperModel
from typing import Dict, Optional
from ..config import settings


class WhisperService:
    """Whisper transcription service using faster-whisper"""
    
    def __init__(self):
        """Initialize Whisper model"""
        self.model_size = settings.WHISPER_MODEL_SIZE
        self.model = None
    
    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            self.model = WhisperModel(self.model_size, device="cpu")
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> Dict:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            language: Language code or None for auto-detect
            
        Returns:
            Dict with text, language, duration, confidence
        """
        self.load_model()
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5
        )
        
        # Collect segments
        transcript_text = ""
        for segment in segments:
            transcript_text += segment.text + " "
        
        return {
            'text': transcript_text.strip(),
            'language': info.language,
            'confidence': round(info.language_probability, 2),
            'duration': round(info.duration, 2)
        }
