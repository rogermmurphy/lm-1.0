# Presenton Manual Configuration Guide

**Since you're setting it up through the UI, here's what to enter:**

---

## Configuration Values

### LLM Settings (Ollama)
**Provider**: Ollama  
**Ollama URL**: `http://ollama:11434`  
**Model Name**: `llama3.2:3b`  
*(Use the exact full name with version)*

### Image Settings (Pexels)
**Image Provider**: Pexels  
**Pexels API Key**: `mcqPLzfW53QOcGe6H2wD2JDhLtfNbVclS0wX4Zk3OGrM6Op9XftrhxK3`

---

## Available Ollama Models

You have 2 models downloaded:

| Model | Size | Status | Use This? |
|-------|------|--------|-----------|
| `llama3.2:3b` | 2.0 GB | ✅ Works | **YES - Use this** |
| `gpt-oss:20b` | 13 GB | ❌ Too big for RAM | NO |

**Important**: Use exact name `llama3.2:3b` (include the `:3b` part)

---

## Ollama Version Info

**Ollama Server**: v0.12.7  
**Container**: lm-ollama  
**API Endpoint**: http://localhost:11434 (or http://ollama:11434 from inside Docker)

---

## If Presenton Asks for GPT-OSS API Key

**What's happening**: Presenton thinks you want to use external API  
**Solution**: Select "Ollama" as provider, NOT "GPT-OSS" or "OpenAI"

**In the UI**:
1. LLM Provider: Select "Ollama"
2. Model: Enter `llama3.2:3b`
3. Ollama URL: `http://ollama:11434`
4. Leave API key fields blank (not needed for Ollama)

---

## For Images

**Provider**: Pexels  
**API Key**: `mcqPLzfW53QOcGe6H2wD2JDhLtfNbVclS0wX4Zk3OGrM6Op9XftrhxK3`  
**Cost**: Free (200 requests/hour)

---

## Quick Reference

Copy/paste these exact values:

```
LLM Provider: Ollama
Ollama URL: http://ollama:11434
Model: llama3.2:3b

Image Provider: Pexels
Pexels Key: mcqPLzfW53QOcGe6H2wD2JDhLtfNbVclS0wX4Zk3OGrM6Op9XftrhxK3
```

---

## After Configuration

Try creating a presentation on any topic. It should:
- Use Ollama for text generation (will take 2-5 minutes)
- Use Pexels for images (instant)
- Generate slides successfully

---

**Note**: Presentation generation will be SLOW (2-5 minutes) because Ollama is CPU-only. But it will work.
