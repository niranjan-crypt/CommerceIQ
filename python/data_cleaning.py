"""
CommerceIQ — Data Cleaning & Transformation Module
Handles: Missing values, timestamp parsing, category normalization, and deduplication.
"""

import os
import csv
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw"))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed"))

os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_customers():
    logging.info("Cleaning Customers dataset...")
    src = os.path.join(RAW_DIR, "olist_customers_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "customers.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "customer_id": row["customer_id"].strip(),
                "customer_unique_id": row["customer_unique_id"].strip(),
                "customer_zip_code_prefix": row["customer_zip_code_prefix"].strip().zfill(5),
                "customer_city": row["customer_city"].strip().title(),
                "customer_state": row["customer_state"].strip().upper()
            })

def clean_sellers():
    logging.info("Cleaning Sellers dataset...")
    src = os.path.join(RAW_DIR, "olist_sellers_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "sellers.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "seller_id": row["seller_id"].strip(),
                "seller_zip_code_prefix": row["seller_zip_code_prefix"].strip().zfill(5),
                "seller_city": row["seller_city"].strip().title(),
                "seller_state": row["seller_state"].strip().upper()
            })

def clean_product_categories():
    logging.info("Cleaning Product Category Translations...")
    src = os.path.join(RAW_DIR, "product_category_name_translation.csv")
    dst = os.path.join(PROCESSED_DIR, "product_categories.csv")
    categories = {}
    with open(src, "r", encoding="utf-8") as f_in:
        reader = csv.reader(f_in)
        next(reader)
        for r in reader:
            if len(r) >= 2:
                cat_orig = r[0].strip().lstrip("\ufeff")
                cat_eng = r[1].strip()
                categories[cat_orig] = cat_eng

    # Fill domain gaps identified in Day 3 exploratory profiling
    categories["pc_gamer"] = "pc_gamer"
    categories["portateis_cozinha_e_preparadores_de_alimentos"] = "kitchen_and_food_prep_appliances"
    categories["outro"] = "other"

    with open(dst, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["category_name", "category_name_english"])
        for k, v in sorted(categories.items()):
            writer.writerow([k, v])

