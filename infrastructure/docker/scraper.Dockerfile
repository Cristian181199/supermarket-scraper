# Scraper Service Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY services/scraper/requirements.txt /usr/src/app/services/scraper/requirements.txt
RUN pip install --no-cache-dir -r services/scraper/requirements.txt

# Install additional dependencies for Scrapy
RUN pip install --no-cache-dir \
    scrapy \
    itemadapter \
    twisted[tls] \
    lxml \
    Pillow

# Copy project files
COPY services/scraper /usr/src/app/services/scraper
COPY shared /usr/src/app/shared

# Set PYTHONPATH
ENV PYTHONPATH=/usr/src/app

# Create directories for scrapy outputs
RUN mkdir -p /usr/src/app/services/scraper/modern_scraper/data \
    && mkdir -p /usr/src/app/services/scraper/modern_scraper/logs \
    && mkdir -p /usr/src/app/services/scraper/modern_scraper/debug

# Default command
CMD ["python", "services/scraper/main.py"]
