import os
import sqlite3
import pandas as pd

def export_to_csv():
    DB_PATH = os.getenv("DB_PATH", os.path.join("app", "prices.db"))
    EXPORT_PATH = os.getenv("EXPORT_PATH", os.path.join("data", "prices_export.csv"))

    try:
        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)

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

        df = pd.read_sql_query("SELECT * FROM prices", conn)
        df.to_csv(EXPORT_PATH, index=False)
        print(f"✅ Exported data to {EXPORT_PATH}")

    except Exception as e:
        print(f"❌ Export failed: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    export_to_csv()
