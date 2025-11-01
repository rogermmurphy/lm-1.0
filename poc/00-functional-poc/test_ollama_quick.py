#!/usr/bin/env python3
"""Quick test to verify Ollama is working"""

import requests
import json

def test_ollama():
    print("Testing Ollama with llama3.2:3b model...")
    print("-" * 60)
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:3b",
        "prompt": "What is 2+2? Answer in one sentence.",
        "stream": False
    }
    
    try:
        print("Sending request to Ollama...")
        print("(Model loading can take 2-5 minutes on CPU...)")
        response = requests.post(url, json=payload, timeout=300)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[SUCCESS] Ollama responded!")
            print(f"Answer: {data.get('response', 'No response')}")
            return True
        else:
            print(f"\n[ERROR] Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    exit(0 if success else 1)
