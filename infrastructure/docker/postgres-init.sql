-- Script de inicialización para PostgreSQL con extensiones necesarias
-- Se ejecuta automáticamente cuando se crea la base de datos

-- Habilitar extensión pgvector para búsqueda vectorial
CREATE EXTENSION IF NOT EXISTS vector;

-- Habilitar extensión uuid-ossp para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Habilitar extensión pg_trgm para búsqueda de texto fuzzy
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Habilitar extensión unaccent para normalizar texto
CREATE EXTENSION IF NOT EXISTS unaccent;

-- Crear función personalizada para búsqueda de texto normalizado
CREATE OR REPLACE FUNCTION normalize_text(text) 
RETURNS text AS $$
BEGIN
    RETURN lower(unaccent($1));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Configuraciones específicas para pgvector
-- Ajustar parámetros para mejor rendimiento con vectores
ALTER SYSTEM SET shared_preload_libraries = 'vector';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '16MB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';

-- Configuraciones específicas para vectores
ALTER SYSTEM SET ivfflat.probes = 10;

SELECT pg_reload_conf();

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL inicializado con extensiones: vector, uuid-ossp, pg_trgm, unaccent';
    RAISE NOTICE 'Base de datos lista para búsqueda vectorial y funcionalidades de IA';
END $$;
