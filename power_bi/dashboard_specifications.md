# CommerceIQ — Enterprise Power BI Dashboard Visual Specifications

## Report Theme & Color Palette
- **Primary Navy**: `#1B2A4A` (Executive cards, headers, borders)
- **Accent Teal**: `#008080` (Delivered orders, growth metrics)
- **Alert Coral**: `#E63946` (Late delivery warnings, 1-star reviews)
- **Neutral Silver**: `#F8F9FA` (Visual canvas background)

---

## Page 1: Executive KPI Command Center

### Layout Grid:
- **Top Header KPI Ribbon (5 Cards)**:
  1. `[Gross Merchandise Value]` (Formatted as Currency R$ Millions)
  2. `[Total Orders]` (Formatted as #,##0)
  3. `[Unique Customers]` (Formatted as #,##0)
  4. `[Average Order Value]` (Formatted as Currency R$)
  5. `[Late Delivery Rate %]` (Formatted as 0.0%, Alert rule: Red if > 7.5%)
- **Left Chart (Area Visual)**:
  - **X-Axis**: `dim_date[year_month]`
  - **Y-Axis**: `[Total Revenue]`
  - **Tooltip**: `[Total Orders]`, `[MoM Revenue Growth %]`
- **Right Visual (Donut Chart)**:
  - **Legend**: `order_payments[payment_type]`
  - **Values**: `[Total Payment Value]`
  - **Data Labels**: Category + Percent of Total
- **Bottom Slicers**:
  - Year/Quarter Buttons (`dim_date[year]`, `dim_date[quarter]`)
  - Customer State Dropdown (`dim_customer[state]`)

---

## Page 2: Customer Retention & RFM Matrix

### Layout Grid:
- **Top Cards**:
  - `[Total Unique Customers]`, `[Repeat Customers]`, `[Repeat Customer Rate %] (3.0%)`
- **Main Visual (Decomposition Tree / Matrix)**:
  - **Row Level 1**: `dim_customer[Customer RFM Segment]` (*Champions, Loyal, At Risk, etc.*)
  - **Values**:
    - Customer Count
    - Total Revenue Contribution (R$)
    - Average Customer Lifetime Spend
    - Average Recency (Days)
- **Bar Chart**:
  - Revenue by RFM Segment sorted descending, highlighting `Potential Loyalists` and `Champions`.

---

## Page 3: Fulfillment & Logistics SLAs

### Layout Grid:
- **Top Gauge Visual**:
  - Target SLA: 95.0% On-Time Delivery
  - Current Performance: `92.01%`
- **Scatter Plot (Logistics Correlation)**:
  - **X-Axis**: `Average Delivery Days`
  - **Y-Axis**: `Average Review Rating`
  - **Bubble Size**: `[Total Orders]`
  - **Legend**: `Fulfillment Status` (On-Time vs Late)
  - Demonstrates the empirical drop from 4.29 stars (10.9 days) to 2.57 stars (31.4 days).
- **Table Visual**:
  - Bottom 15 Sellers by Carrier Dispatch Delay Rate.

---

## Page 4: Merchandising & Market Basket Analytics

### Layout Grid:
- **Treemap Visual**:
  - **Group**: `dim_product[category_name]`
  - **Values**: `[Total Revenue]`
  - **Color Saturation**: `[Average Review Rating]`
- **Cross-Sell Table Visual**:
  - Category A, Category B, Pair Order Count, Support %, Confidence %, Lift.
