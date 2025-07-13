# Load the PostgreSQL credentials
import os 
import sys

sys.path.append(os.path.abspath("../"))
from config.config import load_db_credentials  # ✅ Function to load credentials
import psycopg2                                # ✅ Database driver

import logging                                 # ✅ Logging to track execution
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Step 1: Load DB credentials from .env
logger.info("🔑 Loading database credentials from .env...")
creds = load_db_credentials('../.env')

# Step 2: Establish connection with PostgreSQL using those credentials
logger.info(f"🔌 Connecting to PostgreSQL at {creds['db_host']}:{creds['db_port']}...")
conn = psycopg2.connect(
    dbname=creds['db_name'],
    user=creds['db_user'],
    password=creds['db_password'],
    host=creds['db_host'],
    port=creds['db_port']
)
logger.info("✅ Database connection established.")

# Step 3: Create a cursor — a control object used to execute SQL statements
cursor = conn.cursor()

# Step 4: Execute SQL to create schema and table
logger.info("🧱 Creating raw.telegram_messages table...")
cursor.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;

    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        channel_name TEXT,
        scraped_at TIMESTAMP,
        message_id INTEGER,
        raw_data JSONB,
        PRIMARY KEY (channel_name, message_id)
    );
""")
logger.info("✅ Table raw.telegram_messages created successfully.")


# ✅ Add media table for future enrichment (not used in task-2)
logger.info("🧱 Creating raw.telegram_media table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw.telegram_media (
        channel_name TEXT,
        message_id INTEGER,
        image_filename TEXT,
        image_path TEXT,
        scraped_at TIMESTAMP,
        PRIMARY KEY (channel_name, message_id)
    );
""")
logger.info("✅ Table raw.telegram_media created successfully.")

# Step 5: Finalize changes and release resources
conn.commit()
cursor.close()
conn.close()
logger.info("✅ Tables created and connection closed successfully.")