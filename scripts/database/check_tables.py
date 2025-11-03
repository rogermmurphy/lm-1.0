import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="littlemonster",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()
cur.execute("""
    SELECT tablename FROM pg_tables 
    WHERE schemaname='public' 
    AND tablename LIKE '%note%' OR tablename LIKE '%material%'
    ORDER BY tablename;
""")

tables = cur.fetchall()
print("Tables with 'note' or 'material' in name:")
for table in tables:
    print(f"  - {table[0]}")

cur.close()
conn.close()
