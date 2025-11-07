# Project Handover Instructions Template

**Last Updated:** [DATE]
**Project:** Little Monster GPA Platform
**Version:** Alpha 1.0
**Handover Type:** [Development Continuation / Bug Fix / Feature Addition / etc.]

---

## 🏗️ PROJECT OVERVIEW

### What is Little Monster?
AI-powered educational platform for college students featuring:
- AI tutoring with RAG (Retrieval Augmented Generation)
- Audio transcription (lecture → text)
- Text-to-speech (study materials → audio)
- Class and assignment management
- AI-generated study materials (flashcards, practice tests, notes)
- Notifications and messaging

### Architecture
**Type:** Microservices  
**Deployment:** Docker Compose (24 containers)
**Frontend:** Next.js 14 (React)
**Backend:** FastAPI (Python)
**Database:** PostgreSQL
**Gateway:** Nginx
**Cache/Queue:** Redis
**Vector DB:** ChromaDB
**LLM:** Ollama (local) + AWS Bedrock (cloud)

### Technology Stack

**Frontend:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- TailwindCSS
- Zustand (state) + React Query (server state)

**Backend:**
- FastAPI
- Python 3.11+
- Pydantic v2
- SQLAlchemy
- Alembic (migrations)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- PostgreSQL 15
- Redis 7
- ChromaDB
- Ollama

---

## 📁 PROJECT STRUCTURE

```
lm-1.0/
├── services/           # Backend microservices (13 services)
│   ├── authentication/ # JWT auth (port 8001)
│   ├── llm-agent/      # AI chat (port 8005)
│   ├── speech-to-text/ # Transcription (port 8002)
│   ├── text-to-speech/ # TTS (port 8003)
│   ├── audio-recording/# Recording (port 8004)
│   ├── class-management/ # Classes (port 8006)
│   ├── content-capture/  # OCR/PDF (port 8008)
│   ├── ai-study-tools/   # AI generation (port 8009)
│   ├── social-collaboration/ # Groups (port 8010)
│   ├── gamification/     # Points (port 8011)
│   ├── study-analytics/  # Analytics (port 8012)
│   ├── notifications/    # Notifications (port 8013)
│   └── async-jobs/       # Background worker
├── views/
│   └── web-app/        # Next.js frontend (port 3000)
├── database/
│   ├── schemas/        # SQL schema files
│   ├── migrations/     # Alembic migrations
│   └── seeds/          # Seed data
├── shared/
│   └── python-common/  # Shared Python utilities
├── docs/               # Documentation
├── tests/              # Test suites
├── scripts/            # Utility scripts
├── .clinerules/        # Development methodology
└── docker-compose.yml  # All services
```

---

## 🚀 DEVELOPMENT STANDARDS

### Build-First Requirement
From `.clinerules/build-and-deployment-workflow.md`:
- **ALWAYS** run `npm run build` before starting services
- Never skip build step
- Build catches compilation errors early

### Zero Tolerance Testing
From `.clinerules/zero-tolerance-testing.md`:
- Deploy → Test → Remediate → Deploy → Test cycle
- NO errors tolerated (except favicon 404)
- Test every change immediately
- Don't mark complete without verification

### Application Lifecycle
From `.clinerules/application-lifecycle-management.md`:
- Use `scripts/start-all.bat` to start services
- Use `scripts/stop-all.bat` to stop services  
- Never manually kill processes
- Let npm scripts handle cleanup

### Functional Testing
From `.clinerules/functional-testing-requirement.md`:
- Test ACTUAL user workflows
- "Service running" ≠ "Feature working"
- Must verify end-to-end functionality
- Document what was tested and results

---

## 🛠️ COMMON DEVELOPMENT TASKS

### Start the System

```bash
# Option 1: All containers
docker-compose up -d

# Option 2: Specific services
docker-compose up -d auth-service llm-service web-app nginx

# Option 3: Development frontend
cd views/web-app && npm run dev
```

### Stop the System

```bash
# All containers
docker-compose down

# Keep data (volumes)
docker-compose down --volumes
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker logs lm-auth --tail 50
docker logs lm-web-app --tail 50

# Follow logs
docker logs -f lm-llm
```

### Rebuild Services

```bash
# Backend service (after code change)
docker-compose build --no-cache service-name
docker-compose up -d service-name

# Frontend (after code change)
cd views/web-app
npm run build
docker-compose restart web-app
```

### Database Operations

```bash
# Access PostgreSQL
docker exec -it lm-postgres psql -U postgres -d littlemonster

# Run migrations
cd database
alembic upgrade head

# Seed data
python database/seeds/seed_all.py
```

### Testing

```bash
# Backend tests
cd services/authentication
pytest

# Frontend tests
cd views/web-app
npm test

# E2E tests (Playwright)
cd tests/e2e
pytest test_full_app.py
```

---

