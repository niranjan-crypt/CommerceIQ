"""
CommerceIQ — Executive & Operational Business Intelligence Dashboard
Streamlit Web Application querying the CommerceIQ database.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="CommerceIQ | E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "olist_oltp.db"))

@st.cache_data(ttl=3600)
def run_query(sql_query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    finally:
        conn.close()

# Sidebar Navigation
st.sidebar.title("🛍️ CommerceIQ")
st.sidebar.caption("Data Engineering & Customer Analytics Platform")

page = st.sidebar.radio(
    "Select Intelligence View:",
    [
        "1. Executive Overview",
        "2. Customer Intelligence & RFM",
        "3. Product Intelligence",
        "4. Operations & Logistics",
        "5. Interactive SQL Lab"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Database Engine**: Relational OLTP / Analytical Mart")
st.sidebar.markdown("**Scale**: 100,000+ Orders | 1.5M Records")

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if page == "1. Executive Overview":
    st.title("📊 Executive Performance Overview")
    st.markdown("Top-line operational and financial metrics across the Brazilian e-commerce marketplace.")

    kpi_query = """
    SELECT 
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT c.customer_unique_id) AS total_customers,
        ROUND(SUM(oi.price), 2) AS total_revenue,
        ROUND(SUM(oi.price + oi.freight_value), 2) AS gmv,
        ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS aov,
        ROUND(AVG(r.review_score), 2) AS avg_rating
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered';
    """
    df_kpi = run_query(kpi_query)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Gross Merchandise Value", f"R$ {df_kpi['gmv'].iloc[0]:,.2f}")
    col2.metric("Delivered Orders", f"{df_kpi['total_orders'].iloc[0]:,}")
    col3.metric("Unique Customers", f"{df_kpi['total_customers'].iloc[0]:,}")
    col4.metric("Average Order Value (AOV)", f"R$ {df_kpi['aov'].iloc[0]:,.2f}")
    col5.metric("Platform Avg Rating", f"⭐ {df_kpi['avg_rating'].iloc[0]}")

    st.markdown("---")
    c1, c2 = st.columns([3, 2])

    with c1:
        st.subheader("Monthly Revenue Growth")
        monthly_query = """
        SELECT 
            strftime('%Y-%m', o.order_purchase_timestamp) AS month,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered' AND month >= '2017-01'
        GROUP BY 1
        ORDER BY 1;
        """
        df_monthly = run_query(monthly_query)
        st.bar_chart(data=df_monthly.set_index("month")["revenue"], use_container_width=True)

    with c2:
        st.subheader("Geographic Revenue (Top 5 States)")
        geo_query = """
        SELECT 
            c.customer_state AS state,
            ROUND(SUM(oi.price), 2) AS revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 5;
        """
        df_geo = run_query(geo_query)
        st.dataframe(df_geo, use_container_width=True, hide_index=True)

# ==============================================================================
# PAGE 2: CUSTOMER INTELLIGENCE & RFM
# ==============================================================================
elif page == "2. Customer Intelligence & RFM":
    st.title("🎯 Customer Intelligence & RFM Segmentation")
    st.markdown("Behavioral customer segmentation based on **Recency**, **Frequency**, and **Monetary** scoring.")

    rfm_query = """
    WITH reference_date AS (
        SELECT MAX(order_purchase_timestamp) AS max_purchase_date FROM orders
    ),
    customer_rfm_raw AS (
        SELECT 
            c.customer_unique_id,
            ROUND(julianday((SELECT max_purchase_date FROM reference_date)) - julianday(MAX(o.order_purchase_timestamp)), 0) AS recency_days,
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
            NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
            CASE WHEN frequency >= 3 THEN 5 WHEN frequency = 2 THEN 4 ELSE 1 END AS f_score,
            NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
        FROM customer_rfm_raw
    ),
    rfm_segmented AS (
        SELECT 
            customer_unique_id,
            recency_days,
            frequency,
            monetary,
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
    SELECT 
        customer_segment,
        COUNT(*) AS total_customers,
        ROUND(AVG(recency_days), 1) AS avg_recency_days,
        ROUND(AVG(frequency), 2) AS avg_orders,
        ROUND(AVG(monetary), 2) AS avg_spend,
        ROUND(SUM(monetary), 2) AS segment_revenue
    FROM rfm_segmented
    GROUP BY customer_segment
    ORDER BY segment_revenue DESC;
    """
    df_rfm = run_query(rfm_query)

    st.dataframe(df_rfm, use_container_width=True, hide_index=True)
    st.bar_chart(data=df_rfm.set_index("customer_segment")["segment_revenue"], use_container_width=True)

# ==============================================================================
# PAGE 3: PRODUCT INTELLIGENCE
# ==============================================================================
elif page == "3. Product Intelligence":
    st.title("📦 Product & Merchandising Intelligence")
    st.markdown("Category revenue concentration, product ratings, and unit velocity.")

    cat_query = """
    SELECT 
        COALESCE(cat.category_name_english, p.category_name, 'Unknown') AS product_category,
        COUNT(DISTINCT oi.order_id) AS total_orders,
        COUNT(oi.order_item_id) AS units_sold,
        ROUND(SUM(oi.price), 2) AS total_revenue,
        ROUND(AVG(r.review_score), 2) AS avg_rating
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_categories cat ON p.category_name = cat.category_name
    LEFT JOIN order_reviews r ON oi.order_id = r.order_id
    GROUP BY 1
    ORDER BY total_revenue DESC
    LIMIT 15;
    """
    df_cat = run_query(cat_query)
    st.dataframe(df_cat, use_container_width=True, hide_index=True)

# ==============================================================================
# PAGE 4: OPERATIONS & LOGISTICS
# ==============================================================================
elif page == "4. Operations & Logistics":
    st.title("🚚 Operations, Fulfillment & SLA Analysis")
    st.markdown("Correlation between delivery delays and customer review scores.")

    delay_query = """
    WITH order_logistics AS (
        SELECT 
            o.order_id,
            julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS actual_delivery_days,
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
        ROUND(AVG(actual_delivery_days), 1) AS avg_delivery_days,
        ROUND(AVG(review_score), 2) AS avg_review_score,
        ROUND(100.0 * SUM(CASE WHEN review_score = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS one_star_rate_pct
    FROM order_logistics
    GROUP BY delivery_performance;
    """
    df_delay = run_query(delay_query)
    st.table(df_delay)

# ==============================================================================
# PAGE 5: INTERACTIVE SQL LAB
# ==============================================================================
elif page == "5. Interactive SQL Lab":
    st.title("⚡ Interactive SQL Analytics Lab")
    st.markdown("Execute ad-hoc analytical queries directly against the production database.")

    default_sql = """-- MoM Revenue Growth with LAG() Window Function
WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) AS sale_month,
        ROUND(SUM(oi.price), 2) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    sale_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY sale_month) AS prev_month_revenue,
    ROUND(100.0 * (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sale_month)) / LAG(monthly_revenue, 1) OVER (ORDER BY sale_month), 2) AS mom_growth_pct
FROM monthly_sales
WHERE sale_month >= '2017-01'
ORDER BY sale_month;"""

    user_sql = st.text_area("SQL Query Editor", default_sql, height=220)
    if st.button("Execute Query", type="primary"):
        try:
            res_df = run_query(user_sql)
            st.success(f"Returned {len(res_df)} rows")
            st.dataframe(res_df, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
