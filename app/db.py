import os
import sqlite3

# Default DB path (Termux + GitHub safe)
DB_PATH = os.getenv("DB_PATH", os.path.join("app", "prices.db"))

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY,
            product TEXT,
            price TEXT,
            currency TEXT,
            source TEXT,
            date TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_price(product, price, currency, source, date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO prices (product, price, currency, source, date) VALUES (?, ?, ?, ?, ?)",
        (product, price, currency, source, date)
    )
    conn.commit()
    conn.close()

def init_db():
    create_table()
    return get_connection()
