"""
Google Play Store Review Scraper
Task 1: Data Collection

Scrapes 500+ reviews from Google Play Store for:
- CBE
- BOA
- Dashen
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_play_scraper import reviews, Sort, app
import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

from config import APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS


class PlayStoreScraper:
    """Scraper class for Google Play Store reviews"""

    def __init__(self):
        self.app_ids = APP_IDS
        self.bank_names = BANK_NAMES
        self.reviews_per_bank = SCRAPING_CONFIG["reviews_per_bank"]
        self.lang = SCRAPING_CONFIG["lang"]
        self.country = SCRAPING_CONFIG["country"]
        self.max_retries = SCRAPING_CONFIG["max_retries"]

    # ---------------------------------------------------------
    def get_app_info(self, app_id):
        """Fetch app summary info"""
        try:
            info = app(app_id, lang=self.lang, country=self.country)
            return {
                'app_id': app_id,
                "title": info.get("title", ""),
                "score": info.get("score", 0),
                "ratings": info.get("ratings", 0),
                "reviews": info.get("reviews", 0),
                "installs": info.get("installs", "N/A")
            }
        except Exception as e:
            print(f"Error fetching app info for {app_id}: {e}")
            return None

    # ---------------------------------------------------------
    def scrape_reviews(self, app_id):
        """Scrape reviews using google-play-scraper"""
        print(f"\nScraping reviews for {app_id}...")

        for attempt in range(self.max_retries):
            try:
                result, _ = reviews(
                    app_id,
                    lang=self.lang,
                    country=self.country,
                    sort=Sort.NEWEST,
                    count=self.reviews_per_bank,
                    filter_score_with=None
                )
                print(f"✓ Scraped {len(result)} reviews")
                return result
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(3)
                else:
                    print("❌ Failed after max retries.")
                    return []

    # ---------------------------------------------------------
    def process_reviews(self, raw_reviews, bank_code):
        """Clean & format scraped review dicts"""
        processed = []
        for r in raw_reviews:
            processed.append({
                "review_id": r.get("reviewId"),
                "review_text": r.get("content", ""),
                "rating": r.get("score"),
                "review_date": r.get("at", datetime.now()),
                "user_name": r.get("userName", ""),
                "thumbs_up": r.get("thumbsUpCount", 0),
                "bank_code": bank_code,
                "bank_name": self.bank_names[bank_code],
                "source": "Google Play"
            })
        return processed

    # ---------------------------------------------------------
    def scrape_all_banks(self):
        # Main method to scrape all banks

        all_reviews = []
        app_info_list = []

        print("=" * 60)
        print("Starting Google Play Review Scraper")
        print("=" * 60)

        for bank_code, app_id in tqdm(self.app_ids.items(), desc="Banks"):

            # Get app info
            info = self.get_app_info(app_id)
            if info:
                info["bank_code"] = bank_code
                info["bank_name"] = self.bank_names[bank_code]
                info['app_id'] = app_id 
                app_info_list.append(info)

            # Scrape reviews
            raw = self.scrape_reviews(app_id)
            processed = self.process_reviews(raw, bank_code)
            all_reviews.extend(processed)

            time.sleep(2)

        # Save review CSV
        os.makedirs(DATA_PATHS["raw"], exist_ok=True)
        df = pd.DataFrame(all_reviews)
        df.to_csv(DATA_PATHS["raw_reviews"], index=False)

        print("\n✓ Scraping complete!")
        print(f"Total reviews collected: {len(df)}")
        print(f"Saved to: {DATA_PATHS['raw_reviews']}")

        # Save app info CSV
        if app_info_list:
            app_info_df = pd.DataFrame(app_info_list)
            app_info_df.to_csv(f"{DATA_PATHS['raw']}/app_info.csv", index=False)
            print(f"\nApp information saved to {DATA_PATHS['raw']}/app_info.csv")

        return df


# ---------------------------------------------------------
def main():
    scraper = PlayStoreScraper()
    return scraper.scrape_all_banks()


if __name__ == "__main__":
    df = main()
