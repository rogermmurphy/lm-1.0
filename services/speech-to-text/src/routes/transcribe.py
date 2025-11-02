"""
Speech-to-Text Service - Transcribe Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import os

from lm_common.database import get_db
from lm_common.redis_client import queue_push

from ..models import TranscriptionJob, Transcription
from ..schemas import TranscriptionJobResponse, TranscriptionResponse
from ..config import settings

router = APIRouter(prefix="/transcribe", tags=["transcription"])


@router.post("/", response_model=TranscriptionJobResponse)
async def create_transcription_job(
    file: UploadFile = File(...),
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Upload audio file and create transcription job"""
    # Validate file type
    allowed_types = ['audio/mpeg', 'audio/wav', 'audio/mp3', 'audio/m4a', 'audio/flac']
    if file.content_type not in allowed_types and not file.filename.endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
        raise HTTPException(status_code=400, detail="Invalid audio file type")
    
    # Save file
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"audio_{datetime.utcnow().timestamp()}_{file.filename}")
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create job
    job = TranscriptionJob(
        user_id=1,  # TODO: Get from JWT
        audio_file_path=file_path,
        audio_file_size=len(content),
        status='pending'
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Queue for processing
    queue_push("transcription_jobs", {"job_id": job.id, "file_path": file_path, "language": language})
    
    return TranscriptionJobResponse(job_id=job.id, status=job.status, created_at=job.created_at)


@router.get("/jobs/{job_id}", response_model=TranscriptionJobResponse)
async def get_job_status(job_id: int, db: Session = Depends(get_db)):
    """Get transcription job status"""
    job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return TranscriptionJobResponse(job_id=job.id, status=job.status, created_at=job.created_at)


@router.get("/results/{job_id}", response_model=TranscriptionResponse)
async def get_transcription(job_id: int, db: Session = Depends(get_db)):
    """Get completed transcription"""
    transcription = db.query(Transcription).filter(Transcription.job_id == job_id).first()
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found or not complete")
    return transcription
