import unittest
import json
from logic import analyse_orders


class TestOrdersProcessing(unittest.TestCase):

    def test_basic_aggregation(self):
        data = [
            {"id": "a1", "marketplace": "amazon", "amount_cents": 1000, "created_at": "2024-11-01T10:00:00Z"},
            {"id": "a2", "marketplace": "ebay",   "amount_cents": 500,  "created_at": "2024-11-01T11:00:00Z"},
        ]

        stats, suspects = analyse_orders(iter(data))

        print("\n--- TEST BASIC AGGREGATION ---")
        print(json.dumps(stats, indent=2))
        print("Suspects:", suspects)

        self.assertEqual(stats["revenue_total_eur"], 15.0)
        self.assertEqual(len(suspects), 0)

    def test_with_display(self):
        data = [
            {"id": "o1", "marketplace": "amazon", "amount_cents": 2599, "created_at": "2024-11-01T10:15:00Z"},
            {"id": "o2", "marketplace": "cdiscount", "amount_cents": 1299, "created_at": "2024-11-01T10:20:00Z"},
            {"id": "o3", "marketplace": "amazon", "amount_cents": -500, "created_at": "2024-11-01T10:30:00Z"},
        ]

        stats, suspects = analyse_orders(iter(data))

        print("\n--- TEST WITH DISPLAY ---")
        print(json.dumps({
            "stats": stats,
            "suspects": suspects
        }, indent=2, ensure_ascii=False))

        self.assertEqual(stats["revenue_total_eur"], 38.98)
        self.assertEqual(len(suspects), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
