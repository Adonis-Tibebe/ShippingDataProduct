{{ config(materialized='table') }}

with bounds as (
    select 
        min(posted_at::date) - interval '30 days' as start_date,
        max(posted_at::date) + interval '30 days' as end_date
    from {{ ref('stg_telegram_messages') }}
),

date_series as (
    select generate_series(
        (select start_date from bounds),
        (select end_date from bounds),
        interval '1 day'
    )::date as date
)

select
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    to_char(date, 'Day') as day_name,
    extract(isodow from date) as day_of_week,
    to_char(date, 'Month') as month_name,
    concat_ws('-', extract(year from date)::text, lpad(extract(month from date)::text, 2, '0')) as year_month,
    ceil(extract(month from date) / 3.0)::int as quarter,
    case when extract(isodow from date) in (6,7) then true else false end as is_weekend
from date_series