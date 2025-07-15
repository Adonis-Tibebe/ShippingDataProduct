{{ config(materialized='table') }}

select
  chan.channel_name,
  chan.channel_id,
  count(distinct msg.message_metadata_id) as total_messages,
  count(distinct media.message_metadata_id) as messages_with_detections,
  count(*) filter (
    where media.label = 'no_object_detected'
  ) as media_without_detection_count,
  round(
    count(distinct media.message_metadata_id)::numeric / nullif(count(distinct msg.message_metadata_id), 0),
    2
  ) as detection_rate
from {{ ref('fct_messages') }} msg
join {{ ref('dim_channel') }} chan
  on msg.channel_id = chan.channel_id
left join {{ ref('fct_media') }} media
  on msg.message_metadata_id = media.message_metadata_id
group by chan.channel_name, chan.channel_id
order by detection_rate desc