# Backend Architecture - Agent + Chatbot Layers

## The Two Layers You Need

### Layer 1: Your Backend API (Always Required)
**Purpose**: Handle users, sessions, web/mobile app communication

```
┌─────────────────────────────────────┐
│  Your Backend API                    │
│  - User authentication              │
│  - Chat history management          │
│  - Session handling                 │
│  - WebSocket for real-time chat     │
│  - REST endpoints                   │
│  - Database operations              │
└─────────────────────────────────────┘
```

**This is your Express/FastAPI server** - handles HTTP requests from your web/mobile apps.

### Layer 2: Agent Orchestration (For Tool Calling)
**Purpose**: Decide when LLM should use tools vs. just chat

```
┌─────────────────────────────────────┐
│  Agent Layer (MCPHost)               │
│  - Receives user message            │
│  - Adds tool descriptions           │
│  - Calls Ollama                     │
│  - Parses tool calls                │
│  - Executes via MCP servers         │
│  - Returns result                   │
└─────────────────────────────────────┘
```

**MCPHost handles this** - you don't write orchestration code!

---

## Complete Architecture

```
┌──────────────────────────────────────────────┐
│  Web/Mobile App                               │
│  - Chat interface                             │
│  - Send messages via HTTP/WebSocket           │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  YOUR BACKEND API (Express/FastAPI)          │
│  - Handles HTTP requests                     │
│  - Manages user sessions                     │
│  - Stores chat history in PostgreSQL         │
│  - Routes to agent layer                     │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  AGENT LAYER (MCPHost)                       │
│  - Orchestrates LLM + tools                  │
│  - No code needed - MCPHost handles it       │
└──────────────────────────────────────────────┘
        ↓                    ↓
┌──────────────┐    ┌───────────────────────┐
│  Ollama LLM  │    │  MCP Servers          │
│  (Planning)  │    │  - RAG search         │
└──────────────┘    │  - Presenton          │
                    │  - Flashcards         │
                    │  - Quiz gen           │
                    └───────────────────────┘
                            ↓
                    ┌───────────────────────┐
                    │  Actual Services      │
                    │  - ChromaDB           │
                    │  - Presenton API      │
                    │  - Your generators    │
                    └───────────────────────┘
```

---

## Your Backend API Structure

```python
# main.py - Your Backend
from fastapi import FastAPI, WebSocket
from mcphost_client import MCPHostClient  # Library to talk to MCPHost

app = FastAPI()
mcphost = MCPHostClient("http://localhost:8080")  # MCPHost runs separately

@app.post("/api/chat")
async def chat(message: str, user_id: str, session_id: str):
    # 1. Get chat history from database
    history = get_chat_history(session_id)
    
    # 2. Send to MCPHost (which handles agent orchestration)
    response = await mcphost.chat(
        message=message,
        history=history,
        user_context={"user_id": user_id}
    )
    
    # 3. Save to database
    save_chat_message(session_id, message, response)
    
    # 4. Return to user
    return response

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    # Real-time chat for streaming responses
    await websocket.accept()
    
    async for message in websocket.iter_text():
        # Stream response from MCPHost
        async for chunk in mcphost.chat_stream(message):
            await websocket.send_text(chunk)

# Other endpoints for user management, etc.
@app.post("/api/auth/login")
@app.post("/api/auth/register")
@app.get("/api/history/{session_id}")
# ... etc
```

**Your backend is simple** - just routes to MCPHost and manages users/sessions.

---

## What MCPHost Does (The Agent)

When your backend sends a message to MCPHost:

```python
# Your backend calls:
response = mcphost.chat("Make a presentation from this lecture")
```

**MCPHost internally**:
1. Adds tool descriptions to prompt
2. Sends to Ollama
3. LLM responds with tool call
4. MCPHost executes tool via MCP server
5. Returns result

**You don't write this logic!** MCPHost is the agent framework.

---

## MCP Servers You Need

### 1. RAG Search MCP Server
```python
# Wraps your ChromaDB search
@mcp_tool
def search_content(query: str):
    return chromadb_search(query)
```

### 2. Presenton MCP Server
```javascript
// Wraps Presenton API
@mcp_tool
async function create_presentation(topic, content, slides) {
    return await presenton_api.create(...);
}
```

### 3. Flashcard MCP Server
```python
# Wraps your flashcard generator
@mcp_tool
def generate_flashcards(topic: str, context: str):
    return flashcard_generator.generate(...)
```

**These are simple wrappers** - just expose your existing code as MCP tools.

---

## Comparison: With vs Without Agent

### Simple Chatbot (No Agent)
```python
# Your backend directly calls LLM
@app.post("/chat")
def chat(message: str):
    return ollama.generate(message)
```

**Use for**: Basic Q&A, no tool calling needed

### Agentic Chatbot (With MCPHost)
```python
# Your backend calls MCPHost
@app.post("/chat")
def chat(message: str):
    return mcphost.chat(message)  # MCPHost handles tools
```

**Use for**: Complex requests that need multiple tools

---

## Your Use Case

**User**: "Take that lecture on photosynthesis and make a presentation focused on test topics"

### Without Agent (Manual Logic)
```python
# YOU write this orchestration:
content = chromadb.search("photosynthesis")
slides = presenton.create(content, focus="test topics")
return slides
```

### With Agent (MCPHost)
```python
# MCPHost figures this out automatically:
result = mcphost.chat(user_message)
# LLM decides: search_content → create_presentation
# MCPHost executes both
return result
```

**MCPHost is MUCH easier** - no orchestration code needed!

---

## Bottom Line

**For your chatbot**:
1. ✅ **Your Backend API** - Handles users, sessions, HTTP (you build this)
2. ✅ **MCPHost** - Orchestrates tools (open source, just configure)
3. ✅ **MCP Servers** - Simple wrappers for your APIs (you build these)

**Agent embedded?** YES - in MCPHost!

**Do you code it?** NO - MCPHost is the agent, you just:
- Build your backend API
- Create MCP tool wrappers
- Configure MCPHost

---

**Status**: Architecture clear - 3 layers (Backend, MCPHost, MCP Servers)
