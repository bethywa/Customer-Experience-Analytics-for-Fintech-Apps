# src/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Read DB credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Encode password (important if it contains special characters)
encoded_password = quote_plus(DB_PASSWORD)

# Build database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{encoded_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # prevents "server closed the connection" errors
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Optional helper
def get_db():
    """FastAPI-style dependency (optional for scripts)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
