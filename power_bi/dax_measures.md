# CommerceIQ — Enterprise Power BI DAX Measure Library

This repository contains production-grade **Data Analysis Expressions (DAX)** measures designed for the CommerceIQ **Kimball Star Schema** data warehouse (`fact_orders`, `fact_order_items`, `dim_date`, `dim_customer`, `dim_product`, `dim_seller`).

---

## 1. Core Financial & Volume KPIs

### Gross Merchandise Value (GMV)
Total platform financial throughput including item sales and freight value for delivered orders.
```dax
Gross Merchandise Value = 
CALCULATE(
    SUM(fact_orders[total_items_price]) + SUM(fact_orders[total_freight_value]),
    fact_orders[order_status] = "delivered"
)
```

### Net Item Revenue
```dax
Total Revenue = 
CALCULATE(
    SUM(fact_orders[total_items_price]),
    fact_orders[order_status] = "delivered"
)
```

### Total Freight Value
```dax
Total Freight = 
CALCULATE(
    SUM(fact_orders[total_freight_value]),
    fact_orders[order_status] = "delivered"
)
```

### Total Delivered Orders
```dax
Total Orders = 
CALCULATE(
    DISTINCTCOUNT(fact_orders[order_id]),
    fact_orders[order_status] = "delivered"
)
```

### Unique Customers
```dax
Total Unique Customers = 
DISTINCTCOUNT(dim_customer[customer_unique_id])
```

### Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```

### Freight-to-Revenue Ratio %
```dax
Freight Ratio % = 
DIVIDE([Total Freight], [Total Revenue], 0)
```

---

## 2. Time Intelligence & Growth Measures

### Previous Month Revenue (MoM)
```dax
Revenue PM = 
CALCULATE(
    [Total Revenue],
    DATEADD(dim_date[full_date], -1, MONTH)
)
```

### Month-over-Month Revenue Growth %
```dax
MoM Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR PriorRev = [Revenue PM]
RETURN
    DIVIDE(CurrentRev - PriorRev, PriorRev, 0)
```

### Year-over-Year Revenue Growth %
```dax
YoY Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR PriorYearRev = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(dim_date[full_date]))
RETURN
    DIVIDE(CurrentRev - PriorYearRev, PriorYearRev, 0)
```

### Year-to-Date (YTD) Revenue
```dax
YTD Revenue = 
TOTALYTD([Total Revenue], dim_date[full_date])
```

### 30-Day Rolling Average Revenue
```dax
Rolling 30D Revenue = 
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(dim_date[full_date], MAX(dim_date[full_date]), -30, DAY)
) / 30
```

---

## 3. Operations & Logistics SLA Measures

### On-Time Orders
```dax
On-Time Orders = 
CALCULATE(
    [Total Orders],
    fact_orders[is_late_delivery] = 0
)
```

### Late Orders
```dax
Late Orders = 
CALCULATE(
    [Total Orders],
    fact_orders[is_late_delivery] = 1
)
```

### Late Delivery Rate %
```dax
Late Delivery Rate % = 
DIVIDE([Late Orders], [Total Orders], 0)
```

### Average Delivery Days
```dax
Average Delivery Days = 
AVERAGEX(
    FILTER(fact_orders, fact_orders[order_status] = "delivered" && NOT(ISBLANK(fact_orders[actual_delivery_days]))),
    fact_orders[actual_delivery_days]
)
```

### Average Customer Review Rating
```dax
Average Review Rating = 
AVERAGEX(
    FILTER(fact_orders, NOT(ISBLANK(fact_orders[avg_review_score]))),
    fact_orders[avg_review_score]
)
```

### 1-Star Review Rate %
```dax
1-Star Review Rate % = 
VAR OneStarOrders = 
    CALCULATE(
        COUNTROWS(fact_orders),
        fact_orders[avg_review_score] <= 1.0,
        fact_orders[order_status] = "delivered"
    )
RETURN
    DIVIDE(OneStarOrders, [Total Orders], 0)
```

---

## 4. Customer Intelligence & RFM Dynamic Segmentation in DAX

### Customer Recency Days
```dax
Customer Recency = 
VAR MaxPlatformDate = CALCULATE(MAX(fact_orders[order_date_key]), ALL(fact_orders))
VAR MaxCustomerDate = MAX(fact_orders[order_date_key])
RETURN
    DATEDIFF(
        DATE(LEFT(MaxCustomerDate, 4), MID(MaxCustomerDate, 5, 2), RIGHT(MaxCustomerDate, 2)),
        DATE(LEFT(MaxPlatformDate, 4), MID(MaxPlatformDate, 5, 2), RIGHT(MaxPlatformDate, 2)),
        DAY
    )
```

### Customer Frequency (Lifetime Orders)
```dax
Customer Frequency = 
CALCULATE(
    DISTINCTCOUNT(fact_orders[order_id]),
    ALLEXCEPT(dim_customer, dim_customer[customer_unique_id])
)
```

### Customer Monetary Spend (Lifetime GMV)
```dax
Customer Monetary Spend = 
CALCULATE(
    [Total Revenue],
    ALLEXCEPT(dim_customer, dim_customer[customer_unique_id])
)
```

### Dynamic RFM Segment Classification
```dax
Customer RFM Segment = 
VAR R = [Customer Recency]
VAR F = [Customer Frequency]
VAR M = [Customer Monetary Spend]
RETURN
    SWITCH(
        TRUE(),
        R <= 150 && F >= 2, "Champions",
        R <= 300 && F >= 2, "Loyal Customers",
        R <= 150 && F = 1 && M >= 250, "Potential Loyalists",
        R <= 200 && F = 1, "Recent Customers",
        R > 350 && F >= 2, "At Risk",
        R > 350 && M >= 250, "Lost High-Spenders",
        "Standard Hibernating"
    )
```

### Repeat Customer Count
```dax
Repeat Customers = 
CALCULATE(
    DISTINCTCOUNT(dim_customer[customer_unique_id]),
    FILTER(
        VALUES(dim_customer[customer_unique_id]),
        [Customer Frequency] > 1
    )
)
```

### Repeat Customer Rate %
```dax
Repeat Customer Rate % = 
DIVIDE([Repeat Customers], [Total Unique Customers], 0)
```

---

## 5. Merchandising & Basket Metrics

### Units Sold
```dax
Units Sold = 
COUNTROWS(fact_order_items)
```

### Units Per Order
```dax
Units Per Order = 
DIVIDE([Units Sold], [Total Orders], 0)
```

### Category Revenue Contribution %
```dax
Category Revenue Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(dim_product[category_name])),
    0
)
```
