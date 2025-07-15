{{ config(materialized='table') }}

with base as (
    select *
    from {{ ref('stg_media_detections') }}
),

joined as (
    select
        base.detection_id as media_detection_id,
        base.message_id,
        meta.message_metadata_id,
        chan.channel_id,
        base.label,
        base.confidence
    from base
    left join {{ ref('dim_message_metadata') }} meta
        on base.message_id = meta.message_id
    left join {{ ref('dim_channel') }} chan
        on base.channel_name = chan.channel_name
)

select * from joined
where message_metadata_id is not null