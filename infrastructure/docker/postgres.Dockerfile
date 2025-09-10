# PostgreSQL con pgvector para búsqueda vectorial
FROM pgvector/pgvector:pg15

# Instalar extensiones adicionales
RUN apt-get update && apt-get install -y \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Crear script de inicialización para habilitar extensiones
COPY infrastructure/docker/postgres-init.sql /docker-entrypoint-initdb.d/

# Configuración optimizada para desarrollo con vectores
COPY infrastructure/docker/postgres.conf /etc/postgresql/postgresql.conf

# Exponer puerto
EXPOSE 5432
