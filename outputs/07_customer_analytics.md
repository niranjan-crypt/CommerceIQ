# Query Output: Customer RFM Behavioral Segmentation

- **SQL Script**: [`sql/07_customer_analytics.sql`](../sql/07_customer_analytics.sql)
- **Engine**: PostgreSQL / SQLite Relational Storage
- **Scale**: 100,000+ Records Analyzed

## Execution Results

```text
customer_segment     | total_customers | avg_recency_days | avg_orders | avg_spend | segment_total_spend | pct_of_customer_base | pct_of_total_revenue
---------------------+-----------------+------------------+------------+-----------+---------------------+----------------------+---------------------
Potential Loyalists  | 14497           | 140.4            | 1.0        | 267.74    | 3881356.47          | 15.53                | 29.36               
Recent Customers     | 39704           | 197.4            | 1.0        | 89.39     | 3549052.62          | 42.53                | 26.84               
Lost High-Spenders   | 5701            | 446.4            | 1.0        | 457.41    | 2607684.41          | 6.11                 | 19.72               
Standard Hibernating | 30655           | 443.0            | 1.0        | 80.08     | 2454995.86          | 32.84                | 18.57               
Champions            | 1205            | 137.4            | 2.16       | 271.0     | 326556.39           | 1.29                 | 2.47                
At Risk Customers    | 988             | 430.9            | 2.08       | 246.15    | 243193.07           | 1.06                 | 1.84                
Loyal Customers      | 608             | 266.1            | 2.09       | 260.95    | 158659.29           | 0.65                 | 1.2                 
(7 rows)
```
