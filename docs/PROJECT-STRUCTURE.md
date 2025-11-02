# Little Monster - Project Structure

## Document Control
- **Version**: 1.0
- **Date**: November 1, 2025
- **Status**: Draft
- **Related Documents**: PROJECT-CHARTER.md, TECHNICAL-ARCHITECTURE.md

---

## Overview

This document defines the folder structure for Little Monster's microservices architecture. The structure separates Services (business logic), Database (schemas/migrations), and Views (frontend applications) while maintaining references to validated POCs and legacy code.

**Design Principles:**
1. **Service-Database-View Separation**: Clear separation of concerns
2. **Microservices Ready**: Each service is independently deployable
3. **Container First**: All components containerized
4. **Legacy Preservation**: Keep `old/` and `poc/` for reference
5. **Code Reuse**: Extract best parts from POCs and old codebase

---

## Root Directory Structure

```
lm-1.0/
├── docs/                          # Project documentation
├── services/                      # Microservices (backend)
├── database/                      # Database schemas & migrations
├── views/                         # Frontend applications
├── infrastructure/                # Docker & deployment configs
├── shared/                        # Shared libraries & utilities
├── tests/                         # Integration & E2E tests
├── scripts/                       # Automation scripts
├── old/                          # Legacy code (reference only)
├── poc/                          # Proof of concepts (reference only)
├── .gitignore
├── README.md
├── LICENSE
└── docker-compose.yml            # Main orchestration file
```

---

## 1. Documentation (`docs/`)

### Purpose
Central repository for all project documentation

### Structure
```
docs/
├── PROJECT-CHARTER.md            # ✅ Created - Vision & objectives
├── REQUIREMENTS.md               # ✅ Created - Functional & non-functional
├── FUNCTIONAL-SPECIFICATIONS.md  # Detailed use cases & workflows
├── TECHNICAL-SPECIFICATIONS.md   # API specs, data models
├── INTEGRATION-ARCHITECTURE.md   # Service integration patterns
├── TECHNICAL-ARCHITECTURE.md     # ✅ Created - System architecture
├── PROJECT-STRUCTURE.md          # ✅ This file
├── API-DOCUMENTATION.md          # OpenAPI/Swagger consolidated
├── DEPLOYMENT-GUIDE.md           # How to deploy locally & cloud
├── DEVELOPER-GUIDE.md            # Setup, conventions, workflows
├── USER-GUIDE.md                 # End-user documentation
└── diagrams/                     # Architecture diagrams
    ├── architecture-overview.png
    ├── microservices-diagram.png
    ├── database-erd.png
    └── deployment-flow.png
```

---

## 2. Services (`services/`)

### Purpose
Backend microservices - each POC becomes a production service

### Structure
```
services/
├── authentication/               # POC 12 → Production Service
│   ├── src/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration management
│   │   ├── models.py            # Database models (SQLAlchemy)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # /register, /login, /logout
│   │   │   ├── oauth.py         # OAuth2 endpoints
│   │   │   └── users.py         # User profile endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py  # Business logic
│   │   │   ├── oauth_service.py
│   │   │   └── jwt_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── password.py      # From POC 12
│   │       ├── jwt.py           # From POC 12
│   │       └── validators.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_oauth.py
│   │   └── test_jwt.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── speech-to-text/               # POC 09 → Production Service
│   ├── src/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py
│   │   ├── models.py            # Database models
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── transcribe.py    # /transcribe endpoint
│   │   │   └── jobs.py          # Job status endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── whisper_service.py
│   │   │   └── job_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── audio_utils.py
│   ├── tests/
│   │   ├── test_transcription.py
│   │   └── test_jobs.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── text-to-speech/               # POC 11 → Production Service
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── generate.py      # /generate endpoint
│   │   │   └── voices.py        # /voices endpoint
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── azure_tts.py     # From POC 11
│   │   │   └── coqui_tts.py     # From POC 11.1 (fallback)
│   │   └── utils/
│   ├── tests/
│   │   ├── test_azure_tts.py
│   │   └── test_coqui_tts.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── audio-recording/              # POC 10 → Production Service
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── record.py
│   │   │   └── upload.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── recorder.py      # From POC 10
│   │   │   └── storage.py
│   │   └── utils/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── llm-agent/                    # POC 07 → Production Service
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py          # /chat endpoints
│   │   │   └── materials.py     # Study materials
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── agent_service.py # From POC 07
│   │   │   ├── rag_service.py   # From POC 00
│   │   │   └── vector_service.py
│   │   └── utils/
│   ├── tests/
│   │   ├── test_agent.py
│   │   └── test_rag.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── async-jobs/                   # POC 08 → Production Service
│   ├── src/
│   │   ├── main.py              # FastAPI for job API
│   │   ├── worker.py            # Background worker
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── jobs.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── queue_service.py # From POC 08
│   │   │   └── worker_service.py
│   │   └── utils/
│   ├── tests/
│   │   ├── test_queue.py
│   │   └── test_worker.py
│   ├── Dockerfile.api
│   ├── Dockerfile.worker
│   ├── requirements.txt
│   └── README.md
│
└── api-gateway/                  # NEW - API Gateway/Load Balancer
    ├── nginx.conf               # Nginx configuration
    ├── ssl/                     # SSL certificates
    ├── Dockerfile
    └── README.md
```

