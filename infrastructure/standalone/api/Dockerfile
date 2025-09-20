# RetailFlux API - Standalone Production Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r apiuser && useradd -r -g apiuser apiuser

# Copy requirements first (for better caching)
COPY services/api/requirements.txt /app/requirements-api.txt
COPY shared/requirements.txt /app/requirements-shared.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-api.txt \
    && pip install --no-cache-dir -r requirements-shared.txt \
    && pip install --no-cache-dir gunicorn alembic

# Copy application code
COPY services/api /app/services/api
COPY shared /app/shared
COPY infrastructure/alembic.ini /app/alembic.ini

# Create necessary directories
RUN mkdir -p /app/logs \
    && chown -R apiuser:apiuser /app

# Copy entrypoint script
COPY infrastructure/standalone/api/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER apiuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Entry point
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]