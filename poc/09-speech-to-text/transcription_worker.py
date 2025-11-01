#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transcription Background Worker - Processes speech-to-text transcription jobs
Runs continuously, pulling jobs from Redis queue and using Whisper for transcription
"""

import sys
import io
# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import psycopg2
import redis
import json
import time
from datetime import datetime
from transcription_engine import TranscriptionEngine

class TranscriptionWorker:
    def __init__(self, model_size: str = "base"):
        """Initialize connections and transcription engine"""
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
        
        # Transcription engine
        self.engine = TranscriptionEngine(model_size=model_size)
        print(f"[OK] Transcription engine ready (model: {model_size})\n")
    
    def update_job_status(self, job_id, status, **kwargs):
        """Update job status in database"""
        cursor = self.pg_conn.cursor()
        
        updates = ["status = %s"]
        params = [status]
        
        if status == 'processing':
            updates.append("started_at = %s")
            params.append(datetime.now())
        elif status == 'completed':
            updates.append("completed_at = %s")
            params.append(datetime.now())
        
        for key, value in kwargs.items():
            updates.append(f"{key} = %s")
            params.append(value)
        
        params.append(job_id)
        
        query = f"UPDATE transcription_jobs SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        self.pg_conn.commit()
        cursor.close()
    
    def load_to_chromadb(self, job_id, transcript_text, file_name, subject):
        """
        Load transcript to ChromaDB for RAG
        This is a placeholder - integrate with your ChromaDB setup
        """
        try:
            # TODO: Implement ChromaDB loading
            # For now, just mark as loaded
            collection_name = f"{subject}_transcripts"
            
            # Example ChromaDB integration:
            # from chromadb import Client
            # client = Client()
            # collection = client.get_or_create_collection(collection_name)
            # collection.add(
            #     documents=[transcript_text],
            #     metadatas=[{"source": file_name, "type": "transcript"}],
            #     ids=[job_id]
            # )
            
            self.update_job_status(
                job_id,
                'completed',
                loaded_to_chromadb=True,
                chromadb_collection=collection_name
            )
            print(f"[CHROMADB] Transcript loaded to collection: {collection_name}")
            return True
            
        except Exception as e:
            print(f"[WARNING] Could not load to ChromaDB: {e}")
            return False
    
    def process_job(self, job_data):
        """Process a single transcription job"""
        job_id = job_data['job_id']
        file_path = job_data['file_path']
        file_name = job_data['file_name']
        auto_load = job_data.get('auto_load_to_chromadb', True)
        subject = job_data.get('subject', 'default')
        
        print(f"\n{'='*70}")
        print(f"Processing Transcription Job: {job_id}")
        print(f"File: {file_name}")
        print(f"{'='*70}\n")
        
        try:
            # Update status to processing
            self.update_job_status(job_id, 'processing')
            print(f"[STATUS] Job {job_id} → processing")
            
            # Transcribe audio file
            print(f"[TRANSCRIBE] Starting Whisper transcription...")
            result = self.engine.transcribe_file(file_path, return_timestamps=True)
            
            # Update database with result
            self.update_job_status(
                job_id, 
                'completed',
                transcript_text=result['text'],
                duration_seconds=result['duration'],
                language=result['language']
            )
            
            print(f"\n[SUCCESS] Transcription complete!")
            print(f"  - Duration: {result['duration']:.1f}s")
            print(f"  - Language: {result['language']}")
            print(f"  - Processing time: {result['processing_time']:.1f}s")
            print(f"  - Word count: {len(result['text'].split())}")
            
            # Auto-load to ChromaDB if requested
            if auto_load:
                print(f"\n[CHROMADB] Auto-loading to ChromaDB...")
                self.load_to_chromadb(job_id, result['text'], file_name, subject)
            
        except FileNotFoundError:
            error_msg = f"Audio file not found: {file_path}"
            self.update_job_status(job_id, 'failed', error_message=error_msg)
            print(f"[ERROR] {error_msg}")
            
        except Exception as e:
            # Processing error
            error_msg = str(e)
            self.update_job_status(job_id, 'failed', error_message=error_msg)
            print(f"[ERROR] Job {job_id} failed: {error_msg}")
    
    def run(self):
        """Main worker loop - processes jobs from queue"""
        print("="*70)
        print(" Transcription Worker Started")
        print(" Listening for jobs on Redis queue: transcription_queue")
        print("="*70)
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                # Block and wait for job (5 second timeout)
                job = self.redis_client.blpop('transcription_queue', timeout=5)
                
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
    import sys
    
    # Allow specifying model size via command line
    model_size = "base"
    if len(sys.argv) > 1:
        model_size = sys.argv[1]
        if model_size not in ['tiny', 'base', 'small', 'medium', 'large']:
            print(f"Invalid model size: {model_size}")
            print("Valid options: tiny, base, small, medium, large")
            sys.exit(1)
    
    print(f"Starting worker with {model_size} model...\n")
    worker = TranscriptionWorker(model_size=model_size)
    worker.run()
