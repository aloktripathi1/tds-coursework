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

