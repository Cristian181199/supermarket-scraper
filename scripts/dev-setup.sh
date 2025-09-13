#!/bin/bash
# Development Environment Setup Script

set -e

echo "🚀 Setting up Edeka Scraper Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Navigate to the infrastructure directory
cd "$(dirname "$0")/../infrastructure"

print_status "Setting up development environment..."

# Stop any existing containers
print_status "Stopping existing containers..."
docker-compose -f docker-compose.dev.yml down --remove-orphans

# Build containers
print_status "Building containers..."
docker-compose -f docker-compose.dev.yml build

# Start PostgreSQL
print_status "Starting PostgreSQL..."
docker-compose -f docker-compose.dev.yml up -d postgres_db

# Wait for PostgreSQL to be ready
print_status "Waiting for PostgreSQL to be ready..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.dev.yml exec postgres_db psql -U cristian -d products_db_dev -c "
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
"

# Create a simple migration runner
print_status "Creating tables..."
docker-compose -f docker-compose.dev.yml run --rm api python -c "
import sys
sys.path.append('/usr/src/app')
from shared.database.config import db_manager
from shared.database.models import Base

# Create all tables
db_manager.engine.dispose()
Base.metadata.create_all(db_manager.engine)
print('✅ Database tables created successfully!')
"

print_status "Development environment is ready!"
print_status "Available commands:"
echo "  • Start API: docker-compose -f docker-compose.dev.yml up api"
echo "  • Run Scraper: docker-compose -f docker-compose.dev.yml run --rm scraper"
echo "  • View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "  • Stop all: docker-compose -f docker-compose.dev.yml down"

print_status "Database connection details:"
echo "  • Host: localhost"
echo "  • Port: 5433"
echo "  • Database: products_db_dev"
echo "  • User: cristian"
echo "  • Password: cristian"

print_status "Setup completed! 🎉"