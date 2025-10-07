from app import db
import os

def test_create_and_insert(tmp_path):
    test_db = tmp_path / "test.db"
    os.environ["DB_PATH"] = str(test_db)
    db.create_table()
    db.insert_price("Test", "10.0", "USD", "Site", "2025-01-01")
    rows = db.fetch_prices()
    assert len(rows) > 0

def test_cleanup(tmp_path):
    test_db = tmp_path / "test.db"
    os.environ["DB_PATH"] = str(test_db)
    db.create_table()
    db.insert_price("Old", "5", "USD", "Site", "2020-01-01")
    db.cleanup_old_data(days=1)
