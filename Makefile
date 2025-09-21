# RetailFlux Development Makefile
# Simplify common development tasks

.PHONY: help dev-start dev-stop dev-logs dev-build dev-clean prod-build test lint format

# Default target
help:
	@echo "RetailFlux Development Commands:"
	@echo ""
	@echo "Development:"
	@echo "  dev-start     Start development environment"
	@echo "  dev-stop      Stop development environment"
	@echo "  dev-restart   Restart development environment"
	@echo "  dev-logs      Show logs from all services"
	@echo "  dev-build     Build development images"
	@echo "  dev-clean     Clean up development resources"
	@echo ""
	@echo "Production:"
	@echo "  prod-build-db      Build database production image"
	@echo "  prod-build-api     Build API production image"
	@echo "  prod-build-scraper Build scraper production image"
	@echo "  prod-build-all     Build all production images"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  test          Run tests"
	@echo "  lint          Run linting"
	@echo "  format        Format code"
	@echo ""
	@echo "Utilities:"
	@echo "  db-shell      Connect to development database"
	@echo "  api-shell     Shell into API container"
	@echo "  scraper-run   Run scraper manually"

# Development commands
dev-start:
	@echo "Starting RetailFlux development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Services started. API: http://localhost:8000"

dev-stop:
	@echo "Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

dev-restart: dev-stop dev-start

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-build:
	@echo "Building development images..."
	docker-compose -f docker-compose.dev.yml build

dev-clean:
	@echo "Cleaning up development resources..."
	docker-compose -f docker-compose.dev.yml down -v --rmi local
	docker system prune -f

# Production builds
prod-build-db:
	@echo "Building database production image..."
	docker build -f deployments/database/Dockerfile -t retailflux/database:latest .

prod-build-api:
	@echo "Building API production image..."
	docker build -f deployments/api/Dockerfile -t retailflux/api:latest .

prod-build-scraper:
	@echo "Building scraper production image..."
	docker build -f deployments/scraper/Dockerfile -t retailflux/scraper:latest .

prod-build-all: prod-build-db prod-build-api prod-build-scraper
	@echo "All production images built successfully!"

# Database utilities
db-shell:
	@echo "Connecting to development database..."
	docker-compose -f docker-compose.dev.yml exec postgres_db psql -U cristian -d products_db_dev

# Service utilities
api-shell:
	docker-compose -f docker-compose.dev.yml exec api bash

scraper-shell:
	docker-compose -f docker-compose.dev.yml exec scraper bash

scraper-run:
	@echo "Running scraper manually..."
	docker-compose -f docker-compose.dev.yml exec scraper python services/scraper/run_modern_spider.py

# Testing and quality
test:
	@echo "Running tests..."
	docker-compose -f docker-compose.dev.yml exec api python -m pytest
	docker-compose -f docker-compose.dev.yml exec scraper python -m pytest

lint:
	@echo "Running linting..."
	docker-compose -f docker-compose.dev.yml exec api flake8 services/api/
	docker-compose -f docker-compose.dev.yml exec scraper flake8 services/scraper/

format:
	@echo "Formatting code..."
	docker-compose -f docker-compose.dev.yml exec api black services/api/
	docker-compose -f docker-compose.dev.yml exec scraper black services/scraper/

# Setup commands
setup-dev:
	@echo "Setting up development environment..."
	cp .env.dev .env
	make dev-build
	make dev-start
	@echo "Development environment ready!"

# Health checks
health:
	@echo "Checking service health..."
	@curl -f http://localhost:8000/health || echo "API not responding"
	@docker-compose -f docker-compose.dev.yml exec postgres_db pg_isready -U cristian || echo "Database not ready"