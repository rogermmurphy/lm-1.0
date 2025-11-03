# Phase 6: Study Sessions & Analytics - Implementation Plan

## Document Control
- **Version**: 1.0
- **Date**: November 2, 2025
- **Status**: Ready for Implementation
- **Dependencies**: Phases 1-5 Complete

---

## Executive Summary

Phase 6 implements **Study Sessions & Analytics** - a comprehensive system for tracking study time, analyzing performance, and providing actionable insights to help students optimize their learning.

### Key Features
1. **Study Session Tracking** - Record and manage study sessions
2. **Performance Analytics** - Analyze test scores, flashcard performance, assignment completion
3. **Time Analytics** - Track study time by subject, topic, and activity type
4. **Progress Insights** - AI-powered recommendations and insights
5. **Goal Setting & Tracking** - Set study goals and monitor progress
6. **Reports & Visualizations** - Generate comprehensive study reports

### Integration Points
- **Phase 1**: Class and assignment data for context
- **Phase 2**: Content usage tracking
- **Phase 3**: Test scores, flashcard performance, note usage
- **Phase 4**: Group study sessions, peer comparisons
- **Phase 5**: Points earned during sessions, achievement triggers

---

## Architecture Overview

### Service: study-analytics
- **Port**: 8012
- **Database Schema**: 011_study_analytics.sql
- **Dependencies**: All previous phases
- **API Endpoints**: 12 endpoints across 4 route modules

### Database Tables (6 new tables)
1. `study_sessions` - Individual study session records
2. `session_activities` - Activities within sessions (reading, testing, flashcards)
3. `performance_metrics` - Aggregated performance data
4. `study_goals` - User-defined study goals
5. `goal_progress` - Progress tracking for goals
6. `analytics_snapshots` - Daily/weekly/monthly aggregated data

---

## Database Schema Design

### Table 1: study_sessions
```sql
CREATE TABLE study_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_minutes INTEGER, -- Calculated on end
    session_type VARCHAR(50) NOT NULL, -- 'solo', 'group', 'tutoring'
    focus_mode BOOLEAN DEFAULT FALSE,
    location VARCHAR(100), -- 'library', 'home', 'cafe', etc.
    notes TEXT,
    mood_rating INTEGER CHECK (mood_rating BETWEEN 1 AND 5),
    productivity_rating INTEGER CHECK (productivity_rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_study_sessions_user ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_class ON study_sessions(class_id);
CREATE INDEX idx_study_sessions_start ON study_sessions(start_time);
CREATE INDEX idx_study_sessions_type ON study_sessions(session_type);
```

### Table 2: session_activities
```sql
CREATE TABLE session_activities (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- 'reading', 'testing', 'flashcards', 'notes', 'video', 'chat'
    content_type VARCHAR(50), -- 'textbook', 'note', 'test', 'flashcard_deck'
    content_id INTEGER, -- Reference to specific content
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    items_completed INTEGER, -- Questions answered, cards reviewed, etc.
    items_correct INTEGER, -- For assessments
    accuracy_percentage DECIMAL(5,2),
    points_earned INTEGER DEFAULT 0,
    metadata JSONB, -- Flexible storage for activity-specific data
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_session_activities_session ON session_activities(session_id);
CREATE INDEX idx_session_activities_type ON session_activities(activity_type);
CREATE INDEX idx_session_activities_content ON session_activities(content_type, content_id);
```

### Table 3: performance_metrics
```sql
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'test_average', 'flashcard_mastery', 'assignment_completion'
    metric_period VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly', 'all_time'
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    sample_size INTEGER, -- Number of data points
    trend VARCHAR(20), -- 'improving', 'declining', 'stable'
    percentile_rank INTEGER, -- Compared to other users (optional)
    metadata JSONB,
    calculated_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_performance_metrics_user ON performance_metrics(user_id);
CREATE INDEX idx_performance_metrics_class ON performance_metrics(class_id);
CREATE INDEX idx_performance_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_period ON performance_metrics(period_start, period_end);
CREATE UNIQUE INDEX idx_performance_metrics_unique ON performance_metrics(user_id, class_id, metric_type, metric_period, period_start);
```

