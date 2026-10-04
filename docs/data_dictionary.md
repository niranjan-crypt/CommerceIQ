# CommerceIQ: Comprehensive Dataset Dictionary & Profile

This data dictionary profiles the raw Olist Brazilian E-Commerce dataset.
It details schema structures, cardinality, null counts, and candidate keys for our relational modeling.

## Summary of Raw Datasets

| Table Name | Total Records | Column Count | Potential Primary Key |
| :--- | :--- | :--- | :--- |
| `olist_customers_dataset` | 99,441 | 5 | `customer_id` |
| `olist_geolocation_dataset` | 1,000,163 | 5 | `geolocation_zip_code_prefix` |
| `olist_order_items_dataset` | 112,650 | 7 | `order_id` |
| `olist_order_payments_dataset` | 103,886 | 5 | `order_id` |
| `olist_order_reviews_dataset` | 99,224 | 7 | `review_id` |
| `olist_orders_dataset` | 99,441 | 8 | `order_id` |
| `olist_products_dataset` | 32,951 | 9 | `product_id` |
| `olist_sellers_dataset` | 3,095 | 4 | `seller_id` |
| `product_category_name_translation` | 71 | 2 | `﻿product_category_name` |

---

## Detailed Table Specifications

### Table: `olist_customers_dataset`
- **Row Count**: 99,441
- **Column Count**: 5

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `customer_id` | 0 | 0.0% | `06b8999e2fba1a1fbc88172c00ba8b` | `VARCHAR(32)` |
| `customer_unique_id` | 0 | 0.0% | `861eff4711a542e4b93843c6dd7feb` | `VARCHAR(32)` |
| `customer_zip_code_prefix` | 0 | 0.0% | `14409` | `VARCHAR(5)` |
| `customer_city` | 0 | 0.0% | `franca` | `VARCHAR(255)` |
| `customer_state` | 0 | 0.0% | `SP` | `VARCHAR(2)` |

---

### Table: `olist_geolocation_dataset`
- **Row Count**: 1,000,163
- **Column Count**: 5

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `geolocation_zip_code_prefix` | 0 | 0.0% | `01037` | `VARCHAR(5)` |
| `geolocation_lat` | 0 | 0.0% | `-23.54562128115268` | `NUMERIC(10, 6)` |
| `geolocation_lng` | 0 | 0.0% | `-46.63929204800168` | `NUMERIC(10, 6)` |
| `geolocation_city` | 0 | 0.0% | `sao paulo` | `VARCHAR(255)` |
| `geolocation_state` | 0 | 0.0% | `SP` | `VARCHAR(2)` |

---

### Table: `olist_order_items_dataset`
- **Row Count**: 112,650
- **Column Count**: 7

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | 0 | 0.0% | `00010242fe8c5a6d1ba2dd792cb162` | `VARCHAR(32)` |
| `order_item_id` | 0 | 0.0% | `1` | `INTEGER` |
| `product_id` | 0 | 0.0% | `4244733e06e7ecb4970a6e2683c13e` | `VARCHAR(32)` |
| `seller_id` | 0 | 0.0% | `48436dade18ac8b2bce089ec2a0412` | `VARCHAR(32)` |
| `shipping_limit_date` | 0 | 0.0% | `2017-09-19 09:45:35` | `TIMESTAMP` |
| `price` | 0 | 0.0% | `58.90` | `NUMERIC(10, 2)` |
| `freight_value` | 0 | 0.0% | `13.29` | `NUMERIC(10, 2)` |

---

### Table: `olist_order_payments_dataset`
- **Row Count**: 103,886
- **Column Count**: 5

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | 0 | 0.0% | `b81ef226f3fe1789b1e8b2acac839d` | `VARCHAR(32)` |
| `payment_sequential` | 0 | 0.0% | `1` | `INTEGER` |
| `payment_type` | 0 | 0.0% | `credit_card` | `VARCHAR(255)` |
| `payment_installments` | 0 | 0.0% | `8` | `INTEGER` |
| `payment_value` | 0 | 0.0% | `99.33` | `NUMERIC(10, 2)` |

