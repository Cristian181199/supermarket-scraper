# 🕷️ ANÁLISIS DE MIGRACIÓN DEL SCRAPER

**Fecha:** 11 de Septiembre, 2025  
**Estado:** Análisis Completo  
**Objetivo:** Migrar scraper legacy a nueva arquitectura modular

---

## 📋 ESTRUCTURA ACTUAL (Legacy)

### 🗂️ **Arquitectura Existente**
```
services/scraper/
├── edeka_scraper/                 # Package principal Scrapy
│   ├── spiders/
│   │   └── edeka_spider.py        # Spider principal de Edeka
│   ├── items.py                   # Definición de Items Scrapy
│   ├── pipelines.py               # Pipeline SQLAlchemy (legacy)
│   ├── settings.py                # Configuración Scrapy
│   └── middlewares.py             # Middlewares (no analizados aún)
├── database/                      # Base de datos legacy (obsoleta)
├── main.py                        # Entry point
└── scrapy.cfg                     # Configuración Scrapy
```

---

## 🔍 ANÁLISIS DETALLADO DE COMPONENTES

### 📊 **1. Items Actuales (items.py)**

**Campos existentes en `EdekaProductItem`:**
```python
# Información relacional
store_name           → Store.name
category_path        → Category hierarchy mapping
# manufacturer_name  → Manufacturer.name (comentado)

# Información del producto
name                 → Product.name
price_amount         → Product.price_amount  
price_currency       → Product.price_currency
sku                  → Product.sku

# URLs
product_url          → Product.product_url
image_url            → Product.image_url

# Contenido
description          → Product.description

# Precio base
base_price_text      → Necesita parsing → Product.base_price_*

# Metadatos
scraped_at           → Product.scraped_at
```

### 🕷️ **2. Spider Actual (edeka_spider.py)**

**Funcionalidades implementadas:**
- ✅ **Sitemap parsing** - Navega sitemaps de productos
- ✅ **Product extraction** - Extrae datos de páginas individuales
- ✅ **Category hierarchy** - Maneja breadcrumbs de categorías
- ✅ **Price parsing** - Extrae precios con regex
- ✅ **Image URLs** - Construye URLs completas de imágenes
- ✅ **Metadata** - Timestamps y información de scraping

**Limitaciones identificadas:**
- 🔶 **Hardcoded límite** - Solo 5 productos por sitemap (testing)
- 🔶 **Manufacturer extraction** - No implementado
- 🔶 **Price parsing básico** - Solo precio principal, no base price completo
- 🔶 **Error handling limitado** - Manejo de errores básico

### 🔧 **3. Pipeline Actual (pipelines.py)**

**Funcionalidades:**
- ✅ **SQLAlchemy integration** - Usa modelos legacy
- ✅ **Store management** - Get or create stores
- ✅ **Category hierarchy** - Crea categorías anidadas
- ✅ **Product UPSERT** - Actualiza productos existentes

**Problemas identificados:**
- ❌ **Base de datos incorrecta** - Usa modelos legacy obsoletos
- ❌ **Imports rotos** - `from database import models` (no existe)
- ❌ **Session management** - No usa nuevos repositorios
- ❌ **Data transformation** - No procesa base_price_text correctamente
- ❌ **Error handling** - Rollback básico sin logging

### ⚙️ **4. Configuración (settings.py)**

**Configuración actual:**
- ✅ **Respectful crawling** - ROBOTSTXT_OBEY = True
- ✅ **Rate limiting** - DOWNLOAD_DELAY = 20 (cumple requerimientos)
- ✅ **Conservative concurrency** - 1 request por dominio
- ⚠️ **Database config** - Variables de entorno configuradas pero legacy

---

## 📈 MAPEO DE DATOS: Legacy → New Models

### 🔄 **Transformaciones Requeridas**

| Campo Legacy | Nuevo Campo | Transformación Necesaria |
|-------------|-------------|--------------------------|
| `store_name` | `Store.name` | ✅ Directo |
| `category_path` | `Category` hierarchy | 🔧 Crear/mapear jerarquía |
| `name` | `Product.name` | ✅ Directo |
| `price_amount` | `Product.price_amount` | ✅ Directo |
| `price_currency` | `Product.price_currency` | ✅ Directo |
| `sku` | `Product.sku` | ✅ Directo |
| `product_url` | `Product.product_url` | ✅ Directo |
| `image_url` | `Product.image_url` | ✅ Directo |
| `description` | `Product.description` | ✅ Directo |
| `base_price_text` | `Product.base_price_*` | 🔧 **Parser necesario** |
| `scraped_at` | `Product.scraped_at` | ✅ Directo |

