"""
Base Seeder Class for Little Monster GPA Database
Provides common database connection and utility methods for all seeders
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any, Optional

# Add parent directory to path to import lm_common
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from shared.python_common.lm_common.database import get_db_connection
    from shared.python_common.lm_common.auth.password_utils import hash_password
except ImportError:
    # Fallback if lm_common not available
    def get_db_connection():
        """Get database connection from environment variables"""
        return psycopg2.connect(
            # FIXED: Use local Docker PostgreSQL, NOT Supabase!
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'littlemonster'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
            # NO sslmode for local PostgreSQL
        )
    
    def hash_password(password: str) -> str:
        """Simple password hashing fallback"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()


class BaseSeeder:
    """Base class for all database seeders"""
    
    def __init__(self, conn=None):
        """Initialize seeder with optional database connection"""
        self.conn = conn
        self.should_close_conn = False
        
        if self.conn is None:
            self.conn = get_db_connection()
            self.should_close_conn = True
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection if we created it"""
        if self.should_close_conn and self.conn:
            self.conn.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False) -> Optional[List[Dict]]:
        """Execute a database query"""
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch:
                    return cur.fetchall()
                self.conn.commit()
                return None
        except Exception as e:
            self.conn.rollback()
            print(f"Error executing query: {e}")
            print(f"Query: {query}")
            raise
    
    def insert_one(self, table: str, data: Dict[str, Any]) -> int:
        """Insert a single record and return its ID"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
        
        result = self.execute_query(query, tuple(data.values()), fetch=True)
        return result[0]['id'] if result else None
    
    def insert_many(self, table: str, records: List[Dict[str, Any]]) -> List[int]:
        """Insert multiple records and return their IDs"""
        if not records:
            return []
        
        ids = []
        for record in records:
            record_id = self.insert_one(table, record)
            ids.append(record_id)
        
        return ids
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            )
        """
        result = self.execute_query(query, (table_name,), fetch=True)
        return result[0]['exists'] if result else False
    
    def clear_table(self, table_name: str):
        """Clear all data from a table"""
        if self.table_exists(table_name):
            self.execute_query(f"TRUNCATE TABLE {table_name} CASCADE")
            print(f"✓ Cleared table: {table_name}")
    
    def get_random_date(self, days_ago_min: int = 1, days_ago_max: int = 30) -> datetime:
        """Get a random datetime within the specified range"""
        days_ago = random.randint(days_ago_min, days_ago_max)
        return datetime.now() - timedelta(days=days_ago)
    
    def get_random_future_date(self, days_ahead_min: int = 1, days_ahead_max: int = 30) -> datetime:
        """Get a random future datetime within the specified range"""
        days_ahead = random.randint(days_ahead_min, days_ahead_max)
        return datetime.now() + timedelta(days=days_ahead)
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"✓ {message}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"ℹ {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"✗ {message}")


class SeedDataGenerator:
    """Utility class for generating realistic seed data"""
    
    # Sample data for generating realistic content
    FIRST_NAMES = [
        "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
        "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez"
    ]
    
    SUBJECTS = [
        "Mathematics", "Physics", "Chemistry", "Biology", "English Literature",
        "World History", "Computer Science", "Psychology", "Economics", "Art History",
        "Spanish", "French", "Statistics", "Calculus", "Philosophy"
    ]
    
    ASSIGNMENT_TYPES = [
        "Homework", "Quiz", "Test", "Project", "Essay", "Lab Report",
        "Presentation", "Research Paper", "Problem Set", "Reading Assignment"
    ]
    
    ACHIEVEMENT_TYPES = [
        "First Login", "Complete Profile", "First Study Session", "Study Streak 7 Days",
        "Study Streak 30 Days", "100 Flashcards Reviewed", "First Perfect Quiz",
        "Join Study Group", "Help a Friend", "Upload First Material",
        "Create 10 Notes", "Complete 5 Assignments", "Master a Subject"
    ]
    
    @staticmethod
    def generate_email(first_name: str, last_name: str, domain: str = "test.com") -> str:
        """Generate an email address"""
        return f"{first_name.lower()}.{last_name.lower()}@{domain}"
    
    @staticmethod
    def generate_username(first_name: str, last_name: str) -> str:
        """Generate a username"""
        return f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"
    
    @staticmethod
    def generate_full_name(first_name: str, last_name: str) -> str:
        """Generate a full name"""
        return f"{first_name} {last_name}"
    
    @staticmethod
    def get_random_subject() -> str:
        """Get a random subject"""
        return random.choice(SeedDataGenerator.SUBJECTS)
    
    @staticmethod
    def get_random_assignment_type() -> str:
        """Get a random assignment type"""
        return random.choice(SeedDataGenerator.ASSIGNMENT_TYPES)
    
    @staticmethod
    def get_random_achievement() -> str:
        """Get a random achievement"""
        return random.choice(SeedDataGenerator.ACHIEVEMENT_TYPES)


if __name__ == "__main__":
    # Test the base seeder
    print("Testing BaseSeeder...")
    
    with BaseSeeder() as seeder:
        # Test table existence check
        exists = seeder.table_exists('users')
        print(f"Users table exists: {exists}")
        
        if exists:
            # Test query execution
            result = seeder.execute_query(
                "SELECT COUNT(*) as count FROM users",
                fetch=True
            )
            print(f"Current user count: {result[0]['count']}")
    
    print("\n✓ BaseSeeder test complete!")