def clean_products():
    logging.info("Cleaning Products dataset...")
    src = os.path.join(RAW_DIR, "olist_products_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "products.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = [
            "product_id", "category_name", "product_name_length",
            "product_description_length", "product_photos_qty", "product_weight_g",
            "product_length_cm", "product_height_cm", "product_width_cm"
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            cat = row["product_category_name"].strip() if row["product_category_name"] else "outro"
            writer.writerow({
                "product_id": row["product_id"].strip(),
                "category_name": cat,
                "product_name_length": int(row["product_name_lenght"]) if row["product_name_lenght"] else "",
                "product_description_length": int(row["product_description_lenght"]) if row["product_description_lenght"] else "",
                "product_photos_qty": int(row["product_photos_qty"]) if row["product_photos_qty"] else "",
                "product_weight_g": int(row["product_weight_g"]) if row["product_weight_g"] else "",
                "product_length_cm": int(row["product_length_cm"]) if row["product_length_cm"] else "",
                "product_height_cm": int(row["product_height_cm"]) if row["product_height_cm"] else "",
                "product_width_cm": int(row["product_width_cm"]) if row["product_width_cm"] else ""
            })

def clean_orders():
    logging.info("Cleaning Orders dataset...")
    src = os.path.join(RAW_DIR, "olist_orders_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "orders.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = [
            "order_id", "customer_id", "order_status", "order_purchase_timestamp",
            "order_approved_at", "order_delivered_carrier_date",
            "order_delivered_customer_date", "order_estimated_delivery_date"
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "order_id": row["order_id"].strip(),
                "customer_id": row["customer_id"].strip(),
                "order_status": row["order_status"].strip().lower(),
                "order_purchase_timestamp": row["order_purchase_timestamp"].strip(),
                "order_approved_at": row["order_approved_at"].strip() if row["order_approved_at"] else "",
                "order_delivered_carrier_date": row["order_delivered_carrier_date"].strip() if row["order_delivered_carrier_date"] else "",
                "order_delivered_customer_date": row["order_delivered_customer_date"].strip() if row["order_delivered_customer_date"] else "",
                "order_estimated_delivery_date": row["order_estimated_delivery_date"].strip()
            })

def clean_order_items():
    logging.info("Cleaning Order Items dataset...")
    src = os.path.join(RAW_DIR, "olist_order_items_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "order_items.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "order_id": row["order_id"].strip(),
                "order_item_id": int(row["order_item_id"]),
                "product_id": row["product_id"].strip(),
                "seller_id": row["seller_id"].strip(),
                "shipping_limit_date": row["shipping_limit_date"].strip(),
                "price": f"{float(row['price']):.2f}",
                "freight_value": f"{float(row['freight_value']):.2f}"
            })

def clean_order_payments():
    logging.info("Cleaning Order Payments dataset...")
    src = os.path.join(RAW_DIR, "olist_order_payments_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "order_payments.csv")
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            writer.writerow({
                "order_id": row["order_id"].strip(),
                "payment_sequential": int(row["payment_sequential"]),
                "payment_type": row["payment_type"].strip().lower(),
                "payment_installments": int(row["payment_installments"]),
                "payment_value": f"{float(row['payment_value']):.2f}"
            })

def clean_order_reviews():
    logging.info("Cleaning Order Reviews dataset...")
    src = os.path.join(RAW_DIR, "olist_order_reviews_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "order_reviews.csv")
    seen_pairs = set()
    with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = ["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message", "review_creation_date", "review_answer_timestamp"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            pair = (row["review_id"].strip(), row["order_id"].strip())
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            writer.writerow({
                "review_id": row["review_id"].strip(),
                "order_id": row["order_id"].strip(),
                "review_score": int(row["review_score"]),
                "review_comment_title": row["review_comment_title"].strip(),
                "review_comment_message": row["review_comment_message"].strip(),
                "review_creation_date": row["review_creation_date"].strip(),
                "review_answer_timestamp": row["review_answer_timestamp"].strip()
            })

def clean_geolocation():
    logging.info("Cleaning & Aggregating Geolocation dataset...")
    src = os.path.join(RAW_DIR, "olist_geolocation_dataset.csv")
    dst = os.path.join(PROCESSED_DIR, "geolocation_aggregated.csv")
    
    # Aggregate lat/lng coordinates by 5-digit zip code prefix
    zip_coords = {}
    with open(src, "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
            prefix = row["geolocation_zip_code_prefix"].strip().zfill(5)
            lat = float(row["geolocation_lat"])
            lng = float(row["geolocation_lng"])
            city = row["geolocation_city"].strip().title()
            state = row["geolocation_state"].strip().upper()
            
            if prefix not in zip_coords:
                zip_coords[prefix] = {"lat_sum": lat, "lng_sum": lng, "count": 1, "city": city, "state": state}
            else:
                zip_coords[prefix]["lat_sum"] += lat
                zip_coords[prefix]["lng_sum"] += lng
                zip_coords[prefix]["count"] += 1

    with open(dst, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["zip_code_prefix", "latitude", "longitude", "city", "state"])
        for prefix, data in sorted(zip_coords.items()):
            avg_lat = data["lat_sum"] / data["count"]
            avg_lng = data["lng_sum"] / data["count"]
            writer.writerow([prefix, f"{avg_lat:.6f}", f"{avg_lng:.6f}", data["city"], data["state"]])

def run_all_cleaners():
    logging.info("Starting CommerceIQ Data Cleaning Pipeline...")
    clean_customers()
    clean_sellers()
    clean_product_categories()
    clean_products()
    clean_orders()
    clean_order_items()
    clean_order_payments()
    clean_order_reviews()
    clean_geolocation()
    logging.info("All datasets successfully cleaned and staged in data/processed/!")

if __name__ == "__main__":
    run_all_cleaners()
