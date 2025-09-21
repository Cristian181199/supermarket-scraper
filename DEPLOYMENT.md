# RetailFlux - Guía de Despliegue en Dokploy

Esta guía te ayudará a migrar de un despliegue monolítico con Docker Compose a servicios independientes en Dokploy.

## 🏗️ Arquitectura Nueva

### Servicios Independientes

1. **Database Service** (`retailflux-database`)
   - PostgreSQL 16 con pgvector
   - Volúmenes persistentes
   - Backups automáticos a S3
   - Sin acceso público

2. **API Service** (`retailflux-api`)
   - API REST para clientes
   - Dominio: `api.retailflux.de`
   - SSL automático vía Traefik
   - Zero-downtime deployments

3. **Scraper Service** (`retailflux-scraper`)
   - Ejecutable como job programado o servicio
   - Sin acceso público
   - Múltiples modos de ejecución

## 📋 Prerrequisitos

- Acceso a tu panel Dokploy: `panel.retailflux.de`
- Dominio `api.retailflux.de` configurado en DNS apuntando a tu servidor
- Credenciales de base de datos seguras
- (Opcional) Bucket S3 para backups

## 🚀 Proceso de Migración

### Paso 1: Preparar el Entorno Local

1. **Actualizar desarrollo local**:
```bash
# Usar el nuevo docker-compose para desarrollo
cp docker-compose.dev.yml docker-compose.yml
cp .env.dev .env

# Probar localmente
docker-compose up -d
```

### Paso 2: Crear el Servicio de Base de Datos

1. **En Dokploy UI**:
   - Ir a **Projects** → **Create Application**
   - Nombre: `retailflux-database`
   - Tipo: **Application**
   - Build Type: **Dockerfile**

2. **Configuración**:
   - **Dockerfile Path**: `deployments/database/Dockerfile`
   - **Build Context**: `.` (root del proyecto)
   
3. **Variables de Entorno**:
```env
POSTGRES_DB=retailflux_prod
POSTGRES_USER=retailflux
POSTGRES_PASSWORD=tu_contraseña_segura_aquí
POSTGRES_HOST_AUTH_METHOD=md5
```

4. **Volúmenes**:
   - `/var/lib/postgresql/data` → Volume: `retailflux_db_data`
   - `/var/log/postgresql` → Volume: `retailflux_db_logs`

5. **Red**:
   - Puerto interno: `5432` (NO exponer públicamente)
   - Health check habilitado

6. **Deploy** y verificar que esté funcionando.

### Paso 3: Crear el Servicio API

1. **En Dokploy UI**:
   - **Create Application**
   - Nombre: `retailflux-api`
   - Tipo: **Application**
   - Build Type: **Dockerfile**

2. **Configuración**:
   - **Dockerfile Path**: `deployments/api/Dockerfile`
   - **Build Context**: `.`

3. **Variables de Entorno**:
```env
# Database
POSTGRES_HOST=retailflux-database
POSTGRES_DB=retailflux_prod
POSTGRES_USER=retailflux
POSTGRES_PASSWORD=tu_contraseña_segura_aquí

# API
APP_ENV=production
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_HOSTS=api.retailflux.de
CORS_ORIGINS=https://retailflux.de,https://www.retailflux.de

# Security
SENTRY_DSN=tu_sentry_dsn_opcional
LOG_LEVEL=INFO
DEBUG=false

# Features
ENABLE_AI_FEATURES=false
OPENAI_API_KEY=tu_openai_key_cuando_esté_lista
```

4. **Dominio**:
   - Habilitar **Domain**
   - Hostname: `api.retailflux.de`
   - SSL: **Enabled** (automático con Traefik)

5. **Health Check**:
   - Path: `/health`
   - Enabled: `true`

6. **Scaling** (opcional):
   - Replicas: `2` si tu servidor lo permite
   - Zero Downtime: `Enabled`

7. **Deploy** y verificar acceso en `https://api.retailflux.de/health`

### Paso 4: Crear el Servicio Scraper

