**Last Updated:** November 4, 2025

# Phase 10: Backlog Completion - Implementation Plan

**Created**: November 3, 2025  
**Status**: Ready to Implement  
**Estimated Effort**: 3-5 weeks  
**Priority**: Address critical issues first, then deploy remaining services

> **⚠️ IMPORTANT UPDATE**: This original plan has been analyzed using sequential thinking (MCP tool). See **[PHASE10-ENHANCED-PLAN.md](./PHASE10-ENHANCED-PLAN.md)** for realistic timelines (5-7 weeks full or 3 weeks MVP) and strategic implementation approach. The enhanced plan provides deeper analysis, identifies risks, and recommends an MVP-first strategy.

---

## Current State Assessment

### ✅ Working Features (Alpha 0.9)
- Authentication service
- LLM Chat with RAG
- Speech-to-Text transcription
- Audio recording
- Async job processing
- API Gateway (for core services)
- Basic dashboard UI

### ❌ Not Working / Not Deployed
- Text-to-Speech (broken)
- 7 Phase 4+ services (code exists but not deployed/tested)
- Multiple UI pages with no backend

---

## Phase 10 Sprint Plan

### Sprint 1: Fix Text-to-Speech (CRITICAL)
**Duration**: 2-3 days  
**Priority**: HIGH

#### Tasks
1. **Decision: Choose TTS Provider**
   - [ ] Review Azure TTS cost vs Coqui complexity
   - [ ] If Azure: Get API key, add to .env
   - [ ] If Coqui: Fix Docker build issues from poc/11.1-coqui-tts
   - [ ] If Alternative: Research Google Cloud TTS or AWS Polly

