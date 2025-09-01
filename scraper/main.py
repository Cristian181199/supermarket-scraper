import os
import time
import psycopg2
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # --- Database Connection Details ---
    db_name = os.getenv("POSTGRES_DB")
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_host = "postgres_db" # Service name in docker-compose
    db_port = 5432

    # --- Environment Variable Validation ---
    # Ensure all required database environment variables are set
    if not all([db_name, db_user, db_password]):
        print(f"Error: Missing environment variables:")
        print(f"POSTGRES_DB: {db_name}")
        print(f"POSTGRES_USER: {db_user}")
        print(f"POSTGRES_PASSWORD: {'***' if db_password else None}")
        return

    # --- Database Connection ---
    print(f"Attempting to connect to the database...", flush=True)
    print(f"Host: {db_host}:{db_port}", flush=True)
    print(f"Database: {db_name}", flush=True)
    print(f"User: {db_user}", flush=True)
    
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("✅ Successfully connected to the PostgreSQL database.", flush=True)
        conn.close()
        
        # --- Keep Container Running for Development ---
        # This loop keeps the container active, allowing for manual execution 
        # of the scraper or other development tasks.
        print("🔄 Scraper initialized. Waiting for tasks...", flush=True)
        print("💡 For development: The container will remain active.", flush=True)
        print("⏹️ To stop: docker-compose stop scraper", flush=True)
        
        while True:
            time.sleep(30)  # Wait for 30 seconds
            print(f"⏰ {time.strftime('%H:%M:%S')} - Scraper is active (waiting for tasks...)", flush=True)
            
    except Exception as e:
        # --- Error Handling ---
        # Catch and display any database connection errors
        print(f"❌ Error connecting to the database: {e}")
        # Wait a moment before exiting to ensure logs are visible
        time.sleep(10)

if __name__ == "__main__":
    main()
