"""
Speech-to-Text Service - Database Models
SQLAlchemy ORM models for transcription jobs
Extracted from POC 09 schema
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from lm_common.database import Base


class TranscriptionJob(Base):
    """Transcription job model"""
    __tablename__ = 'transcription_jobs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    audio_file_path = Column(String(500), nullable=False)
    audio_file_size = Column(Integer)
    audio_duration = Column(Float)
    status = Column(String(50), default='pending', index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    # Relationship
    transcription = relationship("Transcription", back_populates="job", uselist=False)
    
    def __repr__(self):
        return f"<TranscriptionJob(id={self.id}, status='{self.status}')>"


class Transcription(Base):
    """Completed transcription model"""
    __tablename__ = 'transcriptions'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('transcription_jobs.id', ondelete='CASCADE'), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    text = Column(Text, nullable=False)
    confidence = Column(Float)
    language = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    job = relationship("TranscriptionJob", back_populates="transcription")
    
    def __repr__(self):
        return f"<Transcription(id={self.id}, job_id={self.job_id})>"
