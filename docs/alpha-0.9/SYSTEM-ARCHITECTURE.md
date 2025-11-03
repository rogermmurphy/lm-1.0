# Little Monster GPA System Architecture
## Alpha 0.9 - Complete Technical Documentation

**Version:** 0.9.0-alpha  
**Date:** November 2, 2025  
**Status:** Production Ready

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Service Registry](#service-registry)
4. [Network Architecture](#network-architecture)
5. [Data Flow](#data-flow)
6. [Security Architecture](#security-architecture)

---

## System Overview

Little Monster is a microservices-based educational platform providing AI-powered study tools, social learning features, and content management capabilities.

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

---

## Architecture Diagrams

### High-Level System Architecture

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

    subgraph "Optional Services"
        Adminer[Adminer<br/>Port 8080]
        Presenton[Presenton<br/>Port 5000]
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
    Presenton --> Ollama

    style Gateway fill:#ff6b6b
    style Auth fill:#4ecdc4
    style LLM fill:#45b7d1
    style Postgres fill:#95e1d3
    style Redis fill:#f38181
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

---

## Service Registry

### Complete Port Allocation

| Service | Container Name | Internal Port | External Port | Protocol | Purpose |
|---------|---------------|---------------|---------------|----------|---------|
| **Infrastructure** |
| PostgreSQL | lm-postgres | 5432 | 5432 | TCP | Primary database |
| Redis | lm-redis | 6379 | 6379 | TCP | Cache & message queue |
| ChromaDB | lm-chroma | 8000 | 8000 | HTTP | Vector database (RAG) |
| Qdrant | lm-qdrant | 6333 | 6333 | HTTP | Vector database (alt) |
| Qdrant gRPC | lm-qdrant | 6334 | 6334 | gRPC | Qdrant gRPC API |
| Ollama | lm-ollama | 11434 | 11434 | HTTP | Local LLM |
| Adminer | lm-adminer | 8080 | 8080 | HTTP | DB management UI |
| **Application Services** |
| API Gateway | lm-gateway | 80 | 80 | HTTP | Reverse proxy |
| Authentication | lm-auth | 8000 | 8001 | HTTP | User auth & sessions |
| Speech-to-Text | lm-stt | 8000 | 8002 | HTTP | Audio transcription |
| Text-to-Speech | lm-tts | 8000 | 8003 | HTTP | Text to audio |
| Audio Recording | lm-recording | 8000 | 8004 | HTTP | Audio capture |
| LLM Agent | lm-llm | 8000 | 8005 | HTTP | AI chat & RAG |
| Class Management | lm-class-mgmt | 8005 | 8006 | HTTP | Classes & assignments |
| Content Capture | lm-content-capture | 8008 | 8008 | HTTP | Photos & OCR |
| AI Study Tools | lm-ai-study-tools | 8009 | 8009 | HTTP | Notes, tests, flashcards |
| Social Collaboration | lm-social-collab | 8010 | 8010 | HTTP | Groups & sharing |
| Gamification | lm-gamification | 8011 | 8011 | HTTP | Points & achievements |
| Study Analytics | lm-study-analytics | 8012 | 8012 | HTTP | Progress tracking |
| Notifications | lm-notifications | 8013 | 8013 | HTTP | Alerts & messages |
| **Optional** |
| Presenton | lm-presenton | 80 | 5000 | HTTP | PowerPoint generation |
| **Background Workers** |
| Async Jobs | lm-jobs | N/A | N/A | Worker | Background processing |
| STT Worker | N/A | N/A | N/A | Worker | Async transcription |

### Service Dependencies

```mermaid
graph LR
    subgraph "Core Infrastructure"
        PG[PostgreSQL]
        RD[Redis]
        CH[ChromaDB]
        OL[Ollama]
    end

    subgraph "Gateway"
        GW[API Gateway]
    end

    subgraph "Auth Tier"
        AU[Auth Service]
    end

    subgraph "Application Tier"
        LLM[LLM Agent]
        STT[Speech-to-Text]
        TTS[Text-to-Speech]
        REC[Recording]
        CLS[Class Mgmt]
        CNT[Content Capture]
        STD[Study Tools]
        SOC[Social]
        GAM[Gamification]
        ANL[Analytics]
        NOT[Notifications]
    end

    subgraph "Workers"
        JOB[Job Worker]
        STW[STT Worker]
    end

    GW --> AU
    GW --> LLM
    GW --> STT
    GW --> TTS
    GW --> REC
    GW --> CLS
    GW --> CNT
    GW --> STD
    GW --> SOC
    GW --> GAM
    GW --> ANL
    GW --> NOT

    AU -.->|validates| LLM
    AU -.->|validates| STT
    AU -.->|validates| TTS
    AU -.->|validates| REC
    AU -.->|validates| CLS
    AU -.->|validates| CNT
    AU -.->|validates| STD
    AU -.->|validates| SOC
    AU -.->|validates| GAM
    AU -.->|validates| ANL
    AU -.->|validates| NOT

    STD -->|uses| LLM
    CNT -->|uses| STT

    AU --> PG
    AU --> RD
    LLM --> PG
    LLM --> RD
    LLM --> CH
    LLM --> OL
    STT --> PG
    STT --> RD
    TTS --> PG
    REC --> PG
    CLS --> PG
    CNT --> PG
    CNT --> RD
    CNT --> CH
    STD --> PG
    SOC --> PG
    GAM --> PG
    ANL --> PG
    NOT --> PG
    NOT --> RD

    JOB --> RD
    JOB --> PG
    STW --> RD
    STW --> PG
```

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

## Data Flow

### Request Processing Flow

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Auth
    participant Service
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

### Authentication Flow

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
└─────────┬───────────┘
          │
          ▼
┌──────────────────────────┐
│  Client stores JWT       │
│  in localStorage         │
│  Includes in all requests│
└──────────────────────────┘

Token Validation (Every Request):
┌──────────┐
│  Client  │──▶ Authorization: Bearer <JWT>
└──────────┘
     │
     ▼
┌────────────────────────────┐
│  Gateway forwards to       │
│  target service            │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Service extracts JWT      │
│  Verifies signature        │
│  Checks expiration         │
│  Validates against Redis   │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────┐
│  Process Request   │
└────────────────────┘
```

### Content Processing Pipeline

```mermaid
graph LR
    A[User Uploads<br/>Content] --> B{Content Type}
    B -->|Photo| C[Content Capture<br/>Service]
    B -->|Audio| D[Recording<br/>Service]
    B -->|Text| E[LLM Agent<br/>Service]
    
    C --> F[OCR Processing<br/>Tesseract]
    C --> G[Vector Embedding<br/>ChromaDB]
    
    D --> H[Queue Job<br/>Redis]
    H --> I[STT Worker<br/>Whisper]
    I --> J[Store Transcript<br/>PostgreSQL]
    
    E --> K[Process with LLM<br/>Ollama/Bedrock]
    K --> L[Generate Response]
    
    F --> M[Store in DB]
    G --> M
    J --> M
    L --> M
    
    M --> N[Return to User]
```

---

## Security Architecture

### Authentication & Authorization

```
Security Layers:

┌─────────────────────────────────────────────┐
│          SECURITY ARCHITECTURE              │
├─────────────────────────────────────────────┤
│                                             │
│  Layer 1: Transport Security                │
│  └─ HTTPS/TLS (production)                 │
│                                             │
│  Layer 2: API Gateway                       │
│  └─ Rate limiting                           │
│  └─ Request validation                      │
│  └─ CORS policy                             │
│                                             │
│  Layer 3: Authentication                    │
│  └─ JWT tokens (HS256)                     │
│  └─ Session management                      │
│  └─ Token expiration (24h)                 │
│  └─ Refresh token rotation                 │
│                                             │
│  Layer 4: Authorization                     │
│  └─ Role-Based Access Control (RBAC)       │
│  └─ Resource ownership validation          │
│  └─ Permission checks per endpoint          │
│                                             │
│  Layer 5: Data Security                     │
│  └─ Password hashing (bcrypt, cost 12)     │
│  └─ SQL injection prevention (ORM)         │
│  └─ Input validation (Pydantic)            │
│  └─ Output sanitization                     │
│                                             │
└─────────────────────────────────────────────┘
```

### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": "uuid",
    "email": "user@example.com",
    "role": "student",
    "exp": 1730593200,
    "iat": 1730506800,
    "jti": "session-uuid"
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + \".\" + base64UrlEncode(payload), secret)"
}
```

### Security Best Practices Implemented

1. ✅ **Password Security**
   - Bcrypt hashing with cost factor 12
   - Minimum 8 characters requirement
   - No password stored in plain text

2. ✅ **Token Security**
   - JWT with short expiration (24h)
   - Refresh token mechanism
   - Session invalidation on logout
   - Redis-backed session store

3. ✅ **API Security**
   - CORS configuration
   - Rate limiting (gateway level)
   - Input validation (Pydantic models)
   - SQL injection prevention (SQLAlchemy ORM)

4. ✅ **Network Security**
   - Internal Docker network isolation
   - No direct database access from outside
   - Service-to-service authentication

---

## Infrastructure Scaling

### Horizontal Scaling Strategy

```
Production Scaling:

Single Instance (Dev):
┌─────────────┐
│  All        │
│  Services   │
│  on 1 host  │
└─────────────┘

Small Scale (< 100 users):
┌─────────────┐  ┌─────────────┐
│  Gateway    │  │  Services   │
│  + DB       │  │  Container  │
└─────────────┘  └─────────────┘

Medium Scale (100-1000 users):
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Gateway    │  │  Services   │  │  Database   │
│  Cluster    │  │  Replicas   │  │  Primary +  │
│             │  │  (2-3x)     │  │  Replicas   │
└─────────────┘  └─────────────┘  └─────────────┘

Large Scale (1000+ users):
┌────────────────┐  ┌──────────────────┐  ┌────────────┐
│   Load         │  │   Service        │  │  Database  │
│   Balancer     │  │   Auto-scaling   │  │  Cluster   │
│   (AWS ALB)    │  │   (ECS/K8s)      │  │  (RDS)     │
└────────────────┘  └──────────────────┘  └────────────┘
```

---

## Monitoring & Observability

### Health Check Endpoints

```
Service Health Checks:

GET /health → Each service returns:
{
  "status": "healthy",
  "service": "service-name",
  "version": "1.0.0",
  "uptime": 3600,
  "dependencies": {
    "database": "connected",
    "redis": "connected"
  }
}

Monitoring Stack (Future):
┌─────────────┐
│  Prometheus │ ◀── Metrics from all services
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Grafana   │ ◀── Visualization dashboards
└─────────────┘
       │
       ▼
┌─────────────┐
│ AlertManager│ ◀── Alert on thresholds
└─────────────┘
```

---

## Deployment Topology

### Development Environment

```
┌────────────────────────────────────────────────────────┐
│              Developer Workstation                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │          Docker Desktop                           │ │
│  │                                                   │ │
│  │  • All services in containers                    │ │
│  │  • Hot-reload enabled                            │ │
│  │  • Direct port access for debugging             │ │
│  │  • Local volumes mounted                         │ │
│  │                                                   │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  Access:                                                │
│  • http://localhost:80      (Gateway)                  │
│  • http://localhost:3000    (Next.js)                  │
│  • http://localhost:8080    (Adminer)                  │
│  • Direct service ports for testing                    │
└────────────────────────────────────────────────────────┘
```

### Production Environment (AWS Example)

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 VPC (10.0.0.0/16)                     │  │
│  │                                                        │  │
│  │  Public Subnet (10.0.1.0/24)                         │  │
│  │  ┌──────────────────┐                                │  │
│  │  │  Application     │                                │  │
│  │  │  Load Balancer   │                                │  │
│  │  └────────┬─────────┘                                │  │
│  │           │                                           │  │
│  │  Private Subnet (10.0.2.0/24)                        │  │
│  │  ┌─────────────────────────────────────────┐        │  │
│  │  │  ECS Fargate Cluster                    │        │  │
│  │  │  ┌──────────┐  ┌──────────┐            │        │  │
│  │  │  │ Service  │  │ Service  │  ...       │        │  │
│  │  │  │ Task 1   │  │ Task 2   │            │        │  │
│  │  │  └──────────┘  └──────────┘            │        │  │
│  │  └────────┬────────────────────────────────┘        │  │
│  │           │                                           │  │
│  │  Private Subnet (10.0.3.0/24)                        │  │
│  │  ┌─────────────────────────────────────────┐        │  │
│  │  │  Data Layer                             │        │  │
│  │  │  ├─ RDS PostgreSQL (Multi-AZ)          │        │  │
│  │  │  ├─ ElastiCache Redis (Cluster)        │        │  │
│  │  │  └─ S3 for file storage                │        │  │
│  │  └─────────────────────────────────────────┘        │  │
│  │                                                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Choices

### Framework Selection

| Component | Technology | Reason |
|-----------|-----------|--------|
| **API Framework** | FastAPI | Async support, auto-docs, type safety |
| **ORM** | SQLAlchemy | Mature, feature-rich, async support |
| **Task Queue** | Redis + RQ | Simple, reliable, Python-native |
| **Vector DB** | ChromaDB | Easy setup, good performance, local-first |
| **LLM** | Ollama + AWS Bedrock | Local dev + prod scalability |
| **Frontend** | Next.js 14 | React Server Components, excellent DX |
| **Styling** | TailwindCSS | Utility-first, consistent design |
| **Auth** | JWT + Sessions | Stateless + stateful hybrid |
| **Containerization** | Docker Compose | Simple, effective,
