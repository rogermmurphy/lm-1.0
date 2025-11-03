#!/usr/bin/env python3
"""
Deploy Schema 009 - Social & Collaboration
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def deploy_schema():
    """Deploy schema 009"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('POSTGRES_DB', 'littlemonster'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'postgres')
    )
    
    try:
        with conn.cursor() as cur:
            # Read and execute schema
            with open('database/schemas/009_social.sql', 'r') as f:
                schema_sql = f.read()
            
            print("Deploying schema 009_social...")
            cur.execute(schema_sql)
            conn.commit()
            print("[SUCCESS] Schema 009 deployed successfully!")
            
            # Verify tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN (
                    'classmate_connections',
                    'shared_content',
                    'study_groups',
                    'study_group_members',
                    'study_group_messages'
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
