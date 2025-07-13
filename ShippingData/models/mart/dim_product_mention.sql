{{ config(materialized='table') }}

with exploded as (
    select
        m.message_metadata_id,
        trim(lower(product)) as product_name,
        s.main_price
    from {{ ref('dim_message_metadata') }} m
    join {{ ref('stg_telegram_messages') }} s
        on m.channel_name = s.channel_name
        and m.message_id = s.message_id
    cross join unnest(string_to_array(m.product_names, '|')) as product
)

select *
from exploded
where length(product_name) > 2  