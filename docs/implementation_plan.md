# Little Monster - Implementation Plan

## Document Control
- **Version**: 1.0
- **Date**: November 1, 2025
- **Status**: Ready for Implementation
- **Related Documents**: PROJECT-STRUCTURE.md, TECHNICAL-ARCHITECTURE.md, IMPLEMENTATION-ROADMAP.md

---

## [Overview]

Build a production-ready AI-powered educational platform by migrating 12 validated POCs into a microservices architecture with containerized deployment.

The Little Monster platform transforms validated proof-of-concepts into a scalable, production-ready system that provides AI tutoring, speech transcription, text-to-speech, and study material generation. The implementation will create 6 core microservices (Authentication, Speech-to-Text, Text-to-Speech, Audio Recording, LLM Agent, Async Jobs), each independently deployable via Docker containers, orchestrated by Docker Compose, and accessible through a unified API Gateway.

This plan leverages:
- **12 validated POCs** with working code and test results
- **Existing infrastructure** (PostgreSQL, Redis, Qdrant, Ollama already running)
- **Previous UI work** from old/Ella-Ai for frontend components
- **Comprehensive documentation** defining requirements, architecture, and structure

The implementation follows an incremental migration strategy: extract core functionality from POCs, wrap in FastAPI services, containerize, test, and integrate. Each service maintains independence while communicating via REST APIs, with all services sharing a common PostgreSQL database and Redis cache/queue.

Key architectural decisions:
- **Microservices**: Each POC becomes an independent service
- **Docker-first**: All components containerized for portability
- **API Gateway**: Nginx for unified entry point and routing
- **Shared Database**: PostgreSQL with consolidated schema
- **Message Queue**: Redis for async job processing
- **Vector Search**: Qdrant for RAG capabilities
- **Local + Cloud**: Ollama (local LLM) + AWS Bedrock (cloud LLM)

Success criteria: All 6 services running in Docker, API Gateway routing traffic, web application deployed, users can register/login/chat/transcribe, comprehensive tests passing, ready for deployment to bigger server or cloud.

---

## [Types]

Define data structures, enums, and type definitions used across the system.

### Database Models (SQLAlchemy ORM)

**User Types:**
```python
class User(Base):
    """User account with authentication credentials"""
    id: int (PK)
    email: str (unique, indexed)
    username: str (unique, indexed)
    password_hash: Optional[str]  # NULL for OAuth-only
    full_name: Optional[str]
    is_verified: bool (default=False)
    is_active: bool (default=True, indexed)
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

class OAuthConnection(Base):
    """OAuth provider connection"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    provider: str  # 'google', 'facebook', 'microsoft'
    provider_user_id: str
    provider_email: Optional[str]
    provider_name: Optional[str]
    access_token: Optional[str] (text)
    refresh_token: Optional[str] (text)
    token_expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

class RefreshToken(Base):
    """JWT refresh tokens"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    token_hash: str (unique, indexed)
    expires_at: datetime (indexed)
    created_at: datetime
    revoked: bool (default=False, indexed)
    revoked_at: Optional[datetime]

class PasswordResetToken(Base):
    """Password reset tokens"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    token_hash: str (unique, indexed)
    expires_at: datetime (indexed)
    created_at: datetime
    used: bool (default=False, indexed)
    used_at: Optional[datetime]
```

**Content Types:**
```python
class TranscriptionJob(Base):
    """Speech-to-text transcription jobs"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    audio_file_path: str
    audio_file_size: int
    audio_duration: Optional[float]
    status: str (indexed)  # 'pending', 'processing', 'completed', 'failed'
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]

class Transcription(Base):
    """Completed transcriptions"""
    id: int (PK)
    job_id: int (FK -> transcription_jobs.id, unique)
    user_id: int (FK -> users.id, indexed)
    text: str (text)
    confidence: Optional[float]
    language: Optional[str]
    created_at: datetime

class TTSAudioFile(Base):
    """Text-to-speech generated audio"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    text: str (text)
    voice: str
    provider: str  # 'azure', 'coqui'
    file_path: str
    file_size: int
    duration: Optional[float]
    created_at: datetime

class Recording(Base):
    """Audio recordings"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    file_path: str
    file_size: int
    duration: Optional[float]
    recording_type: str  # 'lecture', 'note', 'other'
    created_at: datetime
```

