#!/usr/bin/env python3
"""
Deploy Schema 011: Study Sessions & Analytics
Phase 6 database schema deployment script

This script deploys the study analytics schema including:
- study_sessions: Track study sessions
- session_activities: Activities within sessions
- performance_metrics: Aggregated performance data
- study_goals: User-defined goals
- goal_progress: Goal progress tracking
- analytics_snapshots: Pre-calculated analytics

Usage:
    python deploy_011.py
"""

import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', os.getenv('DB_NAME', 'littlemonster')),
    'user': os.getenv('POSTGRES_USER', os.getenv('DB_USER', 'postgres')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('DB_PASSWORD', 'postgres'))
}

SCHEMA_FILE = 'database/schemas/011_study_analytics.sql'

def print_header(message):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {message}")
    print("=" * 80 + "\n")

def print_success(message):
    """Print a success message"""
    print(f"[OK] {message}")

def print_error(message):
    """Print an error message"""
    print(f"[ERROR] {message}")

def print_info(message):
    """Print an info message"""
    print(f"[INFO] {message}")

def check_prerequisites(cursor):
    """Check if prerequisite tables exist"""
    print_header("Checking Prerequisites")
    
    required_tables = ['users', 'classes']
    missing_tables = []
    
    for table in required_tables:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print_success(f"Table '{table}' exists")
        else:
            print_error(f"Table '{table}' is missing")
            missing_tables.append(table)
    
    if missing_tables:
        print_error(f"\nMissing required tables: {', '.join(missing_tables)}")
        print_info("Please deploy schemas 001-010 first")
        return False
    
    print_success("\nAll prerequisites met")
    return True

def deploy_schema(cursor):
    """Deploy the schema from SQL file"""
    print_header("Deploying Schema 011")
    
    # Read schema file
    try:
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        print_success(f"Read schema file: {SCHEMA_FILE}")
    except FileNotFoundError:
        print_error(f"Schema file not found: {SCHEMA_FILE}")
        return False
    except Exception as e:
        print_error(f"Error reading schema file: {e}")
        return False
    
    # Execute schema
    try:
        cursor.execute(schema_sql)
        print_success("Schema SQL executed successfully")
        return True
    except Exception as e:
        print_error(f"Error executing schema: {e}")
        return False

def verify_deployment(cursor):
    """Verify that all tables were created"""
    print_header("Verifying Deployment")
    
    expected_tables = [
        'study_sessions',
        'session_activities',
        'performance_metrics',
        'study_goals',
        'goal_progress',
        'analytics_snapshots'
    ]
    
    all_created = True
    
    for table in expected_tables:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (table,))
        
        exists = cursor.fetchone()[0]
        if exists:
            # Get row count
            cursor.execute(sql.SQL("SELECT COUNT(*) FROM {}").format(
                sql.Identifier(table)
            ))
            count = cursor.fetchone()[0]
            print_success(f"Table '{table}' created ({count} rows)")
        else:
            print_error(f"Table '{table}' was not created")
            all_created = False
    
    return all_created

def verify_functions(cursor):
    """Verify that functions were created"""
    print_header("Verifying Functions")
    
    expected_functions = [
        'calculate_session_duration',
        'calculate_activity_duration',
        'update_goal_progress_percentage',
        'update_goal_current_value',
        'check_expired_goals'
    ]
    
    all_created = True
    
    for func in expected_functions:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM pg_proc 
                WHERE proname = %s
            );
        """, (func,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print_success(f"Function '{func}' created")
        else:
            print_error(f"Function '{func}' was not created")
            all_created = False
    
    return all_created

def verify_views(cursor):
    """Verify that views were created"""
    print_header("Verifying Views")
    
    expected_views = [
        'active_study_sessions',
        'user_study_summary_30d',
        'active_goals_with_progress'
    ]
    
    all_created = True
    
    for view in expected_views:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.views 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, (view,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print_success(f"View '{view}' created")
        else:
            print_error(f"View '{view}' was not created")
            all_created = False
    
    return all_created

def verify_indexes(cursor):
    """Verify that indexes were created"""
    print_header("Verifying Indexes")
    
    cursor.execute("""
        SELECT tablename, indexname 
        FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND tablename IN (
            'study_sessions', 'session_activities', 'performance_metrics',
            'study_goals', 'goal_progress', 'analytics_snapshots'
        )
        ORDER BY tablename, indexname;
    """)
    
    indexes = cursor.fetchall()
    
    if indexes:
        print_success(f"Found {len(indexes)} indexes:")
        for table, index in indexes:
            print(f"  - {table}: {index}")
        return True
    else:
        print_error("No indexes found")
        return False

def print_summary(success):
    """Print deployment summary"""
    print_header("Deployment Summary")
    
    if success:
        print_success("Schema 011 deployed successfully!")
        print_info("\nNew tables:")
        print("  - study_sessions (6 indexes)")
        print("  - session_activities (4 indexes)")
        print("  - performance_metrics (5 indexes)")
        print("  - study_goals (5 indexes)")
        print("  - goal_progress (3 indexes)")
        print("  - analytics_snapshots (4 indexes)")
        print_info("\nNew functions:")
        print("  - calculate_session_duration()")
        print("  - calculate_activity_duration()")
        print("  - update_goal_progress_percentage()")
        print("  - update_goal_current_value()")
        print("  - check_expired_goals()")
        print_info("\nNew views:")
        print("  - active_study_sessions")
        print("  - user_study_summary_30d")
        print("  - active_goals_with_progress")
        print_info("\nNext steps:")
        print("  1. Run verify_011.py to validate the schema")
        print("  2. Create the study-analytics service")
        print("  3. Test with test_service.py")
    else:
        print_error("Schema 011 deployment failed!")
        print_info("\nPlease check the error messages above and try again.")

def main():
    """Main deployment function"""
    print_header("Schema 011 Deployment - Study Sessions & Analytics")
    print_info(f"Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}")
    
    conn = None
    success = False
    
    try:
        # Connect to database
        print_info("\nConnecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print_success("Connected to database")
        
        # Check prerequisites
        if not check_prerequisites(cursor):
            return 1
        
        # Deploy schema
        if not deploy_schema(cursor):
            return 1
        
        # Commit changes
        conn.commit()
        print_success("Changes committed")
        
        # Verify deployment
        tables_ok = verify_deployment(cursor)
        functions_ok = verify_functions(cursor)
        views_ok = verify_views(cursor)
        indexes_ok = verify_indexes(cursor)
        
        success = tables_ok and functions_ok and views_ok and indexes_ok
        
    except psycopg2.Error as e:
        print_error(f"Database error: {e}")
        if conn:
            conn.rollback()
            print_info("Changes rolled back")
        return 1
    
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if conn:
            conn.rollback()
            print_info("Changes rolled back")
        return 1
    
    finally:
        if conn:
            conn.close()
            print_info("\nDatabase connection closed")
    
    # Print summary
    print_summary(success)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
