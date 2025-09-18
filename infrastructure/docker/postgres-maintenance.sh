#!/bin/bash
# ===================================================================
# SCRIPT DE MANTENIMIENTO DE POSTGRESQL para retailflux.de
# ===================================================================

set -e

# --- Variables de Configuración ---
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"

echo "Iniciando tareas de mantenimiento para la base de datos: ${DB_NAME}..."

# --- Tareas de Mantenimiento ---
# 1. VACUUM: Recupera espacio y previene el "wraparound" de IDs de transacción.
echo "Ejecutando VACUUM (VERBOSE, ANALYZE)..."
psql -U "${DB_USER}" -d "${DB_NAME}" -c "VACUUM (VERBOSE, ANALYZE);"

# 2. REINDEX (Opcional, puede ser intensivo): Reconstruye índices corruptos o ineficientes.
# Descomentar si se experimentan problemas de rendimiento en los índices.
# echo "Ejecutando REINDEX DATABASE..."
# psql -U "${DB_USER}" -d "${DB_NAME}" -c "REINDEX DATABASE ${DB_NAME};"

echo "Tareas de mantenimiento completadas exitosamente."