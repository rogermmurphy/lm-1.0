# Little Monster GPA - Database Seed Data

Comprehensive seed data scripts for populating the Little Monster GPA database with realistic test data.

## Overview

The seed data system provides realistic test data across all 12 database schemas, enabling thorough testing and development of all platform features.

## Files

### Core Scripts
- **`base_seeder.py`** - Base seeder class with database utilities
- **`seed_users.py`** - User account seeding (standalone)
- **`seed_all.py`** - Master script that seeds ALL tables (recommended)

### What Gets Seeded

The `seed_all.py` script populates the following data:

#### Phase 1: Core Data (10 users)
- 10 test user accounts with varied profiles
- All users have password: `password123`
- Test user: `testuser@test.com`

#### Phase 2: Academic Data
- 15 classes across different subjects
- 50 assignments (mix of pending, in-progress, completed)
- Realistic due dates (past, present, future)

#### Phase 3: Communication Data
- ~30 AI chat conversations
- 100+ conversation messages
- 100 study materials

#### Phase 4: Study Tools Data
- 200+ AI-generated notes
- 100+ flashcard sets
- 1500+ individual flashcards
- 20+ practice tests

#### Phase 5: Social Data
- 50+ user connections (friendships)
- 10 study groups
- 50+ group memberships
- 20+ shared content items

#### Phase 6: Gamification Data
- 13 achievement types
- 50+ user achievements
- 300+ point events
- 10 leaderboard entries

#### Phase 7: Analytics Data
- 300+ study sessions with realistic durations
- 30+ study goals

#### Phase 8: Notifications Data
- 70+ notifications
- 50+ user-to-user messages

## Usage

### Prerequisites

1. Ensure database schemas are deployed:
   ```bash
   cd database/scripts
   python deploy-schema.py
   ```

2. Set environment variables (or use .env file):
   ```bash
   DB_HOST=aws-0-us-east-1.pooler.supabase.com
   DB_PORT=6543
   DB_NAME=postgres
   DB_USER=postgres.ynrfvvqxqxqxqxqx
   DB_PASSWORD=your_password_here
   ```

### Seed All Data (Recommended)

Seed all tables with comprehensive test data:

```bash
cd database/seeds
python seed_all.py
```

This will:
- Keep existing data by default
- Add new test data across all tables
- Show progress for each phase
- Display summary at completion

### Clear and Reseed (Caution!)

To clear all existing data and start fresh:

```bash
cd database/seeds
python seed_all.py --clear
```

⚠️ **WARNING**: This will DELETE ALL existing data! Use with caution.

### Seed Only Users

To seed only user accounts:

```bash
cd database/seeds
python seed_users.py
```

Clear users first:
```bash
python seed_users.py --clear
```

## Test Credentials

After seeding, you can log in with any of these accounts:

### Primary Test Account
- **Email**: `testuser@test.com`
- **Password**: `password123`
- **User ID**: Varies (check output)

### All Test Users
All generated users have:
- **Password**: `password123`
- **Email format**: `firstname.lastname@test.com`
- **Username format**: `firstnamelastname##`

Example users:
- `emma.smith@test.com`
- `liam.johnson@test.com`
- `olivia.williams@test.com`
- etc.

## Seed Data Statistics

### Typical Seed Results

```
users............................ 10 records
classes.......................... 15 records
assignments...................... 50 records
conversations.................... 30 records
messages........................ 150 records
study_materials................. 100 records
ai_notes........................ 200 records
flashcard_sets.................. 100 records
flashcards..................... 1500 records
practice_tests................... 20 records
user_connections................. 50 records
study_groups..................... 10 records
group_members.................... 50 records
shared_content................... 20 records
achievements..................... 13 records
user_achievements................ 50 records
user_points..................... 300 records
leaderboard_entries.............. 10 records
study_sessions.................. 300 records
study_goals...................... 30 records
notifications.................... 70 records
user_messages.................... 50 records
```

**Total**: ~3,000+ records across 22 tables

## Data Characteristics

### Realistic Patterns

