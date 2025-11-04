#!/usr/bin/env python3
"""Quick script to register a test user"""
import requests

url = "http://localhost/api/auth/register"
data = {
    "email": "test@example.com",
    "password": "Password123!",
    "first_name": "Test",
    "last_name": "User"
}

print("Registering user...")
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
