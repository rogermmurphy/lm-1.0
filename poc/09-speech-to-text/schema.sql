-- Speech-to-Text Transcription Jobs Table
-- PostgreSQL Schema for managing async transcription jobs

CREATE TABLE IF NOT EXISTS transcription_jobs (
    -- Primary identification
    id UUID PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    
    -- File information
    file_name VARCHAR(500) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    
    -- Job status
    status VARCHAR(50) DEFAULT 'pending',
    -- Status values: 'pending', 'processing', 'completed', 'failed'
    
    -- Transcription results
    transcript_text TEXT,
    duration_seconds FLOAT,
    language VARCHAR(10),
    
    -- RAG integration
    auto_load_to_chromadb BOOLEAN DEFAULT true,
    loaded_to_chromadb BOOLEAN DEFAULT false,
    chromadb_collection VARCHAR(100),
    
    -- Organization
    subject VARCHAR(100) DEFAULT 'default',
    
    -- Error handling
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_transcription_user ON transcription_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_transcription_status ON transcription_jobs(status);
CREATE INDEX IF NOT EXISTS idx_transcription_subject ON transcription_jobs(subject);
CREATE INDEX IF NOT EXISTS idx_transcription_created ON transcription_jobs(created_at DESC);

-- Sample query to check pending jobs
-- SELECT id, file_name, status, created_at FROM transcription_jobs WHERE status = 'pending' ORDER BY created_at;

-- Sample query to check user's transcriptions
-- SELECT id, file_name, status, subject, duration_seconds FROM transcription_jobs WHERE user_id = 'test_user' ORDER BY created_at DESC;

-- Sample query to check completed transcriptions in a subject
-- SELECT id, file_name, language, duration_seconds, loaded_to_chromadb FROM transcription_jobs WHERE subject = 'biology' AND status = 'completed';
