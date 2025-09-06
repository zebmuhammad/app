from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from models.product import Product, ProductCreate, ProductUpdate, ProductResponse, Bid
from models.user import UserResponse
from database import products_collection, bids_collection, users_collection
from auth import get_current_user, get_current_user_optional
from bson import ObjectId
from datetime import datetime
import math

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=dict)
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    listing_type: Optional[str] = None,
    brand: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc"
):
    """Get products with filtering, search, and pagination"""
    # Build filter query
    filter_query = {"is_active": True}
    
    if category:
        filter_query["category"] = category
    
    if search:
        filter_query["$text"] = {"$search": search}
    
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filter_query["price"] = price_filter
    
    if condition:
        filter_query["condition"] = condition
    
    if listing_type:
        filter_query["listing_type"] = listing_type
    
    if brand:
        filter_query["brand"] = brand
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Sort configuration
    sort_direction = -1 if sort_order == "desc" else 1
    sort_field = sort_by
    
    # Special sorting for ending soon (auctions)
    if sort_by == "ending_soon":
        sort_field = "auction_end_time"
        filter_query["is_auction"] = True
        filter_query["auction_end_time"] = {"$gte": datetime.utcnow()}
    
    # Get total count for pagination
    total_count = await products_collection.count_documents(filter_query)
    total_pages = math.ceil(total_count / limit)
    
    # Get products
    cursor = products_collection.find(filter_query).sort(sort_field, sort_direction).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    
    # Convert to response format
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
    
    return {
        "products": product_responses,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_count": total_count,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

@router.get("/categories", response_model=List[str])
async def get_categories():
    """Get all product categories"""
    categories = await products_collection.distinct("category")
    return categories

@router.get("/search", response_model=dict)
async def search_products(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None
):
    """Search products by name and description"""
    filter_query = {
        "is_active": True,
        "$text": {"$search": q}
    }
    
    if category and category != "All Categories":
        filter_query["category"] = category
    
    # Calculate skip value for pagination
    skip = (page - 1) * limit
    
    # Get total count
    total_count = await products_collection.count_documents(filter_query)
    total_pages = math.ceil(total_count / limit)
    
    # Get products with text search score
    cursor = products_collection.find(
        filter_query,
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).skip(skip).limit(limit)
    
    products = await cursor.to_list(length=limit)
    
    # Convert to response format
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
    
    return {
        "products": product_responses,
        "query": q,
        "pagination": {
            "current_page": page,
            "total_pages": total_pages,
            "total_count": total_count,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get single product by ID"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    product = await products_collection.find_one({"_id": ObjectId(product_id), "is_active": True})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return ProductResponse(
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
    )

@router.post("/{product_id}/bid", response_model=dict)
async def place_bid(
    product_id: str,
    bid_amount: float,
    current_user: UserResponse = Depends(get_current_user)
):
    """Place a bid on an auction item"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    # Get product
    product = await products_collection.find_one({"_id": ObjectId(product_id), "is_active": True})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if it's an auction
    if not product["is_auction"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This item is not an auction"
        )
    
    # Check if auction has ended
    if product["auction_end_time"] and product["auction_end_time"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This auction has ended"
        )
    
    # Check if bid amount is higher than current bid
    current_bid = product.get("current_bid", product["price"])
    if bid_amount <= current_bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bid amount must be higher than current bid of ${current_bid}"
        )
    
    # Create bid record
    bid = Bid(
        product_id=ObjectId(product_id),
        user_id=ObjectId(current_user.id),
        user_name=current_user.name,
        amount=bid_amount
    )
    
    # Insert bid and update product
    await bids_collection.insert_one(bid.dict(by_alias=True))
    await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {"current_bid": bid_amount},
            "$inc": {"bid_count": 1}
        }
    )
    
    return {
        "message": "Bid placed successfully",
        "bid_amount": bid_amount,
        "current_bid": bid_amount
    }

@router.get("/{product_id}/bids", response_model=List[dict])
async def get_product_bids(product_id: str):
    """Get bid history for a product"""
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )
    
    # Get bids for the product
    cursor = bids_collection.find({"product_id": ObjectId(product_id)}).sort("created_at", -1)
    bids = await cursor.to_list(length=100)
    
    bid_history = []
    for bid in bids:
        bid_history.append({
            "user_name": bid["user_name"],
            "amount": bid["amount"],
            "created_at": bid["created_at"]
        })
    
    return bid_history