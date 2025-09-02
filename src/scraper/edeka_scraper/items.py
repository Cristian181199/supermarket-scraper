# Defines the structure for the scraped data (items).
# For more information, see the Scrapy documentation:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EdekaProductItem(scrapy.Item):
    """
    Defines the fields for a product scraped from Edeka.
    Each field represents a piece of data to be collected.
    """

    # --- Relational Data ---
    store_name = scrapy.Field() # Name of the supermarket (e.g., "Edeka24")
    category_path = scrapy.Field() # Hierarchical list of categories (e.g., ['Groceries', 'Beverages'])
    # manufacturer_name = scrapy.Field() # Product manufacturer (e.g., "Coca-Cola") - Currently commented out

    # --- Core Product Information ---
    name = scrapy.Field() # Product name
    price_amount = scrapy.Field() # Price as a numeric value (e.g., 2.99)
    price_currency = scrapy.Field() # Currency (e.g., 'EUR')
    sku = scrapy.Field() # Unique product identifier (e.g., 'DE123456')

    # --- URLs ---
    product_url = scrapy.Field() # URL of the product page
    image_url = scrapy.Field() # URL of the product image

    # --- Descriptive Data ---
    description = scrapy.Field() # Product description text

    # --- Unit Price Data ---
    base_price_text = scrapy.Field() # Full text for the base price (e.g., "1,99 € / 100 g")

    # --- Scraping Metadata ---
    scraped_at = scrapy.Field() # Timestamp of when the item was scraped (UTC)
    pass
