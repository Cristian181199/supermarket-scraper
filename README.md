# 🛒 AI-Powered Supermarket Scraper

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL+pgvector-blue.svg)
![AI](https://img.shields.io/badge/AI-OpenAI_Embeddings-purple.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A **production-ready**, **AI-powered** web scraping and product search system with semantic search capabilities. Features a modern modular architecture with FastAPI, PostgreSQL with vector search, and OpenAI embeddings for intelligent product recommendations and semantic search.

## ✨ Features

### 🤖 AI & Search Capabilities
- **🧠 Semantic Search**: OpenAI embeddings for intelligent product search beyond keywords
- **🔍 Hybrid Search**: Combines full-text search with vector similarity for best results
- **📊 Vector Database**: PostgreSQL with pgvector extension for efficient similarity searches
- **🎯 Smart Recommendations**: AI-powered similar products based on embeddings
- **💬 Search Intent Recognition**: Natural language query processing

### 🏗️ Modern Architecture
- **⚡ FastAPI REST API**: High-performance async API with automatic docs
- **🗄️ Modular Design**: Clean separation between database, services, and API layers
- **📦 Repository Pattern**: Organized data access with specialized repositories
- **🔄 Database Migrations**: Full Alembic integration for schema versioning
- **🐳 Containerized Environment**: Multi-service Docker setup with hot reload

### 🕷️ Web Scraping
- **🎯 Automated Data Extraction**: Intelligent crawling with sitemap discovery
- **💾 Smart Data Pipeline**: UPSERT operations with duplicate detection
- **🤝 Respectful Crawling**: Obeys robots.txt with configurable delays
- **📈 Extensible Spiders**: Ready for multiple supermarket chains

## 🛠️ Technology Stack

### 🔥 Core Technologies
- **API Framework**: FastAPI 0.104+ with async support
- **Database**: PostgreSQL 15 + pgvector extension for vector search
- **ORM**: SQLAlchemy 2.0+ with async support
- **AI/ML**: OpenAI Embeddings API, pgvector for similarity search
- **Containerization**: Docker & Docker Compose with multi-stage builds

### 🕷️ Web Scraping
- **Framework**: Scrapy 2.13+ with custom pipelines
- **Data Processing**: pandas for data transformation
- **Respectful Crawling**: Custom download delays and robots.txt compliance

### 📁 Infrastructure
- **Migrations**: Alembic for database schema management
- **Environment**: Python 3.11, python-dotenv, psycopg2-binary
- **Monitoring**: Built-in health checks and logging

## 🚀 Quick Start

Get the AI-powered scraper running in minutes with Docker!

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose installed
- [Git](https://git-scm.com/) for cloning the repository
- (Optional) OpenAI API key for AI features

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cristian181199/edeka-scraper.git
   cd edeka-scraper
   ```

2. **Configure environment:**
   Create your environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   # Add OPENAI_API_KEY for AI features (optional)
   ```

3. **Start all services:**
   ```bash
   cd infrastructure
   docker-compose up --build -d
   ```

4. **Initialize the database:**
   ```bash
   # Tables are created automatically on first API startup
   # Check health: http://localhost:8000/health
   ```

## 📚 API Usage

Once running, you have access to a powerful REST API with AI-powered search:

### 🌐 Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 🔍 Key Endpoints

**Product Search:**
```bash
# Semantic search with AI
curl "http://localhost:8000/api/v1/search/?q=cola&limit=5"

# Text-only search
curl "http://localhost:8000/api/v1/search/text-only?q=cola"
```

**Product Management:**
```bash
# List all products
curl "http://localhost:8000/api/v1/products/?limit=10"

# Get specific product
curl "http://localhost:8000/api/v1/products/1"

# Find similar products (AI-powered)
curl "http://localhost:8000/api/v1/products/1/similar"
```

**Advanced Filtering:**
```bash
# Filter by store and price range
curl "http://localhost:8000/api/v1/products/?store_id=1&limit=10"
curl "http://localhost:8000/api/v1/products/by-price-range/?min_price=1&max_price=5"
```

### 🕷️ Running the Scraper

```bash
# Access scraper container
docker exec -it scraper bash

# Run Edeka spider
scrapy crawl edeka
```

### 📁 Database Access

**Connection Details:**
- Host: `localhost:5432`  
- Database: `products_db`
- User/Pass: (from your `.env` file)

## 🏗️ Current Architecture

The project follows a modern, modular architecture:

```
edeka-scraper/
├── shared/                    # 🔄 Shared components
│   ├── database/              # 💾 Database layer
│   │   ├── models/            # 📋 SQLAlchemy models
│   │   ├── repositories/      # 🏢 Data access layer
│   │   ├── services/          # ⚙️ Business logic
│   │   └── migrations/        # 📈 Database migrations
│   ├── ai/                    # 🤖 AI capabilities
│   │   └── embeddings/        # 🧠 Vector processing
│   └── config/               # ⚙️ Configuration
│
├── services/                 # 💼 Microservices
│   ├── api/                  # 🌐 FastAPI REST API
│   │   └── routers/          # 📡 API endpoints
│   └── scraper/              # 🕷️ Web scraping
│
├── infrastructure/           # 🚀 Infrastructure
│   ├── docker/               # 🐳 Container configs
│   └── docker-compose.yml     # 🔗 Service orchestration
└── frontend/                 # 🗺 Frontend (planned)
```

### Key Design Patterns:
- **Repository Pattern**: Clean data access abstraction
- **Service Layer**: Business logic separation
- **Dependency Injection**: Loose coupling between components
- **Microservices**: Independent, scalable services

## 🚯 Future Enhancements

Upcoming features and improvements:

### 🤖 AI & Machine Learning
- [ ] Advanced NLP for query understanding
- [ ] Product recommendation engine
- [ ] Price trend analysis
- [ ] Inventory prediction

### 📱 Frontend & UX
- [ ] React-based chat interface
- [ ] Real-time WebSocket updates
- [ ] Mobile-responsive design
- [ ] PWA capabilities

### 🕷️ Scraping Expansion
- [ ] Additional supermarket chains (Rewe, Lidl, etc.)
- [ ] Proxy rotation for scale
- [ ] Real-time price monitoring
- [ ] Product availability tracking

### ⚙️ Infrastructure
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Monitoring & alerting
- [ ] Auto-scaling capabilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.