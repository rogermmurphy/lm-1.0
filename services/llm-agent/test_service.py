#!/usr/bin/env python3
"""
Test LLM Agent Service
Verify service can start and imports work
"""
import sys

try:
    print("Testing imports...")
    from src.main import app
    from src.models import Conversation, Message
    from src.services import RAGService, LLMService
    from src.config import settings
    
    print("[OK] All imports successful")
    print(f"[OK] Service name: {settings.SERVICE_NAME}")
    print(f"[OK] Ollama URL: {settings.OLLAMA_URL}")
    print(f"[OK] Ollama model: {settings.OLLAMA_MODEL}")
    print(f"[OK] ChromaDB: {settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}")
    
    print("\n[SUCCESS] LLM Agent service is ready to start!")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
