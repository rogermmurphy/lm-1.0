-- Little Monster - Social & Collaboration Schema
-- Migration: 009_social
-- Created: November 2, 2025
-- Description: Classmate connections, content sharing, study groups

-- ============================================================================
-- CLASSMATE_CONNECTIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS classmate_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    classmate_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'blocked')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, classmate_user_id),
    CHECK (user_id != classmate_user_id)
);

CREATE INDEX idx_connections_user ON classmate_connections(user_id, status);
CREATE INDEX idx_connections_classmate ON classmate_connections(classmate_user_id, status);

-- ============================================================================
-- SHARED_CONTENT TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS shared_content (
    id SERIAL PRIMARY KEY,
    content_type VARCHAR(50) NOT NULL CHECK (content_type IN ('note', 'flashcard_deck', 'test', 'recording', 'photo', 'textbook')),
    content_id INTEGER NOT NULL,
    shared_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shared_with_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    permissions VARCHAR(20) DEFAULT 'view' CHECK (permissions IN ('view', 'edit', 'admin')),
    created_at TIMESTAMP DEFAULT NOW(),
    CHECK (shared_by_user_id != shared_with_user_id)
);

CREATE INDEX idx_shared_content_recipient ON shared_content(shared_with_user_id, content_type);
CREATE INDEX idx_shared_content_sender ON shared_content(shared_by_user_id);
CREATE INDEX idx_shared_content_type ON shared_content(content_type, content_id);

-- ============================================================================
-- STUDY_GROUPS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS study_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL,
    created_by_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT true,
    max_members INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_groups_class ON study_groups(class_id);
CREATE INDEX idx_groups_creator ON study_groups(created_by_user_id);
CREATE INDEX idx_groups_active ON study_groups(is_active);

-- ============================================================================
-- STUDY_GROUP_MEMBERS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS study_group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('admin', 'moderator', 'member')),
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(group_id, user_id)
);

CREATE INDEX idx_group_members_group ON study_group_members(group_id);
CREATE INDEX idx_group_members_user ON study_group_members(user_id);

-- ============================================================================
-- STUDY_GROUP_MESSAGES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS study_group_messages (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    is_deleted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_group_messages_group ON study_group_messages(group_id, created_at DESC);
CREATE INDEX idx_group_messages_user ON study_group_messages(user_id);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE TRIGGER update_connections_updated_at
    BEFORE UPDATE ON classmate_connections
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_groups_updated_at
    BEFORE UPDATE ON study_groups
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE classmate_connections IS 'Student connections and friend requests';
COMMENT ON TABLE shared_content IS 'Content shared between students';
COMMENT ON TABLE study_groups IS 'Collaborative study groups';
COMMENT ON TABLE study_group_members IS 'Study group membership';
COMMENT ON TABLE study_group_messages IS 'Study group chat messages';
