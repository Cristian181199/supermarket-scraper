#!/bin/bash
# ===================================================================
# SCRIPT DE BACKUP DE POSTGRESQL para retailflux.de
# ===================================================================

set -e

# --- Variables de Configuración (inyectadas por Docker) ---
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"
BACKUP_DIR="/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql.gz"
DAYS_TO_KEEP=7 # Mantener backups de los últimos 7 días

# --- Lógica del Backup ---
echo "Iniciando backup de la base de datos: ${DB_NAME}..."

# Crear el directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"

# Ejecutar pg_dump para crear el backup comprimido
pg_dump -U "${DB_USER}" -d "${DB_NAME}" -F c -b -v | gzip > "${BACKUP_FILE}"

# Verificar que el backup se ha creado
if [ ${PIPESTATUS[0]} -eq 0 ]; then
  echo "Backup completado exitosamente: ${BACKUP_FILE}"
else
  echo "ERROR: El backup de la base de datos ha fallado."
  exit 1
fi

# --- Limpieza de Backups Antiguos ---
echo "Limpiando backups con más de ${DAYS_TO_KEEP} días..."
find "${BACKUP_DIR}" -type f -name "*.sql.gz" -mtime +${DAYS_TO_KEEP} -exec rm {} \;

echo "Limpieza completada."
echo "Proceso de backup finalizado."