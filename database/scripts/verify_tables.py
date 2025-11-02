#!/usr/bin/env python3
"""Verify database tables exist"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME', 'littlemonster'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres')
)

cur = conn.cursor()
cur.execute("""
    SELECT tablename 
    FROM pg_tables 
    WHERE schemaname = 'public' 
    ORDER BY tablename;
""")

tables = cur.fetchall()
print("\n[OK] Database Tables:")
for table in tables:
    print(f"  - {table[0]}")

print(f"\nTotal tables: {len(tables)}")

# Check for new tables
new_tables = ['classes', 'assignments', 'planner_events', 'class_schedules']
print("\n[CHECK] Verifying new tables from schema 006:")
for table_name in new_tables:
    cur.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cur.fetchone()[0]
    print(f"  [OK] {table_name}: {count} rows")

cur.close()
conn.close()