**Conversation Types:**
```python
class Conversation(Base):
    """Chat conversations with AI tutor"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

class Message(Base):
    """Individual messages in conversations"""
    id: int (PK)
    conversation_id: int (FK -> conversations.id, indexed)
    role: str  # 'user', 'assistant', 'system'
    content: str (text)
    created_at: datetime

class StudyMaterial(Base):
    """Study materials for RAG"""
    id: int (PK)
    user_id: int (FK -> users.id, indexed)
    title: str
    content: str (text)
    file_path: Optional[str]
    subject: Optional[str]
    created_at: datetime
    updated_at: datetime
```

**Job Queue Types:**
```python
class Job(Base):
    """Async job queue entries"""
    id: int (PK)
    user_id: Optional[int] (FK -> users.id, indexed)
    job_type: str (indexed)  # 'transcription', 'tts', 'presentation'
    status: str (indexed)  # 'pending', 'processing', 'completed', 'failed'
    priority: int (default=0, indexed)
    payload: str (JSON text)
    result: Optional[str] (JSON text)
    error_message: Optional[str]
    retry_count: int (default=0)
    max_retries: int (default=3)
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
```

### API Request/Response Schemas (Pydantic)

**Authentication Schemas:**
```python
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars, must have upper, lower, number, special
    username: Optional[str]
    full_name: Optional[str]

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds

class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str]
    full_name: Optional[str]
    is_verified: bool
    created_at: datetime
```

**STT Schemas:**
```python
class TranscribeRequest(BaseModel):
    # File uploaded as multipart/form-data
    language: Optional[str] = "en"

class TranscriptionJobResponse(BaseModel):
    job_id: int
    status: str
    created_at: datetime

class TranscriptionResponse(BaseModel):
    id: int
    job_id: int
    text: str
    confidence: Optional[float]
    created_at: datetime
```

**TTS Schemas:**
```python
class TTSGenerateRequest(BaseModel):
    text: str
    voice: Optional[str] = "default"
    provider: Optional[str] = "azure"  # 'azure' or 'coqui'

class TTSAudioResponse(BaseModel):
    id: int
    file_url: str
    duration: Optional[float]
    provider: str
    created_at: datetime
```

**LLM Schemas:**
```python
class ChatMessageRequest(BaseModel):
    conversation_id: Optional[int]
    message: str
    use_rag: bool = True

class ChatMessageResponse(BaseModel):
    conversation_id: int
    message_id: int
    response: str
    sources: Optional[List[str]]
    created_at: datetime
```

### Enums

```python
class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(str, Enum):
    TRANSCRIPTION = "transcription"
    TTS = "tts"
    PRESENTATION = "presentation"

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    MICROSOFT = "microsoft"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
```

---

## [Files]

Complete file structure creation and modification plan.

### New Files to Create

**Root Infrastructure:**
```
/docker-compose.yml - Main orchestration file
/docker-compose.dev.yml - Development overrides
/docker-compose.prod.yml - Production overrides
/infrastructure/.env.example - Environment variables template
/infrastructure/.env - Local environment (gitignored)
```

**Services - Authentication (services/authentication/):**
```
services/authentication/
├── src/
│   ├── main.py - FastAPI app entry point
│   ├── config.py - Configuration from environment
│   ├── models.py - SQLAlchemy models (from POC 12)
│   ├── schemas.py - Pydantic request/response schemas
│   ├── dependencies.py - FastAPI dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py - /register, /login, /logout, /refresh
│   │   ├── oauth.py - OAuth endpoints
│   │   └── users.py - /me, profile endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py - Business logic
│   │   ├── oauth_service.py - OAuth handling
│   │   └── jwt_service.py - JWT operations
│   └── utils/
│       ├── __init__.py
│       ├── password.py - bcrypt hashing (from POC 12)
│       ├── jwt.py - JWT generation/validation (from POC 12)
│       └── validators.py - Input validation
├── tests/
│   ├── test_auth.py
│   ├── test_oauth.py
│   └── test_jwt.py
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

**Services - Speech-to-Text (services/speech-to-text/):**
```
services/speech-to-text/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models.py - TranscriptionJob, Transcription
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── transcribe.py - /transcribe endpoint
│   │   └── jobs.py - /jobs endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── whisper_service.py - Whisper integration (from POC 09)
│   │   └── job_service.py - Job management
│   └── utils/
│       ├── __init__.py
│       └── audio_utils.py - Audio processing
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

