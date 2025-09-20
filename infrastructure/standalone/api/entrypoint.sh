#!/bin/bash
set -e

echo "🚀 Starting RetailFlux API (Standalone Mode)"
echo "============================================="

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
while ! pg_isready -h "${POSTGRES_HOST:-localhost}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
  echo "  Database not ready, waiting 2 seconds..."
  sleep 2
done
echo "✅ Database connection established"

# Run database migrations
echo "📊 Running database migrations..."
cd /app
export PYTHONPATH=/app
python -m alembic upgrade head
echo "✅ Migrations completed"

# Log configuration info (without sensitive data)
echo "📋 API Configuration:"
echo "  - Environment: ${APP_ENV:-production}"
echo "  - Database Host: ${POSTGRES_HOST:-localhost}"
echo "  - Database Name: ${POSTGRES_DB}"
echo "  - API Host: ${API_HOST:-0.0.0.0}"
echo "  - API Port: ${API_PORT:-8000}"
echo "  - Workers: ${WORKER_PROCESSES:-2}"
echo "  - Domain: ${DOMAIN:-api.retailflux.de}"

# Set defaults
export API_HOST=${API_HOST:-0.0.0.0}
export API_PORT=${API_PORT:-8000}
export WORKER_PROCESSES=${WORKER_PROCESSES:-2}
export LOG_LEVEL=${LOG_LEVEL:-info}

# Start Gunicorn with production settings
echo "🌟 Starting API server..."
exec gunicorn services.api.main:app \
    --workers ${WORKER_PROCESSES} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind ${API_HOST}:${API_PORT} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${LOG_LEVEL} \
    --keepalive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 60 \
    --graceful-timeout 30