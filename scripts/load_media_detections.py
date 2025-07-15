import os
import sys
import json
import logging
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime

sys.path.append(os.path.abspath("../"))
from config.config import load_db_credentials

# 🧾 Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 🔐 Load DB credentials
logger.info(" Loading DB credentials...")
creds = load_db_credentials("../.env")

conn = psycopg2.connect(
    dbname=creds["db_name"],
    user=creds["db_user"],
    password=creds["db_password"],
    host=creds["db_host"],
    port=creds["db_port"]
)

# 🧱 Create table with surrogate key
def create_detection_table():
    with conn.cursor() as cur:
        logger.info("🧱 Creating raw.media_detections table if not exists...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.media_detections (
                detection_id SERIAL PRIMARY KEY,
                message_id INTEGER,
                channel_name TEXT,
                image_path TEXT,
                label TEXT,
                confidence NUMERIC
            );
        """)
    conn.commit()
    logger.info("✅ Table ready.")

# 📥 Load JSON and insert detections
def ingest_detections():
    input_path = "../data/processed/media_detection_results.json"

    if not os.path.isfile(input_path):
        logger.error(f"❌ File not found: {input_path}")
        return

    with open(input_path, 'r') as f:
        detection_data = json.load(f)

    logger.info(f"📂 Loaded {len(detection_data)} entries from detection JSON")

    with conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            inserted_count = 0

            for entry in detection_data:
                msg_id = entry["message_id"]
                channel = entry["channel_name"]
                image_path = entry["image_path"]
                detections = entry.get("detections", [])

                # Handle empty detections
                if not detections:
                    cur.execute("""
                        INSERT INTO raw.media_detections (
                            message_id, channel_name, image_path, label, confidence
                        ) VALUES (%s, %s, %s, %s, %s);
                    """, (msg_id, channel, image_path, "no_object_detected", None))
                    inserted_count += 1
                    continue

                # Insert each detection
                for d in detections:
                    label = d.get("label")
                    conf = d.get("confidence")
                    cur.execute("""
                        INSERT INTO raw.media_detections (
                            message_id, channel_name, image_path, label, confidence
                        ) VALUES (%s, %s, %s, %s, %s);
                    """, (msg_id, channel, image_path, label, conf))
                    inserted_count += 1

            logger.info(f"✅ Inserted {inserted_count} rows into raw.media_detections")

if __name__ == "__main__":
    create_detection_table()
    ingest_detections()