### Service Template Structure

Each service follows this standard structure:

```
service-name/
├── src/                          # Source code
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration (env vars)
│   ├── models.py                # Database models (SQLAlchemy)
│   ├── schemas.py               # Pydantic schemas (validation)
│   ├── dependencies.py          # FastAPI dependencies
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   └── *.py                 # Route modules
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   └── *.py                 # Service modules
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── *.py
├── tests/                       # Tests
│   ├── conftest.py              # Pytest configuration
│   ├── test_*.py                # Test modules
│   └── fixtures/                # Test data
├── Dockerfile                   # Container definition
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # Service documentation
```

---

## 3. Database (`database/`)

### Purpose
Centralized database schemas, migrations, and seed data

### Structure
```
database/
├── schemas/                      # SQL schema definitions
│   ├── 001_authentication.sql   # From POC 12
│   ├── 002_transcription.sql    # From POC 09
│   ├── 003_async_jobs.sql       # From POC 08
│   ├── 004_content.sql          # Study materials, etc.
│   ├── 005_interaction.sql      # Conversations, messages
│   └── master-schema.sql        # Consolidated schema
│
├── migrations/                   # Database migrations (Alembic)
│   ├── versions/
│   │   ├── 001_initial_schema.py
│   │   ├── 002_add_oauth.py
│   │   └── 003_add_indexes.py
│   ├── alembic.ini
│   └── env.py
│
├── seeds/                        # Seed data for development
│   ├── users.sql                # Test users
│   ├── study_materials.sql      # Sample materials
│   └── README.md
│
└── scripts/                      # Database utility scripts
    ├── backup.sh                # Backup database
    ├── restore.sh               # Restore from backup
    ├── migrate.sh               # Run migrations
    └── reset.sh                 # Drop and recreate (dev only)
```

### Migration Strategy

**Alembic (SQLAlchemy Migrations):**
```python
# Example migration
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        # ...
    )

def downgrade():
    op.drop_table('users')
```

**Commands:**
```bash
# Create migration
alembic revision -m "add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 4. Views (`views/`)

### Purpose
Frontend applications for web, mobile, and desktop

### Structure
```
views/
├── web-app/                      # React/Next.js Web Application
│   ├── src/
│   │   ├── app/                 # Next.js app directory
│   │   │   ├── (auth)/          # Auth pages
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── (dashboard)/     # Main app pages
│   │   │   │   ├── chat/        # AI tutor chat
│   │   │   │   ├── transcribe/  # Audio transcription
│   │   │   │   ├── materials/   # Study materials
│   │   │   │   └── recordings/  # Audio recordings
│   │   │   └── layout.tsx
│   │   ├── components/          # Reusable components
│   │   │   ├── auth/
│   │   │   ├── chat/
│   │   │   ├── audio/
│   │   │   └── ui/              # From old/Ella-Ai/web-app
│   │   ├── lib/
│   │   │   ├── api/             # API client
│   │   │   ├── auth/            # Auth utilities
│   │   │   └── utils/
│   │   ├── hooks/               # React hooks
│   │   ├── styles/              # CSS/Tailwind
│   │   └── types/               # TypeScript types
│   ├── public/                  # Static assets
│   ├── tests/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── README.md
│
├── mobile-app/                   # React Native Mobile App
│   ├── src/
│   │   ├── screens/             # Screen components
│   │   │   ├── Auth/
│   │   │   ├── Chat/
│   │   │   ├── Record/
│   │   │   └── Materials/
│   │   ├── components/          # Shared components
│   │   ├── navigation/          # Navigation config
│   │   ├── services/            # API client
│   │   ├── hooks/
│   │   ├── utils/
│   │   └── types/
│   ├── android/                 # Android specific
│   ├── ios/                     # iOS specific
│   ├── assets/                  # Images, fonts
│   ├── package.json
│   ├── app.json
│   ├── tsconfig.json
│   └── README.md
│
└── desktop-app/                  # Electron/Tauri Desktop App
    ├── src/
    │   ├── main/                # Main process (Node.js)
    │   │   ├── index.ts
    │   │   └── ipc-handlers.ts
    │   ├── renderer/            # Renderer process (React)
    │   │   ├── App.tsx
    │   │   ├── screens/
    │   │   ├── components/
    │   │   └── index.html
    │   └── shared/              # Shared utilities
    ├── resources/               # App icons, assets
    ├── build/                   # Build configuration
    ├── package.json
    ├── electron-builder.json
    └── README.md
