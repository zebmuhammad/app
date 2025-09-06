from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from models.user import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image: str

class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "United States"

class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    user_name: str
    items: List[OrderItem]
    total_amount: float
    tax_amount: float
    shipping_amount: float = 0.0
    status: str = "Processing"  # Processing, In Transit, Delivered, Cancelled
    shipping_address: Optional[ShippingAddress] = None
    payment_method: str = "Credit Card"
    tracking_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OrderCreate(BaseModel):
    items: List[OrderItem]
    shipping_address: ShippingAddress
    payment_method: str = "Credit Card"

class OrderResponse(BaseModel):
    id: str
    user_name: str
    items: List[OrderItem]
    total_amount: float
    tax_amount: float
    shipping_amount: float
    status: str
    shipping_address: Optional[ShippingAddress]
    payment_method: str
    tracking_number: Optional[str]
    created_at: datetime