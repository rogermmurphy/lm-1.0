"""Quick test script for auth endpoints"""
import requests
import json

BASE_URL = "http://localhost"

print("Testing Auth Endpoints...")
print("=" * 50)

# Test 1: Register
print("\n1. Testing Registration...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": f"testuser{requests.utils.quote('')}@example.com",
            "password": "TestPass123!"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code == 201:
        print("✅ Registration WORKS!")
        access_token = response.json().get("access_token")
    else:
        print("❌ Registration failed")
        access_token = None
except Exception as e:
    print(f"❌ Error: {e}")
    access_token = None

# Test 2: Login (use existing user or newly created)
print("\n2. Testing Login...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "TestPass123!"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login WORKS!")
        data = response.json()
        access_token = data.get("access_token")
        print(f"Got access token: {access_token[:20]}...")
    else:
        print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Login again immediately (test duplicate token fix)
print("\n3. Testing Login Again (duplicate token test)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "TestPass123!"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login again WORKS! No duplicate token error!")
    else:
        print(f"❌ Failed: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
print("Auth endpoint testing complete")
