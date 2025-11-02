-- Little Monster - Study Tools Schema
-- Migration: 008_study_tools
-- Created: November 2, 2025
-- Description: AI-generated notes, tests, and flashcards

-- ============================================================================
-- NOTE_SOURCES TABLE (links notes to source content)
-- ============================================================================

CREATE TABLE IF NOT EXISTS note_sources (
    id SERIAL PRIMARY KEY,
    note_id INTEGER NOT NULL REFERENCES study_notes(id) ON DELETE CASCADE,
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('recording', 'photo', 'textbook', 'manual')),
    source_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_note_sources_note ON note_sources(note_id);
CREATE INDEX idx_note_sources_source ON note_sources(source_type, source_id);

-- Enhance existing study_notes table
ALTER TABLE study_notes ADD COLUMN IF NOT EXISTS is_ai_generated BOOLEAN DEFAULT false;
ALTER TABLE study_notes ADD COLUMN IF NOT EXISTS vector_id VARCHAR(100);
ALTER TABLE study_notes ADD COLUMN IF NOT EXISTS class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS idx_notes_class ON study_notes(class_id);

-- ============================================================================
-- GENERATED_TESTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS generated_tests (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question_count INTEGER DEFAULT 0,
    time_limit_minutes INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tests_class ON generated_tests(class_id, created_at DESC);
CREATE INDEX idx_tests_user ON generated_tests(user_id);

-- ============================================================================
-- TEST_QUESTIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS test_questions (
    id SERIAL PRIMARY KEY,
    test_id INTEGER NOT NULL REFERENCES generated_tests(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) CHECK (question_type IN ('multiple_choice', 'true_false', 'short_answer', 'essay')),
    correct_answer TEXT,
    options JSONB,
    explanation TEXT,
    points INTEGER DEFAULT 1,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_test ON test_questions(test_id, order_index);

-- ============================================================================
-- TEST_ATTEMPTS TABLE (track student test taking)
-- ============================================================================

CREATE TABLE IF NOT EXISTS test_attempts (
    id SERIAL PRIMARY KEY,
    test_id INTEGER NOT NULL REFERENCES generated_tests(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    score INTEGER,
    max_score INTEGER,
    answers JSONB,
    time_taken_seconds INTEGER
);

CREATE INDEX idx_attempts_test ON test_attempts(test_id);
CREATE INDEX idx_attempts_user ON test_attempts(user_id, completed_at DESC);

-- ============================================================================
-- FLASHCARD_DECKS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS flashcard_decks (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    card_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_decks_class ON flashcard_decks(class_id, created_at DESC);
CREATE INDEX idx_decks_user ON flashcard_decks(user_id);

-- ============================================================================
-- FLASHCARDS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS flashcards (
    id SERIAL PRIMARY KEY,
    deck_id INTEGER NOT NULL REFERENCES flashcard_decks(id) ON DELETE CASCADE,
    front_text TEXT NOT NULL,
    back_text TEXT NOT NULL,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cards_deck ON flashcards(deck_id, order_index);

-- ============================================================================
-- FLASHCARD_REVIEWS TABLE (spaced repetition tracking)
-- ============================================================================

CREATE TABLE IF NOT EXISTS flashcard_reviews (
    id SERIAL PRIMARY KEY,
    card_id INTEGER NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quality INTEGER CHECK (quality >= 0 AND quality <= 5),
    next_review_date TIMESTAMP,
    interval_days INTEGER DEFAULT 1,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,
    reviewed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_card ON flashcard_reviews(card_id, reviewed_at DESC);
CREATE INDEX idx_reviews_user_next ON flashcard_reviews(user_id, next_review_date);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE TRIGGER update_tests_updated_at
    BEFORE UPDATE ON generated_tests
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_decks_updated_at
    BEFORE UPDATE ON flashcard_decks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cards_updated_at
    BEFORE UPDATE ON flashcards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE note_sources IS 'Links notes to source content (recordings, photos, textbooks)';
COMMENT ON TABLE generated_tests IS 'AI-generated practice tests';
COMMENT ON TABLE test_questions IS 'Questions for generated tests';
COMMENT ON TABLE test_attempts IS 'Student test-taking history';
COMMENT ON TABLE flashcard_decks IS 'Flashcard deck collections';
COMMENT ON TABLE flashcards IS 'Individual flashcards';
COMMENT ON TABLE flashcard_reviews IS 'Spaced repetition review history';
