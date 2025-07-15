from sqlalchemy import text
from sqlalchemy.orm import Session

def get_top_products(limit: int, db: Session):
    sql = text("""
        SELECT product_name, channel_name, mention_count
        FROM analysis.top_products
        ORDER BY mention_count DESC
        LIMIT :limit
    """)
    result = db.execute(sql, {"limit": limit})
    return result.fetchall()

from sqlalchemy import text
from sqlalchemy.orm import Session

def get_channel_activity(channel_name: str, db: Session):
    sql = text("""
        SELECT channel_name, channel_id, total_messages, messages_with_detections,  media_without_detection_count, detection_rate
        FROM analysis.media_coverage_by_channel
        WHERE channel_name = :channel_name
    """)
    result = db.execute(sql, {"channel_name": channel_name}).first()
    return result

def search_messages(query: str, db: Session):
    sql = text("""
        SELECT message_id, channel_name, message_text, posted_at
        FROM staging.stg_telegram_messages
        WHERE message_text ILIKE '%' || :query || '%'
        ORDER BY posted_at DESC
        LIMIT 20
    """)
    result = db.execute(sql, {"query": query})
    return result.fetchall()

def get_product_pricing(product_name: str, db: Session):
    sql = text("""
        SELECT product_name, channel_name, min_price, max_price, avg_price
        FROM analysis.product_price_per_channel
        WHERE product_name ILIKE :product_name
        ORDER BY channel_name
    """)
    return db.execute(sql, {"product_name": product_name}).fetchall()