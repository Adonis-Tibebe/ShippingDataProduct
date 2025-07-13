# 📦 Shipping Data dbt Project

Welcome to the `shipping_data` dbt repository — a robust, modular analytics warehouse purpose-built for analyzing Telegram channel data. This project leverages staged ingestion, dimensional enrichment, and fact modeling to extract insights from scraped messages and product mentions.

---

## Project Overview

- **Source**: Scraped Telegram messages across multiple channels, loaded into PostgreSQL tables (e.g., `raw.telegram_messages`, `raw.telegram_enriched`) by the ETL pipeline.
- **Objective**: Identify and enrich product mentions, flag health-related messages, and track performance across time and source.
- **Pipeline Architecture**:
  - `staging/`: Raw ingestion and regex-based parsing from source tables.
  - `dimensions/`: Dimension tables for message, channel, date, product.
  - `mart/`: Fact models for analytics-ready queries and surrogate-keyed reference tables.
  - `analysis/`: Ranked insight models and drill-downs (e.g., top products per channel).
  - `tests/`: Data contract validation and business rule enforcement.
  - `docs/`: Optional screenshots or HTML output.

---

## Data Integration & Warehouse Setup
- **Expected Source Tables:**
  - `raw.telegram_messages`: Raw messages loaded from JSON files.
  - `raw.telegram_enriched`: Enriched messages with extracted product names, prices, and health flags.
  - `raw.telegram_media`: Metadata for downloaded media files.
- **Warehouse:**
  - This project expects a PostgreSQL warehouse. Configure your connection in `~/.dbt/profiles.yml`.
- **Data Flow Example:**
  - `raw.telegram_messages` → `staging.stg_telegram_messages` → `dimensions.dim_product`/`mart.fct_messages` → `analysis.top_products_per_channel`

---

## 📂 Project Structure
analyses/
models/
├── staging/ # Raw cleaned inputs from Telegram scraping
├── dimensions/ # Dimension tables: message, channel, date, product
├── mart/ # Fact tables like fct_messages
├── analysis/ # Insight layers like top 3 products per channel

tests/ # Custom data tests enforcing business rules

macros/ # Utility logic 
snapshots/ # Documentation artifacts or screenshots 
tests/ # for 
.gitignore
dbt_project.yml # Main DBT configuration file

---

## Key Models
- **staging/stg_telegram_messages**: Cleans and normalizes raw Telegram messages for downstream use.
- **dimensions/dim_product**: Unique product names extracted from messages, with optional enrichment.
- **dimensions/dim_channel**: Channel metadata and mapping.
- **mart/fct_messages**: Fact table joining messages, products, and enrichment flags for analytics.
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
- **Missing source tables:** Ensure the ETL pipeline has loaded data into the expected `raw.*` tables.
- **Schema mismatches:** Check that your warehouse schema matches the model definitions.
- **Profile errors:** Verify your `~/.dbt/profiles.yml` is correctly configured for your environment.
- **Data freshness:** If models are empty, check that the ETL pipeline has run and loaded recent data.

---

## Data Testing Strategy

All models include standard and custom data tests:
- not_null and unique tests for surrogate keys
- Business rules like main_price > 0
- SQL-based row-level validations for edge-case filtering

To run tests:
```bash
dbt test
```
