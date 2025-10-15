-- Initialize database with some sample data if needed
-- This file is executed when the PostgreSQL container starts for the first time

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create indexes for better performance
-- These will be created automatically by SQLAlchemy, but we can add additional ones here

-- Example: Add an index on entry content for text search
-- CREATE INDEX IF NOT EXISTS idx_entries_content_search ON entries USING gin(to_tsvector('english', content));

-- Example: Add an index on emotions for faster emotion queries
-- CREATE INDEX IF NOT EXISTS idx_emotions_type_confidence ON emotions(emotion_type, confidence_score);

-- Log successful initialization
INSERT INTO pg_stat_statements_info (dealloc) VALUES (0) ON CONFLICT DO NOTHING;