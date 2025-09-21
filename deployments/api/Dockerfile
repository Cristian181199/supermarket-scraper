# API Production Dockerfile for independent deployment in Dokploy
# This creates an optimized production image for the RetailFlux API

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
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY services/api/requirements.txt ./
COPY shared/requirements.txt ./shared/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r shared/requirements.txt

# Copy application code
COPY services/api/ ./services/api/
COPY shared/ ./shared/

# Set Python path
ENV PYTHONPATH=/usr/src/app

# Create non-root user for security
RUN groupadd -r retailflux && useradd -r -g retailflux retailflux \
    && mkdir -p /usr/src/app/logs \
    && chown -R retailflux:retailflux /usr/src/app

# Switch to non-root user
USER retailflux

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Production command
CMD ["python", "-m", "uvicorn", "services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]