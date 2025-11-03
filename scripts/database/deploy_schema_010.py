#!/usr/bin/env python3
"""
Deploy Schema 010 - Gamification
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_schema():
    """Deploy schema 010"""
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='littlemonster',
        user='postgres',
        password='postgres'
    )
    
    try:
        with conn.cursor() as cur:
            # Read and execute schema
            with open('database/schemas/010_gamification.sql', 'r') as f:
                schema_sql = f.read()
            
            print("Deploying schema 010_gamification...")
            cur.execute(schema_sql)
            conn.commit()
            print("[SUCCESS] Schema 010 deployed successfully!")
            
            # Verify tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN (
                    'user_points',
                    'achievements',
                    'leaderboards',
                    'point_transactions'
                )
                ORDER BY table_name
            """)
            
            tables = cur.fetchall()
            print(f"\n[SUCCESS] Verified {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"[ERROR] {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    deploy_schema()
