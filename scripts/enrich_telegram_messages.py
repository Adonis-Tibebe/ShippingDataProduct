import os
import sys
import json
import logging
import psycopg2
from psycopg2.extras import DictCursor

# 🧠 Import your extractors
sys.path.append(os.path.abspath("../"))  # Adjust path as needed
from config.config import load_db_credentials
from src.utils.Extractors import (
    extract_price,
    extract_health_flag,
    extract_channel_products
)

# ✅ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 🔌 Load DB credentials and connect
logger.info("🔑 Loading DB credentials...")
creds = load_db_credentials("../.env")
conn = psycopg2.connect(
    dbname=creds["db_name"],
    user=creds["db_user"],
    password=creds["db_password"],
    host=creds["db_host"],
    port=creds["db_port"]
)

def create_enriched_table():
    with conn.cursor() as cur:
        logger.info("🧱 Creating raw.telegram_enriched table if it doesn't exist...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.telegram_enriched (
                channel_name TEXT,
                message_id INTEGER,
                product_names TEXT,
                main_price NUMERIC,
                is_health_related BOOLEAN,
                PRIMARY KEY (channel_name, message_id)
            );
        """)
    conn.commit()
    logger.info("✅ Table created.")

def enrich_messages():
    with conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            logger.info("🔍 Fetching raw messages...")
            cur.execute("""
                SELECT channel_name, message_id, raw_data->>'message' AS message_text
                FROM raw.telegram_messages
            """)
            rows = cur.fetchall()
            logger.info(f"🔧 Processing {len(rows)} messages...")

            for row in rows:
                channel = row["channel_name"]
                msg_id = row["message_id"]
                text = row["message_text"]

                # 🧪 Run extractors
                price_list = extract_price(text)
                product_list = extract_channel_products(text, channel)
                health_flag = extract_health_flag(text)

                # 🧼 Normalize values
                main_price = price_list[0] if price_list and product_list else None
                product_str = " | ".join(product_list) if product_list else None

                # 📥 Insert enriched data
                cur.execute("""
                    INSERT INTO raw.telegram_enriched (
                        channel_name,
                        message_id,
                        product_names,
                        main_price,
                        is_health_related
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (channel_name, message_id) DO UPDATE SET
                        product_names = EXCLUDED.product_names,
                        main_price = EXCLUDED.main_price,
                        is_health_related = EXCLUDED.is_health_related;
                """, (
                    channel, msg_id, product_str, main_price, health_flag
                ))

            logger.info("✅ All messages enriched and loaded.")
            conn.commit()

if __name__ == "__main__":
    create_enriched_table()
    enrich_messages()