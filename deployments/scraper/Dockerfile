# Scraper Production Dockerfile for independent deployment in Dokploy
# This creates an optimized production image for the RetailFlux Scraper
# Can be run as scheduled job or as a service

FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        g++ \
        libpq-dev \
        cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/scraper/requirements.txt ./
COPY shared/requirements.txt ./shared/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r shared/requirements.txt

# Copy application code
COPY services/scraper/ ./services/scraper/
COPY shared/ ./shared/

# Set Python path
ENV PYTHONPATH=/usr/src/app

# Create non-root user for security
RUN groupadd -r retailflux && useradd -r -g retailflux retailflux \
    && mkdir -p /usr/src/app/logs \
    && mkdir -p /usr/src/app/data \
    && chown -R retailflux:retailflux /usr/src/app

# Copy entrypoint script
COPY deployments/scraper/entrypoint.sh ./
RUN chmod +x ./entrypoint.sh && chown retailflux:retailflux ./entrypoint.sh

# Switch to non-root user
USER retailflux

# Health check (for service mode)
HEALTHCHECK --interval=60s --timeout=30s --retries=3 --start-period=60s \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command (can be overridden in Dokploy for scheduled jobs)
CMD ["./entrypoint.sh"]