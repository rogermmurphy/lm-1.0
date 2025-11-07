#!/usr/bin/env python3
"""Quick script to seed test user and test authentication"""
import requests
import psycopg2
import bcrypt
import sys

# Database connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "littlemonster",
    "user": "postgres",
    "password": "postgres"
}

def create_test_user():
    """Create test user in database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", ("student@test.com",))
        existing = cursor.fetchone()
        
        if existing:
            print(f"[OK] Test user already exists (ID: {existing[0]})")
            cursor.close()
            conn.close()
            return True
            
        # Create user with hashed password
        password = "Test123!@#"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (%s, %s, %s) RETURNING id",
            ("student@test.com", password_hash, "Test Student")
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"[OK] Created test user (ID: {user_id})")
        print(f"  Email: student@test.com")
        print(f"  Password: Test123!@#")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating user: {e}")
        return False

def test_login():
    """Test login endpoint"""
    try:
        url = "http://localhost:8001/auth/login"
        data = {
            "email": "student@test.com",
            "password": "Test123!@#"
        }
        
        print(f"\nTesting login at {url}...")
        response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("[OK] Login successful!")
            print(f"  Access token: {result.get('access_token', '')[:50]}...")
            print(f"  User: {result.get('user', {})}")
            return True
        else:
            print(f"[ERROR] Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error testing login: {e}")
        return False

def main():
    print("=" * 60)
    print("AUTHENTICATION QUICK TEST")
    print("=" * 60)
    
    # Step 1: Create test user
    if not create_test_user():
        sys.exit(1)
    
    # Step 2: Test login
    if not test_login():
        sys.exit(1)
    
    print("\n[OK] All tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
