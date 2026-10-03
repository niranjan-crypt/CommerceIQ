# Query Output: Executive & Top-Line Revenue KPIs

- **SQL Script**: [`sql/06_business_analytics.sql`](../sql/06_business_analytics.sql)
- **Engine**: PostgreSQL / SQLite Relational Storage
- **Scale**: 100,000+ Records Analyzed

## Execution Results

```text
total_delivered_orders | total_unique_customers | total_item_revenue | total_freight_value | gross_merchandise_value | average_order_value | platform_avg_rating
-----------------------+------------------------+--------------------+---------------------+-------------------------+---------------------+--------------------
96478                  | 93358                  | 13279836.59        | 2209828.96          | 15489665.55             | 137.65              | 4.08               
(1 row)


total_customers | one_time_buyers | repeat_customers | repeat_rate_pct | overall_avg_spend_per_customer
----------------+-----------------+------------------+-----------------+-------------------------------
93358           | 90557           | 2801             | 3.0             | 141.62                        
(1 row)


product_category      | total_orders | items_sold | category_revenue | pct_revenue_share | avg_review_score
----------------------+--------------+------------+------------------+-------------------+-----------------
health_beauty         | 8836         | 9727       | 1263138.54       | 9.29              | 4.14            
watches_gifts         | 5624         | 6001       | 1206075.33       | 8.87              | 4.02            
bed_bath_table        | 9417         | 11270      | 1050936.61       | 7.73              | 3.9             
sports_leisure        | 7720         | 8700       | 993656.51        | 7.31              | 4.11            
computers_accessories | 6689         | 7894       | 919640.54        | 6.77              | 3.93            
furniture_decor       | 6449         | 8415       | 736282.47        | 5.42              | 3.9             
cool_stuff            | 3632         | 3806       | 637258.51        | 4.69              | 4.15            
housewares            | 5884         | 6989       | 634542.6         | 4.67              | 4.06            
auto                  | 3897         | 4256       | 594363.1         | 4.37              | 4.07            
garden_tools          | 3518         | 4361       | 486432.45        | 3.58              | 4.04            
(10 rows)


customer_state | total_orders | total_revenue | avg_freight_per_item | state_revenue_pct
---------------+--------------+---------------+----------------------+------------------
SP             | 40501        | 5067633.16    | 15.12                | 37.28            
RJ             | 12350        | 1759651.13    | 20.91                | 12.95            
MG             | 11354        | 1552481.83    | 20.63                | 11.42            
RS             | 5345         | 728897.47     | 21.61                | 5.36             
PR             | 4923         | 666063.51     | 20.47                | 4.9              
SC             | 3546         | 507012.13     | 21.51                | 3.73             
BA             | 3256         | 493584.14     | 26.49                | 3.63             
DF             | 2080         | 296498.41     | 21.07                | 2.18             
GO             | 1957         | 282836.7      | 22.56                | 2.08             
ES             | 1995         | 268643.45     | 22.03                | 1.98             
PE             | 1593         | 251889.49     | 32.69                | 1.85             
CE             | 1279         | 219757.38     | 32.73                | 1.62             
PA             | 946          | 174470.59     | 35.63                | 1.28             
MT             | 886          | 152191.62     | 28.0                 | 1.12             
MA             | 717          | 117009.38     | 38.49                | 0.86             
MS             | 701          | 115429.97     | 23.35                | 0.85             
PB             | 517          | 112586.82     | 43.09                | 0.83             
PI             | 476          | 84721.0       | 39.12                | 0.62             
RN             | 474          | 82105.66      | 35.72                | 0.6              
AL             | 397          | 78855.72      | 35.87                | 0.58             
SE             | 335          | 56574.19      | 36.57                | 0.42             
TO             | 274          | 48402.51      | 37.44                | 0.36             
RO             | 243          | 45682.76      | 41.33                | 0.34             
AM             | 145          | 22155.84      | 33.31                | 0.16             
AC             | 80           | 15930.97      | 40.05                | 0.12             
AP             | 67           | 13374.81      | 34.16                | 0.1              
RR             | 41           | 7057.47       | 43.09                | 0.05             
(27 rows)


payment_type | total_orders | total_payment_value | avg_installments | payment_value_share_pct
-------------+--------------+---------------------+------------------+------------------------
credit_card  | 76505        | 12542084.19         | 3.5              | 78.34                  
boleto       | 19784        | 2869361.27          | 1.0              | 17.92                  
voucher      | 3866         | 379436.87           | 1.0              | 2.37                   
debit_card   | 1528         | 217989.79           | 1.0              | 1.36                   
not_defined  | 3            | 0.0                 | 1.0              | 0.0                    
(5 rows)
```
