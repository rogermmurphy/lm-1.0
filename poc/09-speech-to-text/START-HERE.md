# Speech-to-Text POC - Quick Start Guide
**Local Whisper Speech Recognition for Lecture Transcription**

---

## What This POC Does

Transcribes audio lectures to text using OpenAI's Whisper model:
- **Async processing** - Queue transcription jobs that process in background
- **Whisper AI** - State-of-the-art speech recognition (runs locally, FREE)
- **Auto-RAG loading** - Transcripts automatically load into ChromaDB
- **Multi-language** - Supports 99+ languages with auto-detection
- **Timestamped** - Get segment-level timestamps for navigation

---

## Prerequisites

### Required Infrastructure
✅ PostgreSQL (localhost:5432)  
✅ Redis (localhost:6379)  
✅ Database: `lm_dev`

### Check Status
```bash
# PostgreSQL
psql -U postgres -d lm_dev -c "\dt"

# Redis
redis-cli ping
# Should return: PONG
```

---

## Step 1: Install Dependencies

```bash
cd poc/09-speech-to-text
pip install -r requirements.txt
```

**Note**: First run will download the Whisper model (~140MB for base model)

### System Requirements
- **FFmpeg** - Required for audio processing
  - Windows: `choco install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Linux: `apt-get install ffmpeg`

---

## Step 2: Create Database Table

```bash
psql -U postgres -d lm_dev -f schema.sql
```

Verify table exists:
```bash
psql -U postgres -d lm_dev -c "SELECT COUNT(*) FROM transcription_jobs;"
```

---

## Step 3: Test the System

### Option A: Run Test Script (Recommended)
```bash
python test_transcription.py
```

This will:
- Test database connection
- List existing transcriptions
- Show how to queue a job
- Explain next steps

### Option B: Manual Test

```python
from async_transcription_tool import AsyncTranscriptionTool

# Initialize
tool = AsyncTranscriptionTool()

# Queue a transcription
result = tool.transcribe_audio_async(
    file_path="lecture.mp3",
    user_id="test_user",
    subject="biology"
)

print(result)
# Returns job_id immediately
```

---

## Step 4: Start the Worker

In a **separate terminal**:

```bash
python transcription_worker.py
```

Options:
- `python transcription_worker.py tiny` - Fastest, lower quality
- `python transcription_worker.py base` - Good balance (default)
- `python transcription_worker.py small` - Better quality, slower
- `python transcription_worker.py medium` - High quality, quite slow

The worker will:
1. Wait for jobs in Redis queue
2. Process transcriptions using Whisper
3. Save results to database
4. Auto-load to ChromaDB (if enabled)

---

## Step 5: Queue & Monitor Jobs

### Queue a Job
```python
from async_transcription_tool import AsyncTranscriptionTool

tool = AsyncTranscriptionTool()

# Transcribe lecture
result = tool.transcribe_audio_async(
    file_path="biology_lecture_1.mp3",
    subject="biology",
    auto_load_to_chromadb=True
)

job_id = result['job_id']
```

### Check Status
```python
status = tool.get_job_status(job_id)
print(status['status'])  # pending, processing, completed, failed
```

### Get Full Transcript
```python
transcript = tool.get_full_transcript(job_id)
print(transcript['transcript'])
print(f"Word count: {transcript['word_count']}")
```

### List Transcriptions
```python
# All transcriptions
all_trans = tool.list_transcriptions()

# By subject
biology = tool.list_transcriptions(subject="biology")

# By status
completed = tool.list_transcriptions(status="completed")
```

---

## Architecture

```
User uploads audio
    ↓
AsyncTranscriptionTool.transcribe_audio_async()
    ↓
Job saved to PostgreSQL (status: pending)
    ↓
Job queued in Redis
    ↓
Worker picks up job
    ↓
Whisper transcribes audio (10-20 min for 1 hour)
    ↓
Transcript saved to database
    ↓
Auto-loaded to ChromaDB (optional)
    ↓
User can query transcript with RAG
```

---

## Performance Expectations

### Base Model (Recommended)
- **1 hour lecture** → 10-20 minutes processing
- **5 minute video** → 1-2 minutes processing
- **Accuracy**: Very good for clear speech
- **Languages**: Auto-detected

### Model Comparison
| Model  | Size  | Speed | Quality | Use Case |
|--------|-------|-------|---------|----------|
| tiny   | 39M   | Fast  | OK      | Quick tests |
| base   | 74M   | Good  | Good    | **Recommended** |
| small  | 244M  | Slow  | Better  | When accuracy matters |
| medium | 769M  | Very slow | Best | Production transcripts |

---

## Supported Audio Formats

✅ MP3  
✅ WAV  
✅ M4A  
✅ FLAC  
✅ OGG  
✅ Any format FFmpeg supports

---

## Integration with RAG

Transcripts can auto-load to ChromaDB:

```python
result = tool.transcribe_audio_async(
    file_path="lecture.mp3",
    auto_load_to_chromadb=True,  # Enable auto-load
    subject="biology"  # Creates 'biology_transcripts' collection
)
```

Then query with your RAG chatbot:
```
User: "What did the professor say about mitochondria?"
RAG: [searches biology_transcripts collection]
```

---

## Troubleshooting

### Error: "Audio file not found"
- Use absolute path: `C:/path/to/audio.mp3`
- Or relative to working directory

### Error: "FFmpeg not found"
- Install FFmpeg (see Step 1)
- Add to system PATH

### Slow Processing
- Use smaller model: `tiny` or `base`
- Consider GPU acceleration (requires CUDA setup)
- For production: Use cloud API (OpenAI Whisper API)

### Database Connection Failed
```bash
# Check PostgreSQL
psql -U postgres -d lm_dev -c "SELECT 1;"

# Recreate table
psql -U postgres -d lm_dev -f schema.sql
```

### Redis Connection Failed
```bash
# Check Redis
redis-cli ping

# Start Redis (if not running)
redis-server
```

---

## Files in This POC

| File | Purpose |
|------|---------|
| `transcription_engine.py` | Core Whisper transcription logic |
| `async_transcription_tool.py` | Queue jobs, check status |
| `transcription_worker.py` | Background worker process |
| `schema.sql` | Database table definition |
| `test_transcription.py` | Test suite |
| `requirements.txt` | Python dependencies |
| `START-HERE.md` | This guide |
| `README.md` | Full documentation |

---

## Next Steps

1. ✅ Test with sample audio file
2. ✅ Verify transcription quality
3. ✅ Integrate with your ChromaDB setup
4. ✅ Add to your API endpoints
5. ✅ Consider GPU acceleration for production

---

## Production Considerations

### Local vs Cloud

**Local Whisper (Current Setup)**
- ✅ FREE
- ✅ Private (no data leaves your system)
- ⚠️ Slow on CPU (10-20 min per hour)
- ⚠️ Requires FFmpeg

**Cloud APIs**
- OpenAI Whisper API: $0.006/minute
- AssemblyAI: $0.00025/second
- Deepgram: $0.0043/minute
- ✅ Fast (real-time or faster)
- ⚠️ Costs add up at scale

**Recommendation**: Local for POC/testing, cloud for production scale

---

## Support

Questions? Check:
- Main README: `poc/09-speech-to-text/README.md`
- Test script: `python test_transcription.py`
- Example usage in `async_transcription_tool.py`

---

**Status**: ✅ POC Ready  
**Last Updated**: 2025-11-01
