# Little Monster - Technical Architecture

## Document Control
- **Version**: 1.0
- **Date**: November 1, 2025
- **Status**: Draft
- **Related Documents**: PROJECT-CHARTER.md, REQUIREMENTS.md

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Microservices Design](#microservices-design)
3. [Data Architecture](#data-architecture)
4. [Network Architecture](#network-architecture)
5. [Security Architecture](#security-architecture)
6. [Deployment Architecture](#deployment-architecture)

---

## Architecture Overview

### Architectural Style: Microservices

Little Monster uses a **microservices architecture** where each POC becomes an independent, containerized service. This design provides:

- **Modularity**: Services can be developed, deployed, and scaled independently
- **Technology Flexibility**: Each service can use optimal technology stack
- **Resilience**: Service failures don't cascade to entire system
- **Scalability**: Services scale based on individual demand
- **Portability**: Containers run anywhere (local, server, cloud)

### High-Level Architecture Diagram

#### ASCII Diagram (Text-based)

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Web App     │  │  Mobile App  │  │ Desktop App  │          │
│  │  (React)     │  │ (React Native│  │  (Electron)  │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │ HTTPS
                             ▼
          ┌──────────────────────────────────────┐
          │      API GATEWAY (nginx)             │
          │      Port 80/443                     │
          │  - Routing                           │
          │  - Load Balancing                    │
          │  - SSL Termination                   │
          │  - Rate Limiting                     │
          └──────────────────┬───────────────────┘
                             │
          ┌──────────────────┴────────────────────┐
          │        lm-network (Docker)            │
          │                                       │
     ┌────┴─────┬──────┬──────┬───────┬────────┐ │
     │          │      │      │       │        │ │
┌────▼────┐ ┌──▼──┐ ┌─▼──┐ ┌─▼───┐ ┌─▼────┐ ┌─▼─────┐
│  Auth   │ │ STT │ │TTS │ │ LLM │ │ Jobs │ │ Audio │
│ Service │ │ Svc │ │Svc │ │Agent│ │Worker│ │  Rec  │
│  :8001  │ │:8002│ │:803│ │:8005│ │:8006 │ │ :8004 │
└────┬────┘ └──┬──┘ └─┬──┘ └──┬──┘ └─┬────┘ └───┬───┘
     │         │      │       │      │          │
     └─────────┴──────┴───────┴──────┴──────────┘
                             │
          ┌──────────────────┴────────────────────┐
          │                                       │
     ┌────▼─────┐  ┌──────▼──────┐  ┌─────▼─────┐
     │PostgreSQL│  │    Redis    │  │  Qdrant   │
     │  :5432   │  │    :6379    │  │  :6333    │
     │          │  │             │  │  Vector   │
     │  Users   │  │   Queue     │  │    DB     │
     │  Jobs    │  │   Sessions  │  │           │
     │  Content │  │   Cache     │  │           │
     └──────────┘  └─────────────┘  └───────────┘
```

#### Mermaid Diagram (GitHub-rendered)

```mermaid
graph TB
    subgraph Clients["CLIENTS"]
        WebApp["Web App<br/>(React)"]
        MobileApp["Mobile App<br/>(React Native)"]
        DesktopApp["Desktop App<br/>(Electron)"]
    end
    
    WebApp & MobileApp & DesktopApp -->|HTTPS| Gateway
    
    Gateway["API GATEWAY<br/>(nginx)<br/>Port 80/443<br/>- Routing<br/>- Load Balancing<br/>- SSL Termination<br/>- Rate Limiting"]
    
    subgraph DockerNetwork["lm-network (Docker)"]
        subgraph Services["MICROSERVICES"]
            AuthService["Auth Service<br/>:8001"]
            STTService["STT Service<br/>:8002"]
            TTSService["TTS Service<br/>:8003"]
            AudioService["Audio Service<br/>:8004"]
            LLMService["LLM Agent<br/>:8005"]
            JobsService["Jobs Service<br/>:8006"]
            JobsWorker["Jobs Worker"]
        end
        
        subgraph DataLayer["DATA & INFRASTRUCTURE"]
            Postgres["PostgreSQL<br/>:5432<br/>Users, Jobs, Content"]
            Redis["Redis<br/>:6379<br/>Queue, Sessions, Cache"]
            Qdrant["Qdrant<br/>:6333<br/>Vector DB"]
            Ollama["Ollama<br/>:11434<br/>Local LLM"]
        end
    end
    
    Gateway --> AuthService & STTService & TTSService & AudioService & LLMService & JobsService
    
    AuthService & STTService & TTSService & AudioService & LLMService & JobsService --> Postgres
    AuthService & STTService & JobsService & JobsWorker --> Redis
    LLMService --> Qdrant
    LLMService --> Ollama
    JobsWorker -.->|polls| Redis
    
    style Clients fill:#e1f5ff
    style Gateway fill:#ffe1e1
    style Services fill:#e1ffe1
    style DataLayer fill:#fff4e1
```

---

## Microservices Design

### Service Catalog

#### 1. Authentication Service (auth-service)
**Port**: 8001  
**Source**: POC 12 (Tested & Working)  
**Language**: Python (FastAPI)

**Responsibilities:**
- User registration (email/password)
- OAuth2 social login (Google, Facebook, Microsoft)
- JWT token generation/validation
- Session management via Redis
- Password reset functionality
- User profile management

**Database Tables:**
- users
- oauth_connections
- refresh_tokens
- password_reset_tokens

**External Dependencies:**
- Google OAuth2 API
- Facebook OAuth2 API
- Microsoft OAuth2 API
- SMTP server (email verification)

**Performance SLA:**
- Login: <200ms
- Registration: <500ms
- Token validation: <5ms

---

#### 2. Speech-to-Text Service (stt-service)
**Port**: 8002  
**Source**: POC 09 (Tested & Working)  
**Language**: Python (FastAPI)

**Responsibilities:**
- Audio file upload handling
- Transcription via OpenAI Whisper
- Async job creation for long audio
- Transcription storage
- Job status tracking

**Database Tables:**
- transcription_jobs
- transcriptions
- audio_files

**External Dependencies:**
- OpenAI Whisper model (local)
- Redis queue (async jobs)

**Performance SLA:**
- Job creation: <100ms
- Transcription: <30s for 5-minute audio
- Status query: <50ms

---

#### 3. Text-to-Speech Service (tts-service)
**Port**: 8003  
**Source**: POC 11 & 11.1 (Tested & Working)  
**Language**: Python (FastAPI)

**Responsibilities:**
- Text-to-speech generation
- Voice selection
- Audio file management
- Azure TTS (primary, <1s generation)
- Coqui TTS (fallback, local)

**Database Tables:**
- tts_audio_files
- tts_requests

**External Dependencies:**
- Azure Speech Services API
- Coqui TTS Docker container (optional)

**Performance SLA:**
- Azure TTS: <1s generation
- Coqui TTS: 2-90s generation (local)
- Audio retrieval: <100ms

---

#### 4. Audio Recording Service (audio-service)
**Port**: 8004  
**Source**: POC 10 (Tested & Working)  
**Language**: Python (FastAPI)

**Responsibilities:**
- Audio recording management
- File storage
- Recording metadata
- Integration with STT service

**Database Tables:**
- recordings
- recording_sessions

**External Dependencies:**
- None (client-side recording preferred)

**Performance SLA:**
- Upload handling: <200ms
- Metadata storage: <50ms

---

#### 5. LLM Agent Service (llm-service)
**Port**: 8005  
**Source**: POC 07 (Tested with Ollama & Bedrock)  
**Language**: Python (FastAPI + LangChain)

**Responsibilities:**
- Conversational AI interface
- RAG (Retrieval Augmented Generation)
- Study material querying
- Context management
- Response generation

**Database Tables:**
- conversations
- messages
- study_materials

**External Dependencies:**
- Ollama API (local LLM)
- AWS Bedrock API (cloud LLM)
- Qdrant/ChromaDB (vector search)

**Performance SLA:**
- First token: <200ms
- Full response: <5s
- RAG query: <500ms

---

#### 6. Async Jobs Service (jobs-service)
**Port**: 8006  
**Source**: POC 08 (Tested & Working)  
**Language**: Python (FastAPI)

**Responsibilities:**
- Job queue management
- Job status tracking
- Worker coordination
- Result storage
- Retry logic

**Database Tables:**
- jobs
- job_results
- job_logs

**External Dependencies:**
- Redis (job queue)

**Performance SLA:**
- Job creation: <50ms
- Status query: <20ms
- Job processing: Varies by type

---

#### 7. Jobs Worker (jobs-worker)
**Port**: N/A (Background process)  
**Source**: POC 08, POC 09  
**Language**: Python

**Responsibilities:**
- Poll Redis queue for jobs
- Execute background tasks
- Update job status
- Handle failures and retries
- Report completion

**Scalability**: Multiple workers can run concurrently

---

#### 8. API Gateway (api-gateway)
**Port**: 80, 443  
**Technology**: Nginx or Kong  
**Role**: Unified entry point

**Responsibilities:**
- Request routing to services
- SSL/TLS termination
- Load balancing
- Rate limiting
- CORS handling
- Request/response logging

---

### Service Communication Patterns

#### Pattern 1: Synchronous REST API
**Used For**: Real-time operations (auth, queries)

```
Client → API Gateway → Service → Response
```

**Example**: User login
```
POST /api/auth/login
→ API Gateway routes to auth-service:8001
→ auth-service validates credentials
→ Response with JWT tokens
```

#### Pattern 2: Asynchronous Jobs
**Used For**: Long-running operations (transcription, TTS, presentations)

```
Client → API Gateway → Service → Create Job → Return Job ID
                                      ↓
                                   Redis Queue
                                      ↓
                                   Worker polls
                                      ↓
                                Process job
                                      ↓
                            Update status in DB
```

**Example**: Audio transcription
```
1. POST /api/stt/transcribe → Returns job_id immediately
2. Worker processes audio asynchronously
3. GET /api/stt/jobs/{job_id} → Check status
4. GET /api/stt/transcripts/{transcript_id} → Get result
```

#### Pattern 3: Service-to-Service
**Used For**: Internal communication

```
Service A → Service B (with JWT forwarding)
```

**Example**: LLM service needs user info
```
llm-service → auth-service (verify token)
```

---

## Data Architecture

### Database: PostgreSQL (Port 5432)

#### Schema Organization

**authentication** schema:
- users
- oauth_connections
- refresh_tokens
- password_reset_tokens

**content** schema:
- study_materials
- documents
- transcriptions
- tts_audio_files
- recordings

**interaction** schema:
- conversations
- messages
- user_activity

**jobs** schema:
- jobs
- job_results
- job_logs

#### Database Connections

- **Connection Pooling**: 10-50 connections per service
- **Idle Timeout**: 300 seconds
- **Max Connection Age**: 3600 seconds
- **Connection Recycling**: Enabled

---

### Cache: Redis (Port 6379)

#### Database Allocations

- **DB 0**: Sessions (authentication)
- **DB 1**: Job queue (async jobs)
- **DB 2**: Cache (general purpose)
- **DB 3**: Rate limiting

#### Redis Usage Patterns

**Sessions:**
```
Key: session:{session_id}
TTL: 3600 seconds (1 hour)
Value: JSON {user_id, email, login_time}
```

**Job Queue:**
```
Queue: jobs:pending
Worker: jobs:processing:{worker_id}
Results: jobs:results:{job_id}
TTL: 86400 seconds (24 hours)
```

**Rate Limiting:**
```
Key: rate_limit:{user_id}:{action}
TTL: Varies (60s for login, 3600s for registration)
Value: Counter
```

---

### Vector Databases

#### Qdrant (Production) - Port 6333

**Collections:**
- study_materials_embeddings
- conversation_history_embeddings

**Embedding Model**: sentence-transformers/all-MiniLM-L6-v2

**Vector Dimensions**: 384

#### ChromaDB (Development) - Port 8000

**Collections:**
- poc_research (created during POC 12)
- authentication_research (POC 12)
- development_notes

---

## Network Architecture

### Docker Network: lm-network

**Type**: Bridge network  
**Driver**: bridge  
**Subnet**: Auto-assigned by Docker

#### Service Connectivity

```
┌─────────────────────────────────────────────────────────┐
│                    lm-network                            │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐           │
│  │  Gateway │   │   Auth   │   │   STT    │           │
│  │   :80    │◄──┤  :8001   │   │  :8002   │           │
│  └─────┬────┘   └────┬─────┘   └────┬─────┘           │
│        │             │              │                   │
│        │    ┌────────┴──────────────┴─────┐            │
│        │    │       Shared Resources      │            │
│        │    │  ┌──────────┐  ┌──────────┐ │            │
│        │    │  │PostgreSQL│  │  Redis   │ │            │
│        │    │  │  :5432   │  │  :6379   │ │            │
│        │    │  └──────────┘  └──────────┘ │            │
│        │    └─────────────────────────────┘            │
│        │                                                │
│  ┌─────▼────┐   ┌──────────┐   ┌──────────┐           │
│  │   TTS    │   │   LLM    │   │  Jobs    │           │
│  │  :8003   │   │  :8005   │   │  :8006   │           │
│  └──────────┘   └────┬─────┘   └────┬─────┘           │
│                      │              │                   │
│                 ┌────▼─────┐   ┌────▼─────┐            │
│                 │  Qdrant  │   │  Ollama  │            │
│                 │  :6333   │   │  :11434  │            │
│                 └──────────┘   └──────────┘            │
└─────────────────────────────────────────────────────────┘
```

### Port Allocation

| Service | Internal Port | External Port | Protocol |
|---------|---------------|---------------|----------|
| API Gateway | 80, 443 | 80, 443 | HTTP/HTTPS |
| Authentication | 8000 | 8001 | HTTP |
| Speech-to-Text | 8000 | 8002 | HTTP |
| Text-to-Speech | 8000 | 8003 | HTTP |
| Audio Recording | 8000 | 8004 | HTTP |
| LLM Agent | 8000 | 8005 | HTTP |
| Async Jobs | 8000 | 8006 | HTTP |
| PostgreSQL | 5432 | 5432 | TCP |
| Redis | 6379 | 6379 | TCP |
| Qdrant | 6333 | 6333 | HTTP |
| ChromaDB | 8000 | 8000 | HTTP |
| Ollama | 11434 | 11434 | HTTP |
| Adminer | 8080 | 8080 | HTTP |

**Note**: All services use internal port 8000, mapped to different external ports

---

## Security Architecture

### Authentication Flow

```
1. User → API Gateway → Auth Service
2. Auth Service validates credentials
3. Auth Service generates JWT tokens
4. Returns: {access_token, refresh_token}
5. User includes access_token in subsequent requests
```

### Authorization Flow

```
1. Request → API Gateway (validates JWT signature)
2. API Gateway forwards with verified user_id
3. Service checks user permissions
4. Service returns response or 403 Forbidden
```

### Inter-Service Authentication

```
Service A → Service B:
  Headers: Authorization: Bearer <service_jwt>
  
Service B validates:
  1. JWT signature
  2. Token not expired
  3. Token type = "service"
  4. Service A authorized to call Service B
```

### Data Encryption

**At Rest:**
- Database: PostgreSQL built-in encryption
- Sensitive fields: Application-level encryption (AES-256)
- OAuth tokens: Encrypted before storage

**In Transit:**
- External: HTTPS/TLS 1.3
- Internal: HTTP (Docker network isolation)
- Production Internal: mTLS (future enhancement)

---

## Deployment Architecture

### Local Development Deployment

```
Developer Machine
├── Docker Desktop (or Docker Engine)
├── docker-compose.yml
└── Containers:
    ├── Infrastructure (postgres, redis, qdrant, ollama)
    ├── Services (auth, stt, tts, llm, jobs)
    └── Gateway (nginx)
```

**Commands:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f service-name

# Scale a service
docker-compose up -d --scale llm-service=3

# Stop all services
docker-compose down
```

### Local Server Deployment (Bigger Hardware)

**Same architecture, better performance:**
- More CPU cores → More service replicas
- More RAM → Larger model support (Ollama 7B/13B)
- More GPU → Faster LLM inference
- **No Code Changes Required**

**Migration Steps:**
1. Export Docker images: `docker save`
2. Transfer to new server
3. Import images: `docker load`
4. Run same `docker-compose up -d`

---

### Cloud Deployment Strategy (AWS - Future)

#### AWS Services Mapping

| Local Component | AWS Equivalent | Notes |
|----------------|----------------|-------|
| Docker Containers | ECS/EKS/App Runner | ECS recommended initially |
| PostgreSQL | RDS PostgreSQL | Managed database |
| Redis | ElastiCache Redis | Managed cache |
| Qdrant | Self-hosted on EC2 or ECS | No managed service yet |
| Ollama | Bedrock | Use Claude/Titan models |
| Load Balancer | ALB/NLB | Application Load Balancer |
| File Storage | S3 | Object storage |
| Monitoring | CloudWatch | Logs & metrics |

#### AWS Architecture Diagram

```
Internet
   ↓
Route 53 (DNS)
   ↓
CloudFront (CDN)
   ↓
ALB (Load Balancer)
   ↓
┌────────────────────────────────────┐
│  AWS ECS Cluster                   │
│  ┌────────┐  ┌────────┐  ┌───────┐│
│  │Auth Svc│  │STT Svc │  │TTS Svc││
│  │ Task   │  │ Task   │  │ Task  ││
│  └────┬───┘  └───┬────┘  └───┬───┘│
│       │          │           │    │
│  ┌────▼──────────▼───────────▼───┐│
│  │      RDS PostgreSQL             ││
│  │      ElastiCache Redis          ││
│  │      S3 (file storage)          ││
│  └─────────────────────────────────┘│
└────────────────────────────────────┘
```

---

## Service Design Patterns

### 1. API First Design

Each service exposes RESTful API with OpenAPI specification:

```yaml
# Example: auth-service OpenAPI
openapi: 3.0.0
info:
  title: Authentication Service API
  version: 1.0.0
paths:
  /register:
    post:
      summary: Register new user
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                email: string
                password: string
      responses:
        201:
          description: User created
        400:
          description: Validation error
```

### 2. Health Check Pattern

All services implement health checks:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow(),
        "dependencies": {
            "database": check_db_connection(),
            "redis": check_redis_connection()
        }
    }
```

### 3. Circuit Breaker Pattern

Services implement circuit breakers for external dependencies:

```python
@circuit_breaker(failure_threshold=5, timeout=60)
async def call_external_service():
    # If 5 failures occur, circuit opens for 60s
    # Prevents cascading failures
    pass
```

### 4. Retry Pattern

Failed operations retry with exponential backoff:

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def process_job(job):
    # Retries 3 times: 2s, 4s, 8s delays
    pass
```

### 5. Event-Driven Pattern (Future)

For loosely coupled services:

```
Service A → Publish event → Message Bus (Redis/RabbitMQ)
                                ↓
                           Service B subscribes
```

---

## Observability Architecture

### Logging Strategy

**Structured Logging** (JSON format):
```json
{
  "timestamp": "2025-11-01T18:00:00Z",
  "level": "INFO",
  "service": "auth-service",
  "trace_id": "abc-123",
  "user_id": 456,
  "action": "login",
  "duration_ms": 45,
  "status": "success"
}
```

**Log Levels:**
- ERROR: Service errors, exceptions
- WARN: Degraded performance, retries
- INFO: Important operations (login, registration)
- DEBUG: Detailed debugging (dev only)

**Log Storage:**
- Local: Docker volume mounts
- Production: Centralized logging (ELK stack or CloudWatch)

### Monitoring Stack

**Metrics to Track:**
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (errors/total requests)
- Service uptime
- Database connections
- Redis queue length
- Memory/CPU usage per service

**Tools:**
- Local: Docker stats, logs
- Production: Prometheus + Grafana or CloudWatch

### Distributed Tracing

**Trace Context Propagation:**
```
trace_id: Unique ID for entire request flow
span_id: Unique ID for each service call
parent_span_id: Link to calling service
```

**Flow:**
```
Client Request (trace_id: ABC)
  → API Gateway (span_id: 1)
    → Auth Service (span_id: 2, parent: 1)
      → Database Query (span_id: 3, parent: 2)
```

---

## Scalability Architecture

### Horizontal Scaling

#### Service Scaling

```bash
# Scale LLM service to 3 replicas
docker-compose up -d --scale llm-service=3

# API Gateway load balances across replicas
```

#### Database Scaling (Future)

```
Master (Write) ← Services write here
    ↓ Replication
Replica 1 (Read) ← Services read here
Replica 2 (Read) ← Load balanced
```

#### Redis Scaling (Future)

```
Redis Sentinel (High Availability)
  Master ← Write operations
    ↓ Replication
  Slave 1 ← Read operations
  Slave 2 ← Automatic failover
```

### Vertical Scaling

**Current Limits** (local deployment):
- Each service: 0.5-2 CPU cores
- Each service: 512MB-2GB RAM
- PostgreSQL: 2GB RAM
- Ollama: 4-8GB RAM (model dependent)

**Bigger Server** (recommended specs):
- 16-32 CPU cores
- 64-128GB RAM
- 1TB SSD storage
- GPU (optional, for faster LLM inference)

---

## Disaster Recovery Architecture

### Backup Strategy

**Daily Backups:**
- PostgreSQL: pg_dump → S3-compatible storage
- Redis: RDB snapshots → Volume backup
- Vector DBs: Qdrant snapshots
- User files: Copy to backup storage

**Retention Policy:**
- Daily: Keep 7 days
- Weekly: Keep 4 weeks
- Monthly: Keep 12 months

### Recovery Procedures

**Service Failure:**
1. Docker restarts container automatically
2. Health check fails → Alert triggered
3. If 3 restarts fail → Manual intervention

**Database Failure:**
1. Restore from latest backup
2. Replay transaction logs (if available)
3. Verify data integrity

**Complete System Failure:**
1. Deploy fresh infrastructure
2. Restore PostgreSQL from backup
3. Restore Redis from snapshot
4. Rebuild vector DB embeddings
5. Verify all services healthy

---

## Technology Stack Details

### Backend Services

**Framework**: FastAPI
- Async/await support
- Automatic OpenAPI documentation
- Pydantic validation
- Dependency injection
- WebSocket support

**Language**: Python 3.11+
- Type hints
- Dataclasses
- Async/await
- Modern syntax

**ORM**: SQLAlchemy 2.0
- Async support
- Connection pooling
- Migration support (Alembic)

### Frontend Applications

**Web**: React + Next.js
- Server-side rendering
- Static site generation
- API routes
- TypeScript

**Mobile**: React Native
- Cross-platform (iOS & Android)
- Native performance
- Shared codebase

**Desktop**: Electron or Tauri
- Cross-platform (Windows, macOS, Linux)
- Native system access
- Web technologies

### Infrastructure

**Containerization**: Docker
- Multi-stage builds
- Layer caching
- Health checks
- Volume management

**Orchestration**: Docker Compose
- Service dependencies
- Network management
- Volume management
- Environment variables

**Future**: Kubernetes
- Auto-scaling
- Self-healing
- Rolling updates
- Service mesh

---

## Performance Optimization

### Caching Strategy

**Level 1: Browser Cache**
- Static assets: 1 year
- API responses: Configurable per endpoint

**Level 2: Redis Cache**
- Frequently accessed data: 5-60 minutes
- User sessions: 1 hour
- API response cache: 1-5 minutes

**Level 3: Database Query Cache**
- PostgreSQL query results: 1-10 minutes
- Vector DB results: 5 minutes

### Database Optimization

**Indexes:**
- Primary keys (auto)
- Foreign keys
- Frequently queried columns
- Composite indexes for common queries

**Query Optimization:**
- Use prepared statements
- Limit result sets
- Paginate large results
- Use database-side aggregation

### API Optimization

**Response Compression:**
- Gzip for JSON responses >1KB
- Reduces bandwidth by 60-80%

**Connection Pooling:**
- Reuse HTTP connections
- Reduce connection overhead

**Async Processing:**
- Long operations → Background jobs
- Return job ID immediately
- Poll for results

---

## Monitoring & Alerting

### Key Metrics

**Service Metrics:**
- Request rate
- Response time (p50, p95, p99)
- Error rate
- Active connections
- Memory usage
- CPU usage

**Business Metrics:**
- Active users
- Registrations per day
- Transcriptions per hour
- Chat messages per hour
- Storage used

### Alert Thresholds

**Critical Alerts:**
- Service down for >1 minute
- Error rate >5%
- Response time p95 >1 second
- Database connections >90% of pool
- Disk usage >90%

**Warning Alerts:**
- Error rate >2%
- Response time p95 >500ms
- Database connections >70% of pool
- Disk usage >75%

---

## Migration Path: Local → Bigger Server → AWS

### Phase 1: Current (Local Dev Machine)
```
Hardware: Standard desktop/laptop
Specs: 8-16GB RAM, 4-8 cores
Services: All running, may be slow
Purpose: Development and testing
```

### Phase 2: Bigger Local Server (Next)
```
Hardware: Dedicated server
Specs: 64-128GB RAM, 16-32 cores, Optional GPU
Services: Same containers, better performance
Migration: docker save → transfer → docker load
Purpose: Production-quality local deployment
```

### Phase 3: AWS Cloud (Future)
```
Infrastructure: AWS ECS/EKS
Managed Services: RDS, ElastiCache, Bedrock
Services: Same containers → AWS repositories
Migration: Push images to ECR → Deploy
Purpose: Global scale, high availability
```

**Key Point**: **Code doesn't change** between phases - only infrastructure configuration!

---

## Security Considerations

### Network Security

**External Traffic:**
- HTTPS only (TLS 1.3)
- API Gateway SSL termination
- Certificate management (Let's Encrypt)

**Internal Traffic:**
- HTTP within Docker network (isolated)
- No external access to internal services
- Future: mTLS for service-to-service

### API Security

**Rate Limiting:**
```nginx
# Nginx rate limiting
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
```

**CORS Policy:**
```python
origins = [
    "http://localhost:3000",  # Dev
    "https://littlemonster.com",  # Prod
]
```

**Input Validation:**
- Pydantic models for all inputs
- SQL parameterization
- XSS prevention
- File type validation

---

## Appendices

### Appendix A: Service Dependencies

| Service | Depends On | Optional Dependencies |
|---------|------------|----------------------|
| API Gateway | All services | - |
| Auth Service | PostgreSQL, Redis | SMTP server |
| STT Service | PostgreSQL, Redis, Jobs Service | - |
| TTS Service | - | Azure API, Coqui container |
| Audio Service | PostgreSQL | STT Service |
| LLM Service | PostgreSQL, Qdrant, Ollama | AWS Bedrock |
| Jobs Service | Redis, PostgreSQL | - |
| Jobs Worker | Redis, PostgreSQL | All job-executing services |

### Appendix B: Container Resource Limits

**Development:**
```yaml
resources:
  limits:
    cpus: '1.0'
    memory: 1G
  reservations:
    cpus: '0.5'
    memory: 512M
```

**Production (Bigger Server):**
```yaml
resources:
  limits:
    cpus: '4.0'
    memory: 8G
  reservations:
    cpus: '2.0'
    memory: 4G
```

### Appendix C: Database Connection Strings

**Format:**
```
postgresql://user:password@host:port/database
redis://host:port/db
http://host:port (vector DBs)
```

**Service to Service:**
```python
