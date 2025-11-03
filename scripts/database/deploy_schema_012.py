#!/usr/bin/env python3
"""
Deploy Schema 012: Notifications & Communication
Phase 7 database schema deployment script
"""
import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', os.getenv('DB_NAME', 'littlemonster')),
    'user': os.getenv('POSTGRES_USER', os.getenv('DB_USER', 'postgres')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('DB_PASSWORD', 'postgres'))
}

SCHEMA_FILE = 'database/schemas/012_notifications.sql'

def print_header(message):
    print("\n" + "=" * 80)
    print(f"  {message}")
    print("=" * 80 + "\n")

def print_success(message):
    print(f"[OK] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def main():
    print_header("Schema 012 Deployment - Notifications & Communication")
    print_info(f"Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    conn = None
    try:
        print_info("\nConnecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print_success("Connected to database")
        
        # Check prerequisites
        print_header("Checking Prerequisites")
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users')")
        if cursor.fetchone()[0]:
            print_success("Table 'users' exists")
        else:
            print_error("Table 'users' missing")
            return 1
        
        # Deploy schema
        print_header("Deploying Schema 012")
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print_success(f"Read schema file: {SCHEMA_FILE}")
        
        cursor.execute(schema_sql)
        print_success("Schema SQL executed successfully")
        
        conn.commit()
        print_success("Changes committed")
        
        # Verify deployment
        print_header("Verifying Deployment")
        expected_tables = ['notifications', 'notification_preferences', 'direct_messages', 
                          'announcements', 'notification_templates']
        
        for table in expected_tables:
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", (table,))
            if cursor.fetchone()[0]:
                cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table)))
                count = cursor.fetchone()[0]
                print_success(f"Table '{table}' created ({count} rows)")
            else:
                print_error(f"Table '{table}' was not created")
                return 1
        
        print_header("Deployment Summary")
        print_success("Schema 012 deployed successfully!")
        print_info("\nNew tables: 5")
        print_info("New functions: 3")
        print_info("New views: 4")
        print_info("\nNext: Create notifications service on port 8013")
        
        return 0
        
    except Exception as e:
        print_error(f"Error: {e}")
        if conn:
            conn.rollback()
        return 1
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    sys.exit(main())
