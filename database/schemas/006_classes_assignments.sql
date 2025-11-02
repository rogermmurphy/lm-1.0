-- Little Monster - Classes & Assignments Schema
-- Migration: 006_classes_assignments
-- Created: November 2, 2025
-- Description: Class management, assignments, and planner events

-- ============================================================================
-- CLASSES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    teacher_name VARCHAR(100),
    period VARCHAR(20),
    color VARCHAR(20) DEFAULT '#3B82F6',
    subject VARCHAR(50),
    current_grade VARCHAR(5),
    grade_percent INTEGER CHECK (grade_percent >= 0 AND grade_percent <= 100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, name)
);

CREATE INDEX idx_classes_user ON classes(user_id);
CREATE INDEX idx_classes_subject ON classes(subject);

-- ============================================================================
-- ASSIGNMENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    type VARCHAR(50) DEFAULT 'homework',
    description TEXT,
    due_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'in-progress', 'completed', 'overdue')),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_assignments_class ON assignments(class_id, due_date);
CREATE INDEX idx_assignments_user_status ON assignments(user_id, status, due_date);
CREATE INDEX idx_assignments_due_date ON assignments(due_date);

-- ============================================================================
-- PLANNER EVENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS planner_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) DEFAULT 'study' CHECK (event_type IN ('study', 'assignment', 'exam', 'class', 'other')),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    is_recurring BOOLEAN DEFAULT false,
    recurrence_rule TEXT,
    is_completed BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_planner_events_user ON planner_events(user_id, start_time);
CREATE INDEX idx_planner_events_class ON planner_events(class_id, start_time);
CREATE INDEX idx_planner_events_date_range ON planner_events(start_time, end_time);

-- ============================================================================
-- CLASS SCHEDULES TABLE (for recurring class times)
-- ============================================================================

CREATE TABLE IF NOT EXISTS class_schedules (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(class_id, day_of_week, start_time)
);

CREATE INDEX idx_class_schedules_class ON class_schedules(class_id);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_classes_updated_at
    BEFORE UPDATE ON classes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assignments_updated_at
    BEFORE UPDATE ON assignments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_planner_events_updated_at
    BEFORE UPDATE ON planner_events
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_class_schedules_updated_at
    BEFORE UPDATE ON class_schedules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- TRIGGER TO AUTO-UPDATE ASSIGNMENT STATUS TO OVERDUE
-- ============================================================================

CREATE OR REPLACE FUNCTION check_assignment_overdue()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.due_date < NOW() AND NEW.status = 'pending' THEN
        NEW.status = 'overdue';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER assignment_overdue_check
    BEFORE INSERT OR UPDATE ON assignments
    FOR EACH ROW
    EXECUTE FUNCTION check_assignment_overdue();

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE classes IS 'Student classes/courses';
COMMENT ON TABLE assignments IS 'Class assignments and homework';
COMMENT ON TABLE planner_events IS 'Calendar events for study planning';
COMMENT ON TABLE class_schedules IS 'Recurring class meeting times';

COMMENT ON COLUMN classes.color IS 'Hex color code for UI display';
COMMENT ON COLUMN assignments.status IS 'pending, in-progress, completed, overdue';
COMMENT ON COLUMN planner_events.recurrence_rule IS 'iCal RRULE format for recurring events';
COMMENT ON COLUMN class_schedules.day_of_week IS '0=Sunday, 1=Monday, ..., 6=Saturday';
