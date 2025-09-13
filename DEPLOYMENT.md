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