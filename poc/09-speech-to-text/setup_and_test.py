#!/usr/bin/env python3
"""
Setup and Test Script - Creates database table and runs tests
"""

import psycopg2
import sys

def setup_database():
    """Create the transcription_jobs table"""
    print("="*70)
    print("SETTING UP DATABASE")
    print("="*70)
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="lm_dev",
            user="postgres",
            password="postgres"
        )
        print("[OK] Connected to PostgreSQL")
        
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        print("[OK] Database table created/verified")
        
        # Check if table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_name = 'transcription_jobs'
        """)
        
        if cursor.fetchone()[0] > 0:
            print("[OK] Table 'transcription_jobs' exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Database setup failed: {e}")
        return False

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        client.ping()
        print("[OK] Redis is running")
        return True
    except Exception as e:
        print(f"[WARNING] Redis check failed: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("SPEECH-TO-TEXT POC - SETUP AND TEST")
    print("="*70 + "\n")
    
    # Step 1: Setup database
    if not setup_database():
        print("\n[ERROR] Database setup failed. Cannot continue.")
        sys.exit(1)
    
    # Step 2: Check Redis
    print("\n" + "="*70)
    print("CHECKING REDIS")
    print("="*70)
    check_redis()
    
    # Step 3: Run tests
    print("\n" + "="*70)
    print("RUNNING TESTS")
    print("="*70)
    
    try:
        from test_transcription import test_async_transcription
        test_async_transcription()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
