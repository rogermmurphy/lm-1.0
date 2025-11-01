#!/usr/bin/env python3
"""
Download Sample Audio and Test Transcription
Automated script - no user interaction needed
"""

import os
import sys
import urllib.request

def download_sample_audio():
    """Download a short sample audio file"""
    print("="*70)
    print("DOWNLOADING SAMPLE AUDIO")
    print("="*70)
    
    # Use a short public domain audio sample
    # This is a ~30 second sample which is good for testing
    url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
    filename = "sample_lecture.wav"
    
    try:
        print(f"\nDownloading from: {url}")
        print(f"Saving to: {filename}")
        
        urllib.request.urlretrieve(url, filename)
        
        size_mb = os.path.getsize(filename) / (1024 * 1024)
        print(f"[OK] Downloaded: {size_mb:.2f} MB")
        return True
        
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        
        # Try alternative source
        print("\nTrying alternative source...")
        try:
            url2 = "https://filesamples.com/samples/audio/mp3/sample1.mp3"
            filename = "sample_lecture.mp3"
            print(f"Downloading from: {url2}")
            
            urllib.request.urlretrieve(url2, filename)
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            print(f"[OK] Downloaded: {size_mb:.2f} MB")
            return True
            
        except Exception as e2:
            print(f"[ERROR] Alternative download failed: {e2}")
            return False

def test_transcription(audio_file):
    """Test transcription on the downloaded audio"""
    print("\n" + "="*70)
    print("TESTING TRANSCRIPTION")
    print("="*70)
    
    try:
        from async_transcription_tool import AsyncTranscriptionTool
        import json
        
        tool = AsyncTranscriptionTool()
        
        print(f"\nQueuing transcription for: {audio_file}")
        result = tool.transcribe_audio_async(
            file_path=audio_file,
            user_id="test_user",
            subject="test",
            auto_load_to_chromadb=True
        )
        
        print("\n[OK] Job queued successfully!")
        print(json.dumps(result, indent=2))
        
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("\n1. Start the worker in a separate terminal:")
        print("   cd poc/09-speech-to-text")
        print("   python transcription_worker.py base")
        print("\n2. The worker will process the job and transcribe the audio")
        print("\n3. Check status:")
        print(f"   job_id = '{result['job_id']}'")
        print("   status = tool.get_job_status(job_id)")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Transcription test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*70)
    print("SPEECH-TO-TEXT POC - AUTOMATED TEST")
    print("="*70 + "\n")
    
    # Check if sample already exists
    audio_files = ['sample_lecture.mp3', 'sample_lecture.wav']
    existing_file = None
    
    for f in audio_files:
        if os.path.exists(f):
            existing_file = f
            break
    
    if existing_file:
        print(f"[INFO] Found existing audio file: {existing_file}")
        size_mb = os.path.getsize(existing_file) / (1024 * 1024)
        print(f"[INFO] Size: {size_mb:.2f} MB")
        
        # Use existing file
        audio_file = existing_file
    else:
        # Download new file
        if not download_sample_audio():
            print("\n[ERROR] Could not download sample audio")
            print("\nAlternative:")
            print("1. Manually download any MP3/WAV file")
            print("2. Place it in this directory as 'sample_lecture.mp3'")
            print("3. Run this script again")
            sys.exit(1)
        
        # Find the downloaded file
        audio_file = 'sample_lecture.wav' if os.path.exists('sample_lecture.wav') else 'sample_lecture.mp3'
    
    # Test transcription
    if test_transcription(audio_file):
        print("\n[SUCCESS] Test completed!")
    else:
        print("\n[ERROR] Test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
