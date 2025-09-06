#!/usr/bin/env python3
"""
Final EasyCart Backend API Tests
Testing with corrected order creation and auction bidding.
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://tradebay-4.preview.emergentagent.com/api"
TIMEOUT = 30

def get_auth_token():
    """Get authentication token"""
    login_data = {"email": "techhub@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=TIMEOUT)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token'), data.get('user')
    return None, None

def test_order_creation_corrected():
    """Test order creation with correct format"""
    print("📦 Testing corrected order creation...")
    
    access_token, user = get_auth_token()
    if not access_token:
        print("❌ Cannot test order creation - no auth token")
        return False
    
    # Get a buy now product
    response = requests.get(f"{BASE_URL}/products", params={"limit": 20}, timeout=TIMEOUT)
    
    if response.status_code != 200:
        print("❌ Cannot get products")
        return False
    
    products = response.json().get("products", [])
    buy_now_products = [p for p in products if p.get("buy_it_now") and not p.get("is_auction") and p.get("quantity", 0) > 0]
    
    if not buy_now_products:
        print("❌ No buy now products available")
        return False
    
    product = buy_now_products[0]
    
    # Create order with full OrderItem structure (as expected by the model)
    order_data = {
        "items": [
            {
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "image": product["images"][0] if product["images"] else ""
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
        print(f"   Tax: ${order.get('tax_amount')}")
        return True
    else:
        print(f"❌ Order creation failed: {response.json()}")
        return False

def test_auction_bidding():
    """Test auction bidding functionality"""
    print("\n🔨 Testing auction bidding...")
    
    access_token, user = get_auth_token()
    if not access_token:
        print("❌ Cannot test bidding - no auth token")
        return False
    
    # Get auction products
    response = requests.get(f"{BASE_URL}/products", params={"limit": 50}, timeout=TIMEOUT)
    
    if response.status_code != 200:
        print("❌ Cannot get products")
        return False
    
    products = response.json().get("products", [])
    auction_products = [p for p in products if p.get("is_auction")]
    
    if not auction_products:
        print("❌ No auction products available")
        return False
    
    auction_product = auction_products[0]
    product_id = auction_product["id"]
    current_bid = auction_product.get("current_bid", auction_product["price"])
    
    print(f"Testing bid on: {auction_product['name']}")
    print(f"Current bid: ${current_bid}")
    
    # Place a bid (higher than current bid)
    bid_amount = current_bid + 10.0
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # The bid endpoint expects bid_amount as a query parameter
    response = requests.post(
        f"{BASE_URL}/products/{product_id}/bid",
        headers=headers,
        params={"bid_amount": bid_amount},
        timeout=TIMEOUT
    )
    
    print(f"Bid placement status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Bid placed successfully!")
        print(f"   Bid amount: ${result.get('bid_amount')}")
        print(f"   New current bid: ${result.get('current_bid')}")
        
        # Test getting bid history
        response = requests.get(f"{BASE_URL}/products/{product_id}/bids", timeout=TIMEOUT)
        
        if response.status_code == 200:
            bids = response.json()
            print(f"✅ Retrieved {len(bids)} bids from history")
            if bids:
                latest_bid = bids[0]
                print(f"   Latest bid: ${latest_bid.get('amount')} by {latest_bid.get('user_name')}")
        
        return True
    else:
        print(f"❌ Bid placement failed: {response.json()}")
        return False

def test_comprehensive_api():
    """Run comprehensive API tests"""
    print("🚀 Final EasyCart Backend API Tests")
    print("=" * 50)
    
    results = {
        "auth": False,
        "products": False,
        "search": False,
        "categories": False,
        "product_detail": False,
        "user_profile": False,
        "watchlist": False,
        "order_creation": False,
        "auction_bidding": False
    }
    
    # Test authentication
    print("\n📝 Testing Authentication...")
    access_token, user = get_auth_token()
    if access_token:
        print(f"✅ Authentication successful for {user.get('name')}")
        results["auth"] = True
    else:
        print("❌ Authentication failed")
    
    # Test products list
    print("\n🛍️ Testing Products List...")
    response = requests.get(f"{BASE_URL}/products", params={"limit": 10}, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data.get('products', []))} products")
        print(f"   Total products in database: {data.get('pagination', {}).get('total_count')}")
        results["products"] = True
    else:
        print(f"❌ Products list failed: {response.status_code}")
    
    # Test search
    print("\n🔍 Testing Product Search...")
    response = requests.get(f"{BASE_URL}/products/search", params={"q": "Nike", "limit": 5}, timeout=TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search found {data.get('pagination', {}).get('total_count')} Nike products")
        results["search"] = True
    else:
        print(f"❌ Product search failed: {response.status_code}")
    
    # Test categories
    print("\n📂 Testing Categories...")
    response = requests.get(f"{BASE_URL}/products/categories", timeout=TIMEOUT)
    if response.status_code == 200:
        categories = response.json()
        print(f"✅ Retrieved {len(categories)} categories: {', '.join(categories)}")
        results["categories"] = True
    else:
        print(f"❌ Categories failed: {response.status_code}")
    
    # Test product detail
    print("\n📄 Testing Product Detail...")
    response = requests.get(f"{BASE_URL}/products", params={"limit": 1}, timeout=TIMEOUT)
    if response.status_code == 200:
        products = response.json().get("products", [])
        if products:
            product_id = products[0]["id"]
            response = requests.get(f"{BASE_URL}/products/{product_id}", timeout=TIMEOUT)
            if response.status_code == 200:
                product = response.json()
                print(f"✅ Retrieved product detail for {product.get('name')}")
                results["product_detail"] = True
            else:
                print(f"❌ Product detail failed: {response.status_code}")
    
    if access_token:
        # Test user profile
        print("\n👤 Testing User Profile...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/users/profile", headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Retrieved profile for {profile.get('name')}")
            results["user_profile"] = True
        else:
            print(f"❌ User profile failed: {response.status_code}")
        
        # Test watchlist
        print("\n⭐ Testing Watchlist...")
        # Get a product to add to watchlist
        response = requests.get(f"{BASE_URL}/products", params={"limit": 1}, timeout=TIMEOUT)
        if response.status_code == 200:
            products = response.json().get("products", [])
            if products:
                product_id = products[0]["id"]
                
                # Add to watchlist
                response = requests.post(f"{BASE_URL}/users/watchlist/{product_id}", headers=headers, timeout=TIMEOUT)
                if response.status_code == 200:
                    print("✅ Added product to watchlist")
                    
                    # Get watchlist
                    response = requests.get(f"{BASE_URL}/users/watchlist", headers=headers, timeout=TIMEOUT)
                    if response.status_code == 200:
                        watchlist = response.json()
                        print(f"✅ Retrieved watchlist with {len(watchlist)} items")
                        results["watchlist"] = True
                    
                    # Remove from watchlist
                    requests.delete(f"{BASE_URL}/users/watchlist/{product_id}", headers=headers, timeout=TIMEOUT)
    
    # Test order creation
    results["order_creation"] = test_order_creation_corrected()
    
    # Test auction bidding
    results["auction_bidding"] = test_auction_bidding()
    
    # Summary
    print("\n📊 Final Test Summary")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    return results

if __name__ == "__main__":
    test_comprehensive_api()