**Services - Text-to-Speech (services/text-to-speech/):**
```
services/text-to-speech/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models.py - TTSAudioFile
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── generate.py - /generate endpoint
│   │   └── voices.py - /voices endpoint
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azure_tts.py - Azure TTS (from POC 11)
│   │   └── coqui_tts.py - Coqui TTS (from POC 11.1)
│   └── utils/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

**Services - Audio Recording (services/audio-recording/):**
```
services/audio-recording/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models.py - Recording
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── record.py - Recording endpoints
│   │   └── upload.py - File upload
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recorder.py - Recording logic (from POC 10)
│   │   └── storage.py - File storage
│   └── utils/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

**Services - LLM Agent (services/llm-agent/):**
```
services/llm-agent/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── models.py - Conversation, Message, StudyMaterial
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py - Chat endpoints
│   │   └── materials.py - Study materials
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent_service.py - LangChain agent (from POC 07)
│   │   ├── rag_service.py - RAG logic (from POC 00)
│   │   └── vector_service.py - Qdrant integration
│   └── utils/
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md
```

**Services - Async Jobs (services/async-jobs/):**
```
services/async-jobs/
├── src/
│   ├── main.py - FastAPI for job API
│   ├── worker.py - Background worker process
│   ├── config.py
│   ├── models.py - Job
│   ├── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── jobs.py - Job endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── queue_service.py - Redis queue (from POC 08)
│   │   └── worker_service.py - Job processing
│   └── utils/
├── tests/
├── Dockerfile.api
├── Dockerfile.worker
├── requirements.txt
└── README.md
```

**Services - API Gateway (services/api-gateway/):**
```
services/api-gateway/
├── nginx.conf - Main nginx configuration
├── ssl/ - SSL certificates (development)
├── Dockerfile
└── README.md
```

**Database:**
```
database/
├── schemas/
│   ├── 001_authentication.sql - From POC 12
│   ├── 002_transcription.sql - From POC 09
│   ├── 003_async_jobs.sql - From POC 08
│   ├── 004_content.sql - Study materials, etc.
│   ├── 005_interaction.sql - Conversations, messages
│   └── master-schema.sql - Consolidated
├── migrations/
│   ├── versions/
│   │   └── 001_initial_schema.py
│   ├── alembic.ini
│   └── env.py
├── seeds/
│   ├── users.sql - Test users
│   └── study_materials.sql - Sample materials
└── scripts/
    ├── backup.sh
    ├── restore.sh
    ├── migrate.sh
    └── reset.sh
```

**Views - Web App:**
```
views/web-app/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── chat/page.tsx
│   │   │   ├── transcribe/page.tsx
│   │   │   ├── materials/page.tsx
│   │   │   └── recordings/page.tsx
│   │   └── layout.tsx
│   ├── components/
│   │   ├── auth/ - Auth forms
│   │   ├── chat/ - Chat interface
│   │   ├── audio/ - Audio components
│   │   └── ui/ - Reusable UI (from old/Ella-Ai)
│   ├── lib/
│   │   ├── api/ - API client
│   │   ├── auth/ - Auth utilities
│   │   └── utils/
│   ├── hooks/ - React hooks
│   ├── styles/ - CSS/Tailwind
│   └── types/ - TypeScript types
├── public/ - Static assets
├── Dockerfile
├── package.json
├── tsconfig.json
├── next.config.js
└── README.md
```

**Shared Libraries:**
```
shared/
├── python-common/
│   ├── lm_common/
│   │   ├── __init__.py
│   │   ├── auth/ - JWT validation middleware
│   │   ├── database/ - DB utilities
│   │   ├── redis/ - Redis utilities
│   │   ├── logging/ - Structured logging
│   │   └── utils/ - Generic utilities
│   ├── setup.py
│   └── README.md
└── typescript-common/
    ├── src/
    │   ├── api/ - API client
    │   ├── types/ - TypeScript types
    │   └── utils/ - Utilities
    ├── package.json
    ├── tsconfig.json
    └── README.md
```

**Tests:**
```
tests/
├── integration/
│   ├── test_auth_to_llm.py
│   ├── test_stt_to_jobs.py
│   └── test_complete_flow.py
├── e2e/
│   ├── scenarios/
│   │   ├── student_registration.py
│   │   ├── lecture_transcription.py
│   │   └── ai_tutoring.py
│   └── conftest.py
├── performance/
│   ├── locust/
│   │   └── locustfile.py
│   └── benchmarks/
└── fixtures/
```

