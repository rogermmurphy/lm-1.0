# Implementation Plan: Complete UI Feature Testing

## [Overview]
Complete end-to-end testing of the remaining 4 untested features (Chat, Materials Upload, Transcription, Text-to-Speech) in the Little Monster AI Tutor application. This involves identifying and fixing backend API mismatches, then testing each feature systematically using Playwright MCP server to ensure full functionality before final delivery.

The current state shows Registration and Login are fully tested and working. However, the 4 core application features have not been tested end-to-end. Investigation reveals several backend API issues that will prevent successful UI testing:

1. **TTS API Mismatch**: Backend expects query parameters but UI sends JSON body
2. **Materials Endpoint Missing**: No GET endpoint to list materials
3. **Materials Upload**: Uses wrong API endpoint (conversations instead of materials)
4. **Response Format Issues**: Some endpoints may not return expected field names

This plan addresses both backend fixes AND comprehensive UI testing to achieve 100% feature completion.

## [Types]

### Request/Response Schema Fixes

**TTSGenerateRequest** - New schema for TTS service:
```python
class TTSGenerateRequest(BaseModel):
    text: str
    voice: Optional[str] = None
```

**TTSGenerateResponse** - Response schema with base64 audio:
```python
class TTSGenerateResponse(BaseModel):
    id: int
    audio_base64: str
    provider: str
    voice: str
```

**MaterialsListResponse** - Response for materials endpoint:
```python
class MaterialsListResponse(BaseModel):
    id: int
    title: str
    subject: Optional[str]
    content_preview: str
    created_at: datetime
```

### UI Type Updates
No changes needed - existing TypeScript interfaces are correct.

## [Files]

### Backend Files to Modify

1. **services/text-to-speech/src/routes/generate.py**
   - Change from query parameters to request body model
   - Add TTSGenerateRequest schema
   - Return audio as base64 in response
   - Add proper error handling

2. **services/text-to-speech/src/schemas.py** (NEW FILE)
   - Create TTSGenerateRequest model
   - Create TTSGenerateResponse model

3. **services/llm-agent/src/routes/chat.py**
   - Add GET /materials endpoint to list user materials
   - Fix materials endpoint response format

4. **services/llm-agent/src/schemas.py**
   - Add MaterialsListResponse schema

### Test Documentation Files

5. **tests/e2e/test_chat.md** (NEW)
   - Playwright test procedure for Chat feature
   - Step-by-step testing instructions

6. **tests/e2e/test_materials.md** (NEW)
   - Playwright test procedure for Materials Upload
   - Verification steps

7. **tests/e2e/test_transcription.md** (NEW)
   - Playwright test procedure for Transcription
   - Async job status checking

8. **tests/e2e/test_tts.md** (NEW)
   - Playwright test procedure for TTS
   - Audio playback verification

### Root Directory Cleanup

9. **UI-COMPLETE-TEST-REPORT.md** - DELETE or MOVE to docs/
10. **FINAL-UI-TEST-STATUS.md** - DELETE or MOVE to docs/
11. **test_bedrock_direct.py** - MOVE to tests/

## [Functions]

### New Functions

**services/text-to-speech/src/routes/generate.py**:
- `generate_speech(request: TTSGenerateRequest, db: Session)` - Modified to accept request body instead of parameters
  - Validates text input
  - Generates speech using Azure TTS
  - Converts audio file to base64
  - Returns TTSGenerateResponse with base64 audio

**services/llm-agent/src/routes/chat.py**:
- `list_materials(db: Session)` - NEW endpoint GET /chat/materials
  - Queries StudyMaterial table
  - Returns list of materials with preview
  - Filters by user_id (from JWT)
  - Orders by created_at DESC

### Modified Functions

**services/text-to-speech/src/services/azure_tts.py**:
- `synthesize()` - May need to return audio bytes instead of just writing file
  - Add return value for audio data
  - Keep file writing for database record

## [Classes]

### New Classes

**services/text-to-speech/src/schemas.py**:
```python
class TTSGenerateRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class TTSGenerateResponse(BaseModel):
    id: int
    audio_base64: str
    provider: str = "azure"
    voice: str
```

**services/llm-agent/src/schemas.py** (add to existing):
```python
class MaterialsListResponse(BaseModel):
    id: int
    title: str
    subject: Optional[str]
    content_preview: str
    created_at: datetime
```

### Modified Classes

No existing classes need modification - only additions.

## [Dependencies]

### Python Package Requirements
No new dependencies - all required packages already installed:
- FastAPI (existing)
- Pydantic (existing)
- base64 (stdlib)

### Infrastructure Requirements
- All Docker services must be running (postgres, redis, chroma, etc.)
- Next.js dev server on port 3001
- Playwright MCP server must be available for testing

### Configuration Requirements
- AWS Bedrock credentials configured (already done)
- Azure TTS credentials configured (already done)
- Database schema deployed (already done)

## [Testing]

### Backend API Testing (Pre-UI Testing)

**Test 1: TTS API Fix**
```bash
curl -X POST http://localhost/api/tts/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"text": "Hello world", "voice": "en-US-AvaMultilingualNeural"}'
```
Expected: JSON response with audio_base64 field

**Test 2: Materials List Endpoint**
```bash
curl -X GET http://localhost/api/chat/materials \
  -H "Authorization: Bearer <token>"
```
Expected: Array of material objects

**Test 3: Materials Upload**
```bash
curl -X POST http://localhost/api/chat/materials \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Test", "content": "Test content", "subject": "Test"}'
```
Expected: Created material object

### UI End-to-End Testing with Playwright

