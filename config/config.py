import os
from dotenv import load_dotenv

def load_credentials(env_path='../.env'):
    load_dotenv(env_path)
    return {
        'api_id': os.getenv('TG_API_ID'),
        'api_hash': os.getenv('TG_API_HASH'),
        'phone': os.getenv('phone')
    }

def load_db_credentials(env_path='../.env'):
    load_dotenv(env_path)
    return {
        'db_name': os.getenv('POSTGRES_DB'),
        'db_user': os.getenv('POSTGRES_USER'),
        'db_password': os.getenv('POSTGRES_PASSWORD'),
        'db_host': os.getenv('DB_HOST', 'localhost'),
        'db_port': int(os.getenv('DB_PORT', 5431))
    }