```

---

## 5. Infrastructure (`infrastructure/`)

### Purpose
Docker configurations and deployment scripts

### Structure
```
infrastructure/
├── docker-compose.yml            # Main orchestration (all services)
├── docker-compose.dev.yml       # Development overrides
├── docker-compose.prod.yml      # Production overrides
├── .env.example                 # Environment variables template
├── .env                         # Local environment (gitignored)
│
├── nginx/                        # API Gateway configuration
│   ├── nginx.conf               # Main config
│   ├── sites-enabled/
│   │   └── littlemonster.conf
│   ├── ssl/
│   │   ├── cert.pem
│   │   └── key.pem
│   └── Dockerfile
│
├── postgres/                     # PostgreSQL configuration
│   ├── init-scripts/            # Initialization SQL
│   │   └── 001_create_databases.sql
│   └── postgres.conf            # Custom config (optional)
│
└── monitoring/                   # Monitoring stack (future)
    ├── prometheus.yml
    ├── grafana/
    └── docker-compose.monitoring.yml
```

### Docker Compose Organization

**docker-compose.yml** (Base - All environments):
```yaml
version: '3.8'
services:
  # Infrastructure
  postgres:
    image: postgres:15-alpine
    # ...
  
  redis:
    image: redis:7-alpine
    # ...
  
  # Services
  auth-service:
    build: ./services/authentication
    # ...
  
  stt-service:
    build: ./services/speech-to-text
    # ...
```

**docker-compose.dev.yml** (Development overrides):
```yaml
version: '3.8'
services:
  auth-service:
    volumes:
      - ./services/authentication/src:/app/src:ro
    environment:
      - DEBUG=true
```

**docker-compose.prod.yml** (Production overrides):
```yaml
version: '3.8'
services:
  auth-service:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
```

---

## 6. Shared (`shared/`)

### Purpose
Common code shared across multiple services and applications

### Structure
```
shared/
├── python-common/                # Shared Python utilities
│   ├── lm_common/
│   │   ├── __init__.py
│   │   ├── auth/                # JWT validation, etc.
│   │   │   ├── __init__.py
│   │   │   ├── jwt.py
│   │   │   └── middleware.py
│   │   ├── database/            # Database utilities
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── base_model.py
│   │   ├── redis/               # Redis utilities
│   │   │   ├── __init__.py
│   │   │   └── client.py
│   │   ├── logging/             # Structured logging
│   │   │   ├── __init__.py
│   │   │   └── logger.py
│   │   └── utils/               # Generic utilities
│   │       ├── __init__.py
│   │       ├── validators.py
│   │       └── helpers.py
│   ├── tests/
│   ├── setup.py
│   └── README.md
│
└── typescript-common/            # Shared TypeScript utilities
    ├── src/
    │   ├── api/                 # API client
    │   │   ├── client.ts
    │   │   ├── auth.ts
    │   │   ├── stt.ts
    │   │   ├── tts.ts
    │   │   └── chat.ts
    │   ├── types/               # TypeScript types
    │   │   ├── auth.ts
    │   │   ├── chat.ts
    │   │   └── api.ts
    │   └── utils/               # Utilities
    │       ├── formatters.ts
    │       └── validators.ts
    ├── package.json
    ├── tsconfig.json
    └── README.md
