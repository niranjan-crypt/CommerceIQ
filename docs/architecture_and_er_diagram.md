# CommerceIQ: Architectural Blueprints & Data Lineage

This document outlines the conceptual, logical, and physical architectures of the **CommerceIQ Platform**, contrasting the **Normalized 3NF Transactional Layer (OLTP)** with the **Kimball Star Schema Analytical Mart (OLAP)**.

---

## 1. End-to-End System Lineage Diagram

```mermaid
flowchart TD
    subgraph S1["Raw Ingestion Layer"]
        CSV1["olist_orders_dataset.csv"]
        CSV2["olist_order_items_dataset.csv"]
        CSV3["olist_customers_dataset.csv"]
        CSV4["olist_products_dataset.csv"]
        CSV5["olist_sellers_dataset.csv"]
        CSV6["olist_payments_dataset.csv"]
        CSV7["olist_reviews_dataset.csv"]
        CSV8["olist_geolocation_dataset.csv"]
    end

    subgraph S2["Python ETL & Data Quality Engine"]
        CLEAN["python/data_cleaning.py<br/>(Datetime normalization, null handling, category translation)"]
        AUDIT["python/data_validation.py<br/>(22 Automated Data Quality Gates)"]
        LOADER["python/database_loader.py<br/>(Topological Dependency Batch Ingestion)"]
    end

    subgraph S3["PostgreSQL Relational Layer (3NF OLTP)"]
        T1[("customers")]
        T2[("sellers")]
        T3[("products")]
        T4[("orders")]
        T5[("order_items")]
        T6[("order_payments")]
        T7[("order_reviews")]
        T8[("geolocation")]
    end

    subgraph S4["Analytical Dimensional Layer (Star Schema OLAP)"]
        F1[("fact_orders")]
        F2[("fact_order_items")]
        D1[("dim_customer")]
        D2[("dim_product")]
        D3[("dim_seller")]
        D4[("dim_date")]
    end

    subgraph S5["Analytical Serving & Business Intelligence"]
        SQL_ADV["Advanced SQL Models<br/>(RFM Segmentation, Cohort Retention, Market Basket)"]
        DASH["Streamlit BI Platform<br/>(Plotly Visuals, Geospatial Brazil Map, SQL Sandbox)"]
    end

    CSV1 & CSV2 & CSV3 & CSV4 & CSV5 & CSV6 & CSV7 & CSV8 --> CLEAN
    CLEAN --> AUDIT
    AUDIT --> LOADER
    LOADER --> T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8
    T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8 --> F1 & F2 & D1 & D2 & D3 & D4
    F1 & F2 & D1 & D2 & D3 & D4 --> SQL_ADV
    SQL_ADV --> DASH
```

---

## 2. Relational OLTP Entity-Relationship Diagram (3NF)

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS ||--o{ ORDER_PAYMENTS : "paid via"
    ORDERS ||--o{ ORDER_REVIEWS : receives
    SELLERS ||--o{ ORDER_ITEMS : fulfills
    PRODUCTS ||--o{ ORDER_ITEMS : contains
    PRODUCT_CATEGORIES ||--o{ PRODUCTS : categorizes

    CUSTOMERS {
        varchar customer_id PK
        varchar customer_unique_id
        varchar customer_zip_code_prefix
        varchar customer_city
        char customer_state
    }

    ORDERS {
        varchar order_id PK
        varchar customer_id FK
        varchar order_status
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }

    ORDER_ITEMS {
        varchar order_id PK,FK
        integer order_item_id PK
        varchar product_id FK
        varchar seller_id FK
        timestamp shipping_limit_date
        numeric price
        numeric freight_value
    }

    ORDER_PAYMENTS {
        varchar order_id PK,FK
        integer payment_sequential PK
        varchar payment_type
        integer payment_installments
        numeric payment_value
    }

    ORDER_REVIEWS {
        varchar review_id PK
        varchar order_id PK,FK
        integer review_score
        text review_comment_title
        text review_comment_message
        timestamp review_creation_date
        timestamp review_answer_timestamp
    }

    PRODUCTS {
        varchar product_id PK
        varchar category_name FK
        integer product_name_length
        integer product_description_length
        integer product_photos_qty
        integer product_weight_g
        integer product_volume_cm3
    }

    SELLERS {
        varchar seller_id PK
        varchar seller_zip_code_prefix
        varchar seller_city
        char seller_state
    }

    PRODUCT_CATEGORIES {
        varchar category_name PK
        varchar category_name_english
    }
```

---

## 3. Kimball Star Schema Dimensional Model (OLAP)

```mermaid
erDiagram
    FACT_ORDERS }o--|| DIM_CUSTOMER : "sliced by"
    FACT_ORDERS }o--|| DIM_DATE : "ordered on"
    FACT_ORDER_ITEMS }o--|| DIM_PRODUCT : "item details"
    FACT_ORDER_ITEMS }o--|| DIM_SELLER : "fulfilled by"
    FACT_ORDER_ITEMS }o--|| DIM_DATE : "purchased on"
    FACT_ORDER_ITEMS }o--|| FACT_ORDERS : "line item parent"

    FACT_ORDERS {
        varchar order_id PK
        varchar customer_key FK
        varchar order_date_key FK
        varchar delivered_date_key FK
        varchar order_status
        integer total_items
        numeric total_items_price
        numeric total_freight_value
        numeric total_payment_value
        numeric avg_review_score
        numeric actual_delivery_days
        integer is_late_delivery
    }

    FACT_ORDER_ITEMS {
        varchar order_id PK,FK
        integer order_item_id PK
        varchar customer_key FK
        varchar product_key FK
        varchar seller_key FK
        varchar order_date_key FK
        numeric price
        numeric freight_value
        numeric total_item_cost
        numeric review_score
    }

    DIM_CUSTOMER {
        varchar customer_key PK
        varchar customer_unique_id
        varchar city
        char state
        varchar zip_code_prefix
    }

    DIM_PRODUCT {
        varchar product_key PK
        varchar category_name
        integer product_photos_qty
        integer product_weight_g
        integer product_volume_cm3
    }

    DIM_SELLER {
        varchar seller_key PK
        varchar city
        char state
        varchar zip_code_prefix
    }

    DIM_DATE {
        varchar date_key PK
        date full_date
        integer year
        integer month
        varchar month_name
        integer quarter
        integer is_weekend
    }
```
