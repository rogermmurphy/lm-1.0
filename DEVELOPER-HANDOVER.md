# Little Monster - Developer Handover

**Last Updated**: 2025-11-02 5:15 PM  
**Status**: Phases 1-5 Complete, All Backend Services Tested ✅

---

## CURRENT STATE

### Services Running (11 total):
1. auth-service (8001) - JWT authentication ✅
2. llm-service (8005) - AI chat with Bedrock Claude Sonnet 4 ✅
3. stt-service (8002) - Whisper transcription ✅
4. tts-service (8003) - Azure TTS ⚠️
5. recording-service (8004) - Audio file management ✅
6. jobs-worker - Background async processing ✅
7. class-management (8006) - Phase 1: Classes/assignments ✅
8. content-capture (8008) - Phase 2: OCR, PDF, vector search ✅
9. ai-study-tools (8009) - Phase 3: AI notes, tests, flashcards ✅
10. social-collaboration (8010) - Phase 4: Groups, connections, sharing ✅
11. gamification (8011) - Phase 5: Points, achievements, leaderboards ✅

### Database: 35 tables deployed
- Core: 12 tables
- Phase 1: 4 tables (classes, assignments, planner_events, class_schedules)
- Phase 2: 3 tables (photos, textbooks, textbook_chunks)
- Phase 3: 7 tables (ai_notes, ai_tests, test_questions, flashcard_decks, flashcards, study_sessions, session_cards)
- Phase 4: 5 tables (classmate_connections, shared_content, study_groups, study_group_members, study_group_messages)
- Phase 5: 4 tables (user_points, achievements, leaderboards, point_transactions)

### Infrastructure:
- PostgreSQL (5432), Redis (6379), ChromaDB (8000), Ollama (11434)
- Nginx API Gateway (80)
- Next.js Web App (3000)

---

## WHAT WORKS (5/6 features = 83%)

1. ✅ User Registration - Full E2E tested
2. ✅ User Login - JWT tokens working
3. ✅ AI Chat - Bedrock Claude Sonnet 4 responding
4. ✅ Materials Upload - Vector indexing working
5. ✅ Class Management - CRUD operations working
6. ❌ Text-to-Speech - BLOCKED (Azure SDK Docker issue)

---

## CRITICAL ISSUES

### TTS Service Blocked:
**Problem**: Azure SDK RuntimeError 2176 in Docker  
**Impact**: Text-to-speech feature completely non-functional  
**Solution**: Switch to Coqui TTS (tested in POC 11.1)

### Phase 2 Undocumented:
**Problem**: content-capture service exists but was never documented  
**Impact**: New developers don't know it exists  
**Solution**: This document now includes it

---

## QUICK START

```bash
# Start all services
docker-compose up -d

# Start web app
cd views/web-app && npm run dev

# Access at http://localhost:3000
# Login: testuser@example.com / password123
```

---

## KEY FILES

### Backend:
- `services/llm-agent/src/routes/chat.py` - AI chat
- `services/class-management/src/routes/classes.py` - Classes CRUD
- `services/content-capture/src/routes/photos.py` - OCR
- `services/content-capture/src/routes/textbooks.py` - PDF processing
- `shared/python-common/lm_common/` - Shared utilities

### Frontend:
- `views/web-app/src/lib/api.ts` - API client
- `views/web-app/src/contexts/AuthContext.tsx` - Auth state
- `views/web-app/src/app/dashboard/classes/page.tsx` - Classes UI
- `views/web-app/src/app/dashboard/assignments/page.tsx` - Assignments UI

### Config:
- `.env` - All credentials
- `docker-compose.yml` - Service orchestration
- `services/api-gateway/nginx.conf` - API routing

---

## CREDENTIALS

All in root `.env`:
- AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (Bedrock)
- AZURE_SPEECH_KEY (TTS - blocked)
- JWT_SECRET_KEY
- Database: postgres/postgres@localhost:5432/littlemonster

---

## TESTING

### Existing Tests:
- `tests/e2e/` - E2E test documentation (markdown)
- `services/*/test_service.py` - Service tests
- `tests/manual/` - Manual test scripts
- `qa/` - New organized test structure (empty, needs tests)

### What Needs Testing:
- content-capture service (Phase 2) - NO TESTS YET
- Transcription E2E workflow
- TTS after Coqui switch

---

## NEXT ACTIONS

### Immediate:
1. Fix TTS - Switch to Coqui TTS
2. Test content-capture service
3. Build Phase 2 frontend pages

### Short-term:
4. Complete transcription E2E test
5. Deploy schema 008 (AI study tools)
6. Build Phase 3 service

---

## PHASE STATUS

- ✅ Phase 1 (Class Management): 100% complete
- ✅ Phase 2 (Content Capture): Backend 100%, Frontend 0%
- ✅ Phase 3 (AI Study Tools): Backend 100% tested
- ✅ Phase 4 (Social & Collaboration): Backend 100%, UI tested with Playwright
- ✅ Phase 5 (Gamification): Backend 100% tested
- ❌ Phase 6+: Not started

---

## DOCUMENTATION

### Core Docs (`docs/`):
- project-charter.md - Vision
- requirements.md - Features
- technical-architecture.md - System design
- architecture-diagrams.md - Visuals
- implementation-roadmap.md - Sprint plan

### Phase Completion Docs:
- PHASE4-COMPLETE.md - Social & Collaboration (19 endpoints)
- PHASE4-UI-TEST-RESULTS.md - Playwright test evidence
- PHASE5-COMPLETE.md - Gamification (8 endpoints)
- PHASE5-IMPLEMENTATION-GUIDE.md - Implementation reference

### Implementation Status:
- IMPLEMENTATION-STATUS.md - Overall status
- services/*/PHASE*-STATUS.md - Per-service docs

### Test User:
- Email: testuser@test.com
- Password: Test123!
- User ID: 7

---

## TROUBLESHOOTING

### Service won't start:
```bash
docker-compose logs <service>
docker-compose restart <service>
```

### Database issues:
```bash
docker exec -it lm-postgres psql -U postgres littlemonster
\dt  # List tables
```

### Test endpoints:
```bash
curl http://localhost/api/auth/health
curl http://localhost/api/chat/materials
```

---

**Read IMPLEMENTATION-STATUS.md for complete current state.**
