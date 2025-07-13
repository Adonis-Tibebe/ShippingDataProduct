{{ config(materialized='table') }}

with enriched as (
    select
        -- 🔑 Surrogate key for the message
        m.message_metadata_id,

        -- 🔗 Channel reference
        c.channel_id,

        -- 📆 Posted date
        d_post.date as posted_date,

        -- 📆 Scraped date
        s.scraped_at as scraped_date

    from {{ ref('dim_message_metadata') }} m

    join {{ ref('stg_telegram_messages') }} s
      on m.channel_name = s.channel_name
     and m.message_id = s.message_id

    join {{ ref('dim_channel') }} c
      on m.channel_name = c.channel_name

    left join {{ ref('dim_dates') }} d_post
      on s.posted_at::date = d_post.date

)

select *
from enriched