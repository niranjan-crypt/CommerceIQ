-- ==============================================================================
-- CommerceIQ — Day 12: Product & Merchandising Analytics
-- File: sql/08_product_analytics.sql
-- Run via: python3 run_query.py sql/08_product_analytics.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Product Pareto (80/20) Revenue Concentration
-- Analyzes what percentage of total products generate 80% of platform revenue.
-- ------------------------------------------------------------------------------
WITH product_revenue_ranked AS (
    SELECT 
        product_id,
        ROUND(SUM(price), 2) AS product_revenue,
        SUM(SUM(price)) OVER (ORDER BY SUM(price) DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue,
        SUM(SUM(price)) OVER () AS total_platform_revenue
    FROM order_items
    GROUP BY product_id
)
SELECT 
    product_id,
    product_revenue,
    ROUND(running_revenue, 2) AS running_revenue,
    ROUND(100.0 * running_revenue / total_platform_revenue, 2) AS cumulative_revenue_pct
FROM product_revenue_ranked
ORDER BY product_revenue DESC
LIMIT 15;


-- ------------------------------------------------------------------------------
-- 2. Heavy vs. Light Freight Economics
-- Evaluates freight-to-price ratio across different product weight classes.
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN p.product_weight_g >= 10000 THEN 'Very Heavy (>10kg)'
        WHEN p.product_weight_g >= 5000  THEN 'Heavy (5-10kg)'
        WHEN p.product_weight_g >= 1000  THEN 'Medium (1-5kg)'
        ELSE 'Light (<1kg)'
    END AS weight_tier,
    COUNT(oi.order_item_id) AS items_sold,
    ROUND(AVG(oi.price), 2) AS avg_item_price,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight,
    ROUND(100.0 * AVG(oi.freight_value) / AVG(oi.price), 2) AS freight_to_price_ratio_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE p.product_weight_g IS NOT NULL
GROUP BY 1
ORDER BY avg_freight DESC;
