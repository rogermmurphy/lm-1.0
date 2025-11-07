"""Test TTS and STT endpoints"""
import requests
import json

# Test TTS endpoint
print("Testing TTS endpoint...")
tts_url = "http://localhost:8005/chat/speak"
tts_payload = {"text": "Hello, this is a test of the text to speech system."}

try:
    response = requests.post(tts_url, json=tts_payload, timeout=15)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Audio base64 length: {len(data.get('audio_base64', ''))}")
        print("✅ TTS endpoint working!")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"❌ TTS test failed: {e}")

print("\n" + "="*50 + "\n")

# Test health
print("Testing health endpoint...")
try:
    response = requests.get("http://localhost:8005/health")
    print(f"Health: {response.json()}")
except Exception as e:
    print(f"Health check failed: {e}")
