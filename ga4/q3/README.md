# Q3: dbt — Weekly GMV Mart Model

## Task

Build a dbt mart model that transforms raw marketplace order data into **weekly GMV** aggregates, covering the last **90 days**, for use in BI dashboards.

---

## Requirements

* Use `{{ ref() }}` to reference upstream model `int_customer_orders`
* Window: `order_date >= current_date - interval '90 days'`
* Group by `date_trunc('week', order_date)` for weekly periods
* Key metrics: `order_count`, `total_gmv`, `avg_order_value`, `unique_customers`
* Order results chronologically (`week_start asc`)
* Structure SQL with CTEs for readability

---

## Approach

### 1. Source CTE
Pull from `{{ ref('int_customer_orders') }}` and filter to last 90 days.

### 2. Weekly Aggregation
Use `date_trunc('week', order_date)` as the grain; compute:
- `total_gmv = sum(order_value)`
- `order_count = count(*)`
- `avg_order_value = avg(order_value)`
- `unique_customers = count(distinct customer_id)`

### 3. Enrich
Add `week_end`, GMV tier label (`high/medium/low`), and `dbt_updated_at` timestamp.

---

## Code

| File | Purpose |
|---|---|
| [`fct_weekly_gmv.sql`](./fct_weekly_gmv.sql) | dbt mart model for weekly GMV analytics |

**Key dbt structure:**
```sql
with

daily_orders as (
    select * from {{ ref('int_customer_orders') }}
    where order_date >= current_date - interval '90 days'
),

weekly_aggregates as (
    select
        date_trunc('week', order_date)   as week_start,
        count(*)                         as order_count,
        round(sum(order_value), 2)       as total_gmv,
        round(avg(order_value), 2)       as avg_order_value,
        count(distinct customer_id)      as unique_customers
    from daily_orders
    group by 1
),

final as (
    select *, current_timestamp as dbt_updated_at
    from weekly_aggregates
)

select * from final
order by week_start asc
```

---

## Execution

```bash
dbt run --select fct_weekly_gmv
dbt test --select fct_weekly_gmv
```

---

## Submission

**Your Answer:**
```
fct_weekly_gmv.sql
```
