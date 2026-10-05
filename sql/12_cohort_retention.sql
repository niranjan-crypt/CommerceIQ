-- ==============================================================================
-- CommerceIQ — Advanced Analytics: Customer Cohort Retention Matrix
-- File: sql/12_cohort_retention.sql
-- Run via: python3 run_query.py sql/12_cohort_retention.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Monthly Customer Cohort Retention Analysis
--
-- Objective:
-- Track customer cohorts acquired in each calendar month and measure what
-- percentage return to make subsequent purchases in Month 1, 2, 3... 12.
--
-- Technical Mechanics:
-- 1. Acquisition Cohort: MIN(order_purchase_timestamp) per customer_unique_id.
-- 2. Activity Months: Distinct calendar months of subsequent purchases.
-- 3. Temporal Offset: (Year_diff * 12) + Month_diff gives exact Month index (0, 1, 2...).
-- 4. Retention Rate: (Active Customers in Month N / Initial Cohort Size) * 100.
-- ------------------------------------------------------------------------------

WITH customer_first_order AS (
    SELECT 
        c.customer_unique_id,
        MIN(strftime('%Y-%m-01', o.order_purchase_timestamp)) AS cohort_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
customer_orders AS (
    SELECT 
        c.customer_unique_id,
        strftime('%Y-%m-01', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1, 2
),
cohort_size AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_unique_id) AS total_cohort_customers
    FROM customer_first_order
    GROUP BY cohort_month
),
cohort_activities AS (
    SELECT 
        f.cohort_month,
        (CAST(strftime('%Y', o.order_month) AS INTEGER) - CAST(strftime('%Y', f.cohort_month) AS INTEGER)) * 12 +
        (CAST(strftime('%m', o.order_month) AS INTEGER) - CAST(strftime('%m', f.cohort_month) AS INTEGER)) AS month_offset,
        COUNT(DISTINCT o.customer_unique_id) AS active_customers
    FROM customer_first_order f
    JOIN customer_orders o ON f.customer_unique_id = o.customer_unique_id
    GROUP BY 1, 2
)
SELECT 
    a.cohort_month,
    s.total_cohort_customers AS cohort_size,
    a.month_offset,
    a.active_customers,
    ROUND(100.0 * a.active_customers / s.total_cohort_customers, 2) AS retention_rate_pct
FROM cohort_activities a
JOIN cohort_size s ON a.cohort_month = s.cohort_month
WHERE a.cohort_month BETWEEN '2017-01-01' AND '2017-12-01'
  AND a.month_offset <= 6
ORDER BY a.cohort_month, a.month_offset;
