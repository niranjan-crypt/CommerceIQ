"""
CommerceIQ — Database Loader Module
Loads cleaned and validated data into PostgreSQL (or SQLite local fallback)
respecting strict topological foreign key dependency order.
"""

import os
import csv
import sys
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))
SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sql"))
SQLITE_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "olist_oltp.db"))

def load_to_sqlite():
    logging.info(f"Initializing local relational database at: {SQLITE_DB}")
    if os.path.exists(SQLITE_DB):
        os.remove(SQLITE_DB)
        
    conn = sqlite3.connect(SQLITE_DB)
    cur = conn.cursor()
    
    # Enable foreign keys in SQLite
    cur.execute("PRAGMA foreign_keys = ON;")

    # 1. Level 0 Tables (Independent)
    logging.info("Creating Level 0 tables (customers, sellers, product_categories, geolocation)...")
    cur.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_unique_id TEXT NOT NULL,
            customer_zip_code_prefix TEXT NOT NULL,
            customer_city TEXT NOT NULL,
            customer_state TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE sellers (
            seller_id TEXT PRIMARY KEY,
            seller_zip_code_prefix TEXT NOT NULL,
            seller_city TEXT NOT NULL,
            seller_state TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE product_categories (
            category_name TEXT PRIMARY KEY,
            category_name_english TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE geolocation (
            zip_code_prefix TEXT PRIMARY KEY,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL
        );
    """)

    # 2. Level 1 Tables
    logging.info("Creating Level 1 tables (products, orders)...")
    cur.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            category_name TEXT,
            product_name_length INTEGER,
            product_description_length INTEGER,
            product_photos_qty INTEGER,
            product_weight_g INTEGER,
            product_length_cm INTEGER,
            product_height_cm INTEGER,
            product_width_cm INTEGER,
            FOREIGN KEY (category_name) REFERENCES product_categories(category_name)
        );
    """)
    cur.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_status TEXT NOT NULL,
            order_purchase_timestamp TEXT NOT NULL,
            order_approved_at TEXT,
            order_delivered_carrier_date TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    """)

    # 3. Level 2 Tables (Dependent Child Tables)
    logging.info("Creating Level 2 child tables (order_items, order_payments, order_reviews)...")
    cur.execute("""
        CREATE TABLE order_items (
            order_id TEXT NOT NULL,
            order_item_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            seller_id TEXT NOT NULL,
            shipping_limit_date TEXT NOT NULL,
            price REAL NOT NULL,
            freight_value REAL NOT NULL,
            PRIMARY KEY (order_id, order_item_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
        );
    """)
    cur.execute("""
        CREATE TABLE order_payments (
            order_id TEXT NOT NULL,
            payment_sequential INTEGER NOT NULL,
            payment_type TEXT NOT NULL,
            payment_installments INTEGER NOT NULL,
            payment_value REAL NOT NULL,
            PRIMARY KEY (order_id, payment_sequential),
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
        );
    """)
    cur.execute("""
        CREATE TABLE order_reviews (
            review_id TEXT NOT NULL,
            order_id TEXT NOT NULL,
            review_score INTEGER NOT NULL,
            review_comment_title TEXT,
            review_comment_message TEXT,
            review_creation_date TEXT NOT NULL,
            review_answer_timestamp TEXT NOT NULL,
            PRIMARY KEY (review_id, order_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
        );
    """)

    # Ingestion Routine
    load_plan = [
        ("customers.csv", "customers", 5),
        ("sellers.csv", "sellers", 4),
        ("product_categories.csv", "product_categories", 2),
        ("geolocation_aggregated.csv", "geolocation", 5),
        ("products.csv", "products", 9),
        ("orders.csv", "orders", 8),
        ("order_items.csv", "order_items", 7),
        ("order_payments.csv", "order_payments", 5),
        ("order_reviews.csv", "order_reviews", 7)
    ]

    for csv_file, table_name, num_cols in load_plan:
        file_path = os.path.join(PROCESSED_DIR, csv_file)
        logging.info(f"Loading {csv_file} into table `{table_name}`...")
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader) # skip headers
            cleaned_rows = [
                [None if val == "" else val for val in row]
                for row in reader
            ]
            placeholders = ", ".join(["?"] * num_cols)
            cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", cleaned_rows)

    conn.commit()

    # Create Foreign Key Indexes
    logging.info("Creating Foreign Key B-Tree indexes for fast joins...")
    indexes = [
        "CREATE INDEX idx_orders_customer ON orders(customer_id);",
        "CREATE INDEX idx_order_items_product ON order_items(product_id);",
        "CREATE INDEX idx_order_items_seller ON order_items(seller_id);",
        "CREATE INDEX idx_order_payments_order ON order_payments(order_id);",
        "CREATE INDEX idx_order_reviews_order ON order_reviews(order_id);",
        "CREATE INDEX idx_customers_unique ON customers(customer_unique_id);"
    ]
    for idx_sql in indexes:
        cur.execute(idx_sql)

    conn.commit()
    logging.info("Database load complete! All relational tables populated and indexed.")
    
    # Audit row counts
    for _, table_name, _ in load_plan:
        cnt = cur.execute(f"SELECT COUNT(*) FROM {table_name};").fetchone()[0]
        logging.info(f"Table `{table_name}`: {cnt:,} records")

    conn.close()

if __name__ == "__main__":
    load_to_sqlite()
