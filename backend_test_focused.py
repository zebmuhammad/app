#!/usr/bin/env python3
"""
Focused EasyCart Backend API Tests
Testing specific issues found in the comprehensive test.
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://tradebay-4.preview.emergentagent.com/api"
TIMEOUT = 30

def test_login_with_seeded_users():
    """Test login with known seeded users"""
    print("🔍 Testing login with seeded users...")
    
    # Test users from seed_data.py
    test_users = [
        {"email": "techhub@example.com", "password": "password123"},
        {"email": "sneakerking@example.com", "password": "password123"},
        {"email": "fashion@example.com", "password": "password123"},
    ]
    
    for user in test_users:
        response = requests.post(f"{BASE_URL}/auth/login", json=user, timeout=TIMEOUT)
        print(f"Login attempt for {user['email']}: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful for {user['email']}")
            print(f"   User: {data.get('user', {}).get('name')}")
            return data.get('access_token'), data.get('user')
        else:
            print(f"❌ Login failed for {user['email']}: {response.json()}")
    
    return None, None

def test_buy_now_products():
    """Find buy now products for order testing"""
    print("\n🛒 Testing buy now products...")
    
    # Get products with buy_it_now = true
    response = requests.get(f"{BASE_URL}/products", params={"limit": 20}, timeout=TIMEOUT)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        
        buy_now_products = []
        for product in products:
            if product.get("buy_it_now") and not product.get("is_auction") and product.get("quantity", 0) > 0:
                buy_now_products.append(product)
        
        print(f"Found {len(buy_now_products)} buy now products with quantity > 0")
        
        if buy_now_products:
            for i, product in enumerate(buy_now_products[:3]):
                print(f"  {i+1}. {product['name']} - ${product['price']} (Qty: {product.get('quantity')})")
        
        return buy_now_products
    else:
        print(f"❌ Failed to get products: {response.status_code}")
        return []

def test_order_creation_with_token(access_token, products):
    """Test order creation with valid token and products"""
    if not access_token or not products:
        print("❌ Cannot test order creation - missing token or products")
        return False
    
    print("\n📦 Testing order creation...")
    
    product = products[0]  # Use first available product
    
    order_data = {
        "items": [
            {
                "product_id": product["id"],
                "quantity": 1
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "New York", 
            "state": "NY",
            "zip_code": "10001",
            "country": "USA"
        },
        "payment_method": "credit_card"
    }
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(f"{BASE_URL}/orders/create", json=order_data, headers=headers, timeout=TIMEOUT)
    
    print(f"Order creation status: {response.status_code}")
    
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order created successfully!")
        print(f"   Order ID: {order.get('id')}")
        print(f"   Total: ${order.get('total_amount')}")
        return True
    else:
        print(f"❌ Order creation failed: {response.json()}")
        return False

def test_auction_products():
    """Check for auction products"""
    print("\n🔨 Checking for auction products...")
    
    response = requests.get(f"{BASE_URL}/products", params={"limit": 50}, timeout=TIMEOUT)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", [])
        
        auction_products = [p for p in products if p.get("is_auction")]
        
        print(f"Found {len(auction_products)} auction products out of {len(products)} total")
        
        if auction_products:
            for i, product in enumerate(auction_products[:3]):
                print(f"  {i+1}. {product['name']} - Current bid: ${product.get('current_bid', 'N/A')}")
        
        return auction_products
    else:
        print(f"❌ Failed to get products: {response.status_code}")
        return []

def main():
    print("🎯 Focused EasyCart Backend API Tests")
    print("=" * 50)
    
    # Test login with seeded users
    access_token, user = test_login_with_seeded_users()
    
    # Test buy now products
    buy_now_products = test_buy_now_products()
    
    # Test order creation if we have token and products
    if access_token and buy_now_products:
        test_order_creation_with_token(access_token, buy_now_products)
    
    # Check auction products
    auction_products = test_auction_products()
    
    print("\n📊 Summary:")
    print(f"✅ Login working: {'Yes' if access_token else 'No'}")
    print(f"✅ Buy now products available: {len(buy_now_products) if buy_now_products else 0}")
    print(f"✅ Auction products available: {len(auction_products) if auction_products else 0}")

if __name__ == "__main__":
    main()