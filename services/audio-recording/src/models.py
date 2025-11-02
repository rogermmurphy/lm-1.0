"""
Audio Recording Service - Database Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from lm_common.database import Base


class Recording(Base):
    """Recording model"""
    __tablename__ = 'recordings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    duration = Column(Float)
    recording_type = Column(String(50), default='other', index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Recording(id={self.id}, type='{self.recording_type}')>"
