# Q4: dbt Daily Inventory Performance Mart

## Task

Build a **dbt intermediate model** that powers the **Orbit Ops dashboards** for inventory performance. The model must track **average days on hand** at a **daily grain** covering the **last 30 days**, drawing from the upstream staging table (`stg_inventory_snapshots`).

---

## Requirements

* Use `{{ config(...) }}` to declare materialization and description.
* Reference upstream models via `{{ ref() }}`.
* Filter rows to the **last 30 days** relative to `current_date`.
* Aggregate results at **daily grain** using `date_trunc`.
* Compute `avg_days_on_hand` by warehouse.
* Handle NULLs with `coalesce` to avoid skewing averages or sums.
* Return columns ordered by date (newest first), ready for BI consumption.
* Compatible with Snowflake / BigQuery SQL dialect.

---

## Approach

### 1. Materialization & Metadata
The model uses `{{ config(materialized='table', description='...') }}` to declare it as a table with a clear description of its purpose for powering Orbit Ops dashboards.

### 2. Upstream Source Reference
The `inventory_data` CTE pulls from `{{ ref('stg_inventory_snapshots') }}` and applies NULL handling to dimensional data (`warehouse_name`) and metrics (`quantity_on_hand`, `days_on_hand`).

### 3. 30-Day Rolling Filter
The staging CTE filters with:
```sql
where cast(snapshot_date as date) >= current_date - interval '30 day'
```
This ensures a 30-day rolling window relative to `current_date` without hard-coded dates.

### 4. Daily Aggregation by Warehouse
The `daily_inventory_metrics` CTE groups by `inventory_date` (daily grain via `date_trunc`) and `warehouse_name`, computing:
- `sum(quantity_on_hand)` → `total_units_on_hand`
- `count(distinct product_id)` → `total_unique_products`
- `avg(days_on_hand)` → `avg_days_on_hand`

### 5. NULL Handling
`coalesce(warehouse_name, 'Unknown Warehouse')` ensures dimensional data has default values.
`coalesce(quantity_on_hand, 0)` and `coalesce(days_on_hand, 0)` are applied to metrics to prevent NULLs from skewing aggregations.

### 6. BI-Ready Output
The final select statement:
- Casts `inventory_date` to date type for clean BI consumption
- Rounds `avg_days_on_hand` to 2 decimal places for readability
- Orders by `inventory_date DESC, warehouse_name ASC` for dashboard consumption

---

## Code

**Model file:** [`mart_support_daily.sql`](./mart_support_daily.sql)

```sql
{{ config(
        materialized='table',
            description='Intermediate model for daily inventory performance powering Orbit Ops dashboards. Tracks average days on hand over the last 30 days.'
) }}

with inventory_data as (
        select 
                snapshot_date,
                        -- Handle NULLs in dimensional data
                                coalesce(warehouse_name, 'Unknown Warehouse') as warehouse_name,
                                        product_id,
                                                -- Handle NULLs in metrics to avoid skewing the averages or sums
                                                        coalesce(quantity_on_hand, 0) as quantity_on_hand,
                                                                coalesce(days_on_hand, 0) as days_on_hand
                                                                    from {{ ref('stg_inventory_snapshots') }}
                                                                        -- Filter rows to the last 30 days relative to current_date
                                                                            where cast(snapshot_date as date) >= current_date - interval '30 day'
),

daily_inventory_metrics as (
        select
                date_trunc('day', snapshot_date) as inventory_date,
                        warehouse_name,
                                sum(quantity_on_hand) as total_units_on_hand,
                                        count(distinct product_id) as total_unique_products,
                                                avg(days_on_hand) as avg_days_on_hand
                                                    from inventory_data
                                                        group by 1, 2
)

select 
    cast(inventory_date as date) as inventory_date,
        warehouse_name,
            total_units_on_hand,
                total_unique_products,
                    -- Rounding for clean BI consumption
                        round(avg_days_on_hand, 2) as avg_days_on_hand
                        from daily_inventory_metrics
                        -- Ordered by date (newest first) and then by warehouse
                        order by inventory_date desc, warehouse_name asc
```

---

## Verification

To test this model locally:

1. Set up a dbt project with the Snowflake or BigQuery adapter.
2. Ensure `stg_inventory_snapshots` exists (or mock it as a seed with columns: `snapshot_date`, `warehouse_name`, `product_id`, `quantity_on_hand`, `days_on_hand`).
3. Place this file under `models/intermediate/inventory/mart_support_daily.sql`.
4. Run:
   ```bash
   dbt run --select mart_support_daily
   dbt test --select mart_support_daily
   ```
5. Validate in the warehouse:
   ```sql
   select * from mart_support_daily
   order by inventory_date desc
   limit 30;
   ```
6. Confirm rows span up to 30 days, `avg_days_on_hand` is non-null and rounded to 2 decimals, `warehouse_name` has no NULLs (shows 'Unknown Warehouse' for missing values), and results are ordered by date descending.
