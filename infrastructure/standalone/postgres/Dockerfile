# RetailFlux PostgreSQL - Standalone Production Dockerfile
FROM pgvector/pgvector:pg15

# Install additional extensions and tools
RUN apt-get update && apt-get install -y \
    postgresql-contrib \
    cron \
    logrotate \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy PostgreSQL production configuration
COPY infrastructure/standalone/postgres/postgresql.conf /etc/postgresql/postgresql.conf
COPY infrastructure/standalone/postgres/pg_hba.conf /etc/postgresql/pg_hba.conf

# Copy initialization scripts
COPY infrastructure/standalone/postgres/init-db.sql /docker-entrypoint-initdb.d/01-init.sql
COPY infrastructure/standalone/postgres/init-extensions.sql /docker-entrypoint-initdb.d/02-extensions.sql
COPY infrastructure/standalone/postgres/init-user.sql /docker-entrypoint-initdb.d/03-user.sql

# Copy backup and maintenance scripts
COPY infrastructure/standalone/postgres/backup.sh /usr/local/bin/backup-db
COPY infrastructure/standalone/postgres/maintenance.sh /usr/local/bin/maintenance

# Set up backup schedule (optional)
COPY infrastructure/standalone/postgres/backup-cron /etc/cron.d/postgres-backup
RUN chmod 0644 /etc/cron.d/postgres-backup
RUN crontab /etc/cron.d/postgres-backup

# Make scripts executable
RUN chmod +x /usr/local/bin/backup-db
RUN chmod +x /usr/local/bin/maintenance

# Create backup directory
RUN mkdir -p /backups && chmod 755 /backups

# Configure PostgreSQL to use custom config
ENV POSTGRES_CONFIG_FILE=/etc/postgresql/postgresql.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-postgres} || exit 1

# Expose port
EXPOSE 5432

# Use custom entrypoint
COPY infrastructure/standalone/postgres/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["postgres"]