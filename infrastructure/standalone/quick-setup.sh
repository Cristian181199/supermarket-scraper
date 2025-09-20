#!/bin/bash

# RetailFlux - Quick Setup Script for Standalone Deployment
# ========================================================

set -e

echo "🚀 RetailFlux Standalone Setup"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to generate random password
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

# Function to generate secret key
generate_secret() {
    openssl rand -hex 32
}

echo -e "${BLUE}Este script te ayudará a configurar RetailFlux para despliegue independiente${NC}"
echo ""

# Ask for basic configuration
echo -e "${YELLOW}📝 Configuración Básica${NC}"
echo "=========================="

read -p "🔗 Dominio para API (default: api.retailflux.de): " API_DOMAIN
API_DOMAIN=${API_DOMAIN:-api.retailflux.de}

read -p "🌍 Dominio principal (default: retailflux.de): " MAIN_DOMAIN
MAIN_DOMAIN=${MAIN_DOMAIN:-retailflux.de}

read -p "🗄️  Nombre de base de datos (default: products_db_prod): " DB_NAME
DB_NAME=${DB_NAME:-products_db_prod}

read -p "👤 Usuario de base de datos (default: retailflux_user): " DB_USER
DB_USER=${DB_USER:-retailflux_user}

# Generate secure passwords
DB_PASSWORD=$(generate_password)
SECRET_KEY=$(generate_secret)
JWT_SECRET=$(generate_secret)

echo ""
echo -e "${YELLOW}🔐 ¿Tienes claves de servicios externos?${NC}"
echo "========================================"

read -p "🤖 OpenAI API Key (opcional, presiona Enter para omitir): " OPENAI_KEY
read -p "📊 Sentry DSN (opcional, presiona Enter para omitir): " SENTRY_DSN

echo ""
echo -e "${GREEN}✨ Generando configuraciones...${NC}"

# Create PostgreSQL .env
cat > infrastructure/standalone/postgres/.env << EOF
# PostgreSQL Configuration - Generated $(date)
POSTGRES_DB=${DB_NAME}
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_HOST_AUTH_METHOD=md5
EOF

# Create API .env
cat > infrastructure/standalone/api/.env << EOF
# API Configuration - Generated $(date)
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WORKER_PROCESSES=2

# Domain Configuration
DOMAIN=${API_DOMAIN}
ALLOWED_HOSTS=${API_DOMAIN},localhost,127.0.0.1

# CORS Configuration
CORS_ORIGINS=https://${MAIN_DOMAIN},https://www.${MAIN_DOMAIN},https://${API_DOMAIN}

# Database Connection
POSTGRES_HOST=retailflux-postgres
POSTGRES_PORT=5432
POSTGRES_DB=${DB_NAME}
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}

# Security
SECRET_KEY=${SECRET_KEY}
JWT_SECRET_KEY=${JWT_SECRET}

# Performance
MAX_CONNECTIONS=100
CONNECTION_TIMEOUT=30

# Monitoring & Logging
SENTRY_DSN=${SENTRY_DSN}
ENABLE_MONITORING=true

# AI Features
OPENAI_API_KEY=${OPENAI_KEY}
ENABLE_AI_FEATURES=$([ -n "$OPENAI_KEY" ] && echo "true" || echo "false")
EOF

# Create Scraper .env
cat > infrastructure/standalone/scraper/.env << EOF
# Scraper Configuration - Generated $(date)
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Scraper Mode
SCRAPER_MODE=wait
SPIDER_NAME=edeka24_spider

# Database Connection
POSTGRES_HOST=retailflux-postgres
POSTGRES_PORT=5432
POSTGRES_DB=${DB_NAME}
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}

# Scraper Configuration
SCRAPER_CONCURRENT_REQUESTS=3
SCRAPER_DOWNLOAD_DELAY=1
SCRAPER_MAX_ITEMS=1000
SCRAPER_MAX_PAGES=100
SCRAPER_TEST_MODE=false

# Output Configuration
OUTPUT_FILE=
SCRAPER_OUTPUT_FORMAT=json

# Performance Settings
SCRAPER_MEMORY_LIMIT=512M
SCRAPER_TIMEOUT=3600

# Retry Configuration
SCRAPER_RETRY_ENABLED=true
SCRAPER_RETRY_TIMES=3
SCRAPER_RETRY_HTTP_CODES=500,502,503,504,408,429

# User Agent and Headers
USER_AGENT=Mozilla/5.0 (compatible; RetailFluxBot/1.0; +https://${MAIN_DOMAIN}/bot)
RESPECT_ROBOTS_TXT=true

# Monitoring
ENABLE_MONITORING=true
SENTRY_DSN=${SENTRY_DSN}

# AI Features
OPENAI_API_KEY=${OPENAI_KEY}
ENABLE_AI_FEATURES=$([ -n "$OPENAI_KEY" ] && echo "true" || echo "false")

# Scheduler Integration
SCHEDULER_ENABLED=true
SCHEDULER_WEBHOOK_URL=
EOF

# Create deployment summary
cat > infrastructure/standalone/DEPLOYMENT_SUMMARY.txt << EOF
RetailFlux Standalone Deployment Summary
========================================
Generated: $(date)

IMPORTANT CREDENTIALS:
=====================
Database Name: ${DB_NAME}
Database User: ${DB_USER}
Database Password: ${DB_PASSWORD}

API Secret Key: ${SECRET_KEY}
JWT Secret: ${JWT_SECRET}

DOMAINS:
========
API Domain: ${API_DOMAIN}
Main Domain: ${MAIN_DOMAIN}

SERVICES ORDER:
===============
1. PostgreSQL: retailflux-postgres
2. API: retailflux-api  
3. Scraper: retailflux-scraper
4. Scheduler: retailflux-scraper-job

NEXT STEPS:
===========
1. Commit these files to your Git repository
2. Deploy PostgreSQL first in Dokploy
3. Deploy API second
4. Deploy Scraper third  
5. Create Scheduler job last

IMPORTANT: Keep this file secure and don't commit it to version control!
EOF

echo ""
echo -e "${GREEN}✅ ¡Configuración completada!${NC}"
echo ""
echo -e "${BLUE}📁 Archivos generados:${NC}"
echo "  - infrastructure/standalone/postgres/.env"
echo "  - infrastructure/standalone/api/.env" 
echo "  - infrastructure/standalone/scraper/.env"
echo "  - infrastructure/standalone/DEPLOYMENT_SUMMARY.txt"
echo ""
echo -e "${YELLOW}🔒 IMPORTANTE:${NC}"
echo "  - Guarda el archivo DEPLOYMENT_SUMMARY.txt en un lugar seguro"
echo "  - NO subas este archivo a Git (contiene contraseñas)"
echo "  - Usa estos valores en las variables de entorno de Dokploy"
echo ""
echo -e "${GREEN}📖 Siguiente paso:${NC}"
echo "  Lee infrastructure/standalone/DEPLOYMENT_GUIDE.md para instrucciones completas"
echo ""
echo -e "${BLUE}🚀 ¡Listo para desplegar!${NC}"