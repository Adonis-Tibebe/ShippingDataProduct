from dagster import op
import sys 
import os
import subprocess
sys.path.append(os.path.abspath('../'))

@op
def scrape_telegram_data(context):
    context.log.info("Starting Telegram scraping via Dagster...")
    from src.services.telegram_scrapper import run_scraper
    run_scraper()
    context.log.info("Scraping complete.")
    return "scraped"

@op
def load_raw_to_postgres(context, scrape_result):
    context.log.info(f"Loading raw messages to Postgres after: {scrape_result}")
    script_path = os.path.join(os.getcwd(), "scripts", "load_messages.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"load_messages.py failed: {result.stderr}")
    context.log.info("Raw messages loaded to Postgres.")
    return "messages_loaded"

@op
def load_media_index(context, scrape_result):
    context.log.info(f"Loading media index to Postgres after: {scrape_result}")
    script_path = os.path.join(os.getcwd(), "scripts", "load_media_index.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"load_media_index.py failed: {result.stderr}")
    context.log.info("Media index loaded to Postgres.")
    return "media_index_loaded"

@op
def run_yolo_enrichment(context, scrape_result):
    context.log.info(f"Running YOLO enrichment after: {scrape_result}")
    script_path = os.path.join(os.getcwd(), "src", "models", "run_yolov8_detection.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"run_yolov8_detection.py failed: {result.stderr}")
    context.log.info("YOLO enrichment complete.")
    return "yolo_done"

@op
def load_media_detections(context, yolo_result):
    context.log.info(f"Loading media detections after: {yolo_result}")
    script_path = os.path.join(os.getcwd(), "scripts", "load_media_detections.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"load_media_detections.py failed: {result.stderr}")
    context.log.info("Media detections loaded to Postgres.")
    return "detections_loaded"

@op
def enrich_telegram_messages(context, messages_loaded, detections_loaded):
    context.log.info(f"Enriching messages after: {messages_loaded}, {detections_loaded}")
    script_path = os.path.join(os.getcwd(), "scripts", "enrich_telegram_messages.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"enrich_telegram_messages.py failed: {result.stderr}")
    context.log.info("Messages enriched and loaded.")
    return "enriched"

@op
def run_dbt_transformations(context, enriched_result, media_index_loaded):
    context.log.info(f"Running dbt transformations after: {enriched_result}, {media_index_loaded}")
    dbt_dir = os.path.join(os.getcwd(), "ShippingData")
    result = subprocess.run(["dbt", "build"], cwd=dbt_dir, capture_output=True, text=True)
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception(f"dbt build failed: {result.stderr}")
    context.log.info("dbt transformations complete.")
    return "dbt_done" 