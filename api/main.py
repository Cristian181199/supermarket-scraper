from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importamos todos nuestros módulos
import crud
import schemas
from db_session import get_db

# Crea una instancia de la aplicación FastAPI
app = FastAPI(
    title="Supermarket Scraper API",
    description="API for scraping supermarket data",
    version="0.1.0"
)

# Define un endpoint de prueba en la raíz
@app.get("/")
async def read_root():
    """Endpoint de prueba que devuelve un mensaje de bienvenida."""
    return {"status": "ok", "message": "¡Bienvenido a la API del Supermarket Scraper!"}

# --- ENDPOINTS DE PRODUCTOS ---

@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Obtiene una lista de productos con paginación.
    """
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un producto específico por su ID.
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

# --- ENDPOINTS DE CATEGORÍAS ---

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Obtiene una lista de las categorías principales (sin padre).
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}/products", response_model=List[schemas.Product])
def read_products_for_category(
    category_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    """
    Obtiene una lista de productos para una categoría específica.
    """
    # Primero, verificamos que la categoría exista para dar un error 404 claro.
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Si la categoría existe, obtenemos sus productos.
    products = crud.get_products_by_category(
        db, category_id=category_id, skip=skip, limit=limit
    )
    return products