**Scripts:**
```
scripts/
├── setup/
│   ├── create-folders.sh
│   ├── setup-local.sh
│   └── install-dependencies.sh
├── database/
│   ├── backup-db.sh
│   ├── restore-db.sh
│   ├── migrate-db.sh
│   └── reset-db.sh
├── docker/
│   ├── build-all.sh
│   ├── push-images.sh
│   └── cleanup.sh
├── deployment/
│   ├── deploy-local.sh
│   └── deploy-server.sh
└── utilities/
    ├── generate-secrets.py
    └── create-admin-user.py
```

### Existing Files to Modify

None. All POC and old code files remain untouched in their respective directories (poc/, old/) for reference.

### Files to Extract From

**From POC 12 (Authentication):**
- poc/12-authentication/models.py → services/authentication/src/models.py
- poc/12-authentication/jwt_utils.py → services/authentication/src/utils/jwt.py
- poc/12-authentication/password_utils.py → services/authentication/src/utils/password.py
- poc/12-authentication/schema.sql → database/schemas/001_authentication.sql

**From POC 09 (Speech-to-Text):**
- poc/09-speech-to-text/transcription_engine.py → services/speech-to-text/src/services/whisper_service.py
- poc/09-speech-to-text/transcription_worker.py → services/async-jobs/src/worker.py (transcription handler)
- poc/09-speech-to-text/schema.sql → database/schemas/002_transcription.sql

**From POC 11/11.1 (Text-to-Speech):**
- poc/11-text-to-speech/azure_tts.py → services/text-to-speech/src/services/azure_tts.py
- poc/11.1-coqui-tts/coqui_tts.py → services/text-to-speech/src/services/coqui_tts.py

**From POC 10 (Audio Recording):**
- poc/10-record-to-text/audio_recorder.py → services/audio-recording/src/services/recorder.py

**From POC 07 (LLM Agent):**
- poc/07-langchain-agent/agent.py → services/llm-agent/src/services/agent_service.py
- poc/07-langchain-agent/agent_bedrock.py → services/llm-agent/src/services/agent_service.py (Bedrock support)

**From POC 00 (RAG Chatbot):**
- poc/00-functional-poc/backend/rag_chatbot.py → services/llm-agent/src/services/rag_service.py
- poc/00-functional-poc/backend/content_loader.py → services/llm-agent/src/services/vector_service.py

**From POC 08 (Async Jobs):**
- poc/08-async-jobs/worker.py → services/async-jobs/src/worker.py
- poc/08-async-jobs/schema.sql → database/schemas/003_async_jobs.sql

**From old/Ella-Ai:**
- old/Ella-Ai/docker-compose.yml → /docker-compose.yml (base template)
- old/Ella-Ai/web-app/src/components/ → views/web-app/src/components/ui/ (UI components)

---

## [Functions]

Key function implementations across services.

### Authentication Service Functions

**New functions in services/authentication/src/routes/auth.py:**
```python
@router.post("/register", response_model=UserResponse)
async def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """Register new user with email/password"""
    # Validate email not exists
    # Validate password strength
    # Hash password with bcrypt
    # Create user record
    # Send verification email
    # Return user data

@router.post("/login", response_model=TokenResponse)
async def login_user(request: UserLoginRequest, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    """Login user and return JWT tokens"""
    # Validate credentials
    # Check if user is active
    # Generate access token (30 min expiry)
    # Generate refresh token (7 day expiry)
    # Store refresh token in DB
    # Store session in Redis
    # Update last_login timestamp
    # Return tokens

@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user and revoke tokens"""
    # Revoke refresh tokens
    # Remove session from Redis
    # Return success

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    # Validate refresh token
    # Check if revoked
    # Check expiry
    # Generate new access token
    # Return new tokens

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    # Return user data
```

**Modified functions from POC 12:**
- `hash_password()` from poc/12-authentication/password_utils.py → services/authentication/src/utils/password.py (keep as-is)
- `verify_password()` from POC 12 (keep as-is)
- `create_access_token()` from poc/12-authentication/jwt_utils.py → services/authentication/src/utils/jwt.py (keep as-is)
- `create_refresh_token()` from POC 12 (keep as-is)
- `verify_token()` from POC 12 (keep as-is)

