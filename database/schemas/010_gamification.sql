-- Little Monster - Gamification Schema
-- Migration: 010_gamification
-- Created: November 2, 2025
-- Description: Points, achievements, and leaderboards

-- ============================================================================
-- USER_POINTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_points (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    total_points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    streak_days INTEGER DEFAULT 0,
    last_activity_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_points_user ON user_points(user_id);
CREATE INDEX idx_points_level ON user_points(level DESC, total_points DESC);

-- ============================================================================
-- ACHIEVEMENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_type VARCHAR(50) NOT NULL,
    achievement_name VARCHAR(100) NOT NULL,
    achievement_description TEXT,
    points_awarded INTEGER DEFAULT 0,
    earned_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_achievements_user ON achievements(user_id, earned_at DESC);
CREATE INDEX idx_achievements_type ON achievements(achievement_type);

-- ============================================================================
-- LEADERBOARDS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS leaderboards (
    id SERIAL PRIMARY KEY,
    leaderboard_type VARCHAR(50) NOT NULL CHECK (leaderboard_type IN ('global', 'class', 'school', 'weekly', 'monthly')),
    reference_id INTEGER,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    rank INTEGER,
    period_start DATE,
    period_end DATE,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leaderboard_type_rank ON leaderboards(leaderboard_type, rank);
CREATE INDEX idx_leaderboard_user ON leaderboards(user_id, leaderboard_type);
CREATE INDEX idx_leaderboard_period ON leaderboards(period_start, period_end);

-- ============================================================================
-- POINT_TRANSACTIONS TABLE (audit trail)
-- ============================================================================

CREATE TABLE IF NOT EXISTS point_transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    points_change INTEGER NOT NULL,
    reason VARCHAR(100) NOT NULL,
    reference_type VARCHAR(50),
    reference_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transactions_user ON point_transactions(user_id, created_at DESC);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE TRIGGER update_user_points_updated_at
    BEFORE UPDATE ON user_points
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_leaderboards_updated_at
    BEFORE UPDATE ON leaderboards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- FUNCTIONS FOR GAMIFICATION
-- ============================================================================

-- Function to award points
CREATE OR REPLACE FUNCTION award_points(
    p_user_id INTEGER,
    p_points INTEGER,
    p_reason VARCHAR(100),
    p_reference_type VARCHAR(50) DEFAULT NULL,
    p_reference_id INTEGER DEFAULT NULL
) RETURNS void AS $$
BEGIN
    -- Insert transaction
    INSERT INTO point_transactions (user_id, points_change, reason, reference_type, reference_id)
    VALUES (p_user_id, p_points, p_reason, p_reference_type, p_reference_id);
    
    -- Update user points
    INSERT INTO user_points (user_id, total_points, last_activity_date)
    VALUES (p_user_id, p_points, CURRENT_DATE)
    ON CONFLICT (user_id) DO UPDATE
    SET total_points = user_points.total_points + p_points,
        last_activity_date = CURRENT_DATE,
        updated_at = NOW();
        
    -- Update level based on points
    UPDATE user_points
    SET level = CASE
        WHEN total_points >= 10000 THEN 10
        WHEN total_points >= 5000 THEN 9
        WHEN total_points >= 2500 THEN 8
        WHEN total_points >= 1000 THEN 7
        WHEN total_points >= 500 THEN 6
        WHEN total_points >= 250 THEN 5
        WHEN total_points >= 100 THEN 4
        WHEN total_points >= 50 THEN 3
        WHEN total_points >= 20 THEN 2
        ELSE 1
    END
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

-- Function to update streak
CREATE OR REPLACE FUNCTION update_streak(p_user_id INTEGER) RETURNS void AS $$
DECLARE
    v_last_activity DATE;
    v_current_streak INTEGER;
BEGIN
    SELECT last_activity_date, streak_days INTO v_last_activity, v_current_streak
    FROM user_points
    WHERE user_id = p_user_id;
    
    IF v_last_activity = CURRENT_DATE THEN
        -- Already logged activity today
        RETURN;
    ELSIF v_last_activity = CURRENT_DATE - INTERVAL '1 day' THEN
        -- Consecutive day - increment streak
        UPDATE user_points
        SET streak_days = streak_days + 1,
            last_activity_date = CURRENT_DATE
        WHERE user_id = p_user_id;
    ELSE
        -- Streak broken - reset to 1
        UPDATE user_points
        SET streak_days = 1,
            last_activity_date = CURRENT_DATE
        WHERE user_id = p_user_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE user_points IS 'User points, levels, and streaks';
COMMENT ON TABLE achievements IS 'Earned achievements and badges';
COMMENT ON TABLE leaderboards IS 'Leaderboard rankings';
COMMENT ON TABLE point_transactions IS 'Point award/deduction history';

COMMENT ON FUNCTION award_points IS 'Award points to user and update level';
COMMENT ON FUNCTION update_streak IS 'Update daily activity streak';
