# Voice Features Backlog

## ⏸️ Features for Future Implementation

### 1. STT (Speech-to-Text) - Chat Microphone Recording
**Status:** 90% Complete - Needs 503 Error Resolution

**What's Done:**
- ✅ Backend endpoint: POST /chat/transcribe
- ✅ Frontend microphone button (🎤) visible and clickable
- ✅ Recording logic implemented (MediaRecorder)
- ✅ User successfully clicked button and triggered recording

**What's Pending:**
- ⬜ Fix 503 error when calling /api/chat/transcribe
- ⬜ Test transcription end-to-end
- ⬜ Verify text appears in input field

**Error Details:**
```
POST /api/chat/transcribe 503 (Service Unavailable)
```

**Next Steps:**
1. Check LLM container logs for startup errors
2. Verify /chat/transcribe endpoint registered in FastAPI
3. Test with sample audio file
4. Retry microphone button after fix

### 2. Lecture Recording Feature
**Status:** Not Started

**Requirements:**
- Long-form audio recording (lectures, classes)
- Save to database
- Auto-transcribe with STT service
- Display in materials library

**Implementation Plan:**
1. Create new page: /dashboard/record
2. Add recording UI with start/stop/pause
3. Show recording duration timer
4. Save audio file to audio-recording service
5. Queue transcription job
6. Display in materials list when complete

**Technical Approach:**
- Use existing audio-recording service (port 8004)
- Leverage STT service for transcription
- Store in PostgreSQL with transcription job tracking
- Add to study materials for RAG indexing

---

## ✅ COMPLETED VOICE FEATURES

### TTS (Text-to-Speech) - AI Response Read-Back
**Status:** 100% Complete & Tested ✅

**Implementation:**
- Backend: POST /chat/speak
- Test Result: 200 OK, 244,060 bytes audio
- Frontend: Audio toggle button (🔊/🔇)
- Auto-play: AI responses read aloud when enabled
- Base64 to WAV conversion working
- Azure TTS integration (<1 second generation)

**User can:**
1. Click audio toggle to enable TTS
2. Send message to AI
3. Hear AI response through speakers
4. Toggle off to disable

---

## 📋 BACKLOG PRIORITY

**High Priority:**
1. Fix STT 503 error (90% done)
2. Test full STT workflow

**Medium Priority:**
3. Implement lecture recording page
4. Add recording duration display
5. Integrate with transcription workflow

**Low Priority:**
6. Add voice selection for TTS
7. Add waveform visualization
8. Cache TTS audio responses
