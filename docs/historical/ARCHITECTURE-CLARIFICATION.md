**Last Updated:** November 4, 2025
> **ARCHIVAL NOTICE**: This document has been archived for historical reference. For current system information, see docs/TECHNICAL-ARCHITECTURE.md and docs/project-status.md.

# Architecture Clarification - You DO Have an API Gateway!

## Your Concern

> "The UI is directly calling each server without a middleware API layer?"

## The Reality: You Have Proper Gateway Architecture! ✅

### Current Architecture (It's Correct!)

```
┌─────────────────────────────────────────────────────────────┐
│  USER'S BROWSER                                              │
│  ┌──────────────┐                                           │
│  │  Frontend    │                                           │
│  │  (Next.js)   │                                           │
│  │  Port 3001   │                                           │
│  └──────┬───────┘                                           │
│         │                                                     │
│         │ ALL requests go to ONE place:                      │
│         │ http://localhost:80                                │
│         │                                                     │
└─────────┼─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│  YOUR COMPUTER (Docker Network)                              │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API GATEWAY (Nginx) - Port 80                         │ │
│  │  ├─ /api/auth      → Auth Service (8001)               │ │
│  │  ├─ /api/chat      → LLM Service (8005)                │ │
│  │  ├─ /api/transcribe → STT Service (8002)               │ │
│  │  ├─ /api/tts       → TTS Service (8003)                │ │
│  │  └─ /api/*         → Other Services                     │ │
│  └──────────────┬─────────────────────────────────────────┘ │
│                 │                                             │
│                 │ Internal Docker Network                     │
│                 │ (Frontend NEVER sees these)                 │
│                 ▼                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MICROSERVICES (Internal Only)                        │  │
│  │  ├─ Authentication (8001)                             │  │
│  │  ├─ LLM Agent (8005)                                  │  │
│  │  ├─ Speech-to-Text (8002)                             │  │
│  │  ├─ Text-to-Speech (8003)                             │  │
│  │  ├─ Audio Recording (8004)                            │  │
│  │  ├─ Class Management (8006)                           │  │
│  │  ├─ Content Capture (8008)                            │  │
│  │  └─ + 6 more services...                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Proof from Your Code

### 1. Frontend ONLY Calls Gateway

**File: views/web-app/src/lib/api.ts**
```typescript
const API_URL = 'http://localhost';  // Port 80 = nginx gateway

// ALL API calls use this:
export const auth = {
  login: (email, password) => 
    api.post('/api/auth/login', ...)  // → Gateway port 80
};

export const chat = {
  sendMessage: (message) =>
    api.post('/api/chat/message', ...) // → Gateway port 80
};

export const transcription = {
  upload: (file) =>
    api.post('/api/transcribe/', ...) // → Gateway port 80
};
```

**Notice:** EVERY call goes to `localhost:80` (the gateway). The frontend has NO IDEA individual services exist!

### 2. Gateway Routes Internally

**File: services/api-gateway/nginx.conf**
```nginx
# Gateway listens on port 80
server {
    listen 80;
    
    # Routes /api/auth to auth service
    location /api/auth/ {
        proxy_pass http://lm-auth:8000;  # Internal routing
    }
    
    # Routes /api/chat to LLM service
    location /api/chat/ {
        proxy_pass http://lm-llm:8000;  # Internal routing
    }
    
    # And so on for all services...
}
```

## Why This is PERFECT Architecture

✅ **Single Point of Entry:** Frontend only knows about port 80
✅ **Gateway Handles Routing:** Nginx routes to appropriate service
✅ **Services are Hidden:** Frontend can't access services directly
✅ **Easy to Add CORS:** Gateway handles it (already configured)
✅ **Easy to Add Auth:** Gateway can check JWT tokens
✅ **Easy to Add Rate Limiting:** Do it at gateway level
✅ **Easy to Scale:** Add/remove services without frontend changes

## Comparison

### ❌ BAD Architecture (What You Thought You Had)
```
Frontend → Service 1 (Port 8001)
Frontend → Service 2 (Port 8005)
Frontend → Service 3 (Port 8002)
...
```

### ✅ GOOD Architecture (What You Actually Have!)
```
Frontend → API Gateway (Port 80)
              ↓
              ├→ Service 1
              ├→ Service 2
              └→ Service 3
```

## For Going "Full Local"

Your setup is ALREADY perfect for running fully local:

1. **All services in Docker** ✅
2. **Single gateway port (80)** ✅
3. **Internal Docker network** ✅
4. **Frontend on port 3001** ✅
5. **Everything stays on your machine** ✅

**What you have is textbook microservices with API gateway pattern!**

## The Only Port You Need to Expose (If Going to Internet)

Since you have proper gateway architecture:

- **Expose:** Port 80 (gateway only)
- **Don't expose:** 8001, 8002, 8005, etc. (they're internal!)
- **Result:** Single entry point, proper security

Your architecture is actually excellent and follows industry best practices!
