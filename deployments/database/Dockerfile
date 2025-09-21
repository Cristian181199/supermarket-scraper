# PostgreSQL with pgvector extension for production deployment
# This will be deployed as an independent service in Dokploy
# Completely self-contained - no external file dependencies

FROM postgres:16

# Install pgvector extension
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-16-pgvector \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create pgvector initialization script directly in the Dockerfile
RUN echo '-- Initialize extensions for RetailFlux database' > /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '-- This script runs after the main database initialization' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '-- Create pgvector extension for AI/ML features' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'CREATE EXTENSION IF NOT EXISTS vector;' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '-- Create pg_stat_statements for query performance monitoring' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'CREATE EXTENSION IF NOT EXISTS pg_stat_statements;' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '-- Create additional useful extensions' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'CREATE EXTENSION IF NOT EXISTS "pg_trgm";' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '-- Grant necessary permissions' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'GRANT USAGE ON SCHEMA public TO PUBLIC;' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'GRANT CREATE ON SCHEMA public TO PUBLIC;' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo '' >> /docker-entrypoint-initdb.d/init-extensions.sql \
    && echo 'COMMIT;' >> /docker-entrypoint-initdb.d/init-extensions.sql

# Create optimized PostgreSQL configuration for production
RUN echo '# PostgreSQL Configuration for Production' > /etc/postgresql/postgresql.conf \
    && echo '# Optimized for RetailFlux Scraper workloads' >> /etc/postgresql/postgresql.conf \
    && echo '' >> /etc/postgresql/postgresql.conf \
    && echo '# Connection Settings' >> /etc/postgresql/postgresql.conf \
    && echo 'listen_addresses = "*"' >> /etc/postgresql/postgresql.conf \
    && echo 'port = 5432' >> /etc/postgresql/postgresql.conf \
    && echo 'max_connections = 100' >> /etc/postgresql/postgresql.conf \
    && echo '' >> /etc/postgresql/postgresql.conf \
    && echo '# Memory Settings' >> /etc/postgresql/postgresql.conf \
    && echo 'shared_buffers = 256MB' >> /etc/postgresql/postgresql.conf \
    && echo 'effective_cache_size = 1GB' >> /etc/postgresql/postgresql.conf \
    && echo 'maintenance_work_mem = 64MB' >> /etc/postgresql/postgresql.conf \
    && echo 'checkpoint_completion_target = 0.9' >> /etc/postgresql/postgresql.conf \
    && echo 'wal_buffers = 16MB' >> /etc/postgresql/postgresql.conf \
    && echo 'default_statistics_target = 100' >> /etc/postgresql/postgresql.conf \
    && echo 'random_page_cost = 1.1' >> /etc/postgresql/postgresql.conf \
    && echo 'effective_io_concurrency = 200' >> /etc/postgresql/postgresql.conf \
    && echo '' >> /etc/postgresql/postgresql.conf \
    && echo '# Write-Ahead Logging' >> /etc/postgresql/postgresql.conf \
    && echo 'wal_level = replica' >> /etc/postgresql/postgresql.conf \
    && echo 'max_wal_size = 1GB' >> /etc/postgresql/postgresql.conf \
    && echo 'min_wal_size = 80MB' >> /etc/postgresql/postgresql.conf \
    && echo 'checkpoint_timeout = 5min' >> /etc/postgresql/postgresql.conf \
    && echo '' >> /etc/postgresql/postgresql.conf \
    && echo '# Logging' >> /etc/postgresql/postgresql.conf \
    && echo 'log_destination = "stderr"' >> /etc/postgresql/postgresql.conf \
    && echo 'logging_collector = on' >> /etc/postgresql/postgresql.conf \
    && echo 'log_directory = "/var/log/postgresql"' >> /etc/postgresql/postgresql.conf \
    && echo 'log_filename = "postgresql-%Y-%m-%d_%H%M%S.log"' >> /etc/postgresql/postgresql.conf \
    && echo 'log_rotation_age = 1d' >> /etc/postgresql/postgresql.conf \
    && echo 'log_rotation_size = 10MB' >> /etc/postgresql/postgresql.conf \
    && echo 'log_min_duration_statement = 1000' >> /etc/postgresql/postgresql.conf \
    && echo '' >> /etc/postgresql/postgresql.conf \
    && echo '# Extensions' >> /etc/postgresql/postgresql.conf \
    && echo 'shared_preload_libraries = "pg_stat_statements"' >> /etc/postgresql/postgresql.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 --start-period=40s \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Expose port (internal use only in Dokploy)
EXPOSE 5432

# Use custom config
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]