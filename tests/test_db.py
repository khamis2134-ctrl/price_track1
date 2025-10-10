# tests/test_db.py
from app.db import init_db, insert_price, fetch_prices
import random

def test_init_and_insert():
    init_db()
    insert_price("TEST_ITEM_"+str(random.randint(1,99999)), 12.34, "USD", source="test")
    rows = fetch_prices(limit=5)
    assert isinstance(rows, list)