#### Opción A: Como Scheduled Job (Recomendada)

1. **En Dokploy UI**:
   - Ir a **Scheduled Jobs** → **Create Job**
   - Nombre: `retailflux-scraper-edeka`

2. **Configuración**:
   - **Image**: Usar la imagen built de `retailflux-scraper` application
   - **Schedule**: `0 */4 * * *` (cada 4 horas)
   - **Command**: `/bin/bash -c "./entrypoint.sh"`

3. **Variables de Entorno**:
```env
POSTGRES_HOST=retailflux-database
POSTGRES_DB=retailflux_prod
POSTGRES_USER=retailflux
POSTGRES_PASSWORD=tu_contraseña_segura_aquí
APP_ENV=production
SCRAPER_MODE=edeka
LOG_LEVEL=INFO
```

#### Opción B: Como Application

1. **Create Application**:
   - Nombre: `retailflux-scraper`
   - Build Type: **Dockerfile**
   - Dockerfile Path: `deployments/scraper/Dockerfile`

2. **Variables** (mismas que arriba) + `SCRAPER_MODE=scheduled`

### Paso 5: Configurar Backups (Opcional pero Recomendado)

1. **En Dokploy** → **Backups**:
   - Source: Volume `retailflux_db_data`
   - Destination: S3 Compatible (Hetzner Storage Box o Cloudflare R2)
   - Schedule: Daily at 02:00 UTC
   - Retention: 30 days

### Paso 6: Deshabilitar el Despliegue Anterior

1. **Stop/Remove** el servicio actual de Docker Compose en Dokploy
2. **Verificar** que todos los servicios nuevos estén funcionando
3. **Test** la API y verificar que el scraper escriba a la base de datos

## 🔧 Comandos Útiles para Debugging

### Verificar conectividad de servicios
```bash
# En el servidor, verificar que los servicios se vean entre sí
docker network ls
docker exec -it <api_container> ping retailflux-database
```

### Logs
```bash
# Ver logs de cada servicio desde Dokploy UI o CLI
dokploy logs retailflux-api
dokploy logs retailflux-database
```

### Acceso temporal a la base de datos
```bash
# Solo para debugging, crear un túnel temporal
ssh -L 5432:localhost:5432 tu_servidor
# Conectar con tu cliente SQL favorito a localhost:5432
```

## 🔄 Workflows de CI/CD

### Auto Deploy desde Git

1. **En cada Application**:
   - Habilitar **Auto Deploy**
   - Connect GitHub/GitLab repository
   - Branch: `main`
   - Path: Different for each service

2. **Webhook URLs** (configurar en tu repo):
   - Database: `https://panel.retailflux.de/api/webhooks/retailflux-database`
   - API: `https://panel.retailflux.de/api/webhooks/retailflux-api` 
   - Scraper: `https://panel.retailflux.de/api/webhooks/retailflux-scraper`

## 📊 Monitoring

### Health Checks
- API: `https://api.retailflux.de/health`
- Database: Internal health checks
- Scraper: Success/failure notifications via Dokploy

### Notifications (Opcional)
1. **Configurar en Settings** → **Notifications**:
   - Discord/Slack webhook para deploy success/failure
   - Email para errores críticos

## 🔐 Seguridad

### Variables de Entorno Sensibles
- Nunca hardcodear passwords en Dockerfiles
- Usar el sistema de variables de Dokploy
- Rotar passwords periódicamente

### Networking
- API: Solo puerto 8000/443 público
- Database: Solo acceso interno
- Scraper: Sin puertos públicos

### SSL/TLS
- API: SSL automático via Traefik/Let's Encrypt
- Internal communication: Docker network encryption

## 🚨 Troubleshooting

### Problema: API no puede conectar a la base de datos
```bash
# Verificar nombre del servicio de DB
docker ps | grep postgres
# El POSTGRES_HOST debe coincidir con el nombre del servicio
```

### Problema: Scraper no escribe a la base de datos
```bash
# Verificar logs del scraper job
dokploy logs retailflux-scraper-edeka
# Verificar conectividad de red
```

