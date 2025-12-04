from sqlalchemy import text
from db import engine

def show(query, title):
    print(f"\n=== {title} ===")
    with engine.connect() as conn:
        rows = conn.execute(text(query)).mappings().all()
        for r in rows:
            print(dict(r))

show("SELECT COUNT(*) AS total_reviews FROM reviews;", "Total Reviews")

show("""
    SELECT b.bank_name, COUNT(*) AS total_reviews
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    GROUP BY b.bank_name;
""", "Reviews Per Bank")

show("""
    SELECT b.bank_name, AVG(r.rating) AS avg_rating
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    GROUP BY b.bank_name;
""", "Average Rating Per Bank")

show("""
    SELECT sentiment_label, COUNT(*) AS count
    FROM reviews
    GROUP BY sentiment_label;
""", "Sentiment Distribution")
