from fastapi import APIRouter, HTTPException
from datetime import datetime
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.mongodb import get_collection

router = APIRouter()

@router.get("/")
async def get_orders():
    try:
        collection = get_collection("orders")
        orders = list(collection.find({}, {"_id": 0}).limit(10))
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_order(order: dict):
    try:
        collection = get_collection("orders")
        order["created_at"] = datetime.now()
        result = collection.insert_one(order)
        return {"message": "Order created successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