### Speech-to-Text Service Functions

**New functions in services/speech-to-text/src/routes/transcribe.py:**
```python
@router.post("/transcribe", response_model=TranscriptionJobResponse)
async def create_transcription_job(
    file: UploadFile = File(...),
    language: Optional[str] = "en",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """Upload audio file and create transcription job"""
    # Validate file type (mp3, wav, m4a, flac, ogg)
    # Validate file size (<50MB)
    # Save file to storage
    # Create transcription job record
    # Queue job in Redis
    # Return job ID

@router.get("/jobs/{job_id}", response_model=TranscriptionJobResponse)
async def get_job_status(job_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get transcription job status"""
    # Check job ownership
    # Return job status

@router.get("/transcripts/{transcript_id}", response_model=TranscriptionResponse)
async def get_transcript(transcript_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get completed transcription"""
    # Check ownership
    # Return transcript
```

**Modified functions from POC 09:**
- `transcribe_audio()` from poc/09-speech-to-text/transcription_engine.py → services/speech-to-text/src/services/whisper_service.py (keep core logic, add error handling)
- `process_transcription_job()` from poc/09-speech-to-text/transcription_worker.py → services/async-jobs/src/worker.py (integrate as job handler)

### Text-to-Speech Service Functions

**New functions in services/text-to-speech/src/routes/generate.py:**
```python
@router.post("/generate", response_model=TTSAudioResponse)
async def generate_speech(
    request: TTSGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate speech from text"""
    # Validate text length (<10000 chars)
    # Select provider (Azure primary, Coqui fallback)
    # Generate audio
    # Save file
    # Create database record
    # Return file URL

@router.get("/voices", response_model=List[VoiceInfo])
async def list_voices():
    """List available voices"""
    # Return voice options
```

**Modified functions from POC 11/11.1:**
- `synthesize_speech()` from poc/11-text-to-speech/azure_tts.py → services/text-to-speech/src/services/azure_tts.py (keep as-is, add retries)
- `generate_audio()` from poc/11.1-coqui-tts/coqui_tts.py → services/text-to-speech/src/services/coqui_tts.py (keep as-is)

### LLM Agent Service Functions

**New functions in services/llm-agent/src/routes/chat.py:**
```python
@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message to AI tutor"""
    # Get or create conversation
    # Store user message
    # If use_rag: retrieve relevant context
    # Call LLM agent
    # Store assistant response
    # Return response

@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List user's conversations"""
    # Return conversations

@router.post("/upload-material", response_model=StudyMaterialResponse)
async def upload_study_material(
    file: UploadFile = File(...),
    title: str = Form(...),
    subject: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload study material"""
    # Save file
    # Extract text
    # Create embeddings
    # Store in Qdrant
    # Create database record
    # Return material info
```

**Modified functions from POC 07:**
- `create_agent()` from poc/07-langchain-agent/agent.py → services/llm-agent/src/services/agent_service.py (wrap in service class)
- `chat()` from POC 07 (integrate as method)
- `create_bedrock_agent()` from poc/07-langchain-agent/agent_bedrock.py (integrate as fallback)

**Modified functions from POC 00:**
- `load_documents()` from poc/00-functional-poc/backend/content_loader.py → services/llm-agent/src/services/vector_service.py
- `query_documents()` from POC 00 (integrate)

### Async Jobs Worker Functions

**New functions in services/async-jobs/src/worker.py:**
```python
async def process_job(job: Job, db: Session, redis: Redis):
    """Main job processing dispatcher"""
    # Update status to processing
    # Route to appropriate handler based on job_type
    # Execute handler
    # Store result
    # Update status to completed/failed
    # Handle retries on failure

async def handle_transcription_job(job: Job, db: Session):
    """Handle transcription jobs"""
    # Load audio file
    # Call Whisper service
    # Store transcription
    # Return result

async def handle_tts_job(job: Job, db: Session):
    """Handle TTS jobs"""
    # Extract text
    # Call TTS service
    # Store audio file
    # Return result

async def handle_presentation_job(job: Job, db: Session):
    """Handle presentation generation jobs"""
    # Extract content
    # Call presentation service
    # Store PPTX file
    # Return result
```

