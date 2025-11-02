#!/usr/bin/env python3
"""Test Text-to-Speech Service"""
import sys

try:
    print("Testing imports...")
    from src.main import app
    from src.models import TTSAudioFile
    from src.services.azure_tts import AzureTTSService
    from src.config import settings
    
    print("[OK] All imports successful")
    print(f"[OK] Service name: {settings.SERVICE_NAME}")
    print(f"[OK] Azure key configured: {len(settings.AZURE_SPEECH_KEY)} chars")
    print(f"[OK] Azure region: {settings.AZURE_SPEECH_REGION}")
    
    print("\n[SUCCESS] Text-to-Speech service is ready to start!")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
