# CommerceIQ: SQL Query Optimization & Indexing Benchmark

## 1. Executive Summary

This optimization study documents a real-world database tuning experiment on the CommerceIQ platform. By analyzing the query execution plan, identifying a table-scanning bottleneck on an unindexed temporal predicate, and deploying a targeted B-tree index, we achieved an **81.3% reduction in query latency** and a **5.35x speedup** on a dataset of over 100,000 orders and 112,000 order items.

---

## 2. The Benchmark Query

We analyzed a typical business reporting query that evaluates high-value orders placed during a promotional month:

```sql
SELECT 
    o.order_id, 
    o.order_status, 
    oi.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_purchase_timestamp BETWEEN '2017-06-01' AND '2017-06-30'
  AND oi.price > 100.00;
```

---

## 3. Empirical Benchmark Results

| Metric | Baseline (No Index) | Optimized (B-Tree Index) | Delta / Improvement |
| :--- | :--- | :--- | :--- |
| **Execution Plan** | Full Sequential Scan (`SCAN oi`) | B-Tree Range Search (`SEARCH o USING INDEX`) | Eliminated 100K+ table row comparisons |
| **Average Latency (30 runs)** | **86.82 ms** | **16.24 ms** | **-70.58 ms (5.35x faster)** |
| **Latency Reduction %** | — | — | **81.3% Faster** |
| **Algorithmic Complexity** | $\mathcal{O}(N)$ sequential disk reads | $\mathcal{O}(\log N + K)$ B-Tree traversal | Logarithmic index lookup |

---

## 4. Execution Plan Dissection

### A. Pre-Optimization Plan (Bottleneck)
```text
SCAN oi
SEARCH o USING INDEX (order_id=?)
```
- **Why it was slow**: Because `order_purchase_timestamp` had no index, the query optimizer was forced to iterate over the entire `order_items` table (112,650 rows) and join each row back to `orders` to check the date range condition.

### B. Index Deployment
```sql
CREATE INDEX idx_orders_purchase_timestamp ON orders(order_purchase_timestamp);
```

### C. Post-Optimization Plan (Optimized)
```text
SEARCH o USING INDEX idx_orders_purchase_timestamp (order_purchase_timestamp>? AND order_purchase_timestamp<?)
SEARCH oi USING INDEX (order_id=?)
```
- **Why it was fast**: With the B-Tree index in place, the query optimizer inverted the join plan. It first jumped directly into the target leaf nodes of the B-Tree covering June 2017 in $\mathcal{O}(\log N)$ time, retrieved only the matching orders, and then performed fast primary key lookups into `order_items`.

---

## 5. Interview Defense Guide

### Q1: "What does an index do under the hood?"
> **Answer**: An index is a distinct auxiliary data structure (typically a balanced B-Tree) maintained by the database engine. In a B-Tree, keys are kept in sorted order across hierarchical nodes. Instead of performing a linear scan of every disk block in a table ($\mathcal{O}(N)$), the engine traverses from root to leaf node in $\mathcal{O}(\log N)$ page accesses, locating exact records or range boundaries with minimal disk I/O.

### Q2: "Why not just index every column?"
> **Answer**: Every index imposes a write tax. When you `INSERT`, `UPDATE`, or `DELETE`, the database engine must synchronously update every corresponding B-Tree structure on disk, increasing write latency and Write-Ahead Log (WAL) volume. Furthermore, unused indexes consume valuable buffer cache RAM. Indexing strategy should be strictly workload-driven: index foreign keys, high-cardinality equality filter columns, and frequent range/sort predicates.
