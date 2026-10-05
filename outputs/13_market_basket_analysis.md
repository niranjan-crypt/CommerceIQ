# Query Output: Market Basket Analysis & Product Affinity Rules

- **SQL Script**: [`sql/13_market_basket_analysis.sql`](../sql/13_market_basket_analysis.sql)
- **Engine**: PostgreSQL / SQLite Relational Storage
- **Scale**: 100,000+ Records Analyzed

## Execution Results

```text
item_a                    | item_b            | pair_order_count | support_pct | confidence_a_to_b_pct | lift
--------------------------+-------------------+------------------+-------------+-----------------------+-----
bed_bath_table            | furniture_decor   | 70               | 0.071       | 0.74                  | 0.11
bed_bath_table            | home_confort      | 43               | 0.044       | 0.46                  | 1.13
furniture_decor           | housewares        | 24               | 0.024       | 0.37                  | 0.06
baby                      | cool_stuff        | 20               | 0.02        | 0.69                  | 0.19
bed_bath_table            | housewares        | 20               | 0.02        | 0.21                  | 0.04
baby                      | toys              | 19               | 0.019       | 0.66                  | 0.17
baby                      | bed_bath_table    | 17               | 0.017       | 0.59                  | 0.06
furniture_decor           | garden_tools      | 17               | 0.017       | 0.26                  | 0.07
health_beauty             | sports_leisure    | 14               | 0.014       | 0.16                  | 0.02
housewares                | other             | 14               | 0.014       | 0.24                  | 0.16
furniture_decor           | home_construction | 13               | 0.013       | 0.2                   | 0.41
baby                      | furniture_decor   | 12               | 0.012       | 0.42                  | 0.06
health_beauty             | perfumery         | 12               | 0.012       | 0.14                  | 0.04
bed_bath_table            | health_beauty     | 11               | 0.011       | 0.12                  | 0.01
construction_tools_lights | furniture_decor   | 11               | 0.011       | 4.51                  | 0.69
(15 rows)
```
