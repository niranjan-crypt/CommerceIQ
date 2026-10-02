-- ==============================================================================
-- CommerceIQ — Analytical Star Schema Transformations (OLAP Layer)
-- File: sql/05_transformations.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Date Dimension (dim_date)
-- Enables slicing and dicing across temporal attributes without runtime parsing.
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date AS
WITH RECURSIVE date_series(curr_date) AS (
    SELECT '2016-01-01'
    UNION ALL
    SELECT date(curr_date, '+1 day')
    FROM date_series
    WHERE curr_date < '2018-12-31'
)
SELECT 
    strftime('%Y%m%d', curr_date) AS date_key,
    curr_date AS full_date,
    CAST(strftime('%Y', curr_date) AS INTEGER) AS year,
    CAST(strftime('%m', curr_date) AS INTEGER) AS month,
    strftime('%Y-%m', curr_date) AS year_month,
    CASE CAST(strftime('%m', curr_date) AS INTEGER)
        WHEN 1 THEN 'January' WHEN 2 THEN 'February' WHEN 3 THEN 'March'
        WHEN 4 THEN 'April'   WHEN 5 THEN 'May'      WHEN 6 THEN 'June'
        WHEN 7 THEN 'July'    WHEN 8 THEN 'August'   WHEN 9 THEN 'September'
        WHEN 10 THEN 'October' WHEN 11 THEN 'November' ELSE 'December'
    END AS month_name,
    ((CAST(strftime('%m', curr_date) AS INTEGER) - 1) / 3) + 1 AS quarter,
    strftime('%w', curr_date) AS day_of_week,
    CASE WHEN strftime('%w', curr_date) IN ('0', '6') THEN 1 ELSE 0 END AS is_weekend
FROM date_series;

CREATE UNIQUE INDEX idx_dim_date_key ON dim_date(date_key);
CREATE INDEX idx_dim_date_full ON dim_date(full_date);


-- ------------------------------------------------------------------------------
-- 2. Customer Dimension (dim_customer)
-- Conformed dimension unifying customer geographic and human identifier data.
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dim_customer;
CREATE TABLE dim_customer AS
SELECT 
    customer_id AS customer_key,
    customer_unique_id,
    customer_zip_code_prefix AS zip_code_prefix,
    customer_city AS city,
    customer_state AS state
FROM customers;

CREATE UNIQUE INDEX idx_dim_customer_key ON dim_customer(customer_key);
CREATE INDEX idx_dim_customer_unique ON dim_customer(customer_unique_id);


-- ------------------------------------------------------------------------------
-- 3. Product Dimension (dim_product)
-- Denormalized dimension bringing together Portuguese categories and English translations.
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dim_product;
CREATE TABLE dim_product AS
SELECT 
    p.product_id AS product_key,
    COALESCE(cat.category_name_english, p.category_name, 'Unknown') AS category_name,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm * p.product_height_cm * p.product_width_cm AS product_volume_cm3
FROM products p
LEFT JOIN product_categories cat ON p.category_name = cat.category_name;

CREATE UNIQUE INDEX idx_dim_product_key ON dim_product(product_key);


-- ------------------------------------------------------------------------------
-- 4. Seller Dimension (dim_seller)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS dim_seller;
CREATE TABLE dim_seller AS
SELECT 
    seller_id AS seller_key,
    seller_zip_code_prefix AS zip_code_prefix,
    seller_city AS city,
    seller_state AS state
FROM sellers;

CREATE UNIQUE INDEX idx_dim_seller_key ON dim_seller(seller_key);


-- ------------------------------------------------------------------------------
-- 5. Fact Orders (fact_orders)
-- Grain: One row per order header. Precomputes order-level aggregates for instant querying.
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_orders;
CREATE TABLE fact_orders AS
WITH order_item_agg AS (
    SELECT 
        order_id,
        COUNT(order_item_id) AS items_count,
        ROUND(SUM(price), 2) AS total_items_price,
        ROUND(SUM(freight_value), 2) AS total_freight_value
    FROM order_items
    GROUP BY order_id
),
order_pay_agg AS (
    SELECT 
        order_id,
        ROUND(SUM(payment_value), 2) AS total_payment_value,
        MAX(payment_installments) AS max_installments
    FROM order_payments
    GROUP BY order_id
),
order_rev_agg AS (
    SELECT 
        order_id,
        AVG(review_score) AS avg_review_score
    FROM order_reviews
    GROUP BY order_id
)
SELECT 
    o.order_id,
    o.customer_id AS customer_key,
    strftime('%Y%m%d', o.order_purchase_timestamp) AS order_date_key,
    strftime('%Y%m%d', o.order_delivered_customer_date) AS delivered_date_key,
    o.order_status,
    COALESCE(i.items_count, 0) AS total_items,
    COALESCE(i.total_items_price, 0.00) AS total_items_price,
    COALESCE(i.total_freight_value, 0.00) AS total_freight_value,
    COALESCE(p.total_payment_value, 0.00) AS total_payment_value,
    p.max_installments,
    r.avg_review_score,
    ROUND(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp), 1) AS actual_delivery_days,
    ROUND(julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp), 1) AS estimated_delivery_days,
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
        ELSE 0 
    END AS is_late_delivery
FROM orders o
LEFT JOIN order_item_agg i ON o.order_id = i.order_id
LEFT JOIN order_pay_agg p ON o.order_id = p.order_id
LEFT JOIN order_rev_agg r ON o.order_id = r.order_id;

CREATE UNIQUE INDEX idx_fact_orders_pk ON fact_orders(order_id);
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_key);
CREATE INDEX idx_fact_orders_date ON fact_orders(order_date_key);


-- ------------------------------------------------------------------------------
-- 6. Fact Order Items (fact_order_items)
-- Grain: One row per individual item line. Finest analytical granularity.
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_order_items;
CREATE TABLE fact_order_items AS
WITH order_rev_agg AS (
    SELECT 
        order_id,
        AVG(review_score) AS avg_review_score
    FROM order_reviews
    GROUP BY order_id
)
SELECT 
    oi.order_id,
    oi.order_item_id,
    o.customer_id AS customer_key,
    oi.product_id AS product_key,
    oi.seller_id AS seller_key,
    strftime('%Y%m%d', o.order_purchase_timestamp) AS order_date_key,
    oi.price,
    oi.freight_value,
    ROUND(oi.price + oi.freight_value, 2) AS total_item_cost,
    r.avg_review_score AS review_score
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN order_rev_agg r ON oi.order_id = r.order_id;

CREATE UNIQUE INDEX idx_fact_items_pk ON fact_order_items(order_id, order_item_id);
CREATE INDEX idx_fact_items_prod ON fact_order_items(product_key);
CREATE INDEX idx_fact_items_seller ON fact_order_items(seller_key);
CREATE INDEX idx_fact_items_date ON fact_order_items(order_date_key);
