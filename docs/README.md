# ShippingDataProduct Documentation

Welcome to the documentation for ShippingDataProduct — a robust, end-to-end data pipeline and analytics platform for Telegram health and product data.

---

## Overview

ShippingDataProduct automates the scraping, enrichment, storage, and analytics of messages and media from Telegram channels. It integrates ETL, computer vision (YOLO), analytics modeling (dbt), orchestration (Dagster), and a FastAPI analytics API.

---

## Architecture

```mermaid
graph TD
    A[Telegram Channels] --> B[Scraper (Telethon)]
    B --> C[Raw Data (JSON, Images)]
    C --> D[ETL Scripts]
    D --> E[PostgreSQL Database]
    E --> F[dbt Transformations]
    F --> G[Analytics Tables]
    C --> H[YOLOv8 Detection]
    H --> I[Detection Results (JSON)]
    I --> D
    G --> J[FastAPI Analytics API]
    G --> K[Dashboards/Notebooks]
```

---

## Data Flow
1. **Scraping:**
   - Messages and media are scraped from Telegram using Telethon and saved as JSON/images.
2. **ETL:**
   - Scripts load raw data into PostgreSQL, enrich messages, and load YOLO detection results.
3. **Analytics Modeling:**
   - dbt transforms raw/enriched data into analytics-ready tables and views.
4. **Orchestration:**
   - Dagster automates and schedules the full pipeline, providing observability and error handling.
5. **API & Analysis:**
   - FastAPI serves analytics endpoints; notebooks and dashboards enable further exploration.

---

## Key Components
- **src/services/telegram_scrapper.py:** Telegram scraping logic
- **src/utils/Extractors.py:** Data extraction utilities
- **scripts/:** ETL and database utility scripts
- **ShippingData/:** dbt analytics project
- **analytics_api/:** FastAPI analytics API
- **dagster_pipeline/:** Dagster orchestration project
- **data/:** Raw and processed data (tracked with DVC)
- **notebooks/:** Jupyter notebooks for prototyping and analysis
- **Makefile:** Common developer commands
- **pyproject.toml:** Project metadata and formatting tools

---

## Setup & Developer Workflow
1. **Clone the repository and install dependencies:**
   ```bash
   make setup
   ```
2. **Configure your `.env` file** with Telegram and database credentials.
3. **Initialize Telegram session:**
   ```bash
   python src/services/initialize_session.py
   ```
4. **Run the pipeline and analytics API as needed:**
   - Dagster UI: `make run-dagster`
   - FastAPI: `make run-api`
   - Docker Compose: `docker-compose up --build`
5. **Run tests:**
   ```bash
   make test
   ```
6. **Build analytics models:**
   ```bash
   make dbt-build
   ```

---

## Data Versioning
- DVC is used to track and version large data files. See `data/README.md` for details.

---

## Subdirectory Documentation
- **ETL Scripts:** `scripts/README.md`
- **Analytics API:** `analytics_api/README.md`
- **dbt Project:** `ShippingData/README.md`
- **Data Directory:** `data/README.md`
- **Notebooks:** `notebooks/README.md`
- **Dagster Pipeline:** `dagster_pipeline/README.md`

---

## Contributing
- Follow the developer workflow above.
- Write tests for new features.
- Document new scripts, models, or endpoints in the appropriate README.
- Use the Makefile for common tasks.

---

## Support
For questions, open an issue or contact the maintainer.
