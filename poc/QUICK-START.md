# Quick Start Guide - Immediate POC Testing
## Test Your Infrastructure NOW!

**Goal**: Validate all existing services in 30 minutes

---

## 🚀 Fastest Path: Test What's Already Running

You have 7 Docker containers running. Let's test each one:

---

## Test 1: Ollama LLM (2 minutes)

### Basic Test
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gpt-oss:20b",
  "prompt": "Explain photosynthesis in one sentence.",
  "stream": false
}'
```

**Expected**: JSON response with generated text about photosynthesis

### Alternative Test (Chat Format)
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss:20b",
  "messages": [
    {"role": "user", "content": "What is 2+2?"}
  ],
  "stream": false
}'
```

**Success Criteria**: ✅ Returns coherent text response

---

## Test 2: ChromaDB (1 minute)

### Heartbeat Test
```bash
curl http://localhost:8000/api/v1/heartbeat
```

**Expected**: Status 200 with timestamp

### List Collections
```bash
curl http://localhost:8000/api/v1/collections
```

**Expected**: JSON array (may be empty if no collections yet)

**Success Criteria**: ✅ ChromaDB responds to API calls

---

## Test 3: PostgreSQL (2 minutes)

### Version Check
```bash
docker exec lm-postgres psql -U postgres -d lm_dev -c "SELECT version();"
```

**Expected**: PostgreSQL 15.x version info

### List Tables
```bash
docker exec lm-postgres psql -U postgres -d lm_dev -c "\dt"
```

**Expected**: List of tables (may be empty)

### Test Query
```bash
docker exec lm-postgres psql -U postgres -d lm_dev -c "SELECT NOW();"
```

**Expected**: Current timestamp

**Success Criteria**: ✅ PostgreSQL accepts queries

---

## Test 4: Redis (1 minute)

### Ping Test
```bash
docker exec lm-redis redis-cli ping
```

**Expected**: `PONG`

### Set/Get Test
```bash
docker exec lm-redis redis-cli SET test_key "hello"
docker exec lm-redis redis-cli GET test_key
```

**Expected**: `OK` then `"hello"`

**Success Criteria**: ✅ Redis stores and retrieves data

---

## Test 5: Qdrant (1 minute)

### Health Check
```bash
curl http://localhost:6333/
```

**Expected**: JSON with version info

### List Collections
```bash
curl http://localhost:6333/collections
```

**Expected**: JSON with collections (may be empty)

**Success Criteria**: ✅ Qdrant API responds

---

## Test 6: Adminer Database UI (30 seconds)

### Open in Browser
```
http://localhost:8080
```

**Login Details**:
- System: `PostgreSQL`
- Server: `postgres`
- Username: `postgres`
- Password: `postgres`
- Database: `lm_dev`

**Success Criteria**: ✅ Can view database through web UI

---

## Test 7: Presenton (30 seconds)

### Open in Browser
```
http://localhost:5000
```

**Expected**: Presenton UI for creating presentations

**Success Criteria**: ✅ Application loads

---

## Test Results Checklist

After running all tests, check:

- [ ] Ollama responds with text generation
- [ ] ChromaDB API is accessible
- [ ] PostgreSQL accepts queries
- [ ] Redis stores/retrieves data
- [ ] Qdrant API responds
- [ ] Adminer UI loads and connects
- [ ] Presenton UI loads

If all checked ✅, proceed to **POC 1: LLM Testing**

---

## Troubleshooting

### If Ollama Doesn't Respond
```bash
# Check if running
docker ps | grep ollama

# View logs
docker logs lm-ollama --tail 50

# Restart if needed
docker restart lm-ollama
```

### If PostgreSQL Connection Fails
```bash
# Check if running
docker ps | grep postgres

# View logs
docker logs lm-postgres --tail 50
```

### If Any Service Is Down
```bash
# View all container status
docker ps -a

# Start all services
cd old/Ella-Ai
docker-compose up -d

# Check logs for errors
docker-compose logs
```

---

## Next Steps After Validation

Once all tests pass:

1. **Go to POC 1** - Start with `poc/01-llm-ollama/README.md`
2. **Run comprehensive LLM tests** - Response quality, streaming, etc.
3. **Move to POC 3** - Test vector database operations
4. **Then POC 5** - Test database CRUD operations

---

## Performance Baseline

While testing, note:
- Ollama response time
- ChromaDB query speed  
- PostgreSQL query speed
- System resource usage (CPU/RAM)

These baselines help evaluate performance later.

---

**Time to Complete**: ~10-15 minutes  
**Next Document**: `poc/01-llm-ollama/README.md`
