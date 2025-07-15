from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os
import sys 

sys.path.append(os.path.abspath("../"))
from config.config import load_db_credentials

# Initialize the loading dtabase credentials
creds = load_db_credentials("../.env")

# Load environment variables
load_dotenv("../.env")  # Adjust path if needed based on your repo structure

# Read credentials
DB_NAME = creds["db_name"]
DB_USER = creds["db_user"]
DB_PASSWORD = creds["db_password"]
DB_HOST = creds["db_host"]
DB_PORT = creds["db_port"]

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine — this is your persistent connection interface
engine: Engine = create_engine(DATABASE_URL)

# Build a session factory — for safe, per-request connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI route injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()