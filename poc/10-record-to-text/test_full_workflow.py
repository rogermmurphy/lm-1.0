"""
POC 10: Complete End-to-End Test
Records real audio, transcribes it, and shows the result
"""
import sys
from pathlib import Path
import time

# Add POC 09 to path
sys.path.insert(0, str(Path(__file__).parent.parent / '09-speech-to-text'))

from audio_recorder import AudioRecorder
from async_transcription_tool import AsyncTranscriptionTool


def main():
    """Complete end-to-end test: Record → Transcribe → Show Result"""
    
    print("\n" + "="*70)
    print("POC 10: COMPLETE END-TO-END TEST")
    print("Record Audio -> Transcribe -> Show Transcript")
    print("="*70)
    
    # Step 1: Initialize recorder
    print("\n[STEP 1] Initializing audio recorder...")
    recorder = AudioRecorder(
        sample_rate=16000,
        channels=1,
        dtype='int16'
    )
    
    # Check microphone
    print("\n[MICROPHONE]")
    device = recorder.get_default_device()
    
    # Step 2: Record audio
    print("\n[STEP 2] Recording audio...")
    print("\n" + "="*70)
    print("PLEASE SPEAK INTO YOUR MICROPHONE NOW!")
    print("Say something like: 'This is a test of the audio recording system'")
    print("Recording will last 10 seconds...")
    print("="*70)
    
    input("\nPress ENTER when ready to start recording...")
    
    # Record for 10 seconds
    audio_data = recorder.record_for_duration(10.0)
    
    if audio_data is None:
        print("\n[ERROR] No audio was recorded!")
        print("Please check your microphone and try again.")
        return
    
    # Step 3: Save recording
    print("\n[STEP 3] Saving recording...")
    recordings_dir = Path(__file__).parent / "recordings"
    filepath = recorder.save_to_file(
        audio_data,
        output_dir=str(recordings_dir),
        filename="test_recording.wav"
    )
    
    duration = len(audio_data) / recorder.sample_rate
    file_size = Path(filepath).stat().st_size / 1024  # KB
    
    print(f"\n[SUCCESS] Recording saved!")
    print(f"  File: {filepath}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  Size: {file_size:.1f} KB")
    
    # Step 4: Queue for transcription
    print("\n[STEP 4] Queuing for transcription...")
    try:
        tool = AsyncTranscriptionTool()
        result = tool.transcribe_audio_async(
            file_path=filepath,
            user_id='test_user',
            subject='end_to_end_test',
            auto_load_to_chromadb=False  # Don't load to ChromaDB for test
        )
        
        if result['status'] != 'queued':
            print(f"\n[ERROR] Transcription failed to queue: {result['status']}")
            return
        
        job_id = result['job_id']
        print(f"\n[SUCCESS] Transcription queued!")
        print(f"  Job ID: {job_id}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to queue transcription: {e}")
        print("\nMake sure POC 09 services are running:")
        print("  - PostgreSQL database")
        print("  - Redis server")
        print("  - Transcription worker (python transcription_worker.py)")
        return
    
    # Step 5: Wait for transcription
    print("\n[STEP 5] Waiting for transcription to complete...")
    print("This may take 10-30 seconds...\n")
    
    max_wait_time = 60  # Wait up to 60 seconds
    start_time = time.time()
    
    while True:
        # Check job status
        status_result = tool.get_job_status(job_id)
        status = status_result.get('status', 'unknown')
        
        elapsed = time.time() - start_time
        print(f"\rStatus: {status.upper()} (elapsed: {elapsed:.1f}s)", end='', flush=True)
        
        if status == 'completed':
            print("\n\n[SUCCESS] Transcription completed!")
            break
        elif status == 'failed':
            print("\n\n[ERROR] Transcription failed!")
            error = status_result.get('error_message', 'Unknown error')
            print(f"Error: {error}")
            return
        elif elapsed > max_wait_time:
            print(f"\n\n[TIMEOUT] Transcription taking longer than {max_wait_time} seconds")
            print("The transcription is still processing in the background.")
            print(f"Check status later with job_id: {job_id}")
            return
        
        time.sleep(2)  # Check every 2 seconds
    
    # Step 6: Get and display transcript
    print("\n[STEP 6] Retrieving transcript...\n")
    
    transcript_text = status_result.get('transcript', '')
    language = status_result.get('language', 'unknown')
    confidence = status_result.get('confidence', 0)
    
    print("="*70)
    print("TRANSCRIPTION RESULT")
    print("="*70)
    print(f"\nLanguage: {language}")
    print(f"Confidence: {confidence:.1%}")
    print(f"\nTranscript:")
    print("-" * 70)
    print(transcript_text)
    print("-" * 70)
    
    # Step 7: Summary
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)
    print(f"\n✓ Recording: {filepath}")
    print(f"✓ Duration: {duration:.2f} seconds")
    print(f"✓ Transcription: {len(transcript_text)} characters")
    print(f"✓ Language: {language} ({confidence:.1%} confidence)")
    
    print("\n" + "="*70)
    print("END-TO-END TEST SUCCESSFUL!")
    print("Recording -> Transcription -> Text WORKING!")
    print("="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