**Modified functions from POC 08:**
- `worker_loop()` from poc/08-async-jobs/worker.py → services/async-jobs/src/worker.py (modernize)
- `enqueue_job()` from POC 08 → services/async-jobs/src/services/queue_service.py

---

## [Classes]

Key class definitions and their responsibilities.

### Service Configuration Classes

```python
class ServiceConfig:
    """Base configuration for all services"""
    DATABASE_URL: str
    REDIS_URL: str
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    
class AuthConfig(ServiceConfig):
    """Authentication service configuration"""
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    GOOGLE_CLIENT_ID: Optional[str]
    GOOGLE_CLIENT_SECRET: Optional[str]
    FACEBOOK_CLIENT_ID: Optional[str]
    FACEBOOK_CLIENT_SECRET: Optional[str]
    MICROSOFT_CLIENT_ID: Optional[str]
    MICROSOFT_CLIENT_SECRET: Optional[str]

class LLMConfig(ServiceConfig):
    """LLM service configuration"""
    QDRANT_URL: str = "http://qdrant:6333"
    OLLAMA_URL: str = "http://ollama:11434"
    AWS_REGION: Optional[str]
    AWS_ACCESS_KEY_ID: Optional[str]
    AWS_SECRET_ACCESS_KEY: Optional[str]
    USE_BEDROCK: bool = False
    
class TTSConfig(ServiceConfig):
    """TTS service configuration"""
    AZURE_SPEECH_KEY: Optional[str]
    AZURE_REGION: Optional[str]
    USE_AZURE: bool = True
    USE_COQUI: bool = False
    COQUI_MODEL: str = "tts_models/en/ljspeech/tacotron2-DDC"
```

### Service Classes (Business Logic)

```python
class AuthService:
    """Authentication business logic"""
    def __init__(self, db: Session, redis: Redis, config: AuthConfig):
        self.db = db
        self.redis = redis
        self.config = config
        
    async def register_user(self, email: str, password: str, username: Optional[str]) -> User:
        """Register new user"""
        
    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user credentials"""
        
    async def create_tokens(self, user: User) -> TokenResponse:
        """Generate access and refresh tokens"""
        
    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token"""

class WhisperService:
    """Speech-to-text service using Whisper"""
    def __init__(self, model_name: str = "base.en"):
        self.model = whisper.load_model(model_name)
        
    async def transcribe(self, audio_file_path: str, language: str = "en") -> Dict[str, Any]:
        """Transcribe audio file"""

class AzureTTSService:
    """Azure text-to-speech service"""
    def __init__(self, api_key: str, region: str):
        self.api_key = api_key
        self.region = region
        self.speech_config = speechsdk.SpeechConfig(subscription=api_key, region=region)
        
    async def synthesize(self, text: str, voice: str = "en-US-JennyNeural") -> bytes:
        """Generate speech from text"""

class LLMAgentService:
    """LLM agent with RAG capabilities"""
    def __init__(self, config: LLMConfig, vector_service: VectorService):
        self.config = config
        self.vector_service = vector_service
        self.ollama_agent = self._create_ollama_agent()
        self.bedrock_agent = self._create_bedrock_agent() if config.USE_BEDROCK else None
        
    async def chat(self, message: str, conversation_history: List[Message], use_rag: bool = True) -> str:
        """Process chat message with optional RAG"""
        
class VectorService:
    """Vector database operations for RAG"""
    def __init__(self, qdrant_url: str):
        self.client = QdrantClient(qdrant_url)
        self.collection_name = "study_materials"
        
    async def add_document(self, text: str, metadata: Dict[str, Any]) -> str:
        """Add document to vector database"""
        
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents"""

class JobQueueService:
    """Redis-based job queue"""
    def __init__(self, redis: Redis):
        self.redis = redis
        self.queue_name = "jobs:pending"
        
    async def enqueue(self, job: Job) -> str:
        """Add job to queue"""
        
    async def dequeue(self) -> Optional[Job]:
        """Get next job from queue"""
        
    async def update_status(self, job_id: int, status: JobStatus, result: Optional[Dict] = None):
        """Update job status"""
```

### Modified Classes from POCs

- `User`, `OAuthConnection`, `RefreshToken`, `PasswordResetToken` from POC 12 → Keep as-is
- `TranscriptionJob`, `Transcription` from POC 09 → Keep as-is
- `Job` from POC 08 → Keep as-is

---

## [Dependencies]

