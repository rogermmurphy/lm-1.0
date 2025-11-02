"""Quick test of Class Management Service"""
import requests

BASE_URL = "http://localhost:8006"

# Test health
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# Test root
response = requests.get(f"{BASE_URL}/")
print(f"Root: {response.json()}")

print("\nClass Management Service is running!")
print("API Docs: http://localhost:8006/docs")
