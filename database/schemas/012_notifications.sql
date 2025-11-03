-- ============================================================================
-- Schema 012: Notifications & Communication
-- Version: 1.0
-- Date: 2025-11-02
-- Description: Notification system, direct messaging, and announcements
-- Dependencies: Schemas 001-011 (all previous phases)
-- ============================================================================

-- ============================================================================
-- Table 1: notifications
-- Purpose: Store all user notifications
-- ============================================================================

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    action_url VARCHAR(500),
    reference_type VARCHAR(50),
    reference_id INTEGER,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_notifications_type ON notifications(notification_type);
CREATE INDEX idx_notifications_created ON notifications(created_at);
CREATE INDEX idx_notifications_reference ON notifications(reference_type, reference_id);

COMMENT ON TABLE notifications IS 'User notifications for all platform events';
COMMENT ON COLUMN notifications.notification_type IS 'Type: assignment, goal, achievement, social, study, system';
COMMENT ON COLUMN notifications.action_url IS 'URL to navigate to when notification clicked';
COMMENT ON COLUMN notifications.reference_type IS 'Type of referenced object';
COMMENT ON COLUMN notifications.reference_id IS 'ID of referenced object';

-- ============================================================================
-- Table 2: notification_preferences
-- Purpose: User notification settings
-- ============================================================================

CREATE TABLE IF NOT EXISTS notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL,
    in_app_enabled BOOLEAN DEFAULT TRUE,
    email_enabled BOOLEAN DEFAULT TRUE,
    push_enabled BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(20) DEFAULT 'immediate' CHECK (frequency IN ('immediate', 'hourly', 'daily', 'weekly', 'never')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, notification_type)
);

CREATE INDEX idx_notification_prefs_user ON notification_preferences(user_id);
CREATE INDEX idx_notification_prefs_type ON notification_preferences(notification_type);

COMMENT ON TABLE notification_preferences IS 'User preferences for notification delivery';
COMMENT ON COLUMN notification_preferences.frequency IS 'How often to send: immediate, hourly, daily, weekly, never';

-- ============================================================================
-- Table 3: direct_messages
-- Purpose: User-to-user direct messaging
-- ============================================================================

CREATE TABLE IF NOT EXISTS direct_messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_message CHECK (sender_id != recipient_id)
);

CREATE INDEX idx_direct_messages_recipient ON direct_messages(recipient_id);
CREATE INDEX idx_direct_messages_sender ON direct_messages(sender_id);
CREATE INDEX idx_direct_messages_conversation ON direct_messages(sender_id, recipient_id);
CREATE INDEX idx_direct_messages_unread ON direct_messages(recipient_id, is_read) WHERE is_read = FALSE;
CREATE INDEX idx_direct_messages_created ON direct_messages(created_at);

COMMENT ON TABLE direct_messages IS 'Direct messages between users';
COMMENT ON COLUMN direct_messages.is_read IS 'Whether recipient has read the message';

-- ============================================================================
-- Table 4: announcements
-- Purpose: Platform-wide and class-specific announcements
-- ============================================================================

CREATE TABLE IF NOT EXISTS announcements (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scope VARCHAR(20) NOT NULL CHECK (scope IN ('platform', 'class')),
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT class_scope_check CHECK (
        (scope = 'platform' AND class_id IS NULL) OR
        (scope = 'class' AND class_id IS NOT NULL)
    )
);

