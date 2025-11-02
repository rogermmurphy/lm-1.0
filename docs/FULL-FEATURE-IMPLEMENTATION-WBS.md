# Little Monster (LM) - Full Feature Implementation Plan
## Work Breakdown Structure for Complete Educational Platform

**Document Version**: 1.0  
**Created**: November 2, 2025  
**Author**: Development Team  
**Status**: Planning Phase  

---

## Executive Summary

This Work Breakdown Structure (WBS) provides a comprehensive roadmap to evolve the current minimal backend (authentication, chat, materials, TTS, transcription) into the complete Little Monster educational platform envisioned in the original project plan. The current system has 12 database tables across 5 schemas. The full vision requires 16+ tables with extensive new features across class management, content capture, study tools, and social features.

### Current State (Phase 1 Complete - November 2025)
**✅ Implemented Features:**
- User authentication (login/register)
- Basic chat with AI (Bedrock Claude Sonnet 4)
- Study materials upload/retrieval
- Text-to-Speech (Azure)
- Speech-to-Text transcription (Whisper)
- Docker Compose deployment
- 12 database tables (users, tokens, audio files, transcripts, jobs, materials, notes, conversations, messages)

**Current Database Schema:**
- `001_authentication.sql` - users, refresh_tokens
- `002_transcription.sql` - audio_files, transcripts, transcription_jobs
- `003_async_jobs.sql` - async_jobs
- `004_content.sql` - study_materials, study_notes
- `005_interactions.sql` - conversations, messages

**Current UI (Next.js 14):**
- Login/Register pages
- Dashboard
- Chat page
- Materials page
- TTS page
- Transcribe page

### Target State (Full Platform Vision)
**🎯 Complete Feature Set:**
- Class management system
- Assignment tracking
- Schedule management
- Lecture recording & transcription
- Photo capture with OCR
- Textbook PDF processing
- AI-generated notes from recordings
- Test/quiz generation
- Flashcard creation
- Study planner with calendar
- Classmate connections
- Content sharing
- Gamification system
- Multi-platform support (Web, Mobile, Desktop)

---

## Part 1: Feature Inventory & Gap Analysis

### 1.1 Class Management Features (NOT IMPLEMENTED)

#### 1.1.1 Class CRUD Operations
**Status**: ❌ Not Implemented  
**Database Requirement**: New `classes` table  
**Description**: Students need to manage their academic classes

**Required Features:**
- Create new class with details (name, teacher, period, subject, color)
- View all classes in dashboard
- Edit class information
- Delete class (with cascade to related content)
- Track current grade and grade percentage
- Associate classes with specific subjects

**Database Schema Needed:**
```sql
CREATE TABLE classes (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(100) NOT NULL,
  teacher_name VARCHAR(100),
  period VARCHAR(20),
  color VARCHAR(20),
  subject VARCHAR(50),
  current_grade VARCHAR(5),
  grade_percent INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/classes` - Create class
- `GET /api/classes` - List user's classes
- `GET /api/classes/:id` - Get class details
- `PUT /api/classes/:id` - Update class
- `DELETE /api/classes/:id` - Delete class

**UI Components Needed:**
- ClassList component
- ClassCard component
- CreateClassModal component
- EditClassModal component
- ClassDashboard page

**Effort Estimate**: 2 weeks (Backend: 1 week, Frontend: 1 week)

#### 1.1.2 Class Dashboard & Analytics
**Status**: ❌ Not Implemented  
**Description**: Per-class view showing all related content and analytics

**Required Features:**
- Class overview with grade tracking
- Recent recordings for class
- Recent photos for class
- Upcoming assignments
- Study materials organized by class
- Class-specific chat conversations
- Performance analytics

**UI Components Needed:**
- ClassDashboardPage
- ClassAnalytics component
- ClassContentTimeline component
- GradeTracker component

**Effort Estimate**: 2 weeks

### 1.2 Assignment Management (NOT IMPLEMENTED)

#### 1.2.1 Assignment Tracking System
**Status**: ❌ Not Implemented  
**Database Requirement**: New `assignments` table

**Required Features:**
- Create assignments with due dates
- Link assignments to classes
- Track assignment status (pending, in-progress, completed)
- Set assignment types (homework, project, exam, quiz)
- Add descriptions and notes
- Due date reminders
- Completion tracking

**Database Schema Needed:**
```sql
CREATE TABLE assignments (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  type VARCHAR(50),
  description TEXT,
  due_date TIMESTAMP NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/assignments` - Create assignment
- `GET /api/assignments` - List assignments (with filters)
- `GET /api/assignments/:id` - Get assignment details
- `PUT /api/assignments/:id` - Update assignment
- `DELETE /api/assignments/:id` - Delete assignment
- `PATCH /api/assignments/:id/status` - Update status

