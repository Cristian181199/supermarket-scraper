# This file defines the item pipelines for the Scrapy project.
# Item pipelines are used to process scraped items, for example,
# by cleaning, validating, or storing them in a database.
# For more info, see: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os

# Add the parent directory to Python path to access database modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from database import models
from database.session import engine


class SQLAlchemyPipeline:
    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        store = self._get_or_create(self.session, Store, name=adapter.get('store_name'))

        category = None
        parent_id = None
        for cat_name in adapter.get('category_path', []):
            category = self._get_or_create_category(self.session, name=cat_name, parent_id=parent_id)
            parent_id = category.id

        product = self.session.query(Product).filter_by(product_url=adapter.get('product_url')).first()
        if not product:
            product = Product()

        product.name = adapter.get('name')
        product.price_amount = adapter.get('price_amount')
        product.price_currency = adapter.get('price_currency')
        product.sku = adapter.get('sku')
        product.product_url = adapter.get('product_url')
        product.image_url = adapter.get('image_url')
        product.description = adapter.get('description')
        product.base_price_text = adapter.get('base_price_text')
        product.scraped_at = adapter.get('scraped_at')
        product.store = store
        product.category = category

        try:
            self.session.add(product)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        return item

    def _get_or_create(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    def _get_or_create_category(self, session, name, parent_id=None):
        instance = session.query(Category).filter_by(name=name, parent_id=parent_id).first()
        if instance:
            return instance
        else:
            instance = Category(name=name, parent_id=parent_id)
            session.add(instance)
            session.commit()
            return instance