### 🆕 **Campos Nuevos a Implementar**

**Campos faltantes en scraper actual:**
```python
# Información de precios detallada
base_price_amount     # Extraer de base_price_text
base_price_unit       # Extraer de base_price_text  
base_price_quantity   # Extraer de base_price_text

# Información estructurada
details              # JSON con información adicional
nutritional_info     # JSON con datos nutricionales

# Estado del producto
in_stock             # Detectar disponibilidad
availability_text    # Texto de disponibilidad

# Campos de IA (automáticos)
search_text          # Generado automáticamente
embedding            # Generado por IA
embedding_model      # Modelo usado
embedding_updated_at # Timestamp de embedding

# Metadatos adicionales
last_price_update    # Timestamp de cambio de precio
scrape_count         # Contador de scrapes
```

---

## 🚧 COMPONENTES A DESARROLLAR

### 🆕 **1. Nuevos Spiders**
- `base_spider.py` - Spider base con funcionalidades comunes
- `edeka_spider.py` - Spider específico de Edeka modernizado

### 🔧 **2. Nuevos Pipelines**  
- `validation.py` - Validación de datos
- `database.py` - Integración con nuevos repositorios
- `enrichment.py` - Enriquecimiento de datos y parsing

### 📊 **3. Nuevos Items**
- `product_item.py` - Items compatibles con nuevos modelos

### ⚙️ **4. Configuración por Entornos**
- `development.py` - Config para desarrollo (límites, delays)
- `production.py` - Config para producción (optimizada)

### 🔧 **5. Servicios de Integración**
- `scraper_service.py` - Business logic para scraping
- `data_transformer.py` - Transformación de datos
- `price_parser.py` - Parser especializado para precios

---

## 🎯 PLAN DE MIGRACIÓN

### 📅 **Fases de Implementación**

#### **Fase 1: Setup Base (30min)**
1. Crear nueva estructura en `services/scraper/`
2. Configurar entornos development/production
3. Implementar base spider class

#### **Fase 2: Data Integration (45min)**
1. Crear nuevos items compatibles
2. Implementar pipelines con nuevos repositorios  
3. Desarrollar data transformers

#### **Fase 3: Spider Modernization (30min)**
1. Migrar lógica de extracción de edeka_spider.py
2. Añadir extracción de campos faltantes
3. Implementar mejor error handling

#### **Fase 4: Testing & Validation (30min)**
1. Testing con configuración de desarrollo
2. Validar integración con API
3. Verificar calidad de datos

### ⚡ **Configuraciones Target**

#### 🧪 **Development Configuration**
```yaml
CONCURRENT_REQUESTS_PER_DOMAIN: 1
DOWNLOAD_DELAY: 3
PRODUCT_LIMIT: 50
SITEMAP_LIMIT: 2
AUTO_STOP_TIME: 300  # 5 minutes
RESPECT_ROBOTS: True
```

#### 🚀 **Production Configuration**  
```yaml
CONCURRENT_REQUESTS_PER_DOMAIN: 3
DOWNLOAD_DELAY: 20  # Compliance requirement
PRODUCT_LIMIT: null  # No limit
SITEMAP_LIMIT: null  # No limit
AUTO_STOP_TIME: 10800  # 3 hours
RESPECT_ROBOTS: True
SMART_THROTTLING: True
```

---

## ✅ COMPONENTES REUTILIZABLES

**Lo que podemos mantener:**
- ✅ Lógica de sitemap parsing
- ✅ CSS selectors para extracción
- ✅ Category breadcrumb extraction
- ✅ Price regex patterns (con mejoras)
- ✅ Image URL construction
- ✅ Basic error handling patterns

**Lo que debe reescribirse:**
- ❌ Pipeline completo (nuevos repositorios)
- ❌ Items definition (nuevos campos)
- ❌ Database integration (nueva arquitectura)
- ❌ Configuration management (entornos)
- ❌ Error handling y logging

---

## 🎉 CONCLUSIONES

**Estado:** ✅ **Migración es factible y directa**

**Ventajas de la migración:**
- 🔥 Mejor organización y mantenibilidad
- 🚀 Integración nativa con nueva arquitectura  
- 🤖 Preparado para funcionalidades de IA
- 📈 Configuración por entornos más flexible
- 🛡️ Mejor error handling y monitoring

**Tiempo estimado:** ~2-2.5 horas total
**Riesgo:** 🟢 Bajo (lógica de extracción probada)
**Beneficio:** 🟢 Alto (integración completa con nueva arquitectura)

**Próximo paso:** Comenzar implementación de nueva estructura modular
