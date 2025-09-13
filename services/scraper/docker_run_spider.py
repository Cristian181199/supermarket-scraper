#!/usr/bin/env python3
"""
Docker entry point for running Scrapy spiders in containerized environment.
This script sets up the environment and runs the specified spider.
"""
import os
import sys
import subprocess
import time
import argparse
from pathlib import Path

def wait_for_database():
    """Wait for the database to be ready."""
    import psycopg2
    from psycopg2 import OperationalError
    
    db_config = {
        'host': os.getenv('POSTGRES_HOST', 'postgres_db'),
        'port': int(os.getenv('POSTGRES_PORT', '5432')),
        'database': os.getenv('POSTGRES_DB', 'products_db'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    }
    
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(**db_config)
            conn.close()
            print(f"✅ Database connection successful!")
            return True
        except OperationalError as e:
            retry_count += 1
            print(f"⏳ Waiting for database... ({retry_count}/{max_retries}) - {e}")
            time.sleep(2)
    
    print("❌ Database connection failed after maximum retries")
    return False

def run_spider(spider_name='edeka24_spider', output_file=None):
    """Run the specified spider with Scrapy."""
    
    # Change to the scraper directory
    scraper_dir = Path('/usr/src/app/services/scraper')
    os.chdir(scraper_dir)
    
    # Set environment variables
    os.environ['PYTHONPATH'] = '/usr/src/app'
    
    # Build the command
    cmd = ['python', '-m', 'scrapy', 'crawl', spider_name]
    
    if output_file:
        cmd.extend(['-o', output_file])
    
    print(f"🚀 Running spider: {' '.join(cmd)}")
    print(f"📁 Working directory: {scraper_dir}")
    print(f"🐍 Python path: {os.environ.get('PYTHONPATH')}")
    
    # Run the spider
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("✅ Spider completed successfully!")
    else:
        print(f"❌ Spider failed with return code: {result.returncode}")
    
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description='Run Scrapy spider in Docker')
    parser.add_argument('--spider', '-s', default='edeka24_spider', help='Spider name to run')
    parser.add_argument('--output', '-o', help='Output file for scraped data')
    parser.add_argument('--skip-db-wait', action='store_true', help='Skip waiting for database')
    
    args = parser.parse_args()
    
    print("🐳 Docker Scrapy Runner Starting...")
    print(f"📊 Spider: {args.spider}")
    if args.output:
        print(f"📄 Output: {args.output}")
    
    # Wait for database unless skipped
    if not args.skip_db_wait:
        print("⏳ Waiting for database connection...")
        if not wait_for_database():
            print("⚠️  Proceeding without database (will cause errors)")
    else:
        print("⚡ Skipping database wait")
    
    # Run the spider
    exit_code = run_spider(args.spider, args.output)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
