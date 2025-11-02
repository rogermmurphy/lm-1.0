This directory contains the PostgreSQL database schemas for the Little Monster platform, extracted and consolidated from validated POCs.

## Schema Files

### Individual Schemas (for reference and incremental deployment)

1. **001_authentication.sql** - User accounts, OAuth, JWT tokens
   - Extracted from: POC 12
   - Tables: users, oauth_connections, refresh_tokens, password_reset_tokens
   - Status: ✅ Tested and validated

2. **002_transcription.sql** - Speech-to-text services
   - Extracted from: POC 09
   - Tables: transcription_jobs, transcriptions
   - Status: ✅ Tested and validated

3. **003_async_jobs.sql** - Background job queue
   - Extracted from: POC 08
   - Tables: jobs
   - Status: ✅ Tested and validated

4. **004_content.sql** - Content management
   - Tables: tts_audio_files, recordings, study_materials
   - Status: ✅ Designed for production

5. **005_interactions.sql** - Conversations and messages
   - Tables: conversations, messages
   - Status: ✅ Designed for production

### Consolidated Schema

- **master-schema.sql** - Complete consolidated schema
  - All tables from individual schemas
  - All indexes and triggers
  - Ready for production deployment
  - Use this for initial database setup

## Database Statistics

- **Total Tables**: 12
- **Total Indexes**: 30+
- **Total Triggers**: 4
- **Foreign Key Constraints**: 15+

## Tables Overview

### Authentication (4 tables)
- `users` - User accounts (email, password, OAuth)
- `oauth_connections` - OAuth provider links
- `refresh_tokens` - JWT refresh tokens
- `password_reset_tokens` - Password reset tokens

### Content (3 tables)
- `transcriptions` - Completed transcriptions
- `tts_audio_files` - Generated speech audio
- `recordings` - User recordings

### Jobs (2 tables)
- `transcription_jobs` - STT job queue
- `jobs` - General async job queue

### Knowledge (1 table)
- `study_materials` - RAG study materials

### Interactions (2 tables)
- `conversations` - Chat sessions
- `messages` - Chat messages

## Deployment

### Option 1: Master Schema (Recommended)
```bash
# Deploy complete schema at once
psql -U postgres -d littlemonster -f master-schema.sql
```

### Option 2: Incremental Deployment
```bash
# Deploy schemas one at a time
psql -U postgres -d littlemonster -f 001_authentication.sql
psql -U postgres -d littlemonster -f 002_transcription.sql
psql -U postgres -d littlemonster -f 003_async_jobs.sql
psql -U postgres -d littlemonster -f 004_content.sql
psql -U postgres -d littlemonster -f 005_interactions.sql
```

### Option 3: Using Docker
```bash
# Copy schema into running container
docker cp master-schema.sql postgres-container:/tmp/
docker exec -it postgres-container psql -U postgres -d littlemonster -f /tmp/master-schema.sql
```

## Key Features

### Automatic Timestamps
- `created_at` - Auto-set on insert
- `updated_at` - Auto-updated on modification (via triggers)

### Cascading Deletes
- User deletion cascades to all related data
- Conversation deletion cascades to messages
- Job deletion handled appropriately

### Indexes for Performance
- All foreign keys indexed
- Status fields indexed (for job queues)
- Created_at fields indexed (for time-based queries)
- Composite indexes for common query patterns

### Data Integrity
- Foreign key constraints
- Unique constraints (emails, tokens)
- Check constraints (token expiry dates)
- NOT NULL constraints on critical fields

## Migration Path

For future schema changes, use Alembic migrations (see `database/migrations/`).

## Validation

All schemas extracted from POCs that passed comprehensive testing:
- POC 12: 10/10 authentication tests passed
- POC 09: Successfully transcribed 5-minute audio in <30s
- POC 08: Async job processing validated

## Environment Variables Required

```env
DATABASE_URL=postgresql://user:password@localhost:5432/littlemonster
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=littlemonster
```

## Next Steps

1. ✅ Schemas created and documented
2. ⏳ Set up Alembic for migrations
3. ⏳ Create seed data for testing
4. ⏳ Deploy to development database
5. ⏳ Validate with service integration tests
