{{ config(materialized='table') }}

select
  d.date,
  d.day_name,
  d.day_of_week,
  d.year_month,
  d.is_weekend,
  count(*) filter (
    where s.is_health_related
  ) as health_related_posts,
  count(*) as total_posts,
  round(
    count(*) filter (where s.is_health_related)::numeric / nullif(count(*), 0),
    2
  ) as health_focus_ratio
from {{ ref('fct_messages') }} f
join {{ ref('dim_dates') }} d on f.posted_date = d.date
join {{ ref('dim_message_metadata') }} s
 on f.message_metadata_id = s.message_metadata_id
join {{ ref('dim_channel') }} c on f.channel_id = c.channel_id
group by d.date, d.day_name, d.day_of_week, d.year_month, d.is_weekend
order by d.date asc