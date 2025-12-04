✅ Task 1 — Data Collection & Preprocessing
1. Scraping Google Play Reviews

 - Using google-play-scraper, the project extracts 500+ reviews per bank.

 - Script:

 - src/scraper.py


Output files:

  - data/raw/reviews_raw.csv — combined raw reviews

  - data/raw/app_info.csv — app metadata (title, ratings, installs, etc.)

2. Preprocessing Steps

 src/preprocessing.py
 
 - Operations performed:

 - Remove duplicate reviews

 - Remove Amharic/Ethiopic script (keep only English text)

 - Drop rows missing essential fields (review_text, rating, bank_name)

 - Normalize dates → YYYY-MM-DD

 - Clean whitespace and text noise

 - Compute text length

-  Validate rating values

Output:

 - data/processed/reviews_processed.csv (clean dataset for analysis)

3. Exploratory Data Analysis (EDA)

 Notebook:

 - notebooks/preprocessing_eda.ipynb


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


🚀 How to Run
1. Install dependencies
   pip install -r requirements.txt

3. Scrape reviews
   python src/scraper.py

4. Preprocess reviews
    python src/preprocessing.py

5. Run notebooks

  Start Jupyter:


⭐ Key Achievements

✔ Successfully collected >1500 authentic Google Play reviews
✔ Clean and structured dataset prepared for NLP analysis
✔ Sentiment scoring using VADER
✔ Theme extraction using TF-IDF + LDA topic modeling
✔ Professional EDA and NLP visualizations


   🧩 Task 3 — PostgreSQL Database Integration

This task focuses on storing the cleaned and processed app review data into a PostgreSQL relational database, simulating real-world data engineering workflows.

📌 Objectives

    Install and configure PostgreSQL locally
 
    Create a relational schema for banks and reviews

    Insert processed dataset (1,463 reviews) into the database

    Run basic SQL queries to validate data
 
    Connect to PostgreSQL using SQLAlchemy

    Explore the stored data in a Jupyter Notebook


🛠 Steps Performed
1️⃣ Install PostgreSQL

    Installed PostgreSQL 18 and set up:

    Default superuser: postgres

    New application user: review_user

    Database: bank_reviews

    Added PostgreSQL /bin folder to PATH so psql works in terminal.

2️⃣ Create Database Schema

    Executed the schema using:

     psql -U postgres -d bank_reviews -f src/schema.sql


Created two tables:

    banks

    reviews

3️⃣ Insert Cleaned Data

     Inserted 1,463 cleaned and sentiment-scored reviews:

    python src/insert_reviews.py


Automatically:

    - Inserted unique banks

    - Linked reviews → banks via foreign key

    - Stored sentiment labels & sentiment scores

4️⃣ Run Verification Queries

     . python src/verify_queries.py



5️⃣ Explore in Notebook

 Notebook: notebooks/db_setup.ipynb

Includes:
✔ Connect to DB
✔ Load reviews into pandas
✔ Visualize sentiment distribution
✔ Ratings distribution
✔ Reviews per bank
✔ Reviews over time
✔ Top negative reviews

✅ Task 4 — Insights & Recommendations

 Goal: Identify drivers, pain points, and improvement opportunities.
What was done:

    Visualized sentiment trends, rating distributions, keyword clouds

    Identified key findings per bank

    Extracted top negative examples for evidence

    Generated actionable recommendations per bank

    Saved visuals to outputs/figures/ and tables to outputs/tables/
  

  📂 Customer-Experience-Analytics-for-Fintech-Apps
│
├── 📁 data
│   ├── 📁 raw
│   ├── 📁 processed
│   └── 📁 sentiment
│
├── 📁 outputs
│   ├── 🖼️ figures
│   └── 📊 tables
│
├── 📓 notebooks
│
├── 📁 reports
│
├── 📁 scripts
│
├── 📁 src
│
├── ⚙️ .env
├── 📄 requirements.txt
└── 📘 README.md

