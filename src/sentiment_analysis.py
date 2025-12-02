"""
Sentiment Analysis using VADER
Task 2: Sentiment Scoring

This script:
- Loads processed reviews
- Applies VADER sentiment scoring
- Generates sentiment label (positive/neutral/negative)
- Saves results to data/sentiment/sentiment_results.csv
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from config import DATA_PATHS
import nltk

# download vader lexicon if not installed
nltk.download('vader_lexicon')


class SentimentAnalyzer:
    def __init__(self):
        self.input_path = DATA_PATHS["processed_reviews"]
        self.output_path = "data/sentiment/sentiment_results.csv"
        self.df = None
        self.analyzer = SentimentIntensityAnalyzer()

    def load_data(self):
        print("Loading processed reviews...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} reviews.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def apply_vader(self):
        print("Applying VADER sentiment analysis...")

        def analyze(text):
            scores = self.analyzer.polarity_scores(text)
            compound = scores["compound"]

            if compound >= 0.05:
                label = "positive"
            elif compound <= -0.05:
                label = "negative"
            else:
                label = "neutral"

            return pd.Series([compound, label])

        self.df[["sentiment_score", "sentiment_label"]] = self.df["review_text"].apply(analyze)
        print("Sentiment scoring complete.")

    def save_results(self):
        os.makedirs("data/sentiment", exist_ok=True)
        self.df.to_csv(self.output_path, index=False)
        print(f"Sentiment results saved to {self.output_path}")

    def process(self):
        if not self.load_data():
            return

        self.apply_vader()
        self.save_results()
        print("✓ Sentiment analysis completed.")


def main():
    analyzer = SentimentAnalyzer()
    analyzer.process()


if __name__ == "__main__":
    main()
