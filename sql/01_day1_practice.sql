-- ==============================================================================
-- CommerceIQ — Day 1: SQL Fundamentals Practice
-- Execute via terminal: python3 run_query.py sql/01_day1_practice.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Exercise 1: Filtered Aggregation
-- Business Question:
-- For each order status in the `orders` table, calculate the total number of orders.
-- Show only statuses with at least 500 orders, sorted from highest to lowest count.
-- ------------------------------------------------------------------------------

-- WRITE YOUR QUERY FOR EXERCISE 1 BELOW:
SELECT 
    order_status, 
    COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
HAVING COUNT(*) >= 500
ORDER BY total_orders DESC;


-- ------------------------------------------------------------------------------
-- Exercise 2: High-Volume Seller Analysis
-- Business Question:
-- From `order_items`, find sellers who sold at least 10 items with an average
-- item price > 150.00. Display: seller_id, items_sold, avg_price (rounded to 2 decimals),
-- and total_revenue. Sort by total_revenue descending.
-- ------------------------------------------------------------------------------

-- WRITE YOUR QUERY FOR EXERCISE 2 BELOW:
SELECT 
    seller_id,
    COUNT(*) AS items_sold,
    ROUND(AVG(price), 2) AS avg_item_price,
    ROUND(SUM(price), 2) AS total_revenue
FROM order_items
GROUP BY seller_id
HAVING COUNT(*) >= 10 AND AVG(price) > 150.00
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------------------------
-- Exercise 3: Order Revenue Classification
-- Business Question:
-- From `order_items`, calculate total item spend per order_id. Using CASE WHEN,
-- classify into:
--   - 'High Value'   (total spend >= 500)
--   - 'Medium Value' (total spend BETWEEN 100 AND 499.99)
--   - 'Low Value'    (total spend < 100)
-- Return order_id, total_spend, and order_tier. Limit to 10 rows.
-- ------------------------------------------------------------------------------

-- WRITE YOUR QUERY FOR EXERCISE 3 BELOW:
SELECT 
    order_id,
    ROUND(SUM(price), 2) AS total_item_spend,
    CASE 
        WHEN SUM(price) >= 500 THEN 'High Value'
        WHEN SUM(price) >= 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_tier
FROM order_items
GROUP BY order_id
ORDER BY total_item_spend DESC
LIMIT 10;
