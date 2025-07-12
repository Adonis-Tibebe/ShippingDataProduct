import os
import sys
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import Message

sys.path.append(os.path.abspath("../../"))
from config.config import load_credentials

# ✅ Helper function for parsing Datetime objects in messsage dictonary
def clean_message(obj):
    if isinstance(obj, dict):
        return {
            k: clean_message(v)
            for k, v in obj.items()
            if not isinstance(v, bytes) # Remove keys that are Binary data
        }
    elif isinstance(obj, list):
        return [clean_message(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()  # or str(obj)
    else:
        return obj

# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ✅ Load credentials from .env
creds = load_credentials('../../.env')
api_id = creds['api_id']
api_hash = creds['api_hash']
phone = creds['phone']

# ✅ Initialize Telegram client
client = TelegramClient('scraping_session', api_id, api_hash)

# ✅ Channel Lists
MESSAGE_CHANNELS = [
    '@CheMed123',
    '@lobelia4cosmetics',
    '@tikvahpharma',
    # Add more channels as needed
]

MEDIA_CHANNELS = [
    '@lobelia4cosmetics',
    '@CheMed123',
    '@tikvahpharma',
]

# ✅ Prepare paths
SCRAPE_DATE = datetime.now().strftime('%Y-%m-%d')
BASE_MESSAGE_PATH = f'../../data/raw/telegram_messages/{SCRAPE_DATE}'
BASE_MEDIA_PATH = '../../data/raw/telegram_media'

os.makedirs(BASE_MESSAGE_PATH, exist_ok=True)
os.makedirs(BASE_MEDIA_PATH, exist_ok=True)

# ✅ Scrape messages
async def scrape_messages():
    logger.info("Started Telegram client for message scraping.")

    for channel in MESSAGE_CHANNELS:
        logger.info(f"Scraping messages from channel: {channel}")
        try:
            messages = []
            entity = await client.get_entity(channel)
            async for msg in client.iter_messages(entity, limit=200):
                if isinstance(msg, Message):
                    messages.append(msg.to_dict())

            out_path = os.path.join(BASE_MESSAGE_PATH, f'{channel.strip("@")}.json')
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(clean_message(messages), f, ensure_ascii=False, indent=2)

            logger.info(f"✅ Saved {len(messages)} messages for {channel} to {out_path}")

        except Exception as e:
            logger.error(f"⚠️ Error scraping {channel}: {e}", exc_info=True)


# ✅ Scrape media
async def scrape_media():
    logger.info("Started Telegram client for media scraping.")

    media_metadata = []  # 🆕 New list to collect structured metadata

    for channel in MEDIA_CHANNELS:
        logger.info(f"Scraping images from channel: {channel}")
        try:
            entity = await client.get_entity(channel)
            count = 0
            async for msg in client.iter_messages(entity, limit=200):
                if msg.media and hasattr(msg.media, 'photo'):
                    filename = f'{channel.strip("@")}_{msg.id}.jpg'
                    save_path = os.path.join(BASE_MEDIA_PATH, filename)
                    await client.download_media(msg.media, save_path)
                    logger.info(f"📷 Saved image: {save_path}")
                    count += 1

                    # 🆕 Add structured metadata for each image
                    media_metadata.append({
                        "channel_name": channel.strip("@"),
                        "message_id": msg.id,
                        "image_filename": filename,
                        "image_path": save_path.replace("../../", ""),  # Optional: make relative
                        "scraped_at": datetime.now().isoformat()
                    })

            logger.info(f"✅ Finished saving {count} images for {channel}")

        except Exception as e:
            logger.error(f"⚠️ Error scraping images from {channel}: {e}", exc_info=True)

    # 🆕 Save media index JSON one directory above BASE_MEDIA_PATH
    media_index_path = os.path.join(os.path.dirname(BASE_MEDIA_PATH), f'media_index_{SCRAPE_DATE}.json')
    with open(media_index_path, 'w', encoding='utf-8') as f:
        json.dump(clean_message(media_metadata), f, ensure_ascii=False, indent=2)

    logger.info(f"🧩 Media index saved to: {media_index_path}")

# ✅ Run both scrapers
async def main():
    logger.info("Starting Telegram scraping pipeline...")
    await scrape_messages()
    await scrape_media()
    logger.info("✅ All scraping tasks completed.")

with client.start(phone=phone) as session:
    session.loop.run_until_complete(main())