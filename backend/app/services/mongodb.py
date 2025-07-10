from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from .models import Conversation, Message, AnalysisResult, UserPreference
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

class MongoDBService:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGODB_URI)
        self.db = self.client.ecommerce
        
    async def get_collection(self, collection_name: str):
        return self.db[collection_name]

    async def save_conversation(self, user_id: str, message: str, response: str, analysis_results: Dict[str, Any] = None):
        conversation = {
            "user_id": user_id,
            "timestamp": datetime.now(),
            "message": message,
            "response": response,
            "analysis": analysis_results,
            "type": "analysis" if analysis_results else "chat"
        }
        collection = await self.get_collection("conversations")
        result = await collection.insert_one(conversation)
        return {**conversation, "_id": result.inserted_id}

    async def get_recent_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        collection = await self.get_collection("conversations")
        cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        conversations = []
        async for doc in cursor:
            conversations.append(doc)
        return conversations

    async def save_analysis_result(self, analysis_type: str, data: Dict[str, Any]):
        collection = await self.get_collection("analysis_results")
        document = {
            "type": analysis_type,
            "data": data,
            "timestamp": datetime.now()
        }
        result = await collection.insert_one(document)
        return {**document, "_id": result.inserted_id}

    async def get_orders(self, query: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        collection = await self.get_collection("orders")
        cursor = collection.find(query or {}).limit(limit)
        orders = []
        async for doc in cursor:
            orders.append(doc)
        return orders

    async def aggregate_orders(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute an aggregation pipeline on the orders collection"""
        collection = await self.get_collection("orders")
        results = []
        async for doc in collection.aggregate(pipeline):
            results.append(doc)
        return results

    async def save_user_preference(self, user_id: str, preferences: Dict[str, Any]):
        collection = await self.get_collection("user_preferences")
        await collection.update_one(
            {"user_id": user_id},
            {"$set": {"preferences": preferences, "updated_at": datetime.now()}},
            upsert=True
        )

    async def get_user_preference(self, user_id: str) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection("user_preferences")
        return await collection.find_one({"user_id": user_id})

    async def init_data(self, csv_path: str = "data_augmented.csv"):
        """
        Load data from CSV into MongoDB 'orders' collection, luôn cập nhật lại toàn bộ dữ liệu.
        """
        collection = await self.get_collection("orders")
        # Xóa toàn bộ dữ liệu cũ
        await collection.delete_many({})
        # Đọc dữ liệu từ CSV
        df = pd.read_csv(csv_path)
        df = df.where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        if records:
            await collection.insert_many(records)
            print(f"Reloaded {len(records)} records from {csv_path} into 'orders' collection.")
        else:
            print(f"No records found in {csv_path}.")

    async def get_top_products(self, limit: int = 5):
        pipeline = [
            {"$group": {
                "_id": "$product_name",
                "product_name": {"$first": "$product_name"},
                "total_sales": {"$sum": "$sales_per_order"},
                "total_quantity": {"$sum": "$order_quantity"},
                "total_profit": {"$sum": "$profit_per_order"},
                "category": {"$first": "$category_name"},
                "price": {"$avg": "$sales_per_order"}
            }},
            {"$sort": {"total_sales": -1}},
            {"$limit": limit}
        ]
        return await self.aggregate_orders(pipeline)

    async def get_top_customers(self, limit: int = 5):
        pipeline = [
            {"$group": {
                "_id": "$customer_id",
                "customer_name": {"$first": {"$concat": ["$customer_first_name", " ", "$customer_last_name"]}},
                "total_spent": {"$sum": "$sales_per_order"},
                "total_orders": {"$sum": 1},
                "city": {"$first": "$customer_city"},
                "state": {"$first": "$customer_state"}
            }},
            {"$sort": {"total_spent": -1}},
            {"$limit": limit}
        ]
        return await self.aggregate_orders(pipeline)

    async def get_delivery_stats(self):
        pipeline = [
            {"$group": {
                "_id": "$delivery_status",
                "count": {"$sum": 1}
            }}
        ]
        return await self.aggregate_orders(pipeline)

    async def search_products_by_name(self, name: str, limit: int = 10):
        collection = await self.get_collection("orders")
        cursor = collection.find({"product_name": {"$regex": name, "$options": "i"}}).limit(limit)
        products = []
        async for doc in cursor:
            products.append(doc)
        return products
