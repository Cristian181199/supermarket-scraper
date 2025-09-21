# PostgreSQL with pgvector extension for production deployment
# This will be deployed as an independent service in Dokploy

FROM postgres:16

# Install pgvector extension
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-16-pgvector \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy custom postgres configuration for production
COPY deployments/database/postgresql.conf /etc/postgresql/postgresql.conf

# Copy initialization scripts
COPY infrastructure/docker/postgres-init.sql /docker-entrypoint-initdb.d/
COPY deployments/database/init-extensions.sql /docker-entrypoint-initdb.d/

# Copy maintenance and backup scripts
COPY infrastructure/docker/postgres-maintenance.sh /usr/local/bin/
COPY infrastructure/docker/postgres-backup.sh /usr/local/bin/

# Make scripts executable
RUN chmod +x /usr/local/bin/postgres-maintenance.sh \
    && chmod +x /usr/local/bin/postgres-backup.sh

# Set proper permissions
RUN chown -R postgres:postgres /usr/local/bin/postgres-*.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 --start-period=40s \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Expose port (internal use only in Dokploy)
EXPOSE 5432

# Use custom config
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]