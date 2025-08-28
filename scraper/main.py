import os
import time
import psycopg2
from dotenv import load_dotenv

def main():
    # Cargar variables de entorno desde .env (por si acaso)
    load_dotenv()
    
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = "postgres_db"
    db_port = 5432

    # Verificar que todas las variables de entorno estén disponibles
    if not all([db_name, db_user, db_password]):
        print(f"Error: Variables de entorno faltantes:")
        print(f"POSTGRES_DB: {db_name}")
        print(f"POSTGRES_USER: {db_user}")
        print(f"POSTGRES_PASSWORD: {'***' if db_password else None}")
        return

    print(f"Intentando conectar a la base de datos...", flush=True)
    print(f"Host: {db_host}:{db_port}", flush=True)
    print(f"Database: {db_name}", flush=True)
    print(f"User: {db_user}", flush=True)
    
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("✅ Conexión exitosa a la base de datos PostgreSQL.", flush=True)
        conn.close()
        
        # Mantener el contenedor activo para desarrollo
        print("🔄 Scraper iniciado. Esperando tareas...", flush=True)
        print("💡 Para desarrollo: El contenedor se mantiene activo.", flush=True)
        print("⏹️  Para detener: docker-compose stop scraper", flush=True)
        
        while True:
            time.sleep(30)  # Esperar 30 segundos
            print(f"⏰ {time.strftime('%H:%M:%S')} - Scraper activo (esperando tareas...)", flush=True)
            
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        # Esperar un poco antes de salir para ver los logs
        time.sleep(10)

if __name__ == "__main__":
    main()
