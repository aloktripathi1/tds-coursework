{{
    config(
        materialized='table',
        tags=['mart', 'gmv', 'weekly', 'marketplace'],
        meta={
            'owner': 'analytics_team',
            'description': 'Weekly GMV mart for marketplace analytics covering the last 90 days, aggregating orders by seller, category, and standardizing GMV calculations.'
        }
    )
}}

-- ============================================================
-- fct_weekly_gmv
-- Grain       : one row per weekly period per seller / category
-- Window      : last 90 days relative to current_date
-- Key metric  : total_gmv, order_count, commission_revenue
-- Source      : int_customer_orders
-- ============================================================

with

-- ----------------------------------------------------------
-- 1. Pull from upstream intermediate model
-- ----------------------------------------------------------
daily_orders as (

    select * from {{ ref('int_customer_orders') }}

    where
        -- restrict to last 90 days
        order_date >= current_date - interval '90 days'
        and order_date <  current_date + interval '1 day'
        -- Marketplace specific: only include successful orders in GMV
        and order_status in ('completed', 'shipped', 'delivered')

),

-- ----------------------------------------------------------
-- 2. Aggregate to weekly grain with marketplace dimensions
-- ----------------------------------------------------------
weekly_aggregates as (

    select
        date_trunc('week', order_date)              as period,
        seller_id,
        product_category,
        
        count(order_id)                             as order_count,
        count(distinct customer_id)                 as unique_customers,
        
        -- GMV calculation (Gross Merchandise Value)
        round(sum(order_value), 2)                  as total_gmv,
        round(avg(order_value), 2)                  as avg_order_value,
        
        -- Marketplace revenue (assuming standard commission rate could be here, or mapped from a dim)
        -- Using a proxy 10% commission for demonstration if not provided in source
        round(sum(coalesce(commission_fee, order_value * 0.10)), 2) as estimated_commission_revenue

    from daily_orders

    group by 1, 2, 3

),

-- ----------------------------------------------------------
-- 3. Enrich with BI-ready labels
-- ----------------------------------------------------------
final as (

    select
        period,
        seller_id,
        product_category,
        
        order_count,
        unique_customers,
        
        total_gmv,
        avg_order_value,
        estimated_commission_revenue,

        -- seller_performance_tier: categorical label for BI filtering
        case
            when total_gmv >= 50000 then 'top_tier'
            when total_gmv >= 10000 then 'mid_tier'
            else                         'growth_tier'
        end                                         as seller_performance_tier,

        current_timestamp                           as dbt_updated_at

    from weekly_aggregates

)

-- ----------------------------------------------------------
-- Final select: ordered chronologically for BI consumption
-- ----------------------------------------------------------
select *
from final
order by
    period asc,
    total_gmv desc