External libraries and their versions for each service.

### Authentication Service (services/authentication/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic[email]==2.5.0
python-dotenv==1.0.0
requests==2.31.0
httpx==0.25.2
```

### Speech-to-Text Service (services/speech-to-text/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
openai-whisper==20231117
torch==2.1.1
torchaudio==2.1.1
numpy==1.24.3
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
```

### Text-to-Speech Service (services/text-to-speech/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
azure-cognitiveservices-speech==1.34.0
TTS==0.21.1  # Coqui TTS
pydantic==2.5.0
python-dotenv==1.0.0
```

### LLM Agent Service (services/llm-agent/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
langchain==0.0.340
langchain-community==0.0.1
qdrant-client==1.7.0
sentence-transformers==2.2.2
boto3==1.34.5  # For Bedrock
python-dotenv==1.0.0
```

### Async Jobs Service (services/async-jobs/requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.0
python-dotenv==1.0.0
```

### Shared Python Library (shared/python-common/requirements.txt)
```
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
python-jose[cryptography]==3.3.0
pydantic==2.5.0
```

---

## [Testing]

Testing strategy and requirements for validation.

### Unit Tests

**Per Service Testing:**
- Authentication: Test all auth routes, JWT generation/validation, password hashing
- STT: Test file upload, job creation, transcription logic
- TTS: Test audio generation, provider fallback
- LLM Agent: Test RAG retrieval, conversation management
- Jobs: Test queue operations, job processing, retries

**Coverage Target:** 80% minimum

### Integration Tests

**Cross-Service Tests (tests/integration/):**
```python
def test_auth_to_llm_flow():
    """Test authenticated user can chat with LLM"""
    # Register user
    # Login
    # Send chat message with JWT
    # Verify response

def test_transcription_workflow():
    """Test complete transcription workflow"""
    # Login
    # Upload audio file
    # Wait for job completion
    # Retrieve transcript
    # Verify accuracy

def test_complete_student_workflow():
    """Test end-to-end student experience"""
    # Register
    # Upload lecture recording
    # Transcribe lecture
    # Upload as study material
    # Chat with AI about material
    # Generate TTS for material
