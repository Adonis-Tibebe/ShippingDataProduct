{{ config(materialized='table') }}

with mention_counts as (
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
),
ranked as (
    select *,
           row_number() over (
               partition by channel_name
               order by mention_count desc
           ) as rank
    from mention_counts
)
select *
from ranked
where rank <= 3
order by channel_name, rank