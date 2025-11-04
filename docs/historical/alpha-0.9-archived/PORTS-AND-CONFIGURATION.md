# Ports and Configuration Reference
## Alpha 0.9 - Complete Service Configuration

**Version:** 0.9.0-alpha  
**Date:** November 2, 2025  

---

## Table of Contents
1. [Port Allocation Reference](#port-allocation-reference)
2. [Environment Variables](#environment-variables)
3. [Database Configuration](#database-configuration)
4. [Service Configuration](#service-configuration)
5. [Network Configuration](#network-configuration)

---

## Port Allocation Reference

### Complete Port Map

```
PORT ALLOCATION MATRIX
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

### Port Conflict Resolution

```
Port Assignment Rules:

1. Infrastructure Layer (< 8000):
   - Standard ports for databases and caches
   - 5432: PostgreSQL (industry standard)
   - 6379: Redis (industry standard)
   - 8000: ChromaDB (vendor default)
   - 8080: Adminer (common alternative to 80)

2. Application Layer (8001-8013):
   - Consistent incremental assignment
   - Easy to remember and document
   - Avoids conflicts with common services

3. Special Ports:
   - 80: Gateway (HTTP standard)
   - 3000: Next.js (framework default)
   - 5000: Presenton (vendor default)
   - 11434: Ollama (vendor default)

4. Reserved/Avoided:
   - 443: HTTPS (future use)
   - 3306: MySQL (not used)
   - 5000-5100: Commonly used
   - 27017: MongoDB (not used)
   - 9000-9200: Elasticsearch range

Conflict Check Command:
netstat -ano | findstr ":<PORT>"
```

---

## Environment Variables

### Required Environment Variables

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
# OCR Configuration
# ---------------------------------
OCR_PROVIDER=tesseract  # Options: tesseract, google-vision
TESSERACT_LANG=eng

# ---------------------------------
# External APIs
# ---------------------------------
# Pexels (for Presenton)
PEXELS_API_KEY=<your-pexels-key>

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

### Environment-Specific Configurations

```
┌──────────────────────────────────────────────────────────┐
│              ENVIRONMENT CONFIGURATIONS                   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Development (.env.development):                         │
│  ├─ LLM_PROVIDER=ollama                                 │
│  ├─ LOG_LEVEL=DEBUG                                      │
│  ├─ ENABLE_HOT_RELOAD=true                              │
│  ├─ DISABLE_AUTH=false                                   │
│  └─ USE_LOCAL_STORAGE=true                              │
│                                                           │
│  Testing (.env.test):                                    │
│  ├─ DATABASE_URL=postgresql://test:test@localhost/test  │
│  ├─ REDIS_URL=redis://localhost:6380/1                  │
│  ├─ LLM_PROVIDER=mock                                    │
│  ├─ DISABLE_EXTERNAL_APIS=true                          │
│  └─ LOG_LEVEL=WARNING                                    │
│                                                           │
│  Production (.env.production):                           │
│  ├─ LLM_PROVIDER=bedrock                                │
│  ├─ DATABASE_URL=${RDS_CONNECTION_STRING}               │
│  ├─ REDIS_URL=${ELASTICACHE_ENDPOINT}                   │
│  ├─ LOG_LEVEL=INFO                                       │
│  ├─ ENABLE_METRICS=true                                  │
│  └─ SECURE_COOKIES=true                                  │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## Database Configuration

### PostgreSQL Configuration

```ini
# postgresql.conf (Production Recommendations)

# Connections
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB
min_wal_size = 1GB
max_wal_size = 4GB

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_line_prefix = '%m [%p] %q%u@%d '
log_timezone = 'UTC'

# Performance
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
track_io_timing = on
track_functions = all

# Replication (for production)
wal_level = replica
max_wal_senders = 10
wal_keep_size = 1GB
```

### Redis Configuration

```ini
# redis.conf (Production Recommendations)

# Network
bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300

# Persistence
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Memory Management
maxmemory 512mb
maxmemory-policy allkeys-lru
maxmemory-samples 5

# Performance
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes

# Logging
loglevel notice
logfile ""
```

---

## Service Configuration

### Service Configuration Matrix

```
┌──────────────────┬──────────┬───────────┬──────────┬──────────────┬──────────┐
│ Service          │Framework │ Language  │ Port(Ext)│ Dependencies │ Workers  │
├──────────────────┼──────────┼───────────┼──────────┼──────────────┼──────────┤
│ Authentication   │ FastAPI  │ Python3.11│   8001   │ PG, Redis    │    2     │
│ LLM Agent        │ FastAPI  │ Python3.11│   8005   │ PG,Redis,    │    2     │
│                  │          │           │          │ ChromaDB,    │          │
│                  │          │           │          │ Ollama       │          │
│ Speech-to-Text   │ FastAPI  │ Python3.11│   8002   │ PG, Redis    │    1     │
│ Text-to-Speech   │ FastAPI  │ Python3.11│   8003   │ PG           │    1     │
│ Audio Recording  │ FastAPI  │ Python3.11│   8004   │ PG           │    1     │
│ Class Management │ FastAPI  │ Python3.11│   8006   │ PG           │    2     │
│ Content Capture  │ FastAPI  │ Python3.11│   8008   │ PG,Redis,    │    2     │
│                  │          │           │          │ ChromaDB     │          │
│ AI Study Tools   │ FastAPI  │ Python3.11│   8009   │ PG, LLM      │    2     │
│ Social Collab    │ FastAPI  │ Python3.11│   8010   │ PG           │    2     │
│ Gamification     │ FastAPI  │ Python3.11│   8011   │ PG           │    1     │
│ Study Analytics  │ FastAPI  │ Python3.11│   8012   │ PG           │    1     │
│ Notifications    │ FastAPI  │ Python3.11│   8013   │ PG, Redis    │    2     │
│ API Gateway      │ Nginx    │ C         │    80    │ All Services │    4     │
│ Async Jobs       │ Custom   │ Python3.11│   N/A    │ Redis, PG    │    4     │
└──────────────────┴──────────┴───────────┴──────────┴──────────────┴──────────┘

Worker Count:
- Development: 1-2 workers per service
- Production: Scale based on load (2-8 workers)
- Async jobs: 4-8 dedicated worker processes
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

## Environment Variables

### Per-Service Environment Configuration

#### Authentication Service

```bash
# Authentication Service Environment Variables

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_MAX_CONNECTIONS=50

# JWT Settings
JWT_SECRET_KEY=${JWT_SECRET_KEY}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
REFRESH_TOKEN_EXPIRATION_DAYS=30

# Password Security
BCRYPT_ROUNDS=12
MIN_PASSWORD_LENGTH=8
REQUIRE_SPECIAL_CHARS=false

# Session Management
SESSION_TIMEOUT_HOURS=24
MAX_SESSIONS_PER_USER=5
ENABLE_SESSION_REFRESH=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
LOGIN_ATTEMPTS_LIMIT=5
LOGIN_LOCKOUT_MINUTES=15

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
SERVICE_NAME=authentication
SERVICE_VERSION=1.0.0
```

#### LLM Agent Service

```bash
# LLM Agent Service Environment Variables

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster

# Cache
REDIS_URL=redis://redis:6379/0

# LLM Provider (Dev)
LLM_PROVIDER=ollama
OLLAMA_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TIMEOUT=300

# LLM Provider (Production)
LLM_PROVIDER=bedrock
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
BEDROCK_MODEL=anthropic.claude-3-sonnet-20240229-v1:0
BEDROCK_MAX_TOKENS=4096
BEDROCK_TEMPERATURE=0.7

# Vector Database
CHROMADB_HOST=chromadb
CHROMADB_PORT=8000
CHROMA_COLLECTION_NAME=lm_content
VECTOR_DIMENSION=768

# RAG Configuration
RAG_ENABLED=true
RAG_TOP_K=5
RAG_SIMILARITY_THRESHOLD=0.7
RAG_CONTEXT_LENGTH=2000

# Performance
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=300
RESPONSE_STREAMING=true

# Logging
LOG_LEVEL=INFO
SERVICE_NAME=llm-agent
```

#### Speech-to-Text Service

```bash
# Speech-to-Text Service Environment Variables

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster

# Redis (for job queue)
REDIS_URL=redis://redis:6379/0
JOB_QUEUE_NAME=transcription_jobs
JOB_TIMEOUT=600

# Whisper Configuration
WHISPER_MODEL=base  # Options: tiny, base, small, medium, large
WHISPER_DEVICE=cpu  # Options: cpu, cuda
WHISPER_LANGUAGE=en
WHISPER_TASK=transcribe  # Options: transcribe, translate

# File Handling
MAX_AUDIO_SIZE_MB=50
SUPPORTED_FORMATS=mp3,wav,m4a,ogg,flac
TEMP_DIR=/tmp/audio
CLEANUP_AFTER_HOURS=24

# Processing
CHUNK_LENGTH_SECONDS=300
ENABLE_VAD=true  # Voice Activity Detection
ENABLE_DIARIZATION=false  # Speaker separation

# Performance
MAX_PARALLEL_JOBS=3
WORKER_TIMEOUT=600

# Logging
LOG_LEVEL=INFO
SERVICE_NAME=speech-to-text
```

#### Text-to-Speech Service

```bash
# Text-to-Speech Service Environment Variables

# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/littlemonster

# Azure Speech Configuration
AZURE_SPEECH_KEY=${AZURE_SPEECH_KEY}
AZURE_SPEECH_REGION=eastus
AZURE_VOICE_NAME=en-US-JennyNeural
AZURE_SPEAKING_RATE=1.0
AZURE_PITCH=0

# Coqui TTS (Alternative)
ENABLE_COQUI=false
COQUI_MODEL=tts_models/en/ljspeech/tacotron2-DDC
COQUI_VOCODER=vocoder_models/en/ljspeech/hifigan_v2

# Output Configuration
OUTPUT_FORMAT=mp3  # Options: mp3, wav, ogg
SAMPLE_RATE=24000
BITRATE=128k

# Limits
MAX_TEXT_LENGTH=5000
MAX_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=INFO
SERVICE_NAME=text-to-speech
```

---

## Database Configuration

### Connection Pool Settings

```python
# Database Connection Pool Configuration

# SQLAlchemy Pool Settings
DATABASE_POOL_CONFIG = {
    "pool_size": 10,              # Normal connection pool size
    "max_overflow": 20,            # Additional connections under load
    "pool_timeout": 30,            # Seconds to wait for connection
    "pool_recycle": 3600,          # Recycle connections every hour
    "pool_pre_ping": True,         # Verify connections before use
    "echo": False,                 # SQL logging (dev: True)
    "echo_pool": False,            # Pool logging (dev: True)
}

# Connection String Format
DATABASE_URL = "postgresql+asyncpg://user:pass@host:port/dbname"

# For async operations:
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_POOL_CONFIG
)
```

### Database Initialization

```sql
-- Database initialization script
-- Run via docker-entrypoint-initdb.d/schema.sql

-- Create database (if not exists)
CREATE DATABASE IF NOT EXISTS littlemonster;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- For encryption

-- Create roles
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'lm_app') THEN
        CREATE ROLE lm_app LOGIN PASSWORD 'secure_password';
    END IF;
END
$$;

-- Grant permissions
GRANT CONNECT ON DATABASE littlemonster TO lm_app;
GRANT USAGE ON SCHEMA public TO lm_app;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lm_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lm_app;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL ON TABLES TO lm_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT ALL ON SEQUENCES TO lm_app;
```

---

## Service Configuration

### FastAPI Service Template

```python
# config.py - Standard Configuration Template

import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Service configuration from environment variables"""
    
    # Service Identity
    SERVICE_NAME: str = "service-name"
    SERVICE_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development, testing, production
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int = 2
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False
    
    # Redis (if needed)
    REDIS_URL: Optional[str] = None
    REDIS_MAX_CONNECTIONS: int = 50
    
    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Performance
    REQUEST_TIMEOUT: int = 30
    MAX_REQUEST_SIZE: int = 10485760  # 10MB
    
    # Feature Flags
    ENABLE_METRICS: bool = False
    ENABLE_TRACING: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Usage
settings = Settings()
```

### Nginx Configuration Breakdown

```nginx
# Complete nginx.conf with annotations

events {
    worker_connections 1024;  # Max concurrent connections per worker
    use epoll;                # Linux-optimized event model
}

http {
    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 50M;  # Must match service limits
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript 
               application/xml+rss application/rss+xml;
    
    # Logging
    log_format json_combined escape=json
        '{'
        '"time":"$time_iso8601",'
        '"request_id":"$request_id",'
        '"remote_addr":"$remote_addr",'
        '"request":"$request",'
        '"status":$status,'
        '"body_bytes_sent":$body_bytes_sent,'
        '"request_time":$request_time,'
        '"upstream_addr":"$upstream_addr",'
        '"upstream_status":"$upstream_status",'
        '"upstream_response_time":"$upstream_response_time"'
        '}';
    
    access_log /var/log/nginx/access.log json_combined;
    error_log /var/log/nginx/error.log warn;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=20r/m;
    
    # Upstream definitions
    upstream auth_service {
        server lm-auth:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }
    
    # ... (other upstreams)
    
    # Main server
    server {
        listen 80;
        server_name _;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        
        # CORS
        add_header Access-Control-Allow-Origin "*" always;
        add_header Access-Control-Allow-Methods "GET,POST,PUT,DELETE,OPTIONS" always;
        add_header Access-Control-Allow-Headers "Authorization,Content-Type" always;
        add_header Access-Control-Max-Age "3600" always;
        
        # OPTIONS handling
        if ($request_method = OPTIONS) {
            return 204;
        }
        
        # Authentication routes (stricter rate limit)
        location /api/auth/ {
            limit_req zone=auth_limit burst=5 nodelay;
            proxy_pass http://auth_service/auth/;
            include /etc/nginx/proxy_params;
        }
        
        # General API routes
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://appropriate_upstream/;
            include /etc/nginx/proxy_params;
        }
        
        # Health check (no auth required)
        location /health {
            access_log off;
            return 200 '{"status":"healthy"}';
            add_header Content-Type application/json;
        }
    }
}
```

---

## Network Configuration

### Docker Network Details

```yaml
# docker-compose.yml network configuration

networks:
  lm-network:
    name: lm-network
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
    driver_opts:
      com.docker.network.bridge.name: lm-bridge
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
```

### Network Security Rules

```
Firewall Rules (Production):

Inbound:
├─ Port 80    → Allow from 0.0.0.0/0 (HTTP)
├─ Port 443   → Allow from 0.0.0.0/0 (HTTPS)
├─ Port 22    → Allow from Admin IPs only (SSH)
└─ All Other  → Deny

Outbound:
├─ Port 443   → Allow (HTTPS to external APIs)
├─ Port 80    → Allow (HTTP to package repos)
└─ All Other  → Allow from VPC internal

Service-to-Service (Internal):
├─ All ports within VPC → Allow
└─ Docker network isolation → Enforce

Database Security Groups:
├─ PostgreSQL 5432 → Allow from app tier only
├─ Redis 6379      → Allow from app tier only
└─ No public access → Enforced
```

### DNS Configuration

```
Internal DNS Resolution (Docker):

Service Discovery:
├─ lm-auth          → 172.20.0.10
├─ lm-llm           → 172.20.0.11
├─ lm-stt           → 172.20.0.12
├─ lm-tts           → 172.20.0.13
├─ lm-recording     → 172.20.0.14
├─ lm-class-mgmt    → 172.20.0.15
├─ lm-content-capture → 172.20.0.16
├─ lm-ai-study-tools → 172.20.0.17
├─ lm-social-collab  → 172.20.0.18
├─ lm-gamification   → 172.20.0.19
├─ lm-study-analytics → 172.20.0.20
├─ lm-notifications  → 172.20.0.21
├─ postgres          → 172.20.0.30
├─ redis             → 172.20.0.31
├─ chromadb          → 172.20.0.32
└─ ollama            → 172.20.0.33

DNS Resolution:
- Automatic via Docker DNS (127.0.0.11)
- No /etc/hosts modification needed
- Use service names, not IPs
- Load balancing handled by Docker
```

---

## Configuration Management

### Configuration Hierarchy

```
Configuration Priority (High to Low):

1. Command-line Arguments
   └─ docker run -e KEY=value

2. Environment Variables
   └─ export KEY=value
   └─ .env file

3. Configuration File
   └─ config.yaml
   └─ settings.json

4. Default Values
   └─ Hardcoded in application

Example:
PORT environment variable overrides config file
```

### Secrets Management

```
Secrets Hierarchy:

Development:
├─ .env files (git-ignored)
└─ Local environment variables

Testing:
├─ .env.test
└─ Mock/fake credentials

Production:
├─ AWS Secrets Manager
├─ Environment variables (ECS/K8s)
└─ Never in code or version control

Secret Rotation:
├─ JWT_SECRET_KEY: Rotate
