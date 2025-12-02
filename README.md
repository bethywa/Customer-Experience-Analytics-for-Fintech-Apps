✅ Task 1 — Data Collection & Preprocessing
1. Scraping Google Play Reviews

Using google-play-scraper, the project extracts 500+ reviews per bank.

Script:

src/scraper.py


Output files:

data/raw/reviews_raw.csv — combined raw reviews

data/raw/app_info.csv — app metadata (title, ratings, installs, etc.)

2. Preprocessing Steps

Script:

src/preprocessing.py


Operations performed:

Remove duplicate reviews

Remove Amharic/Ethiopic script (keep only English text)

Drop rows missing essential fields (review_text, rating, bank_name)

Normalize dates → YYYY-MM-DD

Clean whitespace and text noise

Compute text length

Validate rating values

Output:

data/processed/reviews_processed.csv (clean dataset for analysis)

3. Exploratory Data Analysis (EDA)

Notebook:

notebooks/preprocessing_eda.ipynb


Visualizations include:

Rating distribution

Number of reviews per bank

Review text-length distribution

✅ Task 2 — Sentiment & Thematic Analysis
1. Sentiment Analysis (VADER)

Using VADER:

Calculates sentiment_score (−1 → +1)

Assigns sentiment_label: positive, neutral, negative

Output:

data/sentiment/sentiment_results.csv

Notebook:

notebooks/sentiment_analysis.ipynb


Visualizations:

Sentiment distribution per bank (violin/box plots)

Positive/Negative proportions

2. Theme Extraction

Approach uses:

✔ TF-IDF keyword extraction per bank
✔ LDA topic modeling (4 topics)
✔ Wordclouds per bank
✔ Manual grouping of keywords into themes

Output files:

data/themes/tfidf_keywords.csv

data/themes/lda_topics.csv

data/themes/themes_by_bank.csv

Notebook:

notebooks/theme_extraction.ipynb


Themes identified include examples like:

UX & Interface Issues

Transaction & Payment Problems

Performance & Reliability

Customer Support

Account Access Issues

📁 Project Structure
Customer-Experience-Analytics-for-Fintech-Apps/
│
├── src/
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── sentiment.py (optional)
│   └── theme_extraction.py (optional)
│
├── data/
│   ├── raw/
│   │   ├── reviews_raw.csv
│   │   └── app_info.csv
│   ├── processed/
│   │   └── reviews_processed.csv
│   ├── sentiment/
│   │   └── sentiment_results.csv
│   └── themes/
│       ├── tfidf_keywords.csv
│       ├── lda_topics.csv
│       └── themes_by_bank.csv
│
├── notebooks/
│   ├── preprocessing_eda.ipynb
│   ├── sentiment_analysis.ipynb
│   └── theme_extraction.ipynb
│
├── requirements.txt
├── .env                  (NOT uploaded / in .gitignore)
└── README.md

🚀 How to Run
1. Install dependencies
pip install -r requirements.txt

2. Add .env file (example)
CBE_APP_ID=com.combanketh.mobilebanking
BOA_APP_ID=com.boa.boaMobileBanking
DASHEN_APP_ID=com.dashen.dashensuperapp
REVIEWS_PER_BANK=500
MAX_RETRIES=3

3. Scrape reviews
python src/scraper.py

4. Preprocess reviews
python src/preprocessing.py

5. Run notebooks

Start Jupyter:

jupyter notebook


Then open the notebooks under notebooks/.

⭐ Key Achievements

✔ Successfully collected >1500 authentic Google Play reviews
✔ Clean and structured dataset prepared for NLP analysis
✔ Sentiment scoring using VADER
✔ Theme extraction using TF-IDF + LDA topic modeling
✔ Professional EDA and NLP visualizations