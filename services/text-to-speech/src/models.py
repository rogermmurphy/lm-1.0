"""
Text-to-Speech Service - Database Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from lm_common.database import Base


class TTSAudioFile(Base):
    """TTS generated audio file model"""
    __tablename__ = 'tts_audio_files'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True, index=True)  # Removed ForeignKey - users table not yet set up
    text = Column(Text, nullable=False)
    voice = Column(String(100))
    provider = Column(String(50), index=True)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    duration = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<TTSAudioFile(id={self.id}, provider='{self.provider}')>"