**Feature 1: Chat with AI Tutor** (15 min)
- Use Playwright MCP to navigate and interact
- Login with test credentials
- Navigate to /dashboard/chat
- Send test message: "What is 2+2?"
- Verify: Claude Sonnet 4 responds within 10 seconds
- Verify: Response appears in chat interface
- Screenshot for documentation

**Feature 2: Upload Study Materials** (15 min)
- Navigate to /dashboard/materials
- Click "Upload Material" button
- Fill in title: "Test Material"
- Fill in content: "This is test content"
- Click upload
- Verify: Material appears in materials list
- Verify: No errors in console

**Feature 3: Transcribe Audio** (20 min)
- Navigate to /dashboard/transcribe
- Upload sample audio file (create 5-second test audio)
- Select language: English
- Click "Upload and Transcribe"
- Wait for processing (poll status every 5 seconds)
- Verify: Transcription completes successfully
- Verify: Transcript text is displayed
- Verify: Can download transcript

**Feature 4: Text-to-Speech** (15 min)
- Navigate to /dashboard/tts
- Enter text: "This is a test of the text to speech system"
- Select voice: Ava
- Click "Generate Speech"
- Verify: Audio player appears with generated audio
- Verify: Audio plays correctly
- Verify: Can download audio file

### Test Documentation Files

Each test procedure will be documented in tests/e2e/ directory:
- test_chat.md
- test_materials.md
- test_transcription.md
- test_tts.md

Following the format established in test_registration.md and test_login.md.

## [Implementation Order]

### Phase 1: Backend API Fixes (30 minutes)

1. **Fix TTS API endpoint** (10 min)
   - Create services/text-to-speech/src/schemas.py
   - Add TTSGenerateRequest and TTSGenerateResponse models
   - Modify services/text-to-speech/src/routes/generate.py
   - Change function signature to accept request body
   - Add base64 encoding for audio response
   - Test with curl

2. **Add Materials list endpoint** (10 min)
   - Add MaterialsListResponse to services/llm-agent/src/schemas.py
   - Add list_materials() function to services/llm-agent/src/routes/chat.py
   - Register GET /chat/materials route
   - Test with curl

3. **Verify all services healthy** (10 min)
   - Check docker ps for all container health
   - Test each endpoint with curl
   - Verify database connections
   - Check service logs for errors

### Phase 2: UI Testing - Feature by Feature (65 minutes)

4. **Test Chat Feature** (15 min)
   - Start Playwright MCP session
   - Navigate to http://localhost:3001
   - Login with test credentials
   - Navigate to /dashboard/chat
   - Send test message
   - Verify response from Bedrock
   - Screenshot results
   - Document in tests/e2e/test_chat.md
   - Fix any errors before proceeding

5. **Test Materials Upload** (15 min)
   - Use existing Playwright session
   - Navigate to /dashboard/materials
   - Upload test material
   - Verify material appears in list
   - Screenshot results
   - Document in tests/e2e/test_materials.md
   - Fix any errors before proceeding

6. **Test Transcription** (20 min)
   - Create 5-second test audio file
   - Navigate to /dashboard/transcribe
   - Upload audio file
   - Wait for processing completion
   - Verify transcript appears
   - Screenshot results
   - Document in tests/e2e/test_transcription.md
   - Fix any errors before proceeding

7. **Test Text-to-Speech** (15 min)
   - Navigate to /dashboard/tts
   - Enter test text
   - Generate speech
   - Verify audio plays
   - Screenshot results
   - Document in tests/e2e/test_tts.md
   - Fix any errors before proceeding

### Phase 3: Cleanup and Documentation (10 minutes)

8. **Clean up root directory** (5 min)
   - Move UI-COMPLETE-TEST-REPORT.md to docs/
   - Move FINAL-UI-TEST-STATUS.md to docs/
   - Move test_bedrock_direct.py to tests/
   - Verify root directory is clean

9. **Create final test report** (5 min)
   - Compile all test results
   - Document any issues found and fixed
   - Create FINAL_TESTING_REPORT.md in docs/
   - Include screenshots
   - List all 6 features as TESTED and WORKING

### Phase 4: Verification (10 minutes)

10. **Final end-to-end verification** (10 min)
    - Run through all 6 features one more time
    - Verify no console errors
    - Verify all features work as expected
    - Close Playwright session
    - Mark task as complete

**Total Estimated Time: 115 minutes (~2 hours)**

## Critical Success Criteria

1. ✅ All Docker services running and healthy
2. ✅ TTS API accepts JSON request body and returns base64 audio
3. ✅ Materials list endpoint returns user's materials
4. ✅ Chat sends message and receives Bedrock response
5. ✅ Materials upload saves and displays in list
6. ✅ Transcription processes audio and returns transcript
7. ✅ TTS generates playable audio
8. ✅ All 6 features documented and tested
9. ✅ Root directory cleaned of test files
10. ✅ Zero tolerance: Each feature must work before moving to next

## Risk Mitigation

**Risk 1: Bedrock API timeout or rate limiting**
- Mitigation: Use shorter test messages
- Mitigation: Add timeout handling in UI
- Fallback: Document issue and continue testing other features

**Risk 2: Azure TTS API failures**
- Mitigation: Verify credentials before testing
- Mitigation: Use shorter test text
- Fallback: Document issue, focus on other features

**Risk 3: Transcription takes too long**
- Mitigation: Use very short (5 second) audio files
- Mitigation: Increase polling interval
- Fallback: Document async nature, verify job queuing works

**Risk 4: Playwright MCP connection issues**
- Mitigation: Test Playwright connection before starting
- Mitigation: Keep sessions short
- Fallback: Document manual testing steps

## Success Metrics

- 6/6 features tested and working (100%)
- 0 untested features remaining
- 0 critical bugs blocking usage
- All test documentation created
- Root directory cleaned
- Ready for production deployment
