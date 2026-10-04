-- ==============================================================================
-- CommerceIQ — Day 8: Business Intelligence & Executive KPI Queries
-- File: sql/06_business_analytics.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Executive Platform KPIs (GMV, Item Revenue, Freight, AOV, Unique Customers)
-- Answers: What is the total scale and top-line performance of the platform?
-- ------------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT o.order_id) AS total_delivered_orders,
    COUNT(DISTINCT c.customer_unique_id) AS total_unique_customers,
    ROUND(SUM(oi.price), 2) AS total_item_revenue,
    ROUND(SUM(oi.freight_value), 2) AS total_freight_value,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS gross_merchandise_value,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value,
    ROUND(AVG(r.review_score), 2) AS platform_avg_rating
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered';


-- ------------------------------------------------------------------------------
-- 2. Customer Retention & Repeat Purchase Analysis
-- Answers: What percentage of our customers return to make multiple purchases?
-- Critical Note: Must group by customer_unique_id, NOT customer_id!
-- ------------------------------------------------------------------------------
WITH customer_order_frequencies AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.price), 2) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN total_orders = 1 THEN 1 ELSE 0 END) AS one_time_buyers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_rate_pct,
    ROUND(AVG(total_spend), 2) AS overall_avg_spend_per_customer
FROM customer_order_frequencies;


-- ------------------------------------------------------------------------------
-- 3. Top Product Categories by Revenue Contribution & Quality
-- Answers: Which product categories drive the highest sales, and how satisfied
-- are customers with them?
-- ------------------------------------------------------------------------------
SELECT 
    COALESCE(cat.category_name_english, p.category_name, 'Unknown') AS product_category,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.order_item_id) AS items_sold,
    ROUND(SUM(oi.price), 2) AS category_revenue,
    ROUND(100.0 * SUM(oi.price) / (SELECT SUM(price) FROM order_items), 2) AS pct_revenue_share,
    ROUND(AVG(r.review_score), 2) AS avg_review_score
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_categories cat ON p.category_name = cat.category_name
LEFT JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY 1
ORDER BY category_revenue DESC
LIMIT 10;


-- ------------------------------------------------------------------------------
-- 4. Geographic Revenue & Logistics Distribution by Customer State
-- Answers: Where are our top markets located, and where is freight heaviest?
-- ------------------------------------------------------------------------------
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight_per_item,
    ROUND(100.0 * SUM(oi.price) / (SELECT SUM(price) FROM order_items), 2) AS state_revenue_pct
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


-- ------------------------------------------------------------------------------
-- 5. Payment Instrument Popularity & Installment Behavior
-- Answers: What payment methods do Brazilian consumers prefer, and what is the
-- average number of installments per method?
-- ------------------------------------------------------------------------------
SELECT 
    payment_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_installments), 1) AS avg_installments,
    ROUND(100.0 * SUM(payment_value) / (SELECT SUM(payment_value) FROM order_payments), 2) AS payment_value_share_pct
FROM order_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;
