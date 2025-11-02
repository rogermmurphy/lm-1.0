# Little Monster - Developer Handover

**Last Updated**: 2025-11-02 1:47 PM  
**Status**: Phases 1-2 Complete, 83% Features Working

---

## CURRENT STATE

### Services Running (8 total):
1. auth-service (8001) - JWT authentication
2. llm-service (8005) - AI chat with Bedrock Claude Sonnet 4
3. stt-service (8002) - Whisper transcription
4. tts-service (8003) - Azure TTS (BLOCKED by Docker issue)
5. recording-service (8004) - Audio file management
6. jobs-worker - Background async processing
7. class-management (8006) - Phase 1: Classes and assignments
8. content-capture (8008) - Phase 2: OCR, PDF, vector search

### Database: 19 tables deployed
- Core: 12 tables
- Phase 1: 4 tables (classes, assignments, planner_events, class_schedules)
- Phase 2: 3 tables (photos, textbooks, textbook_chunks)

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
- ❌ Phase 3 (AI Study Tools): 0% (schema created only)
- ❌ Phase 4-6: Not started

---

## DOCUMENTATION

Core docs in `docs/`:
- project-charter.md - Vision
- requirements.md - Features
- technical-architecture.md - System design
- architecture-diagrams.md - Visuals
- implementation-roadmap.md - Sprint plan
- project-status.md - Testing results

See `IMPLEMENTATION-STATUS.md` for detailed current state.

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
