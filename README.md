# ShippingDataProduct

ShippingDataProduct is a robust data pipeline and analytics platform for scraping, extracting, enriching, and analyzing messages and media from Telegram channels related to pharmaceuticals and cosmetics.

---

## Features

- Scrapes messages and media (images) from Telegram channels using Telethon.
- Extracts product names, prices, and health-related flags from messages.
- Runs YOLOv8 object detection on media and integrates results into analytics.
- Orchestrates the full ETL and analytics pipeline with Dagster.
- Serves analytics via a FastAPI API.
- Data versioning and management with DVC.
- Automated testing and CI with GitHub Actions.
- Ready for containerized deployment with Docker and Docker Compose.

---

## Directory Structure

- `src/services/telegram_scrapper.py` — Telegram scraping logic.
- `src/utils/Extractors.py` — Data extraction utilities.
- `data/` — Raw and processed data, tracked with DVC.
- `notebooks/` — Jupyter notebooks for prototyping and analysis.
- `config/` — Configuration and credential loading.
- `scripts/` — ETL and database utility scripts.
- `ShippingData/` — dbt analytics project for transforming and modeling data.
- `analytics_api/` — FastAPI app for serving analytics endpoints.
- `dagster_pipeline/` — Dagster orchestration project for the full pipeline.
- `Makefile` — Common developer commands.
- `pyproject.toml` — Project metadata and formatting tools.

---

## Orchestration & Automation (`dagster_pipeline/`)

- **Purpose:** Automates the full ETL and analytics workflow using Dagster.
- **How to run:**  
  ```bash
  make run-dagster
  # or
  dagster dev -f dagster_pipeline/repository.py
  ```
- **Features:** Visual pipeline, scheduling, observability, and error handling.

---

## Analytics API (`analytics_api/`)

- **Purpose:** Serves analytics endpoints for querying product mentions, pricing, media coverage, and more.
- **How to run:**  
  ```bash
  make run-api
  # or
  uvicorn analytics_api.main:app --reload
  ```
- **Endpoints:** See `analytics_api/README.md` for full API documentation.

---

## ETL & Database Scripts (`scripts/`)

- **Purpose:** Scripts for loading, enriching, and managing data in PostgreSQL.
- **How to use:** See `scripts/README.md` for details and usage order.

---

## Analytics & Modeling (`ShippingData/`)

- **Purpose:** dbt project for transforming raw and enriched data into analytics-ready tables.
- **How to use:**  
  ```bash
  make dbt-build
  # or
  cd ShippingData
  dbt run
  dbt test
  dbt docs serve
  ```
- **Details:** See `ShippingData/README.md` for model and analytics documentation.

---

## Data & Notebooks

- **`data/`**: Raw and processed data, tracked with DVC. See `data/README.md`.
- **`notebooks/`**: Jupyter notebooks for prototyping and analysis. See `notebooks/README.md`.

---

## Testing & CI

- **Unit tests:**  
  ```bash
  make test
  # or
  pytest tests
  ```
- **CI:** Automated with GitHub Actions on Windows (see `.github/workflows/ci.yml`).

---

## Makefile & pyproject.toml

- **Makefile:** Common commands for setup, testing, running services, and cleaning.
- **pyproject.toml:** Project metadata and formatting tool configs.

---

## Installation & Setup

1. **Install dependencies:**  
   ```bash
   make setup
   ```
2. **Configure `.env` file** with Telegram and database credentials.
3. **Initialize Telegram session:**  
   ```bash
   python src/services/initialize_session.py
   ```
4. **Run the pipeline and analytics API as needed.**

---

## Docker & Docker Compose

- **Purpose:** Easily run the full stack (API, database, scraper) in isolated containers.
- **Services:**
  - `analytics_api`: FastAPI analytics service (port 8000)
  - `db`: PostgreSQL database (port 5431 on host, 5432 in container)
  - `telegram_scraper`: Telegram scraping service
- **How to build and run:**
  ```bash
  docker-compose up --build
  ```
- **Volumes:**
  - Database data is persisted in a Docker volume (`pgdata`).
  - Source code and data directories are mounted for live development and data sharing.
- **Environment:**
  - All services use the `.env` file at the project root for credentials and configuration.
- **Stopping and cleaning up:**
  ```bash
  docker-compose down
  # To remove volumes:
  docker-compose down -v
  ```
- **Notes:**
  - Use the docker_requirements.txt to install dependencies.
  - The API and scraper containers mount your local code for easy development.
  - The database is accessible on port 5431 for local tools (e.g., pgAdmin, DBeaver).

---

## Data Versioning

- DVC is used to track and version data files.  
  ```bash
  dvc add data/raw/telegram_messages
  dvc add data/raw/telegram_media
  dvc push
  dvc pull
  ```

---

## License

_None_

---

## For More Details

See the code in each directory, the subdirectory READMEs, and the dbt and Dagster documentation. For questions, open an issue or contact the maintainer.