```

### Shared Library Usage

**Python Services:**
```python
from lm_common.auth import validate_jwt_token
from lm_common.database import get_db_session
from lm_common.logging import get_logger
```

**Frontend Applications:**
```typescript
import { AuthAPI, ChatAPI } from '@lm/api-client';
import { User, Message } from '@lm/types';
```

---

## 7. Tests (`tests/`)

### Purpose
Integration, end-to-end, and performance tests

### Structure
```
tests/
├── integration/                  # Service integration tests
│   ├── test_auth_to_llm.py
│   ├── test_stt_to_jobs.py
│   └── test_complete_flow.py
│
├── e2e/                         # End-to-end tests
│   ├── scenarios/
│   │   ├── student_registration.py
│   │   ├── lecture_transcription.py
│   │   └── ai_tutoring.py
│   ├── conftest.py
│   └── README.md
│
├── performance/                  # Load & performance tests
│   ├── locust/                  # Locust load tests
│   │   ├── locustfile.py
│   │   └── scenarios/
│   ├── benchmarks/              # Service benchmarks
│   │   ├── auth_benchmark.py
│   │   └── llm_benchmark.py
│   └── reports/                 # Test reports
│
├── fixtures/                     # Test data
│   ├── users.json
│   ├── audio_samples/
│   └── study_materials/
│
└── README.md
```

---

## 8. Scripts (`scripts/`)

### Purpose
Automation and utility scripts

### Structure
```
scripts/
├── setup/                        # Initial setup
│   ├── setup-local.sh           # Setup for local dev
│   ├── setup-server.sh          # Setup for bigger server
│   └── install-dependencies.sh
│
├── database/                     # Database utilities
│   ├── backup-db.sh
│   ├── restore-db.sh
│   ├── migrate-db.sh
│   ├── seed-db.sh
│   └── reset-db.sh
│
├── docker/                       # Docker utilities
│   ├── build-all.sh             # Build all service images
│   ├── push-images.sh           # Push to registry
│   ├── pull-images.sh           # Pull from registry
│   └── cleanup.sh               # Remove unused images
│
├── deployment/                   # Deployment scripts
│   ├── deploy-local.sh
│   ├── deploy-server.sh
│   ├── deploy-aws.sh            # Future
│   └── rollback.sh
│
└── utilities/                    # Misc utilities
    ├── generate-secrets.py      # Generate JWT secrets
    ├── create-admin-user.py     # Create admin account
    └── health-check.sh          # Check all services
```

### Example Script: setup-local.sh

```bash
#!/bin/bash
# Setup Little Monster for local development

echo "Setting up Little Monster..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }
command -v python >/dev/null 2>&1 || { echo "Python required"; exit 1; }

# Copy environment files
cp infrastructure/.env.example infrastructure/.env
echo "✓ Environment file created"

# Generate secrets
python scripts/utilities/generate-secrets.py >> infrastructure/.env
echo "✓ Secrets generated"

# Build Docker images
cd infrastructure
docker-compose build
echo "✓ Docker images built"

# Start infrastructure services
docker-compose up -d postgres redis qdrant ollama
echo "✓ Infrastructure started"

# Wait for databases
sleep 10

# Run migrations
docker-compose run --rm auth-service alembic upgrade head
echo "✓ Database migrations applied"

# Start application services
docker-compose up -d
echo "✓ All services started"

echo ""
echo "Little Monster is ready!"
echo "  Web UI: http://localhost"
echo "  API Docs: http://localhost/api/docs"
echo "  Database Admin: http://localhost:8080"
```

---

## 9. Legacy Code (`old/` and `poc/`)

### Purpose
Reference implementations - DO NOT modify, only extract from

### Structure
```
old/                              # Previous implementation
├── Ella-Ai/                     # Keep for UI components
│   ├── web-app/                 # Extract React components
│   ├── mobile-app/              # Extract mobile screens
│   ├── desktop-app/             # Extract desktop logic
│   ├── backend/                 # Reference only
│   ├── docker-compose.yml       # Base for new compose
│   └── docs/                    # Historical documentation
│
poc/                              # Validated proof of concepts
├── 00-functional-poc/           # Initial RAG chatbot
├── 07-langchain-agent/          # LLM agent (extract to llm-service)
├── 08-async-jobs/               # Job queue (extract to async-jobs)
├── 09-speech-to-text/           # STT (extract to stt-service)
├── 10-record-to-text/           # Recording (extract to audio-service)
├── 11-text-to-speech/           # TTS (extract to tts-service)
├── 11.1-coqui-tts/             # Local TTS (extract to tts-service)
└── 12-authentication/           # Auth (extract to auth-service)
```

### Extraction Guidelines

**DO:**
- Copy core functionality to new services
- Improve code quality during migration
- Add proper error handling
- Add comprehensive tests
- Update documentation

**DON'T:**
- Modify original POC files
- Delete POC folders (keep for reference)
- Assume POC code is production-ready as-is

---

## Development Workflow Structure

### Local Development

```
Developer Machine:
1. Clone repository
2. Run setup script: ./scripts/setup/setup-local.sh
3. Access services:
   - Web: http://localhost
   - API: http://localhost/api
   - Docs: http://localhost/api/docs
