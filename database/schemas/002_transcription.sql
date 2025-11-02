-- Speech-to-Text Transcription Schema
-- Extracted from POC 09 - Tested and Validated
-- PostgreSQL Schema for managing async transcription jobs

-- Transcription Jobs Table
CREATE TABLE IF NOT EXISTS transcription_jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Audio file information
    audio_file_path VARCHAR(500) NOT NULL,
    audio_file_size INTEGER,
    audio_duration FLOAT,
    
    -- Job status
    status VARCHAR(50) DEFAULT 'pending',
    -- Status values: 'pending', 'processing', 'completed', 'failed'
    
    -- Processing timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Error handling
    error_message TEXT
);

-- Transcriptions Table (completed transcriptions)
CREATE TABLE IF NOT EXISTS transcriptions (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL UNIQUE REFERENCES transcription_jobs(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Transcription results
    text TEXT NOT NULL,
    confidence FLOAT,
    language VARCHAR(10),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_transcription_jobs_user_id ON transcription_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_transcription_jobs_status ON transcription_jobs(status);
CREATE INDEX IF NOT EXISTS idx_transcription_jobs_created_at ON transcription_jobs(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_transcriptions_user_id ON transcriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_job_id ON transcriptions(job_id);
CREATE INDEX IF NOT EXISTS idx_transcriptions_created_at ON transcriptions(created_at DESC);

-- Table comments
COMMENT ON TABLE transcription_jobs IS 'Async transcription job queue';
COMMENT ON TABLE transcriptions IS 'Completed speech-to-text transcriptions';

-- Column comments
COMMENT ON COLUMN transcription_jobs.status IS 'Job status: pending, processing, completed, failed';
COMMENT ON COLUMN transcriptions.text IS 'Transcribed text from audio';
COMMENT ON COLUMN transcriptions.confidence IS 'Transcription confidence score (0-1)';
COMMENT ON COLUMN transcriptions.language IS 'Detected or specified language code';
