# Query Output: Product Pareto & Logistics Freight Economics

- **SQL Script**: [`sql/08_product_analytics.sql`](../sql/08_product_analytics.sql)
- **Engine**: PostgreSQL / SQLite Relational Storage
- **Scale**: 100,000+ Records Analyzed

## Execution Results

```text
product_id                       | product_revenue | running_revenue | cumulative_revenue_pct
---------------------------------+-----------------+-----------------+-----------------------
bb50f2e236e5eea0100680137654686c | 63885.0         | 63885.0         | 0.47                  
6cdd53843498f92890544667809f1595 | 54730.2         | 118615.2        | 0.87                  
d6160fb7873f184099d9bc95e30376af | 48899.34        | 167514.54       | 1.23                  
d1c427060a0f73f6b889a5c7c61f2ac4 | 47214.51        | 214729.05       | 1.58                  
99a4788cb24856965c36a24e339b6058 | 43025.56        | 257754.61       | 1.9                   
3dd2a17168ec895c781a9191c1e95ad7 | 41082.6         | 298837.21       | 2.2                   
25c38557cf793876c5abdd5931f922db | 38907.32        | 337744.53       | 2.48                  
5f504b3a1c75b73d6151be81eb05bdc9 | 37733.9         | 375478.43       | 2.76                  
53b36df67ebb7c41585e8d54d6772e08 | 37683.42        | 413161.85       | 3.04                  
aca2eb7d00ea1a7b8ebd4e68314663af | 37608.9         | 450770.75       | 3.32                  
e0d64dcfaa3b6db5c54ca298ae101d05 | 31786.82        | 482557.57       | 3.55                  
d285360f29ac7fd97640bf0baef03de0 | 31623.81        | 514181.38       | 3.78                  
7a10781637204d8d10485c71a6108a2e | 30467.5         | 544648.88       | 4.01                  
f1c7f353075ce59d8a6f3cf58f419c9c | 29997.36        | 574646.24       | 4.23                  
f819f0c84a64f02d3a5606ca95edd272 | 29024.48        | 603670.72       | 4.44                  
(15 rows)


weight_tier        | items_sold | avg_item_price | avg_freight | freight_to_price_ratio_pct
-------------------+------------+----------------+-------------+---------------------------
Very Heavy (>10kg) | 5325       | 334.14         | 54.53       | 16.32                     
Heavy (5-10kg)     | 8684       | 183.86         | 30.65       | 16.67                     
Medium (1-5kg)     | 32017      | 135.86         | 20.11       | 14.8                      
Light (<1kg)       | 66606      | 88.03          | 15.78       | 17.93                     
(4 rows)
```
