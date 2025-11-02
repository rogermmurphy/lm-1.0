import requests
import json
import base64

# Test TTS endpoint
url = "http://localhost/api/tts/generate"
payload = {
    "text": "Hello world, this is a test",
    "voice": "en-US-AvaNeural"
}

headers = {"Content-Type": "application/json"}

print("Testing TTS endpoint...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess! Response keys: {list(data.keys())}")
        if 'audio' in data:
            audio_data = data['audio']
            print(f"Audio data length: {len(audio_data)} characters")
            print(f"First 100 chars: {audio_data[:100]}")
            
            # Try to decode base64
            try:
                audio_bytes = base64.b64decode(audio_data)
                print(f"Decoded audio bytes: {len(audio_bytes)} bytes")
                print("✅ TTS endpoint working - audio generated!")
            except Exception as e:
                print(f"Error decoding base64: {e}")
        else:
            print("Response structure:", json.dumps(data, indent=2)[:500])
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
