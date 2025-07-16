# Dagster Pipeline for ShippingDataProduct

This directory contains the Dagster orchestration project for the ShippingDataProduct data pipeline.

## What is Dagster?
Dagster is a modern data orchestrator for building, running, and monitoring data pipelines. It helps you:
- Automate and schedule your workflows
- Track and debug pipeline runs
- Visualize dependencies and data flow
- Develop pipelines locally with a powerful UI

## What Does This Pipeline Do?
This pipeline automates the end-to-end ETL and analytics workflow:
1. **Scrape Telegram Data:** Collects messages and media from Telegram channels
2. **Load Raw Data to Postgres:** Loads scraped messages into the database
3. **Load Media Index:** Loads media metadata into the database
4. **Run YOLO Enrichment:** Runs YOLOv8 object detection on media
5. **Load Media Detections:** Loads YOLO detection results into the database
6. **Enrich Telegram Messages:** Extracts product, price, and health info from messages
7. **Run dbt Transformations:** Runs dbt models for analytics and reporting

## How to Run the Pipeline
1. **Start the Dagster UI:**
   ```bash
   dagster dev -f dagster_pipeline/repository.py
   ```
   This launches the Dagster web UI at http://localhost:3000

2. **Run the Pipeline:**
   - In the UI, select the `shipping_data_pipeline` job and click "Launch Run".
   - You can monitor progress, view logs, and debug failures.

3. **Scheduling:**
   - The pipeline is scheduled to run daily at 2am UTC by default.
   - You can adjust the schedule in `schedules.py`.

## Learning Resources
- [Dagster Documentation](https://docs.dagster.io/)
- [Dagster Concepts: Jobs, Ops, Schedules](https://docs.dagster.io/concepts)
- [Dagster Tutorials](https://docs.dagster.io/tutorial)

## Next Steps
- Implement each op in `ops.py` to call your existing scripts or refactor them as functions.
- Add error handling and logging for observability.
- Use the Dagster UI to experiment, debug, and learn how orchestration works!

---

If you have questions about any step or want to learn more about orchestration, just ask! 