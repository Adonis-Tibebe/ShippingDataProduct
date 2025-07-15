{{ config(materialized='table') }}

select
    p.product_name,
    c.channel_name,
    count(*) as mention_count
from {{ ref('dim_product_mention') }} p
join {{ ref('fct_messages') }} f
  on p.message_metadata_id = f.message_metadata_id
join {{ ref('dim_channel') }} c
  on f.channel_id = c.channel_id
group by p.product_name, c.channel_name
order by mention_count desc
limit 100