import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='littlemonster',
    user='postgres',
    password='postgres'
)

cur = conn.cursor()
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
print(f'Found {len(tables)} Phase 4 tables:')
for t in tables:
    print(f'  - {t[0]}')

conn.close()
