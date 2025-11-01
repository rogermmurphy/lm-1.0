#!/usr/bin/env python3
"""
Test Transcription System - End-to-end test of speech-to-text POC
Tests transcription engine, async tool, and database integration
"""

import json
import time
import os
from async_transcription_tool import AsyncTranscriptionTool

def print_separator():
    print("\n" + "="*70 + "\n")

def test_async_transcription():
    """Test the async transcription workflow"""
    
    print_separator()
    print("SPEECH-TO-TEXT POC TEST")
    print_separator()
    
    # Initialize tool
    print("Initializing async transcription tool...")
    tool = AsyncTranscriptionTool()
    
    print_separator()
    print("TEST 1: List Existing Transcriptions")
    print_separator()
    
    transcriptions = tool.list_transcriptions()
    if transcriptions:
        print(f"Found {len(transcriptions)} existing transcription(s):")
        for trans in transcriptions[:5]:  # Show first 5
            print(f"  - {trans['file_name']} ({trans['status']})")
    else:
        print("No existing transcriptions found")
    
    print_separator()
    print("TEST 2: Queue Sample Transcription Job")
    print_separator()
    
    # Check for sample audio file
    sample_audio = "sample_lecture.mp3"
    
    if not os.path.exists(sample_audio):
        print(f"[INFO] No sample audio file found: {sample_audio}")
        print("\nTo test transcription:")
        print("1. Place an audio file (MP3, WAV, M4A, etc.) in this directory")
        print("2. Rename it to 'sample_lecture.mp3' or update the path below")
        print("3. Run this test again")
        print("\nExample:")
        print("  result = tool.transcribe_audio_async('your_audio.mp3')")
        print("  print(json.dumps(result, indent=2))")
    else:
        print(f"Found sample audio: {sample_audio}")
        print("Queuing transcription job...")
        
        result = tool.transcribe_audio_async(
            file_path=sample_audio,
            user_id="test_user",
            auto_load_to_chromadb=True,
            subject="test"
        )
        
        print("\nJob Created:")
        print(json.dumps(result, indent=2))
        
        if 'job_id' in result:
            job_id = result['job_id']
            
            print_separator()
            print("TEST 3: Check Job Status")
            print_separator()
            
            print("Checking initial status...")
            status = tool.get_job_status(job_id)
            print(json.dumps(status, indent=2))
            
            print("\n[INFO] Job is queued and waiting for worker")
            print("[INFO] Start the worker to process this job:")
            print("       python transcription_worker.py")
            
            # Wait a bit and check again
            print("\nWaiting 3 seconds...")
            time.sleep(3)
            
            status = tool.get_job_status(job_id)
            print(f"\nCurrent status: {status['status']}")
            
            if status['status'] == 'completed':
                print("\n[SUCCESS] Transcription completed!")
                print(f"Duration: {status['duration_seconds']}s")
                print(f"Language: {status['language']}")
                print(f"Loaded to ChromaDB: {status['loaded_to_chromadb']}")
    
    print_separator()
    print("TEST 4: Filter Transcriptions by Status")
    print_separator()
    
    pending = tool.list_transcriptions(status='pending')
    print(f"Pending jobs: {len(pending)}")
    
    completed = tool.list_transcriptions(status='completed')
    print(f"Completed jobs: {len(completed)}")
    
    if completed:
        print("\nRecent completed transcriptions:")
        for trans in completed[:3]:
            print(f"  - {trans['file_name']}")
            print(f"    Duration: {trans['duration_seconds']}s")
            print(f"    Language: {trans['language']}")
    
    print_separator()
    print("TEST COMPLETE")
    print_separator()
    
    print("\nNext Steps:")
    print("1. Ensure PostgreSQL and Redis are running")
    print("2. Create database table: psql -U postgres -d lm_dev -f schema.sql")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start worker: python transcription_worker.py")
    print("5. Queue jobs using async_transcription_tool.py")


if __name__ == "__main__":
    try:
        test_async_transcription()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        print("\nMake sure:")
        print("- PostgreSQL is running on localhost:5432")
        print("- Redis is running on localhost:6379")
        print("- Database 'lm_dev' exists")
        print("- Table 'transcription_jobs' exists (run schema.sql)")
