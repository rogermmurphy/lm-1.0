#!/usr/bin/env python3
"""
Test Authentication Service
Verify service can start and imports work
"""
import sys

try:
    print("Testing imports...")
    from src.main import app
    from src.models import User
    from src.schemas import UserRegisterRequest
    from src.config import settings
    
    print("[OK] All imports successful")
    print(f"[OK] Service name: {settings.SERVICE_NAME}")
    print(f"[OK] Database URL configured: {settings.DATABASE_URL[:50]}...")
    print(f"[OK] JWT secret configured: {len(settings.JWT_SECRET_KEY)} chars")
    
    print("\n[SUCCESS] Authentication service is ready to start!")
    sys.exit(0)
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
