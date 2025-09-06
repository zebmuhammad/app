from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models.user import PyObjectId

class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    images: List[str]
    category: str
    subcategory: Optional[str] = None
    condition: str = "New"  # New, Used, Refurbished, For parts
    listing_type: str = "Buy It Now"  # Auction, Buy It Now, Best Offer
    seller: PyObjectId
    seller_name: str
    is_auction: bool = False
    auction_end_time: Optional[datetime] = None
    current_bid: Optional[float] = None
    bid_count: int = 0
    buy_it_now: bool = True
    quantity: int = 1
    brand: Optional[str] = None
    rating: float = 4.5
    review_count: int = 0
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    original_price: Optional[float] = None
    images: List[str]
    category: str
    subcategory: Optional[str] = None
    condition: str = "New"
    listing_type: str = "Buy It Now"
    is_auction: bool = False
    auction_end_time: Optional[datetime] = None
    buy_it_now: bool = True
    quantity: int = 1
    brand: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    images: Optional[List[str]] = None
    condition: Optional[str] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    original_price: Optional[float]
    images: List[str]
    category: str
    subcategory: Optional[str]
    condition: str
    listing_type: str
    seller: str
    seller_name: str
    is_auction: bool
    auction_end_time: Optional[datetime]
    current_bid: Optional[float]
    bid_count: int
    buy_it_now: bool
    quantity: int
    brand: Optional[str]
    rating: float
    review_count: int
    created_at: datetime

class Bid(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_id: PyObjectId
    user_id: PyObjectId
    user_name: str
    amount: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}