**UI Components Needed:**
- AssignmentList component
- AssignmentCard component
- CreateAssignmentModal component
- AssignmentCalendarView component
- AssignmentFilters component

**Effort Estimate**: 2 weeks

### 1.3 Content Capture Features (PARTIALLY IMPLEMENTED)

#### 1.3.1 Audio Recording & Transcription
**Status**: ⚠️ Partially Implemented  
**Current**: Basic transcription service exists  
**Missing**: Recording UI, class association, vector embeddings

**Required Enhancements:**
- In-browser audio recording interface
- Associate recordings with specific classes
- Auto-transcription on upload
- Vector embeddings for semantic search
- Playback controls with transcript sync
- Edit transcript capability
- Generate notes from transcripts

**Database Schema Enhancement:**
```sql
CREATE TABLE audio_recordings (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  file_url TEXT NOT NULL,
  duration_seconds INTEGER,
  transcript_text TEXT,
  transcript_status VARCHAR(20),
  vector_id VARCHAR(100),  -- For semantic search
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/recordings` - Upload recording
- `GET /api/recordings` - List recordings
- `GET /api/recordings/:id` - Get recording details
- `POST /api/recordings/:id/transcribe` - Trigger transcription
- `PUT /api/recordings/:id/transcript` - Update transcript
- `POST /api/recordings/:id/generate-notes` - AI note generation

**UI Components Needed:**
- AudioRecorder component
- RecordingsList component
- TranscriptViewer component
- AudioPlayer component with sync
- RecordingUploader component

**Effort Estimate**: 3 weeks

#### 1.3.2 Photo Capture with OCR
**Status**: ❌ Not Implemented  
**Database Requirement**: New `photos` table

**Required Features:**
- Camera integration for capturing whiteboard/notes
- Photo upload from device
- OCR text extraction
- Associate photos with classes
- Vector embeddings for search
- Photo gallery view
- Edit extracted text

