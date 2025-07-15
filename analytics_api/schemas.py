from pydantic import BaseModel
from typing import Generic, TypeVar, List, Any
from pydantic.generics import GenericModel
from datetime import datetime

# Generic type variable
T = TypeVar("T")

# Generic response wrapper
class StandardResponse(GenericModel, Generic[T]):
    success: bool = True
    count: int
    data: List[T]
 

class TopProductSchema(BaseModel):
    product_name: str
    channel_name: str
    mention_count: int

class ChannelActivitySchema(BaseModel):
    channel_name: str
    channel_id: int
    total_messages: int
    messages_with_detections: int
    media_without_detection_count: int
    detection_rate: float


class MessageSearchSchema(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    posted_at: Any

class ProductPricingSchema(BaseModel):
    product_name: str
    channel_name: str
    min_price: float
    max_price: float
    avg_price: float