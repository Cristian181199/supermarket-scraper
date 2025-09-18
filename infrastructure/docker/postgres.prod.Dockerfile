# Production PostgreSQL Dockerfile with optimizations
FROM pgvector/pgvector:pg15

# Install additional extensions and tools
RUN apt-get update && apt-get install -y \
    postgresql-contrib \
    cron \
    logrotate \
    && rm -rf /var/lib/apt/lists/*

# Copy production PostgreSQL configuration
COPY postgres.prod.conf /etc/postgresql/postgresql.conf

# Copy initialization scripts
COPY postgres-init.sql /docker-entrypoint-initdb.d/
COPY postgres-backup.sh /usr/local/bin/backup-db
COPY postgres-maintenance.sh /usr/local/bin/maintenance

# Set up backup schedule
COPY postgres-crontab /etc/cron.d/postgres-backup
RUN chmod 0644 /etc/cron.d/postgres-backup
RUN crontab /etc/cron.d/postgres-backup

# Make scripts executable
RUN chmod +x /usr/local/bin/backup-db
RUN chmod +x /usr/local/bin/maintenance

# Create backup directory
RUN mkdir -p /backups

# Expose port
EXPOSE 5432