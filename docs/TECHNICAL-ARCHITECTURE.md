# Little Monster GPA - Technical Architecture
## Alpha 1.0 - Complete System Documentation

**Version:** 1.0.0-alpha  
**Date:** November 4, 2025  
**Status:** Production Ready  
**Consolidation Note:** This document consolidates architecture documentation from docs/alpha-0.9/ (SYSTEM-ARCHITECTURE.md, INTEGRATION-ARCHITECTURE.md, PORTS-AND-CONFIGURATION.md, DEPLOYMENT-OPERATIONS.md) with updates for Alpha 1.0 current system status.

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Service Registry](#service-registry)
3. [Network Architecture](#network-architecture)
4. [Integration Architecture](#integration-architecture)
5. [Configuration Reference](#configuration-reference)
6. [Data Architecture](#data-architecture)
7. [Security Architecture](#security-architecture)
8. [Deployment & Operations](#deployment--operations)
9. [Scalability & Performance](#scalability--performance)

---

## System Overview

### Current System Status (Alpha 1.0)

Little Monster GPA is a microservices-based educational platform with **13 application services deployed** (100% of Phase 1-10 services):

**✅ Operational Services (13):**
1. Authentication Service (Port 8001)
2. LLM Agent Service (Port 8005)
3. Speech-to-Text Service (Port 8002)
4. Text-to-Speech Service (Port 8003)
5. Audio Recording Service (Port 8004)
6. Async Jobs Worker (background)
7. Class Management Service (Port 8006)
8. Content Capture Service (Port 8008)
9. AI Study Tools Service (Port 8009)
10. Social Collaboration Service (Port 8010)
11. Gamification Service (Port 8011)
12. Study Analytics Service (Port 8012)
13. Notifications Service (Port 8013)

**Infrastructure (6):** PostgreSQL, Redis, ChromaDB, Qdrant, Ollama, Adminer  
**Frontend (2):** Next.js Web App (Port 3000), Nginx Gateway (Port 80)  
**Optional (1):** Presenton (Port 5000)

**Total Services in docker-compose.yml: 22**

**Status:** All services defined and deployable via docker-compose up -d

### Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                          │
├─────────────────────────────────────────────────────────────┤
│ Frontend:  Next.js 14, React 18, TypeScript, TailwindCSS   │
│ Backend:   Python 3.11, FastAPI, PostgreSQL 15             │
│ Cache:     Redis 7, ChromaDB, Qdrant                       │
│ AI/ML:     Ollama, AWS Bedrock, OpenAI Whisper            │
│ Infra:     Docker, Nginx, AWS (optional)                   │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Microservices Architecture** - Independent, scalable services
2. **API-First Design** - RESTful APIs with OpenAPI specs
3. **Cloud-Native** - Containerized, horizontally scalable
4. **Security by Design** - JWT auth, encrypted data, RBAC
5. **Async Processing** - Redis queues for heavy operations
6. **Observability** - Structured logging, health checks

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WebApp[Web Application<br/>Next.js]
        Mobile[Mobile App<br/>React Native]
    end

    subgraph "API Gateway Layer"
        Gateway[Nginx API Gateway<br/>Port 80]
    end

    subgraph "Application Services"
        Auth[Authentication<br/>Port 8001]
        LLM[LLM Agent<br/>Port 8005]
        STT[Speech-to-Text<br/>Port 8002]
        TTS[Text-to-Speech<br/>Port 8003]
        Record[Audio Recording<br/>Port 8004]
        Class[Class Management<br/>Port 8006]
        Content[Content Capture<br/>Port 8008]
        Study[AI Study Tools<br/>Port 8009]
        Social[Social Collaboration<br/>Port 8010]
        Game[Gamification<br/>Port 8011]
        Analytics[Study Analytics<br/>Port 8012]
        Notif[Notifications<br/>Port 8013]
    end

    subgraph "Infrastructure Services"
        Postgres[(PostgreSQL<br/>Port 5432)]
        Redis[(Redis<br/>Port 6379)]
        Chroma[(ChromaDB<br/>Port 8000)]
        Qdrant[(Qdrant<br/>6333/6334)]
        Ollama[Ollama LLM<br/>Port 11434]
    end

    subgraph "Background Workers"
        JobWorker[Async Job Worker]
        STTWorker[Transcription Worker]
    end

    WebApp --> Gateway
    Mobile --> Gateway
    
    Gateway --> Auth
    Gateway --> LLM
    Gateway --> STT
    Gateway --> TTS
    Gateway --> Record
    Gateway --> Class
    Gateway --> Content
    Gateway --> Study
    Gateway --> Social
    Gateway --> Game
    Gateway --> Analytics
    Gateway --> Notif

    Auth --> Postgres
    Auth --> Redis
    LLM --> Postgres
    LLM --> Redis
    LLM --> Chroma
    LLM --> Ollama
    STT --> Postgres
    STT --> Redis
    TTS --> Postgres
    Record --> Postgres
    Class --> Postgres
    Content --> Postgres
    Content --> Redis
    Content --> Chroma
    Study --> Postgres
    Social --> Postgres
    Game --> Postgres
    Analytics --> Postgres
    Notif --> Postgres
    Notif --> Redis

    JobWorker --> Redis
    JobWorker --> Postgres
    STTWorker --> Redis
    STTWorker --> Postgres

    Study --> LLM
    Content --> STT

    style Gateway fill:#ff6b6b
    style Auth fill:#4ecdc4
    style LLM fill:#45b7d1
    style Postgres fill:#95e1d3
    style Redis fill:#f38181
```

---

## Service Registry

### Complete Port Allocation

```
PORT ALLOCATION MATRIX (Alpha 1.0)
═══════════════════════════════════════════════════════════════

Infrastructure Services:
├─ 5432      PostgreSQL Database        (lm-postgres)
├─ 6379      Redis Cache/Queue          (lm-redis)
├─ 6333      Qdrant Vector DB (HTTP)    (lm-qdrant)
├─ 6334      Qdrant Vector DB (gRPC)    (lm-qdrant)
├─ 8000      ChromaDB Vector DB         (lm-chroma)
├─ 8080      Adminer DB UI              (lm-adminer)
└─ 11434     Ollama LLM                 (lm-ollama)

Gateway & Frontend:
├─ 80        Nginx API Gateway          (lm-gateway)
└─ 3000      Next.js Dev Server         (local)

Application Services (External → Internal):
├─ 8001:8000 Authentication Service     (lm-auth)
├─ 8002:8000 Speech-to-Text Service     (lm-stt)
├─ 8003:8000 Text-to-Speech Service     (lm-tts)
├─ 8004:8000 Audio Recording Service    (lm-recording)
├─ 8005:8000 LLM Agent Service          (lm-llm)
├─ 8006:8005 Class Management Service   (lm-class-mgmt)
├─ 8008:8008 Content Capture Service    (lm-content-capture)
├─ 8009:8009 AI Study Tools Service     (lm-ai-study-tools)
├─ 8010:8010 Social Collaboration       (lm-social-collab)
├─ 8011:8011 Gamification Service       (lm-gamification)
├─ 8012:8012 Study Analytics Service    (lm-study-analytics)
└─ 8013:8013 Notifications Service      (lm-notifications)

Optional Services:
└─ 5000:80   Presenton PPT Generator    (lm-presenton)

Background Workers (No External Ports):
├─ N/A       Async Jobs Worker          (lm-jobs)
└─ N/A       Transcription Worker       (internal)

TOTAL PORTS USED: 21 external ports
```

### Service Communication Matrix

```
┌─────────────┬──────┬─────┬─────┬─────┬─────┬───────┬─────────┬───────┐
│ Service     │ Auth │ LLM │ STT │ TTS │ DB  │ Redis │ ChromaDB│ Ollama│
├─────────────┼──────┼─────┼─────┼─────┼─────┼───────┼─────────┼───────┤
│ Auth        │  -   │  ✗  │  ✗  │  ✗  │  ✓  │   ✓   │    ✗    │   ✗   │
│ LLM Agent   │  ✓   │  -  │  ✗  │  ✗  │  ✓  │   ✓   │    ✓    │   ✓   │
│ STT         │  ✓   │  ✗  │  -  │  ✗  │  ✓  │   ✓   │    ✗    │   ✗   │
│ TTS         │  ✓   │  ✗  │  ✗  │  -  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Recording   │  ✓   │  ✗  │  ✓  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Class Mgmt  │  ✓   │  ✗  │  ✗  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Content Cap │  ✓   │  ✗  │  ✓  │  ✗  │  ✓  │   ✓   │    ✓    │   ✗   │
│ AI Study    │  ✓   │  ✓  │  ✗  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Social      │  ✓   │  ✗  │  ✗  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Gamification│  ✓   │  ✗  │  ✗  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Analytics   │  ✓   │  ✗  │  ✗  │  ✗  │  ✓  │   ✗   │    ✗    │   ✗   │
│ Notification│  ✓   │  ✗  │  ✗  │  ✗  │  ✓  │   ✓   │    ✗    │   ✗   │
└─────────────┴──────┴─────┴─────┴─────┴─────┴───────┴─────────┴───────┘

Legend: ✓ = Direct dependency, ✗ = No dependency
```

### Service Details

| Service | Container Name | Internal Port | External Port | Framework | Status |
|---------|---------------|---------------|---------------|-----------|--------|
| **Infrastructure** |
| PostgreSQL | lm-postgres | 5432 | 5432 | PostgreSQL 15 | ✅ Operational |
| Redis | lm-redis | 6379 | 6379 | Redis 7 | ✅ Operational |
| ChromaDB | lm-chroma | 8000 | 8000 | ChromaDB | ✅ Operational |
| Qdrant | lm-qdrant | 6333 | 6333 | Qdrant | ✅ Operational |
| Ollama | lm-ollama | 11434 | 11434 | Ollama | ✅ Operational |
| Adminer | lm-adminer | 8080 | 8080 | Adminer | ✅ Operational |
| **Application Services** |
| Authentication | lm-auth | 8000 | 8001 | FastAPI | ✅ Operational |
| Speech-to-Text | lm-stt | 8000 | 8002 | FastAPI | ✅ Operational |
| Text-to-Speech | lm-tts | 8000 | 8003 | FastAPI | ✅ Operational |
| Audio Recording | lm-recording | 8000 | 8004 | FastAPI | ✅ Operational |
| LLM Agent | lm-llm | 8000 | 8005 | FastAPI | ✅ Operational |
| Class Management | lm-class-mgmt | 8005 | 8006 | FastAPI | ✅ Operational |
| Content Capture | lm-content-capture | 8008 | 8008 | FastAPI | ⚠️ OCR needs work |
| AI Study Tools | lm-ai-study-tools | 8009 | 8009 | FastAPI | ✅ Operational |
| Social Collaboration | lm-social-collab | 8010 | 8010 | FastAPI | ✅ Operational |
| Gamification | lm-gamification | 8011 | 8011 | FastAPI | ✅ Operational |
| Study Analytics | lm-study-analytics | 8012 | 8012 | FastAPI | ✅ Operational |
| Notifications | lm-notifications | 8013 | 8013 | FastAPI | ✅ Operational |
| **Gateway** |
| API Gateway | lm-gateway | 80 | 80 | Nginx | ✅ Operational |
| **Workers** |
| Async Jobs | lm-jobs | N/A | N/A | Python | ✅ Operational |

---

## Network Architecture

### Docker Network Configuration

All services run on a single bridge network: `lm-network`

```
┌────────────────────────────────────────────────────────────────┐
│                      lm-network (bridge)                        │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Gateway    │───▶│     Auth     │───▶│  PostgreSQL  │    │
│  │   Port 80    │    │   Port 8001  │    │  Port 5432   │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                     │                                 │
│         │                     ▼                                 │
│         │            ┌──────────────┐                          │
│         │            │    Redis     │                          │
│         │            │  Port 6379   │                          │
│         │            └──────────────┘                          │
│         │                                                       │
│         ├──▶ LLM Service (8005)                               │
│         ├──▶ STT Service (8002)                               │
│         ├──▶ TTS Service (8003)                               │
│         ├──▶ Recording (8004)                                 │
│         ├──▶ Class Mgmt (8006)                                │
│         ├──▶ Content Capture (8008)                           │
│         ├──▶ AI Study Tools (8009)                            │
│         ├──▶ Social Collab (8010)                             │
│         ├──▶ Gamification (8011)                              │
│         ├──▶ Analytics (8012)                                 │
│         └──▶ Notifications (8013)                             │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

External Access:
├─ Port 80      → API Gateway (HTTP)
├─ Port 3000    → Next.js Dev Server
├─ Port 5432    → PostgreSQL (dev only)
├─ Port 6379    → Redis (dev only)
├─ Port 8080    → Adminer (dev only)
└─ Ports 8001+  → Direct service access (dev only)
```

### API Gateway Routing

```
Client Request Flow:
┌─────────┐
│ Client  │
└────┬────┘
     │
     ▼
┌─────────────────────┐
│  Nginx Gateway :80  │
│  (lm-gateway)       │
└────┬────────────────┘
     │
     ├─ /api/auth/*       ──▶  Auth Service :8001
     ├─ /api/chat/*       ──▶  LLM Service :8005
     ├─ /api/transcribe/* ──▶  STT Service :8002
     ├─ /api/tts/*        ──▶  TTS Service :8003
     ├─ /api/recordings/* ──▶  Recording Service :8004
     ├─ /api/jobs/*       ──▶  Jobs Service (via worker)
     ├─ /api/classes/*    ──▶  Class Mgmt :8006
     ├─ /api/content/*    ──▶  Content Capture :8008
     ├─ /api/study/*      ──▶  AI Study Tools :8009
     ├─ /api/social/*     ──▶  Social Collab :8010
     ├─ /api/game/*       ──▶  Gamification :8011
     ├─ /api/analytics/*  ──▶  Analytics :8012
     └─ /api/notify/*     ──▶  Notifications :8013
```

---

## Integration Architecture

### Integration Patterns

```
┌─────────────────────────────────────────────────────────┐
│           INTEGRATION PATTERNS                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. API Gateway Pattern                                 │
│     └─ Central entry point for all client requests     │
│                                                          │
│  2. Service Mesh (Docker Network)                       │
│     └─ Internal service-to-service communication       │
│                                                          │
│  3. Database per Service                                │
│     └─ Shared PostgreSQL with logical separation       │
│                                                          │
│  4. Async Messaging (Redis Queues)                     │
│     └─ Background job processing                        │
│                                                          │
│  5. Event-Driven (Future)                              │
│     └─ Pub/Sub for real-time features                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant Database
    participant Redis
    
    Client->>Gateway: HTTP Request + JWT
    Gateway->>Auth: Validate Token
    Auth->>Database: Check Session
    Database-->>Auth: Session Valid
    Auth-->>Gateway: Token Valid
    Gateway->>Service: Forward Request
    Service->>Database: Query/Update
    Database-->>Service: Data
    Service->>Redis: Cache Result
    Service-->>Gateway: Response
    Gateway-->>Client: HTTP Response
```

### REST API Standards

All services follow consistent API design:

```
API Design Standards:

1. URL Structure:
   /api/{service}/{resource}/{id}/{action}
   
   Examples:
   - POST   /api/auth/register
   - POST   /api/auth/login
   - GET    /api/classes/{class_id}
   - POST   /api/classes/{class_id}/assignments
   - POST   /api/transcribe/audio
   - GET    /api/chat/conversations/{conversation_id}

2. HTTP Methods:
   - GET    → Retrieve resource(s)
   - POST   → Create new resource
   - PUT    → Update entire resource
   - PATCH  → Update partial resource
   - DELETE → Remove resource

3. Status Codes:
   - 200 OK              → Success (GET, PUT, PATCH)
   - 201 Created         → Success (POST)
   - 202 Accepted        → Async job queued
   - 204 No Content      → Success (DELETE)
   - 400 Bad Request     → Invalid input
   - 401 Unauthorized    → Missing/invalid token
   - 403 Forbidden       → Insufficient permissions
   - 404 Not Found       → Resource doesn't exist
   - 409 Conflict        → Resource conflict
   - 422 Unprocessable   → Validation error
   - 500 Internal Error  → Server error
   - 503 Service Unavail → Service down

4. Response Format (Success):
   {
     "success": true,
     "data": { ... },
     "meta": {
       "timestamp": "2025-11-04T00:00:00Z",
       "request_id": "uuid"
     }
   }

5. Response Format (Error):
   {
     "success": false,
     "error": {
       "code": "INVALID_INPUT",
       "message": "Email is required",
       "details": { "field": "email" }
     },
     "meta": {
       "timestamp": "2025-11-04T00:00:00Z",
       "request_id": "uuid"
     }
   }

6. Authentication Header:
   Authorization: Bearer <JWT_TOKEN>

7. Content-Type:
   - application/json (default)
   - multipart/form-data (file uploads)
   - audio/mpeg (audio streaming)
```

### Asynchronous Job Pattern

```
Long-Running Operations:

Client              Gateway          Service          Redis Queue        Worker
  │                   │                │                  │                │
  ├─ Upload Audio ───▶│                │                  │                │
  │                   ├─ POST /api ───▶│                  │                │
  │                   │                ├─ Queue Job ─────▶│                │
  │                   │                │                  │                │
  │                   │◀─ Job ID ──────┤                  │                │
  │◀─ 202 Accepted ───┤                │                  │                │
  │                   │                │                  │                │
  │                   │                │                  ├─ Dequeue ─────▶│
  │                   │                │                  │                │
  │                   │                │                  │                │
  ├─ Poll Status ────▶│                │                  │                │
  │                   ├─ GET /jobs/:id▶│                  │                │
  │                   │                ├─ Check Status ──▶│                │
  │                   │                │◀─ Processing ────┤                │
  │◀─ Processing... ──┤                │                  │                │
  │                   │                │                  │◀─ Complete ────┤
  │                   │                │                  │                │
  ├─ Poll Status ────▶│                │                  │                │
  │                   ├─ GET /jobs/:id▶│                  │                │
  │                   │                ├─ Check Status ──▶│                │
  │                   │                │◀─ Complete ──────┤                │
  │◀─ Result ─────────┤                │                  │                │

Typical Processing Time: 10s - 5min
Used For: Transcription, PPT generation, AI analysis
```

---

## Configuration Reference

### Environment Variables Template

```bash
# ============================================================================
# .env File Template - Copy to .env and fill in values
# ============================================================================

# ---------------------------------
# JWT Configuration
# ---------------------------------
JWT_SECRET_KEY=<generate-with-scripts/utilities/generate-secrets.py>
# Must be at least 32 characters
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

# ---------------------------------
# Database Configuration
# ---------------------------------
# PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_NAME=littlemonster
DB_USER=postgres
DB_PASSWORD=postgres  # CHANGE IN PRODUCTION
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster

# ---------------------------------
# Redis Configuration
# ---------------------------------
REDIS_URL=redis://redis:6379/0
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# ---------------------------------
# Vector Database Configuration
# ---------------------------------
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000
VECTOR_DB_TYPE=chroma
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# ---------------------------------
# LLM Configuration
# ---------------------------------
LLM_PROVIDER=ollama  # Options: ollama, bedrock
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b

# AWS Bedrock (Production)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
BEDROCK_MODEL=anthropic.claude-3-sonnet-20240229-v1:0

# ---------------------------------
# Speech Services Configuration
# ---------------------------------
# Azure Text-to-Speech
AZURE_SPEECH_KEY=<your-azure-speech-key>
AZURE_SPEECH_REGION=eastus

# OpenAI Whisper (STT)
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large

# ---------------------------------
# Feature Flags
# ---------------------------------
ENABLE_PRESENTON=true
ENABLE_SOCIAL_FEATURES=true
ENABLE_GAMIFICATION=true
ENABLE_ANALYTICS=true
CAN_CHANGE_KEYS=true
DISABLE_ANONYMOUS_TELEMETRY=true

# ---------------------------------
# Performance Tuning
# ---------------------------------
MAX_FILE_SIZE_MB=50
MAX_AUDIO_LENGTH_SECONDS=3600
MAX_CONCURRENT_JOBS=5
WORKER_THREADS=2

# ---------------------------------
# Security Settings
# ---------------------------------
CORS_ORIGINS=http://localhost:3000,http://localhost:80
SESSION_TIMEOUT_HOURS=24
RATE_LIMIT_PER_MINUTE=100
BCRYPT_ROUNDS=12

# ---------------------------------
# Logging
# ---------------------------------
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=json  # Options: json, text
```

### Service Resource Allocation

```
CONTAINER RESOURCE LIMITS (Production)
═══════════════════════════════════════════════════════════

Service              CPU (cores)    Memory (MB)    Disk (GB)
───────────────────────────────────────────────────────────
PostgreSQL               2.0           2048           50
Redis                    1.0            512            5
ChromaDB                 1.0           1024           20
Qdrant                   1.0           1024           20
Ollama                   4.0           8192           50
───────────────────────────────────────────────────────────
API Gateway              0.5            256            1
Authentication           1.0            512            1
LLM Agent                2.0           2048            5
Speech-to-Text           2.0           2048            5
Text-to-Speech           1.0            512            2
Audio Recording          0.5            256            2
Class Management         1.0            512            1
Content Capture          1.5           1024            5
AI Study Tools           1.0            512            1
Social Collaboration     1.0            512            1
Gamification             0.5            256            1
Study Analytics          0.5            256            1
Notifications            0.5            256            1
Async Jobs Worker        1.0            512            2
───────────────────────────────────────────────────────────
TOTAL                   22.5          21248          173

Development: Reduce by 50%
Minimum: 12 CPU cores, 11GB RAM, 90GB Disk
```

---

## Data Architecture

### Database Schema Organization

**authentication** schema:
- users
- oauth_connections
- refresh_tokens
- password_reset_tokens
- sessions

**content** schema:
- study_materials
- documents
- transcriptions
- tts_audio_files
- recordings
- photos
- textbooks

**classes** schema:
- classes
- class_members
- assignments
- submissions

**interaction** schema:
- conversations
- messages
- user_activity
- connections
- groups
- group_members

**study_tools** schema:
- notes
- flashcards
- practice_tests

**gamification** schema:
- user_points
- achievements
- leaderboards

**analytics** schema:
- study_sessions
- progress_tracking
- goals

**notifications** schema:
- notifications
- messages

**jobs** schema:
- jobs
- job_results
- job_logs

### Redis Database Allocations

- **DB 0**: Sessions (authentication)
- **DB 1**: Job queue (async jobs)
- **DB 2**: Cache (general purpose)
- **DB 3**: Rate limiting

### Vector Databases

**ChromaDB (Port 8000):**
- Collections: study_materials_embeddings, conversation_history_embeddings
- Embedding Model: sentence-transformers/all-MiniLM-L6-v2
- Vector Dimensions: 384

**Qdrant (Ports 6333/6334):**
- Collections: content_vectors
- Embedding Model: same as ChromaDB
- Vector Dimensions: 384

---

## Security Architecture

### Authentication & Authorization Flow

```
User Authentication Process:
┌──────────┐
│  User    │
└────┬─────┘
     │
     ▼
┌─────────────────────┐
│ POST /api/auth/     │
│ register or login   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────────────────┐
│   Authentication Service            │
│                                     │
│  1. Validate credentials            │
│  2. Hash password (bcrypt)          │
│  3. Generate JWT (HS256)            │
│  4. Create session in DB            │
│  5. Cache session in Redis          │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────┐
│  Return JWT Token   │
│  + User Profile     │
└─────────┬───────────
