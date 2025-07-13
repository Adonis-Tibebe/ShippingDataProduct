import os
import sys
import json
import logging
from datetime import datetime
import psycopg2

sys.path.append(os.path.abspath("../"))
from config.config import load_db_credentials

# ✅ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ✅ Load DB credentials
logger.info("🔑 Loading database credentials...")
creds = load_db_credentials("../.env")

# ✅ Connect to PostgreSQL
logger.info("🔌 Connecting to PostgreSQL database...")
conn = psycopg2.connect(
    dbname=creds['db_name'],
    user=creds['db_user'],
    password=creds['db_password'],
    host=creds['db_host'],
    port=creds['db_port']
)
cursor = conn.cursor()
logger.info("✅ Connection established.")

# ✅ Locate media index file
INDEX_PATH = "../data/raw/media_index_2025-07-12.json"  # Update this dynamically later if needed for incrementing 
index_filename_date = INDEX_PATH.split("_")[-1].replace(".json", "")
scraped_at = datetime.strptime(index_filename_date, "%Y-%m-%d")

if not os.path.exists(INDEX_PATH):
    logger.error(f"❌ Media index not found: {INDEX_PATH}")
    exit(1)

logger.info(f"📂 Loading media metadata from: {INDEX_PATH}")

try:
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        media_records = json.load(f)

    for record in media_records:
        cursor.execute("""
            INSERT INTO raw.telegram_media (
                channel_name,
                message_id,
                image_filename,
                image_path,
                scraped_at
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            record["channel_name"],
            record["message_id"],
            record["image_filename"],
            record["image_path"],
            scraped_at
        ))

    logger.info(f"✅ Inserted {len(media_records)} media records into raw.telegram_media.")

except Exception as e:
    logger.error(f"❌ Error during media index load: {e}", exc_info=True)

# ✅ Finalize
conn.commit()
cursor.close()
conn.close()
logger.info("🎉 Media metadata successfully loaded.")