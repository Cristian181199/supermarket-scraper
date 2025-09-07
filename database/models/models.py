from sqlalchemy import (Column, Integer, String, Numeric, DateTime,
                        ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from .base import Base

class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship("Product", back_populates="store")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")
    __table_args__ = (UniqueConstraint('name', 'parent_id', name='_category_parent_uc'),)

class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    products = relationship("Product", back_populates="manufacturer")

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price_amount = Column(Numeric(10, 2))
    price_currency = Column(String(10))
    sku = Column(String(50), nullable=True)
    product_url = Column(String, unique=True, index=True)
    image_url = Column(String)
    description = Column(String)
    base_price_text = Column(String)
    scraped_at = Column(DateTime)
    store_id = Column(Integer, ForeignKey('stores.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=True)
    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")
    manufacturer = relationship("Manufacturer", back_populates="products")