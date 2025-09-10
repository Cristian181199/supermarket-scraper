from sqlalchemy.orm import Session
from sqlalchemy import text # Importamos la función 'text' para usar SQL "crudo" de forma segura
# Importamos los modelos de SQLAlchemy desde nuestro módulo 'database'
from database import models

def get_product(db: Session, product_id: int):
    """Obtiene un único producto por su ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 20):
    """Obtiene una lista paginada de productos."""
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    """Obtiene una única categoría por su ID."""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de categorías de primer nivel."""
    return db.query(models.Category).filter(models.Category.parent_id == None).offset(skip).limit(limit).all()

# --- FUNCIÓN MEJORADA ---
def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 20):
    """
    Obtiene una lista paginada de productos para una categoría específica,
    incluyendo todos los productos de sus subcategorías (recursivamente).
    """

    # 1. Definimos la consulta recursiva (CTE)
    # Usamos text() para que SQLAlchemy la trate como una consulta SQL segura.
    recursive_cte = text("""
        WITH RECURSIVE subcategories AS (
            SELECT id FROM categories WHERE id = :cat_id
            UNION ALL
            SELECT c.id FROM categories c
            INNER JOIN subcategories sc ON c.parent_id = sc.id
        )
        SELECT id FROM subcategories
    """)

    # 2. Ejecutamos la CTE para obtener todos los IDs de las subcategorías
    category_ids_result = db.execute(recursive_cte, {'cat_id': category_id}).fetchall()
    category_ids = [row[0] for row in category_ids_result]

    # 3. Buscamos todos los productos cuyo category_id esté en la lista que hemos generado
    return db.query(models.Product).filter(models.Product.category_id.in_(category_ids)).offset(skip).limit(limit).all()