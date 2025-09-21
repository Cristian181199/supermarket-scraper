-- Initialize extensions for RetailFlux database
-- This script runs after the main database initialization

-- Create pgvector extension for AI/ML features
CREATE EXTENSION IF NOT EXISTS vector;

-- Create pg_stat_statements for query performance monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Create additional useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO PUBLIC;
GRANT CREATE ON SCHEMA public TO PUBLIC;

-- Create indexes for better performance (examples - adjust based on your schema)
-- These can be created after your application creates the tables

COMMIT;