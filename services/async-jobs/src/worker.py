"""
Async Jobs Service - Background Worker
Processes jobs from Redis queue
Extracted from POC 08 - Adapted for transcription
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session
from lm_common.database import get_db_session
from lm_common.redis_client import queue_pop
import sys
sys.path.insert(0, '/app')
from src.models import Job


class JobWorker:
    """Background job processor"""
    
    def __init__(self):
        """Initialize worker"""
        self.running = False
    
    def process_transcription_job(self, job: Job, payload: dict, db: Session):
        """Process transcription job"""
        # Import here to avoid circular dependencies
        import sys
        sys.path.insert(0, "../../speech-to-text/src")
        from services.whisper_service import WhisperService
        
        whisper = WhisperService()
        result = whisper.transcribe(payload['file_path'], payload.get('language'))
        
        # Store result
        from ..models import Transcription, TranscriptionJob
        transcription = Transcription(
            job_id=payload['job_id'],
            user_id=job.user_id or 1,
            text=result['text'],
            confidence=result.get('confidence'),
            language=result.get('language')
        )
        db.add(transcription)
        
        # Update job
        trans_job = db.query(TranscriptionJob).filter(TranscriptionJob.id == payload['job_id']).first()
        if trans_job:
            trans_job.status = 'completed'
            trans_job.completed_at = datetime.utcnow()
        
        return result
    
    def process_job(self, job_data: dict):
        """Process a single job"""
        with get_db_session() as db:
            job_id = job_data.get('job_id')
            job_type = job_data.get('job_type', 'transcription')
            
            # Get or create job
            job = db.query(Job).filter(Job.id == job_id).first() if job_id else None
            if not job:
                job = Job(
                    job_type=job_type,
                    status='processing',
                    payload=json.dumps(job_data),
                    started_at=datetime.utcnow()
                )
                db.add(job)
                db.commit()
            
            try:
                # Route to handler
                if job_type == 'transcription':
                    result = self.process_transcription_job(job, job_data, db)
                else:
                    result = {"error": "Unknown job type"}
                
                # Update job
                job.status = 'completed'
                job.result = json.dumps(result)
                job.completed_at = datetime.utcnow()
                db.commit()
                
            except Exception as e:
                job.status = 'failed'
                job.error_message = str(e)
                job.retry_count += 1
                db.commit()
    
    def run(self):
        """Main worker loop"""
        self.running = True
        print("Job Worker Started - Listening on transcription_jobs queue")
        
        while self.running:
            job = queue_pop("transcription_jobs", timeout=5)
            if job:
                print(f"Processing job: {job}")
                self.process_job(job)


if __name__ == "__main__":
    worker = JobWorker()
    worker.run()
