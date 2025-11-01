#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Background Worker - Processes presentation generation jobs
Runs continuously, pulling jobs from Redis queue and calling Presenton API
"""

import sys
import io
# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import psycopg2
import redis
import json
import requests
import time
from datetime import datetime

class PresentationWorker:
    def __init__(self):
        """Initialize connections"""
        # PostgreSQL
        self.pg_conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="lm_dev",
            user="postgres",
            password="postgres"
        )
        print("[OK] Worker connected to PostgreSQL")
        
        # Redis
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )
        print("[OK] Worker connected to Redis")
        
        # Presenton API
        self.presenton_url = "http://localhost:5000/api/v1/ppt/presentation/generate"
        print("[OK] Worker configured for Presenton\n")
    
    def update_job_status(self, job_id, status, **kwargs):
        """Update job status in database"""
        cursor = self.pg_conn.cursor()
        
        updates = [f"status = %s"]
        params = [status]
        
        if status == 'processing':
            updates.append("started_at = %s")
            params.append(datetime.now())
        elif status == 'complete':
            updates.append("completed_at = %s")
            params.append(datetime.now())
        
        for key, value in kwargs.items():
            updates.append(f"{key} = %s")
            params.append(value)
        
        params.append(job_id)
        
        query = f"UPDATE presentation_jobs SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        self.pg_conn.commit()
        cursor.close()
    
    def process_job(self, job_data):
        """Process a single presentation job"""
        job_id = job_data['job_id']
        topic = job_data['topic']
        n_slides = job_data.get('n_slides', 5)
        
        print(f"\n{'='*70}")
        print(f"Processing Job: {job_id}")
        print(f"Topic: {topic}")
        print(f"{'='*70}\n")
        
        try:
            # Update status to processing
            self.update_job_status(job_id, 'processing')
            print(f"[STATUS] Job {job_id} → processing")
            
            # Call Presenton API
            print(f"[API] Calling Presenton API...")
            response = requests.post(
                self.presenton_url,
                json={
                    "content": topic,
                    "n_slides": n_slides,
                    "language": "English",
                    "template": "general",
                    "export_as": "pptx",
                    "tone": "educational"
                },
                timeout=1800  # 30 minutes max
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update database with result
                self.update_job_status(
                    job_id, 
                    'complete',
                    presenton_id=result.get('presentation_id'),
                    presenton_url=result.get('edit_path'),
                    presenton_file_path=result.get('path')
                )
                
                print(f"[SUCCESS] Job {job_id} complete!")
                print(f"  - Presentation ID: {result.get('presentation_id')}")
                print(f"  - URL: http://localhost:5000{result.get('edit_path')}")
            else:
                # API error
                error_msg = f"Presenton API error: {response.status_code}"
                self.update_job_status(job_id, 'error', error_message=error_msg)
                print(f"[ERROR] {error_msg}")
        
        except Exception as e:
            # Processing error
            error_msg = str(e)
            self.update_job_status(job_id, 'error', error_message=error_msg)
            print(f"[ERROR] Job {job_id} failed: {error_msg}")
    
    def run(self):
        """Main worker loop - processes jobs from queue"""
        print("="*70)
        print(" Presentation Worker Started")
        print(" Listening for jobs on Redis queue: presentation_queue")
        print("="*70)
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                # Block and wait for job (5 second timeout)
                job = self.redis_client.blpop('presentation_queue', timeout=5)
                
                if job:
                    # job is tuple: (queue_name, job_data)
                    job_data = json.loads(job[1])
                    self.process_job(job_data)
                else:
                    # No jobs, just waiting
                    print(".", end="", flush=True)
                    time.sleep(5)
        
        except KeyboardInterrupt:
            print("\n\nWorker stopped by user")
        except Exception as e:
            print(f"\n[ERROR] Worker crashed: {e}")
        finally:
            self.pg_conn.close()
            print("\nConnections closed")

if __name__ == "__main__":
    worker = PresentationWorker()
    worker.run()
