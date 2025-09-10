# Importamos la sesión y el motor que ya definimos en nuestro módulo 'database'
from database.session import SessionLocal, engine
from database.models import base

def get_db():
    """Generador que proporciona una sesión de base de datos a un endpoint."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()