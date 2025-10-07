import os
import pandas as pd
from data.export_to_csv import export_to_csv
from app import db

def test_export_to_csv(tmp_path):
    test_db = tmp_path / "test.db"
    test_csv = tmp_path / "out.csv"

    os.environ["DB_PATH"] = str(test_db)
    os.environ["EXPORT_PATH"] = str(test_csv)

    db.create_table()
    db.insert_price("Item1", "15", "USD", "Test", "2025-01-01")

    export_to_csv()

    assert os.path.exists(test_csv), "CSV file was not created"
    df = pd.read_csv(test_csv)
    assert not df.empty, "CSV file is empty"
