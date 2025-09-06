from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models.user import UserResponse, UserUpdate
from models.product import ProductResponse
from models.order import OrderResponse
from database import users_collection, products_collection, orders_collection
from auth import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: UserResponse = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    """Update current user's profile"""
    update_data = {}
    if user_update.name is not None:
        update_data["name"] = user_update.name
    if user_update.avatar is not None:
        update_data["avatar"] = user_update.avatar
    
    if update_data:
        await users_collection.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": update_data}
        )
        
        # Get updated user data
        updated_user = await users_collection.find_one({"_id": ObjectId(current_user.id)})
        return UserResponse(
            id=str(updated_user["_id"]),
            name=updated_user["name"],
            email=updated_user["email"],
            avatar=updated_user["avatar"],
            rating=updated_user["rating"],
            member_since=updated_user["member_since"],
            is_verified=updated_user["is_verified"]
        )
    
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(current_user: UserResponse = Depends(get_current_user)):
    """Get current user's order history"""
    cursor = orders_collection.find({"user_id": ObjectId(current_user.id)}).sort("created_at", -1)
    orders = await cursor.to_list(length=100)
    
    order_responses = []
    for order in orders:
        order_responses.append(OrderResponse(
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
        ))
    
    return order_responses

@router.get("/watchlist", response_model=List[ProductResponse])
async def get_user_watchlist(current_user: UserResponse = Depends(get_current_user)):
    """Get current user's watchlist"""
    # Get user's watchlist
    user = await users_collection.find_one({"_id": ObjectId(current_user.id)})
    if not user or not user.get("watchlist"):
        return []
    
    # Get products in watchlist
    watchlist_ids = [ObjectId(pid) for pid in user["watchlist"] if ObjectId.is_valid(str(pid))]
    cursor = products_collection.find({"_id": {"$in": watchlist_ids}, "is_active": True})
    products = await cursor.to_list(length=100)
    
    product_responses = []
    for product in products:
        product_responses.append(ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            description=product["description"],
            price=product["price"],
            original_price=product.get("original_price"),
            images=product["images"],
            category=product["category"],
            subcategory=product.get("subcategory"),
            condition=product["condition"],
            listing_type=product["listing_type"],
            seller=str(product["seller"]),
            seller_name=product["seller_name"],
            is_auction=product["is_auction"],
            auction_end_time=product.get("auction_end_time"),
            current_bid=product.get("current_bid"),
            bid_count=product["bid_count"],
            buy_it_now=product["buy_it_now"],
            quantity=product["quantity"],
            brand=product.get("brand"),
            rating=product["rating"],
            review_count=product["review_count"],
            created_at=product["created_at"]
        ))
    
    return product_responses

@router.post("/watchlist/{product_id}", response_model=dict)
async def add_to_watchlist(
    product_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Add product to user's watchlist"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    # Check if product exists
    product = await products_collection.find_one({"_id": ObjectId(product_id), "is_active": True})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Add to watchlist (using $addToSet to avoid duplicates)
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"watchlist": ObjectId(product_id)}}
    )
    
    return {"message": "Product added to watchlist"}

@router.delete("/watchlist/{product_id}", response_model=dict)
async def remove_from_watchlist(
    product_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    """Remove product from user's watchlist"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    # Remove from watchlist
    await users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"watchlist": ObjectId(product_id)}}
    )
    
    return {"message": "Product removed from watchlist"}