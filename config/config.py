import os
from dotenv import load_dotenv

def load_credentials(env_path='../.env'):
    load_dotenv(env_path)
    return {
        'api_id': os.getenv('TG_API_ID'),
        'api_hash': os.getenv('TG_API_HASH'),
        'phone': os.getenv('phone')
    }