### Table 4: study_goals
```sql
CREATE TABLE study_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    goal_type VARCHAR(50) NOT NULL, -- 'study_time', 'test_score', 'assignment_completion', 'flashcard_mastery'
    goal_name VARCHAR(200) NOT NULL,
    goal_description TEXT,
    target_value DECIMAL(10,2) NOT NULL,
    current_value DECIMAL(10,2) DEFAULT 0,
    unit VARCHAR(50), -- 'hours', 'percentage', 'count'
    start_date DATE NOT NULL,
    target_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'abandoned', 'expired'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high'
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50), -- 'daily', 'weekly', 'monthly'
    reminder_enabled BOOLEAN DEFAULT TRUE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_study_goals_user ON study_goals(user_id);
CREATE INDEX idx_study_goals_class ON study_goals(class_id);
CREATE INDEX idx_study_goals_status ON study_goals(status);
CREATE INDEX idx_study_goals_dates ON study_goals(start_date, target_date);
```

### Table 5: goal_progress
```sql
CREATE TABLE goal_progress (
    id SERIAL PRIMARY KEY,
    goal_id INTEGER NOT NULL REFERENCES study_goals(id) ON DELETE CASCADE,
    recorded_date DATE NOT NULL,
    progress_value DECIMAL(10,2) NOT NULL,
    percentage_complete DECIMAL(5,2),
    notes TEXT,
    milestone_reached BOOLEAN DEFAULT FALSE,
    milestone_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_goal_progress_goal ON goal_progress(goal_id);
CREATE INDEX idx_goal_progress_date ON goal_progress(recorded_date);
CREATE UNIQUE INDEX idx_goal_progress_unique ON goal_progress(goal_id, recorded_date);
```

### Table 6: analytics_snapshots
```sql
CREATE TABLE analytics_snapshots (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    snapshot_type VARCHAR(20) NOT NULL, -- 'daily', 'weekly', 'monthly'
    total_study_minutes INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    avg_session_duration INTEGER,
    total_points_earned INTEGER DEFAULT 0,
    tests_taken INTEGER DEFAULT 0,
    avg_test_score DECIMAL(5,2),
    flashcards_reviewed INTEGER DEFAULT 0,
    flashcard_accuracy DECIMAL(5,2),
    assignments_completed INTEGER DEFAULT 0,
    notes_created INTEGER DEFAULT 0,
    most_studied_class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    most_studied_minutes INTEGER,
    streak_days INTEGER DEFAULT 0,
    productivity_score DECIMAL(5,2), -- Calculated metric
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analytics_snapshots_user ON analytics_snapshots(user_id);
CREATE INDEX idx_analytics_snapshots_date ON analytics_snapshots(snapshot_date);
CREATE INDEX idx_analytics_snapshots_type ON analytics_snapshots(snapshot_type);
CREATE UNIQUE INDEX idx_analytics_snapshots_unique ON analytics_snapshots(user_id, snapshot_date, snapshot_type);
```

---

## API Endpoints Design

### Route Module 1: Sessions (`/api/analytics/sessions`)

#### POST /api/analytics/sessions/start
Start a new study session
```json
Request:
{
  "class_id": 1,
  "session_type": "solo",
  "focus_mode": true,
  "location": "library"
}

Response:
{
  "session_id": 123,
  "start_time": "2025-11-02T17:30:00Z",
  "message": "Study session started"
}
```

#### PUT /api/analytics/sessions/{session_id}/end
End an active study session
```json
Request:
{
  "mood_rating": 4,
  "productivity_rating": 5,
  "notes": "Great study session, covered chapters 5-7"
}

Response:
{
  "session_id": 123,
  "duration_minutes": 90,
  "points_earned": 45,
  "message": "Study session ended"
}
```

#### POST /api/analytics/sessions/{session_id}/activities
Log an activity within a session
```json
Request:
{
  "activity_type": "testing",
  "content_type": "test",
  "content_id": 5,
  "items_completed": 20,
  "items_correct": 18,
  "duration_minutes": 30
}

Response:
{
  "activity_id": 456,
  "accuracy_percentage": 90.0,
  "points_earned": 18,
  "message": "Activity logged"
}
```

