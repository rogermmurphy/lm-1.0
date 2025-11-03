import requests
import json

# Register user
url = "http://localhost:8001/auth/register"
data = {
    "email": "testuser@test.com",
    "password": "Test123!",
    "username": "testuser"
}

print("Registering test user...")
response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    print("\n[SUCCESS] User registered!")
    result = response.json()
    print(f"User ID: {result['user']['id']}")
    print(f"Email: {result['user']['email']}")
    print(f"Username: {result['user']['username']}")
else:
    print("\n[ERROR] Registration failed")
