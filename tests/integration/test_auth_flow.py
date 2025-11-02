#!/usr/bin/env python3
"""
Integration Test: Authentication Flow
Tests complete user authentication workflow
"""
import requests
import sys

API_URL = "http://localhost:8001"

def test_auth_flow():
    """Test complete authentication workflow"""
    print("="*70)
    print("INTEGRATION TEST: Authentication Flow")
    print("="*70)
    
    # Test 1: Register User
    print("\n[TEST 1] Register new user...")
    register_data = {
        "email": "testuser@example.com",
        "password": "TestPass123!",
        "username": "testuser"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("[PASS] User registered successfully")
            user = response.json()
            print(f"  User ID: {user['id']}")
            print(f"  Email: {user['email']}")
        else:
            print(f"[FAIL] Registration failed: {response.status_code}")
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    
    # Test 2: Login
    print("\n[TEST 2] Login with credentials...")
    login_data = {
        "email": "testuser@example.com",
        "password": "TestPass123!"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("[PASS] Login successful")
            tokens = response.json()
            access_token = tokens['access_token']
            refresh_token = tokens['refresh_token']
            print(f"  Access token: {access_token[:20]}...")
            print(f"  Refresh token: {refresh_token[:20]}...")
            print(f"  Expires in: {tokens['expires_in']} seconds")
        else:
            print(f"[FAIL] Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    
    # Test 3: Refresh Token
    print("\n[TEST 3] Refresh access token...")
    try:
        response = requests.post(f"{API_URL}/auth/refresh", json={"refresh_token": refresh_token})
        if response.status_code == 200:
            print("[PASS] Token refresh successful")
            new_tokens = response.json()
            print(f"  New access token: {new_tokens['access_token'][:20]}...")
        else:
            print(f"[FAIL] Refresh failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    
    # Test 4: Logout
    print("\n[TEST 4] Logout...")
    try:
        response = requests.post(f"{API_URL}/auth/logout", json={"refresh_token": refresh_token})
        if response.status_code == 200:
            print("[PASS] Logout successful")
        else:
            print(f"[FAIL] Logout failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False
    
    print("\n"+"="*70)
    print("[SUCCESS] All authentication tests passed!")
    print("="*70)
    return True

if __name__ == "__main__":
    print("\nPrerequisite: Start auth service on port 8001")
    print("Command: cd services/authentication && python -m uvicorn src.main:app --port 8001\n")
    
    input("Press Enter when service is running...")
    
    success = test_auth_flow()
    sys.exit(0 if success else 1)
