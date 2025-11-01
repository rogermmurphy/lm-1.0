#!/usr/bin/env python3
"""
Run Worker Once - Process one transcription job and exit
"""

import sys
import time
from transcription_worker import TranscriptionWorker

def main():
    print("\n" + "="*70)
    print("RUNNING TRANSCRIPTION WORKER (ONE JOB)")
    print("="*70 + "\n")
    
    # Get model size from command line, default to tiny for testing
    model_size = "tiny" if len(sys.argv) <= 1 else sys.argv[1]
    
    print(f"Using model: {model_size}")
    print("Note: Using 'tiny' model for faster testing (lower quality)")
    print("      Use 'base' or 'small' for production\n")
    
    try:
        worker = TranscriptionWorker(model_size=model_size)
        
        # Check for pending job
        print("Checking for pending jobs...")
        job = worker.redis_client.blpop('transcription_queue', timeout=2)
        
        if job:
            import json
            job_data = json.loads(job[1])
            print(f"[OK] Found job: {job_data['job_id']}")
            print(f"[OK] File: {job_data['file_name']}\n")
            
            # Process the job
            worker.process_job(job_data)
            
            print("\n" + "="*70)
            print("JOB PROCESSING COMPLETE")
            print("="*70)
            
            # Check final status
            print("\nChecking job status...")
            status = worker.pg_conn.cursor()
            status.execute("""
                SELECT status, transcript_text, language, duration_seconds
                FROM transcription_jobs
                WHERE id = %s
            """, (job_data['job_id'],))
            
            row = status.fetchone()
            status.close()
            
            if row:
                print(f"Status: {row[0]}")
                if row[0] == 'completed':
                    print(f"Language: {row[2]}")
                    print(f"Duration: {row[3]:.1f}s")
                    print(f"\nTranscript preview:")
                    print("-" * 70)
                    print(row[1][:500] if row[1] else "No transcript")
                    print("-" * 70)
        else:
            print("[INFO] No pending jobs in queue")
            print("[INFO] Job may have already been processed")
        
        worker.pg_conn.close()
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
    except Exception as e:
        print(f"\n[ERROR] Worker failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
