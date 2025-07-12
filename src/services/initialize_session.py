import os
import sys
from telethon import TelegramClient

sys.path.append(os.path.abspath("../../"))
from config.config import load_credentials


# Load API credentials from your .env file
creds = load_credentials('../../.env')  # Adjust path if needed
api_id = creds['api_id']
api_hash = creds['api_hash']
phone = creds['phone']

# Initialize the client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start(phone=phone)
    print("✅ Telegram session authenticated and saved as 'scraping_session.session'.")
 
with client:
    client.loop.run_until_complete(main())