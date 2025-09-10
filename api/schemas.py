from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Schemas Base ---
# Usaremos estos para evitar repetir código

class CategoryBase(BaseModel):
    name: str

class ProductBase(BaseModel):
    name: str
    price_amount: Optional[float] = None
    product_url: str
    image_url: Optional[str] = None

# --- Schemas para Creacion (si los necesitamos en el futuro) ---
# No los usaremos ahora mismo, pero los dejo por si acaso
class CategoryCreate(CategoryBase):
    pass

# --- Schemas para Lectura (estos definirán cómo se ven los datos en las respuestas de la API) ---
class Product(ProductBase):
    id: int
    description: Optional[str] = None

    # Le decimos a Pydantic que puede mapear desde un objeto ORM
    class Config:
        from_attributes = True

class Category(CategoryBase):
    id: int
    parent_id: Optional[int] = None
    # Incluimos una lista de sus subcategorías
    children: List['Category'] = []

    class Config:
        from_attributes = True