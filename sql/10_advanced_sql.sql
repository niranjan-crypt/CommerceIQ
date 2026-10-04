-- ==============================================================================
-- CommerceIQ — Day 10: Advanced SQL & Analytical Window Functions
-- File: sql/10_advanced_sql.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Month-over-Month (MoM) Growth Analysis with LAG()
-- Demonstrates: CTEs, LAG() window function, growth rate calculation.
-- Interview concept: LAG() accesses data from a previous row in the same result
-- set without requiring a self-join.
-- ------------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) AS sale_month,
        ROUND(SUM(oi.price), 2) AS monthly_revenue,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
),
mom_comparison AS (
    SELECT 
        sale_month,
        monthly_revenue,
        total_orders,
        LAG(monthly_revenue, 1) OVER (ORDER BY sale_month) AS prev_month_revenue,
        LAG(total_orders, 1) OVER (ORDER BY sale_month) AS prev_month_orders
    FROM monthly_sales
)
SELECT 
    sale_month,
    monthly_revenue,
    COALESCE(prev_month_revenue, 0) AS prev_month_revenue,
    ROUND(
        100.0 * (monthly_revenue - prev_month_revenue) / prev_month_revenue, 
        2
    ) AS mom_revenue_growth_pct,
    total_orders,
    ROUND(
        100.0 * (total_orders - prev_month_orders) / prev_month_orders, 
        2
    ) AS mom_orders_growth_pct
FROM mom_comparison
WHERE sale_month >= '2017-01'
ORDER BY sale_month;


-- ------------------------------------------------------------------------------
-- 2. Cumulative Running Totals with SUM() OVER (ORDER BY ...)
-- Demonstrates: Window frame specification (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW).
-- ------------------------------------------------------------------------------
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) AS sale_month,
        COUNT(DISTINCT o.order_id) AS monthly_orders,
        ROUND(SUM(oi.price), 2) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    sale_month,
    monthly_orders,
    monthly_revenue,
    ROUND(SUM(monthly_revenue) OVER (
        ORDER BY sale_month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_cumulative_revenue,
    SUM(monthly_orders) OVER (
        ORDER BY sale_month 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_cumulative_orders
FROM monthly_revenue
WHERE sale_month >= '2017-01'
ORDER BY sale_month;


-- ------------------------------------------------------------------------------
-- 3. Top 3 Products per Category using DENSE_RANK() OVER (PARTITION BY ...)
-- Demonstrates: PARTITION BY for grouped rankings; DENSE_RANK vs RANK vs ROW_NUMBER.
-- Interview concept: 
-- - ROW_NUMBER(): unique sequential integer (1, 2, 3, 4) - arbitrarily breaks ties.
-- - RANK(): leaves gaps on ties (1, 2, 2, 4).
-- - DENSE_RANK(): consecutive ranking without gaps on ties (1, 2, 2, 3).
-- ------------------------------------------------------------------------------
WITH product_revenue AS (
    SELECT 
        COALESCE(c.category_name_english, p.category_name, 'Unknown') AS category,
        p.product_id,
        COUNT(oi.order_item_id) AS units_sold,
        ROUND(SUM(oi.price), 2) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_categories c ON p.category_name = c.category_name
    GROUP BY 1, 2
),
ranked_products AS (
    SELECT 
        category,
        product_id,
        units_sold,
        total_revenue,
        DENSE_RANK() OVER (
            PARTITION BY category 
            ORDER BY total_revenue DESC
        ) AS rank_in_category
    FROM product_revenue
)
SELECT 
    category,
    rank_in_category,
    product_id,
    units_sold,
    total_revenue
FROM ranked_products
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;


-- ------------------------------------------------------------------------------
-- 4. Customer Purchase Interval (Days Between Consecutive Purchases)
-- Demonstrates: Multi-level windowing, TIMESTAMP difference calculation.
-- ------------------------------------------------------------------------------
WITH customer_orders_ordered AS (
    SELECT 
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        LAG(o.order_purchase_timestamp) OVER (
            PARTITION BY c.customer_unique_id 
            ORDER BY o.order_purchase_timestamp
        ) AS prev_order_timestamp
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
)
SELECT 
    customer_unique_id,
    order_id,
    order_purchase_timestamp,
    prev_order_timestamp,
    ROUND(
        julianday(order_purchase_timestamp) - julianday(prev_order_timestamp), 
        1
    ) AS days_since_last_purchase
FROM customer_orders_ordered
WHERE prev_order_timestamp IS NOT NULL
ORDER BY days_since_last_purchase ASC
LIMIT 15;
