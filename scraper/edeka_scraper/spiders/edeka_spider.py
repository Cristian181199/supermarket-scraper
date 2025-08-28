import scrapy
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

        spider.logger.info(f"Se encontraron {len(product_urls)} URLs de productos en el sitemap.")

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
        item['name'] = response.css('h1.product-title::text').get().strip()
        item['price_amount'] = response.css('meta[itemprop="price"]::attr(content)').get()
        item['price_currency'] = response.css('meta[itemprop="priceCurrency"]::attr(content)').get()
        item['sku'] = response.css('div[itemprop="sku"]::text').get()
        
        item['product_url'] = response.url
        # La URL de la imagen a veces es relativa, la convertimos en absoluta
        img_src = response.css('img.article-image::attr(src)').get()
        item['image_url'] = response.urljoin(img_src)
        
        # Usamos .getall() para obtener todo el texto y lo unimos
        item['description'] = " ".join(response.css('div.longdesc div.desc::text').getall()).strip()
        item['category'] = response.css('ul.breadcrumb li a::text').getall()[-1].strip()
        
        item['base_price_text'] = response.css('div.price-per-unit::text').get().strip()
        
        # Añadimos metadatos
        item['scraped_at'] = datetime.utcnow()
        item['source_supermarket'] = 'Edeka24'

        # Devolvemos el item para que viaje al Pipeline
        yield item