{{ config(materialized='table') }}

select
  detection_id,
  message_id,
  channel_name,
  image_path,
  lower(label) as label,
  cast(confidence as float) as confidence
from {{ source('raw', 'media_detections') }}