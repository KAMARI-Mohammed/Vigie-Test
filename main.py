import argparse
from logic import read_json_file, analyse_orders

def main():
    parser = argparse.ArgumentParser(description="Process and analyze order data from a JSON file.")
    parser.add_argument("file_path", type=str, help="Path to the JSON file containing order data.")
    parser.add_argument("--from_date", type=str, help="Optional date filter in YYYY-MM-DD format.", default=None)

    args = parser.parse_args()

    orders = read_json_file(args.file_path)
    stats, suspicious_orders = analyse_orders(orders, from_date=args.from_date)

    print("Suspicious Orders:")
    for order in suspicious_orders:
        print(order)

    print("\nRevenue by Marketplace:")
    for mp, revenue in stats['revenue_by_marketplace'].items():
        print(f" - {mp}: {revenue}")

    print()

    if suspicious_orders:
        print(f"Total suspicious orders: {len(suspicious_orders)}")
    for s in suspicious_orders:
        print(f" - Order ID: {s['order_id']}, Reason: {s['reason']}")
    else:
        print("No suspicious orders found.")

    
def test_with_display(self):
    data = [
        {"id": "o1", "marketplace": "amazon",    "country": "FR", "amount_cents": 2599, "created_at": "2024-11-01T10:15:00Z"},
        {"id": "o2", "marketplace": "cdiscount", "country": "FR", "amount_cents": 1299, "created_at": "2024-11-01T10:20:00Z"},
        {"id": "o3", "marketplace": "amazon",    "country": "DE", "amount_cents": -500, "created_at": "2024-11-01T10:30:00Z"},
        {"id": "o4", "marketplace": "",          "country": "FR", "amount_cents": 5000, "created_at": "2024-11-01T11:00:00Z"},
        {"id": "o5", "marketplace": "amazon",    "country": "FR", "amount_cents": 0,    "created_at": "2024-11-01T11:15:00Z"},
        {"id": "o6", "marketplace": "cdiscount", "country": "ES", "amount_cents": 3499, "created_at": "2024-11-01T11:30:00Z"},
        {"id": "o7", "marketplace": "ebay",      "country": "FR", "amount_cents": 799,  "created_at": "2024-11-01T11:45:00Z"},
        {"id": "o8", "marketplace": "amazon",    "country": "IT", "amount_cents": 1599, "created_at": "2024-11-01T12:00:00Z"},
    ]
    stats,suspicious_orders = analyse_orders(iter(data))
    print("Stats Orders:")
    print(json.dumps(stats, indent=2))
    print("Supicious Orders:")
    print(json.dumps(suspicious_orders, indent=2))



if __name__ == "__main__":
    main()