"""
CommerceIQ — Automated Data Quality & Integrity Test Suite
Compatible with pytest and standard unittest runner.
"""

import os
import sqlite3
import unittest

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "olist_oltp.db"))

class TestCommerceIQDataQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_database_tables_exist(self):
        """Ensure all 9 core normalized tables are present."""
        expected_tables = {
            "customers", "sellers", "product_categories", "geolocation",
            "products", "orders", "order_items", "order_payments", "order_reviews"
        }
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in self.cur.fetchall()}
        for t in expected_tables:
            self.assertIn(t, tables, f"Missing expected table: {t}")

    def test_no_orphan_order_items(self):
        """Verify referential integrity between order_items and orders."""
        query = """
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL;
        """
        self.cur.execute(query)
        orphans = self.cur.fetchone()[0]
        self.assertEqual(orphans, 0, "Found orphan order_items without parent orders!")

    def test_no_negative_prices(self):
        """Verify that price and freight_value are non-negative."""
        query = "SELECT COUNT(*) FROM order_items WHERE price < 0 OR freight_value < 0;"
        self.cur.execute(query)
        violations = self.cur.fetchone()[0]
        self.assertEqual(violations, 0, "Found negative prices or freight values!")

    def test_review_score_domain(self):
        """Verify review scores are strictly between 1 and 5."""
        query = "SELECT COUNT(*) FROM order_reviews WHERE review_score < 1 OR review_score > 5;"
        self.cur.execute(query)
        violations = self.cur.fetchone()[0]
        self.assertEqual(violations, 0, "Found review scores outside [1, 5] range!")

    def test_order_delivery_chronology(self):
        """Verify orders are not recorded delivered before they were purchased."""
        query = """
            SELECT COUNT(*) FROM orders 
            WHERE order_delivered_customer_date IS NOT NULL 
              AND order_delivered_customer_date < order_purchase_timestamp;
        """
        self.cur.execute(query)
        violations = self.cur.fetchone()[0]
        self.assertEqual(violations, 0, "Found delivery date before purchase date!")

if __name__ == "__main__":
    unittest.main()
