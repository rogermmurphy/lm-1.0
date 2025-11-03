# Task: Fix Little Monster UI Authentication & Complete Build

## Task Overview

**Goal**: Debug and fix the broken UI authentication, then complete the full UI build with zero tolerance for errors.

**Status**: UI renders correctly but authentication is completely broken (422 errors). Must fix auth first, then build remaining features.

**Approach**: Use Playwright MCP to inspect actual HTTP requests/responses, identify root cause, fix issues, then complete build with proper testing.

## MANDATORY Reading (Read ALL Before Starting)

### Critical Context (MUST READ FIRST - Priority Order):
1. **`views/web-app/FINAL-STATUS.md`** - Current state, all known issues
2. **`views/web-app/UI-CRITICAL-ISSUES.md`** - Detailed problem analysis  
3. **`DEVELOPER-HANDOVER.md`** - Handover from previous developer
4. **`views/web-app/src/lib/api.ts`** - Current API client implementation
5. **`services/authentication/src/schemas.py`** - Backend data schemas
6. **`services/authentication/src/routes/auth.py`** - Auth endpoint implementation
7. **`views/web-app/src/contexts/AuthContext.tsx`** - Current auth logic

### Project Understanding (MUST READ):
8. **`README.md`** - Project overview
9. **`docs/PROJECT-CHARTER.md`** - Vision, mission, objectives
10. **`docs/TECHNICAL-ARCHITECTURE.md`** - System architecture
11. **`docs/REQUIREMENTS.md`** - Functional requirements
12. **`TESTING-RESULTS.md`** - Backend testing status

### Testing Standards (MUST READ):
13. **`old/Ella-Ai/.clinerules/zero-tolerance-testing.md`** - Testing philosophy
14. **`old/Ella-Ai/.clinerules/functional-testing-requirement.md`** - What counts as tested
15. **`old/Ella-Ai/.clinerules/testing-standards.md`** - Testing best practices

## Current State

### What Works ✅:
- Backend: 13 Docker containers running, all services healthy
- UI Rendering: All pages display correctly
- Navigation: Users can click between pages
- Forms: Accept input correctly
- API Gateway: Routes to services (nginx recently fixed)

### What's Broken ❌:
- **Registration**: Returns 422 errors, cannot create accounts
- **Login**: Untested (no accounts exist to test with)
- **Authentication**: Completely non-functional
- **Dashboard**: Cannot access (requires auth)
- **All Features**: Unusable without auth

## Phase 1: Debug Authentication (Use Playwright MCP)

### Step 1: Inspect Actual HTTP Requests

Use Playwright MCP to:
1. Navigate to registration page
2. Fill out form
3. Click submit
4. **CAPTURE the actual HTTP request** (headers, body, format)
5. **CAPTURE the 422 response** (error details)

**Playwright MCP Tools Available:**
- `playwright_navigate` - Go to page
- `playwright_fill` - Fill form fields
- `playwright_click` - Click buttons
- `playwright_get_visible_html` - See page source
- Browser dev tools to inspect network requests

### Step 2: Compare Request vs Schema

**Backend Expects** (from `services/authentication/src/schemas.py`):
```python
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    username: Optional[str] = Field(None, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
```

**UI Sends** (from `views/web-app/src/lib/api.ts`):
```typescript
register: (email: string, password: string, username?: string) =>
  api.post('/api/auth/register', { email, password, username })
```

**Question**: Why is this failing? Inspect the actual request to find out.

### Step 3: Fix Data Format Issues

Based on Step 1 findings:
- Fix request payload format
- Fix headers (Content-Type, etc.)
- Fix any serialization issues
- Test until 422 error is resolved

### Step 4: Test Registration End-to-End

**Success Criteria**:
- User fills registration form
- Clicks "Sign up"
- Account created in database
- JWT tokens received and stored
- User redirected to dashboard
- **Screenshot evidence of success**

## Phase 2: Complete Authentication

### Step 5: Test Login Workflow

With registered account from Step 4:
- Navigate to login page
- Enter credentials
- Submit form
- Verify tokens received
- Verify dashboard access
- **Screenshot evidence**

### Step 6: Test Protected Routes

- Verify non-authenticated users redirected to login
- Verify authenticated users can access dashboard
- Test logout clears session
- **Screenshot evidence**

## Phase 3: Build Remaining Features

### Step 7: Audio Transcription Page

**Requirements** (from docs/REQUIREMENTS.md FR-3):
- File upload component
- Support MP3, WAV, M4A formats
- Upload progress indicator
- Job status polling
- Display transcription results
- Download transcript

