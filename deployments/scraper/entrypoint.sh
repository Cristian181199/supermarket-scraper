#!/bin/bash
set -e

# RetailFlux Scraper Entrypoint Script
# This script provides flexible execution modes for the scraper

echo "Starting RetailFlux Scraper..."
echo "Environment: ${APP_ENV:-production}"
echo "Mode: ${SCRAPER_MODE:-single}"

# Wait for database to be ready
echo "Waiting for database connection..."
python -c "
import os
import time
import psycopg2
from psycopg2 import OperationalError

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        conn.close()
        print('Database is ready!')
        break
    except OperationalError:
        retry_count += 1
        print(f'Database not ready, retrying ({retry_count}/{max_retries})...')
        time.sleep(2)
        
if retry_count >= max_retries:
    print('Failed to connect to database after maximum retries')
    exit(1)
"

# Determine execution mode
case "${SCRAPER_MODE:-single}" in
    "single")
        echo "Running single scraper execution..."
        python services/scraper/run_modern_spider.py ${SCRAPER_ARGS:-}
        ;;
    "scheduled")
        echo "Running scheduled scraper (every ${SCRAPER_INTERVAL:-4h})..."
        while true; do
            echo "$(date): Starting scraping cycle..."
            python services/scraper/run_modern_spider.py ${SCRAPER_ARGS:-}
            echo "$(date): Scraping cycle completed. Sleeping for ${SCRAPER_INTERVAL:-4h}..."
            sleep ${SCRAPER_SLEEP:-14400}  # 4 hours default
        done
        ;;
    "daemon")
        echo "Running scraper in daemon mode..."
        python services/scraper/run_modern_spider.py --daemon ${SCRAPER_ARGS:-}
        ;;
    "edeka")
        echo "Running Edeka scraper specifically..."
        python services/scraper/run_modern_spider.py --market edeka ${SCRAPER_ARGS:-}
        ;;
    *)
        echo "Unknown SCRAPER_MODE: ${SCRAPER_MODE}"
        echo "Available modes: single, scheduled, daemon, edeka"
        exit 1
        ;;
esac

echo "Scraper execution completed."