# CommerceIQ — Enterprise Power BI Star Schema Data Model Guide

This guide details the architectural blueprint for connecting **Power BI Desktop** directly to the CommerceIQ PostgreSQL database (or local analytical mart) using the **Kimball Star Schema**.

---

## 1. Storage Mode Recommendation

| Scenario | Recommended Mode | Rationale |
| :--- | :--- | :--- |
| **Production Analytics (< 5M rows)** | **Import Mode (VertiPaq Engine)** | Delivers sub-second DAX calculation latency, maximum compression (in-memory columnar storage), and full support for advanced time-intelligence functions (`DATEADD`, `SAMEPERIODLASTYEAR`). |
| **Real-Time Logistics Monitoring** | **DirectQuery Mode** | Queries pass directly to PostgreSQL 16 on visual refresh, ensuring zero data stale time for live delivery SLA dispatchers. |
| **Enterprise Hybrid** | **Composite Mode** | Dimensions and aggregated `fact_orders` cached in Import mode; granular `fact_order_items` accessed via DirectQuery. |

---

## 2. Entity-Relationship & Cardinality Mapping

In Power BI Model View, relationships must be configured as **One-to-Many ($1 \to *)$** with **Single Cross-Filter Direction** from Dimensions to Facts:

```text
       ┌──────────────┐                 ┌──────────────┐
       │   dim_date   │                 │ dim_customer │
       └──────┬───────┘                 └──────┬───────┘
              │ 1                              │ 1
              │                                │
              │ * (order_date_key)             │ * (customer_key)
       ┌──────┴────────────────────────────────┴───────┐
       │                  fact_orders                  │
       └──────────────────────┬────────────────────────┘
                              │ 1 (order_id)
                              │
                              │ * (order_id)
       ┌──────────────────────┴────────────────────────┐
       │               fact_order_items                │
       └──────┬────────────────────────────────┬───────┘
              │ * (product_key)                │ * (seller_key)
              │                                │
              │ 1                              │ 1
       ┌──────┴───────┐                 ┌──────┴───────┐
       │ dim_product  │                 │  dim_seller  │
       └──────────────┘                 └──────────────┘
```

### Table Relationships Configuration Matrix:

| From Table (Dimension) | Primary Key (`1`) | To Table (Fact) | Foreign Key (`*`) | Cardinality | Cross-Filter Direction |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `dim_date` | `date_key` | `fact_orders` | `order_date_key` | 1 to Many | Single (`dim_date` filters `fact_orders`) |
| `dim_date` | `date_key` | `fact_orders` | `delivered_date_key` | 1 to Many | Inactive (activate via `USERELATIONSHIP`) |
| `dim_customer` | `customer_key` | `fact_orders` | `customer_key` | 1 to Many | Single (`dim_customer` filters `fact_orders`) |
| `dim_product` | `product_key` | `fact_order_items` | `product_key` | 1 to Many | Single (`dim_product` filters `fact_order_items`) |
| `dim_seller` | `seller_key` | `fact_order_items` | `seller_key` | 1 to Many | Single (`dim_seller` filters `fact_order_items`) |
| `fact_orders` | `order_id` | `fact_order_items` | `order_id` | 1 to Many | Single (`fact_orders` filters `fact_order_items`) |

---

## 3. Dimension Hierarchies & Sort By Columns

### A. Temporal Hierarchy (`dim_date`)
Mark `dim_date` as the **Official Date Table** in Power BI (`full_date` as Date column):
- **Hierarchy**: `Year` $\to$ `Quarter` $\to$ `Month Name` $\to$ `Day`
- **Critical Configuration**: Select column `month_name` and set **Sort by Column** $\to$ `month` (prevents alphabetical sorting like "April, August, December").

### B. Geographic Hierarchy (`dim_customer`, `dim_seller`)
- **Data Category**: Set `state` $\to$ **State or Province**, `city` $\to$ **City**, `zip_code_prefix` $\to$ **Postal Code**.
- **Hierarchy**: `State` $\to$ `City` $\to$ `Postal Code`.

---

## 4. Performance Optimization Checklist for Power BI

1. **Hide Foreign Keys from Report View**:
   - Hide `customer_key`, `product_key`, `seller_key`, and `order_date_key` in Fact tables so report authors are forced to use the Dimension attributes.
2. **Disable Auto Date/Time**:
   - Go to *Options and Settings $\to$ Current File $\to$ Data Load $\to$ Time Intelligence* and turn off **Auto Date/Time**. This eliminates hidden internal date tables and reduces PBIX file size by 40-70%.
3. **Use Integer Date Keys**:
   - Join keys use `YYYYMMDD` integers (`20171002`), which VertiPaq encodes via high-speed dictionary and bit-packing compression.
