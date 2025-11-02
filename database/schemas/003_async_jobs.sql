-- Async Jobs Queue Schema
-- Extracted from POC 08 - Tested and Validated
-- PostgreSQL Schema for managing background job processing

-- Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Job details
    job_type VARCHAR(50) NOT NULL,
    -- Job types: 'transcription', 'tts', 'presentation', etc.
    
    status VARCHAR(50) DEFAULT 'pending',
    -- Status values: 'pending', 'processing', 'completed', 'failed'
    
    priority INTEGER DEFAULT 0,
    
    -- Job data and results
    payload TEXT,  -- JSON payload
    result TEXT,   -- JSON result
    
    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_job_type ON jobs(job_type);
CREATE INDEX IF NOT EXISTS idx_jobs_user_id ON jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_jobs_priority ON jobs(priority DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_status_priority ON jobs(status, priority DESC) WHERE status = 'pending';

-- Table comments
COMMENT ON TABLE jobs IS 'Async job queue for background processing';

-- Column comments
COMMENT ON COLUMN jobs.job_type IS 'Type of job: transcription, tts, presentation, etc.';
COMMENT ON COLUMN jobs.status IS 'Job status: pending, processing, completed, failed';
COMMENT ON COLUMN jobs.priority IS 'Job priority (higher number = higher priority)';
COMMENT ON COLUMN jobs.payload IS 'JSON payload with job parameters';
COMMENT ON COLUMN jobs.result IS 'JSON result data after job completion';
COMMENT ON COLUMN jobs.retry_count IS 'Number of retry attempts';
COMMENT ON COLUMN jobs.max_retries IS 'Maximum retry attempts before marking failed';
