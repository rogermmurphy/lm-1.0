"""
Seed Users for Little Monster GPA Database
Generates 10 test users with different profiles
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from base_seeder import BaseSeeder, SeedDataGenerator, hash_password
import random


class UserSeeder(BaseSeeder):
    """Seeder for user accounts"""
    
    def seed(self, count=10, clear_existing=False):
        """
        Seed user accounts
        
        Args:
            count: Number of users to create (default: 10)
            clear_existing: Whether to clear existing users first (default: False)
        
        Returns:
            List of created user IDs
        """
        self.print_info(f"Seeding {count} users...")
        
        if clear_existing:
            self.print_info("Clearing existing users...")
            self.clear_table('users')
        
        # Generate diverse user profiles
        users_data = []
        
        # User 1: Test user (existing user with ID 7 mentioned in docs)
        users_data.append({
            'email': 'testuser@test.com',
            'username': 'testuser',
            'password_hash': hash_password('password123'),
            'full_name': 'Test User',
            'is_verified': True,
            'is_active': True
        })
        
        # Users 2-10: Generated users with various profiles
        first_names = random.sample(SeedDataGenerator.FIRST_NAMES, count - 1)
        last_names = random.sample(SeedDataGenerator.LAST_NAMES, count - 1)
        
        for i in range(count - 1):
            first_name = first_names[i]
            last_name = last_names[i]
            
            users_data.append({
                'email': SeedDataGenerator.generate_email(first_name, last_name),
                'username': SeedDataGenerator.generate_username(first_name, last_name),
                'password_hash': hash_password('password123'),  # Same password for all test users
                'full_name': SeedDataGenerator.generate_full_name(first_name, last_name),
                'is_verified': random.choice([True, True, True, False]),  # 75% verified
                'is_active': True
            })
        
        # Insert users
        user_ids = []
        for user_data in users_data:
            try:
                user_id = self.insert_one('users', user_data)
                user_ids.append(user_id)
                self.print_success(f"Created user: {user_data['email']} (ID: {user_id})")
            except Exception as e:
                # If user already exists, try to get their ID
                if 'unique constraint' in str(e).lower() or 'duplicate' in str(e).lower():
                    result = self.execute_query(
                        "SELECT id FROM users WHERE email = %s",
                        (user_data['email'],),
                        fetch=True
                    )
                    if result:
                        user_id = result[0]['id']
                        user_ids.append(user_id)
                        self.print_info(f"User already exists: {user_data['email']} (ID: {user_id})")
                else:
                    raise
        
        self.print_success(f"Seeded {len(user_ids)} users")
        return user_ids
    
    def get_all_user_ids(self):
        """Get all user IDs from database"""
        result = self.execute_query("SELECT id FROM users ORDER BY id", fetch=True)
        return [row['id'] for row in result] if result else []
    
    def get_random_user_ids(self, count=5):
        """Get random user IDs"""
        all_ids = self.get_all_user_ids()
        return random.sample(all_ids, min(count, len(all_ids)))


def main():
    """Main function to run user seeding"""
    print("\n" + "="*60)
    print("SEEDING USERS")
    print("="*60 + "\n")
    
    with UserSeeder() as seeder:
        # Check if we should clear existing data
        import sys
        clear_existing = '--clear' in sys.argv
        
        if clear_existing:
            print("⚠️  WARNING: This will delete all existing users and related data!")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
        
        # Seed users
        user_ids = seeder.seed(count=10, clear_existing=clear_existing)
        
        print(f"\n{'='*60}")
        print(f"✓ Successfully seeded {len(user_ids)} users")
        print(f"{'='*60}\n")
        
        # Display summary
        print("User Summary:")
        print(f"  Total Users: {len(user_ids)}")
        print(f"  User IDs: {user_ids}")
        print("\nAll users have password: password123")
        print("Test user: testuser@test.com")


if __name__ == "__main__":
    main()
