"""
Async Jobs Service - Database Models
From POC 08 schema
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from lm_common.database import Base


class Job(Base):
    """Async job model"""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), index=True)
    job_type = Column(String(50), nullable=False, index=True)
    status = Column(String(50), default='pending', index=True)
    priority = Column(Integer, default=0, index=True)
    payload = Column(Text)
    result = Column(Text)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Job(id={self.id}, type='{self.job_type}', status='{self.status}')>"
