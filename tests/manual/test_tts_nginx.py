import requests
import json

url = "http://localhost/api/tts/generate"
payload = {"text": "Hello world", "voice": "en-US-AvaNeural"}

print("Testing TTS service through nginx gateway...")
try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        if 'audio_base64' in data:
            print(f"SUCCESS - Audio length: {len(data['audio_base64'])} chars")
        else:
            print(f"ERROR - No audio_base64 in response: {data}")
    else:
        print(f"ERROR: {response.text}")
except Exception as e:
    print(f"ERROR: {e}")
