# Production Scraper Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        cron \
        && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r scraper && useradd -r -g scraper scraper

# Copy requirements and install Python dependencies
COPY services/scraper/requirements.txt /usr/src/app/services/scraper/requirements.txt
COPY shared/requirements.txt /usr/src/app/shared/requirements.txt

# Install production dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r services/scraper/requirements.txt
RUN pip install --no-cache-dir -r shared/requirements.txt

# Install additional Scrapy dependencies
RUN pip install --no-cache-dir \
    scrapy \
    itemadapter \
    twisted[tls] \
    lxml \
    Pillow

# Copy project files
COPY services/scraper /usr/src/app/services/scraper
COPY shared /usr/src/app/shared

# Create directories and set permissions
RUN mkdir -p /usr/src/app/data \
    && mkdir -p /usr/src/app/logs \
    && mkdir -p /usr/src/app/services/scraper/modern_scraper/data \
    && mkdir -p /usr/src/app/services/scraper/modern_scraper/logs \
    && mkdir -p /usr/src/app/services/scraper/modern_scraper/debug \
    && chown -R scraper:scraper /usr/src/app

# Copy cron jobs
COPY infrastructure/docker/scraper-crontab /etc/cron.d/scraper-jobs
RUN chmod 0644 /etc/cron.d/scraper-jobs

# Switch to non-root user
USER scraper

# Set PYTHONPATH
ENV PYTHONPATH=/usr/src/app

# Default command
CMD ["python", "services/scraper/docker_run_spider.py"]