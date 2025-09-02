# Scrapy settings for the edeka_scraper project.
# For a full list of settings and their documentation, see:
# https://docs.scrapy.org/en/latest/topics/settings.html
import os
from dotenv import load_dotenv

# --- Load Environment Variables ---
# Load variables from the .env file located at the project root.
# __file__ is the path to this settings.py file.
# os.path.dirname is used three times to navigate up to the project root.
# env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
# load_dotenv(dotenv_path=env_path)


# --- General Project Settings ---
BOT_NAME = "edeka_scraper"
SPIDER_MODULES = ["edeka_scraper.spiders"]
NEWSPIDER_MODULE = "edeka_scraper.spiders"

ADDONS = {}


# --- Crawling Politeness ---
# 1. Identify your bot with a descriptive User-Agent.
# It's good practice to include contact information.
USER_AGENT = "EdekaScraper/1.0 (+cristian181199@gmail.com)"

# 2. Obey the rules defined in the target website's robots.txt file.
ROBOTSTXT_OBEY = True

# 3. Configure a download delay to avoid overwhelming the server.
# This helps to be a responsible crawler.
# CONCURRENT_REQUESTS = 16  # Default is 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 20 # A significant delay to be respectful

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "edeka_scraper.middlewares.EdekaScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "edeka_scraper.middlewares.EdekaScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# --- Item Pipelines ---
# 4. Activate your custom pipeline. The number (e.g., 300) indicates
# the order of execution if multiple pipelines are used.
ITEM_PIPELINES = {
    "edeka_scraper.pipelines.PostgresPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# --- Database Configuration ---
# 5. Add database settings using environment variables.
# This keeps sensitive information out of the code.
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres_db')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# --- Feed Export Settings ---
# Set a future-proof value for feed export encoding.
FEED_EXPORT_ENCODING = "utf-8"
