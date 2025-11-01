#!/usr/bin/env python3
"""
Async Transcription Tool - Queues speech-to-text transcription jobs
Returns immediately while job processes in background
"""

import psycopg2
import redis
import json
import uuid
import os
from datetime import datetime
from typing import Dict, Optional

class AsyncTranscriptionTool:
    def __init__(self, 
                 postgres_host="localhost",
                 postgres_port=5432,
                 postgres_db="lm_dev",
                 postgres_user="postgres",
                 postgres_password="postgres",
                 redis_host="localhost",
                 redis_port=6379):
        """Initialize connections to PostgreSQL and Redis"""
        
        # Connect to PostgreSQL
        self.pg_conn = psycopg2.connect(
            host=postgres_host,
            port=postgres_port,
            database=postgres_db,
            user=postgres_user,
            password=postgres_password
        )
        print(f"[OK] Connected to PostgreSQL")
        
        # Connect to Redis
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        print(f"[OK] Connected to Redis")
    
    def transcribe_audio_async(self, 
                               file_path: str,
                               user_id: str = "default_user",
                               auto_load_to_chromadb: bool = True,
                               subject: str = "default") -> Dict:
        """
        Queue an audio transcription job
        Returns immediately with job ID
        
        Args:
            file_path: Path to audio file
            user_id: User ID for tracking
            auto_load_to_chromadb: Auto-load transcript to ChromaDB for RAG
            subject: Subject category for organization
            
        Returns:
            Dictionary with job information
        """
        
        # Validate file exists
        if not os.path.exists(file_path):
            return {
                'error': 'File not found',
                'path': file_path
            }
        
        # Get file info
        file_name = os.path.basename(file_path)
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Insert into database
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            INSERT INTO transcription_jobs 
                (id, user_id, file_name, file_path, status, 
                 auto_load_to_chromadb, subject, created_at)
            VALUES 
                (%s, %s, %s, %s, 'pending', %s, %s, %s)
        """, (job_id, user_id, file_name, file_path, 
              auto_load_to_chromadb, subject, datetime.now()))
        self.pg_conn.commit()
        cursor.close()
        
        print(f"[DB] Created job record: {job_id}")
        
        # Queue job in Redis
        job_data = {
            'job_id': job_id,
            'file_path': file_path,
            'file_name': file_name,
            'user_id': user_id,
            'auto_load_to_chromadb': auto_load_to_chromadb,
            'subject': subject
        }
        self.redis_client.rpush('transcription_queue', json.dumps(job_data))
        
        print(f"[QUEUE] Job queued for processing")
        
        return {
            'job_id': job_id,
            'status': 'pending',
            'file_name': file_name,
            'file_size_mb': round(file_size_mb, 2),
            'message': f'Started transcribing "{file_name}"',
            'check_status': f'/api/transcriptions/{job_id}',
            'estimated_time': 'Approximately 10-20 minutes for 1 hour audio'
        }
    
    def get_job_status(self, job_id: str) -> Dict:
        """Get status of a transcription job"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT id, file_name, status, transcript_text, duration_seconds, 
                   language, loaded_to_chromadb, chromadb_collection,
                   error_message, created_at, started_at, completed_at
            FROM transcription_jobs
            WHERE id = %s
        """, (job_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return {'error': 'Job not found'}
        
        result = {
            'job_id': row[0],
            'file_name': row[1],
            'status': row[2],
            'transcript': row[3][:500] + '...' if row[3] and len(row[3]) > 500 else row[3],
            'full_transcript_available': row[3] is not None,
            'duration_seconds': row[4],
            'language': row[5],
            'loaded_to_chromadb': row[6],
            'chromadb_collection': row[7],
            'error': row[8],
            'created_at': str(row[9]),
            'started_at': str(row[10]) if row[10] else None,
            'completed_at': str(row[11]) if row[11] else None
        }
        
        # Add processing time if completed
        if row[10] and row[11]:  # started_at and completed_at
            processing_seconds = (row[11] - row[10]).total_seconds()
            result['processing_time_seconds'] = round(processing_seconds, 1)
        
        return result
    
    def get_full_transcript(self, job_id: str) -> Dict:
        """Get the complete transcript text"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT file_name, transcript_text, language, duration_seconds, status
            FROM transcription_jobs
            WHERE id = %s
        """, (job_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return {'error': 'Job not found'}
        
        if row[4] != 'completed':
            return {
                'error': 'Transcription not complete',
                'status': row[4]
            }
        
        return {
            'job_id': job_id,
            'file_name': row[0],
            'transcript': row[1],
            'language': row[2],
            'duration_seconds': row[3],
            'word_count': len(row[1].split()) if row[1] else 0
        }
    
    def list_transcriptions(self, 
                           subject: Optional[str] = None, 
                           status: Optional[str] = None,
                           limit: int = 50) -> list:
        """
        List transcriptions with optional filters
        
        Args:
            subject: Filter by subject category
            status: Filter by status (pending, processing, completed, failed)
            limit: Maximum number of results
        """
        cursor = self.pg_conn.cursor()
        
        # Build query based on filters
        query = """
            SELECT id, file_name, status, subject, duration_seconds, 
                   language, loaded_to_chromadb, created_at, completed_at
            FROM transcription_jobs
            WHERE 1=1
        """
        params = []
        
        if subject:
            query += " AND subject = %s"
            params.append(subject)
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        
        return [{
            'job_id': row[0],
            'file_name': row[1],
            'status': row[2],
            'subject': row[3],
            'duration_seconds': row[4],
            'language': row[5],
            'loaded_to_chromadb': row[6],
            'created_at': str(row[7]),
            'completed_at': str(row[8]) if row[8] else None
        } for row in rows]
    
    def update_subject(self, job_id: str, subject: str) -> Dict:
        """Update subject category for a transcription"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            UPDATE transcription_jobs
            SET subject = %s
            WHERE id = %s
        """, (subject, job_id))
        self.pg_conn.commit()
        cursor.close()
        
        return {'job_id': job_id, 'subject': subject}
    
    def delete_transcription(self, job_id: str) -> Dict:
        """Delete a transcription job"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            DELETE FROM transcription_jobs
            WHERE id = %s
        """, (job_id,))
        self.pg_conn.commit()
        deleted = cursor.rowcount > 0
        cursor.close()
        
        if deleted:
            return {'job_id': job_id, 'deleted': True}
        else:
            return {'error': 'Job not found'}


if __name__ == "__main__":
    # Test the async tool
    print("\n" + "="*70)
    print("ASYNC TRANSCRIPTION TOOL TEST")
    print("="*70)
    
    tool = AsyncTranscriptionTool()
    
    # Example: Queue a transcription job
    # Replace with actual audio file path to test
    print("\nTo test transcription:")
    print("1. Place an audio file in this directory")
    print("2. Update the file path below")
    print("3. Run this script")
    print("\nExample usage:")
    print("  result = tool.transcribe_audio_async('lecture.mp3')")
    print("  print(json.dumps(result, indent=2))")
    print("\n  status = tool.get_job_status(result['job_id'])")
    print("  print(json.dumps(status, indent=2))")
    
    # List all transcriptions
    print("\n" + "="*70)
    print("LISTING ALL TRANSCRIPTIONS:")
    print("="*70)
    transcriptions = tool.list_transcriptions()
    if transcriptions:
        print(json.dumps(transcriptions, indent=2))
    else:
        print("No transcriptions found")
