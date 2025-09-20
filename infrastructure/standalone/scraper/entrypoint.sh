#!/bin/bash
set -e

echo "🕷️  RetailFlux Scraper (Standalone Mode)"
echo "========================================"

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
while ! pg_isready -h "${POSTGRES_HOST:-localhost}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
  echo "  Database not ready, waiting 3 seconds..."
  sleep 3
done
echo "✅ Database connection established"

# Log configuration info (without sensitive data)
echo "📋 Scraper Configuration:"
echo "  - Environment: ${APP_ENV:-production}"
echo "  - Database Host: ${POSTGRES_HOST:-localhost}"
echo "  - Database Name: ${POSTGRES_DB}"
echo "  - Scraper Mode: ${SCRAPER_MODE:-wait}"
echo "  - Spider: ${SPIDER_NAME:-edeka24_spider}"
echo "  - Max Items: ${SCRAPER_MAX_ITEMS:-1000}"
echo "  - Max Pages: ${SCRAPER_MAX_PAGES:-100}"

# Set up environment
export PYTHONPATH=/app
cd /app/services/scraper

# Handle different modes
MODE=${1:-${SCRAPER_MODE:-wait}}

case "$MODE" in
    "wait")
        echo "⏸️  Scraper in WAIT mode - Ready for scheduled execution"
        echo "  Use 'docker exec <container> /usr/local/bin/entrypoint.sh run' to execute scraping"
        echo "  Or set SCRAPER_MODE=run to start immediately"
        
        # Keep container alive but don't run scraper
        while true; do
            echo "$(date '+%Y-%m-%d %H:%M:%S') - Scraper waiting for execution command..."
            sleep 3600  # Sleep for 1 hour
        done
        ;;
        
    "run")
        echo "🚀 Starting scraper execution..."
        
        # Set scraper parameters
        SPIDER_NAME=${SPIDER_NAME:-edeka24_spider}
        OUTPUT_FILE=${OUTPUT_FILE:-}
        SCRAPER_ARGS=""
        
        if [ ! -z "$OUTPUT_FILE" ]; then
            SCRAPER_ARGS="-o $OUTPUT_FILE"
        fi
        
        # Log execution start
        echo "📊 Execution Details:"
        echo "  - Spider: $SPIDER_NAME"
        echo "  - Output File: ${OUTPUT_FILE:-none}"
        echo "  - Max Items: ${SCRAPER_MAX_ITEMS:-1000}"
        echo "  - Max Pages: ${SCRAPER_MAX_PAGES:-100}"
        echo "  - Concurrent Requests: ${SCRAPER_CONCURRENT_REQUESTS:-3}"
        echo "  - Download Delay: ${SCRAPER_DOWNLOAD_DELAY:-1}"
        
        # Run the scraper
        echo "🕷️  Executing spider: $SPIDER_NAME"
        python -m scrapy crawl $SPIDER_NAME $SCRAPER_ARGS
        
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ Scraping completed successfully!"
        else
            echo "❌ Scraping failed with exit code: $EXIT_CODE"
            exit $EXIT_CODE
        fi
        ;;
        
    "test")
        echo "🧪 Running scraper in test mode..."
        export SCRAPER_TEST_MODE=true
        export SCRAPER_MAX_ITEMS=${SCRAPER_MAX_ITEMS:-10}
        export SCRAPER_MAX_PAGES=${SCRAPER_MAX_PAGES:-2}
        
        SPIDER_NAME=${SPIDER_NAME:-edeka24_spider}
        echo "🕷️  Testing spider: $SPIDER_NAME (limited to ${SCRAPER_MAX_ITEMS} items)"
        python -m scrapy crawl $SPIDER_NAME
        
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ Test scraping completed successfully!"
        else
            echo "❌ Test scraping failed with exit code: $EXIT_CODE"
            exit $EXIT_CODE
        fi
        ;;
        
    "shell")
        echo "🐚 Starting interactive shell..."
        exec /bin/bash
        ;;
        
    *)
        echo "❓ Unknown mode: $MODE"
        echo "Available modes:"
        echo "  wait  - Keep container alive without running scraper (default)"
        echo "  run   - Execute scraper once"
        echo "  test  - Run scraper in test mode (limited items)"
        echo "  shell - Start interactive shell"
        echo ""
        echo "Usage examples:"
        echo "  docker run scraper:latest wait"
        echo "  docker exec scraper_container /usr/local/bin/entrypoint.sh run"
        echo "  docker run -e SCRAPER_MODE=run scraper:latest"
        exit 1
        ;;
esac