# This file defines the item pipelines for the Scrapy project.
# Item pipelines are used to process scraped items, for example,
# by cleaning, validating, or storing them in a database.
# For more info, see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from itemadapter import ItemAdapter


class PostgresPipeline:
    """
    A pipeline that connects to a PostgreSQL database and stores scraped items.
    """

    def __init__(self):
        """
        Initializes the pipeline with no active connection or cursor.
        """
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        """
        Called when the spider is opened. This method establishes the
        database connection and creates tables if they don't exist.
        """
        # Retrieve database settings from the spider's configuration
        settings = spider.settings

        # Connect to the PostgreSQL database
        self.connection = psycopg2.connect(
            host=settings.get('POSTGRES_HOST'),
            port=settings.get('POSTGRES_PORT'),
            database=settings.get('POSTGRES_DB'),
            user=settings.get('POSTGRES_USER'),
            password=settings.get('POSTGRES_PASSWORD')
        )
        self.cursor = self.connection.cursor()

        # --- Create Tables if They Don't Exist ---
        # This is a good practice to ensure the database schema is ready.
        self.cursor.execute("""
                            
            CREATE TABLE IF NOT EXISTS stores (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );
                            
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                parent_id INTEGER REFERENCES categories(id),
                -- The combination of name and parent_id must be unique
                UNIQUE(name, parent_id) 
            );
                            
            CREATE TABLE IF NOT EXISTS manufacturers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price_amount NUMERIC(10, 2),
                price_currency VARCHAR(10),
                sku VARCHAR(50),
                product_url TEXT UNIQUE,
                image_url TEXT,
                description TEXT,
                base_price_text TEXT,
                scraped_at TIMESTAMP,
                store_id INTEGER REFERENCES stores(id),
                category_id INTEGER REFERENCES categories(id),
                manufacturer_id INTEGER REFERENCES manufacturers(id)
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        """
        Called when the spider is closed. This method closes the
        database cursor and connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def _process_category_path(self, category_path):
        """
        Processes a list of categories, inserts them hierarchically,
        and returns the ID of the last (most specific) category.
        """
        parent_id = None
        for category_name in category_path:
            # Look for the category with the correct name and parent_id
            self.cursor.execute(
                "SELECT id FROM categories WHERE name = %s AND (parent_id = %s OR parent_id IS NULL AND %s IS NULL)",
                (category_name, parent_id, parent_id)
            )
            result = self.cursor.fetchone()
            
            if result:
                parent_id = result[0] # This will be the parent for the next iteration
            else:
                # If it doesn't exist, create it and get its new ID
                self.cursor.execute(
                    "INSERT INTO categories (name, parent_id) VALUES (%s, %s) RETURNING id",
                    (category_name, parent_id)
                )
                parent_id = self.cursor.fetchone()[0]
                self.connection.commit()
        return parent_id # Return the ID of the last category

    def _get_or_create_id(self, table_name, name):
        """
        A helper function to get the ID of an existing item (like a store or
        manufacturer) or create a new one if it doesn't exist.
        """
        self.cursor.execute(f"SELECT id FROM {table_name} WHERE name = %s", (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            self.cursor.execute(f"INSERT INTO {table_name} (name) VALUES (%s) RETURNING id", (name,))
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def process_item(self, item, spider):
        """
        This method is called for every item produced by the spider.
        It handles the insertion or update of the item in the database.
        """
        adapter = ItemAdapter(item)

        # Get foreign key IDs for relationships
        store_id = self._get_or_create_id('stores', adapter.get('store_name'))
        # Process the full category hierarchy and get the final category ID
        category_id = self._process_category_path(adapter.get('category_path'))
        
        # Only get manufacturer_id if manufacturer_name exists
        manufacturer_name = adapter.get('manufacturer_name')
        manufacturer_id = self._get_or_create_id('manufacturers', manufacturer_name) if manufacturer_name else None


        # --- Insert or Update Product Data ---
        # Using ON CONFLICT (product_url) DO UPDATE to prevent duplicates
        # and update existing products with new information.
        self.cursor.execute("""
            INSERT INTO products (
                name, price_amount, price_currency, sku, product_url, image_url, 
                description, base_price_text, scraped_at, store_id, category_id, manufacturer_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_url) DO UPDATE SET
                name = EXCLUDED.name,
                price_amount = EXCLUDED.price_amount,
                description = EXCLUDED.description,
                base_price_text = EXCLUDED.base_price_text,
                scraped_at = EXCLUDED.scraped_at,
                category_id = EXCLUDED.category_id;
        """, (
            adapter.get('name'),
            adapter.get('price_amount'),
            adapter.get('price_currency'),
            adapter.get('sku'),
            adapter.get('product_url'),
            adapter.get('image_url'),
            adapter.get('description'),
            adapter.get('base_price_text'),
            item.get('scraped_at'),
            store_id,
            category_id,
            manufacturer_id
        ))
        self.connection.commit()
        return item