2. **Fix TTS Service**
   - [ ] Update services/text-to-speech/Dockerfile with working configuration
   - [ ] Test TTS generation locally
   - [ ] Fix services/text-to-speech/src/services/*.py
   - [ ] Verify audio file generation and streaming

3. **Test End-to-End**
   - [ ] Use browser to test /dashboard/tts page
   - [ ] Verify audio plays in browser
   - [ ] Test with different text lengths
   - [ ] Test error handling

**Success Criteria**: TTS page generates and plays audio without errors

---

### Sprint 2: Deploy Gamification Service (EASIEST FIRST)
**Duration**: 1-2 days  
**Priority**: MEDIUM

#### Tasks
1. **Fix Docker Configuration**
   - [ ] services/gamification/Dockerfile already correct
   - [ ] Verify all dependencies in requirements.txt
   - [ ] Check .env configuration

2. **Start Service**
   - [ ] Run `docker-compose up -d gamification-service`
   - [ ] Check logs: `docker logs lm-gamification`
   - [ ] Verify container is healthy
   - [ ] Test health endpoint

3. **Add to Nginx Gateway**
   - [ ] Add to services/api-gateway/nginx.conf:
     ```nginx
     upstream gamification_service {
         server lm-gamification:8011;
     }
     
     location /api/points/ {
         proxy_pass http://gamification_service/points/;
         # ... proxy headers
     }
     location /api/achievements/ {
         proxy_pass http://gamification_service/achievements/;
     }
     location /api/leaderboards/ {
         proxy_pass http://gamification_service/leaderboards/;
     }
     ```
   - [ ] Restart nginx: `docker-compose restart nginx`

4. **Test Endpoints**
   - [ ] GET /api/points/user/{user_id}
   - [ ] POST /api/achievements/unlock
   - [ ] GET /api/leaderboards/global
   - [ ] Verify in browser console

**Success Criteria**: All gamification endpoints return 200 OK

---

### Sprint 3: Deploy Notifications Service
**Duration**: 1-2 days  
**Priority**: HIGH (fixes dashboard errors)

#### Tasks
1. **Fix Dockerfile**
   - [ ] Update services/notifications/Dockerfile (already partially fixed)
   - [ ] Verify paths are correct
   - [ ] Test Docker build

2. **Start Service**
   - [ ] Build: `docker-compose build notifications-service`
   - [ ] Start: `docker-compose up -d notifications-service`
   - [ ] Check logs for errors
   - [ ] Verify database connection

3. **Add to Nginx**
   - [ ] Add upstream and location blocks
   - [ ] Restart nginx
   - [ ] Test with curl

4. **Test in Dashboard**
   - [ ] Notification bell should load without errors
   - [ ] Create test notification
   - [ ] Verify unread count updates

**Success Criteria**: Notification bell works, no console errors

---

### Sprint 4: Deploy Study Analytics Service
**Duration**: 1-2 days  
**Priority**: MEDIUM

#### Tasks
1. **Fix Dockerfile**
   - [ ] Update services/study-analytics/Dockerfile with correct paths:
     ```dockerfile
     COPY services/study-analytics/requirements.txt .
     COPY shared/python-common /tmp/lm-common
     RUN pip install --no-cache-dir /tmp/lm-common
     COPY services/study-analytics/src ./src
     ```

2. **Deploy**
   - [ ] Build and start service
   - [ ] Add to nginx
   - [ ] Test /api/sessions/ and /api/goals/ endpoints

3. **Test Functionality**
   - [ ] Create study session
   - [ ] Set a goal
   - [ ] Track progress
   - [ ] Verify data persists

**Success Criteria**: Sessions and goals API work end-to-end

---

### Sprint 5: Deploy Class Management Service
**Duration**: 1-2 days  
**Priority**: MEDIUM

#### Tasks
1. **Fix Port Configuration**
   - [ ] docker-compose.yml shows 8006:8005 mapping
   - [ ] Either fix to 8006:8000 OR update service to listen on 8005
   - [ ] Verify in services/class-management/src/config.py

2. **Deploy and Test**
   - [ ] Start service
   - [ ] Add to nginx (use correct internal port)
   - [ ] Test class CRUD operations
   - [ ] Test assignment creation
   - [ ] Test grade submission

**Success Criteria**: Can create class, add assignments, view roster

---

### Sprint 6: Deploy Content Capture Service
**Duration**: 2-3 days  
**Priority**: MEDIUM

#### Tasks
1. **Debug Unhealthy Status**
   - [ ] Check why container is unhealthy
   - [ ] Review logs: `docker logs lm-content-capture`
   - [ ] Fix missing dependencies (OCR, vector DB)
   - [ ] Verify ChromaDB connection

2. **Fix and Deploy**
   - [ ] Install Tesseract or configure OCR provider
   - [ ] Test vector embedding
   - [ ] Fix PDF processing
   - [ ] Test photo upload and OCR

3. **Add to Nginx and Test**
   - [ ] Add /api/photos/ and /api/textbooks/ routes
   - [ ] Test photo upload
   - [ ] Test textbook PDF processing
   - [ ] Verify OCR text extraction

**Success Criteria**: Can upload photo, extract text, search content

---

### Sprint 7: Deploy AI Study Tools Service
**Duration**: 2-3 days  
**Priority**: HIGH (core feature)

#### Tasks
1. **Fix 500 Errors**
   - [ ] Check logs: `docker logs lm-ai-study-tools`
   - [ ] Verify AWS Bedrock credentials in .env
   - [ ] Test AI service connection
   - [ ] Fix any import or dependency errors

2. **Deploy and Configure**
   - [ ] Ensure service connects to Bedrock/Ollama
   - [ ] Add to nginx gateway
   - [ ] Test each endpoint separately

3. **Test Features**
   - [ ] Generate study notes from content
   - [ ] Create flashcards from notes
   - [ ] Generate practice tests
   - [ ] Verify AI quality

**Success Criteria**: Can generate notes, flashcards, and tests successfully

---

### Sprint 8: Deploy Social Collaboration Service
**Duration**: 2-3 days  
**Priority**: LOW

#### Tasks
1. **Fix Connection Issues**
   - [ ] Container not starting (port 8010)
   - [ ] Check Dockerfile
   - [ ] Verify dependencies
   - [ ] Start service

2. **Deploy**
   - [ ] Add to nginx
   - [ ] Test friend connections
   - [ ] Test group creation
   - [ ] Test content sharing

**Success Criteria**: Can connect with friends, create groups, share content

---

### Sprint 9: Integration Testing
**Duration**: 3-5 days  
**Priority**: HIGH

#### Tasks
1. **Service Integration**
   - [ ] Test all services work together
   - [ ] Verify data flows between services
   - [ ] Test concurrent users
   - [ ] Check for race conditions

2. **UI Integration**
   - [ ] Test all dashboard pages
   - [ ] Verify no console errors
   - [ ] Test navigation flows
   - [ ] Check mobile responsive

3. **Performance Testing**
   - [ ] Load test with 10 concurrent users
   - [ ] Measure response times
   - [ ] Identify bottlenecks
   - [ ] Optimize slow queries

4. **Security Review**
   - [ ] Test JWT token expiration
   - [ ] Verify CORS configuration
   - [ ] Check SQL injection vulnerabilities
   - [ ] Test file upload limits

**Success Criteria**: All features work without errors under normal load

---

### Sprint 10: Error Handling & Polish
**Duration**: 2-3 days  
**Priority**: MEDIUM

#### Tasks
1. **Graceful Degradation**
   - [ ] Hide UI components when services aren't available
   - [ ] Show friendly error messages instead of console errors
   - [ ] Add "Coming Soon" badges for undeployed features
   - [ ] Implement retry logic for failed API calls

2. **User Experience**
   - [ ] Add loading spinners
   - [ ] Improve error messages
   - [ ] Add success notifications
   - [ ] Implement optimistic UI updates

3. **Documentation**
   - [ ] Update README with accurate feature list
   - [ ] Create deployment runbook
   - [ ] Document known limitations
   - [ ] Create troubleshooting guide

**Success Criteria**: Professional user experience even when services fail

---

## Detailed Task Breakdown by Service

### Text-to-Speech Service Tasks

**Files to Modify**:
- `services/text-to-speech/Dockerfile`
- `services/text-to-speech/.env`
- `services/text-to-speech/src/services/azure_tts.py` OR
- `services/text-to-speech/src/services/coqui_tts.py`

**Steps**:
```bash
# Option A: Azure TTS (Paid but Reliable)
1. Get Azure Speech API key
2. Add to services/text-to-speech/.env:
   AZURE_SPEECH_KEY=your_key_here
3. docker-compose restart tts-service
4. Test: curl POST http://localhost/api/tts/generate

# Option B: Coqui TTS (Free but Complex)
1. Review poc/11.1-coqui-tts/INSTALLATION-FAILED.md
2. Fix Docker build issues
3. Test locally before containerizing
4. Deploy once working
```

**Testing**:
- Generate short text (<100 chars)
- Generate long text (>1000 chars)
- Test different voices
- Verify audio format (WAV/MP3)
- Test streaming vs download

---

### Gamification Service Tasks

**Files to Review**:
- `services/gamification/src/main.py`
- `services/gamification/src/routes/*.py`
- `services/gamification/Dockerfile`

**Deployment Steps**:
```bash
1. docker-compose build gamification-service
2. docker-compose up -d gamification-service
3. docker logs -f lm-gamification
4. # If successful, add to nginx
5. Test endpoints with curl
```

**Nginx Routes to Add**:
```nginx
upstream gamification_service {
    server lm-gamification:8011;
}

location /api/points/ {
    proxy_pass http://gamification_service/points/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /api/achievements/ {
    proxy_pass http://gamification_service/achievements/;
    # ... same headers
}

location /api/leaderboards/ {
    proxy_pass http://gamification_service/leaderboards/;
    # ... same headers
}
```

---

### Notifications Service Tasks

**Already Started**: Dockerfile partially fixed, service in docker-compose.yml

**Remaining Steps**:
```bash
1. Fix Dockerfile completely (paths already updated)
2. docker-compose build notifications-service
3. docker-compose up -d notifications-service
4. Check logs for errors
5. Add nginx routes
6. Test notification creation and retrieval
```

**Expected Result**: Dashboard notification bell works without errors

---

### Study Analytics Service Tasks

**Dockerfile Needs Fix**:
```dockerfile
# Line 12: Change
COPY requirements.txt .
# To:
COPY services/study-analytics/requirements.txt .

# After line 13, add:
COPY shared/python-common /tmp/lm-common
RUN pip install --no-cache-dir /tmp/lm-common && rm -rf /tmp/lm-common

# Line 16: Change
COPY . .
# To:
COPY services/study-analytics/src ./src
```

**Deployment**:
```bash
1. Fix Dockerfile
2. docker-compose build study-analytics-service
3. docker-compose up -d study-analytics-service
4. Add nginx routes
5. Test session tracking and goal management
```

---

### Class Management Service Tasks

**Port Issue to Fix**:
- docker-compose.yml: `ports: - "8006:8005"`
- But nginx expects lm-class-mgmt:8005
- **Fix**: Change to `ports: - "8006:8000"` AND update service to listen on 8000
- OR: Keep as-is and use 8005 in nginx upstream

**Steps**:
```bash
1. Decide on port configuration
2. Update either docker-compose.yml OR nginx.conf
3. Rebuild if needed
4. Test class and assignment endpoints
```

---

### Content Capture Service Tasks

**Currently**: Container unhealthy

**Debug Steps**:
```bash
1. docker logs lm-content-capture --tail 100
2. Identify error (likely missing OCR or vector DB)
3. Fix Dockerfile to install Tesseract
4. Verify ChromaDB connection
5. Restart and retest
```

**Likely Issues**:
- Tesseract OCR not installed
- ChromaDB connection failing
- Missing Python packages
- File upload path issues

---

### AI Study Tools Service Tasks

**Currently**: Returns 500 errors

**Debug Steps**:
```bash
1. docker logs lm-ai-study-tools --tail 100
2. Check AWS Bedrock credentials in .env
3. Verify service can reach Bedrock API
4. Test AI generation locally first
5. Fix and redeploy
```

**Testing Plan**:
- Generate notes from uploaded content
- Create flashcards from notes
- Generate practice test
- Verify quality of AI outputs

---

### Social Collaboration Service Tasks

**Currently**: Connection refused (not running)

**Steps**:
```bash
1. Check why container isn't starting
2. Review Dockerfile
3. Start service: docker-compose up -d social-collaboration-service
4. Add to nginx
5. Test friend, group, and sharing features
```

---

## Nginx Configuration Strategy

**Current Approach**: Only add routes for deployed services

**Process for Each Service**:
1. Deploy service and verify it's running
2. Add upstream definition to nginx.conf
3. Add location blocks for service routes  
4. Restart nginx: `docker-compose restart nginx`
5. Test routes with curl before UI testing

**Example Template**:
```nginx
upstream {service}_service {
    server lm-{container-name}:{internal-port};
}

location /api/{route}/ {
    proxy_pass http://{service}_service/{route}/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    # Add timeouts for slow operations
    # Add client_max_body_size for file uploads
}
```

---

## Testing Checklist (Per Service)

For each deployed service, complete this checklist:

### Service Deployment
- [ ] Dockerfile builds successfully
- [ ] Container starts and stays running
- [ ] Container passes health check
- [ ] Service connects to database
- [ ] Service connects to required dependencies (Redis, ChromaDB, etc.)

### Nginx Configuration
- [ ] Upstream added to nginx.conf
- [ ] Location blocks added
- [ ] Nginx config validated
- [ ] Nginx restarted successfully
- [ ] Routes resolve (not 404)

### API Testing
- [ ] All GET endpoints return data or empty arrays
- [ ] POST endpoints create resources
- [ ] PUT endpoints update resources
- [ ] DELETE endpoints remove resources
- [ ] Error cases return appropriate status codes

### UI Testing
- [ ] Dashboard page loads without errors
- [ ] Can interact with UI components
- [ ] Data displays correctly
- [ ] Forms submit successfully
- [ ] Error messages display appropriately

---

## Risk Mitigation

### If Services Won't Start
1. Check Docker logs immediately
2. Verify environment variables
3. Test database connection manually
4. Simplify service to minimal working state
5. Add features incrementally

### If Nginx Won't Start
1. Comment out new routes
2. Restart nginx with minimal config
3. Add routes back one at a time
4. Test after each addition

### If Endpoints Return 500
1. Check service logs
2. Verify database schema matches code
3. Test service endpoint directly (bypass nginx)
4. Fix error and redeploy
5. Clear Docker cache if needed

---

## Definition of Done

A service is considered "complete" when:
1. ✅ Container runs successfully
2. ✅ Nginx routes traffic to it
3. ✅ All API endpoints return correct responses
4. ✅ UI pages work without console errors
5. ✅ End-to-end user workflow tested
6. ✅ Error cases handled gracefully
7. ✅ Changes committed to git

---

## Priority Matrix

| Service | Priority | Complexity | User Impact | Recommended Order |
|---------|----------|------------|-------------|-------------------|
| Text-to-Speech | HIGH | Medium | High | 1st (Sprint 1) |
| Notifications | HIGH | Low | Medium | 3rd (Sprint 3) |
| AI Study Tools | HIGH | High | High | 7th (after easier ones) |
| Gamification | MEDIUM | Low | Low | 2nd (Sprint 2) |
| Study Analytics | MEDIUM | Low | Medium | 4th (Sprint 4) |
| Class Management | MEDIUM | Medium | High | 5th (Sprint 5) |
| Content Capture | MEDIUM | High | Medium | 6th (Sprint 6) |
| Social Collab | LOW | Medium | Low | 8th (if time) |

---

## Alternative: Minimum Viable Product (MVP) Approach

If 3-5 weeks is too long, consider MVP:

### Option A: Keep Only Working Features
**Time**: 1-2 days

**Tasks**:
- [ ] Remove non-working dashboard pages from UI
- [ ] Update README to list only working features
- [ ] Add "Roadmap" section for future features
- [ ] Clean up console errors
- [ ] Polish existing features
- [ ] Call it "Alpha 1.0 - Core Features"

### Option B: Deploy Top 3 Services Only
**Time**: 1 week

**Deploy**:
1. Text-to-Speech (fixes broken feature)
2. Notifications (fixes dashboard errors)
3. Gamification (adds engagement)

**Skip**: Classes, Content, AI Tools, Social, Analytics

**Document** remaining as "Phase 11" for future

---

## Recommendations

1. **Start with TTS** - It's broken and expected to work
2. **Deploy services incrementally** - One at a time, test thoroughly
3. **Update BACKLOG.md** as you complete each sprint
4. **Don't rush** - Broken deployments create more work than careful deployments
5. **Test end-to-end** - Don't just check if container runs

---

## Next Steps

Choose your approach:

**Full Completion** (3-5 weeks):
- Follow Sprint 1-10 sequentially
- Deploy all services
- Complete all testing
- Polish everything

**MVP** (1-2 days):
- Clean up UI
- Document limitations
- Focus on polish
- Call it complete

**Hybrid** (1-2 weeks):
- Fix TTS
- Deploy 2-3 key services
- Document rest as roadmap
- Good balance of effort/value

Whichever you choose, update this document as you progress.