**Database Schema Needed:**
```sql
CREATE TABLE photos (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  image_url TEXT NOT NULL,
  extracted_text TEXT,
  extraction_status VARCHAR(20),
  vector_id VARCHAR(100),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**Technology Stack:**
- OCR: Tesseract.js or Google Cloud Vision API
- Image processing: Sharp
- Storage: S3 or similar

**API Endpoints Needed:**
- `POST /api/photos` - Upload photo
- `GET /api/photos` - List photos
- `GET /api/photos/:id` - Get photo details
- `POST /api/photos/:id/extract-text` - Trigger OCR
- `PUT /api/photos/:id/text` - Update extracted text

**UI Components Needed:**
- CameraCapture component
- PhotoUploader component
- PhotoGallery component
- PhotoViewer component
- ExtractedTextEditor component

**Effort Estimate**: 3 weeks

#### 1.3.3 Textbook PDF Processing
**Status**: ❌ Not Implemented  
**Database Requirement**: New `textbook_downloads` table

**Required Features:**
- PDF upload and storage
- PDF text extraction
- Chunking for vector embeddings
- Full-text search
- Page-by-page navigation
- Highlight and annotate
- Link to class

**Database Schema Needed:**
```sql
CREATE TABLE textbook_downloads (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  class_id UUID REFERENCES classes(id),
  title VARCHAR(200) NOT NULL,
  author VARCHAR(200),
  isbn VARCHAR(20),
  file_url TEXT NOT NULL,
  file_type VARCHAR(20),
  file_size_bytes INTEGER,
  page_count INTEGER,
  total_chunks INTEGER,
  embedding_status VARCHAR(20),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**Technology Stack:**
- PDF processing: pdf-parse or PyPDF2
- Vector DB: Chroma or Pinecone
- Chunking: LangChain text splitters

**API Endpoints Needed:**
- `POST /api/textbooks` - Upload textbook
- `GET /api/textbooks` - List textbooks
- `GET /api/textbooks/:id` - Get textbook details
- `POST /api/textbooks/:id/process` - Process for embeddings
- `GET /api/textbooks/:id/pages/:page` - Get specific page

**UI Components Needed:**
- TextbookUploader component
- TextbookLibrary component
- PDFViewer component
- TextbookSearch component

**Effort Estimate**: 4 weeks

### 1.4 AI-Generated Study Tools (NOT IMPLEMENTED)

#### 1.4.1 AI Note Generation
**Status**: ❌ Not Implemented  
**Database Requirement**: Enhance `study_notes` table, add `note_sources` table

**Required Features:**
- Generate notes from audio transcripts
- Generate notes from photos/OCR text
- Generate notes from textbook sections
- Combine multiple sources into comprehensive notes
- Edit and refine AI-generated notes
- Track note sources
- Export notes (PDF, Markdown)

**Database Schema Enhancement:**
```sql
-- Enhance existing study_notes table
ALTER TABLE study_notes ADD COLUMN is_ai_generated BOOLEAN DEFAULT false;
ALTER TABLE study_notes ADD COLUMN vector_id VARCHAR(100);

-- New table to track note sources
CREATE TABLE note_sources (
  id UUID PRIMARY KEY,
  note_id UUID REFERENCES study_notes(id),
  source_type VARCHAR(50) NOT NULL,  -- 'recording', 'photo', 'textbook'
  source_id UUID NOT NULL,
  created_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/notes/generate` - Generate notes from sources
- `POST /api/notes/:id/refine` - Refine existing notes
- `GET /api/notes/:id/sources` - Get note sources
- `POST /api/notes/:id/export` - Export notes

**UI Components Needed:**
- NoteGenerator component
- SourceSelector component
- NoteEditor component (rich text)
- NoteExporter component

**Effort Estimate**: 3 weeks

#### 1.4.2 Test/Quiz Generation
**Status**: ❌ Not Implemented  
**Database Requirement**: New `generated_tests` and `test_questions` tables

**Required Features:**
- Generate tests from notes/transcripts
- Multiple question types (multiple choice, true/false, short answer)
- Difficulty levels
- Time limits
- Answer keys with explanations
- Practice mode
- Track test history

**Database Schema Needed:**
```sql
CREATE TABLE generated_tests (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  description TEXT,
  difficulty VARCHAR(20),
  question_count INTEGER DEFAULT 0,
  time_limit_minutes INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE test_questions (
  id UUID PRIMARY KEY,
  test_id UUID REFERENCES generated_tests(id),
  question_text TEXT NOT NULL,
  question_type VARCHAR(50),
  correct_answer TEXT,
  options JSONB,
  explanation TEXT,
  points INTEGER DEFAULT 1,
  order_index INTEGER,
  created_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/tests/generate` - Generate test
- `GET /api/tests` - List tests
- `GET /api/tests/:id` - Get test details
- `POST /api/tests/:id/take` - Start test session
- `POST /api/tests/:id/submit` - Submit answers

**UI Components Needed:**
- TestGenerator component
- TestList component
- TestTaker component
- TestResults component
- QuestionEditor component

**Effort Estimate**: 4 weeks

#### 1.4.3 Flashcard Generation
**Status**: ❌ Not Implemented  
**Database Requirement**: New `flashcard_decks` and `flashcards` tables

**Required Features:**
- Generate flashcards from notes
- Create custom flashcards
- Organize into decks
- Spaced repetition algorithm
- Study mode with flip animation
- Track mastery level
- Share decks

**Database Schema Needed:**
```sql
CREATE TABLE flashcard_decks (
  id UUID PRIMARY KEY,
  class_id UUID REFERENCES classes(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(200) NOT NULL,
  description TEXT,
  card_count INTEGER DEFAULT 0,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE flashcards (
  id UUID PRIMARY KEY,
  deck_id UUID REFERENCES flashcard_decks(id),
  front_text TEXT NOT NULL,
  back_text TEXT NOT NULL,
  order_index INTEGER,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/flashcards/generate` - Generate deck
- `GET /api/flashcards/decks` - List decks
- `POST /api/flashcards/decks` - Create deck
- `GET /api/flashcards/decks/:id` - Get deck
- `POST /api/flashcards/decks/:id/cards` - Add card
- `GET /api/flashcards/decks/:id/study` - Study session

**UI Components Needed:**
- FlashcardGenerator component
- DeckList component
- FlashcardStudy component
- FlashcardEditor component
- SpacedRepetitionTracker component

**Effort Estimate**: 3 weeks

### 1.5 Schedule & Planning Features (NOT IMPLEMENTED)

#### 1.5.1 Study Planner with Calendar
**Status**: ❌ Not Implemented  
**Database Requirement**: New `planner_events` table

**Required Features:**
- Calendar view (day, week, month)
- Create study sessions
- Link to assignments
- Recurring events
- Reminders/notifications
- Time blocking
- Integration with class schedule
- Progress tracking

**Database Schema Needed:**
```sql
CREATE TABLE planner_events (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  class_id UUID REFERENCES classes(id),
  assignment_id UUID REFERENCES assignments(id),
  title VARCHAR(200) NOT NULL,
  description TEXT,
  event_type VARCHAR(50),  -- 'study', 'assignment', 'exam', 'class'
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  is_recurring BOOLEAN DEFAULT false,
  recurrence_rule TEXT,
  is_completed BOOLEAN DEFAULT false,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/planner/events` - Create event
- `GET /api/planner/events` - List events (with date range)
- `PUT /api/planner/events/:id` - Update event
- `DELETE /api/planner/events/:id` - Delete event
- `PATCH /api/planner/events/:id/complete` - Mark complete

**UI Components Needed:**
- CalendarView component
- EventCreator component
- EventList component
- TimeBlocker component
- StudySessionPlanner component

**Effort Estimate**: 3 weeks

#### 1.5.2 Schedule Upload & Management
**Status**: ❌ Not Implemented

**Required Features:**
- Upload class schedule (CSV, image)
- Parse schedule automatically
- Manual schedule entry
- Recurring class times
- Room numbers
- Teacher contact info

**Effort Estimate**: 2 weeks

### 1.6 Social & Collaboration Features (NOT IMPLEMENTED)

#### 1.6.1 Classmate Connections
**Status**: ❌ Not Implemented  
**Database Requirement**: New `classmate_connections` table

**Required Features:**
- Find classmates by school/class
- Send connection requests
- Accept/reject requests
- View classmate profiles
- See shared classes
- Privacy controls

**Database Schema Needed:**
```sql
CREATE TABLE classmate_connections (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  classmate_user_id UUID REFERENCES users(id),
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP,
  UNIQUE(user_id, classmate_user_id)
);
```

**API Endpoints Needed:**
- `GET /api/classmates/search` - Search for classmates
- `POST /api/classmates/connect` - Send request
- `PUT /api/classmates/:id/accept` - Accept request
- `DELETE /api/classmates/:id` - Remove connection
- `GET /api/classmates` - List connections

**UI Components Needed:**
- ClassmateSearch component
- ConnectionRequests component
- ClassmateList component
- ClassmateProfile component

**Effort Estimate**: 2 weeks

#### 1.6.2 Content Sharing
**Status**: ❌ Not Implemented  
**Database Requirement**: New `shared_content` table

**Required Features:**
- Share notes with classmates
- Share flashcard decks
- Share study guides
- Permission controls
- Track who shared what
- Revoke sharing

**Database Schema Needed:**
```sql
CREATE TABLE shared_content (
  id UUID PRIMARY KEY,
  content_type VARCHAR(50) NOT NULL,
  content_id UUID NOT NULL,
  shared_by_user_id UUID REFERENCES users(id),
  shared_with_user_id UUID REFERENCES users(id),
  permissions VARCHAR(20) DEFAULT 'view',
  created_at TIMESTAMP
);
```

**API Endpoints Needed:**
- `POST /api/share` - Share content
- `GET /api/share/received` - Content shared with me
- `GET /api/share/sent` - Content I shared
- `DELETE /api/share/:id` - Revoke sharing

**UI Components Needed:**
- ShareModal component
- SharedContentList component
- PermissionSelector component

**Effort Estimate**: 2 weeks

#### 1.6.3 Study Groups
**Status**: ❌ Not Implemented

**Required Features:**
- Create study groups
- Invite classmates
- Group chat
- Shared resources
- Group study sessions
- Video calls (optional)

**Effort Estimate**: 4 weeks

### 1.7 Gamification Features (NOT IMPLEMENTED)

#### 1.7.1 Points & Currency System
**Status**: ❌ Not Implemented  
**Database Requirement**: New `user_points`, `achievements` tables

**Required Features:**
- Earn points for activities
- Daily streaks
- Level system
- Leaderboards
- Rewards/badges
- Point redemption

**Database Schema Needed:**
```sql
CREATE TABLE user_points (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  points INTEGER DEFAULT 0,
  level INTEGER DEFAULT 1,
  streak_days INTEGER DEFAULT 0,
  last_activity_date DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE achievements (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  achievement_type VARCHAR(50),
  achievement_name VARCHAR(100),
  earned_at TIMESTAMP
);
```

**Effort Estimate**: 3 weeks

#### 1.7.2 Educational Games
**Status**: ❌ Not Implemented

**Required Features:**
- Quiz games
- Memory games
- Timed challenges
- Multiplayer competitions
- Game leaderboards

**Effort Estimate**: 4 weeks

### 1.8 Advanced Chat Features (PARTIALLY IMPLEMENTED)

**Status**: ⚠️ Basic chat exists  
**Missing**: RAG with uploaded content, conversation history, class-specific chats

**Required Enhancements:**
- RAG integration with all uploaded content
- Search through recordings, notes, textbooks
- Class-specific chat contexts
- Conversation management
- Export conversations
- Voice input/output

**Effort Estimate**: 3 weeks

---

## Part 2: Database Migration Plan

### 2.1 Current Schema (12 Tables)
```
authentication (2 tables):
  - users
  - refresh_tokens

transcription (3 tables):
  - audio_files
  - transcripts
  - transcription_jobs

async_jobs (1 table):
  - async_jobs

content (2 tables):
  - study_materials
  - study_notes

interactions (2 tables):
  - conversations
  - messages
```

### 2.2 Target Schema (28+ Tables)

**New Schema Files Needed:**

#### `006_classes_assignments.sql` (4 tables)
- classes
- assignments
- planner_events
- class_schedules

#### `007_content_capture.sql` (3 tables)
- audio_recordings (enhanced from audio_files)
- photos
- textbook_downloads

#### `008_study_tools.sql` (6 tables)
- note_sources
- generated_tests
- test_questions
- flashcard_decks
- flashcards
- test_attempts

#### `009_social.sql` (3 tables)
- classmate_connections
- shared_content
- study_groups

#### `010_gamification.sql` (3 tables)
- user_points
- achievements
- leaderboards

### 2.3 Migration Strategy

**Phase 1: Core Extensions (Weeks 1-4)**
1. Deploy `006_classes_assignments.sql`
2. Migrate existing study_materials to link with classes
3. Test class CRUD operations

**Phase 2: Content Capture (Weeks 5-8)**
1. Deploy `007_content_capture.sql`
2. Enhance audio_files → audio_recordings
3. Add vector embedding support

**Phase 3: Study Tools (Weeks 9-12)**
1. Deploy `008_study_tools.sql`
2. Implement AI generation services
3. Test note/test/flashcard generation

**Phase 4: Social & Gamification (Weeks 13-16)**
1. Deploy `009_social.sql` and `010_gamification.sql`
2. Implement connection logic
3. Add points/achievements system

---

## Part 3: Backend API Endpoints Plan

### 3.1 New Service: Class Management Service

**Port**: 8005  
**Endpoints**: 15+

```
POST   /api/classes
GET    /api/classes
GET    /api/classes/:id
PUT    /api/classes/:id
DELETE /api/classes/:id
GET    /api/classes/:id/dashboard
GET    /api/classes/:id/analytics

POST   /api/assignments
GET    /api/assignments
GET    /api/assignments/:id
PUT    /api/assignments/:id
DELETE /api/assignments/:id
PATCH  /api/assignments/:id/status
GET    /api/assignments/upcoming
```

### 3.2 New Service: Content Capture Service

**Port**: 8006  
**Endpoints**: 20+

```
# Audio Recordings
POST   /api/recordings
GET    /api/recordings
GET    /api/recordings/:id
POST   /api/recordings/:id/transcribe
PUT    /api/recordings/:id/transcript
POST   /api/recordings/:id/generate-notes

# Photos
POST   /api/photos
GET    /api/photos
GET    /api/photos/:id
POST   /api/photos/:id/extract-text
PUT    /api/photos/:id/text

# Textbooks
POST   /api/textbooks
GET    /api/textbooks
GET    /api/textbooks/:id
POST   /api/textbooks/:id/process
GET    /api/textbooks/:id/pages/:page
GET    /api/textbooks/:id/search
```

### 3.3 New Service: Study Tools Service

**Port**: 8007  
**Endpoints**: 25+

```
# Notes
POST   /api/notes/generate
POST   /api/notes/:id/refine
GET    /api/notes/:id/sources
POST   /api/notes/:id/export

# Tests
POST   /api/tests/generate
GET    /api/tests
GET    /api/tests/:id
POST   /api/tests/:id/take
POST   /api/tests/:id/submit
GET    /api/tests/:id/results

# Flashcards
POST   /api/flashcards/generate
GET    /api/flashcards/decks
POST   /api/flashcards/decks
GET    /api/flashcards/decks/:id
POST   /api/flashcards/decks/:id/cards
GET    /api/flashcards/decks/:id/study
POST   /api/flashcards/decks/:id/cards/:cardId/review
```

### 3.4 New Service: Planner Service

**Port**: 8008  
**Endpoints**: 10+

```
POST   /api/planner/events
GET    /api/planner/events
GET    /api/planner/events/:id
PUT    /api/planner/events/:id
DELETE /api/planner/events/:id
PATCH  /api/planner/events/:id/complete
GET    /api/planner/calendar
POST   /api/planner/schedule/upload
```

### 3.5 New Service: Social Service

**Port**: 8009  
**Endpoints**: 15+

```
# Classmates
GET    /api/classmates/search
POST   /api/classmates/connect
PUT    /api/classmates/:id/accept
DELETE /api/classmates/:id
GET    /api/classmates

# Sharing
POST   /api/share
GET    /api/share/received
GET    /api/share/sent
DELETE /api/share/:id

# Study Groups
POST   /api/groups
GET    /api/groups
GET    /api/groups/:id
POST   /api/groups/:id/invite
```

### 3.6 Enhanced Service: LLM Agent Service

**Current Port**: 8002  
**New Endpoints**: 10+

```
# Enhanced RAG
POST   /api/chat/rag-query
GET    /api/chat/search-content
POST   /api/chat/generate-notes
POST   /api/chat/generate-test
POST   /api/chat/generate-flashcards
POST   /api/chat/summarize
POST   /api/chat/explain
```

---

## Part 4: Frontend Components Plan

### 4.1 New Pages (Next.js App Router)

```
app/
├── dashboard/
│   ├── classes/
│   │   ├── page.tsx                    # Classes list
│   │   ├── [id]/
│   │   │   ├── page.tsx                # Class dashboard
│   │   │   ├── assignments/page.tsx    # Class assignments
│   │   │   ├── recordings/page.tsx     # Class recordings
│   │   │   ├── photos/page.tsx         # Class photos
│   │   │   └── analytics/page.tsx      # Class analytics
│   ├── assignments/
│   │   ├── page.tsx                    # All assignments
│   │   └── [id]/page.tsx               # Assignment details
│   ├── recordings/
│   │   ├── page.tsx                    # All recordings
│   │   ├── record/page.tsx             # Record new
│   │   └── [id]/page.tsx               # Recording details
│   ├── photos/
│   │   ├── page.tsx                    # Photo gallery
│   │   ├── capture/page.tsx            # Capture new
│   │   └── [id]/page.tsx               # Photo details
│   ├── textbooks/
│   │   ├── page.tsx                    # Textbook library
│   │   └── [id]/page.tsx               # Textbook viewer
│   ├── notes/
│   │   ├── page.tsx                    # Notes list
│   │   ├── generate/page.tsx           # Generate notes
│   │   └── [id]/page.tsx               # Note editor
│   ├── tests/
│   │   ├── page.tsx                    # Tests list
│   │   ├── generate/page.tsx           # Generate test
│   │   ├── [id]/page.tsx               # Test details
│   │   └── [id]/take/page.tsx          # Take test
│   ├── flashcards/
│   │   ├── page.tsx                    # Decks list
│   │   ├── [id]/page.tsx               # Deck details
│   │   └── [id]/study/page.tsx         # Study mode
│   ├── planner/
│   │   └── page.tsx                    # Calendar planner
│   ├── classmates/
│   │   ├── page.tsx                    # Classmates list
│   │   ├── search/page.tsx             # Find classmates
│   │   └── [id]/page.tsx               # Classmate profile
│   └── profile/
│       ├── page.tsx                    # User profile
│       └── achievements/page.tsx       # Achievements
```

### 4.2 New Component Library (50+ Components)

**Class Management (8 components):**
- ClassList
- ClassCard
- CreateClassModal
- EditClassModal
- ClassDashboard
- ClassAnalytics
- GradeTracker
- ClassSelector

**Assignment Management (6 components):**
- AssignmentList
- AssignmentCard
- CreateAssignmentModal
- AssignmentCalendarView
- AssignmentFilters
- AssignmentStatusBadge

**Content Capture (12 components):**
- AudioRecorder
- RecordingsList
- TranscriptViewer
- AudioPlayer
- CameraCapture
- PhotoUploader
- PhotoGallery
- PhotoViewer
- ExtractedTextEditor
- TextbookUploader
- TextbookLibrary
- PDFViewer

**Study Tools (15 components):**
- NoteGenerator
- SourceSelector
- NoteEditor
- NoteExporter
- TestGenerator
- TestList
- TestTaker
- TestResults
- QuestionEditor
- FlashcardGenerator
- DeckList
- FlashcardStudy
- FlashcardEditor
- SpacedRepetitionTracker
- StudyModeSelector

**Planner (5 components):**
- CalendarView
- EventCreator
- EventList
- TimeBlocker
- StudySessionPlanner

**Social (6 components):**
- ClassmateSearch
- ConnectionRequests
- ClassmateList
- ClassmateProfile
- ShareModal
- SharedContentList

**Gamification (4 components):**
- PointsDisplay
- LevelProgress
- AchievementBadges
- Leaderboard

---

## Part 5: Implementation Phases & Timeline

### Phase 1: Class Management Foundation (Weeks 1-4)
**Goal**: Enable students to organize their academic life

**Deliverables:**
- Classes CRUD API service
- Assignments tracking system
- Database schema 006 deployed
- Class management UI pages
- Assignment management UI

**Success Criteria:**
- Students can create/edit/delete classes
- Students can track assignments with due dates
- All tests passing (unit + integration)

**Effort**: 4 weeks (1 backend dev, 1 frontend dev)

### Phase 2: Content Capture Enhancement (Weeks 5-10)
**Goal**: Capture and process all types of educational content

**Deliverables:**
- Enhanced audio recording with class association
- Photo capture with OCR
- Textbook PDF processing
- Vector embeddings for semantic search
- Database schema 007 deployed
- Content capture UI components

**Success Criteria:**
- Students can record lectures and auto-transcribe
- Students can capture whiteboard photos with OCR
- Students can upload textbooks and search content
- Vector search working across all content types

**Effort**: 6 weeks (2 backend devs, 1 frontend dev, 1 ML engineer)

### Phase 3: AI Study Tools (Weeks 11-18)
**Goal**: Generate study materials automatically from captured content

**Deliverables:**
- AI note generation from multiple sources
- Test/quiz generation with multiple question types
- Flashcard generation with spaced repetition
- Database schema 008 deployed
- Study tools UI components

**Success Criteria:**
- AI can generate comprehensive notes from recordings
- AI can create practice tests from notes
- Flashcard study mode with spaced repetition working
- Students report improved study efficiency

**Effort**: 8 weeks (2 backend devs, 1 frontend dev, 1 ML engineer)

### Phase 4: Planning & Scheduling (Weeks 19-22)
**Goal**: Help students manage their time effectively

**Deliverables:**
- Study planner with calendar views
- Schedule upload and parsing
- Event management with reminders
- Integration with assignments
- Database schema updates
- Planner UI components

**Success Criteria:**
- Students can plan study sessions
- Calendar shows all classes and assignments
- Reminders working for due dates
- Time blocking functional

**Effort**: 4 weeks (1 backend dev, 1 frontend dev)

### Phase 5: Social & Collaboration (Weeks 23-28)
**Goal**: Enable students to connect and share resources

**Deliverables:**
- Classmate connection system
- Content sharing with permissions
- Study groups (basic)
- Database schema 009 deployed
- Social features UI

**Success Criteria:**
- Students can find and connect with classmates
- Students can share notes and flashcards
- Privacy controls working
- Study groups functional

**Effort**: 6 weeks (2 backend devs, 1 frontend dev)

### Phase 6: Gamification & Polish (Weeks 29-32)
**Goal**: Increase engagement through gamification

**Deliverables:**
- Points and currency system
- Achievements and badges
- Leaderboards
- Daily streaks
- Database schema 010 deployed
- Gamification UI components

**Success Criteria:**
- Points awarded for all activities
- Achievement system working
- Leaderboards updating in real-time
- User engagement metrics improved

**Effort**: 4 weeks (1 backend dev, 1 frontend dev)

---

## Part 6: Effort Summary & Resource Requirements

### 6.1 Total Effort Estimate

**Development Time**: 32 weeks (8 months)

**Feature Breakdown:**
- Class Management: 4 weeks
- Content Capture: 6 weeks
- AI Study Tools: 8 weeks
- Planning & Scheduling: 4 weeks
- Social & Collaboration: 6 weeks
- Gamification: 4 weeks

**By Discipline:**
- Backend Development: ~24 weeks
- Frontend Development: ~20 weeks
- ML/AI Engineering: ~14 weeks
- DevOps/Infrastructure: ~4 weeks (ongoing)

### 6.2 Team Requirements

**Recommended Team:**
- 2 Senior Backend Engineers (Python/FastAPI)
- 2 Frontend Engineers (React/Next.js/TypeScript)
- 1 ML Engineer (LLM integration, RAG, embeddings)
- 1 DevOps Engineer (part-time, infrastructure)
- 1 Product Manager (requirements, prioritization)
- 1 UX Designer (UI/UX design, user testing)

**Alternative Minimal Team:**
- 1 Full-stack Engineer (backend + frontend)
- 1 ML Engineer
- Part-time DevOps support

### 6.3 Technology Stack Summary

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- Redis 7+
- AWS Bedrock (Claude Sonnet 4)
- Chroma (vector database)
- Docker + Docker Compose

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS
- React Query
- Zustand (state management)

**AI/ML:**
- AWS Bedrock (Claude Sonnet 4)
- LangChain
- Chroma vector DB
- Azure Speech Services
- Whisper (speech-to-text)
- Tesseract.js or Google Vision (OCR)

**Infrastructure:**
- Docker Compose (development)
- AWS ECS or Kubernetes (production)
- Nginx (API gateway)
- GitHub Actions (CI/CD)

---

## Part 7: Risk Assessment & Mitigation

### 7.1 Technical Risks

**Risk 1: Vector Database Performance**
- **Impact**: High
- **Probability**: Medium
- **Mitigation**: 
  - Start with Chroma, benchmark early
  - Have Pinecone as backup option
  - Implement caching layer
  - Optimize chunk sizes

**Risk 2: AI Generation Quality**
- **Impact**: High
- **Probability**: Medium
- **Mitigation**:
  - Extensive prompt engineering
  - User feedback loops
  - Manual review option
  - Multiple model options

**Risk 3: OCR Accuracy**
- **Impact**: Medium
- **Probability**: High
- **Mitigation**:
  - Allow manual text correction
  - Try multiple OCR engines
  - Image preprocessing
  - User training on photo capture

**Risk 4: Real-time Features Complexity**
- **Impact**: Medium
- **Probability**: Medium
- **Mitigation**:
  - Use WebSockets carefully
  - Implement polling fallback
  - Thorough load testing
  - Gradual rollout

### 7.2 Project Risks

**Risk 1: Scope Creep**
- **Impact**: High
- **Probability**: High
- **Mitigation**:
  - Strict phase gates
  - MVP-first approach
  - Regular stakeholder reviews
  - Feature freeze periods

**Risk 2: Resource Constraints**
- **Impact**: High
- **Probability**: Medium
- **Mitigation**:
  - Prioritize core features
  - Consider outsourcing
  - Extend timeline if needed
  - Reduce scope strategically

**Risk 3: User Adoption**
- **Impact**: High
- **Probability**: Medium
- **Mitigation**:
  - Early user testing
  - Iterative feedback
  - Onboarding optimization
  - Marketing strategy

---

## Part 8: Success Metrics & KPIs

### 8.1 Development Metrics

**Code Quality:**
- Test coverage > 80%
- Zero critical security vulnerabilities
- API response time < 200ms (P95)
- Frontend load time < 2s

**Delivery:**
- On-time phase completion
- Sprint velocity consistency
- Bug resolution time < 48h
- Zero production incidents

### 8.2 Product Metrics

**Engagement:**
- Daily Active Users (DAU)
- Weekly Active Users (WAU)
- Session duration > 15 minutes
- Feature adoption rates

**Value:**
- Content items created per user
- AI generations per week
- Study sessions completed
- Grade improvements (self-reported)

**Retention:**
- 7-day retention > 40%
- 30-day retention > 20%
- Churn rate < 10%/month

---

## Part 9: Next Steps & Recommendations

### 9.1 Immediate Actions (Week 1)

1. **Review & Approve WBS**
   - Stakeholder review meeting
   - Budget approval
   - Timeline confirmation

2. **Team Assembly**
   - Hire/assign team members
   - Set up communication channels
   - Establish development workflow

3. **Infrastructure Setup**
   - Provision cloud resources
   - Set up CI/CD pipelines
   - Configure monitoring

4. **Design Sprint**
   - UI/UX design for Phase 1
   - Database schema finalization
   - API contract definition

### 9.2 Phase 1 Kickoff (Week 2)

1. **Sprint Planning**
   - Break down Phase 1 into 2-week sprints
   - Assign tasks to team members
   - Set up project tracking

2. **Development Environment**
   - Clone and set up repositories
   - Configure local development
   - Run existing tests

3. **Begin Development**
   - Start with database migrations
   - Implement class CRUD API
   - Build class management UI

### 9.3 Long-term Recommendations

**Prioritization Strategy:**
- Focus on features that provide immediate value
- Defer nice-to-have features to later phases
- Get user feedback early and often
- Be prepared to pivot based on usage data

**Quality Over Speed:**
- Don't rush to meet arbitrary deadlines
- Maintain high code quality standards
- Invest in automated testing
- Regular code reviews

**User-Centric Development:**
- Involve real students in testing
- Iterate based on feedback
- Monitor usage analytics
- Build what users actually need

---

## Appendix A: Database Schema Evolution

### Current Schema (12 tables)
```
users, refresh_tokens
audio_files, transcripts, transcription_jobs
async_jobs
study_materials, study_notes
conversations, messages
```

### Target Schema (28+ tables)
```
# Authentication (2)
users, refresh_tokens

# Classes & Assignments (4)
classes, assignments, planner_events, class_schedules

# Content Capture (6)
audio_recordings, transcripts, transcription_jobs
photos, textbook_downloads, textbook_chunks

# Study Tools (8)
study_materials, study_notes, note_sources
generated_tests, test_questions, test_attempts
flashcard_decks, flashcards

# Interactions (3)
conversations, messages, chat_contexts

# Social (3)
classmate_connections, shared_content, study_groups

# Gamification (3)
user_points, achievements, leaderboards

# System (1)
async_jobs
```

---

## Appendix B: API Endpoint Summary

### Current Endpoints (25)
- Authentication: 4 endpoints
- Chat: 3 endpoints
- Materials: 3 endpoints
- TTS: 2 endpoints
- Transcription: 3 endpoints

### Target Endpoints (100+)
- Authentication: 4 endpoints
- Classes: 15 endpoints
- Assignments: 10 endpoints
- Recordings: 12 endpoints
- Photos: 10 endpoints
- Textbooks: 12 endpoints
- Notes: 15 endpoints
- Tests: 15 endpoints
- Flashcards: 15 endpoints
- Planner: 10 endpoints
- Chat (enhanced): 10 endpoints
- Social: 15 endpoints
- Gamification: 8 endpoints

---

## Appendix C: UI Component Inventory

### Current Components (~15)
- Authentication forms
- Dashboard layout
- Chat interface
- Materials list
- TTS controls
- Transcription viewer

### Target Components (70+)
- Class Management: 8 components
- Assignment Management: 6 components
- Content Capture: 12 components
- Study Tools: 15 components
- Planner: 5 components
- Social: 6 components
- Gamification: 4 components
- Shared/Common: 14 components

---

## Document Control

**Version History:**
- v1.0 (Nov 2, 2025) - Initial comprehensive WBS created

**Approval:**
- [ ] Product Owner
- [ ] Technical Lead
- [ ] Project Manager

**Next Review Date**: After Phase 1 completion

**Contact**: Development Team

---

*End of Work Breakdown Structure Document*
