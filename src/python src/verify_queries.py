from db import engine
from sqlalchemy import text

def run_query(query):
    result = engine.execute(text(query))

    for row in result:
        print(row._mapping)   # <—— bulletproof way
    print("\n")


print("✔ Total reviews:")
run_query("SELECT COUNT(*) AS total_reviews FROM reviews;")

print("✔ Reviews per bank:")
run_query("""
    SELECT b.bank_name, COUNT(*) AS total_reviews
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    GROUP BY b.bank_name;
""")

print("✔ Average rating per bank:")
run_query("""
    SELECT b.bank_name, ROUND(AVG(r.rating), 2) AS avg_rating
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    GROUP BY b.bank_name;
""")

print("✔ Sentiment distribution:")
run_query("""
    SELECT sentiment_label, COUNT(*) AS count
    FROM reviews
    GROUP BY sentiment_label;
""")
