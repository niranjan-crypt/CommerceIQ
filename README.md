<div align="center">

# 🛍️ CommerceIQ
### End-to-End E-Commerce Data Engineering & Customer Analytics Platform
*A production-grade transactional and analytical data platform processing 100,000+ orders across 1.5M records.*

[![CI/CD](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen.svg)](ci/github-actions-ci.yml)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20%7C%20Window%20Functions-blue.svg)](sql/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2016%20%7C%20SQLite-336791.svg)](sql/02_tables.sql)
[![Docker](https://img.shields.io/badge/Docker-Multi--Container%20Compose-2496ED.svg)](docker-compose.yml)
[![Data Quality](https://img.shields.io/badge/Data%20Quality-22%2F22%20Passed-brightgreen.svg)](data/validation/data_quality_report.md)
[![Query Tuning](https://img.shields.io/badge/Query%20Optimization-5.35x%20Faster-orange.svg)](docs/optimization_study.md)
[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB.svg)](python/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit%20%7C%20Plotly-FF4B4B.svg)](dashboard/app.py)

[Platform Architecture](#-system-architecture) •
[Executive Findings](#-executive-findings--business-impact) •
[Data Quality Gates](#-automated-data-quality-engine) •
[SQL Deep-Dive](#-advanced-sql-engineering-highlights) •
[Query Tuning](#-empirical-query-optimization-benchmark) •
[Docker Deployment](#-quickstart-guide) •
[Interview Defense](#-technical-interview-defense-cheat-sheet)

</div>

---

## 📖 Executive Narrative: The Business Problem

In high-growth e-commerce marketplaces, raw transactional logs are messy, distributed, and disconnected from business strategy. **CommerceIQ** solves the full lifecycle challenge of **Olist** (Brazil’s largest department store marketplace aggregator), transforming **100,000+ fragmented orders** into an enterprise-grade decision engine.

Unlike superficial toy projects that read raw CSVs into a single Pandas notebook, CommerceIQ models the complete enterprise lifecycle:
1. **Raw Ingestion & Type Cleansing**: Automated normalization, timezone parsing, and translation remediation.
2. **Automated Data Quality Gating**: A 22-test automated firewall ensuring zero foreign key orphans and mathematical domain validity.
3. **Normalized 3NF Transactional Layer (OLTP)**: 9 relational tables enforcing ACID guarantees, strict PK/FK cascades, and domain constraints.
4. **Kimball Star Schema Data Warehouse (OLAP)**: Fact tables (`fact_orders`, `fact_order_items`) and conformed dimensions (`dim_customer`, `dim_product`, `dim_seller`, `dim_date`) built for sub-second analytical aggregations.
5. **Advanced SQL Intelligence Engine**: Monthly triangular cohort retention matrices, SQL-native RFM customer segmentation, and Market Basket cross-sell affinity mining.
6. **Empirical Performance Engineering**: `EXPLAIN` query plan profiling, eliminating full-table sequential scans via targeted B-Trees (**5.35x measured speedup**).
7. **Interactive Streamlit BI Platform**: Plotly geospatial maps of Brazil, customer retention heatmaps, and a live ad-hoc SQL sandbox with one-click CSV export.

---

## 🏗️ System Architecture & Data Lineage

```mermaid
flowchart TD
    subgraph Raw["1. Raw Ingestion Layer (Olist Data Lake)"]
        CSV["9 Raw CSV Datasets<br/>(100k Orders | 1.5M Records)"]
    end

    subgraph ETL["2. Python Data Engineering Pipeline"]
        CLEAN["python/data_cleaning.py<br/>(Datetime parsing, null handling, category normalization)"]
        DQ["python/data_validation.py<br/>(22 Automated Data Quality Gates)"]
        LOAD["python/database_loader.py<br/>(Topological Ingestion & Batch Loading)"]
    end

    subgraph OLTP["3. Relational OLTP Layer (PostgreSQL - 3NF)"]
        T_CUST["customers (PK: customer_id)"]
        T_ORD["orders (PK: order_id)"]
        T_ITEM["order_items (PK: order_id, order_item_id)"]
        T_PAY["order_payments (PK: order_id, payment_seq)"]
        T_REV["order_reviews (PK: review_id, order_id)"]
        T_PROD["products & product_categories"]
        T_SELL["sellers & geolocation"]
    end

    subgraph OLAP["4. Analytical Data Warehouse (Kimball Star Schema)"]
        FACT_O[("fact_orders")]
        FACT_I[("fact_order_items")]
        DIM_C[("dim_customer")]
        DIM_P[("dim_product")]
        DIM_S[("dim_seller")]
        DIM_D[("dim_date")]
    end

    subgraph SQL["5. Advanced SQL Intelligence Models"]
        M1["RFM Customer Segmentation (NTILE)"]
        M2["Monthly Cohort Retention Matrix"]
        M3["Market Basket Affinity (Support, Confidence, Lift)"]
        M4["Logistics Delay vs CSAT Review Collapse"]
    end

    subgraph BI["6. Presentation & BI Web Layer"]
        DASH["Streamlit Interactive BI Dashboard<br/>(Plotly Area Charts, Brazil Map, Cohort Heatmap, SQL Sandbox)"]
    end

    Raw --> CLEAN --> DQ --> LOAD --> OLTP --> OLAP --> SQL --> BI
```

*(Full architectural and ER diagram documentation available in [`docs/architecture_and_er_diagram.md`](docs/architecture_and_er_diagram.md))*

---

## 📊 Executive Findings & Business Impact

Every metric below was calculated via SQL executed directly against the live database:

| Business Dimension | Measured Empirical Finding | Strategic Operational Impact |
| :--- | :--- | :--- |
| **Gross Merchandise Value (GMV)** | **R$ 15,419,773.75** | Total financial volume delivered across 96,478 verified transactions. |
| **Average Order Value (AOV)** | **R$ 137.04** | Stable across weekdays (R$ 137.95) and weekends (R$ 135.20). |
| **The Repeat Buyer Dilemma** | **3.0% Repeat Purchase Rate** | 2,801 customers made $>1$ purchase, but generated **R$ 1.58M in GMV** with an AOV of R$ 260.95 (nearly 2x the platform average). |
| **The Delivery "Death Spiral"** | **On-Time Rating: ⭐ 4.29 / 5.0**<br>**Late Delivery: ⭐ 2.57 / 5.0** | Late deliveries (7.99% of volume) average 31.4 days in transit, causing **1-star complaints to skyrocket from 6.6% to 46.2%**. Carrier dispatch delays by sellers cause 68% of these bottlenecks. |
| **Financing Habits** | **78.34% Paid via Credit Card** | Average of 3.5 installments per transaction. Boleto bancário accounts for 17.92% of sales but introduces a 2-day cash reconciliation lag. |
| **Product Cross-Sell Affinity** | **Lift = 1.13 (`bed_bath_table` + `home_confort`)** | Proves customers buying bedding are 13% more likely to buy home comfort items, unlocking dynamic cross-sell bundles at checkout. |

*(Read the full strategic whitepaper in [`docs/business_insights.md`](docs/business_insights.md))*

---

## 🛡️ Automated Data Quality Engine

Data integrity is guaranteed before any record reaches storage via an automated 22-test validation engine ([`python/data_validation.py`](python/data_validation.py)):

<div align="center">

| Validation Category | Rules Evaluated | Test Status | Violations Found |
| :--- | :---: | :---: | :---: |
| **Primary Key Uniqueness** | 9 Core Tables | ✅ **PASSED** | 0 / 1,500,000+ records |
| **Referential Integrity (Foreign Keys)** | 7 Entity Relationships | ✅ **PASSED** | 0 orphan records |
| **Numeric & Financial Bounds** | Prices, Freight, Payments $\ge 0.00$ | ✅ **PASSED** | 0 negative values |
| **Domain Constraints** | Review Scores $\in [1, 5]$ | ✅ **PASSED** | 0 out-of-bounds scores |
| **Chronological Causality** | Delivered Date $\ge$ Purchase Timestamp | ✅ **PASSED** | 0 chronological violations |
| **Categorical Domains** | Valid Order Status & Payment Types | ✅ **PASSED** | 0 invalid enums |

</div>

*(Full automated audit log available in [`data/validation/data_quality_report.md`](data/validation/data_quality_report.md))*

---

## ⚡ Empirical Query Optimization Benchmark

In real enterprise systems, slow queries bring down web apps and exhaust database buffer pools. We profiled and tuned a typical business reporting query joining `orders` and `order_items` across June 2017:

```sql
SELECT o.order_id, o.order_status, oi.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp BETWEEN '2017-06-01' AND '2017-06-30'
  AND oi.price > 100.00;
```

### The Query Plan Comparison (`EXPLAIN QUERY PLAN`):

```text
BEFORE (Sequential Scan Bottleneck):
├── SCAN oi                                   <-- Full table scan of 112,650 order item rows
└── SEARCH o USING INDEX (order_id=?)         <-- PK lookup for each item
⏱️ Average Latency: 86.82 ms

AFTER (Targeted B-Tree Index Deployment):
CREATE INDEX idx_orders_purchase_timestamp ON orders(order_purchase_timestamp);

├── SEARCH o USING INDEX idx_orders_purchase_timestamp (timestamp BETWEEN ?) <-- O(log N) B-Tree scan
└── SEARCH oi USING INDEX (order_id=?)        <-- Fast PK item retrieval
⚡ Average Latency: 16.24 ms
🚀 Measured Performance Gain: 5.35x Speedup (81.3% Latency Reduction)
```

*(Complete optimization study with B-Tree mechanics available in [`docs/optimization_study.md`](docs/optimization_study.md))*

---

## 💡 Advanced SQL Engineering Highlights

<details>
<summary><b>🔍 1. Triangular Customer Cohort Retention Matrix (Click to expand)</b></summary>

```sql
-- File: sql/12_cohort_retention.sql
WITH customer_first_order AS (
    SELECT c.customer_unique_id, MIN(strftime('%Y-%m-01', o.order_purchase_timestamp)) AS cohort_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
customer_orders AS (
    SELECT c.customer_unique_id, strftime('%Y-%m-01', o.order_purchase_timestamp) AS order_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1, 2
),
cohort_activities AS (
    SELECT 
        f.cohort_month,
        (CAST(strftime('%Y', o.order_month) AS INT) - CAST(strftime('%Y', f.cohort_month) AS INT)) * 12 +
        (CAST(strftime('%m', o.order_month) AS INT) - CAST(strftime('%m', f.cohort_month) AS INT)) AS month_offset,
        COUNT(DISTINCT o.customer_unique_id) AS active_customers
    FROM customer_first_order f
    JOIN customer_orders o ON f.customer_unique_id = o.customer_unique_id
    GROUP BY 1, 2
)
SELECT a.cohort_month, a.month_offset, ROUND(100.0 * a.active_customers / s.total_cohort_customers, 2) AS retention_rate_pct
FROM cohort_activities a
JOIN (SELECT cohort_month, COUNT(*) AS total_cohort_customers FROM customer_first_order GROUP BY 1) s
  ON a.cohort_month = s.cohort_month
ORDER BY a.cohort_month, a.month_offset;
```
</details>

<details>
<summary><b>🛒 2. Market Basket Co-Occurrence & Cross-Sell Lift (Click to expand)</b></summary>

```sql
-- File: sql/13_market_basket_analysis.sql
WITH order_categories AS (
    SELECT DISTINCT oi.order_id, COALESCE(c.category_name_english, p.category_name, 'unknown') AS category
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN product_categories c ON p.category_name = c.category_name
),
category_pairs AS (
    SELECT c1.category AS item_a, c2.category AS item_b, COUNT(DISTINCT c1.order_id) AS pair_order_count
    FROM order_categories c1
    JOIN order_categories c2 ON c1.order_id = c2.order_id AND c1.category < c2.category
    GROUP BY c1.category, c2.category
    HAVING COUNT(DISTINCT c1.order_id) >= 10
)
SELECT 
    p.item_a, p.item_b, p.pair_order_count,
    ROUND(100.0 * p.pair_order_count / t.total_orders, 3) AS support_pct,
    ROUND(100.0 * p.pair_order_count / f1.single_orders, 2) AS confidence_pct,
    ROUND((CAST(p.pair_order_count AS REAL) / t.total_orders) / 
          ((CAST(f1.single_orders AS REAL) / t.total_orders) * (CAST(f2.single_orders AS REAL) / t.total_orders)), 2) AS lift
FROM category_pairs p
CROSS JOIN (SELECT COUNT(DISTINCT order_id) AS total_orders FROM order_categories) t
JOIN (SELECT category, COUNT(DISTINCT order_id) AS single_orders FROM order_categories GROUP BY 1) f1 ON p.item_a = f1.category
JOIN (SELECT category, COUNT(DISTINCT order_id) AS single_orders FROM order_categories GROUP BY 1) f2 ON p.item_b = f2.category
ORDER BY p.pair_order_count DESC;
```
</details>

<details>
<summary><b>📈 3. Month-over-Month Revenue Growth with LAG() (Click to expand)</b></summary>

```sql
-- File: sql/10_advanced_sql.sql
WITH monthly_sales AS (
    SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS sale_month, ROUND(SUM(oi.price), 2) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
)
SELECT 
    sale_month,
    monthly_revenue,
    LAG(monthly_revenue, 1) OVER (ORDER BY sale_month) AS prev_month_revenue,
    ROUND(100.0 * (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sale_month)) / 
          LAG(monthly_revenue, 1) OVER (ORDER BY sale_month), 2) AS mom_growth_pct
FROM monthly_sales
WHERE sale_month >= '2017-01'
ORDER BY sale_month;
```
</details>

---

## 🗄️ Project Repository Layout

```text
CommerceIQ/
├── data/
│   ├── raw/                  # 9 Raw Olist CSV datasets
│   ├── processed/            # Cleaned, type-normalized CSVs
│   ├── validation/           # Automated Data Quality audit reports
│   └── olist_oltp.db         # Populated relational database (15 tables)
├── sql/
│   ├── 01_database.sql       # Schemas, namespaces, enum domain types
│   ├── 02_tables.sql         # 3NF DDL (Primary keys, types, lengths)
│   ├── 03_constraints.sql    # Foreign keys, CHECK constraints, FK B-Tree indexes
│   ├── 04_data_quality.sql   # Pure SQL integrity and assertion checks
│   ├── 05_transformations.sql# Kimball Star Schema (fact_orders, conformed dims)
│   ├── 06_business_analytics.sql # Executive KPIs, AOV, Gross Merchandise Value
│   ├── 07_customer_analytics.sql # Pure SQL RFM segmentation with NTILE()
│   ├── 08_product_analytics.sql  # Pareto 80/20 analysis & freight weight tiers
│   ├── 09_operations_analytics.sql # Logistics latency vs review score correlation
│   ├── 10_advanced_sql.sql   # Window functions (LAG, DENSE_RANK, running totals)
│   ├── 11_optimization.sql   # EXPLAIN benchmark and targeted B-Tree indexing
│   ├── 12_cohort_retention.sql # Monthly Customer Cohort Retention Matrix
│   └── 13_market_basket_analysis.sql # Market Basket Analysis (Support, Confidence, Lift)
├── python/
│   ├── data_cleaning.py      # Automated ingestion and cleaning pipeline
│   ├── data_validation.py    # 22 automated data quality test suite
│   ├── database_loader.py    # Topological batch database ingestion with NULL handling
│   ├── exploratory_profiler.py # Schema and cardinality auditor
│   └── export_outputs.py     # Markdown query results exporter
├── dashboard/
│   └── app.py                # 5-Page Streamlit BI Web Platform (Plotly, Maps, Heatmaps)
├── docs/
│   ├── 01_dbms_relational_concepts.md # ACID, 1NF/2NF/3NF Normalization, OLTP vs OLAP
│   ├── architecture_and_er_diagram.md # Complete ERD and Kimball lineage diagrams
│   ├── business_insights.md  # Strategic C-suite executive whitepaper
│   ├── data_dictionary.md    # Full table & column specifications
│   └── optimization_study.md # EXPLAIN benchmark deep-dive (5.35x speedup)
├── outputs/                  # Exported query execution outputs (Markdown)
├── tests/
│   └── test_data_quality.py  # Automated regression test suite
├── ci/
│   └── github-actions-ci.yml # Automated CI/CD pipeline template
├── Dockerfile                # Multi-tier container image
├── docker-compose.yml        # PostgreSQL 16 + Streamlit container stack
├── requirements.txt          # Python dependencies
└── run_query.py              # Interactive CLI query runner & REPL
```

---

## 🚀 Quickstart Guide

### Option 1: Run with Docker Compose (One-Command Deployment)
```bash
docker compose up --build
```
*Spins up a local **PostgreSQL 16** server with all 3NF tables initialized, plus the **Streamlit BI Web Platform** at `http://localhost:8501`.*

### Option 2: Run Locally in Terminal / VS Code

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Launch interactive SQL shell with ASCII banner & millisecond timer
python3 run_query.py

# 3. Execute any SQL model directly
python3 run_query.py sql/06_business_analytics.sql
python3 run_query.py sql/07_customer_analytics.sql
python3 run_query.py sql/12_cohort_retention.sql
python3 run_query.py sql/13_market_basket_analysis.sql

# 4. Run automated test suite
python3 tests/test_data_quality.py

# 5. Launch visual Streamlit dashboard
streamlit run dashboard/app.py
```

---

## 💼 Resume-Ready Project Bullets

```markdown
CommerceIQ — E-Commerce Data Engineering & Customer Analytics Platform
Tech Stack: Python, SQL, PostgreSQL, Docker, Kimball Star Schema, Pandas, Streamlit, Git

• Architected an end-to-end data platform processing 100,000+ transactions across 9 relational entities; designed a 3NF normalized OLTP schema and converted it into an analytical Kimball Star Schema (fact_orders, fact_order_items, conformed dimensions).
• Developed an automated Data Quality Engine enforcing 22 pre-ingestion validation rules across 1.5M records, achieving 100% referential integrity, zero orphan records, and strict chronological causality.
• Formulated advanced analytical SQL models leveraging Window Functions (LAG, DENSE_RANK, cumulative running totals), triangular monthly cohort retention matrices, and SQL-native RFM customer segmentation (NTILE) to profile 93,000+ unique customers.
• Engineered a Market Basket Analysis model using analytical self-joins on multi-item orders, computing Support, Confidence, and Lift to discover high-affinity product cross-sell bundles (Lift = 1.13).
• Profiled and optimized complex join queries using EXPLAIN execution plans; eliminated full-table sequential scans by implementing targeted B-Tree indexes, achieving a verified 5.35x speedup (81.3% latency reduction).
• Built and containerized a multi-page interactive Streamlit Business Intelligence platform using Docker Compose and Plotly, featuring interactive geospatial maps of Brazil, customer retention heatmaps, and an embedded live SQL query sandbox with CSV export.
```

---

## 🎯 Technical Interview Defense Cheat Sheet

<details>
<summary><b>1. "Tell me about this project."</b></summary>

> *"CommerceIQ is an enterprise-grade data platform processing over 100,000 Brazilian e-commerce transactions across a 1.5-million-record database. Instead of treating this as a simple flat-file analysis, I modeled the complete enterprise data lifecycle: Python automated ETL with a 22-rule Data Quality firewall, a normalized 3NF transactional database, an analytical Kimball Star Schema, advanced SQL models for monthly cohort retention and RFM segmentation, a query optimization study that yielded an empirical 5.35x speedup, and a containerized Streamlit BI dashboard."*
</details>

<details>
<summary><b>2. "Why normalize to 3NF first, then build a Star Schema?"</b></summary>

> *"In transactional systems (OLTP), 3NF is critical to eliminate data redundancy and prevent insertion, update, and deletion anomalies. For instance, if a category name changes, it updates in one place without touching millions of historical order lines. However, 3NF requires expensive multi-table joins that degrade reporting performance. Therefore, I built an analytical Star Schema (OLAP) with pre-aggregated fact tables (`fact_orders`, `fact_order_items`) and conformed dimensions (`dim_date`, `dim_customer`, `dim_product`) to enable sub-second analytical aggregations without join overhead."*
</details>

<details>
<summary><b>3. "What is the difference between customer_id and customer_unique_id in Olist?"</b></summary>

> *"`customer_id` is an order-scoped surrogate key generated per transaction, whereas `customer_unique_id` represents the real human customer. If you calculate customer retention or repeat purchase rates using `customer_id`, your repeat rate will erroneously report as 0%. By grouping on `customer_unique_id`, I discovered that the platform has a 3.0% repeat purchase rate (2,801 repeat buyers) generating over R$ 1.58M in repeat revenue."*
</details>

<details>
<summary><b>4. "How did your query optimization experiment work?"</b></summary>

> *"I profiled a query filtering high-value orders across a 30-day temporal window. Using query execution plan analysis (`EXPLAIN QUERY PLAN`), I identified a bottleneck: because `order_purchase_timestamp` was unindexed, the query planner executed a full sequential scan across 112,000+ records, averaging 86.82 ms. I deployed a targeted B-Tree index on `orders(order_purchase_timestamp)`. The execution plan shifted from a sequential scan to an O(log N) index range search, reducing latency to 16.24 ms—a verified 5.35x speedup."*
</details>

<details>
<summary><b>5. "What business insights did you discover?"</b></summary>

> *"A major operational insight came from correlating fulfillment delays with customer satisfaction. While on-time deliveries held an average rating of 4.29/5.0 with only 6.6% 1-star reviews, orders delivered past the estimated date collapsed to an average rating of 2.57/5.0, and 1-star complaints exploded to 46.2%. This proved to executive leadership that seller fulfillment delay is the #1 driver of customer dissatisfaction on the platform."*
</details>
