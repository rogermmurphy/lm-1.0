-- Content Management Schema
-- PostgreSQL Schema for TTS audio, recordings, and study materials

-- Text-to-Speech Audio Files Table
CREATE TABLE IF NOT EXISTS tts_audio_files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Audio generation details
    text TEXT NOT NULL,
    voice VARCHAR(100),
    provider VARCHAR(50),  -- 'azure', 'coqui'
    
    -- File information
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    duration FLOAT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audio Recordings Table
CREATE TABLE IF NOT EXISTS recordings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- File information
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    duration FLOAT,
    recording_type VARCHAR(50) DEFAULT 'other',  -- 'lecture', 'note', 'other'
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Study Materials Table
CREATE TABLE IF NOT EXISTS study_materials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Material details
    title VARCHAR(500) NOT NULL,
    content TEXT,
    file_path VARCHAR(500),
    subject VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_tts_audio_user_id ON tts_audio_files(user_id);
CREATE INDEX IF NOT EXISTS idx_tts_audio_created_at ON tts_audio_files(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_tts_audio_provider ON tts_audio_files(provider);

CREATE INDEX IF NOT EXISTS idx_recordings_user_id ON recordings(user_id);
CREATE INDEX IF NOT EXISTS idx_recordings_created_at ON recordings(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_recordings_type ON recordings(recording_type);

CREATE INDEX IF NOT EXISTS idx_study_materials_user_id ON study_materials(user_id);
CREATE INDEX IF NOT EXISTS idx_study_materials_subject ON study_materials(subject);
CREATE INDEX IF NOT EXISTS idx_study_materials_created_at ON study_materials(created_at DESC);

-- Trigger for study_materials updated_at
CREATE TRIGGER update_study_materials_updated_at 
    BEFORE UPDATE ON study_materials
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Table comments
COMMENT ON TABLE tts_audio_files IS 'Text-to-speech generated audio files';
COMMENT ON TABLE recordings IS 'User-uploaded or recorded audio files';
COMMENT ON TABLE study_materials IS 'Study materials for RAG-enhanced tutoring';

-- Column comments
COMMENT ON COLUMN tts_audio_files.provider IS 'TTS provider: azure, coqui';
COMMENT ON COLUMN recordings.recording_type IS 'Recording type: lecture, note, other';
COMMENT ON COLUMN study_materials.content IS 'Text content for RAG indexing';
