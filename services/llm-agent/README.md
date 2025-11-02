# LLM Agent Service

AI tutoring service with Retrieval Augmented Generation (RAG) capabilities for Little Monster platform.

## Overview

FastAPI-based LLM agent service combining POC 07 (LangChain agent) and POC 00 (RAG chatbot). Provides intelligent tutoring using Ollama LLM with ChromaDB for context retrieval.

## Features

✅ **Implemented**:
- AI chat with conversation history
- RAG-enhanced responses using ChromaDB
- Study material upload and indexing
- Conversation management
- Ollama integration (llama3.2:3b)
- ChromaDB vector search
- Health check endpoint

🚧 **Planned**:
- AWS Bedrock integration (cloud LLM fallback)
- Flashcard generation
- Quiz generation  
- Presentation generation
- Multi-user context isolation

## API Endpoints

### Chat

**POST /chat/message**
```json
{
  "conversation_id": 123,  // optional, creates new if not provided
  "message": "What is photosynthesis?",
  "use_rag": true
}
```
Response: AI response with optional sources

**GET /chat/conversations**  
List user's chat conversations

**POST /chat/materials**
```json
{
  "title": "Biology Chapter 3",
  "content": "Photosynthesis is the process...",
  "subject": "biology"
}
```
Upload study material for RAG indexing

### System

**GET /health**  
Health check with service status

**GET /docs**  
Interactive API documentation

## Local Development Setup

### Prerequisites

- Python 3.10+
- PostgreSQL running on localhost:5432
- Redis running on localhost:6379
- **Ollama running on localhost:11434** with llama3.2:3b model
- **ChromaDB running on localhost:8000**

### Installation

```bash
# Navigate to service directory
cd services/llm-agent

# Install shared library
pip install -e ../../shared/python-common

# Install service dependencies
pip install -r requirements.txt

# Real .env file is already configured
# Connects to your ACTUAL running Ollama and ChromaDB instances

# Run the service
python -m uvicorn src.main:app --reload --port 8005
```

Service will be available at: http://localhost:8005

### Testing with curl

```bash
# Upload study material
curl -X POST http://localhost:8005/chat/materials \
  -H "Content-Type: application/json" \
  -d '{"title":"Biology Notes","content":"Photosynthesis is the process by which plants convert light energy into chemical energy.","subject":"biology"}'

# Send chat message with RAG
curl -X POST http://localhost:8005/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"What is photosynthesis?","use_rag":true}'

# List conversations
curl http://localhost:8005/chat/conversations

# Health check
curl http://localhost:8005/health
```

## Infrastructure Dependencies

### Required Services (REAL, must be running)

✅ **Ollama** (localhost:11434):
- Model: llama3.2:3b
- Used for: LLM response generation
- Validated in POC 07 and POC 00

✅ **ChromaDB** (localhost:8000):
- Collection: "education"
- Used for: Vector similarity search
- Validated in POC 00

✅ **PostgreSQL** (localhost:5432):
- Database: littlemonster
- Tables: conversations, messages, study_materials

✅ **Redis** (localhost:6379):
- Used for: Caching, future rate limiting

## Environment Variables

All configuration in `.env` file (REAL working config):

### Required
- `DATABASE_URL` - PostgreSQL (configured)
- `REDIS_URL` - Redis (configured)
- `OLLAMA_URL` - Ollama API (configured: http://localhost:11434)
- `OLLAMA_MODEL` - Model name (configured: llama3.2:3b)
- `CHROMADB_HOST` - ChromaDB host (configured: localhost)
- `CHROMADB_PORT` - ChromaDB port (configured: 8000)

### Optional
- `USE_BEDROCK` - Enable AWS Bedrock (false)
- `AWS_REGION` - AWS region
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials

## How It Works

### RAG Flow

```
1. User sends question
2. Service queries ChromaDB for relevant study materials
3. Top 3 most relevant chunks retrieved
4. Context + question sent to Ollama
5. Ollama generates contextual response
6. Response stored in conversation history
7. Sources returned to user
```

### Chat Flow

```
1. User sends message
2. Get or create conversation
3. Store user message
4. Retrieve conversation history (last 5 messages)
5. If use_rag: Get relevant context from ChromaDB
6. Build prompt with context + history
7. Call Ollama for response
8. Store assistant message
9. Return response to user
```

## Database Schema

Uses tables from `database/schemas/004_content.sql` and `005_interactions.sql`:
- conversations
- messages
- study_materials

## Integration

### With Authentication Service
```python
# Future: Verify JWT token
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.post("http://localhost:8005/chat/message", 
                        headers=headers, 
                        json={"message": "Hello"})
```

### With Other Services
- Study materials can come from STT transcriptions
- Responses can be sent to TTS for audio output

## Monitoring

- Health check shows Ollama and ChromaDB connectivity
- Structured logging for all operations
- Request/response timing

## Migration from POCs

### From POC 00 (RAG Chatbot):
- ✅ ChromaDB integration
- ✅ Vector search
- ✅ Context retrieval
- ✅ Source tracking

### From POC 07 (LangChain Agent):
- ✅ Ollama LLM integration
- ✅ ReAct agent pattern (simplified for production)
- ✅ Tool orchestration (for future expansion)

## Performance

From POC testing:
- Ollama response time: 2-10 seconds (depends on prompt length)
- ChromaDB search: <100ms
- Total chat response: 3-15 seconds

## Port

- Local: 8005
- Container: 8000 (mapped to 8005)

## Status

🟢 **READY** - Service uses REAL Ollama and ChromaDB running on your machine
