import scrapy
import re
from datetime import datetime
from edeka_scraper.items import EdekaProductItem

class EdekaSpider(scrapy.Spider):
    """
    A spider to crawl and scrape product data from edeka24.de.
    It starts by parsing sitemaps to find product URLs and then
    extracts details from each product page.
    """

    # 1. A unique name for the spider.
    name = 'edeka'

    # (Optional) The domain(s) this spider is allowed to crawl.
    allowed_domains = ['edeka24.de']

    # 2. The list of URLs where the spider will begin to crawl.
    start_urls = ['https://www.edeka24.de/sitemaps/sitemap-index.xml']

    # 3. The method that is automatically called to handle the response
    #    for the URLs in start_urls.
    def parse(self, response):
        """
        Parses the main sitemap index to find product sitemaps.
        """
        self.logger.info(f'Parsing the sitemap INDEX...')
        # Sitemaps are XML files, and Scrapy handles them automatically.
        # We need to register the namespace to use XPath selectors.
        response.selector.register_namespace('s', 'http://www.sitemaps.org/schemas/sitemap/0.9')

        # Use XPath to extract all sitemap URLs that contain 'products'.
        product_sitemaps = response.xpath("//s:loc[contains(text(), 'products')]/text()").getall()

        self.logger.info(f'Found product sitemaps: {product_sitemaps}')
        # For each product sitemap, send a request to parse it.
        for sitemap_url in product_sitemaps:
            yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)


    def parse_sitemap(self, response):
        """
        Parses an individual product sitemap to extract all product URLs.
        """
        self.logger.info(f"Parsing product sitemap: {response.url}")
        response.selector.register_namespace('s', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        product_urls = response.xpath('//s:loc/text()').getall()
        self.logger.info(f"Found {len(product_urls)} product URLs in this sitemap.")

        # For testing, limit the number of products to scrape.
        # Remove `[:5]` to scrape all products.
        for url in product_urls[:5]:
            yield scrapy.Request(url, callback=self.parse_product)


    def parse_product(self, response):
        """
        Parses a product page to extract its details.
        """
        # Instantiate the item to store the scraped data.
        item = EdekaProductItem()

        # --- Extract Category Path ---
        # Use .getall() to get a list of all category names.
        # Skip the first element 'Startseite' (Homepage) with [1:].
        category_list = response.css('div.breadcrumb li a::text').getall()
        item['category_path'] = [cat.strip() for cat in category_list[1:]]

        # --- Fill in the Item Fields ---
        item['store_name'] = 'Edeka24' # Fixed value for this spider
        item['name'] = response.css('div.detail-description h1::text').get(default='').strip()
        
        # Extract and clean the price.
        price_text = response.css('div.price::text').get()
        if price_text:
            match = re.search(r'(\d+,\d+)', price_text)
            if match:
                # Convert price from '1,23' to a float 1.23
                item['price_amount'] = float(match.group(1).replace(',', '.'))

        item['price_currency'] = 'EUR'
        item['sku'] = response.css('div[itemprop="sku"]::text').get(default='N/A').strip()
        item['product_url'] = response.url
        
        # Construct the full image URL.
        img_src = response.css('div.detail-image img::attr(src)').get()
        item['image_url'] = response.urljoin(img_src)
        
        # Combine all parts of the description into a single string.
        description_parts = response.css('div#description *::text').getall()
        item['description'] = " ".join(part.strip() for part in description_parts if part.strip())
        
        # Extract the base price text (e.g., "€1.99 / 100g").
        base_price_text = response.xpath("//li[contains(., 'Grundpreis')]/text()").get()
        item['base_price_text'] = base_price_text.strip() if base_price_text else 'N/A'
        
        # Add a timestamp for when the item was scraped.
        item['scraped_at'] = datetime.utcnow()

        # Return the item to be processed by the pipeline.
        yield item