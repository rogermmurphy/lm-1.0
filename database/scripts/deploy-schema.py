#!/usr/bin/env python3
"""
Deploy Database Schema using Python
"""
import psycopg2
import sys

try:
    # First connect to postgres database to create littlemonster
    print("[INFO] Creating database if not exists...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='littlemonster'")
    exists = cursor.fetchone()
    
    if not exists:
        cursor.execute("CREATE DATABASE littlemonster")
        print("[OK] Database 'littlemonster' created")
    else:
        print("[OK] Database 'littlemonster' already exists")
    
    cursor.close()
    conn.close()
    
    # Now connect to littlemonster database
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="littlemonster",
        user="postgres",
        password="postgres"
    )
    
    print("[OK] Connected to littlemonster database")
    
    # Read and execute schema
    with open('../../database/schemas/master-schema.sql', 'r') as f:
        schema_sql = f.read()
    
    cursor = conn.cursor()
    cursor.execute(schema_sql)
    conn.commit()
    
    print("[OK] Schema deployed successfully")
    
    # Verify tables
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
    table_count = cursor.fetchone()[0]
    print(f"[OK] Tables created: {table_count}")
    
    cursor.close()
    conn.close()
    print("[SUCCESS] Database ready!")
    
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
