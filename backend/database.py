from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING, TEXT
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Collections
users_collection = db.users
products_collection = db.products
orders_collection = db.orders
bids_collection = db.bids

async def create_indexes():
    """Create database indexes for better performance"""
    
    # User indexes
    await users_collection.create_index([("email", ASCENDING)], unique=True)
    
    # Product indexes
    await products_collection.create_index([("name", TEXT), ("description", TEXT)])
    await products_collection.create_index([("category", ASCENDING)])
    await products_collection.create_index([("brand", ASCENDING)])
    await products_collection.create_index([("price", ASCENDING)])
    await products_collection.create_index([("seller", ASCENDING)])
    await products_collection.create_index([("is_active", ASCENDING)])
    await products_collection.create_index([("created_at", ASCENDING)])
    
    # Order indexes
    await orders_collection.create_index([("user_id", ASCENDING)])
    await orders_collection.create_index([("status", ASCENDING)])
    await orders_collection.create_index([("created_at", ASCENDING)])
    
    # Bid indexes
    await bids_collection.create_index([("product_id", ASCENDING)])
    await bids_collection.create_index([("user_id", ASCENDING)])
    await bids_collection.create_index([("created_at", ASCENDING)])

async def close_db_connection():
    """Close database connection"""
    client.close()