# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EdekaProductItem(scrapy.Item):
    # Datos básicos
    name = scrapy.Field()
    price_amount = scrapy.Field() # El precio como número (ej: 2.99)
    price_currency = scrapy.Field() # La moneda (ej: 'EUR')
    sku = scrapy.Field() # El ID de producto único (ej: 'DE123456')

    # URLs
    product_url = scrapy.Field()
    image_url = scrapy.Field()

    # Datps descriptivos
    description = scrapy.Field()
    category = scrapy.Field()

    # Datos de precio por unidad
    base_price_text = scrapy.Field() # El texto completo (ej: "1,99 € / 100 g")

    # Metadatos del scrapeo
    scraped_at = scrapy.Field() # Fecha y hora del scrapeo
    source_supermarket = scrapy.Field() # Nombre del supermercado (ej: "Edeka")
    pass
