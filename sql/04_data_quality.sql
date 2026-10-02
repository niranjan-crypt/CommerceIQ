-- ==============================================================================
-- CommerceIQ — Data Quality & Integrity Validation Queries
-- File: sql/04_data_quality.sql
-- Run via: python3 run_query.py sql/04_data_quality.sql
-- ==============================================================================

-- 1. Check for Orphan Order Items (Must be 0)
SELECT COUNT(*) AS orphan_items_count
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;

-- 2. Check for Duplicate Primary Keys in Orders (Must be 0)
SELECT order_id, COUNT(*) AS occurrences
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 3. Check for Negative Prices or Freight (Must be 0)
SELECT COUNT(*) AS invalid_financial_records
FROM order_items
WHERE price < 0.00 OR freight_value < 0.00;

-- 4. Check for Out-of-Range Review Scores (Must be 0)
SELECT COUNT(*) AS invalid_review_scores
FROM order_reviews
WHERE review_score NOT BETWEEN 1 AND 5;

-- 5. Check for Chronological Inconsistencies (Must be 0)
SELECT COUNT(*) AS delivery_before_purchase_count
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_delivered_customer_date < order_purchase_timestamp;
