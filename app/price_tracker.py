import datetime
from app import db
from data.export_to_csv import export_to_csv

def scrape_example():
    # Simulate scraping 2 items
    db.insert_price("Example Product A", "12.99", "USD", "ExampleShop", str(datetime.date.today()))
    db.insert_price("Example Product B", "22.50", "USD", "ExampleShop", str(datetime.date.today()))
    print("✅ Scraped ExampleShop (2 items)")

def scrape_all():
    db.create_table()
    scrape_example()
    export_to_csv()

if __name__ == "__main__":
    scrape_all()
