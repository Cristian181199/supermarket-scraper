#!/usr/bin/env python3
"""
Run Modern Edeka24 Spider

Script para ejecutar el spider moderno de Edeka24 con límites de desarrollo.
Configurado para scrapear 5 productos desde el sitemap.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Change to the scraper directory
os.chdir(Path(__file__).parent)

def run_edeka24_spider():
    """Ejecuta el spider de Edeka24 con configuración de desarrollo."""
    
    print("🏪 Running Edeka24 Modern Spider")
    print("=" * 50)
    print("📍 Mode: Development (5 products from sitemap)")
    print("🌐 Source: https://www.edeka24.de/sitemaps/sitemap_0-products-0.xml")
    print("=" * 50)
    
    # Set working directory to modern_scraper
    os.chdir(Path(__file__).parent / "modern_scraper")
    
    # Get settings for development environment
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'modern_scraper.settings.development'
    settings = get_project_settings()
    
    print(f"📊 Environment: {settings.get('ENVIRONMENT', 'unknown')}")
    print(f"🕷️  Bot name: {settings.get('BOT_NAME')}")
    print(f"📦 Item limit: {settings.get('CLOSESPIDER_ITEMCOUNT')}")
    print(f"⏱️  Download delay: {settings.get('DOWNLOAD_DELAY')}s")
    print(f"🔄 Concurrent requests: {settings.get('CONCURRENT_REQUESTS')}")
    print()
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    print("🚀 Starting Edeka24 spider...")
    process.crawl('edeka24_spider')
    
    # Start the crawling process
    print("🏁 Starting crawl process...")
    process.start()
    
    print("✅ Edeka24 spider completed!")
    print()
    print("📁 Check the following files for results:")
    print("  - data/dev_products_*.jsonl.gz (scraped products)")
    print("  - debug/debug_*.log (debug information)")
    print("  - logs/dev_scraper.log (spider logs)")
    print()
    print("🔍 Results summary:")
    
    # Try to show a quick summary of results
    try:
        import glob
        import gzip
        import json
        
        # Find the most recent data file
        data_files = glob.glob("data/dev_products_*.jsonl.gz")
        if data_files:
            latest_file = max(data_files, key=os.path.getctime)
            print(f"📄 Latest output: {latest_file}")
            
            # Count products
            product_count = 0
            with gzip.open(latest_file, 'rt', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    if 'name' in data and '_metadata' not in data and '_final_metadata' not in data:
                        product_count += 1
            
            print(f"🛒 Products scraped: {product_count}")
        else:
            print("❌ No output files found")
            
    except Exception as e:
        print(f"⚠️  Could not read results: {e}")


if __name__ == "__main__":
    try:
        run_edeka24_spider()
    except KeyboardInterrupt:
        print("\n⛔ Spider interrupted by user")
    except Exception as e:
        print(f"\n❌ Spider failed: {e}")
        import traceback
        traceback.print_exc()
