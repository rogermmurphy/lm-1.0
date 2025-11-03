# Little Monster GPA - Project Backlog

**Last Updated**: November 3, 2025  
**Status**: Alpha 0.9 - Core Features Working, Extended Features Pending

---

## What "Phase 9 Complete" Actually Means

Phase 9 focused on **infrastructure, code organization, and production readiness preparation**. It included:
- ✅ Database schemas created for all features (12 schemas)
- ✅ Service scaffolding for 8 additional microservices
- ✅ UI components created for all planned features
- ✅ Docker configuration established
- ✅ Testing framework established

**However**, many features have code/schemas but are **NOT tested, deployed, or functional**.

---

## Currently Working Features (Alpha 0.9)

### Core Services ✅
- **Authentication** (lm-auth:8001) - Login, registration, sessions, password reset
- **LLM Agent/Chat** (lm-llm:8005) - Conversational AI, RAG, content loading
- **Speech-to-Text** (lm-stt:8002) - Audio transcription with Whisper
- **Audio Recording** (lm-recording:8004) - Recording management
- **Async Jobs** (lm-jobs worker) - Background job processing
- **API Gateway** (lm-gateway:80) - Nginx routing for core services

### Working UI Pages ✅
- Login/Registration
- Dashboard (main)
- Chat interface
- Transcribe audio page
- Materials upload page

---

## CRITICAL: Text-to-Speech NOT Working ⚠️

### Issue
TTS service container runs but audio generation **fails** with errors:
- Azure TTS: Works but requires paid API key
- Coqui TTS: Installation failed, Docker build issues
- Current workaround: Service returns 500 errors

### Why This Matters
- Users cannot listen to generated study notes
- AI-generated summaries cannot be read aloud
- Accessibility feature is broken

### To Fix
1. Choose TTS solution: Azure (paid, reliable) vs Coqui (free, complex setup)
2. Fix Docker configuration for chosen solution
3. Test audio generation end-to-end
4. Update UI to handle TTS responses

**Effort**: 2-3 days  
**Priority**: HIGH (affects user experience)

---

## Phase 4+ Services: Created But NOT Deployed ⚠️

All these services have:
- ✅ Database schemas
- ✅ Python service code
- ✅ FastAPI routes
- ✅ UI components
- ❌ NOT in docker-compose (except stubs)
- ❌ NOT tested
- ❌ NOT accessible via nginx gateway

### 1. Class Management Service
**Container**: lm-class-mgmt (exists but port mismatch)  
**Port**: Should be 8006 (currently mapped incorrectly)  
**Routes Needed**: `/api/classes/`, `/api/assignments/`

#### Features
- Create/edit classes
- Manage assignments
- Grade submissions
- Class roster

**Status**: Service exists, needs deployment testing  
**Effort**: 1-2 days

---

### 2. Content Capture Service
**Container**: lm-content-capture:8008 (exists, unhealthy)  
**Routes Needed**: `/api/photos/`, `/api/textbooks/`

#### Features
- Photo capture from textbooks
- OCR text extraction
- PDF processing
- Vector embedding for search

**Status**: Container exists but unhealthy, needs debugging  
**Effort**: 2-3 days

---

### 3. AI Study Tools Service
**Container**: lm-ai-study-tools:8009 (exists)  
**Routes Needed**: `/api/notes/`, `/api/flashcards/`, `/api/tests/`

#### Features
- AI-generated study notes
- Flashcard generation from content
- Practice test creation
- Quiz generation

**Status**: Container runs, returns 500 errors, needs testing  
**Effort**: 2-3 days

---

### 4. Social Collaboration Service
**Container**: lm-social-collab:8010 (exists, connection refused)  
**Routes Needed**: `/api/connections/`, `/api/groups/`, `/api/sharing/`

#### Features
- Friend connections
- Study groups
- Content sharing
- Collaborative learning

**Status**: Container not running, needs deployment  
**Effort**: 2-3 days

---

### 5. Gamification Service
**Container**: lm-gamification:8011 (exists but not started)  
**Routes Needed**: `/api/points/`, `/api/achievements/`, `/api/leaderboards/`

#### Features
- Award points for activities
- Achievement system
- Leaderboards
- Badges and rewards

**Status**: Code ready, container not deployed  
**Effort**: 1-2 days

---

### 6. Study Analytics Service
**Container**: lm-analytics:8012 (not in docker-compose)  
**Routes Needed**: `/api/sessions/`, `/api/goals/`

#### Features
- Study session tracking
- Goal setting and tracking
- Performance analytics
- Progress reports

**Status**: Code ready, needs deployment  
**Effort**: 1-2 days

---

### 7. Notifications Service
**Container**: lm-notifications:8013 (not in docker-compose)  
**Routes Needed**: `/api/notifications/`, `/api/messages/`

#### Features
- Real-time notifications
- Message system
- Alert preferences
- Notification history

**Status**: Code ready, needs deployment  
**Effort**: 1-2 days

---

