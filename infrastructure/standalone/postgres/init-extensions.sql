-- PostgreSQL Extensions Setup for RetailFlux
-- =============================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Create custom functions
CREATE OR REPLACE FUNCTION normalize_text(text) 
RETURNS text AS $$
BEGIN
    RETURN lower(unaccent($1));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Configure pgvector
ALTER SYSTEM SET shared_preload_libraries = 'vector';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';

-- Vector-specific settings
ALTER SYSTEM SET ivfflat.probes = 10;

-- Reload configuration
SELECT pg_reload_conf();

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL extensions initialized successfully';
    RAISE NOTICE 'Available extensions: vector, uuid-ossp, pg_trgm, unaccent';
END $$;