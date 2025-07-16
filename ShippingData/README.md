# 📦 Shipping Data dbt Project

Welcome to the `shipping_data` dbt repository — a robust, modular analytics warehouse purpose-built for analyzing Telegram channel data. This project leverages staged ingestion, dimensional enrichment, and fact modeling to extract insights from scraped messages, product mentions, and media object detections (YOLO).

---

## Project Overview

- **Source**: Scraped Telegram messages and media across multiple channels, loaded into PostgreSQL tables (e.g., `raw.telegram_messages`, `raw.telegram_enriched`, `raw.media_detections`) by the ETL pipeline.
- **Objective**: Identify and enrich product mentions, flag health-related messages, track media content and object detections, and analyze performance across time and source.
- **Pipeline Architecture**:
  - `staging/`: Raw ingestion and regex-based parsing from source tables, including YOLO detection results.
  - `dimensions/`: Dimension tables for message, channel, date, product.
  - `mart/`: Fact models for analytics-ready queries and surrogate-keyed reference tables, including media detections.
  - `analysis/`: Ranked insight models and drill-downs (e.g., top products per channel, media coverage).
  - `tests/`: Data contract validation and business rule enforcement.
  - `docs/`: Optional screenshots or HTML output.

---

## Data Integration & Warehouse Setup
- **Expected Source Tables:**
  - `raw.telegram_messages`: Raw messages loaded from JSON files.
  - `raw.telegram_enriched`: Enriched messages with extracted product names, prices, and health flags.
  - `raw.telegram_media`: Metadata for downloaded media files.
  - `raw.media_detections`: YOLOv8 detection results for Telegram media (images), loaded from processed JSON.
- **Warehouse:**
  - This project expects a PostgreSQL warehouse. Configure your connection in `~/.dbt/profiles.yml`.
- **Data Flow Example:**
  - `raw.telegram_messages` → `staging.stg_telegram_messages` → `dimensions.dim_product`/`mart.fct_messages`
  - `raw.media_detections` → `staging.stg_media_detections` → `mart.fct_media` → `analysis.media_coverage_by_channel`

---

## 📂 Project Structure
analyses/
models/
├── staging/ # Raw cleaned inputs from Telegram scraping and YOLO detections
├── dimensions/ # Dimension tables: message, channel, date, product
├── mart/ # Fact tables like fct_messages, fct_media
├── analysis/ # Insight layers like top 3 products per channel, media coverage

tests/ # Custom data tests enforcing business rules

macros/ # Utility logic 
snapshots/ # Documentation artifacts or screenshots 
tests/ # for 
.gitignore
dbt_project.yml # Main DBT configuration file

---

## Key Models
- **staging/stg_telegram_messages**: Cleans and normalizes raw Telegram messages for downstream use.
- **staging/stg_media_detections**: Stages YOLOv8 object detection results from media for analytics.
- **dimensions/dim_product**: Unique product names extracted from messages, with optional enrichment.
- **dimensions/dim_channel**: Channel metadata and mapping.
- **mart/fct_messages**: Fact table joining messages, products, and enrichment flags for analytics.
- **mart/fct_media**: Fact table for YOLO object detections, joined to message and channel dimensions.
- **analysis/media_coverage_by_channel**: Channel-level breakdown of visual content and detection rates.
- **analysis/top_products_per_channel**: Ranks and aggregates product mentions by channel and time.

---

## Custom Macros & Tests
- **Custom Macros:** Found in `macros/`, used for reusable SQL logic (e.g., surrogate key generation, date handling).
- **Custom Tests:** Found in `tests/`, enforce business rules (e.g., `main_price > 0`, not_null/unique constraints, row-level filters).

---

## Example Queries & Use Cases
- **Top 3 products per channel in the last month:**
  ```sql
  select * from analysis.top_products_per_channel where date >= current_date - interval '30 days';
  ```
- **All health-related product mentions:**
  ```sql
  select * from mart.fct_messages where is_health_related = true;
  ```
- **Product mention trends over time:**
  ```sql
  select product_name, date_trunc('month', message_date) as month, count(*)
  from mart.fct_messages
  group by product_name, month
  order by month, count desc;
  ```
- **Media coverage and detection rates by channel:**
  ```sql
  select * from analysis.media_coverage_by_channel order by detection_rate desc;
  ```
- **YOLO object detection results for a specific channel:**
  ```sql
  select * from mart.fct_media where channel_id = 123;
  ```

---

## How to Use This Project

### Setup

Ensure your warehouse profile is configured in `~/.dbt/profiles.yml`. Then run:
- ```bash
dbt deps           # Install any packages (not applicable for this project)
dbt seed           # Load CSV seed files (not used for this project)
dbt run            # Build all models
dbt test           # Validate models with schema and custom tests
dbt docs generate  # Compile interactive documentation
dbt docs serve     # Preview docs locally in your browser
```

### You can also run specific models or tests
```bash
dbt run --select fct_messages
dbt test --select dim_message_metadata
```

---

## Contribution & Development Notes
- Add new models in the appropriate subdirectory (`staging/`, `dimensions/`, `mart/`, `analysis/`).
- Document models with `description` fields in .yml files for better docs.
- Use `dbt test` to validate changes before merging.
- Follow existing naming conventions for consistency.

---

## Troubleshooting & Common Issues
- **Missing source tables:** Ensure the ETL pipeline has loaded data into the expected `raw.*` tables, including `raw.media_detections` for YOLO results.
- **Schema mismatches:** Check that your warehouse schema matches the model definitions.
- **Profile errors:** Verify your `~/.dbt/profiles.yml` is correctly configured for your environment.
- **Data freshness:** If models are empty, check that the ETL pipeline has run and loaded recent data, including YOLO detection results.

---

## Data Testing Strategy

All models include standard and custom data tests:
- not_null and unique tests for surrogate keys
- Business rules like main_price > 0
- SQL-based row-level validations for edge-case filtering
- Media detection models include tests for detection_id, label, and relationships to message/channel dimensions

To run tests:
```bash
dbt test
```
