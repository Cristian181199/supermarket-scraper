#!/bin/bash

# scripts/manage.sh

# Salir inmediatamente si un comando falla
set -e

# --- Funciones ---

# Levantar los contenedores en modo detached (background)
start() {
    echo "Levantando contenedores de desarrollo..."
    docker-compose up --build -d
    echo "¡Entorno listo!"
}

# Detener y eliminar los contenedores
stop() {
    echo "Deteniendo contenedores..."
    docker-compose down
    echo "Contenedores detenidos."
}

# Reconstruir las imágenes y levantar los contenedores
rebuild() {
    echo "Reconstruyendo y levantando contenedores..."
    docker-compose up --build -d --force-recreate
    echo "¡Entorno reconstruido!"
}

# Limpiar todo, incluyendo los volúmenes de la base de datos
clean() {
    echo "Deteniendo y eliminando contenedores..."
    docker-compose down
    echo "Eliminando volúmenes de Docker (¡SE PERDERÁN LOS DATOS DE LA DB!)..."
    docker volume rm supermarket-scraper_postgres_data || true # || true para no fallar si no existe
    echo "¡Limpieza completada!"
}

# Ejecutar el scraper de Edeka
scrape_edeka() {
    echo "Ejecutando el scraper de Edeka dentro del contenedor..."
    docker-compose exec scraper scrapy crawl edeka
}

makemigrations() {
    echo "Generando nuevo script de migración..."
    docker-compose exec scraper alembic revision --autogenerate -m "$1"
}

migrate() {
    echo "Aplicando migraciones a la base de datos..."
    docker-compose exec scraper alembic upgrade head
}

# Mostrar la ayuda
usage() {
    echo "Uso: ./scripts/manage.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  start       Levanta los contenedores de desarrollo."
    echo "  stop        Detiene los contenedores."
    echo "  rebuild     Reconstruye las imágenes y levanta los contenedores."
    echo "  clean       Detiene todo y elimina el volumen de la base de datos."
    echo "  scrape      Ejecuta el scraper de Edeka."
    echo "  makemigrations <mensaje> Genera un nuevo script de migración."
    echo "  migrate     Aplica las migraciones a la base de datos."
    echo "  help        Muestra este mensaje de ayuda."
}

# --- Lógica Principal ---

# Verificar que se pasó un comando
if [ -z "$1" ]; then
    usage
    exit 1
fi

# Ejecutar la función correspondiente al comando
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    rebuild)
        rebuild
        ;;
    clean)
        clean
        ;;
    scrape)
        scrape_edeka
        ;;
    help)
        usage
        ;;
    makemigrations)
        if [ -z "$2" ]; then
            echo "Error: Debes proporcionar un mensaje para la migración."
            exit 1
        fi
        makemigrations "$2"
        ;;
    migrate)
        migrate
        ;;
    *)
        echo "Error: Comando '$1' no reconocido."
        usage
        exit 1
        ;;
esac