# Little Monster - Deployment Guide

## Complete Deployment Instructions

---

## Prerequisites

### Infrastructure Required
- PostgreSQL 13+ (localhost:5432)
- Redis 6+ (localhost:6379)
- Ollama with llama3.2:3b model (localhost:11434)
- ChromaDB (localhost:8000)
- Python 3.10+
- Node.js 18+

### Verify Prerequisites
```bash
# PostgreSQL
python -c "import psycopg2; psycopg2.connect('postgresql://postgres:postgres@localhost:5432/postgres')" && echo "PostgreSQL OK"

# Redis
python -c "import redis; redis.Redis('localhost', 6379).ping()" && echo "Redis OK"

# Ollama
curl http://localhost:11434/api/tags && echo "Ollama OK"

# ChromaDB  
curl http://localhost:8000/api/v1/heartbeat && echo "ChromaDB OK"
```

---

## Step 1: Deploy Database

```bash
cd database/scripts
python deploy-schema.py
```

**Expected Output:**
```
[OK] Database 'littlemonster' created
[OK] Schema deployed successfully
[OK] Tables created: 12
[SUCCESS] Database ready!
```

---

## Step 2: Install Shared Library

```bash
cd shared/python-common
pip install -e .
```

**Verify:**
```bash
python -c "from lm_common.auth import jwt_utils; print('lm-common OK')"
```

---

## Step 3: Deploy Backend Services

### 3.1 Authentication Service (Port 8001)
```bash
cd services/authentication
pip install -r requirements.txt
python test_service.py  # Verify imports
python -m uvicorn src.main:app --reload --port 8001
```

**Test:**
```bash
curl http://localhost:8001/health
curl http://localhost:8001/docs  # OpenAPI docs
```

### 3.2 LLM Agent Service (Port 8005)
```bash
cd services/llm-agent
pip install -r requirements.txt
python test_service.py  # Verify imports
python -m uvicorn src.main:app --reload --port 8005
```

### 3.3 Speech-to-Text Service (Port 8002)
```bash
cd services/speech-to-text
pip install -r requirements.txt
python test_service.py  # Verify imports
python -m uvicorn src.main:app --reload --port 8002
```

### 3.4 Text-to-Speech Service (Port 8003)
```bash
cd services/text-to-speech
pip install -r requirements.txt
python test_service.py  # Verify imports
python -m uvicorn src.main:app --reload --port 8003
```

### 3.5 Audio Recording Service (Port 8004)
```bash
cd services/audio-recording
pip install -r requirements.txt
python -m uvicorn src.main:app --reload --port 8004
```

### 3.6 Async Jobs Worker
```bash
cd services/async-jobs
pip install -r requirements.txt
python src/worker.py
```

---

## Step 4: Deploy Frontend

```bash
cd views/web-app
npm install  # Already done if 86 TS errors fixed
npm run dev
```

**Access:** http://localhost:3000

---

## Step 5: Deploy API Gateway (Optional)

```bash
# Install nginx if not installed
# Copy config
nginx -c $(pwd)/services/api-gateway/nginx.conf -t  # Test config
nginx -c $(pwd)/services/api-gateway/nginx.conf     # Start
```

**Access:** http://localhost (routes to all services)

---

## Verification Tests

### Health Checks
```bash
curl http://localhost:8001/health  # Auth
curl http://localhost:8005/health  # LLM
curl http://localhost:8002/health  # STT
curl http://localhost:8003/health  # TTS
curl http://localhost:8004/health  # Recording
```

### Integration Test
```bash
cd tests/integration
python test_auth_flow.py
```

### Performance Test
```bash
pip install locust
locust -f tests/performance/locustfile.py
# Open http://localhost:8089
# Run with 1000 users, spawn rate 100
```

---

## Production Deployment (Docker)

### Build All Images
```bash
cd services/authentication && docker build -t lm-auth:1.0 .
cd services/llm-agent && docker build -t lm-llm:1.0 .
cd services/speech-to-text && docker build -t lm-stt:1.0 .
cd services/text-to-speech && docker build -t lm-tts:1.0 .
cd services/audio-recording && docker build -t lm-recording:1.0 .
cd services/async-jobs && docker build -t lm-jobs:1.0 .
cd views/web-app && docker build -t lm-web:1.0 .
```

### Run with Docker Compose (Future)
```bash
docker-compose up -d
```

---

## Environment Variables

All services use .env files with REAL credentials:
- Root `.env` - master configuration
- Each service has its own `.env`
- Web app has `.env.local`

**Security:** .env files are in .gitignore - do not commit!

---

## Monitoring

### Logs
Each service outputs structured JSON logs in production:
```bash
# View logs
docker logs lm-auth
docker logs lm-llm
# etc
```

### Metrics
- Health endpoints on each service
- Response time tracking
- Error rate monitoring
- Future: Prometheus integration

---

## Troubleshooting

### Service Won't Start
1. Check .env file exists
2. Verify database connection
3. Check port not already in use
4. Review service logs

### Database Connection Error
```bash
cd database/scripts
python deploy-schema.py  # Re-deploy
```

### Dependency Issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### TypeScript Errors
```bash
cd views/web-app
rm -rf node_modules package-lock.json
npm install
```

---

## Production Checklist

Before deploying to production:

- [ ] Change DEBUG=false in all .env files
- [ ] Update CORS origins (remove *)
- [ ] Enable HTTPS (nginx SSL)
- [ ] Configure rate limiting
- [ ] Set up monitoring/alerts
- [ ] Configure backups
- [ ] Load test with Locust
- [ ] Security audit
- [ ] Documentation review

---

## Performance Targets

From PROJECT-CHARTER.md:
- API response time: <500ms (p95)
- Login time: <200ms
- TTS generation: <1s
- STT transcription: <30s for 5min audio
- Concurrent users: 1000+

---

## Support

- Quick Start: QUICK-START.md
- Testing Results: TESTING-RESULTS.md
- Implementation Status: IMPLEMENTATION-STATUS.md
- Service READMEs: services/*/README.md

All services use validated POC code - refer to poc/ directory for reference implementations.