```

### End-to-End Tests

**User Scenarios (tests/e2e/scenarios/):**
- Student registration and first use
- Lecture recording and transcription
- AI tutoring session with RAG
- Study material management

### Performance Tests

**Load Testing with Locust (tests/performance/locust/locustfile.py):**
```python
class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Login before tasks"""
        self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "TestPass123!"
        })
    
    @task(3)
    def chat_with_ai(self):
        """Chat endpoint load test"""
        
    @task(1)
    def transcribe_audio(self):
        """Transcription endpoint load test"""
```

**Target Metrics:**
- 1000+ concurrent users
- <500ms response time (p95)
- <5% error rate

---

## [Implementation Order]

Step-by-step implementation sequence with dependencies.

### Phase 1: Foundation (Week 1-2)

**Step 1.1: Create Folder Structure**
```bash
# Create all service directories
mkdir -p services/{authentication,speech-to-text,text-to-speech,audio-recording,llm-agent,async-jobs,api-gateway}
mkdir -p database/{schemas,migrations,seeds,scripts}
mkdir -p views/web-app
mkdir -p shared/{python-common,typescript-common}
mkdir -p tests/{integration,e2e,performance,fixtures}
mkdir -p scripts/{setup,database,docker,deployment,utilities}
mkdir -p infrastructure/nginx
```

**Step 1.2: Database Setup**
- Extract schemas from POC 12, 09, 08
- Create consolidated master-schema.sql
- Set up Alembic migrations
- Create initial migration
- Apply migrations to PostgreSQL

**Step 1.3: Shared Libraries**
- Create python-common package
- Add JWT validation utilities
- Add database connection utilities
- Add Redis client utilities
- Add logging configuration

### Phase 2: Authentication Service (Week 3)

**Step 2.1: Service Structure**
- Create authentication service folders
- Copy models.py from POC 12
- Copy jwt_utils.py and password_utils.py from POC 12
- Create config.py with environment variables

**Step 2.2: API Implementation**
- Implement POST /register endpoint
- Implement POST /login endpoint
- Implement POST /logout endpoint
- Implement POST /refresh endpoint
- Implement GET /me endpoint

**Step 2.3: Testing & Docker**
- Write unit tests (10 tests from POC 12)
- Create Dockerfile
- Add to docker-compose.yml
- Test service independently

**Step 2.4: Integration**
- Test with PostgreSQL
- Test with Redis
- Verify JWT tokens work across services

### Phase 3: Core AI Services (Week 4)

**Step 3.1: LLM Agent Service**
- Extract agent.py from POC 07
- Extract rag_chatbot.py from POC 00
- Implement chat routes
- Integrate Qdrant
- Support Ollama and Bedrock
- Create Dockerfile

**Step 3.2: Speech-to-Text Service**
- Extract transcription_engine.py from POC 09
- Implement transcribe route
- Implement job status routes
- Integrate with async-jobs service
- Create Dockerfile

**Step 3.3: Service Integration**
- Test authentication with LLM service
- Test STT job creation and processing
- Verify end-to-end flows

### Phase 4: Content Services (Week 5)

**Step 4.1: Text-to-Speech Service**
- Extract azure_tts.py from POC 11
- Extract coqui_tts.py from POC 11.1
- Implement generate route
- Implement voices route
- Provider fallback logic
- Create Dockerfile

**Step 4.2: Audio Recording Service**
- Extract audio_recorder.py from POC 10
- Implement upload route
- Implement recording management
- File storage handling
- Create Dockerfile

**Step 4.3: Integration Testing**
- Test complete audio workflow
- Record → Transcribe → Study Material → TTS

### Phase 5: Job Processing (Week 6)

**Step 5.1: Async Jobs Service**
- Extract worker.py from POC 08
- Implement job API routes
- Implement worker process
- Job retry logic
- Create Dockerfiles (API + Worker)

**Step 5.2: Worker Integration**
- Integrate transcription handler
- Integrate TTS handler
- Test multi-worker setup
- Test job failures and retries

### Phase 6: API Gateway (Week 7)

**Step 6.1: Nginx Configuration**
- Create nginx.conf
- Route /api/auth → auth-service:8000
- Route /api/stt → stt-service:8000
- Route /api/tts → tts-service:8000
- Route /api/chat → llm-service:8000
- Route /api/jobs → jobs-service:8000

**Step 6.2: Gateway Features**
- Add rate limiting
- Add CORS configuration
- Add SSL/TLS (development)
- Add request logging
- Create Dockerfile

**Step 6.3: End-to-End Testing**
- Test all routes through gateway
- Load testing with Locust
- Performance optimization

### Phase 7: Web Application (Week 8-10)

**Step 7.1: Frontend Setup**
- Create Next.js project
- Set up Tailwind CSS
- Extract UI components from old/Ella-Ai
- Create API client library

**Step 7.2: Authentication Pages**
- Login page
- Register page
- OAuth integration
- Protected route handling

**Step 7.3: Feature Pages**
- Dashboard
- Chat interface with streaming
- Audio transcription page
- Study materials library
- Audio recording interface

**Step 7.4: Integration**
- Connect to API Gateway
- Test all features
- Responsive design testing
- Create Dockerfile

### Phase 8: Testing & Polish (Week 11-12)

**Step 8.1: Comprehensive Testing**
- Complete integration test suite
- End-to-end scenario tests
- Performance benchmarking
- Security audit

**Step 8.2: Documentation**
- API documentation (OpenAPI)
- Service READMEs
- Deployment guides
- User guides

**Step 8.3: Deployment Preparation**
- Build all Docker images
- Create deployment scripts
- Test on bigger server
- Smoke testing

task_progress Items:
- [ ] Step 1: Create folder structure
- [ ] Step 2: Set up database schemas and migrations
- [ ] Step 3: Create shared libraries
- [ ] Step 4: Implement Authentication service
- [ ] Step 5: Implement LLM Agent service
- [ ] Step 6: Implement Speech-to-Text service
- [ ] Step 7: Implement Text-to-Speech service
- [ ] Step 8: Implement Audio Recording service
- [ ] Step 9: Implement Async Jobs service and worker
- [ ] Step 10: Set up API Gateway
- [ ] Step 11: Develop Web Application
- [ ] Step 12: Integration testing
- [ ] Step 13: Performance testing and optimization
- [ ] Step 14: Documentation and deployment
- [ ] Step 15: Deploy to bigger server

---

## Revision History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2025-11-01 | Development Team | Initial comprehensive implementation plan |
