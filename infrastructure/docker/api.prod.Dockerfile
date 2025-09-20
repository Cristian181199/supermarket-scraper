# Production API Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ curl postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy requirements and install Python dependencies
COPY services/api/requirements.txt /usr/src/app/services/api/requirements.txt
COPY shared/requirements.txt /usr/src/app/shared/requirements.txt
COPY infrastructure/alembic.ini ./infrastructure/alembic.ini

# Install production dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r services/api/requirements.txt
RUN pip install --no-cache-dir -r shared/requirements.txt
RUN pip install --no-cache-dir gunicorn alembic

# Copy project files
COPY services/api /usr/src/app/services/api
COPY shared /usr/src/app/shared

# Create directories and set permissions
RUN mkdir -p /usr/src/app/logs \
    && chown -R appuser:appuser /usr/src/app

COPY infrastructure/docker/api-entrypoint.prod.sh /usr/local/bin/api-entrypoint.prod.sh
RUN chmod +x /usr/local/bin/api-entrypoint.prod.sh

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set PYTHONPATH
ENV PYTHONPATH=/usr/src/app

# Expose port
EXPOSE 8000

# Default command (can be overridden)
ENTRYPOINT ["/usr/local/bin/api-entrypoint.prod.sh"]