**API**: POST `/api/transcribe/`, GET `/api/transcribe/jobs/{id}`

### Step 8: Text-to-Speech Page

**Requirements** (from docs/REQUIREMENTS.md FR-4):
- Text input area
- Voice selection
- Generate button
- Audio playback controls
- Download audio

**API**: POST `/api/tts/generate`

### Step 9: Materials Management Page

**Requirements** (from docs/REQUIREMENTS.md FR-7):
- List uploaded materials
- Upload new files (PDF, DOCX, TXT, MD)
- Delete materials
- Show indexing status
- Material preview

**API**: POST `/api/chat/materials`, GET `/api/chat/materials`

## Phase 4: Containerization & Final Testing

### Step 10: Containerize UI

Create `views/web-app/Dockerfile`:
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production
EXPOSE 3000
CMD ["npm", "start"]
```

### Step 11: Add to docker-compose.yml

```yaml
web-app:
  build: ./views/web-app
  container_name: lm-web-app
  ports:
    - "3000:3000"
  environment:
    - NEXT_PUBLIC_API_URL=http://localhost
  networks:
    - lm-network
  depends_on:
    - api-gateway
```

### Step 12: End-to-End Testing

Test complete user journeys:
1. Register → Login → Chat → Logout
2. Register → Upload Audio → Transcribe → View Results
3. Register → Generate TTS → Play Audio
4. Register → Upload Material → See in Chat Context

**Document with screenshots for each workflow**

## Testing Requirements (Zero Tolerance)

### What Counts as "Working":
- ✅ User completes full workflow
- ✅ Data persists in database
- ✅ Features produce expected results
- ✅ Error cases handled gracefully
- ✅ Screenshot evidence provided

### What Does NOT Count:
- ❌ Page renders (not enough)
- ❌ API returns 200 (without verifying result)
- ❌ "Should work" (must actually test)
- ❌ Claiming complete without screenshots

## Known Issues to Fix

### Issue #1: Registration 422 Error (TOP PRIORITY)
**Symptoms**: Backend returns "422 Unprocessable Entity"
**Impact**: Cannot create accounts, entire system unusable
**Debug Steps**:
1. Use Playwright to capture actual request
2. Compare to backend schema
3. Fix format mismatch
4. Test until it works

### Issue #2: Login Untested
**Symptoms**: Unknown if it works (no accounts to test)
**Depends On**: Issue #1 must be fixed first
**Test After**: Registration works

### Issue #3: JWT Token Handling
**Current**: AuthContext decodes JWT for user info
**Verify**: Tokens stored correctly, refresh works, logout clears

## Success Criteria

Task is complete when:
- [ ] Registration works (user can create account)
- [ ] Login works (user can authenticate)
- [ ] Dashboard accessible (protected routes work)
- [ ] Chat works (can send/receive messages)
- [ ] Transcription works (can upload and transcribe audio)
- [ ] TTS works (can generate and play speech)
- [ ] Materials work (can upload and manage files)
- [ ] Logout works (session cleared)
- [ ] UI containerized (runs in Docker)
- [ ] All workflows documented with screenshots
- [ ] Zero tolerance testing applied to everything

## Tools Available

### Playwright MCP Server:
- Full browser automation
- Network request inspection
- Form filling and submission
- Screenshot capture
- Console log monitoring
- HTML inspection

### Development Server:
```bash
cd views/web-app
npm run dev  # Runs on http://localhost:3001
```

### Backend Services:
- All running in Docker
- API docs at `http://localhost:PORT/docs`
- Logs via `docker logs lm-SERVICENAME`

## Previous Mistakes to Avoid

1. **Don't claim complete without testing** - Previous dev claimed 50%, actually 15%
2. **Test early and often** - Don't wait until "done" to test
3. **Use Playwright MCP** - Inspect actual requests, don't guess
4. **Document honestly** - Show what works AND what doesn't
5. **Follow zero tolerance** - Feature isn't done until user completes workflow

## Expected Timeline

- **Phase 1** (Debug Auth): 2-3 hours
- **Phase 2** (Complete Auth): 1 hour
- **Phase 3** (Build Features): 4-6 hours
- **Phase 4** (Containerize/Test): 2 hours
- **Total**: 9-12 hours for complete, working UI

## Deliverables

At completion, provide:
1. Updated documentation with test results
2. Screenshots proving each workflow works
3. Dockerfile for UI container
4. Updated docker-compose.yml
5. Final test report with evidence
6. Honest assessment of completion percentage

---

**Start Date**: TBD  
**Priority**: HIGH - Platform unusable without working UI  
**Difficulty**: MEDIUM - Issues are known, just need proper debugging
