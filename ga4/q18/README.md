# 18: Data Preparation for RetailCo Analytics

## Task

Analyze an `orders` table to extract specific sales metrics for the LATAM region. Clean missing customer data, bin order amounts into distinct price categories, and compute the total order count and revenue exclusively for the "medium" price tier.

---

## Requirements

* Write a **single DuckDB SQL query**
* Filter records to strictly `region = 'LATAM'`
* Replace `NULL` values in the `customer` column with `'Unknown'` using `COALESCE`
* Assign a `price_band` using a `CASE` expression:
* `'high'` if amount > 720
* `'medium'` if amount > 323
* `'low'` otherwise


* Return exactly **one row** for the `'medium'` band containing `order_count` and `total_amount` (sum of amounts rounded to 2 decimal places)

---

## Approach

### 1. Data Cleaning & Binning (CTE)

Use a Common Table Expression (`WITH cleaned_orders AS (...)`) to isolate the 'LATAM' region data first. Within this step, apply `COALESCE` to handle missing customer names and implement the `CASE WHEN` logic to evaluate the `amount` column and assign the appropriate `price_band` label to every row.

### 2. Aggregation & Filtering

Query the prepared data from the CTE, applying a `WHERE price_band = 'medium'` filter to isolate the exact tier requested by the business.

### 3. Metric Calculation

Use `COUNT(*)` to calculate the `order_count` and wrap the sum function in a round function: `ROUND(SUM(amount), 2)` to compute the `total_amount` accurately formatted as currency.

---

## Code

**Script:** [`query.sql`](https://www.google.com/search?q=./query.sql)

```sql
WITH cleaned_orders AS (
    SELECT
        order_id,
        COALESCE(customer, 'Unknown') AS customer,
        amount,
        CASE 
            WHEN amount > 720 THEN 'high'
            WHEN amount > 323 THEN 'medium'
            ELSE 'low'
        END AS price_band
    FROM orders
    WHERE region = 'LATAM'
)

SELECT
    COUNT(*) AS order_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM cleaned_orders
WHERE price_band = 'medium';

```

---

## Verification

```bash
duckdb retailco.db < query.sql

```

| Metric | Output Format / Value |
| --- | --- |
| Region evaluated | `LATAM` |
| Target price band | `medium` |
| order_count | *Count of rows matching criteria (Integer)* |
| total_amount | *Sum of amounts (Decimal rounded to 2 places)* |
