# 🏗️ PLAN DE REESTRUCTURACIÓN - EDEKA SCRAPER

## 🎯 Objetivos
1. Separar responsabilidades claramente
2. Crear arquitectura modular y escalable
3. Preparar para funcionalidades de IA (PLN + Embeddings)
4. Facilitar el desarrollo de frontend de chat
5. Soporte para múltiples supermercados

## 📁 Nueva Estructura Propuesta

```
edeka-scraper/
├── shared/                              # 🔄 Código compartido
│   ├── database/                        # 💾 Núcleo de base de datos
│   │   ├── models/                      # 📊 Modelos SQLAlchemy
│   │   ├── repositories/                # 🏪 Repository pattern
│   │   ├── services/                    # 🔧 Servicios de datos
│   │   ├── migrations/                  # 📈 Migraciones Alembic
│   │   └── config.py                    # ⚙️ Configuración DB
│   ├── ai/                              # 🤖 Funcionalidades de IA
│   │   ├── embeddings/                  # 🧠 Generación embeddings
│   │   │   ├── generator.py             # Genera embeddings
│   │   │   └── storage.py               # Almacena vectores
│   │   ├── nlp/                         # 🗣️ Procesamiento PLN
│   │   │   ├── processor.py             # Analisis de texto
│   │   │   └── intent_classifier.py     # Clasificación intenciones
│   │   └── vector_search/               # 🔍 Búsqueda vectorial
│   │       ├── similarity.py            # Búsqueda por similitud
│   │       └── ranking.py               # Ranking resultados
│   └── config/                          # ⚙️ Configuración general
│       ├── settings.py                  # Configuración base
│       └── environment.py               # Variables de entorno
│
├── services/                            # 🏢 Microservicios
│   ├── api/                             # 🌐 API REST
│   │   ├── routers/                     # 📍 Endpoints organizados
│   │   │   ├── products.py              # Productos
│   │   │   ├── search.py                # Búsqueda
│   │   │   ├── ai.py                    # Endpoints IA
│   │   │   └── chat.py                  # Chat endpoints
│   │   ├── dependencies/                # 🔗 Dependencias FastAPI
│   │   ├── middleware/                  # 🛡️ Middleware
│   │   └── main.py                      # 🚀 App principal
│   │
│   ├── scraper/                         # 🕸️ Scraping service
│   │   ├── spiders/                     # 🕷️ Spiders por supermercado
│   │   │   ├── edeka/                   # Edeka spider
│   │   │   └── base_spider.py           # Spider base reutilizable
│   │   └── main.py                      # Scraper principal
│   │
│   └── chat/                            # 💬 Chat service (futuro)
│       ├── websocket/                   # 🔌 WebSocket handlers
│       ├── conversation/                # 💭 Gestión conversaciones
│       └── main.py                      # Chat service
│
├── infrastructure/                      # 🏗️ Infraestructura
│   ├── docker/                          # 🐳 Contenedores Docker
│   │   ├── api.Dockerfile               # API container
│   │   ├── scraper.Dockerfile           # Scraper container
│   │   └── postgres.Dockerfile          # PostgreSQL + pgvector
│   ├── scripts/                         # 📜 Scripts utilidad
│   └── docker-compose.yml               # 🐳 Orquestación servicios
│
└── frontend/                            # 🖥️ Frontend (futuro)
    └── chat-ui/                         # Chat interface
```

## 🔄 Pasos de Migración

### Fase 1: Preparación Base de Datos Central
- [ ] Crear `shared/database/` como núcleo central
- [ ] Migrar modelos actuales
- [ ] Implementar repository pattern
- [ ] Configurar pgvector para embeddings

### Fase 2: Reestructurar Servicios
- [ ] Separar API del código de base de datos
- [ ] Modularizar scraper para múltiples sitios
- [ ] Crear interfaces limpias entre servicios

### Fase 3: Funcionalidades de IA
- [ ] Sistema de embeddings para productos
- [ ] Búsqueda semántica
- [ ] Procesamiento de lenguaje natural

### Fase 4: Infraestructura Chat
- [ ] WebSockets para tiempo real
- [ ] Gestión de conversaciones
- [ ] Integración con IA

## 🎁 Beneficios Esperados

1. **🔧 Mantenibilidad**: Código organizado y separación clara
2. **📈 Escalabilidad**: Fácil añadir nuevos supermercados
3. **🤖 IA-Ready**: Preparado para funcionalidades avanzadas
4. **🔄 Reutilización**: Componentes compartidos eficientes
5. **🧪 Testing**: Estructura testeable y modular
