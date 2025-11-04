import requests
import json

# Test login
response = requests.post(
    "http://localhost/api/auth/login",
    json={"email": "testuser@example.com", "password": "TestPass123!"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
