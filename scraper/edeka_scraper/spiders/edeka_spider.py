import scrapy
import re
from datetime import datetime
from edeka_scraper.items import EdekaProductItem

class EdekaSpider(scrapy.Spider):
    # 1. Nombre unico del spider
    name = 'edeka'

    # (Opcional) Dominio(s) permitido(s) para el spider
    allowed_domains = ['edeka24.de']

    # 2. Lista de URLs con las que empezar
    start_urls = ['https://www.edeka24.de/sitemaps/sitemap_0-products-0.xml']

    # 3. El metodo que se llama automaticamente para manejar la respuesta de las URLs en start_urls
    def parse(self, response):
        # Los sitemaps son ficheros XML. Scrapy los detecta automáticamente.
        # Necesitamos registrar el "namespace" para poder buscar etiquetas con XPath.
        response.selector.register_namespace('s', 'http://www.sitemaps.org/schemas/sitemap/0.9')

        # Usamos XPath para extraer todas las URLs de productos del sitemap
        product_urls = response.xpath('//s:loc/text()').getall()

        self.logger.info(f"Se encontraron {len(product_urls)} URLs de productos en el sitemap.")

        # Para cada URL de producto, creamos una nueva solicitud (Request)
        # para que Scrapy la visite y la procese con el metodo parse_product
        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        # Instanciamos el item
        item = EdekaProductItem()
        
        # Rellenamos los campos usando selectores CSS
        # El método .get() devuelve el primer resultado, o None si no encuentra nada.
        # El método .strip() elimina espacios en blanco al principio y al final.
        item['name'] = response.css('div.detail-description h1::text').get().strip()
        price_text = response.css('div.price::text').get()
        if price_text:
            # Usamos una expresión regular para extraer solo los números y la coma
            match = re.search(r'(\d+,\d+)', price_text)
            if match:
                # Reemplazamos la coma por un punto para convertirlo a número decimal
                item['price_amount'] = float(match.group(1).replace(',', '.'))
        
        item['price_currency'] = 'EUR'

        item['sku'] = response.css('div[itemprop="sku"]::text').get(default='N/A').strip()
        
        # La URL de la imagen a veces es relativa, la convertimos en absoluta
        item['product_url'] = response.url
        img_src = response.css('div.detail-image img::attr(src)').get()
        item['image_url'] = response.urljoin(img_src)
        
        # Usamos .getall() para obtener todo el texto y lo unimos
        description_parts = response.css('div#description *::text').getall()
        item['description'] = " ".join(part.strip() for part in description_parts if part.strip())
        item['category'] = response.css('div.breadcrumb li:last-child a::text').get().strip()
        
        base_price_text = response.xpath("//li[contains(., 'Grundpreis')]/text()").get()
        item['base_price_text'] = base_price_text.strip() if base_price_text else 'N/A'
        
        # Añadimos metadatos
        item['scraped_at'] = datetime.utcnow()
        item['source_supermarket'] = 'Edeka24'

        # Devolvemos el item para que viaje al Pipeline
        yield item