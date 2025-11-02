"""
Test Backend API Fixes
Tests the TTS and Materials endpoints with proper authentication
"""
import requests
import json
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost"

def test_login():
    """Get authentication token"""
    print("1. Testing Login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": "testuser@example.com", "password": "TestPass123!"}
    )
    if response.status_code == 200:
        data = response.json()
        print(f"[OK] Login successful! Token: {data['access_token'][:20]}...")
        return data['access_token']
    else:
        print(f"[FAIL] Login failed: {response.status_code} - {response.text}")
        return None

def test_materials_list(token):
    """Test GET /api/chat/materials endpoint"""
    print("\n2. Testing Materials List Endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/chat/materials", headers=headers)
    
    if response.status_code == 200:
        materials = response.json()
        print(f"[OK] Materials list endpoint working! Found {len(materials)} materials")
        if materials:
            print(f"  Sample: {materials[0]}")
        return True
    else:
        print(f"[FAIL] Materials list failed: {response.status_code} - {response.text}")
        return False

def test_tts_generate(token):
    """Test POST /api/tts/generate endpoint with JSON body"""
    print("\n3. Testing TTS Generate Endpoint (JSON body)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": "Hello world, this is a test",
        "voice": "en-US-AvaMultilingualNeural"
    }
    response = requests.post(
        f"{BASE_URL}/api/tts/generate",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] TTS endpoint working!")
        print(f"  ID: {result.get('id')}")
        print(f"  Provider: {result.get('provider')}")
        print(f"  Voice: {result.get('voice')}")
        has_audio = 'audio_base64' in result and len(result['audio_base64']) > 0
        print(f"  Has audio_base64: {has_audio}")
        if has_audio:
            print(f"  Audio size: {len(result['audio_base64'])} characters")
        return True
    else:
        print(f"[FAIL] TTS failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    print("=== Backend API Fixes Test ===\n")
    
    # Get token
    token = test_login()
    if not token:
        print("\n[FAIL] Cannot proceed without authentication token")
        exit(1)
    
    # Test materials list
    materials_ok = test_materials_list(token)
    
    # Test TTS
    tts_ok = test_tts_generate(token)
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Materials List Endpoint: {'[PASS]' if materials_ok else '[FAIL]'}")
    print(f"TTS Generate Endpoint: {'[PASS]' if tts_ok else '[FAIL]'}")
    
    if materials_ok and tts_ok:
        print("\n[OK] All backend fixes verified successfully!")
        exit(0)
    else:
        print("\n[FAIL] Some tests failed - review errors above")
        exit(1)
