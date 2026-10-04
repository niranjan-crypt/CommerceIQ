# Query Output: Empirical Indexing & Query Plan Optimization Benchmark

- **SQL Script**: [`sql/11_optimization.sql`](../sql/11_optimization.sql)
- **Engine**: PostgreSQL / SQLite Relational Storage
- **Scale**: 100,000+ Records Analyzed

## Execution Results

```text
id | parent | notused | detail                                  
---+--------+---------+-----------------------------------------
5  | 0      | 163     | SEARCH o USING INDEX idx_orders_purchase
11 | 0      | 62      | SEARCH oi USING INDEX sqlite_autoindex_o
(2 rows)

Statement executed successfully.

id | parent | notused | detail                                  
---+--------+---------+-----------------------------------------
5  | 0      | 163     | SEARCH o USING INDEX idx_orders_purchase
11 | 0      | 62      | SEARCH oi USING INDEX sqlite_autoindex_o
(2 rows)
```
