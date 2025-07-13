# ETL & Database Scripts

This directory contains essential scripts for managing the ETL pipeline and database integration for the ShippingDataProduct project. These scripts are responsible for creating tables, loading raw and enriched data, and preparing the warehouse for analytics and modeling.

## Scripts Overview

- **create_tables.py**
  - Creates the necessary PostgreSQL schema and tables for storing raw Telegram messages and media.
  - Run this script first to initialize your database structure.

- **load_messages.py**
  - Loads scraped Telegram messages from JSON files (produced by the scraper) into the `raw.telegram_messages` table in PostgreSQL.
  - Run after new data is scraped and available in the `data/raw/telegram_messages/` directory.

- **load_media_index.py**
  - Loads media metadata from the media index JSON file into the `raw.telegram_media` table in PostgreSQL.
  - Run after new media is scraped and indexed in `data/raw/media_index_<date>.json`.

- **enrich_telegram_messages.py**
  - Enriches raw messages in the database by extracting product names, prices, and health-related flags using custom extractors.
  - Stores the results in the `raw.telegram_enriched` table for downstream analytics.

## Usage

1. **Set up your environment:**
   - Ensure your PostgreSQL credentials are set in a `.env` file at the project root.
   - Install dependencies from the main `requirements.txt`.

2. **Run the scripts in order:**
   ```bash
   python create_tables.py
   python load_messages.py
   python load_media_index.py
   python enrich_telegram_messages.py
   ```

3. **Check your database:**
   - The tables `raw.telegram_messages`, `raw.telegram_media`, and `raw.telegram_enriched` should be populated and ready for analytics.

## Notes

- All scripts use the shared configuration loader in `config/config.py` to read database credentials.
- Logging is enabled for each script to provide progress and error information.
- These scripts are designed to be run manually or orchestrated as part of a larger pipeline.

## Extending

- To add new ETL steps, create additional scripts in this directory and follow the existing structure for configuration and logging.
- For analytics and modeling, see the `ShippingData/` dbt project.

---

For more details on the data pipeline and analytics, see the main project README and the dbt project documentation.
