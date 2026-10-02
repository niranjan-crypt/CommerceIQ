# CommerceIQ: Automated Data Quality Audit Report
**Generated**: 2026-10-03 06:27:16 UTC
**Audit Summary**: 22 Passed | 0 Failed (Total: 22)

## Quality Checks Matrix

| Check Name | Category | Status | Total Records | Violations | Details |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Customers PK Uniqueness | Primary Key | ✅ PASSED | 99,441 | 0 | Checked columns: ['customer_id'] |
| Sellers PK Uniqueness | Primary Key | ✅ PASSED | 3,095 | 0 | Checked columns: ['seller_id'] |
| Products PK Uniqueness | Primary Key | ✅ PASSED | 32,951 | 0 | Checked columns: ['product_id'] |
| Categories PK Uniqueness | Primary Key | ✅ PASSED | 74 | 0 | Checked columns: ['category_name'] |
| Orders PK Uniqueness | Primary Key | ✅ PASSED | 99,441 | 0 | Checked columns: ['order_id'] |
| Order Items Composite PK Uniqueness | Primary Key | ✅ PASSED | 112,650 | 0 | Checked columns: ['order_id', 'order_item_id'] |
| Order Payments Composite PK Uniqueness | Primary Key | ✅ PASSED | 103,886 | 0 | Checked columns: ['order_id', 'payment_sequential'] |
| Order Reviews Composite PK Uniqueness | Primary Key | ✅ PASSED | 99,224 | 0 | Checked columns: ['review_id', 'order_id'] |
| Geolocation Aggregated Zip Uniqueness | Primary Key | ✅ PASSED | 19,015 | 0 | Checked columns: ['zip_code_prefix'] |
| FK: Orders -> Customers | Foreign Key | ✅ PASSED | 99,441 | 0 | orders.csv.customer_id in customers.csv.customer_id |
| FK: Order Items -> Orders | Foreign Key | ✅ PASSED | 112,650 | 0 | order_items.csv.order_id in orders.csv.order_id |
| FK: Order Items -> Products | Foreign Key | ✅ PASSED | 112,650 | 0 | order_items.csv.product_id in products.csv.product_id |
| FK: Order Items -> Sellers | Foreign Key | ✅ PASSED | 112,650 | 0 | order_items.csv.seller_id in sellers.csv.seller_id |
| FK: Order Payments -> Orders | Foreign Key | ✅ PASSED | 103,886 | 0 | order_payments.csv.order_id in orders.csv.order_id |
| FK: Order Reviews -> Orders | Foreign Key | ✅ PASSED | 99,224 | 0 | order_reviews.csv.order_id in orders.csv.order_id |
| FK: Products -> Product Categories | Foreign Key | ✅ PASSED | 32,951 | 0 | products.csv.category_name in product_categories.csv.category_name |
| Non-Negative Item Price | Numeric Bound | ✅ PASSED | 112,650 | 0 | price within [0.0, None] |
| Non-Negative Freight Value | Numeric Bound | ✅ PASSED | 112,650 | 0 | freight_value within [0.0, None] |
| Non-Negative Payment Value | Numeric Bound | ✅ PASSED | 103,886 | 0 | payment_value within [0.0, None] |
| Review Score Range (1-5) | Numeric Bound | ✅ PASSED | 99,224 | 0 | review_score within [1, 5] |
| Chronological Order: Delivered >= Purchased | Temporal Consistency | ✅ PASSED | 96,476 | 0 | Delivered timestamp vs purchase timestamp |
| Valid Order Status Domain | Domain Validation | ✅ PASSED | 99,441 | 0 | Allowed: ['approved', 'canceled', 'created', 'delivered', 'invoiced', 'processing', 'shipped', 'unavailable'] |

---
## Data Engineering Sign-Off
All staged datasets meet relational constraints, referential integrity criteria, and business logic validations.
Datasets are verified ready for loading into the PostgreSQL normalized OLTP layer.