# Edeka Scraper

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Scrapy Version](https://img.shields.io/badge/scrapy-2.13-green.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL-blue.svg)
![Migrations](https://img.shields.io/badge/migrations-Alembic-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A production-ready web scraping system designed to collect product data from **Edeka24 (Germany)**. Built with a clean, maintainable architecture that separates concerns between data extraction and database management. This project serves as the foundation for a future AI-powered shopping assistant.

## ✨ Features

- **🕷️ Automated Data Extraction**: Crawls Edeka24 starting from sitemaps to discover and scrape comprehensive product information
- **🗄️ Normalized Database Schema**: Structured PostgreSQL database with relational tables for products, hierarchical categories, stores, and manufacturers  
- **🔄 Database Migrations**: Full Alembic integration for schema versioning and automated database updates
- **🐳 Containerized Environment**: Complete Docker setup with separate containers for scraper and PostgreSQL
- **🛠️ Management Scripts**: Easy-to-use commands for all operations (start, migrate, scrape, clean)
- **💾 Smart Data Pipeline**: Intelligent UPSERT operations to handle product updates and avoid duplicates
- **🤝 Respectful Crawling**: Obeys robots.txt, implements download delays, and uses descriptive User-Agent
- **🏗️ Clean Architecture**: Separated scraper logic from database models with proper dependency injection

## 🛠️ Technology Stack

- **Web Scraping**: Scrapy 2.13+ with custom pipelines
- **Database**: PostgreSQL 15 with SQLAlchemy ORM  
- **Migrations**: Alembic for database schema management
- **Containerization**: Docker & Docker Compose
- **Environment**: Python 3.11, python-dotenv, psycopg2-binary

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose installed.
- [Git](https://git-scm.com/) installed.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/cristian181199/supermarket-scraper.git
    cd supermarket-scraper
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the project root by copying the example file.
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and set your desired database credentials.

3.  **Build and Run the Containers:**
    This command will build the Scrapy image, pull the PostgreSQL image, and start both services in detached mode.
    ```bash
    docker-compose up --build -d
    ```
    The scraper container will start and wait for tasks. The database will be initialized, and the necessary tables will be created automatically by the pipeline on the first run.

## Usage

The scraper is designed to be run manually from within its Docker container.

1.  **Access the scraper container's shell:**
    ```bash
    docker exec -it scraper /bin/bash
    ```

2.  **Run the Edeka spider:**
    Once inside the container, you can start the crawl with the following command:
    ```bash
    scrapy crawl edeka
    ```
    The spider will begin by parsing the sitemaps, discovering product URLs, and scraping the data. You will see the progress in the terminal logs.

3.  **Check the data in the database:**
    You can connect to the PostgreSQL database using any standard client (like DBeaver or TablePlus) with the credentials you set in your `.env` file.
    - **Host**: `localhost`
    - **Port**: `5432`
    - **Database**: `products_db`
    - **User**: (your user)
    - **Password**: (your password)

##  Roadmap & Future Improvements

This project is under active development. Future enhancements include:

- [ ] **Implement SQLAlchemy ORM**: Integrate **SQLAlchemy** to abstract database interactions, enabling schema migrations (with Alembic) and preparing for advanced features like vector search with `pgvector`.
- [ ] **Refactor Project Structure**: Reorganize the project layout by moving all Docker-related files into a dedicated `/docker` directory to better separate infrastructure from application code.
- [ ] **Environment-Specific Configurations**: Create separate setups for **development** and **production** environments (e.g., distinct `Dockerfiles`) to optimize for security, performance, and ease of development.
- [ ] **Robust Error Handling**: Improve spider resilience to handle missing data fields or changes in website structure without crashing.
- [ ] **Proxy Integration**: Implement rotating proxies to increase scraping speed and avoid IP bans.
- [ ] **API Development**: Build a **FastAPI** service to expose the collected data.
- [ ] **AI Shopping Assistant**: Use the API to power a conversational AI that provides smart shopping recommendations.
- [ ] **Expansion**: Develop new spiders for other supermarkets (e.g., Rewe, Lidl).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.