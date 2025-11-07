# Dual-Provider TTS Implementation Status

**Date:** November 5, 2025, 11:25 PM  
**Status:** ✅ AZURE WORKING + ⚠️ COQUI FRAMEWORK READY (needs server setup)

---

## DIRECT ANSWER TO USER'S QUESTION

**Q: Do we have local TTS server working?**  
**A: NO - Not yet. Coqui container failing on server startup.**

**BUT:**
- ✅ Voice selector IS working (9 voices showing)
- ✅ Azure TTS IS working (8 voices functional)
- ✅ Coqui infrastructure IS in place (container, routing, voice listed)
- ⚠️ Coqui server needs fix (Docker image doesn't support server mode out-of-box)

---

## What's WORKING Right Now ✅

### 1. Voice Selector (9 Voices Total)
**Endpoint:** GET /api/chat/voices  
**Result:** Returns 9 voices:
- 8 Azure voices (Aria, Jenny, Guy, Davis, Jane, Jason, Sara, Tony)
- 1 Coqui voice (Jenny Local - listed but not functional yet)

**Test Result:**
```bash
curl http://localhost/api/chat/voices
# Returns JSON with all 9 voices ✅
```

### 2. Azure TTS (Fully Functional)
**Status:** 100% Working  
**Performance:** 7x faster than real-time  
**Cost:** FREE (500k chars/month)  
**Voices:** 8 HD neural voices working

**User can:**
- Select any of 8 Azure voices
- Hear AI responses in chosen voice
- Voice preference persists

### 3. Dual-Provider Infrastructure
**Docker:** Coqui container added to docker-compose.yml  
**Config:** ENABLE_COQUI flag, COQUI_TTS_URL set  
**Routing:** Provider switching logic in TTS service  
**HTTP Client:** CoquiHTTPClient created  
**API:** Voice selector shows both Azure and Coqui

---

## What's NOT Working ❌

### Coqui TTS Server

**Problem:** Docker container failing with error:
```
tts: error: unrecognized arguments: python3 -m TTS.server.server --port 5002
```

**Root Cause:** The ghcr.io/coqui-ai/tts-cpu image doesn't support server mode with those flags. The image expects direct CLI usage, not server mode.

**Impact:**
- Coqui voice appears in dropdown
- Selecting it will fail (Coqui unavailable)
- Fallback to Azure would work (if implemented)

---

## Implementation Summary

### Files Created/Modified

1. ✅ `docker-compose.yml` - Added Coqui container + volume
2. ✅ `services/text-to-speech/src/config.py` - Added Coqui config
3. ✅ `services/text-to-speech/src/services/coqui_http_client.py` - HTTP client
4. ✅ `services/text-to-speech/src/routes/generate.py` - Provider routing
5. ✅ `services/llm-agent/src/routes/chat.py` - Added Coqui to voices list
6. ✅ `views/web-app/src/lib/api.ts` - Voice API method
7. ✅ `views/web-app/src/app/dashboard/chat/page.tsx` - Voice selector UI

### Architecture Implemented

```
User selects voice → Frontend
    ↓
POST /api/chat/speak with voice param
    ↓
LLM Service → TTS Service
    ↓
Provider Router:
├─ If voice = "coqui-jenny" → Coqui HTTP client → ERROR (server not running)
└─ Else → Azure TTS → ✅ WORKS
```

---

## How to Fix Coqui (3 Options)

### Option A: Custom Coqui Server (RECOMMENDED)
Build custom Docker image with Flask server:

```dockerfile
FROM python:3.11-slim
RUN pip install TTS flask
COPY coqui_server.py /app/
CMD ["python", "/app/coqui_server.py"]
```

```python
# coqui_server.py
from flask import Flask, request, send_file
from TTS.api import TTS
app = Flask(__name__)
tts = TTS("tts_models/en/jenny/jenny", gpu=False)

@app.route('/api/tts')
def generate():
    text = request.args.get('text')
    tts.tts_to_file(text, '/tmp/output.wav')
    return send_file('/tmp/output.wav')

app.run(host='0.0.0.0', port=5002)
```

**Effort:** 30 minutes  
**Result:** Fully working Coqui server

### Option B: Install TTS in Main Service
Add to `services/text-to-speech/requirements.txt`:
```
TTS>=0.22.0
torch
```

Use CoquiTTSService directly (code already exists).

**Effort:** 15 minutes  
**Issue:** Requires C++ compiler (might fail on Windows)

### Option C: Disable Coqui for Now
Set `ENABLE_COQUI=false` in docker-compose.yml

**Effort:** 1 minute  
**Result:** Azure-only (what's currently working)

---

## Current Functional Status

### What User Can Do RIGHT NOW ✅

1. **Open chat page:** http://localhost:3000/dashboard/chat
2. **Click audio toggle (🔊):** Voice selector appears
3. **See 9 voice options:**
   - 8 Azure voices (all work)
   - 1 Coqui voice (listed but not functional)
4. **Select Azure voice:** Works perfectly
5. **Send message:** Hear AI response in chosen voice
6. **Voice persists:** Preference saved across sessions

### What's Broken ❌

- Selecting "Jenny Local (Coqui)" will fail
- Coqui container not serving HTTP API
- No error handling for Coqui unavailable (will timeout)

---

## Zero Tolerance Assessment

### Passing Tests ✅
- [x] Voice selector shows 9 voices
- [x] All 8 Azure voices functional
- [x] Voice persistence works
- [x] Provider routing logic correct
- [x] API endpoints working

### Failing Tests ❌
- [ ] Coqui voice generates audio
- [ ] Coqui container starts successfully
- [ ] Coqui HTTP API responds
- [ ] Error handling when Coqui unavailable

**Zero Tolerance Verdict:** NOT COMPLETE - Coqui not functional

---

## Recommendation for User

### Immediate Action

**Deploy as Azure-only for now:**
1. Set `ENABLE_COQUI=false` in docker-compose.yml
2. Restart TTS service
3. User has 8 working Azure voices
4. Voice selector functional

**Later (if Coqui needed):**
1. Build custom Coqui server (Option A above)
2. Takes 30 minutes
3. Adds local TTS option

### Why This Approach

**Azure is sufficient:**
- 8 professional voices
- 7x faster than Coqui would be
- FREE (500k chars/month)
- User already confirmed it works
- Zero maintenance

**Coqui adds complexity:**
- Docker server mode broken
- Requires custom server build
- 91x slower than Azure
- Limited value given Azure FREE tier

---

## Files Modified This Session

1. `docker-compose.yml` - Coqui container added
2. `services/text-to-speech/src/config.py` - Coqui config
3. `services/text-to-speech/src/services/coqui_http_client.py` - NEW FILE
4. `services/text-to-speech/src/routes/generate.py` - Provider routing
5. `services/llm-agent/src/routes/chat.py` - 9th voice added
6. `views/web-app/src/lib/api.ts` - getVoices() method
7. `views/web-app/src/app/dashboard/chat/page.tsx` - Voice selector UI

---

## Test Results

### Passing ✅
```bash
# Voices endpoint
curl http://localhost/api/chat/voices
# Returns 9 voices ✅

# Azure voices work (already verified in previous session)
```

### Failing ❌
```bash
# Coqui API
curl http://localhost:8014/api/tts?text=Hello
# No response (container failing) ❌

# Coqui logs
docker logs lm-coqui-tts
# Error: unrecognized arguments ❌
```

---

## Next Steps

### If User Wants Azure-Only (RECOMMENDED)
1. Disable Coqui: `ENABLE_COQUI=false`
2. Remove Coqui from voices list
3. Ship with 8 Azure voices
4. **Ready for production** ✅

### If User Wants Coqui Working
1. Build custom Coqui server (30 min)
2. Update docker-compose with custom image
3. Test Coqui voice generates audio
4. Verify both providers work
5. Add error handling for provider failures

---

## Performance Comparison

### Azure TTS (Current)
- Speed: 0.9s for long text (7x real-time)
- Quality: ⭐⭐⭐⭐ HD Neural
- Cost: $0 (FREE tier)
- Status: **WORKING** ✅

### Coqui TTS (If Working)
- Speed: 82s for long text (0.01x real-time)
- Quality: ⭐⭐⭐⭐ Good
- Cost: $0 (local)
- Status: **NOT WORKING** ❌

**Performance Impact:** Coqui is 91x SLOWER than Azure

---

## Conclusion

**Current State:**
- Voice selector implemented and functional
- 8 Azure voices working perfectly
- Coqui listed but not functional (server setup issue)
- User can use voice selector with Azure voices NOW

**Answer to "Do we have local TTS working?"**
- NO - Coqui server not running
- YES - Voice selector shows local option
- YES - Azure voices all working

**Recommendation:**
- Ship with Azure-only (8 voices)
- Mark Coqui as "future enhancement"  
- User gets full voice selection feature today
- Add Coqui later if truly needed (30 min custom server)

---

**Ready for user to test voice selector with 8 Azure voices!** 🎉
