-- ============================================================================
-- Schema 011: Study Sessions & Analytics
-- Version: 1.0
-- Date: 2025-11-02
-- Description: Study session tracking, performance analytics, goals, and reports
-- Dependencies: Schemas 001-010 (all previous phases)
-- ============================================================================

-- ============================================================================
-- Table 1: study_sessions
-- Purpose: Track individual study sessions with metadata
-- ============================================================================

CREATE TABLE IF NOT EXISTS study_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    session_type VARCHAR(50) NOT NULL CHECK (session_type IN ('solo', 'group', 'tutoring')),
    focus_mode BOOLEAN DEFAULT FALSE,
    location VARCHAR(100),
    notes TEXT,
    mood_rating INTEGER CHECK (mood_rating BETWEEN 1 AND 5),
    productivity_rating INTEGER CHECK (productivity_rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for study_sessions
CREATE INDEX idx_study_sessions_user ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_class ON study_sessions(class_id);
CREATE INDEX idx_study_sessions_start ON study_sessions(start_time);
CREATE INDEX idx_study_sessions_type ON study_sessions(session_type);
CREATE INDEX idx_study_sessions_active ON study_sessions(user_id, end_time) WHERE end_time IS NULL;

-- Comments
COMMENT ON TABLE study_sessions IS 'Individual study session records with timing and context';
COMMENT ON COLUMN study_sessions.session_type IS 'Type: solo, group, or tutoring';
COMMENT ON COLUMN study_sessions.focus_mode IS 'Whether user enabled focus/distraction-free mode';
COMMENT ON COLUMN study_sessions.duration_minutes IS 'Calculated when session ends';

-- ============================================================================
-- Table 2: session_activities
-- Purpose: Track activities within study sessions
-- ============================================================================

CREATE TABLE IF NOT EXISTS session_activities (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES study_sessions(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL CHECK (activity_type IN ('reading', 'testing', 'flashcards', 'notes', 'video', 'chat', 'assignment')),
    content_type VARCHAR(50),
    content_id INTEGER,
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    items_completed INTEGER DEFAULT 0,
    items_correct INTEGER DEFAULT 0,
    accuracy_percentage DECIMAL(5,2),
    points_earned INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for session_activities
CREATE INDEX idx_session_activities_session ON session_activities(session_id);
CREATE INDEX idx_session_activities_type ON session_activities(activity_type);
CREATE INDEX idx_session_activities_content ON session_activities(content_type, content_id);
CREATE INDEX idx_session_activities_time ON session_activities(start_time);

-- Comments
COMMENT ON TABLE session_activities IS 'Activities performed during study sessions';
COMMENT ON COLUMN session_activities.activity_type IS 'Type of activity: reading, testing, flashcards, etc.';
COMMENT ON COLUMN session_activities.content_type IS 'Type of content: textbook, note, test, flashcard_deck';
COMMENT ON COLUMN session_activities.content_id IS 'Reference to specific content item';
COMMENT ON COLUMN session_activities.metadata IS 'Flexible JSON storage for activity-specific data';

-- ============================================================================
-- Table 3: performance_metrics
-- Purpose: Aggregated performance data over time periods
-- ============================================================================

CREATE TABLE IF NOT EXISTS performance_metrics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    metric_type VARCHAR(50) NOT NULL CHECK (metric_type IN ('test_average', 'flashcard_mastery', 'assignment_completion', 'study_time', 'attendance')),
    metric_period VARCHAR(20) NOT NULL CHECK (metric_period IN ('daily', 'weekly', 'monthly', 'all_time')),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    metric_value DECIMAL(10,2) NOT NULL,
    sample_size INTEGER,
    trend VARCHAR(20) CHECK (trend IN ('improving', 'declining', 'stable', 'insufficient_data')),
    percentile_rank INTEGER CHECK (percentile_rank BETWEEN 0 AND 100),
    metadata JSONB,
    calculated_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance_metrics
CREATE INDEX idx_performance_metrics_user ON performance_metrics(user_id);
CREATE INDEX idx_performance_metrics_class ON performance_metrics(class_id);
CREATE INDEX idx_performance_metrics_type ON performance_metrics(metric_type);
CREATE INDEX idx_performance_metrics_period ON performance_metrics(period_start, period_end);
CREATE UNIQUE INDEX idx_performance_metrics_unique ON performance_metrics(user_id, COALESCE(class_id, 0), metric_type, metric_period, period_start);

-- Comments
COMMENT ON TABLE performance_metrics IS 'Aggregated performance metrics over time periods';
COMMENT ON COLUMN performance_metrics.metric_type IS 'Type of metric being tracked';
COMMENT ON COLUMN performance_metrics.metric_period IS 'Time period: daily, weekly, monthly, all_time';
COMMENT ON COLUMN performance_metrics.trend IS 'Performance trend: improving, declining, stable';
COMMENT ON COLUMN performance_metrics.percentile_rank IS 'User rank compared to peers (0-100)';

-- ============================================================================
-- Table 4: study_goals
-- Purpose: User-defined study goals with tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS study_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    goal_type VARCHAR(50) NOT NULL CHECK (goal_type IN ('study_time', 'test_score', 'assignment_completion', 'flashcard_mastery', 'streak', 'custom')),
    goal_name VARCHAR(200) NOT NULL,
    goal_description TEXT,
    target_value DECIMAL(10,2) NOT NULL,
    current_value DECIMAL(10,2) DEFAULT 0,
    unit VARCHAR(50),
    start_date DATE NOT NULL,
    target_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned', 'expired')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_pattern VARCHAR(50),
    reminder_enabled BOOLEAN DEFAULT TRUE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_date_range CHECK (target_date >= start_date),
    CONSTRAINT valid_target CHECK (target_value > 0)
);

-- Indexes for study_goals
CREATE INDEX idx_study_goals_user ON study_goals(user_id);
CREATE INDEX idx_study_goals_class ON study_goals(class_id);
CREATE INDEX idx_study_goals_status ON study_goals(status);
CREATE INDEX idx_study_goals_dates ON study_goals(start_date, target_date);
CREATE INDEX idx_study_goals_active ON study_goals(user_id, status) WHERE status = 'active';

-- Comments
COMMENT ON TABLE study_goals IS 'User-defined study goals with progress tracking';
COMMENT ON COLUMN study_goals.goal_type IS 'Type of goal: study_time, test_score, etc.';
COMMENT ON COLUMN study_goals.unit IS 'Unit of measurement: hours, percentage, count';
COMMENT ON COLUMN study_goals.is_recurring IS 'Whether goal repeats on a schedule';
COMMENT ON COLUMN study_goals.recurrence_pattern IS 'Pattern: daily, weekly, monthly';

-- ============================================================================
-- Table 5: goal_progress
-- Purpose: Daily progress tracking for goals
-- ============================================================================

CREATE TABLE IF NOT EXISTS goal_progress (
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

-- Indexes for goal_progress
CREATE INDEX idx_goal_progress_goal ON goal_progress(goal_id);
CREATE INDEX idx_goal_progress_date ON goal_progress(recorded_date);
CREATE UNIQUE INDEX idx_goal_progress_unique ON goal_progress(goal_id, recorded_date);

-- Comments
COMMENT ON TABLE goal_progress IS 'Daily progress records for study goals';
COMMENT ON COLUMN goal_progress.percentage_complete IS 'Calculated percentage toward goal';
COMMENT ON COLUMN goal_progress.milestone_reached IS 'Whether a milestone was achieved this day';

-- ============================================================================
-- Table 6: analytics_snapshots
-- Purpose: Daily/weekly/monthly aggregated analytics data
-- ============================================================================

CREATE TABLE IF NOT EXISTS analytics_snapshots (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    snapshot_type VARCHAR(20) NOT NULL CHECK (snapshot_type IN ('daily', 'weekly', 'monthly')),
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
    productivity_score DECIMAL(5,2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for analytics_snapshots
CREATE INDEX idx_analytics_snapshots_user ON analytics_snapshots(user_id);
CREATE INDEX idx_analytics_snapshots_date ON analytics_snapshots(snapshot_date);
CREATE INDEX idx_analytics_snapshots_type ON analytics_snapshots(snapshot_type);
CREATE UNIQUE INDEX idx_analytics_snapshots_unique ON analytics_snapshots(user_id, snapshot_date, snapshot_type);

-- Comments
COMMENT ON TABLE analytics_snapshots IS 'Pre-calculated daily/weekly/monthly analytics snapshots';
COMMENT ON COLUMN analytics_snapshots.snapshot_type IS 'Type: daily, weekly, or monthly';
COMMENT ON COLUMN analytics_snapshots.productivity_score IS 'Calculated productivity metric (0-100)';
COMMENT ON COLUMN analytics_snapshots.streak_days IS 'Current study streak in days';

-- ============================================================================
-- Functions and Triggers
-- ============================================================================

-- Function: Calculate session duration when session ends
CREATE OR REPLACE FUNCTION calculate_session_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.end_time IS NOT NULL AND OLD.end_time IS NULL THEN
        NEW.duration_minutes := EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time)) / 60;
    END IF;
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-calculate duration on session end
DROP TRIGGER IF EXISTS trg_calculate_session_duration ON study_sessions;
CREATE TRIGGER trg_calculate_session_duration
    BEFORE UPDATE ON study_sessions
    FOR EACH ROW
    EXECUTE FUNCTION calculate_session_duration();

-- Function: Calculate activity duration
CREATE OR REPLACE FUNCTION calculate_activity_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.end_time IS NOT NULL AND NEW.start_time IS NOT NULL THEN
        NEW.duration_minutes := EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time)) / 60;
    END IF;
    
    -- Calculate accuracy if items_completed > 0
    IF NEW.items_completed > 0 AND NEW.items_correct IS NOT NULL THEN
        NEW.accuracy_percentage := (NEW.items_correct::DECIMAL / NEW.items_completed) * 100;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-calculate activity metrics
DROP TRIGGER IF EXISTS trg_calculate_activity_duration ON session_activities;
CREATE TRIGGER trg_calculate_activity_duration
    BEFORE INSERT OR UPDATE ON session_activities
    FOR EACH ROW
    EXECUTE FUNCTION calculate_activity_duration();

-- Function: Update goal progress percentage
CREATE OR REPLACE FUNCTION update_goal_progress_percentage()
RETURNS TRIGGER AS $$
DECLARE
    goal_target DECIMAL(10,2);
BEGIN
    -- Get target value from goal
    SELECT target_value INTO goal_target
    FROM study_goals
    WHERE id = NEW.goal_id;
    
    -- Calculate percentage
    IF goal_target > 0 THEN
        NEW.percentage_complete := (NEW.progress_value / goal_target) * 100;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-calculate goal progress percentage
DROP TRIGGER IF EXISTS trg_update_goal_progress_percentage ON goal_progress;
CREATE TRIGGER trg_update_goal_progress_percentage
    BEFORE INSERT OR UPDATE ON goal_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_goal_progress_percentage();

-- Function: Update goal current value from progress
CREATE OR REPLACE FUNCTION update_goal_current_value()
RETURNS TRIGGER AS $$
BEGIN
    -- Update the goal's current_value with the latest progress
    UPDATE study_goals
    SET current_value = NEW.progress_value,
        updated_at = NOW()
    WHERE id = NEW.goal_id;
    
    -- Check if goal is completed
    UPDATE study_goals
    SET status = 'completed',
        completed_at = NOW()
    WHERE id = NEW.goal_id
        AND current_value >= target_value
        AND status = 'active';
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Update goal when progress is recorded
DROP TRIGGER IF EXISTS trg_update_goal_current_value ON goal_progress;
CREATE TRIGGER trg_update_goal_current_value
    AFTER INSERT OR UPDATE ON goal_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_goal_current_value();

-- Function: Check for expired goals
CREATE OR REPLACE FUNCTION check_expired_goals()
RETURNS void AS $$
BEGIN
    UPDATE study_goals
    SET status = 'expired',
        updated_at = NOW()
    WHERE status = 'active'
        AND target_date < CURRENT_DATE
        AND current_value < target_value;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View: Active study sessions
CREATE OR REPLACE VIEW active_study_sessions AS
SELECT 
    s.id,
    s.user_id,
    s.class_id,
    c.name as class_name,
    s.start_time,
    EXTRACT(EPOCH FROM (NOW() - s.start_time)) / 60 as current_duration_minutes,
    s.session_type,
    s.focus_mode,
    s.location
FROM study_sessions s
LEFT JOIN classes c ON s.class_id = c.id
WHERE s.end_time IS NULL;

-- View: User study summary (last 30 days)
CREATE OR REPLACE VIEW user_study_summary_30d AS
SELECT 
    user_id,
    COUNT(*) as total_sessions,
    SUM(duration_minutes) as total_minutes,
    AVG(duration_minutes) as avg_session_duration,
    SUM(CASE WHEN mood_rating >= 4 THEN 1 ELSE 0 END) as positive_mood_sessions,
    SUM(CASE WHEN productivity_rating >= 4 THEN 1 ELSE 0 END) as productive_sessions
FROM study_sessions
WHERE start_time >= CURRENT_DATE - INTERVAL '30 days'
    AND end_time IS NOT NULL
GROUP BY user_id;

-- View: Active goals with progress
CREATE OR REPLACE VIEW active_goals_with_progress AS
SELECT 
    g.id,
    g.user_id,
    g.class_id,
    g.goal_name,
    g.goal_type,
    g.target_value,
    g.current_value,
    g.unit,
    g.start_date,
    g.target_date,
    g.priority,
    (g.current_value / g.target_value * 100) as percentage_complete,
    (g.target_date - CURRENT_DATE) as days_remaining,
    CASE 
        WHEN g.current_value >= g.target_value THEN 'completed'
        WHEN (g.current_value / NULLIF((CURRENT_DATE - g.start_date), 0)) * 
             (g.target_date - g.start_date) >= g.target_value THEN 'on_track'
        ELSE 'behind'
    END as progress_status
FROM study_goals g
WHERE g.status = 'active';

-- ============================================================================
-- Sample Data (for testing)
-- ============================================================================

-- Note: Sample data will be inserted via test scripts, not in schema

-- ============================================================================
-- Grants (adjust based on your user roles)
-- ============================================================================

-- Grant permissions to application user (adjust username as needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO lm_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO lm_app_user;

-- ============================================================================
-- Schema Verification Queries
-- ============================================================================

-- Verify all tables exist
-- SELECT table_name FROM information_schema.tables 
-- WHERE table_schema = 'public' 
-- AND table_name IN ('study_sessions', 'session_activities', 'performance_metrics', 
--                    'study_goals', 'goal_progress', 'analytics_snapshots');

-- Verify all indexes exist
-- SELECT indexname FROM pg_indexes 
-- WHERE schemaname = 'public' 
-- AND tablename IN ('study_sessions', 'session_activities', 'performance_metrics', 
--                   'study_goals', 'goal_progress', 'analytics_snapshots');

-- ============================================================================
-- End of Schema 011
-- ============================================================================
