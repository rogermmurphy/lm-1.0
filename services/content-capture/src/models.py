"""
Content Capture Service - Database Models
SQLAlchemy models for photos, textbooks, and chunks
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Photo(Base):
    """Photo model for captured images with OCR"""
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    image_url = Column(Text, nullable=False)
    extracted_text = Column(Text, nullable=True)
    extraction_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    vector_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TextbookDownload(Base):
    """Textbook download model"""
    __tablename__ = "textbook_downloads"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=True)
    isbn = Column(String(20), nullable=True)
    file_url = Column(Text, nullable=False)
    file_type = Column(String(20), default="pdf")
    file_size_bytes = Column(BigInteger, nullable=True)
    page_count = Column(Integer, nullable=True)
    total_chunks = Column(Integer, default=0)
    embedding_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to chunks
    chunks = relationship("TextbookChunk", back_populates="textbook", cascade="all, delete-orphan")

class TextbookChunk(Base):
    """Textbook chunk model for vector search"""
    __tablename__ = "textbook_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    textbook_id = Column(Integer, ForeignKey("textbook_downloads.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    vector_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to textbook
    textbook = relationship("TextbookDownload", back_populates="chunks")

# Enhanced audio files model (extending existing table)
class AudioFile(Base):
    """Enhanced audio file model with class association"""
    __tablename__ = "audio_files"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)  # New field
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(BigInteger, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    transcription_id = Column(Integer, ForeignKey("transcriptions.id"), nullable=True)
    vector_id = Column(String(100), nullable=True)  # New field
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
