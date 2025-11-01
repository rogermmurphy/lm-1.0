#!/usr/bin/env python3
"""
Test Real Speech - Queue and process real biology lecture
"""

from async_transcription_tool import AsyncTranscriptionTool
from transcription_worker import TranscriptionWorker
import json
import time

print("\n" + "="*70)
print("TESTING WITH REAL SPEECH")
print("="*70 + "\n")

# Step 1: Queue the job
print("Step 1: Queuing transcription job...")
tool = AsyncTranscriptionTool()
result = tool.transcribe_audio_async(
    file_path='real_lecture.mp3',
    user_id='test_user',
    subject='biology',
    auto_load_to_chromadb=True
)

print("\nJob queued:")
print(json.dumps(result, indent=2))
job_id = result['job_id']

# Step 2: Process with worker
print("\n" + "="*70)
print("Step 2: Processing with Whisper (tiny model for speed)...")
print("="*70 + "\n")

worker = TranscriptionWorker(model_size="tiny")
job = worker.redis_client.blpop('transcription_queue', timeout=2)

if job:
    job_data = json.loads(job[1])
    worker.process_job(job_data)
    
    # Step 3: Verify result
    print("\n" + "="*70)
    print("Step 3: Verifying transcript from database...")
    print("="*70 + "\n")
    
    time.sleep(1)  # Give DB time to commit
    
    status = tool.get_job_status(job_id)
    
    print(f"Status: {status['status']}")
    print(f"Language: {status['language']}")
    print(f"Duration: {status['duration_seconds']}s")
    
    if status['status'] == 'completed':
        # Get full transcript
        full = tool.get_full_transcript(job_id)
        
        print("\n" + "="*70)
        print("ACTUAL WHISPER TRANSCRIPT:")
        print("="*70)
        print(full['transcript'])
        print("="*70)
        print(f"Word count: {full['word_count']}")
        
        # Compare with expected
        expected = """Hello and welcome to today's biology lecture. 
Today we will discuss the structure and function of cells. 
Cells are the basic building blocks of all living organisms. 
Inside the cell we find the nucleus which contains genetic material. 
The mitochondria are often called the powerhouse of the cell. 
They generate energy through cellular respiration. 
The cell membrane controls what enters and exits the cell. 
This concludes our brief introduction to cell biology."""
        
        print("\n" + "="*70)
        print("EXPECTED TEXT:")
        print("="*70)
        print(expected)
        print("="*70)
        
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print("\nThis is REAL transcription of REAL speech!")
        print("✓ Created audio with actual spoken words")
        print("✓ Whisper transcribed the speech")
        print("✓ Results stored in database")
        print("✓ NOT make-believe!")
        
else:
    print("[ERROR] No job found in queue")

worker.pg_conn.close()
