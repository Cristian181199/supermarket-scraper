from sqlalchemy import (Column, Integer, String, Numeric, DateTime,
                        ForeignKey, JSON)
from sqlalchemy.orm import relationship
from .base import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sku = Column(String(50), nullable=True)
    product_url = Column(String, unique=True, index=True)
    image_url = Column(String)

    # --- Campos de Precio Mejorados ---
    price_amount = Column(Numeric(10, 2))
    price_currency = Column(String(10))
    base_price_amount = Column(Numeric(10, 2), nullable=True)
    base_price_unit = Column(String(20), nullable=True)
    base_price_quantity = Column(Numeric(10, 2), nullable=True)

    # --- Campo de Detalles Estructurados ---
    details = Column(JSON, nullable=True) # Usaremos JSONB en la migración

    # --- Metadatos y Relaciones ---
    scraped_at = Column(DateTime)
    store_id = Column(Integer, ForeignKey('stores.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'), nullable=True)

    store = relationship("Store", back_populates="products")
    category = relationship("Category", back_populates="products")
    manufacturer = relationship("Manufacturer", back_populates="products")