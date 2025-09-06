from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models.order import Order, OrderCreate, OrderResponse, OrderItem
from models.user import UserResponse
from database import orders_collection, products_collection
from auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/create", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Create a new order"""
    # Validate all products exist and calculate total
    total_amount = 0
    validated_items = []
    
    for item in order_data.items:
        if not ObjectId.is_valid(item.product_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid product ID: {item.product_id}"
            )
        
        product = await products_collection.find_one({"_id": ObjectId(item.product_id), "is_active": True})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: {item.product_id}"
            )
        
        # Check if product is available (not auction or has quantity)
        if product["is_auction"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot purchase auction item: {product['name']}"
            )
        
        if product["quantity"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient quantity for {product['name']}"
            )
        
        validated_items.append(OrderItem(
            product_id=item.product_id,
            name=product["name"],
            price=product["price"],
            quantity=item.quantity,
            image=product["images"][0] if product["images"] else ""
        ))
        
        total_amount += product["price"] * item.quantity
    
    # Calculate tax (8% for demo)
    tax_amount = total_amount * 0.08
    
    # Create order
    order = Order(
        user_id=ObjectId(current_user.id),
        user_name=current_user.name,
        items=validated_items,
        total_amount=total_amount,
        tax_amount=tax_amount,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method
    )
    
    # Insert order
    result = await orders_collection.insert_one(order.dict(by_alias=True))
    
    # Update product quantities
    for item in validated_items:
        await products_collection.update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"quantity": -item.quantity}}
        )
    
    return OrderResponse(
        id=str(result.inserted_id),
        user_name=order.user_name,
        items=order.items,
        total_amount=order.total_amount,
        tax_amount=order.tax_amount,
        shipping_amount=order.shipping_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        tracking_number=order.tracking_number,
        created_at=order.created_at
    )

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get order details"""
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid order ID"
        )
    
    order = await orders_collection.find_one({
        "_id": ObjectId(order_id),
        "user_id": ObjectId(current_user.id)
    })
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponse(
        id=str(order["_id"]),
        user_name=order["user_name"],
        items=order["items"],
        total_amount=order["total_amount"],
        tax_amount=order["tax_amount"],
        shipping_amount=order["shipping_amount"],
        status=order["status"],
        shipping_address=order.get("shipping_address"),
        payment_method=order["payment_method"],
        tracking_number=order.get("tracking_number"),
        created_at=order["created_at"]
    )