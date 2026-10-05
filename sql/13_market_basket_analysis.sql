-- ==============================================================================
-- CommerceIQ — Advanced Analytics: Market Basket Analysis & Association Rules
-- File: sql/13_market_basket_analysis.sql
-- Run via: python3 run_query.py sql/13_market_basket_analysis.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Market Basket Analysis: Category Co-occurrence & Cross-Sell Affinity
--
-- Objective:
-- Uncover product categories frequently purchased together in the same order
-- to power merchandising recommendations and cross-selling bundles.
--
-- Statistical Metrics:
-- 1. Pair Order Count: Number of orders containing both Item A and Item B.
-- 2. Support: P(A ∩ B) = Pair orders / Total orders.
-- 3. Confidence: P(B | A) = Pair orders / Orders with Item A.
-- 4. Lift: P(A ∩ B) / (P(A) * P(B)). A lift > 1.0 indicates a true complementary
--    relationship beyond random chance.
-- ------------------------------------------------------------------------------

WITH order_categories AS (
    SELECT DISTINCT 
        oi.order_id,
        COALESCE(c.category_name_english, p.category_name, 'unknown') AS category
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_categories c ON p.category_name = c.category_name
),
category_frequency AS (
    SELECT 
        category,
        COUNT(DISTINCT order_id) AS single_category_orders
    FROM order_categories
    GROUP BY category
),
total_order_base AS (
    SELECT COUNT(DISTINCT order_id) AS total_orders FROM order_categories
),
category_pairs AS (
    SELECT 
        c1.category AS item_a,
        c2.category AS item_b,
        COUNT(DISTINCT c1.order_id) AS pair_order_count
    FROM order_categories c1
    JOIN order_categories c2 
      ON c1.order_id = c2.order_id 
     AND c1.category < c2.category -- Avoid self-pairs and duplicates (A,B vs B,A)
    GROUP BY c1.category, c2.category
    HAVING COUNT(DISTINCT c1.order_id) >= 10
)
SELECT 
    p.item_a,
    p.item_b,
    p.pair_order_count,
    ROUND(100.0 * p.pair_order_count / t.total_orders, 3) AS support_pct,
    ROUND(100.0 * p.pair_order_count / f1.single_category_orders, 2) AS confidence_a_to_b_pct,
    ROUND(
        (CAST(p.pair_order_count AS REAL) / t.total_orders) / 
        ((CAST(f1.single_category_orders AS REAL) / t.total_orders) * (CAST(f2.single_category_orders AS REAL) / t.total_orders)),
        2
    ) AS lift
FROM category_pairs p
CROSS JOIN total_order_base t
JOIN category_frequency f1 ON p.item_a = f1.category
JOIN category_frequency f2 ON p.item_b = f2.category
ORDER BY p.pair_order_count DESC
LIMIT 15;
