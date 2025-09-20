#!/bin/sh
# ===================================================================
# ENTRYPOINT PARA EL SERVICIO DE API EN PRODUCCIÓN
# ===================================================================

# Salir inmediatamente si un comando falla
set -e

# --- 1. Esperar a que la Base de Datos esté lista ---
echo "Esperando a que la base de datos en '$POSTGRES_HOST' esté disponible..."

# Usamos un bucle para esperar a que el puerto 5432 del host de la DB esté abierto
# Esto es más fiable que depender solo del healthcheck de Docker
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres no está disponible todavía - esperando..."
  sleep 1
done

>&2 echo "¡Postgres está disponible! Continuando..."

# --- 2. Ejecutar Migraciones de la Base de Datos ---
echo "Ejecutando migraciones de la base de datos con Alembic..."

# Navegamos al directorio correcto donde está alembic.ini
cd /usr/src/app/infrastructure
alembic upgrade head

echo "¡Migraciones completadas!"

# --- 3. Iniciar la Aplicación Principal (API) ---
echo "Iniciando servidor Gunicorn..."

# Volvemos al directorio de trabajo principal
cd /usr/src/app

# Ejecutamos el comando que estaba originalmente en el docker-compose
exec gunicorn services.api.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile - \
  --log-level info