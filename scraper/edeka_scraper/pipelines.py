# scraper/edeka_scraper/pipelines.py
import psycopg2
from itemadapter import ItemAdapter


class PostgresPipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        # Esta funcion se llama cuando la araña empieza a trabajar
        # Obtenemos la configuracion de la base de datos desde las settings
        settings = spider.settings

        # Conectamos a la base de datos PostgreSQL
        self.connection = psycopg2.connect(
            host=settings.get('POSTGRES_HOST'),
            port=settings.get('POSTGRES_PORT'),
            database=settings.get('POSTGRES_DB'),
            user=settings.get('POSTGRES_USER'),
            password=settings.get('POSTGRES_PASSWORD')
        )
        self.cursor = self.connection.cursor()

        # Creamos la tabla si no existe
        # Es una buena práctica definir los tipos de columna adecuados
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT,
                price_amount NUMERIC(10, 2),
                price_currency VARCHAR(10),
                sku VARCHAR(50),
                product_url TEXT UNIQUE,
                image_url TEXT,
                description TEXT,
                category TEXT,
                base_price_text TEXT,
                scraped_at TIMESTAMP,
                source_supermarket VARCHAR(50)
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        # Esta funcion se llama cuando la araña termina de trabajar
        # Cerramos el cursor y la conexion
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def process_item(self, item, spider):
        # Esta función se llama para cada item que la araña produce.
        # Aquí escribimos la lógica para insertar el item en la base de datos.
        # Usamos ON CONFLICT (sku) DO UPDATE para actualizar productos existentes
        # en lugar de crear duplicados.
        self.cursor.execute("""
            INSERT INTO products (
                name, price_amount, price_currency, sku, product_url,
                image_url, description, category, base_price_text,
                scraped_at, source_supermarket
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_url) DO UPDATE SET
                name = EXCLUDED.name,
                price_amount = EXCLUDED.price_amount,
                price_currency = EXCLUDED.price_currency,
                product_url = EXCLUDED.product_url,
                image_url = EXCLUDED.image_url,
                description = EXCLUDED.description,
                category = EXCLUDED.category,
                base_price_text = EXCLUDED.base_price_text,
                scraped_at = EXCLUDED.scraped_at,
                source_supermarket = EXCLUDED.source_supermarket
        """, (
            item.get('name'),
            item.get('price_amount'),
            item.get('price_currency'),
            item.get('sku'),
            item.get('product_url'),
            item.get('image_url'),
            item.get('description'),
            item.get('category'),
            item.get('base_price_text'),
            item.get('scraped_at'),
            item.get('source_supermarket')
        ))
        self.connection.commit()
        return item