{{ config(materialized='table') }}

with base as (
    select
        -- Surrogate key: one unique ID per channel
        row_number() over (order by channel_name) as channel_id,

        -- Core identifiers
        channel_name,

        -- Aggregated metrics
        count(*) as total_messages,
        sum(view_count) as total_views,
        count(*) filter (where has_media) as messages_with_media,
        count(*) filter (where not has_media) as messages_without_media,
        count(*) filter (where is_health_related) as health_related_messages
    from {{ ref('stg_telegram_messages') }}
    group by channel_name
)

select *
from base
order by total_messages desc