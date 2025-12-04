"""
Configuration file for Customer Experience Analytics for Fintech Apps
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Play Store App IDs (Ethiopian banks)
APP_IDS = {
    "CBE": os.getenv("CBE_APP_ID", "com.combanketh.mobilebanking"),
    "BOA": os.getenv("BOA_APP_ID", "com.boa.boaMobileBanking"),
    "Dashen": os.getenv("DASHEN_APP_ID", "com.dashen.dashensuperapp"),
}

# Bank Names Mapping
BANK_NAMES = {
    "CBE": "Commercial Bank of Ethiopia",
    "BOA": "Bank of Abyssinia",
    "Dashen": "Dashen Bank"
}

# Scraping Configuration
SCRAPING_CONFIG = {
    "reviews_per_bank": int(os.getenv("REVIEWS_PER_BANK", 500)),
    "max_retries": int(os.getenv("MAX_RETRIES", 3)),
    "lang": "en",
    "country": "et"    # Ethiopia
}

# File Paths
DATA_PATHS = {
    "raw": "data/raw",
    "processed": "data/processed",
    "raw_reviews": "data/raw/reviews_raw.csv",
    "processed_reviews": "data/processed/reviews_processed.csv",
    "sentiment_results": "data/processed/reviews_with_sentiment.csv",
    "final_results": "data/processed/reviews_final.csv",
}



class Settings:

    # PostgreSQL credentials
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # Data paths
    PROCESSED_CSV = os.getenv("PROCESSED_CSV", "data/sentiment/sentiment_results.csv")

settings = Settings()

