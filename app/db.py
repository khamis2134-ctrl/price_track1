# app/db.py
from pathlib import Path
import sqlite3
from contextlib import contextmanager
from app.config import DB_PATH, CLEAN_DIR

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    """Create DB and table if not exists, and create indexes."""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                item TEXT,
                price REAL,
                currency TEXT,
                extra JSON,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Indexes for faster queries
        c.execute("CREATE INDEX IF NOT EXISTS idx_item ON prices(item)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON prices(timestamp)")

def insert_price(item, price, currency="USD", source=None, extra=None):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO prices (source, item, price, currency, extra) VALUES (?, ?, ?, ?, ?)",
            (source, item, price, currency, json_or_none(extra))
        )

def bulk_insert(rows):
    """rows: iterable of tuples (source, item, price, currency, extra)"""
    with get_conn() as conn:
        c = conn.cursor()
        c.executemany(
            "INSERT INTO prices (source, item, price, currency, extra) VALUES (?, ?, ?, ?, ?)",
            [(r[0], r[1], r[2], r[3], json_or_none(r[4])) for r in rows]
        )

def fetch_prices(item=None, limit=100, since=None):
    q = "SELECT id, source, item, price, currency, extra, timestamp FROM prices"
    args = []
    if item:
        q += " WHERE item = ?"
        args.append(item)
    q += " ORDER BY timestamp DESC LIMIT ?"
    args.append(limit)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(q, args)
        return c.fetchall()

def json_or_none(obj):
    import json
    if obj is None:
        return None
    try:
        return json.dumps(obj)
    except Exception:
        return None
