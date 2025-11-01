"""
POC 10: CLI Audio Recorder
Simple command-line interface for recording audio
Press ENTER to start/stop recording
"""
import sys
import os
from pathlib import Path
import time
from audio_recorder import AudioRecorder

# Add POC 09 to path for transcription integration
sys.path.insert(0, str(Path(__file__).parent.parent / '09-speech-to-text'))

try:
    from async_transcription_tool import AsyncTranscriptionTool
    POC09_AVAILABLE = True
except ImportError:
    POC09_AVAILABLE = False
    print("⚠️  Warning: POC 09 not available. Transcription disabled.")


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_header():
    """Show CLI header"""
    print("\n" + "="*60)
    print("POC 10: RECORD-TO-TEXT")
    print("Press ENTER to Start/Stop Recording")
    print("="*60)


def show_recording_status(recorder):
    """Show real-time recording status"""
    print(f"\r🔴 RECORDING... Duration: {recorder.get_duration():.1f}s ", end='', flush=True)


def main():
    """Main CLI recording loop"""
    clear_screen()
    show_header()
    
    # Initialize recorder
    recorder = AudioRecorder(
        sample_rate=16000,  # Optimal for Whisper
        channels=1,         # Mono
        dtype='int16'
    )
    
    # Show device info
    print("\n📱 Audio Device Info:")
    default_device = recorder.get_default_device()
    
    # Recording loop
    while True:
        print("\n" + "-"*60)
        print("Press ENTER to start recording (or 'q' + ENTER to quit)")
        user_input = input("> ").strip().lower()
        
        if user_input == 'q':
            print("\n👋 Goodbye!")
            break
        
        # Start recording
        print("\n🎤 Starting recording...")
        print("Press ENTER to stop recording\n")
        recorder.start_recording()
        
        # Show real-time duration
        try:
            while recorder.recording:
                show_recording_status(recorder)
                time.sleep(0.1)
                
                # Check for ENTER key (non-blocking)
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key == b'\r':  # ENTER key
                        break
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted!")
        
        # Stop recording
        audio_data = recorder.stop_recording()
        
        if audio_data is None:
            print("\n❌ No audio recorded")
            continue
        
        # Save to file
        recordings_dir = Path(__file__).parent / "recordings"
        filepath = recorder.save_to_file(
            audio_data,
            output_dir=str(recordings_dir)
        )
        
        # Show file info
        file_size = Path(filepath).stat().st_size / 1024  # KB
        duration = len(audio_data) / recorder.sample_rate
        print(f"\n✅ Recording saved:")
        print(f"   File: {filepath}")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   Size: {file_size:.1f} KB")
        
        # Queue for transcription if POC 09 is available
        if POC09_AVAILABLE:
            print("\n🔄 Queuing for transcription...")
            try:
                tool = AsyncTranscriptionTool()
                result = tool.transcribe_audio_async(
                    file_path=filepath,
                    user_id='cli_user',
                    subject='voice_recording',
                    auto_load_to_chromadb=True
                )
                
                if result['status'] == 'queued':
                    print(f"✅ Transcription queued!")
                    print(f"   Job ID: {result['job_id']}")
                    print(f"\n💡 Check status with:")
                    print(f"   cd ../09-speech-to-text")
                    print(f"   python -c \"from async_transcription_tool import AsyncTranscriptionTool; ")
                    print(f"   tool = AsyncTranscriptionTool(); ")
                    print(f"   print(tool.get_job_status('{result['job_id']}'))\"")
                else:
                    print(f"⚠️  Status: {result['status']}")
                    
            except Exception as e:
                print(f"\n⚠️  Could not queue for transcription: {e}")
                print("   Make sure POC 09 services are running:")
                print("   - PostgreSQL database")
                print("   - Redis server")
                print("   - Transcription worker")
        else:
            print("\n💡 To enable auto-transcription:")
            print("   1. Set up POC 09 (see ../09-speech-to-text/START-HERE.md)")
            print("   2. Run this script again")
        
        print("\n" + "-"*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
