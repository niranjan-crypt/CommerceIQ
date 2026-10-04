-- ==============================================================================
-- CommerceIQ — Normalized OLTP Tables (3NF)
-- File: sql/02_tables.sql
-- ==============================================================================

-- Drop existing tables in reverse dependency order if recreating
DROP TABLE IF EXISTS oltp.order_reviews CASCADE;
DROP TABLE IF EXISTS oltp.order_payments CASCADE;
DROP TABLE IF EXISTS oltp.order_items CASCADE;
DROP TABLE IF EXISTS oltp.orders CASCADE;
DROP TABLE IF EXISTS oltp.products CASCADE;
DROP TABLE IF EXISTS oltp.product_categories CASCADE;
DROP TABLE IF EXISTS oltp.sellers CASCADE;
DROP TABLE IF EXISTS oltp.customers CASCADE;
DROP TABLE IF EXISTS oltp.geolocation CASCADE;

-- ------------------------------------------------------------------------------
-- 1. Customers Table
-- Note: `customer_id` is an order-scoped surrogate key generated per transaction.
-- `customer_unique_id` represents the unique human consumer across multiple orders.
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.customers (
    customer_id                 VARCHAR(32) PRIMARY KEY,
    customer_unique_id          VARCHAR(32) NOT NULL,
    customer_zip_code_prefix    VARCHAR(5) NOT NULL,
    customer_city               VARCHAR(100) NOT NULL,
    customer_state              CHAR(2) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 2. Sellers Table
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.sellers (
    seller_id                   VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix      VARCHAR(5) NOT NULL,
    seller_city                 VARCHAR(100) NOT NULL,
    seller_state                CHAR(2) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 3. Product Categories (Translation / Domain Table)
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.product_categories (
    category_name               VARCHAR(100) PRIMARY KEY,
    category_name_english       VARCHAR(100) NOT NULL
);

-- ------------------------------------------------------------------------------
-- 4. Products Table
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.products (
    product_id                  VARCHAR(32) PRIMARY KEY,
    category_name               VARCHAR(100),
    product_name_length         INTEGER,
    product_description_length  INTEGER,
    product_photos_qty          INTEGER,
    product_weight_g            INTEGER,
    product_length_cm           INTEGER,
    product_height_cm           INTEGER,
    product_width_cm            INTEGER
);

-- ------------------------------------------------------------------------------
-- 5. Orders Table
-- Header record representing customer checkout transactions.
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.orders (
    order_id                    VARCHAR(32) PRIMARY KEY,
    customer_id                 VARCHAR(32) NOT NULL,
    order_status                VARCHAR(20) NOT NULL,
    order_purchase_timestamp    TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    order_approved_at           TIMESTAMP WITHOUT TIME ZONE,
    order_delivered_carrier_date TIMESTAMP WITHOUT TIME ZONE,
    order_delivered_customer_date TIMESTAMP WITHOUT TIME ZONE,
    order_estimated_delivery_date TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- ------------------------------------------------------------------------------
-- 6. Order Items Table
-- Associative table resolving M:N relationship between Orders and Products/Sellers.
-- Composite Primary Key: (order_id, order_item_id)
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.order_items (
    order_id                    VARCHAR(32) NOT NULL,
    order_item_id               INTEGER NOT NULL,
    product_id                  VARCHAR(32) NOT NULL,
    seller_id                   VARCHAR(32) NOT NULL,
    shipping_limit_date         TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    price                       NUMERIC(10, 2) NOT NULL,
    freight_value               NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, order_item_id)
);

-- ------------------------------------------------------------------------------
-- 7. Order Payments Table
-- Line items detailing payment methods and installments per order.
-- Composite Primary Key: (order_id, payment_sequential)
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.order_payments (
    order_id                    VARCHAR(32) NOT NULL,
    payment_sequential          INTEGER NOT NULL,
    payment_type                VARCHAR(20) NOT NULL,
    payment_installments        INTEGER NOT NULL,
    payment_value               NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (order_id, payment_sequential)
);

-- ------------------------------------------------------------------------------
-- 8. Order Reviews Table
-- Composite Primary Key: (review_id, order_id) handles multi-order review submissions.
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.order_reviews (
    review_id                   VARCHAR(32) NOT NULL,
    order_id                    VARCHAR(32) NOT NULL,
    review_score                INTEGER NOT NULL,
    review_comment_title        TEXT,
    review_comment_message      TEXT,
    review_creation_date        TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    review_answer_timestamp     TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (review_id, order_id)
);

-- ------------------------------------------------------------------------------
-- 9. Geolocation Table (Raw Coordinates)
-- Holds raw postal coordinate observations across Brazilian municipalities.
-- ------------------------------------------------------------------------------
CREATE TABLE oltp.geolocation (
    geolocation_id              SERIAL PRIMARY KEY,
    geolocation_zip_code_prefix VARCHAR(5) NOT NULL,
    geolocation_lat             NUMERIC(10, 6) NOT NULL,
    geolocation_lng             NUMERIC(10, 6) NOT NULL,
    geolocation_city            VARCHAR(100) NOT NULL,
    geolocation_state           CHAR(2) NOT NULL
);
