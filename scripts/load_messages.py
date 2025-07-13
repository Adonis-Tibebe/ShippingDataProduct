import os
import sys
import json
import logging
from datetime import datetime
import psycopg2

sys.path.append(os.path.abspath("../"))
from config.config import load_db_credentials

# ✅ Configure logging
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

# ✅ Locate JSON files
BASE_PATH = "../data/raw/telegram_messages"
if not os.path.exists(BASE_PATH):
    logger.error(f"❌ Folder not found: {BASE_PATH}")
    exit(1)

# ✅ Iterate over dated directories
for date_folder in os.listdir(BASE_PATH):
    folder_path = os.path.join(BASE_PATH, date_folder)
    if not os.path.isdir(folder_path):
        continue

    # Use folder name as scraped_at timestamp
    try:
        scraped_at = datetime.strptime(date_folder, "%Y-%m-%d")
    except ValueError:
        logger.warning(f"⚠️ Skipping folder '{date_folder}' (invalid date format)")
        continue

    logger.info(f"📂 Loading messages from: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            channel_name = filename.replace(".json", "")
            file_path = os.path.join(folder_path, filename)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = json.load(f)

                for msg in messages:
                    message_id = msg.get("id")
                    cursor.execute("""
                        INSERT INTO raw.telegram_messages (channel_name, scraped_at, message_id, raw_data)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        channel_name,
                        scraped_at,
                        message_id,
                        json.dumps(msg)
                    ))

                logger.info(f"✅ Loaded {len(messages)} messages from {channel_name}")

            except Exception as e:
                logger.error(f"❌ Error loading {file_path}: {e}", exc_info=True)

# ✅ Finalize
conn.commit()
cursor.close()
conn.close()
logger.info("🎉 All messages loaded successfully.") 