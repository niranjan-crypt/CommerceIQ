-- ==============================================================================
-- CommerceIQ — Referential Integrity & Domain Constraints
-- File: sql/03_constraints.sql
-- ==============================================================================

SET search_path TO oltp, public;

-- ------------------------------------------------------------------------------
-- 1. Foreign Key Constraints
-- Enforce referential integrity across transactional entities.
-- ------------------------------------------------------------------------------

-- Orders -> Customers
ALTER TABLE oltp.orders
    ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) 
    REFERENCES oltp.customers(customer_id)
    ON DELETE RESTRICT;

-- Products -> Categories
ALTER TABLE oltp.products
    ADD CONSTRAINT fk_products_category
    FOREIGN KEY (category_name)
    REFERENCES oltp.product_categories(category_name)
    ON DELETE SET NULL;

-- Order Items -> Orders
ALTER TABLE oltp.order_items
    ADD CONSTRAINT fk_order_items_order
    FOREIGN KEY (order_id)
    REFERENCES oltp.orders(order_id)
    ON DELETE CASCADE;

-- Order Items -> Products
ALTER TABLE oltp.order_items
    ADD CONSTRAINT fk_order_items_product
    FOREIGN KEY (product_id)
    REFERENCES oltp.products(product_id)
    ON DELETE RESTRICT;

-- Order Items -> Sellers
ALTER TABLE oltp.order_items
    ADD CONSTRAINT fk_order_items_seller
    FOREIGN KEY (seller_id)
    REFERENCES oltp.sellers(seller_id)
    ON DELETE RESTRICT;

-- Order Payments -> Orders
ALTER TABLE oltp.order_payments
    ADD CONSTRAINT fk_order_payments_order
    FOREIGN KEY (order_id)
    REFERENCES oltp.orders(order_id)
    ON DELETE CASCADE;

-- Order Reviews -> Orders
ALTER TABLE oltp.order_reviews
    ADD CONSTRAINT fk_order_reviews_order
    FOREIGN KEY (order_id)
    REFERENCES oltp.orders(order_id)
    ON DELETE CASCADE;

-- ------------------------------------------------------------------------------
-- 2. Domain / Business Rule CHECK Constraints
-- Guardrails ensuring invalid financial or temporal values never enter storage.
-- ------------------------------------------------------------------------------

-- Ensure item prices and freight values are non-negative
ALTER TABLE oltp.order_items
    ADD CONSTRAINT chk_item_price_positive
    CHECK (price >= 0.00),
    ADD CONSTRAINT chk_item_freight_positive
    CHECK (freight_value >= 0.00);

-- Ensure payment amounts and installments are non-negative
ALTER TABLE oltp.order_payments
    ADD CONSTRAINT chk_payment_val_positive
    CHECK (payment_value >= 0.00),
    ADD CONSTRAINT chk_payment_installments_positive
    CHECK (payment_installments >= 0);

-- Ensure review score adheres to 1-5 star scale
ALTER TABLE oltp.order_reviews
    ADD CONSTRAINT chk_review_score_range
    CHECK (review_score BETWEEN 1 AND 5);

-- Ensure chronological causality: Delivery must occur on or after purchase
ALTER TABLE oltp.orders
    ADD CONSTRAINT chk_order_delivery_after_purchase
    CHECK (order_delivered_customer_date IS NULL OR order_delivered_customer_date >= order_purchase_timestamp);

-- ------------------------------------------------------------------------------
-- 3. Foreign Key B-Tree Indexes
-- Essential in PostgreSQL: child tables do NOT automatically index foreign keys!
-- Without these indexes, parent DELETE/UPDATE operations require sequential table scans
-- on child tables to verify referential integrity, causing massive locking delays.
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON oltp.orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON oltp.order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_order_items_seller_id ON oltp.order_items(seller_id);
CREATE INDEX IF NOT EXISTS idx_order_payments_order_id ON oltp.order_payments(order_id);
CREATE INDEX IF NOT EXISTS idx_order_reviews_order_id ON oltp.order_reviews(order_id);
CREATE INDEX IF NOT EXISTS idx_customers_unique_id ON oltp.customers(customer_unique_id);
CREATE INDEX IF NOT EXISTS idx_geolocation_zip ON oltp.geolocation(geolocation_zip_code_prefix);
