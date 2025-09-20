-- PostgreSQL User Setup for RetailFlux
-- =====================================

-- Create application user if it doesn't exist
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = '${POSTGRES_USER}') THEN

      CREATE ROLE "${POSTGRES_USER}" LOGIN PASSWORD '${POSTGRES_PASSWORD}';
   END IF;
END
$do$;

-- Grant necessary privileges
ALTER USER "${POSTGRES_USER}" CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE "${POSTGRES_DB}" TO "${POSTGRES_USER}";
GRANT ALL ON SCHEMA public TO "${POSTGRES_USER}";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "${POSTGRES_USER}";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "${POSTGRES_USER}";

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "${POSTGRES_USER}";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "${POSTGRES_USER}";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO "${POSTGRES_USER}";

-- Grant extension usage
GRANT USAGE ON SCHEMA public TO "${POSTGRES_USER}";

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'User "${POSTGRES_USER}" created and configured successfully';
    RAISE NOTICE 'Database: "${POSTGRES_DB}"';
    RAISE NOTICE 'Privileges: ALL on database and schema public';
END $$;