### Problema: SSL no funciona para API
- Verificar que DNS apunte correctamente
- Esperar ~5 minutos para provisioning de certificado
- Verificar en Dokploy UI que el dominio esté configurado

## 🎯 Próximos Pasos

1. **Expandir a más supermercados**: Crear jobs adicionales para otros mercados
2. **Implementar autenticación**: JWT tokens para la API
3. **Rate limiting**: Para la monetización futura
4. **Monitoring avanzado**: Prometheus/Grafana
5. **Chat AI**: Agregar como cuarto servicio cuando esté listo

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de cada servicio en Dokploy UI
2. Verifica variables de entorno
3. Consulta la documentación oficial de Dokploy
4. Contacta soporte si es necesario

---

**¡Buena suerte con el despliegue!** 🚀

# 🚀 Deployment Guide: Development + Production

This guide covers setting up both **local development** and **production deployment** on Hetzner with Dokploy.

## 📋 Prerequisites

### Local Development
- Docker Desktop installed and running
- Git configured
- 8GB+ RAM recommended

### Production (Hetzner + Dokploy)
- Hetzner VPS (minimum 4GB RAM, 2 CPU cores)
- Dokploy installed
- Domain name configured
- SSH access to server

---

## 🏠 Local Development Setup

### 1. Clone and Setup
```bash
git clone <your-repo>
cd edeka-scraper

# Make setup script executable
chmod +x scripts/dev-setup.sh

# Run setup (this will take 5-10 minutes)
./scripts/dev-setup.sh
```

### 2. Verify Installation
```bash
# Check if everything is running
cd infrastructure
docker-compose -f docker-compose.dev.yml ps

# Test database connection
docker-compose -f docker-compose.dev.yml exec postgres_db psql -U cristian -d products_db_dev -c "\\dt"
```

### 3. Run Your First Scrape
```bash
# Run the scraper
docker-compose -f docker-compose.dev.yml run --rm scraper

# Check results
docker-compose -f docker-compose.dev.yml exec postgres_db psql -U cristian -d products_db_dev -c "SELECT COUNT(*) FROM products;"
```

### 4. Development Workflow
```bash
# Start development stack (API + DB)
docker-compose -f docker-compose.dev.yml up -d postgres_db api

# API available at: http://localhost:8001
# Database available at: localhost:5433

# Run scraper as needed
docker-compose -f docker-compose.dev.yml run --rm scraper

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop everything
docker-compose -f docker-compose.dev.yml down
```

---

## 🌐 Production Deployment on Hetzner + Dokploy

### Phase 1: Server Preparation

#### 1. Create Hetzner VPS
- **Instance Type**: CPX31 (4GB RAM, 2 vCPU) minimum
- **Operating System**: Ubuntu 22.04 LTS
- **Location**: Choose closest to your users
- **Networking**: Enable IPv4 + IPv6

#### 2. Initial Server Setup
```bash
# Connect to server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install basic tools
apt install -y curl wget git htop unzip fail2ban ufw

# Configure firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 3000  # Dokploy admin port
ufw --force enable
```

#### 3. Install Dokploy
```bash
# Run Dokploy installation
curl -sSL https://dokploy.com/install.sh | sh

# Wait for installation to complete (5-10 minutes)
# Access Dokploy at: http://your-server-ip:3000
```

### Phase 2: Application Deployment

#### 1. Prepare Production Environment
Create `.env.prod` on your server with secure values:

```bash
# Create secure production environment file
cat > /opt/edeka-scraper/.env.prod << 'EOF'
# PRODUCTION ENVIRONMENT
POSTGRES_DB=products_db
POSTGRES_USER=edeka_scraper
POSTGRES_PASSWORD=YOUR_SECURE_DB_PASSWORD_HERE
POSTGRES_HOST=postgres_db
POSTGRES_PORT=5432

APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO

API_HOST=0.0.0.0
API_PORT=8000

SCRAPER_DEBUG=false
SCRAPER_CONCURRENT_REQUESTS=3
SCRAPER_DOWNLOAD_DELAY=1
SCRAPER_MAX_ITEMS=1000
SCRAPER_MAX_PAGES=100
SCRAPER_TEST_MODE=false

OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
ENABLE_AI_FEATURES=true

ENABLE_MONITORING=true
SENTRY_DSN=YOUR_SENTRY_DSN_HERE

ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ORIGINS=https://yourdomain.com
EOF
```

