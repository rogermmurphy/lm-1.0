-- Presentation Jobs Table
-- Stores async presentation generation jobs

CREATE TABLE IF NOT EXISTS presentation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    topic VARCHAR(500) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    subject VARCHAR(100) DEFAULT 'default',
    
    -- Presenton API details
    presenton_id VARCHAR(255),
    presenton_url VARCHAR(500),
    presenton_file_path VARCHAR(500),
    
    -- Job configuration
    n_slides INTEGER DEFAULT 5,
    language VARCHAR(50) DEFAULT 'English',
    template VARCHAR(100) DEFAULT 'general',
    tone VARCHAR(50) DEFAULT 'educational',
    
    -- Status tracking
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Create indexes separately
CREATE INDEX IF NOT EXISTS idx_status ON presentation_jobs(status);
CREATE INDEX IF NOT EXISTS idx_subject ON presentation_jobs(subject);
CREATE INDEX IF NOT EXISTS idx_user_id ON presentation_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_created_at ON presentation_jobs(created_at);

-- Status values: 'pending', 'processing', 'complete', 'error'
-- Subject values: 'default', 'biology', 'chemistry', 'math', 'history', etc.

-- Comments removed for compatibility
