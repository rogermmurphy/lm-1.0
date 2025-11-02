"""
Audio Recording Service - Main Application
File upload service for audio recordings
"""
from fastapi import FastAPI, UploadFile, File, Depends
# from fastapi.middleware.cors import CORSMiddleware  # CORS handled by nginx gateway
from sqlalchemy.orm import Session
from lm_common.logging import setup_logging, get_logger
from lm_common.database import get_db
from .config import settings
from .models import Recording
import os
from datetime import datetime

setup_logging(service_name=settings.SERVICE_NAME, level=settings.LOG_LEVEL)
logger = get_logger(__name__)

app = FastAPI(title="Little Monster Audio Recording Service", version="1.0.0")
# CORS middleware - DISABLED: CORS is handled by nginx API gateway
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/upload")
async def upload_recording(file: UploadFile = File(...), recording_type: str = "lecture", db: Session = Depends(get_db)):
    """Upload audio recording"""
    os.makedirs(settings.RECORDINGS_DIR, exist_ok=True)
    file_path = os.path.join(settings.RECORDINGS_DIR, f"rec_{datetime.utcnow().timestamp()}_{file.filename}")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    recording = Recording(user_id=1, file_path=file_path, file_size=len(content), recording_type=recording_type)
    db.add(recording)
    db.commit()
    
    return {"id": recording.id, "file_path": file_path}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}