## Nginx Gateway Issues

### Current State
- ❌ Routes defined for non-existent services cause crash loop
- ✅ Temporarily removed to allow core services to work
- ❌ Need to add routes incrementally as services deploy

### Fix Required
1. Deploy one Phase 4+ service at a time
2. Add its upstream and routes to nginx.conf
3. Test before moving to next service
4. Document working configuration

**Effort**: Ongoing as services deploy

---

## UI Components Without Backend

These dashboard pages exist but have no working backend:
- `/dashboard/classes` - Class Management (service not deployed)
- `/dashboard/assignments` - Assignments (service not deployed)
- `/dashboard/flashcards` - Flashcards (AI service returns 500)
- `/dashboard/groups` - Study Groups (service not running)
- `/dashboard/notifications` - Notifications (service not deployed)
- `/dashboard/messages` - Messages (service not deployed)
- `/dashboard/tts` - Text-to-Speech (broken)

**Impact**: These pages will show errors/loading states indefinitely

---

## Docker Configuration Issues

### Services Missing from docker-compose.yml
- study-analytics-service (added but Dockerfile has path issues)
- notifications-service (added but Dockerfile has path issues)

### Port Mapping Issues
- class-management: 8006:8005 (should be 8006:8000 or fix service config)
- Multiple services have internal port mismatches

### Dockerfile Path Issues
Both new services need Dockerfile updates:
```dockerfile
# Wrong (current):
COPY requirements.txt .
COPY . .

# Correct (needed):
COPY services/{service-name}/requirements.txt .
COPY shared/python-common /tmp/lm-common
RUN pip install --no-cache-dir /tmp/lm-common && rm -rf /tmp/lm-common
COPY services/{service-name}/src ./src
```

**Effort**: 1 day to fix all Dockerfiles and port mappings

---

## Recommended Priority Order

### Sprint 1: Get Login Working Again (URGENT)
1. ✅ Fix nginx configuration (removed non-existent upstreams)
2. ✅ Restart nginx successfully
3. ⏳ Test login functionality
**Effort**: < 1 day  
**Status**: IN PROGRESS

### Sprint 2: Fix TTS (HIGH PRIORITY)
1. Choose TTS provider (Azure vs Coqui vs alternative)
2. Fix Docker configuration
3. Test audio generation
4. Update UI to handle responses properly
**Effort**: 2-3 days

### Sprint 3: Deploy One Phase 4+ Service (PROVE CONCEPT)
Choose easiest service (probably Gamification):
1. Fix Dockerfile
2. Start container
3. Add nginx routes
4. Test endpoints
5. Document process
**Effort**: 1-2 days

### Sprint 4-10: Deploy Remaining Services
One service at a time, following proven process:
- Class Management
- Content Capture (fix unhealthy status)
- AI Study Tools (fix 500 errors)
- Social Collaboration
- Study Analytics
- Notifications
**Effort**: 1-2 days each = 6-12 days total

### Sprint 11: Integration Testing
- Test all services together
- Fix integration issues
- Performance testing
- Security review
**Effort**: 3-5 days

---

## What Phase 9 Should Have Included (But Didn't)

Phase 9 was supposed to be "Production Readiness" but only covered:
- Code organization
- Schema creation
- Service scaffolding
- Testing framework

**It did NOT include:**
- Deploying the new services
- Testing the new services
- Fixing integration issues
- Making features actually work end-to-end

---

## Total Remaining Effort

- Fix TTS: 2-3 days
- Deploy 7 services: 7-14 days
- Integration testing: 3-5 days
- Bug fixes: 2-4 days
- **Total**: 14-26 days (3-5 weeks)

---

## Decision Needed

**Option A**: Minimal Viable Product (MVP)
- Keep only working features (auth, chat, STT, recording)
- Remove non-working UI pages
- Document as "Alpha 0.9 - Core Features"
- **Time**: 1-2 days

**Option B**: Complete All Features
- Follow Sprint 1-11 plan above
- Deploy all Phase 4+ services
- **Time**: 3-5 weeks

**Option C**: Hybrid Approach
- Fix TTS (high value)
- Deploy 2-3 most important services
- Document remaining as "roadmap"
- **Time**: 1-2 weeks

---

## Files to Update

When we clarify scope:
1. `PROJECT-COMPLETE.md` - Remove or rename (project not actually complete)
2. `docs/phases/PHASE9-COMPLETE.md` - Clarify what was actually completed
3. `README.md` - Update status and list working vs planned features
4. `docker-compose.yml` - Either fix or remove non-working services
5. `services/api-gateway/nginx.conf` - Keep clean with only working routes

---

## Questions to Answer

1. **Business Priority**: Which features are must-haves vs nice-to-haves?
2. **Timeline**: How much time can be invested in completing features?
3. **TTS Decision**: Azure paid vs Coqui free vs skip feature?
4. **Scope**: MVP (core only) vs Full (all features) vs Hybrid?
5. **Testing**: How much testing is required before considering "complete"?
