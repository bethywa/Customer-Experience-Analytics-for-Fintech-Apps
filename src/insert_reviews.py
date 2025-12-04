import pandas as pd
from sqlalchemy import text
from db import engine

CSV_PATH = "data/sentiment/sentiment_results.csv"

df = pd.read_csv(CSV_PATH)
print(f"Loaded {len(df)} reviews from {CSV_PATH}")

# Connect
with engine.begin() as conn:

    # -------------------------------------
    # 1. Insert banks
    # -------------------------------------
    print("\n➡ Inserting banks...")

    unique_banks = df[['bank_code', 'bank_name']].drop_duplicates()

    for _, row in unique_banks.iterrows():
        conn.execute(
            text("""
                INSERT INTO banks (bank_name, bank_code)
                VALUES (:bank_name, :bank_code)
                ON CONFLICT (bank_code) DO NOTHING;
            """),
            {"bank_name": row.bank_name, "bank_code": row.bank_code}
        )

    # -------------------
    # Retrieve bank_id map
    # -------------------
    bank_map = {
        code: id for code, id in conn.execute(
            text("SELECT bank_code, bank_id FROM banks")
        )
    }

    print("Bank ID map:", bank_map)

    # -------------------------------------
    # 2. Insert reviews
    # -------------------------------------
    print("\n➡ Inserting reviews...")

    for _, row in df.iterrows():
        conn.execute(
            text("""
                INSERT INTO reviews (
                    review_id, bank_id, review_text, rating,
                    review_date, sentiment_label, sentiment_score, source
                )
                VALUES (
                    :review_id, :bank_id, :review_text, :rating,
                    :review_date, :sentiment_label, :sentiment_score, :source
                )
                ON CONFLICT (review_id) DO NOTHING;
            """),
            {
                "review_id": row.review_id,
                "bank_id": bank_map[row.bank_code],
                "review_text": row.review_text,
                "rating": int(row.rating),
                "review_date": row.review_date,
                "sentiment_label": row.sentiment_label,
                "sentiment_score": float(row.sentiment_score),
                "source": row.source
            }
        )

print("\n✅ Done! All reviews inserted successfully.")
