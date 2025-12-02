"""
Theme Extraction Script (TF-IDF + LDA Topic Modeling)
Task 2: Thematic Analysis

This script:
- Loads sentiment-scored reviews
- Extracts keywords using TF-IDF
- Performs LDA topic modeling (4 topics per bank)
- Assigns rule-based themes
- Saves results to data/themes/
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from config import DATA_PATHS


class ThemeExtractor:
    def __init__(self):
        self.input_path = "data/sentiment/sentiment_results.csv"
        self.output_path = "data/themes/themes_by_bank.csv"
        self.lda_output_path = "data/themes/lda_topics_by_bank.csv"
        self.df = None

    # -----------------------------------------------------------
    def load_data(self):
        print("Loading sentiment-scored data...")
        try:
            self.df = pd.read_csv(self.input_path)
            print(f"Loaded {len(self.df)} rows.")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    # -----------------------------------------------------------
    def extract_keywords_tfidf(self):
        print("\nExtracting keywords using TF-IDF...")

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=50,
            ngram_range=(1, 2)
        )

        keywords_per_bank = []

        for bank in self.df["bank_code"].unique():
            bank_df = self.df[self.df["bank_code"] == bank]

            tfidf_matrix = vectorizer.fit_transform(bank_df["review_text"])
            features = vectorizer.get_feature_names_out()

            keywords_per_bank.append({
                "bank_code": bank,
                "bank_name": bank_df["bank_name"].iloc[0],
                "keywords": ", ".join(features)
            })

        self.keywords_df = pd.DataFrame(keywords_per_bank)
        print("✓ TF-IDF extraction complete.")

    # -----------------------------------------------------------
    def lda_topic_modeling(self, num_topics=4, top_words=8):
        print("\nPerforming LDA Topic Modeling (4 topics per bank)...")

        lda_results = []

        for bank in self.df["bank_code"].unique():
            bank_df = self.df[self.df["bank_code"] == bank]

            # Convert to bow (bag of words)
            count_vectorizer = CountVectorizer(stop_words="english")
            bow_matrix = count_vectorizer.fit_transform(bank_df["review_text"])
            feature_names = count_vectorizer.get_feature_names_out()

            # Run LDA
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                random_state=42,
                learning_method="batch"
            )
            lda.fit(bow_matrix)

            # Extract top words for each topic
            for i, topic in enumerate(lda.components_):
                top_indices = topic.argsort()[-top_words:]
                topic_words = [feature_names[idx] for idx in reversed(top_indices)]

                lda_results.append({
                    "bank_code": bank,
                    "bank_name": bank_df["bank_name"].iloc[0],
                    "topic_number": i + 1,
                    "topic_keywords": ", ".join(topic_words)
                })

        self.lda_df = pd.DataFrame(lda_results)
        print("✓ LDA Topic Modeling complete.")

    # -----------------------------------------------------------
    def assign_themes(self):
        print("\nAssigning rule-based themes...")

        def map_themes(keyword_string):
            words = keyword_string.lower()

            themes = []

            if any(k in words for k in ["login", "password", "account", "access", "verification"]):
                themes.append("Account Access Issues")

            if any(k in words for k in ["slow", "loading", "crash", "error", "fail", "not working"]):
                themes.append("Performance & Reliability")

            if any(k in words for k in ["ui", "interface", "design", "easy", "navigation"]):
                themes.append("User Interface & Experience")

            if any(k in words for k in ["support", "service", "help", "call"]):
                themes.append("Customer Support")

            if any(k in words for k in ["transfer", "transaction", "payment", "balance"]):
                themes.append("Transactions & Payments")

            if not themes:
                themes.append("General Feedback")

            return ", ".join(themes)

        self.keywords_df["themes"] = self.keywords_df["keywords"].apply(map_themes)

    # -----------------------------------------------------------
    def save_results(self):
        os.makedirs("data/themes", exist_ok=True)

        self.keywords_df.to_csv(self.output_path, index=False)
        self.lda_df.to_csv(self.lda_output_path, index=False)

        print(f"\nTF-IDF themes saved to → {self.output_path}")
        print(f"LDA topics saved to   → {self.lda_output_path}")

    # -----------------------------------------------------------
    def process(self):
        if not self.load_data():
            return

        self.extract_keywords_tfidf()
        self.lda_topic_modeling(num_topics=4)
        self.assign_themes()
        self.save_results()

        print("\n✓ THEME EXTRACTION COMPLETED\n")


def main():
    extractor = ThemeExtractor()
    extractor.process()


if __name__ == "__main__":
    main()
