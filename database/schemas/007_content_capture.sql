-- Little Monster - Content Capture Schema
-- Migration: 007_content_capture
-- Created: November 2, 2025
-- Description: Photos, textbooks, and enhanced recordings

-- ============================================================================
-- PHOTOS TABLE (for whiteboard/notes capture)
-- ============================================================================

CREATE TABLE IF NOT EXISTS photos (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    image_url TEXT NOT NULL,
    extracted_text TEXT,
    extraction_status VARCHAR(20) DEFAULT 'pending' CHECK (extraction_status IN ('pending', 'processing', 'completed', 'failed')),
    vector_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_photos_class ON photos(class_id, created_at DESC);
CREATE INDEX idx_photos_user ON photos(user_id);
CREATE INDEX idx_photos_extraction_status ON photos(extraction_status);

-- ============================================================================
-- TEXTBOOK_DOWNLOADS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS textbook_downloads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    class_id INTEGER REFERENCES classes(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200),
    isbn VARCHAR(20),
    file_url TEXT NOT NULL,
    file_type VARCHAR(20) DEFAULT 'pdf',
    file_size_bytes BIGINT,
    page_count INTEGER,
    total_chunks INTEGER DEFAULT 0,
    embedding_status VARCHAR(20) DEFAULT 'pending' CHECK (embedding_status IN ('pending', 'processing', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_textbooks_class ON textbook_downloads(class_id);
CREATE INDEX idx_textbooks_user ON textbook_downloads(user_id);
CREATE INDEX idx_textbooks_status ON textbook_downloads(embedding_status);

-- ============================================================================
-- TEXTBOOK_CHUNKS TABLE (for vector search)
-- ============================================================================

CREATE TABLE IF NOT EXISTS textbook_chunks (
    id SERIAL PRIMARY KEY,
    textbook_id INTEGER NOT NULL REFERENCES textbook_downloads(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    page_number INTEGER,
    content TEXT NOT NULL,
    vector_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(textbook_id, chunk_index)
);

CREATE INDEX idx_chunks_textbook ON textbook_chunks(textbook_id, chunk_index);
CREATE INDEX idx_chunks_vector ON textbook_chunks(vector_id);

-- ============================================================================
-- ENHANCE EXISTING AUDIO_FILES TABLE
-- ============================================================================

-- Add class association and vector ID to existing audio_files
ALTER TABLE audio_files ADD COLUMN IF NOT EXISTS class_id INTEGER REFERENCES classes(id) ON DELETE SET NULL;
ALTER TABLE audio_files ADD COLUMN IF NOT EXISTS vector_id VARCHAR(100);

CREATE INDEX IF NOT EXISTS idx_audio_class ON audio_files(class_id);

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE TRIGGER update_photos_updated_at
    BEFORE UPDATE ON photos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_textbooks_updated_at
    BEFORE UPDATE ON textbook_downloads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE photos IS 'Captured photos of whiteboard, notes, etc.';
COMMENT ON TABLE textbook_downloads IS 'Uploaded textbooks and PDFs';
COMMENT ON TABLE textbook_chunks IS 'Chunked textbook content for vector search';

COMMENT ON COLUMN photos.extraction_status IS 'OCR extraction status';
COMMENT ON COLUMN photos.vector_id IS 'Vector DB ID for semantic search';
COMMENT ON COLUMN textbook_downloads.embedding_status IS 'Vector embedding status';
COMMENT ON COLUMN textbook_chunks.vector_id IS 'Vector DB ID for this chunk';
