# RetailFlux - Servicios Independientes 🚀

Esta carpeta contiene todo lo necesario para desplegar RetailFlux con **servicios completamente independientes** en Dokploy, siguiendo las mejores prácticas de producción.

## 🎯 ¿Por qué Servicios Independientes?

✅ **Control Total**: Reinicia, actualiza y escala cada servicio por separado  
✅ **Debugging Fácil**: Logs y métricas separadas por servicio  
✅ **Escalabilidad**: Escala solo lo que necesitas  
✅ **Flexibilidad**: Diferentes configuraciones por servicio  
✅ **Scheduler Integrado**: Control total sobre cuándo ejecutar scraping  
✅ **Dominio Personalizado**: API accesible en `api.retailflux.de`

## 📁 Estructura

```
infrastructure/standalone/
├── api/
│   ├── Dockerfile              # API independiente
│   ├── entrypoint.sh          # Script de inicio con migraciones
│   └── .env                   # Variables de entorno para API
├── scraper/
│   ├── Dockerfile             # Scraper independiente (no auto-start)
│   ├── entrypoint.sh          # Script con modos: wait/run/test
│   └── .env                   # Variables de entorno para scraper
├── postgres/
│   ├── Dockerfile             # PostgreSQL optimizado
│   ├── init-extensions.sql    # Extensiones (vector, pg_trgm, etc.)
│   └── init-user.sql          # Configuración de usuario
├── DEPLOYMENT_GUIDE.md        # 📖 Guía completa paso a paso
├── quick-setup.sh            # 🚀 Script de configuración rápida
└── README.md                 # Este archivo
```

## 🚀 Inicio Rápido

### 1. Configuración Automática
```bash
cd infrastructure/standalone/
./quick-setup.sh
```

Este script:
- ✨ Genera contraseñas seguras automáticamente
- 🔧 Crea archivos `.env` personalizados para cada servicio  
- 📝 Te pregunta por dominios y servicios externos (OpenAI, Sentry)
- 📄 Genera un resumen con todas las credenciales

### 2. Despliegue en Dokploy

**Orden obligatorio:**
1. **PostgreSQL** (`retailflux-postgres`)
2. **API** (`retailflux-api`) 
3. **Scraper** (`retailflux-scraper`)
4. **Scheduler** (Job en Dokploy)

📖 **Guía detallada**: Lee `DEPLOYMENT_GUIDE.md` para instrucciones completas

## 🏗️ Arquitectura

```
🌐 Internet
     │
     ├── api.retailflux.de (HTTPS) ──► API Service
     └── SSH Access ──────────────────► Server Management
                                          │
┌─────────────────────────────────────────┼─────────────────────────────────────────┐
│ Docker Network (Dokploy)               │                                         │
│                                        ▼                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │
│  │   PostgreSQL    │    │       API       │    │    Scraper      │              │
│  │   (Always On)   │◄──►│  (Always On)    │    │   (On Demand)   │              │
│  │   Port: 5432    │    │   Port: 8000    │    │   Scheduled     │              │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘              │
│           ▲                       ▲                       ▲                     │
│           │                       │                       │                     │
│           └───────────────────────┼───────────────────────┘                     │
│                                   │                                             │
│                      ┌─────────────────┐                                        │
│                      │   Dokploy       │                                        │
│                      │   Scheduler     │                                        │
│                      │   (Triggers     │                                        │
│                      │   Scraper)      │                                        │
│                      └─────────────────┘                                        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Características del Scraper

### Modos de Operación:
- **`wait`** (default): Contenedor vivo, esperando comando de ejecución
- **`run`**: Ejecuta scraping una vez y termina
- **`test`**: Modo test con límites reducidos
- **`shell`**: Shell interactivo para debugging

### Comandos de Control:
```bash
# Ejecutar scraping manualmente
docker exec retailflux-scraper /usr/local/bin/entrypoint.sh run

# Modo test (pocos productos)
docker exec retailflux-scraper /usr/local/bin/entrypoint.sh test

# Acceder al shell
docker exec -it retailflux-scraper /usr/local/bin/entrypoint.sh shell
```

## 🎛️ Configuración de Scheduler en Dokploy

1. **Crear Job**: `retailflux-scraper-job`
2. **Comando**: `docker exec retailflux-scraper /usr/local/bin/entrypoint.sh run`
3. **Frecuencia**: 
   - `0 */6 * * *` = Cada 6 horas
   - `0 2 * * *` = Diario a las 2 AM
   - `0 9,15,21 * * *` = 9 AM, 3 PM, 9 PM

## 🔍 Monitoreo

### Health Checks Automáticos:
- **PostgreSQL**: `pg_isready` cada 30s
- **API**: `curl /health` cada 30s
- **Scraper**: Verificación de conexión DB cada 60s

### Logs por Servicio:
```bash
docker logs retailflux-postgres -f  # Base de datos
docker logs retailflux-api -f       # API
docker logs retailflux-scraper -f   # Scraper
```

### Verificación de API:
```bash
curl https://api.retailflux.de/health
curl https://api.retailflux.de/products
curl https://api.retailflux.de/metrics
```

## 🛠️ Variables de Entorno Importantes

### API:
- `DOMAIN=api.retailflux.de`
- `POSTGRES_HOST=retailflux-postgres`
- `WORKER_PROCESSES=2`

### Scraper:
- `SCRAPER_MODE=wait` (no auto-start)
- `POSTGRES_HOST=retailflux-postgres`  
- `SCRAPER_MAX_ITEMS=1000`

### PostgreSQL:
- `POSTGRES_DB=products_db_prod`
- `POSTGRES_USER=retailflux_user`
- Extensiones: vector, pg_trgm, unaccent, uuid-ossp

## 🚨 Solución de Problemas

### API no accesible en api.retailflux.de:
1. Verificar configuración de dominio en Dokploy
2. Verificar que HTTPS está habilitado
3. Verificar logs: `docker logs retailflux-api`

### Scraper no funciona:
1. Verificar conexión DB: `docker exec retailflux-scraper pg_isready -h retailflux-postgres -U retailflux_user`
2. Ejecutar test: `docker exec retailflux-scraper /usr/local/bin/entrypoint.sh test`
3. Verificar variables: `docker exec retailflux-scraper env | grep SCRAPER`

### Base de datos:
1. Conectar: `docker exec -it retailflux-postgres psql -U retailflux_user -d products_db_prod`
2. Ver productos: `SELECT COUNT(*) FROM products;`
3. Ver tablas: `\dt`

## 📚 Documentación Adicional

- **📖 Guía Completa**: `DEPLOYMENT_GUIDE.md`
- **🔧 Configuración**: Usa `quick-setup.sh` para generar configs
- **🌐 API Docs**: Una vez desplegada, visita `https://api.retailflux.de/docs`

## 🎉 Beneficios vs Docker Compose

| Aspecto | Docker Compose | Servicios Independientes |
|---------|----------------|--------------------------|
| **Control** | Todo junto | Granular por servicio |
| **Escalado** | Todo o nada | Por servicio |
| **Updates** | Reinicia todo | Solo el servicio necesario |
| **Debugging** | Logs mezclados | Logs separados |
| **Scheduler** | Manual/externo | Integrado en Dokploy |
| **Dominio** | Puerto directo | Dominio personalizado |
| **Flexibilidad** | Limitada | Máxima |

---

¡Tu RetailFlux estará ejecutándose con máxima flexibilidad y control! 🚀