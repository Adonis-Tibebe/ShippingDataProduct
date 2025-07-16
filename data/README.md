# Data Directory

This directory contains all data files used and produced by the ShippingDataProduct project.

## Structure

- `raw/` — Contains raw data files as scraped or received, including:
  - `telegram_messages/` — Raw Telegram messages (JSON)
  - `telegram_media/` — Raw media files (images, etc.)
  - `media_index_<date>.json` — Index of media files with metadata
- `processed/` — Contains processed or enriched data, such as:
  - `media_detection_results.json` — YOLO detection results on media
- `.dvc` files — Data Version Control (DVC) files track large data files and directories for reproducibility and sharing.

## Data Flow
- Raw data is scraped and stored in `raw/`.
- Media and message indexes are generated and tracked with DVC.
- Processed data (e.g., detection results) is saved in `processed/` for downstream analytics.

## Notes
- Do not commit large data files directly to git; use DVC for versioning and sharing data.
- See the main project README for more on the data pipeline and usage.
