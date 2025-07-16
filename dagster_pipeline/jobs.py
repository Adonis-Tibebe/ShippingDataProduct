from dagster import job
from dagster_pipeline.ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    load_media_index,
    run_yolo_enrichment,
    load_media_detections,
    enrich_telegram_messages,
    run_dbt_transformations
)

@job
def shipping_data_pipeline():
    # 1. Scrape Telegram data (messages and media)
    scrape = scrape_telegram_data()

    # 2. Load raw messages to Postgres (depends on scraping)
    load_msgs = load_raw_to_postgres(scrape)

    # 3. Load media index to Postgres (depends on scraping)
    load_media = load_media_index(scrape)

    # 4. Run YOLO enrichment on media (depends on scraping)
    yolo = run_yolo_enrichment(scrape)

    # 5. Load YOLO detections to Postgres (depends on YOLO enrichment)
    load_detections = load_media_detections(yolo)

    # 6. Enrich Telegram messages (depends on loading messages and detections)
    enrich = enrich_telegram_messages(load_msgs, load_detections)

    # 7. Run dbt transformations (depends on all data loaded and enriched)
    run_dbt_transformations(enrich, load_media) 