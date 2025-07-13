{{ config(materialized='table') }}

with source_data as (
    select
        -- Message metadata
        raw.message_id,
        raw.channel_name,
        raw.scraped_at,
        (raw.raw_data->>'date')::timestamp     as posted_at,
        raw.raw_data->>'message'               as message_text,
        length(raw.raw_data->>'message')       as message_length,

        -- Extracted enrichment
        enriched.product_names,
        enriched.main_price,
        enriched.is_health_related,

        -- ✅ New: View count from raw_data
        (raw.raw_data->>'views')::integer      as view_count,

        -- ✅ New: Media presence flag
        case
            when raw.raw_data->'media' is not null then true
            else false
        end as has_media

    from raw.telegram_messages raw
    left join raw.telegram_enriched enriched
      on raw.channel_name = enriched.channel_name
     and raw.message_id = enriched.message_id
)

select * from source_data