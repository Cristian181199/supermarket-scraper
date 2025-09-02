# Supermarket Scraper

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Scrapy Version](https://img.shields.io/badge/scrapy-2.11%2B-green.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL-blue.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

A robust and scalable web scraping system designed to collect product data from supermarket websites. This project is the data acquisition engine for a future AI-powered shopping assistant. The initial implementation targets **Edeka24 (Germany)**, with a modular architecture built for expansion.

## ✨ Features

- **Automated Data Extraction**: Crawls supermarket websites starting from sitemap indexes to discover and scrape product information.
- **Normalized Database Schema**: Stores data in a structured PostgreSQL database with relational tables for products, categories (hierarchical), stores, and manufacturers.
- **Containerized Environment**: Uses **Docker** and **Docker Compose** for a reproducible, isolated, and easy-to-deploy development environment.
- **Resilient Pipeline**: The Scrapy pipeline handles the creation of the database schema and intelligently inserts or updates products (`UPSERT`) to avoid duplicates.
- **Respectful Crawling**: Configured to obey `robots.txt` rules and maintain a polite `DOWNLOAD_DELAY` to minimize server load.

## 🛠️ Technology Stack

- **Scraper**: **Scrapy** (Python)
- **Database**: **PostgreSQL**
- **Containerization**: **Docker** & **Docker Compose**
- **Dependencies**: `psycopg2-binary`, `python-dotenv`

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose installed.
- [Git](https://git-scm.com/) installed.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/cristian181199/supermarket-scraper.git](https://github.com/cristian181199/supermarket-scraper.git)
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