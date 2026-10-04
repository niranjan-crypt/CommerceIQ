-- ==============================================================================
-- CommerceIQ — Day 11: Customer Analytics & RFM Segmentation
-- File: sql/07_customer_analytics.sql
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- RFM (Recency, Frequency, Monetary) Customer Segmentation Model
--
-- Technical Rationale:
-- 1. Reference Anchor: E-commerce datasets have a historical cutoff date.
--    Instead of using CURRENT_DATE (which would artificially make all customers 
--    dormant by several years), we anchor to MAX(order_purchase_timestamp).
-- 2. Granularity: Grouped strictly by `customer_unique_id` to aggregate 
--    cross-order transactions of the same human consumer.
-- 3. NTILE() Scoring: Divides customers into quintiles (1-5) across Recency,
--    Frequency, and Monetary dimensions.
-- ------------------------------------------------------------------------------

WITH reference_date AS (
    SELECT MAX(order_purchase_timestamp) AS max_purchase_date 
    FROM orders
),
customer_rfm_raw AS (
    SELECT 
        c.customer_unique_id,
        ROUND(
            julianday((SELECT max_purchase_date FROM reference_date)) - 
            julianday(MAX(o.order_purchase_timestamp)), 
            0
        ) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.price), 2) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
rfm_scores AS (
    SELECT 
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        -- Higher score (5) = More recent purchase (lower recency days)
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Discrete distribution for frequency due to low repeat rate in marketplace
        CASE 
            WHEN frequency >= 3 THEN 5
            WHEN frequency = 2 THEN 4
            ELSE 1
        END AS f_score,
        -- Higher score (5) = Higher spend
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM customer_rfm_raw
),
rfm_segmented AS (
    SELECT 
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        CASE 
            WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
            WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score < 4 AND m_score >= 4 THEN 'Potential Loyalists'
            WHEN r_score >= 3 AND f_score = 1 THEN 'Recent Customers'
            WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk Customers'
            WHEN r_score <= 2 AND monetary >= 200 THEN 'Lost High-Spenders'
            ELSE 'Standard Hibernating'
        END AS customer_segment
    FROM rfm_scores
)
-- Segment Performance Aggregation
SELECT 
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 2) AS avg_orders,
    ROUND(AVG(monetary), 2) AS avg_spend,
    ROUND(SUM(monetary), 2) AS segment_total_spend,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_rfm_raw), 2) AS pct_of_customer_base,
    ROUND(100.0 * SUM(monetary) / (SELECT SUM(monetary) FROM customer_rfm_raw), 2) AS pct_of_total_revenue
FROM rfm_segmented
GROUP BY customer_segment
ORDER BY segment_total_spend DESC;
