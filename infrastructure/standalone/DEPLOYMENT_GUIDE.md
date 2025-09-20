# RetailFlux - Guía de Despliegue Independiente en Dokploy

Esta guía te ayuda a desplegar cada servicio de RetailFlux de forma independiente en Dokploy, dándote control total sobre cada componente.

## 📋 Prerequisitos

- Dokploy instalado y funcionando
- Dominio `api.retailflux.de` apuntando a tu servidor
- Acceso SSH al servidor
- Git repository configurado

## 🏗️ Arquitectura de Servicios

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │       API       │    │    Scraper      │
│   Database      │◄──►│  api.retailflux │    │   (Scheduled)   │
│   Port: 5432    │    │   Port: 8000    │    │   On-demand     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Dokploy       │
                    │   Scheduler     │
                    │   (Manages      │
                    │   Scraper)      │
                    └─────────────────┘
```

## 🚀 Orden de Despliegue

### 1. PostgreSQL Database (Primero)

#### Crear Servicio en Dokploy:
1. **Tipo**: Docker
2. **Nombre**: `retailflux-postgres`
3. **Repository**: Tu repositorio Git
4. **Dockerfile Path**: `infrastructure/standalone/postgres/Dockerfile`
5. **Build Context**: Root del proyecto

#### Variables de Entorno:
```env
POSTGRES_DB=products_db_prod
POSTGRES_USER=retailflux_user
POSTGRES_PASSWORD=TU_PASSWORD_SEGURA_AQUI
POSTGRES_HOST_AUTH_METHOD=md5
```

#### Configuración de Red:
- **Puerto interno**: 5432
- **Puerto externo**: 5432 (si necesitas acceso externo)

#### Volúmenes:
- `/var/lib/postgresql/data` → Volumen persistente
- `/backups` → Volumen para backups

---

### 2. API Service (Segundo)

#### Crear Servicio en Dokploy:
1. **Tipo**: Docker
2. **Nombre**: `retailflux-api`
3. **Repository**: Tu repositorio Git
4. **Dockerfile Path**: `infrastructure/standalone/api/Dockerfile`
5. **Build Context**: Root del proyecto

#### Variables de Entorno:
```env
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
WORKER_PROCESSES=2

# Domain
DOMAIN=api.retailflux.de
ALLOWED_HOSTS=api.retailflux.de,localhost,127.0.0.1

# CORS
CORS_ORIGINS=https://retailflux.de,https://www.retailflux.de,https://api.retailflux.de

# Database (usar el nombre del servicio PostgreSQL)
POSTGRES_HOST=retailflux-postgres
POSTGRES_PORT=5432
POSTGRES_DB=products_db_prod
POSTGRES_USER=retailflux_user
POSTGRES_PASSWORD=LA_MISMA_PASSWORD_QUE_EN_POSTGRES

# Security
SECRET_KEY=tu_secret_key_muy_segura_aqui
JWT_SECRET_KEY=tu_jwt_secret_muy_segura_aqui

# AI (opcional)
OPENAI_API_KEY=tu_openai_key_aqui
ENABLE_AI_FEATURES=true

# Monitoring
SENTRY_DSN=tu_sentry_dsn_aqui
ENABLE_MONITORING=true
```

#### Configuración de Red:
- **Puerto interno**: 8000
- **Dominio personalizado**: `api.retailflux.de`
- **HTTPS**: Habilitado

#### Dependencias:
- Debe esperar a que PostgreSQL esté saludable

---

### 3. Scraper Service (Tercero)

#### Crear Servicio en Dokploy:
1. **Tipo**: Docker
2. **Nombre**: `retailflux-scraper`
3. **Repository**: Tu repositorio Git
4. **Dockerfile Path**: `infrastructure/standalone/scraper/Dockerfile`
5. **Build Context**: Root del proyecto

#### Variables de Entorno:
```env
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# Scraper Mode (IMPORTANTE: wait para no auto-iniciar)
SCRAPER_MODE=wait
SPIDER_NAME=edeka24_spider

# Database
POSTGRES_HOST=retailflux-postgres
POSTGRES_PORT=5432
POSTGRES_DB=products_db_prod
POSTGRES_USER=retailflux_user
POSTGRES_PASSWORD=LA_MISMA_PASSWORD_QUE_EN_POSTGRES

# Scraper Settings
SCRAPER_CONCURRENT_REQUESTS=3
SCRAPER_DOWNLOAD_DELAY=1
SCRAPER_MAX_ITEMS=1000
SCRAPER_MAX_PAGES=100
SCRAPER_TEST_MODE=false

