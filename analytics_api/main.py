from fastapi import FastAPI, Depends
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from crud import (get_top_products, get_channel_activity,
                   search_messages, get_product_pricing)
from schemas import (TopProductSchema, StandardResponse, ChannelActivitySchema, 
                     MessageSearchSchema, ProductPricingSchema)
import json

app = FastAPI(
    title="Analytical API for Telegram Health Insights",
    description="Serves insights from dbt models: product mentions, pricing trends, media coverage, and search.",
    version="1.0.0"
)

# CORS setup — adjust allow_origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic API health-check for testing
@app.get("/api/health-check")
def health_check():
    return {"status": "ok", "message": "API is alive"}

# Database connectivity check — using SELECT 1
@app.get("/api/db-check")
def db_check(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {"db_status": "connected", "query_result": result}
    except Exception as e:
        return {"db_status": "error", "details": str(e)}
    
# Top products route
@app.get("/api/reports/top-products", response_model=list[TopProductSchema])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    data = get_top_products(limit, db)
    payload = [TopProductSchema(**row._mapping) for row in data]
    response = StandardResponse(
        success=True,
        count=len(payload),
        data=payload
    )
    json_str = json.dumps(
        response.dict(),
        indent=2,               
        ensure_ascii=False      
    )
    
    return Response(
        content=json_str,
        media_type="application/json",
        status_code=200
    )

from schemas import ChannelActivitySchema, StandardResponse
from crud import get_channel_activity

@app.get("/api/channels/{channel_name}/activity", response_model=StandardResponse[ChannelActivitySchema])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    row = get_channel_activity(channel_name, db)

    if not row:
        response = StandardResponse(success=False, count=0, data=None)
        return Response(content=json.dumps(response.dict(), indent=2, ensure_ascii=False), media_type="application/json", status_code=404)

    payload = [ChannelActivitySchema(**row._mapping)]
    response = StandardResponse(success=True, count=1, data=payload)

    json_str = json.dumps(response.dict(), indent=2, ensure_ascii=False)
    return Response(content=json_str, media_type="application/json", status_code=200)


from schemas import MessageSearchSchema, StandardResponse
from crud import search_messages

@app.get("/api/search/messages", response_model=StandardResponse[list[MessageSearchSchema]])
def search_messages_route(query: str, db: Session = Depends(get_db)):
    raw_data = search_messages(query, db)
    payload = [MessageSearchSchema(**row._mapping) for row in raw_data]

    response = StandardResponse(
        success=True,
        count=len(payload),
        data=payload
    )
    json_str = json.dumps(response.dict(), indent=2, ensure_ascii=False, default=str)
    return Response(content=json_str, media_type="application/json", status_code=200)

@app.get("/api/reports/product-pricing", response_model=StandardResponse[list[ProductPricingSchema]])
def product_pricing(product_name: str, db: Session = Depends(get_db)):
    raw_data = get_product_pricing(product_name, db)
    payload = [ProductPricingSchema(**row._mapping) for row in raw_data]

    response = StandardResponse(
        success=True,
        count=len(payload),
        data=payload
    )
    json_str = json.dumps(response.dict(), indent=2, ensure_ascii=False, default=str)
    return Response(content=json_str, media_type="application/json", status_code=200)
