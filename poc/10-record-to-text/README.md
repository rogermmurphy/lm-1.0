# POC 10: Record-to-Text
## Push-to-Record Audio Transcription

**Goal**: Record audio with push-button interface → Auto-transcribe with Whisper  
**Time**: 1 day  
**Priority**: HIGH  
**Builds on**: POC 09 (Speech-to-Text)

---

## Why Record-to-Text?

**Use Cases**:
1. **Live Lecture Recording** - Click record during class → Auto-transcribe
2. **Voice Notes** - Quick voice memos → Text in minutes
3. **Interview Recording** - Record conversations → Searchable transcripts
4. **Study Sessions** - Record yourself explaining concepts → Review later
5. **Accessibility** - Real-time transcription for hearing impaired

---

## What's New vs POC 09?

### POC 09 (Speech-to-Text)
- ✅ Transcribes existing audio files
- ✅ Queue-based processing
- ✅ ChromaDB integration

### POC 10 (Record-to-Text) **NEW!**
- 🎤 **Record audio** with push-button interface
- ⏱️ **Real-time status** - Shows recording time
- 💾 **Auto-save** - Saves to file when done
- 🔄 **Auto-queue** - Automatically queues for transcription
- 📝 **End-to-end** - Record → Transcribe → RAG in one flow

---

## Architecture

```
User clicks "Start Recording"
    ↓
Audio recording begins (using microphone)
    ↓
User clicks "Stop Recording"
    ↓
Audio saved to file (recording_TIMESTAMP.wav)
    ↓
Auto-queued for transcription (POC 09)
    ↓
Worker transcribes (Whisper)
    ↓
Transcript saved to database
    ↓
Auto-loaded to ChromaDB
    ↓
User can ask questions about what they recorded
```

---

## Implementation Options

### Option 1: CLI Interface (Simplest)
```python
import pyaudio
import wave

# Press Enter to start
# Press Enter to stop
# Auto-transcribe
```

**Pros**: Simple, no UI needed  
**Cons**: Not as intuitive

### Option 2: GUI with Tkinter (Recommended)
```python
import tkinter as tk
import sounddevice as sd

# Button to start/stop recording
# Shows recording time
# Visual feedback
```

**Pros**: User-friendly, visual feedback  
**Cons**: Requires GUI library

### Option 3: Web Interface
```python
# HTML5 MediaRecorder API
# Flask backend
# Modern web UI
```

**Pros**: Professional, accessible  
**Cons**: More complex setup

---

## Technology Stack

### Audio Recording
- **sounddevice** - Modern audio I/O (Recommended)
- **pyaudio** - Classic audio library (Alternative)
- **wave** - WAV file handling

### GUI (Optional)
- **tkinter** - Built-in Python GUI
- **PyQt5** - Advanced GUI (if needed)

### Integration
- **POC 09** - Whisper transcription
- **PostgreSQL** - Job tracking
- **Redis** - Job queue
- **ChromaDB** - RAG integration

---

## User Experience Flow

### Simple CLI Version:
```
$ python record_to_text.py

[READY] Microphone detected
Press ENTER to start recording...

[RECORDING] 0:05 elapsed (press ENTER to stop)
[RECORDING] 0:10 elapsed (press ENTER to stop)
[RECORDING] 0:15 elapsed (press ENTER to stop)

[STOPPED] Recording saved: recording_20251101_143000.wav
[QUEUE] Transcription job queued: abc-123-def
[INFO] Check status: python check_status.py abc-123-def

Done!
```

### GUI Version:
```
┌────────────────────────────┐
│   Record Audio Lecture     │
├────────────────────────────┤
│                            │
│   🎤 [Start Recording]     │
│                            │
│   Status: Ready            │
│   Duration: 0:00           │
│                            │
└────────────────────────────┘
```

---

## Implementation Steps

### Day 1: Core Recording
1. Install audio libraries
2. Test microphone detection
3. Implement start/stop recording
4. Save to WAV file
5. Integrate with POC 09 transcription

### Day 1 (cont): Polish
1. Add GUI with tkinter
2. Add recording timer
3. Auto-queue for transcription
4. Show transcription status
5. Test end-to-end

---

## Code Structure

```
poc/10-record-to-text/
├── README.md              # This file
├── requirements.txt       # sounddevice, etc.
├── audio_recorder.py      # Core recording logic
├── cli_recorder.py        # Simple CLI interface
├── gui_recorder.py        # Tkinter GUI version
├── test_microphone.py     # Test mic detection
└── START-HERE.md          # Setup guide
```

---

## Database Integration

**Reuses POC 09 schema** - No new tables needed!

The recorded audio is just saved as a file, then queued using the existing `transcription_jobs` table from POC 09.

---

## Dependencies

```txt
# Audio recording
sounddevice==0.4.6
numpy==1.24.3
scipy==1.11.3

# POC 09 integration (already installed)
openai-whisper==20231117
faster-whisper==1.0.3
psycopg2-binary==2.9.9
redis==5.0.1
```

---

## Example Usage

### CLI Version:
```bash
python cli_recorder.py

# Press ENTER to start
# Speak into microphone
# Press ENTER to stop
# Auto-transcribes!
```

### GUI Version:
```bash
python gui_recorder.py

# Click "Start Recording"
# Speak into microphone
# Click "Stop Recording"
# Shows transcription status
```

### Integration:
```python
from audio_recorder import AudioRecorder
from async_transcription_tool import AsyncTranscriptionTool

# Record
recorder = AudioRecorder()
audio_file = recorder.record_until_stopped()

# Transcribe (POC 09)
tool = AsyncTranscriptionTool()
result = tool.transcribe_audio_async(audio_file)

# Done!
```

---

## Testing

### Test 1: Microphone Detection
```bash
python test_microphone.py
# Should list available microphones
```

### Test 2: Record 10 seconds
```bash
python audio_recorder.py
# Records 10 second sample
```

### Test 3: Full workflow
```bash
python cli_recorder.py
# Record → Transcribe → Check result
```

---

## Expected Results

### Recording Quality
- **Format**: WAV (uncompressed)
- **Sample Rate**: 16kHz (optimal for Whisper)
- **Channels**: Mono
- **Bit Depth**: 16-bit

### Performance
- **Recording**: Real-time (no lag)
- **File Size**: ~1 MB per minute
- **Transcription**: Uses POC 09 (10-20 min per hour)

---

## Integration with Your System

### Workflow:
1. Student in class → Clicks "Record"
2. Lecture proceeds → Recording saves audio
3. Clicks "Stop" → Audio saved, job queued
4. 10-20 minutes later → Transcript ready
5. Student asks: "What did professor say about mitochondria?"
6. RAG searches transcript → Answers question

---

## Production Considerations

### Hardware
- ✅ Built-in microphone works
- ✅ External USB mic (better quality)
- ✅ Headset mic (clear audio)

### Storage
- 1 hour lecture = ~60 MB WAV file
- Consider compression to MP3
- Archive old recordings

### Real-time Transcription
- For live captions, consider:
  - Cloud APIs (faster)
  - GPU acceleration
  - Streaming transcription

---

## Next Steps

1. Install audio libraries
2. Test microphone detection
3. Create CLI recorder
4. Create GUI recorder
5. Integrate with POC 09
6. Test end-to-end workflow

Ready to build POC 10?

---

**Status**: Ready to implement  
**Estimated Time**: 1 day  
**Dependencies**: sounddevice, POC 09
