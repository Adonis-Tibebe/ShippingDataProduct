# Analytics API

This directory contains the FastAPI-based analytics service for the ShippingDataProduct project. The API exposes analytical endpoints for querying insights from the processed Telegram health data warehouse, including product mentions, pricing trends, media coverage, and message search.

## Overview

- **Framework:** FastAPI
- **Database:** PostgreSQL (accesses dbt-generated models/views)
- **ORM:** SQLAlchemy (read-only queries)
- **Schema Validation:** Pydantic
- **Location:** `analytics_api/`

## Features

- **Top Product Mentions:** Retrieve the most mentioned products across Telegram channels.
- **Channel Activity:** Get media coverage and detection rates for a specific channel.
- **Message Search:** Search Telegram messages by text content.
- **Product Pricing:** View price statistics for products by channel.
- **Health Checks:** API and database connectivity checks.

## Directory Structure

- `main.py` — FastAPI app and route definitions
- `crud.py` — SQL query functions for analytics
- `database.py` — Database connection/session management
- `schemas.py` — Pydantic models for request/response validation
- `models.py` — (Placeholder for future ORM models)

## Setup & Running

1. **Install dependencies:**
   Ensure you have Python 3.9+ and install requirements:
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Configure environment:**
   - Place a `.env` file with PostgreSQL credentials at the project root (see `config/config.py` for required variables).

3. **Run the API server:**
   ```bash
   uvicorn main:app --reload
   ```
   (Run from within the `analytics_api/` directory.)

## API Endpoints

### Health & Connectivity
- `GET /api/health-check` — Check if the API is running.
- `GET /api/db-check` — Check database connectivity.

### Analytics & Reports
- `GET /api/reports/top-products?limit=10` — List top mentioned products (limit configurable).
- `GET /api/channels/{channel_name}/activity` — Get media coverage and detection stats for a channel.
- `GET /api/search/messages?query=...` — Search messages containing a text query.
- `GET /api/reports/product-pricing?product_name=...` — Get price stats for a product by channel.

## Example Usage

- **Get top 5 products:**
  ```bash
  curl 'http://localhost:8000/api/reports/top-products?limit=5'
  ```
- **Channel activity:**
  ```bash
  curl 'http://localhost:8000/api/channels/SomeChannel/activity'
  ```
- **Search messages:**
  ```bash
  curl 'http://localhost:8000/api/search/messages?query=aspirin'
  ```
- **Product pricing:**
  ```bash
  curl 'http://localhost:8000/api/reports/product-pricing?product_name=aspirin'
  ```

## Notes
- All endpoints return JSON responses wrapped in a standard format: `{ success, count, data }`.
- The API is read-only and safe for analytics workloads.
- CORS is enabled for development (allowing all origins).

## Extending
- To add new analytics endpoints, implement SQL queries in `crud.py`, define schemas in `schemas.py`, and add routes in `main.py`.
- For more on the data pipeline and dbt models, see the main project README and `ShippingData/` directory.

---

For questions or contributions, see the main project repository. 