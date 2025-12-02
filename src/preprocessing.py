"""
Data Preprocessing Script
Task 1: Data Preprocessing

This script cleans and preprocesses the scraped reviews data.
- Handles missing values
- Normalizes dates
- Cleans text data
- Removes duplicates
- Removes Amharic text
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from datetime import datetime
import re

from config import DATA_PATHS


class ReviewPreprocessor:
    """Preprocessor class for review data"""

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path or DATA_PATHS['raw_reviews']
        self.output_path = output_path or DATA_PATHS['processed_reviews']
        self.df = None
        self.stats = {}

    def load_data(self):
        print("Loading raw data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews")
            self.stats['original_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"ERROR loading file: {e}")
            return False

    # -----------------------------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------------------------
    def remove_duplicates(self):
        print("\n[0/5] Removing duplicate reviews...")

        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=['review_id', 'review_text'])
        removed = before - len(self.df)

        print(f"Removed {removed} duplicate rows")
        self.stats['duplicates_removed'] = removed

    # -----------------------------------------------------------
    # REMOVE AMHARIC TEXT
    # -----------------------------------------------------------
    def remove_amharic_text(self):
        print("\n[1/5] Removing Amharic/Ethiopic text...")

        amharic_pattern = re.compile(r"[\u1200-\u137F]+")

        def clean_amharic(text):
            if isinstance(text, str):
                return amharic_pattern.sub("", text)
            return text

        self.df['review_text'] = self.df['review_text'].apply(clean_amharic)
        print("Amharic text removed")

    # -----------------------------------------------------------
    # MISSING VALUE CHECK
    # -----------------------------------------------------------
    def check_missing_data(self):
        print("\n[2/5] Checking for missing data...")

        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100

        print("\nMissing values:")
        for col in missing.index:
            if missing[col] > 0:
                print(f"  {col}: {missing[col]} ({missing_pct[col]:.2f}%)")

        critical_cols = ['review_text', 'rating', 'bank_name']
        missing_critical = self.df[critical_cols].isnull().sum()

        if missing_critical.sum() > 0:
            print("\nWARNING: Missing values in critical columns:")
            print(missing_critical[missing_critical > 0])

    # -----------------------------------------------------------
    # HANDLE MISSING VALUES
    # -----------------------------------------------------------
    def handle_missing_values(self):
        print("\n[3/5] Handling missing values...")

        critical_cols = ['review_text', 'rating', 'bank_name']
        before_count = len(self.df)

        # Remove rows missing critical info
        self.df = self.df.dropna(subset=critical_cols)
        removed = before_count - len(self.df)

        if removed > 0:
            print(f"Removed {removed} rows with missing critical values")

        # Fill non-critical columns
        if 'user_name' in self.df.columns:
            self.df['user_name'] = self.df['user_name'].fillna('Anonymous')

        if 'thumbs_up' in self.df.columns:
            self.df['thumbs_up'] = self.df['thumbs_up'].fillna(0)

        self.stats['rows_removed_missing'] = removed
        self.stats['count_after_missing'] = len(self.df)

    # -----------------------------------------------------------
    # NORMALIZE DATE
    # -----------------------------------------------------------
    def normalize_dates(self):
        print("\n[4/5] Normalizing dates...")

        try:
            self.df['review_date'] = pd.to_datetime(self.df['review_date'])
            self.df['review_date'] = self.df['review_date'].dt.strftime('%Y-%m-%d')

            print(f"Date range: {self.df['review_date'].min()} to {self.df['review_date'].max()}")

        except Exception as e:
            print(f"WARNING: Error normalizing dates: {e}")

    # -----------------------------------------------------------
    # CLEAN REVIEW TEXT
    # -----------------------------------------------------------
    def clean_text(self):
        print("\n[5/5] Cleaning review text...")

        def clean_review_text(text):
            if pd.isna(text) or text == '':
                return ''
            text = str(text)
            text = re.sub(r'\s+', ' ', text)
            return text.strip()

        before_count = len(self.df)

        self.df['review_text'] = self.df['review_text'].apply(clean_review_text)
        self.df = self.df[self.df['review_text'].str.len() > 0]

        removed = before_count - len(self.df)

        if removed > 0:
            print(f"Removed {removed} empty reviews")

        # Add text length
        self.df['text_length'] = self.df['review_text'].str.len()

        self.stats['empty_reviews_removed'] = removed

    # -----------------------------------------------------------
    # FINAL CLEAN OUTPUT
    # -----------------------------------------------------------
    def prepare_final_output(self):
        print("\nPreparing final dataset...")

        output_columns = [
            'review_id', 'review_text', 'rating', 'review_date',
            'bank_code', 'bank_name',
            'user_name', 'thumbs_up',
            'text_length', 'source'
        ]

        # Keep only columns that exist
        output_columns = [c for c in output_columns if c in self.df.columns]

        self.df = self.df[output_columns]
        self.df = self.df.sort_values(['bank_code', 'review_date'], ascending=[True, False])
        self.df = self.df.reset_index(drop=True)

        print(f"Final dataset: {len(self.df)} reviews")

    # -----------------------------------------------------------
    # SAVE OUTPUT
    # -----------------------------------------------------------
    def save_data(self):
        print("\nSaving processed data...")

        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            self.df.to_csv(self.output_path, index=False)
            print(f"Data saved to: {self.output_path}")
            self.stats['final_count'] = len(self.df)
            return True
        except Exception as e:
            print(f"ERROR saving file: {e}")
            return False

    # -----------------------------------------------------------
    # REPORT
    # -----------------------------------------------------------
    def generate_report(self):
        print("\n" + "=" * 60)
        print("PREPROCESSING REPORT")
        print("=" * 60)

        print(f"\nOriginal: {self.stats.get('original_count', 0)}")
        print(f"Duplicates removed: {self.stats.get('duplicates_removed', 0)}")
        print(f"Rows missing removed: {self.stats.get('rows_removed_missing', 0)}")
        print(f"Empty removed: {self.stats.get('empty_reviews_removed', 0)}")
        print(f"Final cleaned count: {self.stats.get('final_count', 0)}")

    # -----------------------------------------------------------
    # MASTER PROCESS
    # -----------------------------------------------------------
    def process(self):
        print("=" * 60)
        print("STARTING DATA PREPROCESSING")
        print("=" * 60)

        if not self.load_data():
            return False

        self.remove_duplicates()
        self.remove_amharic_text()
        self.check_missing_data()
        self.handle_missing_values()
        self.normalize_dates()
        self.clean_text()
        self.prepare_final_output()

        if self.save_data():
            self.generate_report()
            print("\n✓ Preprocessing completed successfully!")
            return True

        print("\n✗ Preprocessing failed!")
        return False


def main():
    processor = ReviewPreprocessor()
    processor.process()


if __name__ == "__main__":
    main()
