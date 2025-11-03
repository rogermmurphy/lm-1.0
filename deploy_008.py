import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="littlemonster",
        user="postgres",
        password="postgres"
    )
    
    with open('database/schemas/008_study_tools.sql', 'r') as f:
        schema_sql = f.read()
    
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    
    print("[OK] Schema 008 deployed successfully")
    
    # Verify tables
    cur.execute("""
        SELECT tablename FROM pg_tables 
        WHERE schemaname='public' 
        AND tablename IN ('note_sources', 'generated_tests', 'test_questions', 'test_attempts', 'flashcard_decks', 'flashcards', 'flashcard_reviews')
        ORDER BY tablename;
    """)
    
    tables = cur.fetchall()
    print(f"[OK] Schema 008 tables created: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
