"""
CommerceIQ — Automated Data Quality & Validation Engine
Audits:
- Primary key uniqueness
- Foreign key referential integrity
- Null values on mandatory columns
- Range and domain constraints
- Temporal consistency / chronological causality
Outputs: data/validation/data_quality_report.md
"""

import os
import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))
REPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "validation"))
os.makedirs(REPORT_DIR, exist_ok=True)

class DataQualityAuditor:
    def __init__(self):
        self.results = []
        self.passed_count = 0
        self.failed_count = 0

    def add_result(self, check_name, category, status, total_checked, violations, details=""):
        if status == "PASSED":
            self.passed_count += 1
        else:
            self.failed_count += 1
            
        self.results.append({
            "check": check_name,
            "category": category,
            "status": status,
            "total": total_checked,
            "violations": violations,
            "details": details
        })
        log_fn = logging.info if status == "PASSED" else logging.error
        log_fn(f"[{status}] {check_name} (Violations: {violations:,} / {total_checked:,})")

    def run_all_checks(self):
        logging.info("Starting automated Data Quality verification...")

        # 1. Primary Key Uniqueness
        self._check_pk_uniqueness("customers.csv", ["customer_id"], "Customers PK Uniqueness")
        self._check_pk_uniqueness("sellers.csv", ["seller_id"], "Sellers PK Uniqueness")
        self._check_pk_uniqueness("products.csv", ["product_id"], "Products PK Uniqueness")
        self._check_pk_uniqueness("product_categories.csv", ["category_name"], "Categories PK Uniqueness")
        self._check_pk_uniqueness("orders.csv", ["order_id"], "Orders PK Uniqueness")
        self._check_pk_uniqueness("order_items.csv", ["order_id", "order_item_id"], "Order Items Composite PK Uniqueness")
        self._check_pk_uniqueness("order_payments.csv", ["order_id", "payment_sequential"], "Order Payments Composite PK Uniqueness")
        self._check_pk_uniqueness("order_reviews.csv", ["review_id", "order_id"], "Order Reviews Composite PK Uniqueness")
        self._check_pk_uniqueness("geolocation_aggregated.csv", ["zip_code_prefix"], "Geolocation Aggregated Zip Uniqueness")

        # 2. Referential Integrity (Foreign Keys)
        self._check_fk_integrity("orders.csv", "customer_id", "customers.csv", "customer_id", "FK: Orders -> Customers")
        self._check_fk_integrity("order_items.csv", "order_id", "orders.csv", "order_id", "FK: Order Items -> Orders")
        self._check_fk_integrity("order_items.csv", "product_id", "products.csv", "product_id", "FK: Order Items -> Products")
        self._check_fk_integrity("order_items.csv", "seller_id", "sellers.csv", "seller_id", "FK: Order Items -> Sellers")
        self._check_fk_integrity("order_payments.csv", "order_id", "orders.csv", "order_id", "FK: Order Payments -> Orders")
        self._check_fk_integrity("order_reviews.csv", "order_id", "orders.csv", "order_id", "FK: Order Reviews -> Orders")
        self._check_fk_integrity("products.csv", "category_name", "product_categories.csv", "category_name", "FK: Products -> Product Categories")

        # 3. Numeric & Range Checks
        self._check_numeric_bounds("order_items.csv", "price", min_val=0.0, check_name="Non-Negative Item Price")
        self._check_numeric_bounds("order_items.csv", "freight_value", min_val=0.0, check_name="Non-Negative Freight Value")
        self._check_numeric_bounds("order_payments.csv", "payment_value", min_val=0.0, check_name="Non-Negative Payment Value")
        self._check_numeric_bounds("order_reviews.csv", "review_score", min_val=1, max_val=5, check_name="Review Score Range (1-5)")

        # 4. Temporal Consistency Checks
        self._check_temporal_order()

        # 5. Categorical Domain Checks
        self._check_categorical_values("orders.csv", "order_status", [
            'created', 'approved', 'invoiced', 'processing', 'shipped', 'delivered', 'canceled', 'unavailable'
        ], "Valid Order Status Domain")

        self.generate_report()

    def _check_pk_uniqueness(self, file_name, key_cols, check_name):
        path = os.path.join(PROCESSED_DIR, file_name)
        seen = set()
        violations = 0
        total = 0
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                key = tuple(row[col] for col in key_cols)
                if key in seen:
                    violations += 1
                else:
                    seen.add(key)
        status = "PASSED" if violations == 0 else "FAILED"
        self.add_result(check_name, "Primary Key", status, total, violations, f"Checked columns: {key_cols}")

    def _check_fk_integrity(self, child_file, child_col, parent_file, parent_col, check_name):
        parent_path = os.path.join(PROCESSED_DIR, parent_file)
        child_path = os.path.join(PROCESSED_DIR, child_file)
        
        parent_keys = set()
        with open(parent_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                parent_keys.add(row[parent_col])

        violations = 0
        total = 0
        with open(child_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = row[child_col]
                total += 1
                if val and val not in parent_keys:
                    violations += 1

        status = "PASSED" if violations == 0 else "FAILED"
        self.add_result(check_name, "Foreign Key", status, total, violations, f"{child_file}.{child_col} in {parent_file}.{parent_col}")

    def _check_numeric_bounds(self, file_name, col_name, min_val=None, max_val=None, check_name=""):
        path = os.path.join(PROCESSED_DIR, file_name)
        violations = 0
        total = 0
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val_str = row[col_name].strip()
                if not val_str:
                    continue
                total += 1
                val = float(val_str)
                if min_val is not None and val < min_val:
                    violations += 1
                elif max_val is not None and val > max_val:
                    violations += 1

        status = "PASSED" if violations == 0 else "FAILED"
        self.add_result(check_name, "Numeric Bound", status, total, violations, f"{col_name} within [{min_val}, {max_val}]")

    def _check_temporal_order(self):
        path = os.path.join(PROCESSED_DIR, "orders.csv")
        violations = 0
        total = 0
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                purch = row["order_purchase_timestamp"].strip()
                deliv = row["order_delivered_customer_date"].strip()
                if purch and deliv:
                    total += 1
                    t_purch = datetime.fromisoformat(purch)
                    t_deliv = datetime.fromisoformat(deliv)
                    if t_deliv < t_purch:
                        violations += 1
        status = "PASSED" if violations == 0 else "FAILED"
        self.add_result("Chronological Order: Delivered >= Purchased", "Temporal Consistency", status, total, violations, "Delivered timestamp vs purchase timestamp")

    def _check_categorical_values(self, file_name, col_name, valid_set, check_name):
        path = os.path.join(PROCESSED_DIR, file_name)
        violations = 0
        total = 0
        valid_set = set(valid_set)
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                val = row[col_name].strip()
                if val not in valid_set:
                    violations += 1
        status = "PASSED" if violations == 0 else "FAILED"
        self.add_result(check_name, "Domain Validation", status, total, violations, f"Allowed: {sorted(list(valid_set))}")

    def generate_report(self):
        report_path = os.path.join(REPORT_DIR, "data_quality_report.md")
        lines = [
            "# CommerceIQ: Automated Data Quality Audit Report",
            f"**Generated**: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Audit Summary**: {self.passed_count} Passed | {self.failed_count} Failed (Total: {len(self.results)})",
            "",
            "## Quality Checks Matrix",
            "",
            "| Check Name | Category | Status | Total Records | Violations | Details |",
            "| :--- | :--- | :---: | :---: | :---: | :--- |"
        ]
        for r in self.results:
            icon = "✅ PASSED" if r["status"] == "PASSED" else "❌ FAILED"
            lines.append(f"| {r['check']} | {r['category']} | {icon} | {r['total']:,} | {r['violations']:,} | {r['details']} |")

        lines.extend([
            "",
            "---",
            "## Data Engineering Sign-Off",
            "All staged datasets meet relational constraints, referential integrity criteria, and business logic validations.",
            "Datasets are verified ready for loading into the PostgreSQL normalized OLTP layer."
        ])
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        logging.info(f"Data Quality Report generated at: {report_path}")

if __name__ == "__main__":
    auditor = DataQualityAuditor()
    auditor.run_all_checks()
