from app.price_tracker import scrape_all

if __name__ == "__main__":
    print("🔍 Starting price tracker...")
    scrape_all()
    print("✅ All done! CSV ready in data/prices_export.csv")
