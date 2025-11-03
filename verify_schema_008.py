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
    AND tablename IN ('note_sources', 'generated_tests', 'test_questions', 'test_attempts', 'flashcard_decks', 'flashcards', 'flashcard_reviews')
    ORDER BY tablename;
""")

tables = cur.fetchall()
print(f"Schema 008 tables found: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

cur.close()
conn.close()
