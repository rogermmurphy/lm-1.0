"""
Master Seed Script for Little Monster GPA Database
Seeds all tables with comprehensive test data
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from base_seeder import BaseSeeder, SeedDataGenerator
from seed_users import UserSeeder
import random
from datetime import datetime, timedelta


class MasterSeeder(BaseSeeder):
    """Master seeder that coordinates all seeding operations"""
    
    def __init__(self, conn=None):
        super().__init__(conn)
        self.user_seeder = UserSeeder(self.conn)
        self.user_ids = []
    
    def seed_all(self, clear_existing=False):
        """Seed all tables with test data"""
        print("\n" + "="*80)
        print(" "*25 + "LITTLE MONSTER GPA")
        print(" "*22 + "DATABASE SEED SCRIPT")
        print("="*80 + "\n")
        
        if clear_existing:
            print("⚠️  WARNING: Clearing all existing data!")
            self.clear_all_tables()
        
        # Seed in dependency order
        print("\n📊 Phase 1: Core Data")
        print("-" * 80)
        self.user_ids = self.user_seeder.seed(count=10, clear_existing=False)
        
        print("\n📚 Phase 2: Academic Data")
        print("-" * 80)
        class_ids = self.seed_classes()
        assignment_ids = self.seed_assignments(class_ids)
        
        print("\n💬 Phase 3: Communication Data")
        print("-" * 80)
        conversation_ids = self.seed_conversations()
        self.seed_messages(conversation_ids)
        material_ids = self.seed_study_materials()
        
        print("\n📝 Phase 4: Study Tools Data")
        print("-" * 80)
        note_ids = self.seed_notes(class_ids)
        flashcard_set_ids = self.seed_flashcard_sets(class_ids)
        self.seed_flashcards(flashcard_set_ids)
        test_ids = self.seed_practice_tests(class_ids)
        
        print("\n👥 Phase 5: Social Data")
        print("-" * 80)
        self.seed_connections()
        group_ids = self.seed_groups()
        self.seed_group_members(group_ids)
        self.seed_shared_content(note_ids, flashcard_set_ids)
        
        print("\n🏆 Phase 6: Gamification Data")
        print("-" * 80)
        self.seed_achievements()
        self.seed_user_achievements()
        self.seed_points()
        self.seed_leaderboard_entries()
        
        print("\n📈 Phase 7: Analytics Data")
        print("-" * 80)
        self.seed_study_sessions()
        self.seed_goals()
        
        print("\n🔔 Phase 8: Notifications Data")
        print("-" * 80)
        self.seed_notifications()
        self.seed_user_messages()
        
        print("\n" + "="*80)
        print("✅ DATABASE SEEDING COMPLETE!")
        print("="*80)
        self.print_summary()
    
    def clear_all_tables(self):
        """Clear all tables in reverse dependency order"""
        tables = [
            # Dependent tables first
            'notification_preferences', 'user_messages', 'notifications',
            'study_goals', 'study_sessions',
            'leaderboard_entries', 'user_points', 'user_achievements', 'achievements',
            'shared_content', 'group_members', 'study_groups', 'user_connections',
            'practice_test_questions', 'practice_tests', 'flashcards', 'flashcard_sets', 'ai_notes',
            'study_materials', 'messages', 'conversations',
            'assignments', 'class_schedules', 'planner_events', 'classes',
            'transcriptions', 'transcription_jobs',
            'tts_audio_files', 'recordings',
            'jobs',
            'password_reset_tokens', 'refresh_tokens', 'oauth_connections',
            'users'
        ]
        
        for table in tables:
            try:
                if self.table_exists(table):
                    self.clear_table(table)
            except Exception as e:
                self.print_info(f"Skipping {table}: {str(e)}")
    
    def seed_classes(self):
        """Seed 15 classes across different subjects"""
        self.print_info("Seeding classes...")
        
        class_data = []
        subjects = SeedDataGenerator.SUBJECTS[:15]  # Take first 15 subjects
        
        for subject in subjects:
            # Each class owned by a random user
            user_id = random.choice(self.user_ids)
            
            class_data.append({
                'user_id': user_id,
                'name': subject,
                'description': f'Comprehensive course in {subject}',
                'subject': subject.split()[0],  # First word as subject category
                'color': random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']),
                'is_archived': False
            })
        
        class_ids = self.insert_many('classes', class_data)
        self.print_success(f"Created {len(class_ids)} classes")
        return class_ids
    
    def seed_assignments(self, class_ids):
        """Seed 50 assignments across classes"""
        self.print_info("Seeding assignments...")
        
        assignment_data = []
        statuses = ['pending', 'in_progress', 'completed']
        priorities = ['low', 'medium', 'high']
        
        for i in range(50):
            class_id = random.choice(class_ids)
            assignment_type = SeedDataGenerator.get_random_assignment_type()
            
            # Mix of past, current, and future assignments
            if i < 15:  # Past assignments (completed)
                due_date = self.get_random_date(7, 60)
                status = 'completed'
            elif i < 35:  # Current assignments
                due_date = self.get_random_future_date(1, 14)
                status = random.choice(['pending', 'in_progress'])
            else:  # Future assignments
                due_date = self.get_random_future_date(15, 90)
                status = 'pending'
            
            assignment_data.append({
                'class_id': class_id,
                'title': f'{assignment_type} #{i+1}',
                'description': f'Complete the {assignment_type.lower()} assignment',
                'due_date': due_date,
                'status': status,
                'priority': random.choice(priorities)
            })
        
        assignment_ids = self.insert_many('assignments', assignment_data)
        self.print_success(f"Created {len(assignment_ids)} assignments")
        return assignment_ids
    
    def seed_conversations(self):
        """Seed AI chat conversations"""
        self.print_info("Seeding conversations...")
        
        conversation_data = []
        topics = [
            "Help with Calculus homework",
            "Explain photosynthesis",
            "World War II timeline",
            "Python programming basics",
            "Essay writing tips",
            "Chemistry lab questions",
            "Statistics concepts",
            "Spanish grammar help",
            "Physics problem solving",
            "Literature analysis"
        ]
        
        for user_id in self.user_ids[:7]:  # First 7 users have conversations
            for i in range(random.randint(2, 5)):  # 2-5 conversations per user
                conversation_data.append({
                    'user_id': user_id,
                    'title': random.choice(topics),
                    'created_at': self.get_random_date(1, 30)
                })
        
        conversation_ids = self.insert_many('conversations', conversation_data)
        self.print_success(f"Created {len(conversation_ids)} conversations")
        return conversation_ids
    
    def seed_messages(self, conversation_ids):
        """Seed conversation messages"""
        self.print_info("Seeding messages...")
        
        message_count = 0
        for conv_id in conversation_ids:
            # 3-8 messages per conversation
            num_messages = random.randint(3, 8)
            
            for i in range(num_messages):
                role = 'user' if i % 2 == 0 else 'assistant'
                content = f"Sample {role} message in conversation {conv_id}"
                
                self.insert_one('messages', {
                    'conversation_id': conv_id,
                    'role': role,
                    'content': content,
                    'created_at': self.get_random_date(1, 30)
                })
                message_count += 1
        
        self.print_success(f"Created {message_count} messages")
    
    def seed_study_materials(self):
        """Seed study materials"""
        self.print_info("Seeding study materials...")
        
        material_data = []
        subjects = ['Math', 'Science', 'English', 'History', 'Computer Science']
        
        for user_id in self.user_ids:
            for i in range(random.randint(8, 12)):  # 8-12 materials per user
                material_data.append({
                    'user_id': user_id,
                    'title': f'Study Material {i+1} - {random.choice(subjects)}',
                    'content': f'Comprehensive study content for {random.choice(subjects)}',
                    'subject': random.choice(subjects)
                })
        
        material_ids = self.insert_many('study_materials', material_data)
        self.print_success(f"Created {len(material_ids)} study materials")
        return material_ids
    
    def seed_notes(self, class_ids):
        """Seed AI-generated notes"""
        self.print_info("Seeding AI notes...")
        
        note_data = []
        for user_id in self.user_ids:
            for class_id in random.sample(class_ids, min(5, len(class_ids))):
                for i in range(random.randint(2, 4)):
                    note_data.append({
                        'user_id': user_id,
                        'class_id': class_id,
                        'title': f'Notes - Chapter {i+1}',
                        'content': f'AI-generated study notes for chapter {i+1}',
                        'source_type': random.choice(['lecture', 'textbook', 'recording'])
                    })
        
        note_ids = self.insert_many('ai_notes', note_data)
        self.print_success(f"Created {len(note_ids)} AI notes")
        return note_ids
    
    def seed_flashcard_sets(self, class_ids):
        """Seed flashcard sets"""
        self.print_info("Seeding flashcard sets...")
        
        set_data = []
        for user_id in self.user_ids:
            for class_id in random.sample(class_ids, min(3, len(class_ids))):
                for i in range(random.randint(1, 3)):
                    set_data.append({
                        'user_id': user_id,
                        'class_id': class_id,
                        'title': f'Flashcards Set {i+1}',
                        'description': f'Study flashcards for key concepts'
                    })
        
        set_ids = self.insert_many('flashcard_sets', set_data)
        self.print_success(f"Created {len(set_ids)} flashcard sets")
        return set_ids
    
    def seed_flashcards(self, flashcard_set_ids):
        """Seed individual flashcards"""
        self.print_info("Seeding flashcards...")
        
        flashcard_count = 0
        for set_id in flashcard_set_ids:
            # 10-20 flashcards per set
            num_cards = random.randint(10, 20)
            
            for i in range(num_cards):
                self.insert_one('flashcards', {
                    'set_id': set_id,
                    'front': f'Question {i+1}: What is...?',
                    'back': f'Answer: The explanation for question {i+1}',
                    'card_order': i
                })
                flashcard_count += 1
        
        self.print_success(f"Created {flashcard_count} flashcards")
    
    def seed_practice_tests(self, class_ids):
        """Seed practice tests"""
        self.print_info("Seeding practice tests...")
        
        test_data = []
        for user_id in self.user_ids:
            for class_id in random.sample(class_ids, min(2, len(class_ids))):
                test_data.append({
                    'user_id': user_id,
                    'class_id': class_id,
                    'title': f'Practice Test - Midterm',
                    'description': 'Comprehensive practice test',
                    'difficulty': random.choice(['easy', 'medium', 'hard'])
                })
        
        test_ids = self.insert_many('practice_tests', test_data)
        self.print_success(f"Created {len(test_ids)} practice tests")
        return test_ids
    
    def seed_connections(self):
        """Seed user connections (friendships)"""
        self.print_info("Seeding user connections...")
        
        connection_count = 0
        for user_id in self.user_ids:
            # Each user has 2-5 connections
            num_connections = random.randint(2, 5)
            potential_friends = [uid for uid in self.user_ids if uid != user_id]
            friends = random.sample(potential_friends, min(num_connections, len(potential_friends)))
            
            for friend_id in friends:
                # Avoid duplicate connections
                existing = self.execute_query(
                    "SELECT id FROM user_connections WHERE (user_id = %s AND connected_user_id = %s) OR (user_id = %s AND connected_user_id = %s)",
                    (user_id, friend_id, friend_id, user_id),
                    fetch=True
                )
                
                if not existing:
                    self.insert_one('user_connections', {
                        'user_id': user_id,
                        'connected_user_id': friend_id,
                        'status': 'accepted',
                        'created_at': self.get_random_date(5, 60)
                    })
                    connection_count += 1
        
        self.print_success(f"Created {connection_count} user connections")
    
    def seed_groups(self):
        """Seed study groups"""
        self.print_info("Seeding study groups...")
        
        group_names = [
            "Calculus Study Group",
            "Biology Lab Partners",
            "History Essay Circle",
            "Computer Science Coders",
            "Physics Problem Solvers",
            "Chemistry Study Squad",
            "Spanish Language Learners",
            "Literature Book Club",
            "Economics Discussion Group",
            "Psychology Study Team"
        ]
        
        group_data = []
        for i, name in enumerate(group_names):
            creator_id = self.user_ids[i % len(self.user_ids)]
            group_data.append({
                'name': name,
                'description': f'Collaborative study group for {name.split()[0]}',
                'created_by': creator_id,
                'is_public': random.choice([True, True, False])  # 66% public
            })
        
        group_ids = self.insert_many('study_groups', group_data)
        self.print_success(f"Created {len(group_ids)} study groups")
        return group_ids
    
    def seed_group_members(self, group_ids):
        """Seed group memberships"""
        self.print_info("Seeding group members...")
        
        member_count = 0
        for group_id in group_ids:
            # 3-7 members per group
            num_members = random.randint(3, 7)
            members = random.sample(self.user_ids, min(num_members, len(self.user_ids)))
            
            for user_id in members:
                self.insert_one('group_members', {
                    'group_id': group_id,
                    'user_id': user_id,
                    'role': 'member' if user_id != members[0] else 'admin',
                    'joined_at': self.get_random_date(5, 30)
                })
                member_count += 1
        
        self.print_success(f"Created {member_count} group members")
    
    def seed_shared_content(self, note_ids, flashcard_set_ids):
        """Seed shared content"""
        self.print_info("Seeding shared content...")
        
        shared_count = 0
        
        # Share some notes
        for note_id in random.sample(note_ids, min(20, len(note_ids))):
            shared_with = random.sample(self.user_ids, random.randint(1, 3))
            for user_id in shared_with:
                self.insert_one('shared_content', {
                    'content_type': 'note',
                    'content_id': note_id,
                    'shared_by': random.choice(self.user_ids),
                    'shared_with': user_id,
                    'permission': random.choice(['view', 'edit'])
                })
                shared_count += 1
        
        self.print_success(f"Created {shared_count} shared content items")
    
    def seed_achievements(self):
        """Seed achievement definitions"""
        self.print_info("Seeding achievements...")
        
        achievement_data = []
        for achievement in SeedDataGenerator.ACHIEVEMENT_TYPES:
            achievement_data.append({
                'name': achievement,
                'description': f'Earned by: {achievement.lower()}',
                'icon': 'trophy',
                'points': random.randint(10, 100)
            })
        
        self.insert_many('achievements', achievement_data)
        self.print_success(f"Created {len(achievement_data)} achievements")
    
    def seed_user_achievements(self):
        """Seed user achievements"""
        self.print_info("Seeding user achievements...")
        
        # Get all achievement IDs
        achievements = self.execute_query("SELECT id FROM achievements", fetch=True)
        achievement_ids = [a['id'] for a in achievements]
        
        achievement_count = 0
        for user_id in self.user_ids:
            # Each user has earned 2-8 achievements
            num_achievements = random.randint(2, 8)
            earned = random.sample(achievement_ids, min(num_achievements, len(achievement_ids)))
            
            for achievement_id in earned:
                self.insert_one('user_achievements', {
                    'user_id': user_id,
                    'achievement_id': achievement_id,
                    'earned_at': self.get_random_date(5, 90)
                })
                achievement_count += 1
        
        self.print_success(f"Created {achievement_count} user achievements")
    
    def seed_points(self):
        """Seed user points"""
        self.print_info("Seeding user points...")
        
        for user_id in self.user_ids:
            # 10-30 point events per user
            num_events = random.randint(10, 30)
            
            for i in range(num_events):
                points = random.choice([5, 10, 15, 20, 25, 50])
                self.insert_one('user_points', {
                    'user_id': user_id,
                    'points': points,
                    'activity_type': random.choice(['study_session', 'flashcard_review', 'assignment_complete', 'help_friend']),
                    'description': f'Earned {points} points',
                    'earned_at': self.get_random_date(1, 90)
                })
        
        self.print_success(f"Seeded points for {len(self.user_ids)} users")
    
    def seed_leaderboard_entries(self):
        """Seed leaderboard entries"""
        self.print_info("Seeding leaderboard entries...")
        
        # Calculate total points for each user
        for user_id in self.user_ids:
            result = self.execute_query(
                "SELECT COALESCE(SUM(points), 0) as total FROM user_points WHERE user_id = %s",
                (user_id,),
                fetch=True
            )
            total_points = result[0]['total']
            
            self.insert_one('leaderboard_entries', {
                'user_id': user_id,
                'total_points': total_points,
                'rank': 0,  # Will be calculated by application
                'period': 'all_time'
            })
        
        self.print_success(f"Created {len(self.user_ids)} leaderboard entries")
    
    def seed_study_sessions(self):
        """Seed study sessions"""
        self.print_info("Seeding study sessions...")
        
        session_count = 0
        for user_id in self.user_ids:
            # 20-40 study sessions per user
            num_sessions = random.randint(20, 40)
            
            for i in range(num_sessions):
                duration = random.randint(15, 180)  # 15 minutes to 3 hours
                started_at = self.get_random_date(1, 90)
                ended_at = started_at + timedelta(minutes=duration)
                
                self.insert_one('study_sessions', {
                    'user_id': user_id,
                    'duration_minutes': duration,
                    'focus_score': random.randint(60, 100),
                    'started_at': started_at,
                    'ended_at': ended_at
                })
                session_count += 1
        
        self.print_success(f"Created {session_count} study sessions")
    
    def seed_goals(self):
        """Seed study goals"""
        self.print_info("Seeding study goals...")
        
        goal_count = 0
        for user_id in self.user_ids:
            # 2-5 goals per user
            num_goals = random.randint(2, 5)
            
            for i in range(num_goals):
                target_date = self.get_random_future_date(7, 60)
                
                self.insert_one('study_goals', {
                    'user_id': user_id,
                    'title': f'Study Goal {i+1}',
                    'description': 'Complete study objectives',
                    'target_date': target_date,
                    'target_hours': random.randint(10, 50),
                    'status': random.choice(['active', 'active', 'completed']),
                    'current_progress': random.randint(0, 100)
                })
                goal_count += 1
        
        self.print_success(f"Created {goal_count} study goals")
    
    def seed_notifications(self):
        """Seed notifications"""
        self.print_info("Seeding notifications...")
        
        notification_types = [
            'assignment_due', 'friend_request', 'achievement_earned',
            'group_invitation', 'shared_content', 'study_reminder'
        ]
        
        notification_count = 0
        for user_id in self.user_ids:
            # 5-10 notifications per user
            num_notifications = random.randint(5, 10)
            
            for i in range(num_notifications):
                self.insert_one('notifications', {
                    'user_id': user_id,
                    'type': random.choice(notification_types),
                    'title': f'Notification {i+1}',
                    'message': 'You have a new notification',
                    'is_read': random.choice([True, False]),
                    'created_at': self.get_random_date(1, 14)
                })
                notification_count += 1
        
        self.print_success(f"Created {notification_count} notifications")
    
    def seed_user_messages(self):
        """Seed user-to-user messages"""
        self.print_info("Seeding user messages...")
        
        message_count = 0
        for sender_id in self.user_ids[:7]:  # First 7 users send messages
            # Get their connections
            connections = self.execute_query(
                "SELECT connected_user_id FROM user_connections WHERE user_id = %s AND status = 'accepted'",
                (sender_id,),
                fetch=True
            )
            
            if connections:
                for conn in random.sample(connections, min(2, len(connections))):
                    receiver_id = conn['connected_user_id']
                    
                    # 2-5 messages in conversation
                    for i in range(random.randint(2, 5)):
                        self.insert_one('user_messages', {
                            'sender_id': sender_id,
                            'receiver_id': receiver_id,
                            'content': f'Message {i+1} from user {sender_id}',
                            'is_read': random.choice([True, False]),
                            'sent_at': self.get_random_date(1, 30)
                        })
                        message_count += 1
        
        self.print_success(f"Created {message_count} user messages")
    
    def print_summary(self):
        """Print summary of seeded data"""
        print("\n📊 SEEDED DATA SUMMARY:")
        print("-" * 80)
        
        tables = [
            'users', 'classes', 'assignments', 'conversations', 'messages',
            'study_materials', 'ai_notes', 'flashcard_sets', 'flashcards',
            'practice_tests', 'user_connections', 'study_groups', 'group_members',
            'shared_content', 'achievements', 'user_achievements', 'user_points',
            'leaderboard_entries', 'study_sessions', 'study_goals',
            'notifications', 'user_messages'
        ]
        
        for table in tables:
            if self.table_exists(table):
                result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}", fetch=True)
                count = result[0]['count']
                if count > 0:
                    print(f"  {table:.<30} {count:>6} records")
        
        print("-" * 80)
        print("\n✅ All test users have password: password123")
        print("✅ Test user: testuser@test.com")
        print("✅ Database ready for testing and development!")
        print()


def main():
    """Main function"""
    import sys
    
    # Parse command line arguments
    clear_existing = '--clear' in sys.argv
    
    with MasterSeeder() as seeder:
        if clear_existing:
            print("\n⚠️  WARNING: This will delete ALL existing data!")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted.")
                return
        
        try:
            seeder.seed_all(clear_existing=clear_existing)
        except Exception as e:
            print(f"\n❌ Error during seeding: {e}")
            import traceback
            traceback.print_exc()
            return 1
        
        return 0


if __name__ == "__main__":
    exit(main())