#### GET /api/analytics/sessions
Get user's study sessions with filters
```
Query params: ?class_id=1&start_date=2025-11-01&end_date=2025-11-30&limit=50

Response:
{
  "sessions": [...],
  "total_count": 25,
  "total_minutes": 1800,
  "avg_duration": 72
}
```

---

### Route Module 2: Performance (`/api/analytics/performance`)

#### GET /api/analytics/performance/overview
Get comprehensive performance overview
```
Query params: ?class_id=1&period=monthly

Response:
{
  "user_id": 7,
  "period": "monthly",
  "period_start": "2025-11-01",
  "period_end": "2025-11-30",
  "metrics": {
    "study_time": {
      "total_minutes": 1800,
      "avg_per_day": 60,
      "trend": "improving"
    },
    "test_performance": {
      "tests_taken": 5,
      "avg_score": 87.5,
      "trend": "stable"
    },
    "flashcard_mastery": {
      "cards_reviewed": 250,
      "accuracy": 82.0,
      "mastered_count": 180
    },
    "assignment_completion": {
      "total_assignments": 10,
      "completed": 9,
      "completion_rate": 90.0
    }
  },
  "strengths": ["Consistent study schedule", "High test scores"],
  "areas_for_improvement": ["Flashcard accuracy could improve"],
  "recommendations": [...]
}
```

#### GET /api/analytics/performance/trends
Get performance trends over time
```
Query params: ?metric_type=test_average&period=weekly&weeks=12

Response:
{
  "metric_type": "test_average",
  "data_points": [
    {"week": "2025-W40", "value": 82.5, "sample_size": 2},
    {"week": "2025-W41", "value": 85.0, "sample_size": 3},
    ...
  ],
  "overall_trend": "improving",
  "trend_percentage": 12.5
}
```

#### GET /api/analytics/performance/comparison
Compare performance across classes or time periods
```
Query params: ?compare_by=class&period=monthly

Response:
{
  "comparison_type": "class",
  "period": "monthly",
  "comparisons": [
    {
      "class_id": 1,
      "class_name": "Calculus I",
      "study_minutes": 600,
      "avg_test_score": 88.0,
      "rank": 1
    },
    ...
  ]
}
```

---

### Route Module 3: Goals (`/api/analytics/goals`)

#### POST /api/analytics/goals
Create a new study goal
```json
Request:
{
  "class_id": 1,
  "goal_type": "study_time",
  "goal_name": "Study 20 hours this month",
  "target_value": 1200,
  "unit": "minutes",
  "target_date": "2025-11-30",
  "priority": "high",
  "reminder_enabled": true
}

Response:
{
  "goal_id": 10,
  "status": "active",
  "current_value": 0,
  "percentage_complete": 0,
  "message": "Goal created successfully"
}
```

#### GET /api/analytics/goals
Get user's study goals
```
Query params: ?status=active&class_id=1

Response:
{
  "goals": [
    {
      "goal_id": 10,
      "goal_name": "Study 20 hours this month",
      "target_value": 1200,
      "current_value": 450,
      "percentage_complete": 37.5,
      "days_remaining": 15,
      "on_track": true
    },
    ...
  ]
}
```

#### PUT /api/analytics/goals/{goal_id}
Update a study goal
```json
Request:
{
  "target_value": 1500,
  "priority": "medium"
}

Response:
{
  "goal_id": 10,
  "message": "Goal updated successfully"
}
```

#### POST /api/analytics/goals/{goal_id}/progress
Record progress toward a goal
```json
Request:
{
  "progress_value": 500,
  "notes": "Halfway there!"
}

Response:
{
  "goal_id": 10,
  "percentage_complete": 41.7,
  "milestone_reached": true,
  "milestone_name": "50% Complete"
}
```

#### DELETE /api/analytics/goals/{goal_id}
Delete or abandon a goal
```
Response:
{
  "message": "Goal deleted successfully"
}
```

---

### Route Module 4: Reports (`/api/analytics/reports`)

