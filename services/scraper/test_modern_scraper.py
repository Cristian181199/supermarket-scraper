#!/usr/bin/env python3
"""
Test Modern Scraper

Script para probar el scraper moderno en entorno de desarrollo.
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Change to the scraper directory
os.chdir(Path(__file__).parent / "modern_scraper")

def test_scrapers():
    """Ejecuta los spiders de prueba."""
    
    print("🧪 Testing Modern Scraper Infrastructure")
    print("=" * 50)
    
    # Get settings for development environment
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'modern_scraper.settings.development'
    settings = get_project_settings()
    
    print(f"📊 Environment: {settings.get('ENVIRONMENT', 'unknown')}")
    print(f"🕷️  Bot name: {settings.get('BOT_NAME')}")
    print(f"📋 Item pipelines: {len(settings.get('ITEM_PIPELINES', {}))}")
    print(f"⏱️  Download delay: {settings.get('DOWNLOAD_DELAY')}s")
    print(f"📦 Item limit: {settings.get('CLOSESPIDER_ITEMCOUNT')}")
    print()
    
    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Add spiders to test
    test_spiders = [
        # 'test_spider',  # Test spider with sample data
        'edeka24_spider',  # Real Edeka24 spider
        # 'mock_edeka_spider',  # Mock Edeka spider  
    ]
    
    for spider_name in test_spiders:
        print(f"🚀 Starting {spider_name}...")
        process.crawl(spider_name)
    
    # Start the crawling process
    print("🏁 Starting crawl process...")
    process.start()
    
    print("✅ Test completed!")
    print()
    print("📁 Check the following files for results:")
    print("  - data/dev_products_*.jsonl (scraped products)")
    print("  - debug/debug_*.log (debug information)")
    print("  - logs/dev_scraper.log (spider logs)")


if __name__ == "__main__":
    try:
        test_scrapers()
    except KeyboardInterrupt:
        print("\n⛔ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
