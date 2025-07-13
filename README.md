# ShippingDataProduct

ShippingDataProduct is a data pipeline for scraping, extracting, and storing messages and media from selected Telegram channels related to pharmaceuticals and cosmetics. The project is designed for data collection, analysis, and future integration with data science or backend services.

## Features
- Scrapes messages and media (images) from specified Telegram channels using Telethon.
- Saves messages as structured JSON files and media as images, organized by date and channel.
- Utilities for extracting product names, prices, and health-related flags from messages.
- Data versioning and management with DVC.
- Ready for containerized deployment with Docker and Docker Compose.

## Directory Structure
- `src/services/telegram_scrapper.py` — Main script for scraping Telegram messages and media.
- `src/utils/Extractors.py` — Utilities for extracting structured data (products, prices, etc.) from messages.
- `data/raw/telegram_messages/` — Scraped messages in JSON format, organized by date and channel.
- `data/raw/telegram_media/` — Downloaded media files (images) from Telegram channels.
- `config/` — Configuration and credential loading scripts.
- `requirements.txt` — Python dependencies.
- `docker-compose.yml` — Multi-service orchestration (scraper, database, and a placeholder for a future app backend).
- `scripts/` — ETL and database utility scripts for loading, enriching, and managing data in PostgreSQL.
- `ShippingData/` — dbt analytics project for transforming and modeling Telegram data for analysis.

---

## ETL & Database Scripts (`scripts/`)
This directory contains essential scripts for managing the ETL pipeline and database:
- **create_tables.py**: Creates the necessary PostgreSQL schema and tables for raw Telegram messages and media.
- **load_messages.py**: Loads scraped Telegram messages from JSON files into the database.
- **load_media_index.py**: Loads media metadata (from the media index JSON) into the database.
- **enrich_telegram_messages.py**: Enriches raw messages in the database by extracting product names, prices, and health-related flags, and stores the results in a new table.

Run these scripts in order to set up and populate your database with both raw and enriched data.

---

## Analytics & Modeling (`ShippingData/`)
This directory is a full-featured **dbt analytics project** for transforming and modeling the Telegram data:
- **Purpose**: Turns raw scraped and loaded data into analytics-ready tables and insights.
- **Structure**: Includes staging, dimension, mart, and analysis models, as well as tests and macros.
- **Usage**: See `ShippingData/README.md` for full details. Typical workflow:
  ```bash
  cd ShippingData
  dbt run            # Build all models
  dbt test           # Validate models
  dbt docs generate  # Generate documentation
  dbt docs serve     # Preview docs locally
  ```
- **Testing**: Includes both standard and custom data tests for data quality and business rules.

---

## Installation

```bash
pip install -r requirements.txt
```

Or, using Docker Compose (recommended for full pipeline):

```bash
docker-compose up --build
```

## Setup
1. **Telegram API Credentials:**
   - Create a `.env` file in the project root with the following variables:
     ```env
     TG_API_ID=your_telegram_api_id
     TG_API_HASH=your_telegram_api_hash
     phone=your_telegram_phone_number
     POSTGRES_USER=your_db_user
     POSTGRES_PASSWORD=your_db_password
     POSTGRES_DB=your_db_name
     DB_HOST=db
     DB_PORT=5432
     ```
2. **Initialize Telegram Session:**
   - Run the session initializer to authenticate your Telegram account:
     ```bash
     python src/services/initialize_session.py
     ```

## Usage
- **Run the Scraper:**
  ```bash
  python src/services/telegram_scrapper.py
  ```
  This will scrape messages and media from the configured channels and save them in `data/raw/telegram_messages/` and `data/raw/telegram_media/`.

- **Data Output:**
  - Messages: `data/raw/telegram_messages/<YYYY-MM-DD>/<channel>.json`
  - Media: `data/raw/telegram_media/`
  - Media index: `data/raw/media_index_<YYYY-MM-DD>.json`

- **Data Extraction Utilities:**
  Use functions in `src/utils/Extractors.py` to extract product names, prices, and health flags from the scraped messages.

## Data Versioning
- DVC is used to track and version data files. To push/pull data, use:
  ```bash
  dvc add data/raw/telegram_messages
  dvc add data/raw/telegram_media
  dvc push
  dvc pull
  ```

## Extending the Project
- The project is ready for further development, such as:
  - **FastAPI backend:** The `docker-compose.yml` reserves port 8000 for a future FastAPI (or similar) backend, but this is currently just a placeholder and not implemented yet.
  - Integrating with PostgreSQL for structured data storage.
  - Building data analysis or visualization notebooks in `notebooks/`.

## Dependencies
See `requirements.txt` for the full list. Key packages:
- Telethon
- python-dotenv
- DVC
- Docker, Docker Compose
- dbt (for analytics in ShippingData/)

## License
 None 
---
For more details, see the code in `src/services/telegram_scrapper.py`, `src/utils/Extractors.py`, the `scripts/` directory, and the `ShippingData/` dbt project. For questions, open an issue or contact the maintainer.