4. Make changes in services/
5. Docker live-reloads on file change (development mode)
6. Run tests: pytest tests/
7. Commit changes
```

### Bigger Server Deployment

```
Bigger Server:
1. Export images: docker-compose -f docker-compose.prod.yml build
2. Save: docker save $(docker images -q) | gzip > lm-images.tar.gz
3. Transfer to server: scp lm-images.tar.gz server:/opt/littlemonster/
4. Import: gunzip -c lm-images.tar.gz | docker load
5. Start: docker-compose -f docker-compose.prod.yml up -d
6. Monitor: docker stats
```

---

## File Naming Conventions

### Python Files
- **Module names**: `snake_case` (e.g., `auth_service.py`)
- **Class names**: `PascalCase` (e.g., `AuthService`)
- **Function names**: `snake_case` (e.g., `validate_password`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_LOGIN_ATTEMPTS`)

### TypeScript/JavaScript Files
- **File names**: `kebab-case` (e.g., `auth-service.ts`)
- **Component names**: `PascalCase` (e.g., `ChatInterface.tsx`)
- **Function names**: `camelCase` (e.g., `validatePassword`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)

### SQL Files
- **Migration files**: `001_description.sql`
- **Schema files**: `service_name.sql`
- **Seed files**: `entity_name_seeds.sql`

---

## Configuration Management

### Environment Variables Organization

**infrastructure/.env:**
```bash
# Database
DATABASE_URL=postgresql://lmuser:lmpass@postgres:5432/lm_db

# Redis
REDIS_URL=redis://redis:6379

# JWT
JWT_SECRET_KEY=generated-secret-key-here
JWT_ALGORITHM=HS256

# Services
AUTH_SERVICE_URL=http://auth-service:8000
STT_SERVICE_URL=http://stt-service:8000
TTS_SERVICE_URL=http://tts-service:8000
LLM_SERVICE_URL=http://llm-service:8000

# External APIs
AZURE_SPEECH_KEY=your-azure-key
AZURE_REGION=eastus
GOOGLE_CLIENT_ID=your-google-client-id
FACEBOOK_CLIENT_ID=your-facebook-app-id
```

**Service-Specific** (services/authentication/.env):
```bash
# Inherits from infrastructure/.env
# Service-specific overrides only
LOG_LEVEL=DEBUG
OAUTH_CALLBACK_URL=http://localhost/api/auth/callback
```

---

## CI/CD Pipeline Structure (Future)

```
.github/
├── workflows/
│   ├── ci-tests.yml             # Run tests on PR
│   ├── build-images.yml         # Build Docker images
│   ├── deploy-dev.yml           # Deploy to dev
│   ├── deploy-staging.yml       # Deploy to staging
│   └── deploy-prod.yml          # Deploy to production
│
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
│
└── PULL_REQUEST_TEMPLATE.md
```

---

## Migration Checklist: POC → Service

### For Each Service

- [ ] Create service folder structure
- [ ] Extract core code from POC
- [ ] Add FastAPI application wrapper
- [ ] Implement all required endpoints
- [ ] Add Pydantic schemas for validation
- [ ] Add proper error handling
- [ ] Add structured logging
- [ ] Create Dockerfile
- [ ] Add comprehensive tests
- [ ] Add service README
- [ ] Update docker-compose.yml
- [ ] Update API Gateway routes
- [ ] Test service independently
- [ ] Test service integration
- [ ] Document API endpoints

---

## Summary: Folder Structure Benefits

### ✅ Service-Database-View Separation
- **Services**: Backend microservices with business logic
- **Database**: Centralized schema management
- **Views**: Frontend applications (web, mobile, desktop)

### ✅ Microservices Ready
- Each service independently deployable
- Services scale separately
- Minimal inter-service dependencies

### ✅ Container Portability
- Runs on local dev machine
- Runs on bigger local server
- Runs on AWS (same containers)

### ✅ Code Reusability
- Shared libraries (Python, TypeScript)
- Extract best parts from POCs
- Reuse UI components from old

### ✅
