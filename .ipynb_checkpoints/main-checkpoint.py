from app.price_tracker import add_price, get_prices
from app.utils import format_currency, find_item

def main():
    print("📊 Price Tracker Running...")

    # Add example data
    add_price("Apple", 1.5)
    add_price("Banana", 0.9)

    # Show prices
    data = get_prices()
    for row in data:
        print(f"{row['item']}: {format_currency(row['price'])}")

    # Find an item
    item = find_item(data, "apple")
    if item:
        print("Found:", item)

if __name__ == "__main__":
    main()