#### GET /api/analytics/reports/daily
Get daily study report
```
Query params: ?date=2025-11-02

Response:
{
  "date": "2025-11-02",
  "summary": {
    "total_study_minutes": 120,
    "sessions_count": 2,
    "points_earned": 60,
    "tests_taken": 1,
    "flashcards_reviewed": 50
  },
  "sessions": [...],
  "achievements_earned": [...],
  "goals_progress": [...]
}
```

#### GET /api/analytics/reports/weekly
Get weekly study report
```
Query params: ?week=2025-W44

Response:
{
  "week": "2025-W44",
  "week_start": "2025-10-28",
  "week_end": "2025-11-03",
  "summary": {
    "total_study_minutes": 840,
    "avg_daily_minutes": 120,
    "total_sessions": 14,
    "streak_maintained": true
  },
  "daily_breakdown": [...],
  "top_subjects": [...],
  "performance_highlights": [...]
}
```

#### GET /api/analytics/reports/monthly
Get monthly study report
```
Query params: ?month=2025-11

Response:
{
  "month": "2025-11",
  "summary": {
    "total_study_minutes": 3600,
    "total_sessions": 60,
    "avg_session_duration": 60,
    "total_points": 1800
  },
  "performance_summary": {...},
  "goals_achieved": [...],
  "top_achievements": [...],
  "recommendations": [...]
}
```

---

## Service Implementation

### File Structure
```
services/study-analytics/
├── Dockerfile
├── requirements.txt
├── .env
├── test_service.py
└── src/
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── models.py
    ├── services/
    │   ├── __init__.py
    │   ├── session_service.py
    │   ├── performance_service.py
    │   ├── goal_service.py
    │   └── report_service.py
    └── routes/
        ├── __init__.py
        ├── sessions.py
        ├── performance.py
        ├── goals.py
        └── reports.py
```

### Key Service Logic

#### session_service.py
- Start/end session tracking
- Calculate session duration and points
- Log activities within sessions
- Integrate with gamification for point awards
- Track focus mode and productivity

#### performance_service.py
- Aggregate performance metrics from multiple sources
- Calculate trends and percentiles
- Generate AI-powered insights
- Compare performance across classes/periods
- Identify strengths and weaknesses

#### goal_service.py
- Create and manage study goals
- Track progress automatically
- Detect milestone achievements
- Send reminders (integrate with notification system)
- Calculate goal completion predictions

#### report_service.py
- Generate daily/weekly/monthly reports
- Aggregate data from all analytics tables
- Create visualizations data
- Export reports (PDF, CSV)
- Schedule automated report generation

---

## Integration Requirements

### Phase 1 Integration (Class Management)
- Link sessions to classes
- Track study time per class
- Include assignment completion in analytics

### Phase 2 Integration (Content Capture)
- Track textbook reading time
- Monitor photo/PDF usage
- Include content engagement metrics

### Phase 3 Integration (AI Study Tools)
- Track test scores and performance
- Monitor flashcard review sessions
- Include note creation/usage stats

### Phase 4 Integration (Social Collaboration)
- Track group study sessions
- Compare performance with peers
- Include collaboration metrics

### Phase 5 Integration (Gamification)
- Award points for study sessions
- Trigger achievements based on analytics
- Update leaderboards with study time

---

## Testing Strategy

### Unit Tests
- Session CRUD operations
- Performance calculation logic
- Goal progress tracking
- Report generation

### Integration Tests
- Session → Points integration
- Performance → Achievements integration
- Goal → Notifications integration
- Multi-phase data aggregation

### End-to-End Tests
1. Start session → Log activities → End session → Verify points
2. Create goal → Study → Check progress → Complete goal
3. Study for week → Generate report → Verify accuracy
4. Compare performance across classes

---

## UI Components

### Dashboard Widgets
1. **Active Session Card** - Current study session timer
2. **Today's Progress** - Study time, points, activities
3. **Goals Overview** - Active goals with progress bars
4. **Performance Chart** - Weekly/monthly trends
5. **Insights Panel** - AI-generated recommendations

### New Pages

