{{ config(materialized='table') }}

select
  p.product_name,
  c.channel_name,
  count(*) as mention_count,
  min(p.main_price)::numeric as min_price,
  max(p.main_price)::numeric as max_price,
  round(avg(p.main_price)::numeric, 2) as avg_price
from {{ ref('dim_product_mention') }} p
join {{ ref('fct_messages') }} f
  on p.message_metadata_id = f.message_metadata_id
join {{ ref('dim_channel') }} c
  on f.channel_id = c.channel_id
where p.main_price is not null  -- filter to price-bearing mentions
group by p.product_name, c.channel_name
order by mention_count desc