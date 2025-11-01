#!/usr/bin/env python3
"""
Async Presentation Tool - Queues presentation generation jobs
Returns immediately while job processes in background
"""

import psycopg2
import redis
import json
import uuid
from datetime import datetime

class AsyncPresentationTool:
    def __init__(self, 
                 postgres_host="localhost",
                 postgres_port=5432,
                 postgres_db="lm_dev",
                 postgres_user="postgres",
                 postgres_password="postgres",
                 redis_host="localhost",
                 redis_port=6379):
        """Initialize connections"""
        
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
    
    def create_presentation_async(self, 
                                  topic: str, 
                                  user_id: str = "default_user",
                                  n_slides: int = 5) -> dict:
        """
        Queue a presentation generation job
        Returns immediately with job ID
        """
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Insert into database
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            INSERT INTO presentation_jobs 
                (id, user_id, topic, status, subject, n_slides, created_at)
            VALUES 
                (%s, %s, %s, 'pending', 'default', %s, %s)
        """, (job_id, user_id, topic, n_slides, datetime.now()))
        self.pg_conn.commit()
        cursor.close()
        
        print(f"[DB] Created job record: {job_id}")
        
        # Queue job in Redis
        job_data = {
            'job_id': job_id,
            'topic': topic,
            'n_slides': n_slides,
            'user_id': user_id
        }
        self.redis_client.rpush('presentation_queue', json.dumps(job_data))
        
        print(f"[QUEUE] Job queued for processing")
        
        return {
            'job_id': job_id,
            'status': 'pending',
            'message': f'Started generating presentation on "{topic}"',
            'check_status': f'/api/presentations/{job_id}'
        }
    
    def get_job_status(self, job_id: str) -> dict:
        """Get status of a presentation job"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            SELECT id, topic, status, subject, presenton_id, presenton_url, 
                   error_message, created_at, completed_at
            FROM presentation_jobs
            WHERE id = %s
        """, (job_id,))
        
        row = cursor.fetchone()
        cursor.close()
        
        if not row:
            return {'error': 'Job not found'}
        
        return {
            'job_id': row[0],
            'topic': row[1],
            'status': row[2],
            'subject': row[3],
            'presenton_id': row[4],
            'presenton_url': row[5],
            'error': row[6],
            'created_at': str(row[7]),
            'completed_at': str(row[8]) if row[8] else None
        }
    
    def list_presentations(self, subject: str = None, limit: int = 50) -> list:
        """List presentations, optionally filtered by subject"""
        cursor = self.pg_conn.cursor()
        
        if subject:
            cursor.execute("""
                SELECT id, topic, status, subject, created_at, completed_at
                FROM presentation_jobs
                WHERE subject = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (subject, limit))
        else:
            cursor.execute("""
                SELECT id, topic, status, subject, created_at, completed_at
                FROM presentation_jobs
                ORDER BY created_at DESC
                LIMIT %s
            """, (limit,))
        
        rows = cursor.fetchall()
        cursor.close()
        
        return [{
            'job_id': row[0],
            'topic': row[1],
            'status': row[2],
            'subject': row[3],
            'created_at': str(row[4]),
            'completed_at': str(row[5]) if row[5] else None
        } for row in rows]
    
    def update_subject(self, job_id: str, subject: str):
        """Update subject category for a presentation"""
        cursor = self.pg_conn.cursor()
        cursor.execute("""
            UPDATE presentation_jobs
            SET subject = %s
            WHERE id = %s
        """, (subject, job_id))
        self.pg_conn.commit()
        cursor.close()
        
        return {'job_id': job_id, 'subject': subject}

if __name__ == "__main__":
    # Test the async tool
    tool = AsyncPresentationTool()
    
    # Create a job
    result = tool.create_presentation_async(
        topic="Photosynthesis for Biology Test",
        user_id="test_user"
    )
    
    print("\n" + "="*70)
    print("JOB CREATED:")
    print("="*70)
    print(json.dumps(result, indent=2))
    
    # Check status
    status = tool.get_job_status(result['job_id'])
    print("\n" + "="*70)
    print("JOB STATUS:")
    print("="*70)
    print(json.dumps(status, indent=2))
    
    # List all presentations with subject='default'
    presentations = tool.list_presentations(subject='default')
    print("\n" + "="*70)
    print("UNORGANIZED PRESENTATIONS:")
    print("="*70)
    print(json.dumps(presentations, indent=2))
