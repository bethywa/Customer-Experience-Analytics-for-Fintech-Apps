-- schema.sql

DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS banks CASCADE;

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name TEXT NOT NULL,
    bank_code TEXT UNIQUE NOT NULL
);

CREATE TABLE reviews (
    review_id TEXT PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    sentiment_label TEXT,
    sentiment_score FLOAT,
    source TEXT
);