#### 2. Configure Dokploy Project

**In Dokploy Admin Panel (http://your-server-ip:3000):**

1. **Create New Project**
   - Name: `edeka-scraper`
   - Description: `Product scraping system`

2. **Add GitHub Repository**
   - Repository URL: Your GitHub repo URL
   - Branch: `main`
   - Build Path: `/infrastructure`

3. **Configure Services**

   **Service 1: PostgreSQL Database**
   ```yaml
   name: postgres_db_prod
   image: Built from dockerfile
   dockerfile: ./docker/postgres.prod.Dockerfile
   environment_variables:
     - From .env.prod file
   volumes:
     - postgres_data_prod:/var/lib/postgresql/data
     - postgres_logs_prod:/var/log/postgresql
   ports:
     - "5432:5432"
   healthcheck:
     enabled: true
     path: /health
   ```

   **Service 2: API**
   ```yaml
   name: api_prod
   image: Built from dockerfile
   dockerfile: ./docker/api.prod.Dockerfile
   environment_variables:
     - From .env.prod file
   ports:
     - "8000:8000"
   depends_on:
     - postgres_db_prod
   domain: api.yourdomain.com
   ssl: enabled
   ```

   **Service 3: Scraper**
   ```yaml
   name: scraper_prod
   image: Built from dockerfile
   dockerfile: ./docker/scraper.prod.Dockerfile
   environment_variables:
     - From .env.prod file
   depends_on:
     - postgres_db_prod
   restart_policy: unless-stopped
   ```

#### 3. Deploy and Verify

```bash
# Monitor deployment logs in Dokploy
# Check service status
# Verify API endpoint: https://api.yourdomain.com/health

# Connect to production database
docker exec -it postgres_db_prod psql -U edeka_scraper -d products_db

# View scraper logs
docker logs -f scraper_prod
```

---

## 🔄 Development to Production Workflow

### 1. Local Development
```bash
# Work on features locally
./scripts/dev-setup.sh
docker-compose -f docker-compose.dev.yml up -d

# Make changes, test, commit
git add .
git commit -m "feat: new feature"
git push origin main
```

### 2. Production Deployment
```bash
# Dokploy will auto-deploy on git push (if configured)
# Or manually deploy from Dokploy panel

# Monitor deployment
# Check logs
# Verify functionality
```

### 3. Rollback (if needed)
```bash
# In Dokploy panel:
# 1. Go to deployment history
# 2. Select previous stable version
# 3. Click "Rollback"
```

---

## 📊 Monitoring and Maintenance

### Production Health Checks
```bash
# API health
curl https://api.yourdomain.com/health

# Database connection
docker exec postgres_db_prod pg_isready

# Scraper status
docker logs --tail 100 scraper_prod

# System resources
htop
df -h
```

### Automated Backups
Dokploy provides:
- Automatic database backups
- Container snapshots
- Configuration versioning

### Scaling Recommendations

**For higher loads:**
- Upgrade to CPX41 (8GB RAM, 4 vCPU)
- Add Redis for caching
- Implement load balancing
- Add monitoring with Grafana

---

## 🎯 Ready to Deploy Checklist

Before production deployment, ensure:

- [ ] Local development environment works perfectly
- [ ] All tests pass
- [ ] Database migrations work
- [ ] Environment variables configured securely
- [ ] Domain names configured
- [ ] SSL certificates ready
- [ ] Monitoring tools configured
- [ ] Backup strategy in place

---

## 📞 Support

If you encounter issues:
1. Check Dokploy logs
2. Verify environment variables
3. Test database connectivity
4. Review application logs
5. Check system resources

**Ready to go live!** 🚀