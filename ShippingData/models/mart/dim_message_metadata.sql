{{ config(materialized='table') }}

with base as (
    select
        -- Surrogate key for each message
        row_number() over (order by channel_name, message_id) as message_metadata_id,

        -- Composite identifiers
        channel_name,
        message_id,

        -- Raw descriptors
        message_text,
        message_length,
        product_names,
        is_health_related,
        view_count,
        has_media
    from {{ ref('stg_telegram_messages') }}
)

select *
from base