# Performance
SCRAPER_MEMORY_LIMIT=512M
SCRAPER_TIMEOUT=3600

# AI (opcional)
OPENAI_API_KEY=tu_openai_key_aqui
ENABLE_AI_FEATURES=true
```

#### Configuración de Red:
- No necesita puerto externo (funciona internamente)

#### Recursos:
- **Memoria**: 512MB - 1GB
- **CPU**: 0.5 - 1 core

---

### 4. Scheduler en Dokploy (Cuarto)

#### Crear Job/Scheduler:
1. Ve a la sección **Jobs** o **Scheduler** en Dokploy
2. **Nombre**: `retailflux-scraper-job`
3. **Comando**: `docker exec retailflux-scraper /usr/local/bin/entrypoint.sh run`
4. **Cron Expression**: `0 */6 * * *` (cada 6 horas)
   - `0 2 * * *` = Diario a las 2 AM
   - `0 */4 * * *` = Cada 4 horas
   - `0 9,15,21 * * *` = A las 9 AM, 3 PM y 9 PM

---

## 🔧 Comandos Útiles

### Ejecutar Scraper Manualmente:
```bash
# Ejecutar scraping normal
docker exec retailflux-scraper /usr/local/bin/entrypoint.sh run

# Ejecutar en modo test (pocos productos)
docker exec retailflux-scraper /usr/local/bin/entrypoint.sh test

# Acceder al shell del scraper
docker exec -it retailflux-scraper /usr/local/bin/entrypoint.sh shell
```

### Verificar API:
```bash
# Health check
curl https://api.retailflux.de/health

# Ver productos
curl https://api.retailflux.de/products

# Ver métricas
curl https://api.retailflux.de/metrics
```

### Verificar Base de Datos:
```bash
# Conectar a PostgreSQL
docker exec -it retailflux-postgres psql -U retailflux_user -d products_db_prod

# Ver cantidad de productos
docker exec retailflux-postgres psql -U retailflux_user -d products_db_prod -c "SELECT COUNT(*) FROM products;"
```

---

## 🔍 Monitoreo y Logs

### Ver Logs de Servicios:
```bash
# API logs
docker logs retailflux-api -f

# Scraper logs
docker logs retailflux-scraper -f

# PostgreSQL logs
docker logs retailflux-postgres -f
```

### Health Checks:
- **PostgreSQL**: `pg_isready` cada 30s
- **API**: `curl /health` cada 30s  
- **Scraper**: Verificación de conexión DB cada 60s

---

## 🛠️ Troubleshooting

### Si la API no es accesible desde api.retailflux.de:

1. **Verificar DNS**: 
   ```bash
   nslookup api.retailflux.de
   ```

2. **Verificar que el servicio esté corriendo**:
   ```bash
   docker ps | grep retailflux-api
   ```

3. **Verificar logs de la API**:
   ```bash
   docker logs retailflux-api
   ```

4. **Verificar configuración de Dokploy**:
   - Dominio personalizado configurado
   - HTTPS habilitado
   - Puerto 8000 mapeado correctamente

### Si el Scraper no funciona:

1. **Verificar conexión a base de datos**:
   ```bash
   docker exec retailflux-scraper pg_isready -h retailflux-postgres -U retailflux_user
   ```

2. **Ejecutar en modo test**:
   ```bash
   docker exec retailflux-scraper /usr/local/bin/entrypoint.sh test
   ```

3. **Ver configuración actual**:
   ```bash
   docker exec retailflux-scraper env | grep SCRAPER
   ```

---

## 🎯 Ventajas de esta Configuración

✅ **Servicios Independientes**: Reinicia solo lo que necesitas
✅ **Control Granular**: Configura cada servicio por separado  
✅ **Escalabilidad**: Escala cada servicio según necesidades
✅ **Monitoreo**: Logs y métricas separadas por servicio
✅ **Mantenimiento**: Actualizaciones sin afectar otros servicios
✅ **Debugging**: Más fácil identificar problemas específicos
✅ **Scheduler Integrado**: Control total sobre cuándo ejecutar scraping

---

## 📞 Soporte

Si tienes problemas durante el despliegue:

1. Revisa los logs de cada servicio
2. Verifica las variables de entorno
3. Confirma que los servicios están saludables
4. Revisa la configuración de red en Dokploy

¡Tu RetailFlux estará ejecutándose con máxima flexibilidad! 🚀