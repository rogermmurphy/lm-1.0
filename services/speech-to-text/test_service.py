#!/usr/bin/env python3
"""Test Speech-to-Text Service"""
import sys

try:
    print("Testing imports...")
    from src.main import app
    from src.models import TranscriptionJob, Transcription
    from src.services.whisper_service import WhisperService
    from src.config import settings
    
    print("[OK] All imports successful")
    print(f"[OK] Service name: {settings.SERVICE_NAME}")
    print(f"[OK] Whisper model: {settings.WHISPER_MODEL_SIZE}")
    
    print("\n[SUCCESS] Speech-to-Text service is ready to start!")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