---

### Table: `olist_order_reviews_dataset`
- **Row Count**: 99,224
- **Column Count**: 7

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `review_id` | 0 | 0.0% | `7bc2406110b926393aa56f80a40eba` | `VARCHAR(32)` |
| `order_id` | 0 | 0.0% | `73fc7af87114b39712e6da79b0a377` | `VARCHAR(32)` |
| `review_score` | 0 | 0.0% | `4` | `INTEGER` |
| `review_comment_title` | 87,658 | 88.3% | `recomendo` | `VARCHAR(255)` |
| `review_comment_message` | 58,274 | 58.7% | `Recebi bem antes do prazo esti` | `VARCHAR(255)` |
| `review_creation_date` | 0 | 0.0% | `2018-01-18 00:00:00` | `TIMESTAMP` |
| `review_answer_timestamp` | 0 | 0.0% | `2018-01-18 21:46:59` | `TIMESTAMP` |

---

### Table: `olist_orders_dataset`
- **Row Count**: 99,441
- **Column Count**: 8

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | 0 | 0.0% | `e481f51cbdc54678b7cc49136f2d6a` | `VARCHAR(32)` |
| `customer_id` | 0 | 0.0% | `9ef432eb6251297304e76186b10a92` | `VARCHAR(32)` |
| `order_status` | 0 | 0.0% | `delivered` | `VARCHAR(255)` |
| `order_purchase_timestamp` | 0 | 0.0% | `2017-10-02 10:56:33` | `TIMESTAMP` |
| `order_approved_at` | 160 | 0.2% | `2017-10-02 11:07:15` | `TIMESTAMP` |
| `order_delivered_carrier_date` | 1,783 | 1.8% | `2017-10-04 19:55:00` | `TIMESTAMP` |
| `order_delivered_customer_date` | 2,965 | 3.0% | `2017-10-10 21:25:13` | `TIMESTAMP` |
| `order_estimated_delivery_date` | 0 | 0.0% | `2017-10-18 00:00:00` | `TIMESTAMP` |

---

### Table: `olist_products_dataset`
- **Row Count**: 32,951
- **Column Count**: 9

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `product_id` | 0 | 0.0% | `1e9e8ef04dbcff4541ed26657ea517` | `VARCHAR(32)` |
| `product_category_name` | 610 | 1.9% | `perfumaria` | `VARCHAR(255)` |
| `product_name_lenght` | 610 | 1.9% | `40` | `VARCHAR(255)` |
| `product_description_lenght` | 610 | 1.9% | `287` | `VARCHAR(255)` |
| `product_photos_qty` | 610 | 1.9% | `1` | `INTEGER` |
| `product_weight_g` | 2 | 0.0% | `225` | `INTEGER` |
| `product_length_cm` | 2 | 0.0% | `16` | `INTEGER` |
| `product_height_cm` | 2 | 0.0% | `10` | `INTEGER` |
| `product_width_cm` | 2 | 0.0% | `14` | `INTEGER` |

---

### Table: `olist_sellers_dataset`
- **Row Count**: 3,095
- **Column Count**: 4

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `seller_id` | 0 | 0.0% | `3442f8959a84dea7ee197c632cb2df` | `VARCHAR(32)` |
| `seller_zip_code_prefix` | 0 | 0.0% | `13023` | `VARCHAR(5)` |
| `seller_city` | 0 | 0.0% | `campinas` | `VARCHAR(255)` |
| `seller_state` | 0 | 0.0% | `SP` | `VARCHAR(2)` |

---

### Table: `product_category_name_translation`
- **Row Count**: 71
- **Column Count**: 2

| Column Name | Null Count | Null % | Sample Value | Suggested Postgres Type |
| :--- | :--- | :--- | :--- | :--- |
| `﻿product_category_name` | 0 | 0.0% | `beleza_saude` | `VARCHAR(255)` |
| `product_category_name_english` | 0 | 0.0% | `health_beauty` | `VARCHAR(255)` |

---