1. **Temporal Distribution**
   - Past data: 1-90 days ago
   - Current data: Today
   - Future data: 1-90 days ahead

2. **User Activity Levels**
   - Active users: 70%
   - Verified users: 75%
   - Average connections per user: 2-5

3. **Academic Data**
   - Completed assignments: 30%
   - In-progress assignments: 40%
   - Pending assignments: 30%

4. **Study Sessions**
   - Duration: 15 minutes to 3 hours
   - Focus score: 60-100%
   - Frequency: 20-40 per user

5. **Gamification**
   - Points range: 10-100 per activity
   - Achievements: 2-8 per user
   - Active leaderboard competition

### Data Relationships

All seed data maintains referential integrity:
- Users → Classes → Assignments
- Users → Conversations → Messages
- Users → Notes → Shared Content
- Users → Groups → Members
- Users → Points → Achievements → Leaderboard

## Extending Seed Data

### Adding New Seeders

To add seeding for new tables:

1. Create a new method in `seed_all.py`:
   ```python
   def seed_my_table(self):
       """Seed my_table"""
       self.print_info("Seeding my_table...")
       
       data = []
       for user_id in self.user_ids:
           data.append({
               'user_id': user_id,
               'field': 'value'
           })
       
       ids = self.insert_many('my_table', data)
       self.print_success(f"Created {len(ids)} records")
       return ids
   ```

2. Call it in `seed_all()` at the appropriate phase

3. Add table to `print_summary()` table list

### Customizing Seed Data

Modify these constants in `base_seeder.py`:

```python
class SeedDataGenerator:
    FIRST_NAMES = [...]  # Add more names
    LAST_NAMES = [...]   # Add more names
    SUBJECTS = [...]     # Add more subjects
    ACHIEVEMENT_TYPES = [...]  # Add achievements
```

## Troubleshooting

### Connection Issues

**Error**: `Unable to connect to database`

Solution:
1. Check environment variables
2. Verify database is accessible
3. Confirm credentials are correct
4. Check firewall/security groups

### Schema Not Found

**Error**: `Table 'users' does not exist`

Solution:
```bash
cd database/scripts
python deploy-schema.py
```

### Duplicate Key Errors

**Error**: `duplicate key value violates unique constraint`

Solution: Use `--clear` flag to reset data:
```bash
python seed_all.py --clear
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'psycopg2'`

Solution:
```bash
pip install psycopg2-binary
```

## Development Tips

### Testing Individual Seeders

Test the base seeder:
```bash
python base_seeder.py
```

Test user seeder:
```bash
python seed_users.py
```

### Incremental Seeding

The scripts are designed to work incrementally:
- Running without `--clear` adds to existing data
- Duplicate users are detected and reused
- Foreign key relationships are maintained

### Performance

Seeding ~3,000 records typically takes:
- Local database: 30-60 seconds
- Remote database: 1-2 minutes

## Best Practices

1. **Development**: Run `seed_all.py` once to set up test environment
2. **Testing**: Use `--clear` before major test runs for clean slate
3. **CI/CD**: Include seeding in automated test pipelines
4. **Staging**: Seed staging environments before deployment
5. **Production**: NEVER run seeders on production databases!

## Integration with Services

After seeding, you can test all services:

### Authentication Service (8001)
```bash
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@test.com","password":"password123"}'
```

### Class Management Service (8006)
```bash
curl http://localhost/api/classes \
  -H "Authorization: Bearer <token>"
```

### AI Chat Service (8005)
```bash
curl http://localhost/api/chat/conversations \
  -H "Authorization: Bearer <token>"
```

## Support

For issues or questions:
1. Check logs: Seeder prints detailed progress
2. Verify schema deployment
3. Check database connectivity
4. Review environment variables

## License

Part of Little Monster GPA project.

## Changelog

### Version 1.0 (2025-11-02)
- Initial release
- Comprehensive seeding for all 12 schemas
- 22 tables, ~3,000+ records
- Realistic test data patterns
- Full relationship integrity
