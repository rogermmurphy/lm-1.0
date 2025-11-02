# Transcription Feature Test Script

## Test: Audio Transcription End-to-End

**Status**: ⚠️ UI VERIFIED (Full test requires audio file)  
**Date**: November 2, 2025  
**Environment**: Local Development (Docker + Whisper)

## Prerequisites

- Docker services running and healthy
- Next.js UI running on port 3001
- Playwright MCP server connected
- User already logged in (testuser@example.com)
- Speech-to-text service with Whisper running
- Async jobs worker running for background processing

## Test Steps

### 1. Navigate to Transcribe Page

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_click
  args:
    selector: "a[href='/dashboard/transcribe']"
```

### 2. Take Screenshot

```
use_mcp_tool:
  server: github.com/executeautomation/mcp-playwright
  tool: playwright_screenshot
  args:
    name: "transcribe-page"
    fullPage: false
```

### 3. Upload Audio File (Requires Real Audio)

To complete testing, you would:
- Create a test audio file (5-10 seconds)
- Use file upload via Playwright
- Monitor async job status
- Verify transcript appears

```python
# Create test audio (example - not executed in this test)
from gtts import gTTS
tts = gTTS("This is a test of speech to text transcription")
tts.save("test_audio.mp3")
```

### 4. Select Language

Select "English" from language dropdown.

### 5. Click Upload and Transcribe

Click the submit button to start async transcription.

### 6. Monitor Job Status

Poll the job status endpoint every 5 seconds until completion.

### 7. Verify Transcript

Check that transcript text appears in the UI.

## Expected Results

### Console Logs Should Show:
- `[DEBUG] [API Request] POST /api/stt/transcribe`
- `[DEBUG] [API Response] 200 /api/stt/transcribe`
- Job ID returned in response
- Status polling requests at regular intervals

### Backend Response Format (Job Created):
```json
{
  "job_id": "uuid-here",
  "status": "pending",
  "created_at": "2025-11-02T16:20:00Z"
}
```

### Backend Response Format (Job Completed):
```json
{
  "job_id": "uuid-here",
  "status": "completed",
  "transcript": "This is a test of speech to text transcription",
  "language": "en",
  "duration": 5.2,
  "completed_at": "2025-11-02T16:20:15Z"
}
```

### Page Should:
- ✅ Display file upload interface
- ✅ Show language selection dropdown
- ✅ Display job status (pending/processing/completed)
- ✅ Show transcript when ready
- ✅ Provide download transcript option

## Actual Results (November 2, 2025)

⚠️ **UI VERIFIED**: Transcription UI functional, full test pending
- Transcription page loads successfully
- Upload interface renders correctly
- Form elements present and functional
- Backend `/api/stt/transcribe` endpoint exists
- Async job worker is running
- Full end-to-end test requires creating audio file

## Test Data Required

- Audio file: 5-10 seconds of speech
- Language: English (en)
- Supported formats: MP3, WAV, M4A, OGG

## Backend Services

### STT Service (Port 8002):
- Whisper-based transcription
- Supports multiple languages
- Creates async job for processing

### Async Jobs Worker:
- Polls Redis queue for transcription jobs
- Processes audio with Whisper
- Updates job status in PostgreSQL
- Stores transcript in database

## Notes

- Transcription is asynchronous - may take 10-60 seconds depending on audio length
- UI should poll job status every 5 seconds
- Whisper model runs in Docker container
- Job status tracked in PostgreSQL

## Screenshots

- `transcribe-page-2025-11-02T16-20-00-897Z.png` - Transcription page interface

## Next Steps for Complete Testing

1. Create test audio file using gTTS or record sample
2. Upload via Playwright file upload
3. Monitor async job completion
4. Verify transcript accuracy
5. Test download transcript functionality