CREATE INDEX idx_announcements_scope ON announcements(scope);
CREATE INDEX idx_announcements_class ON announcements(class_id);
CREATE INDEX idx_announcements_active ON announcements(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_announcements_expires ON announcements(expires_at);
CREATE INDEX idx_announcements_created ON announcements(created_at);

COMMENT ON TABLE announcements IS 'Platform-wide and class-specific announcements';
COMMENT ON COLUMN announcements.scope IS 'Scope: platform (all users) or class (specific class)';
COMMENT ON COLUMN announcements.is_active IS 'Whether announcement is currently active';
COMMENT ON COLUMN announcements.expires_at IS 'When announcement expires (NULL = never)';

-- ============================================================================
-- Table 5: notification_templates
-- Purpose: Reusable notification templates
-- ============================================================================

CREATE TABLE IF NOT EXISTS notification_templates (
    id SERIAL PRIMARY KEY,
    template_key VARCHAR(100) NOT NULL UNIQUE,
    notification_type VARCHAR(50) NOT NULL,
    title_template VARCHAR(200) NOT NULL,
    message_template TEXT NOT NULL,
    action_url_template VARCHAR(500),
    default_priority VARCHAR(20) DEFAULT 'normal',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notification_templates_key ON notification_templates(template_key);
CREATE INDEX idx_notification_templates_type ON notification_templates(notification_type);

COMMENT ON TABLE notification_templates IS 'Reusable templates for notifications';
COMMENT ON COLUMN notification_templates.template_key IS 'Unique key for template (e.g., assignment_due_soon)';
COMMENT ON COLUMN notification_templates.title_template IS 'Title with {{placeholders}}';
COMMENT ON COLUMN notification_templates.message_template IS 'Message with {{placeholders}}';

-- ============================================================================
-- Functions and Triggers
-- ============================================================================

-- Function: Auto-mark message as creating notification
CREATE OR REPLACE FUNCTION create_message_notification()
RETURNS TRIGGER AS $$
BEGIN
    -- Create notification for recipient
    INSERT INTO notifications (
        user_id,
        notification_type,
        title,
        message,
        action_url,
        reference_type,
        reference_id,
        priority
    ) VALUES (
        NEW.recipient_id,
        'direct_message',
        'New message from user',
        LEFT(NEW.message, 100) || CASE WHEN LENGTH(NEW.message) > 100 THEN '...' ELSE '' END,
        '/dashboard/messages',
        'direct_message',
        NEW.id,
        'normal'
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_create_message_notification ON direct_messages;
CREATE TRIGGER trg_create_message_notification
    AFTER INSERT ON direct_messages
    FOR EACH ROW
    EXECUTE FUNCTION create_message_notification();

-- Function: Mark notification as read
CREATE OR REPLACE FUNCTION mark_notification_read()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_read = TRUE AND OLD.is_read = FALSE THEN
        NEW.read_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_mark_notification_read ON notifications;
CREATE TRIGGER trg_mark_notification_read
    BEFORE UPDATE ON notifications
    FOR EACH ROW
    EXECUTE FUNCTION mark_notification_read();

-- Function: Mark message as read
CREATE OR REPLACE FUNCTION mark_message_read()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.is_read = TRUE AND OLD.is_read = FALSE THEN
        NEW.read_at := NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_mark_message_read ON direct_messages;
CREATE TRIGGER trg_mark_message_read
    BEFORE UPDATE ON direct_messages
    FOR EACH ROW
    EXECUTE FUNCTION mark_message_read();

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- View: Unread notifications per user
CREATE OR REPLACE VIEW unread_notifications_count AS
SELECT 
    user_id,
    COUNT(*) as unread_count,
    COUNT(*) FILTER (WHERE priority = 'urgent') as urgent_count,
    COUNT(*) FILTER (WHERE priority = 'high') as high_count
FROM notifications
WHERE is_read = FALSE
GROUP BY user_id;

-- View: Recent notifications (last 30 days)
CREATE OR REPLACE VIEW recent_notifications AS
SELECT *
FROM notifications
WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY created_at DESC;

-- View: Active announcements
CREATE OR REPLACE VIEW active_announcements AS
SELECT *
FROM announcements
WHERE is_active = TRUE
    AND (expires_at IS NULL OR expires_at > NOW())
ORDER BY priority DESC, created_at DESC;

-- View: Message conversations
CREATE OR REPLACE VIEW message_conversations AS
SELECT DISTINCT
    CASE 
        WHEN sender_id < recipient_id THEN sender_id
        ELSE recipient_id
    END as user1_id,
    CASE 
        WHEN sender_id < recipient_id THEN recipient_id
        ELSE sender_id
    END as user2_id,
    MAX(created_at) as last_message_at,
    COUNT(*) as message_count,
    COUNT(*) FILTER (WHERE is_read = FALSE) as unread_count
FROM direct_messages
GROUP BY user1_id, user2_id;

-- ============================================================================
-- Sample Notification Templates
-- ============================================================================

INSERT INTO notification_templates (template_key, notification_type, title_template, message_template, action_url_template, default_priority)
VALUES 
    ('assignment_created', 'assignment', 'New Assignment: {{assignment_name}}', 'A new assignment has been posted in {{class_name}}', '/dashboard/assignments/{{assignment_id}}', 'normal'),
    ('assignment_due_soon', 'assignment', 'Assignment Due Soon', '{{assignment_name}} is due in {{hours}} hours', '/dashboard/assignments/{{assignment_id}}', 'high'),
    ('goal_milestone', 'goal', 'Goal Milestone Reached!', 'You reached {{percentage}}% of your goal: {{goal_name}}', '/dashboard/goals/{{goal_id}}', 'normal'),
    ('goal_completed', 'goal', 'Goal Completed!', 'Congratulations! You completed: {{goal_name}}', '/dashboard/goals/{{goal_id}}', 'high'),
    ('achievement_unlocked', 'achievement', 'Achievement Unlocked!', 'You earned: {{achievement_name}}', '/dashboard/achievements', 'high'),
    ('level_up', 'achievement', 'Level Up!', 'You reached level {{level}}!', '/dashboard/profile', 'high'),
    ('friend_request', 'social', 'New Friend Request', '{{sender_name}} sent you a friend request', '/dashboard/friends', 'normal'),
    ('group_invitation', 'social', 'Group Invitation', 'You were invited to join {{group_name}}', '/dashboard/groups/{{group_id}}', 'normal'),
    ('study_reminder', 'study', 'Study Reminder', 'Time to study for {{class_name}}', '/dashboard/sessions', 'normal')
ON CONFLICT (template_key) DO NOTHING;

-- ============================================================================
-- End of Schema 012
-- ============================================================================
