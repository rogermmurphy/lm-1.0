#!/usr/bin/env python3
"""Test authentication through nginx gateway"""
import requests

def test_through_nginx():
    """Test login through nginx gateway at port 80"""
    try:
        url = "http://localhost/api/auth/login"
        data = {
            "email": "student@test.com",
            "password": "Test123!@#"
        }
        
        print(f"Testing login through nginx gateway...")
        print(f"URL: {url}")
        response = requests.post(url, json=data, timeout=5)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("[OK] Login through nginx successful!")
            return True
        else:
            print(f"[ERROR] Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def test_direct():
    """Test login directly to auth service at port 8001"""
    try:
        url = "http://localhost:8001/auth/login"
        data = {
            "email": "student@test.com",
            "password": "Test123!@#"
        }
        
        print(f"\nTesting login directly to auth service...")
        print(f"URL: {url}")
        response = requests.post(url, json=data, timeout=5)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        if response.status_code == 200:
            print("[OK] Direct login successful!")
            return True
        else:
            print(f"[ERROR] Direct login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("NGINX ROUTING TEST")
    print("=" * 60)
    
    direct_ok = test_direct()
    nginx_ok = test_through_nginx()
    
    print("\n" + "=" * 60)
    print(f"Direct to service (port 8001): {'OK' if direct_ok else 'FAILED'}")
    print(f"Through nginx (port 80): {'OK' if nginx_ok else 'FAILED'}")
    print("=" * 60)