## 📚 REQUIRED READING

### Project Rules & Standards (READ FIRST)
1. `.clinerules/zero-tolerance-yolo-debugging.md` - Core methodology
2. `.clinerules/yolo-zero-tolerance-handover-mandate.md` - Handover requirements
3. `.clinerules/application-lifecycle-management.md` - Start/stop procedures
4. `.clinerules/build-and-deployment-workflow.md` - Build requirements
5. `.clinerules/functional-testing-requirement.md` - What counts as tested

### Architecture & Design
6. `docs/TECHNICAL-ARCHITECTURE.md` - System architecture
7. `docs/PROJECT-STRUCTURE.md` - Folder organization
8. `docs/BUSINESS-PROCESS-FLOWS.md` - User workflows
9. `docs/IMPLEMENTATION-ROADMAP.md` - Development phases

### Current State
10. `docs/BACKLOG.md` - What's complete vs pending
11. `docs/phases/PHASE10-COMPLETE.md` - Latest phase status
12. `docs/implementation/DEVELOPER-HANDOVER.md` - Active development notes
13. `HANDOVER-INSTRUCTIONS.md` - Current task specifics

---

## 🔧 SERVICE PORTS & ENDPOINTS

| Service | Container | Internal Port | External Port | Status |
|---------|-----------|---------------|---------------|--------|
| Frontend | lm-web-app | 3000 | 3000 | Running |
| Gateway | lm-gateway | 80 | 80 | Running |
| Auth | lm-auth | 8000 | 8001 | Unhealthy |
| LLM | lm-llm | 8000 | 8005 | Healthy |
| STT | lm-stt | 8000 | 8002 | Running |
| TTS | lm-tts | 8000 | 8003 | Running |
| Recording | lm-recording | 8000 | 8004 | Running |
| Classes | lm-class-mgmt | 8005 | 8006 | Running |
| Content | lm-content-capture | 8008 | 8008 | Unhealthy |
| AI Tools | lm-ai-study-tools | 8009 | 8009 | Running |
| Social | lm-social-collab | 8010 | 8010 | Running |
| Gamification | lm-gamification | 8011 | 8011 | Running |
| Analytics | lm-analytics | 8012 | 8012 | Running |
| Notifications | lm-notifications | 8013 | 8013 | Running |
| PostgreSQL | lm-postgres | 5432 | 5432 | Healthy |
| Redis | lm-redis | 6379 | 6379 | Running |
| ChromaDB | lm-chroma | 8000 | 8000 | Running |
| Ollama | lm-ollama | 11434 | 11434 | Running |

---

## 🧪 TESTING CREDENTIALS

**Test User:**
- Email: `testuser@example.com`
- Password: `TestPass123!`

**Database:**
- Host: `localhost` (or `lm-postgres` inside Docker)
- Port: `5432`
- Database: `littlemonster`
- User: `postgres`
- Password: `postgres`

**Redis:**
- Host: `localhost` (or `lm-redis` inside Docker)  
- Port: `6379`
- No password

---

## 🐛 KNOWN ISSUES

### Critical (Blocking)
- None currently

### Important (Should Fix)
1. **Auth Service Unhealthy** - Container running but health check fails
2. **Content Capture OCR Not Configured** - Tesseract not set up

### Minor (Nice to Fix)
1. Some UI pages show 404 errors (not blocking)
2. Groups page had TypeError (reportedly fixed)

---

## 📝 CURRENT TASK: [FILL IN TASK NAME]

### Objective
[One sentence describing what this handover is for]

### Current Status
[What's been done, what's left]

### Files Modified
[List of files changed in this session]

### Next Steps
[Specific actions for next developer]

### Testing Instructions
[How to verify the work]

### Success Criteria
[How to know it's complete]

---

## 🎓 FOR NEXT DEVELOPER

### Before You Start
1. Read all documents in "Required Reading" section
2. Verify system is running: `docker ps`
3. Test login: Navigate to http://localhost:3000
4. Review current task in "Next Steps" section

### Development Workflow
1. Make code changes
2. Build/restart affected services
3. Test functionality end-to-end
4. Check logs for errors
5. Fix issues immediately
6. Document changes

### When Complete
1. Update this handover with results
2. Mark all checklist items complete
3. Test all affected workflows
4. Document any new issues found
5. Update DEVELOPER-HANDOVER.md with session notes

---

## 📞 GETTING HELP

### Documentation
- Check `docs/` folder for architectural decisions
- Review `.clinerules/` for development standards
- Check service README files for API details

### Debugging
- Use `docker logs <container>` to check service logs
- Use browser DevTools to check frontend errors
- Use `docker exec` to run commands inside containers
- Check `docs/implementation/DEVELOPER-HANDOVER.md` for known issues

---

**Remember:** Zero Tolerance = no errors accepted. YOLO Mode = continue until actually complete.

Good luck! 🦖
