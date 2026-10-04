-- ==============================================================================
-- CommerceIQ — Day 12: Operations, Logistics & Customer Satisfaction Analytics
-- File: sql/09_operations_analytics.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Delivery Performance vs Customer Satisfaction (Review Scores)
-- Question: Does delivery delay directly degrade customer review ratings?
-- Findings: On-time delivery yields a 4.29/5 rating; late delivery collapses 
-- ratings to 2.57/5, with 1-star complaints skyrocketing from 6.6% to 46.2%!
-- ------------------------------------------------------------------------------
WITH order_logistics AS (
    SELECT 
        o.order_id,
        julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS actual_delivery_days,
        julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) AS delay_days,
        CASE 
            WHEN julianday(o.order_delivered_customer_date) > julianday(o.order_estimated_delivery_date) THEN 'Late Delivery'
            ELSE 'On-Time / Early'
        END AS delivery_performance,
        r.review_score
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered' 
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_estimated_delivery_date IS NOT NULL
)
SELECT 
    delivery_performance,
    COUNT(*) AS total_orders,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM order_logistics), 2) AS pct_of_orders,
    ROUND(AVG(actual_delivery_days), 1) AS avg_delivery_days,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    SUM(CASE WHEN review_score = 5 THEN 1 ELSE 0 END) AS five_star_reviews,
    SUM(CASE WHEN review_score = 1 THEN 1 ELSE 0 END) AS one_star_reviews,
    ROUND(100.0 * SUM(CASE WHEN review_score = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS one_star_rate_pct
FROM order_logistics
GROUP BY delivery_performance;


-- ------------------------------------------------------------------------------
-- 2. Seller Dispatch SLA Adherence
-- Question: Which sellers frequently miss shipping deadlines to carriers?
-- ------------------------------------------------------------------------------
WITH seller_shipping AS (
    SELECT 
        oi.seller_id,
        COUNT(oi.order_item_id) AS items_sold,
        SUM(CASE 
            WHEN julianday(o.order_delivered_carrier_date) > julianday(oi.shipping_limit_date) THEN 1 
            ELSE 0 
        END) AS late_carrier_dispatches
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_delivered_carrier_date IS NOT NULL
    GROUP BY oi.seller_id
    HAVING COUNT(oi.order_item_id) >= 20
)
SELECT 
    s.seller_id,
    s.seller_city,
    s.seller_state,
    ss.items_sold,
    ss.late_carrier_dispatches,
    ROUND(100.0 * ss.late_carrier_dispatches / ss.items_sold, 2) AS carrier_delay_rate_pct
FROM seller_shipping ss
JOIN sellers s ON ss.seller_id = s.seller_id
ORDER BY carrier_delay_rate_pct DESC
LIMIT 15;


-- ------------------------------------------------------------------------------
-- 3. Interstate Freight Economics & Route Latency
-- Question: What are the transit durations and freight costs from Seller State 
-- to Customer State?
-- ------------------------------------------------------------------------------
SELECT 
    s.seller_state,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS order_volume,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_transit_days,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY s.seller_state, c.customer_state
HAVING COUNT(DISTINCT o.order_id) >= 500
ORDER BY order_volume DESC
LIMIT 10;