#### /dashboard/analytics
Main analytics dashboard with:
- Study time overview
- Performance metrics
- Goal progress
- Recent sessions
- Insights and recommendations

#### /dashboard/sessions
Study session management:
- Active session controls
- Session history
- Session details view
- Activity logs

#### /dashboard/goals
Goal management:
- Create new goals
- Active goals list
- Goal progress tracking
- Completed goals archive

#### /dashboard/reports
Report generation:
- Daily/weekly/monthly reports
- Custom date range reports
- Export options
- Scheduled reports

---

## Implementation Checklist

### Phase 6.1: Database & Core Service (Week 1)
- [ ] Create database schema 011_study_analytics.sql
- [ ] Deploy schema with deploy_011.py
- [ ] Verify tables with verify_011.py
- [ ] Create service structure
- [ ] Implement config and models
- [ ] Set up CORS and authentication

### Phase 6.2: Session Tracking (Week 1-2)
- [ ] Implement session_service.py
- [ ] Create sessions.py routes
- [ ] Add session start/end endpoints
- [ ] Add activity logging
- [ ] Integrate with gamification points
- [ ] Test session workflow

### Phase 6.3: Performance Analytics (Week 2)
- [ ] Implement performance_service.py
- [ ] Create performance.py routes
- [ ] Add metrics calculation
- [ ] Add trend analysis
- [ ] Add comparison features
- [ ] Test performance calculations

### Phase 6.4: Goals System (Week 2-3)
- [ ] Implement goal_service.py
- [ ] Create goals.py routes
- [ ] Add goal CRUD operations
- [ ] Add progress tracking
- [ ] Add milestone detection
- [ ] Test goal workflows

### Phase 6.5: Reports (Week 3)
- [ ] Implement report_service.py
- [ ] Create reports.py routes
- [ ] Add daily/weekly/monthly reports
- [ ] Add data aggregation
- [ ] Add export functionality
- [ ] Test report generation

### Phase 6.6: Testing (Week 3)
- [ ] Create comprehensive test suite
- [ ] Test all endpoints
- [ ] Test integrations with other phases
- [ ] Test performance under load
- [ ] Fix any issues found

### Phase 6.7: UI Implementation (Week 4)
- [ ] Create analytics dashboard page
- [ ] Create sessions management page
- [ ] Create goals page
- [ ] Create reports page
- [ ] Add dashboard widgets
- [ ] Test UI with Playwright

### Phase 6.8: Documentation (Week 4)
- [ ] Document all endpoints
- [ ] Create user guide
- [ ] Update DEVELOPER-HANDOVER.md
- [ ] Create PHASE6-COMPLETE.md
- [ ] Update docker-compose.yml

---

## Success Criteria

### Backend
- ✅ All 12 API endpoints functional
- ✅ 100% test pass rate
- ✅ Session tracking accurate
- ✅ Performance calculations correct
- ✅ Goal progress updates automatically
- ✅ Reports generate successfully

### Integration
- ✅ Points awarded for study sessions
- ✅ Achievements triggered by analytics
- ✅ Data aggregates from all phases
- ✅ No data inconsistencies

### UI
- ✅ Analytics dashboard displays correctly
- ✅ Session timer works
- ✅ Goals update in real-time
- ✅ Reports export successfully
- ✅ Playwright tests pass

### Performance
- ✅ Report generation < 2 seconds
- ✅ Analytics queries < 500ms
- ✅ Session updates < 100ms
- ✅ Dashboard loads < 1.5 seconds

---

## Timeline

**Total Duration**: 4 weeks

- **Week 1**: Database + Session Tracking
- **Week 2**: Performance Analytics + Goals
- **Week 3**: Reports + Testing
- **Week 4**: UI + Documentation

**Target Completion**: November 30, 2025

---

## Next Steps

1. Review and approve this implementation plan
2. Create database schema file
3. Deploy schema to database
4. Begin service implementation
5. Follow zero-tolerance testing workflow

---

## Notes

- This phase completes the core educational platform features
- Future phases could add: AI tutoring improvements, mobile apps, advanced analytics
- Consider adding real-time notifications for goal milestones
- May want to add data export for students to share with teachers/parents
