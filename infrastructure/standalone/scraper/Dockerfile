# RetailFlux Scraper - Standalone Production Dockerfile
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
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r scraperuser && useradd -r -g scraperuser scraperuser

# Copy requirements first (for better caching)
COPY services/scraper/requirements.txt /app/requirements-scraper.txt
COPY shared/requirements.txt /app/requirements-shared.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-scraper.txt \
    && pip install --no-cache-dir -r requirements-shared.txt \
    && pip install --no-cache-dir scrapy itemadapter twisted[tls] lxml Pillow

# Copy application code
COPY services/scraper /app/services/scraper
COPY shared /app/shared

# Create necessary directories
RUN mkdir -p /app/data \
    && mkdir -p /app/logs \
    && mkdir -p /app/services/scraper/modern_scraper/data \
    && mkdir -p /app/services/scraper/modern_scraper/logs \
    && mkdir -p /app/services/scraper/modern_scraper/debug \
    && chown -R scraperuser:scraperuser /app

# Copy entrypoint script
COPY infrastructure/standalone/scraper/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER scraperuser

# Health check (verify scraper can connect to DB)
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "from shared.database.config import test_connection; test_connection()" || exit 1

# Entry point - WAIT MODE by default (no auto-start)
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["wait"]