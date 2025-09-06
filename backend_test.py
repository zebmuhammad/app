#!/usr/bin/env python3
"""
EasyCart Backend API Test Suite
Tests all backend APIs comprehensively including authentication, products, users, and orders.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "https://tradebay-4.preview.emergentagent.com/api"
TIMEOUT = 30

class EasyCartAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        self.access_token = None
        self.current_user = None
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str, details: Dict = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request with error handling"""
        url = f"{BASE_URL}{endpoint}"
        request_headers = {"Content-Type": "application/json"}
        
        if self.access_token:
            request_headers["Authorization"] = f"Bearer {self.access_token}"
        
        if headers:
            request_headers.update(headers)
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=request_headers, params=params)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=request_headers, json=data, params=params)
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=request_headers, json=data, params=params)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=request_headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "headers": {}
            }
        except json.JSONDecodeError:
            return {
                "status_code": response.status_code,
                "data": {"error": "Invalid JSON response", "content": response.text[:200]},
                "headers": dict(response.headers)
            }

    def test_auth_register(self):
        """Test user registration"""
        test_user = {
            "name": "Sarah Johnson",
            "email": f"sarah.johnson.{int(time.time())}@example.com",
            "password": "SecurePass123!"
        }
        
        response = self.make_request("POST", "/auth/register", test_user)
        
        if response["status_code"] == 200:
            data = response["data"]
            if "access_token" in data and "user" in data:
                self.access_token = data["access_token"]
                self.current_user = data["user"]
                self.log_test("Auth Registration", True, "User registered successfully", {
                    "user_id": data["user"]["id"],
                    "user_name": data["user"]["name"],
                    "token_type": data.get("token_type")
                })
                return True
            else:
                self.log_test("Auth Registration", False, "Missing required fields in response", data)
        else:
            self.log_test("Auth Registration", False, f"Registration failed with status {response['status_code']}", response["data"])
        
        return False

    def test_auth_login(self):
        """Test user login with existing user"""
        # Try to login with a seeded user
        login_data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }
        
        response = self.make_request("POST", "/auth/login", login_data)
        
        if response["status_code"] == 200:
            data = response["data"]
            if "access_token" in data and "user" in data:
                self.access_token = data["access_token"]
                self.current_user = data["user"]
                self.log_test("Auth Login", True, "User logged in successfully", {
                    "user_id": data["user"]["id"],
                    "user_name": data["user"]["name"]
                })
                return True
            else:
                self.log_test("Auth Login", False, "Missing required fields in response", data)
        else:
            self.log_test("Auth Login", False, f"Login failed with status {response['status_code']}", response["data"])
        
        return False

    def test_auth_me(self):
        """Test getting current user info"""
        if not self.access_token:
            self.log_test("Auth Me", False, "No access token available")
            return False
        
        response = self.make_request("GET", "/auth/me")
        
        if response["status_code"] == 200:
            data = response["data"]
            if "id" in data and "name" in data and "email" in data:
                self.log_test("Auth Me", True, "Current user info retrieved successfully", {
                    "user_id": data["id"],
                    "user_name": data["name"]
                })
                return True
            else:
                self.log_test("Auth Me", False, "Missing required user fields", data)
        else:
            self.log_test("Auth Me", False, f"Get current user failed with status {response['status_code']}", response["data"])
        
        return False

    def test_auth_logout(self):
        """Test user logout"""
        if not self.access_token:
            self.log_test("Auth Logout", False, "No access token available")
            return False
        
        response = self.make_request("POST", "/auth/logout")
        
        if response["status_code"] == 200:
            self.log_test("Auth Logout", True, "User logged out successfully")
            return True
        else:
            self.log_test("Auth Logout", False, f"Logout failed with status {response['status_code']}", response["data"])
        
        return False

    def test_products_list(self):
        """Test getting products list with pagination"""
        response = self.make_request("GET", "/products", params={"page": 1, "limit": 10})
        
        if response["status_code"] == 200:
            data = response["data"]
            if "products" in data and "pagination" in data:
                products = data["products"]
                pagination = data["pagination"]
                
                self.log_test("Products List", True, f"Retrieved {len(products)} products", {
                    "total_count": pagination.get("total_count"),
                    "current_page": pagination.get("current_page"),
                    "total_pages": pagination.get("total_pages")
                })
                return True
            else:
                self.log_test("Products List", False, "Missing products or pagination in response", data)
        else:
            self.log_test("Products List", False, f"Get products failed with status {response['status_code']}", response["data"])
        
        return False

    def test_products_categories(self):
        """Test getting product categories"""
        response = self.make_request("GET", "/products/categories")
        
        if response["status_code"] == 200:
            categories = response["data"]
            if isinstance(categories, list) and len(categories) > 0:
                self.log_test("Products Categories", True, f"Retrieved {len(categories)} categories", {
                    "categories": categories[:5]  # Show first 5 categories
                })
                return True
            else:
                self.log_test("Products Categories", False, "No categories found or invalid format", categories)
        else:
            self.log_test("Products Categories", False, f"Get categories failed with status {response['status_code']}", response["data"])
        
        return False

    def test_products_search(self):
        """Test product search functionality"""
        search_queries = ["iPhone", "Nike", "laptop"]
        
        for query in search_queries:
            response = self.make_request("GET", "/products/search", params={"q": query, "limit": 5})
            
            if response["status_code"] == 200:
                data = response["data"]
                if "products" in data and "pagination" in data:
                    products = data["products"]
                    self.log_test(f"Products Search ({query})", True, f"Found {len(products)} products for '{query}'", {
                        "query": query,
                        "total_count": data["pagination"].get("total_count")
                    })
                else:
                    self.log_test(f"Products Search ({query})", False, "Missing products or pagination in response", data)
                    return False
            else:
                self.log_test(f"Products Search ({query})", False, f"Search failed with status {response['status_code']}", response["data"])
                return False
        
        return True

    def test_products_filtering(self):
        """Test product filtering by category, price, condition"""
        # Test category filtering
        response = self.make_request("GET", "/products", params={"category": "electronics", "limit": 5})
        
        if response["status_code"] == 200:
            data = response["data"]
            if "products" in data:
                electronics_count = len(data["products"])
                self.log_test("Products Filter (Category)", True, f"Found {electronics_count} electronics products")
            else:
                self.log_test("Products Filter (Category)", False, "Missing products in response", data)
                return False
        else:
            self.log_test("Products Filter (Category)", False, f"Category filter failed with status {response['status_code']}", response["data"])
            return False
        
        # Test price filtering
        response = self.make_request("GET", "/products", params={"min_price": 100, "max_price": 500, "limit": 5})
        
        if response["status_code"] == 200:
            data = response["data"]
            if "products" in data:
                price_filtered_count = len(data["products"])
                self.log_test("Products Filter (Price)", True, f"Found {price_filtered_count} products in $100-$500 range")
            else:
                self.log_test("Products Filter (Price)", False, "Missing products in response", data)
                return False
        else:
            self.log_test("Products Filter (Price)", False, f"Price filter failed with status {response['status_code']}", response["data"])
            return False
        
        return True

    def test_product_detail(self):
        """Test getting single product details"""
        # First get a product ID from the products list
        response = self.make_request("GET", "/products", params={"limit": 1})
        
        if response["status_code"] != 200 or not response["data"].get("products"):
            self.log_test("Product Detail", False, "Could not get product list to test detail")
            return False
        
        product_id = response["data"]["products"][0]["id"]
        
        # Now test getting the product detail
        response = self.make_request("GET", f"/products/{product_id}")
        
        if response["status_code"] == 200:
            product = response["data"]
            if "id" in product and "name" in product and "price" in product:
                self.log_test("Product Detail", True, f"Retrieved product details for {product['name']}", {
                    "product_id": product["id"],
                    "product_name": product["name"],
                    "price": product["price"]
                })
                return True
            else:
                self.log_test("Product Detail", False, "Missing required product fields", product)
        else:
            self.log_test("Product Detail", False, f"Get product detail failed with status {response['status_code']}", response["data"])
        
        return False

    def test_user_profile(self):
        """Test getting and updating user profile"""
        if not self.access_token:
            self.log_test("User Profile", False, "No access token available")
            return False
        
        # Test getting profile
        response = self.make_request("GET", "/users/profile")
        
        if response["status_code"] == 200:
            profile = response["data"]
            if "id" in profile and "name" in profile:
                self.log_test("User Profile Get", True, f"Retrieved profile for {profile['name']}")
                
                # Test updating profile
                update_data = {"name": f"Updated {profile['name']}"}
                response = self.make_request("PUT", "/users/profile", update_data)
                
                if response["status_code"] == 200:
                    updated_profile = response["data"]
                    self.log_test("User Profile Update", True, f"Updated profile name to {updated_profile['name']}")
                    return True
                else:
                    self.log_test("User Profile Update", False, f"Profile update failed with status {response['status_code']}", response["data"])
            else:
                self.log_test("User Profile Get", False, "Missing required profile fields", profile)
        else:
            self.log_test("User Profile Get", False, f"Get profile failed with status {response['status_code']}", response["data"])
        
        return False

    def test_user_watchlist(self):
        """Test watchlist functionality"""
        if not self.access_token:
            self.log_test("User Watchlist", False, "No access token available")
            return False
        
        # Get a product ID to add to watchlist
        response = self.make_request("GET", "/products", params={"limit": 1})
        
        if response["status_code"] != 200 or not response["data"].get("products"):
            self.log_test("User Watchlist", False, "Could not get product to test watchlist")
            return False
        
        product_id = response["data"]["products"][0]["id"]
        
        # Add to watchlist
        response = self.make_request("POST", f"/users/watchlist/{product_id}")
        
        if response["status_code"] == 200:
            self.log_test("Watchlist Add", True, "Product added to watchlist successfully")
            
            # Get watchlist
            response = self.make_request("GET", "/users/watchlist")
            
            if response["status_code"] == 200:
                watchlist = response["data"]
                self.log_test("Watchlist Get", True, f"Retrieved watchlist with {len(watchlist)} items")
                
                # Remove from watchlist
                response = self.make_request("DELETE", f"/users/watchlist/{product_id}")
                
                if response["status_code"] == 200:
                    self.log_test("Watchlist Remove", True, "Product removed from watchlist successfully")
                    return True
                else:
                    self.log_test("Watchlist Remove", False, f"Remove from watchlist failed with status {response['status_code']}", response["data"])
            else:
                self.log_test("Watchlist Get", False, f"Get watchlist failed with status {response['status_code']}", response["data"])
        else:
            self.log_test("Watchlist Add", False, f"Add to watchlist failed with status {response['status_code']}", response["data"])
        
        return False

    def test_auction_bidding(self):
        """Test auction bidding functionality"""
        if not self.access_token:
            self.log_test("Auction Bidding", False, "No access token available")
            return False
        
        # Find an auction item
        response = self.make_request("GET", "/products", params={"listing_type": "auction", "limit": 5})
        
        if response["status_code"] != 200:
            self.log_test("Auction Bidding", False, "Could not get products to find auction items")
            return False
        
        products = response["data"].get("products", [])
        auction_products = [p for p in products if p.get("is_auction")]
        
        if not auction_products:
            self.log_test("Auction Bidding", True, "No auction items found to test bidding (this is acceptable)")
            return True
        
        auction_product = auction_products[0]
        product_id = auction_product["id"]
        current_bid = auction_product.get("current_bid", auction_product["price"])
        
        # Place a bid (higher than current bid)
        bid_amount = current_bid + 10.0
        response = self.make_request("POST", f"/products/{product_id}/bid", params={"bid_amount": bid_amount})
        
        if response["status_code"] == 200:
            self.log_test("Auction Bidding", True, f"Successfully placed bid of ${bid_amount}")
            
            # Get bid history
            response = self.make_request("GET", f"/products/{product_id}/bids")
            
            if response["status_code"] == 200:
                bids = response["data"]
                self.log_test("Auction Bid History", True, f"Retrieved {len(bids)} bids for auction item")
                return True
            else:
                self.log_test("Auction Bid History", False, f"Get bid history failed with status {response['status_code']}", response["data"])
        else:
            self.log_test("Auction Bidding", False, f"Place bid failed with status {response['status_code']}", response["data"])
        
        return False

    def test_order_creation(self):
        """Test order creation process"""
        if not self.access_token:
            self.log_test("Order Creation", False, "No access token available")
            return False
        
        # Find a non-auction product with quantity > 0
        response = self.make_request("GET", "/products", params={"listing_type": "buy_now", "limit": 10})
        
        if response["status_code"] != 200:
            self.log_test("Order Creation", False, "Could not get products for order creation")
            return False
        
        products = response["data"].get("products", [])
        available_products = [p for p in products if not p.get("is_auction") and p.get("quantity", 0) > 0]
        
        if not available_products:
            self.log_test("Order Creation", False, "No available products found for order creation")
            return False
        
        product = available_products[0]
        
        # Create order
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
        
        response = self.make_request("POST", "/orders/create", order_data)
        
        if response["status_code"] == 200:
            order = response["data"]
            if "id" in order and "total_amount" in order:
                order_id = order["id"]
                self.log_test("Order Creation", True, f"Order created successfully with ID {order_id}", {
                    "order_id": order_id,
                    "total_amount": order["total_amount"]
                })
                
                # Test getting order details
                response = self.make_request("GET", f"/orders/{order_id}")
                
                if response["status_code"] == 200:
                    order_details = response["data"]
                    self.log_test("Order Details", True, f"Retrieved order details for order {order_id}")
                    return True
                else:
                    self.log_test("Order Details", False, f"Get order details failed with status {response['status_code']}", response["data"])
            else:
                self.log_test("Order Creation", False, "Missing required order fields", order)
        else:
            self.log_test("Order Creation", False, f"Order creation failed with status {response['status_code']}", response["data"])
        
        return False

    def test_user_orders(self):
        """Test getting user order history"""
        if not self.access_token:
            self.log_test("User Orders", False, "No access token available")
            return False
        
        response = self.make_request("GET", "/users/orders")
        
        if response["status_code"] == 200:
            orders = response["data"]
            self.log_test("User Orders", True, f"Retrieved {len(orders)} orders from user history")
            return True
        else:
            self.log_test("User Orders", False, f"Get user orders failed with status {response['status_code']}", response["data"])
        
        return False

    def test_error_handling(self):
        """Test API error handling"""
        # Test invalid product ID
        response = self.make_request("GET", "/products/invalid_id")
        
        if response["status_code"] == 400:
            self.log_test("Error Handling (Invalid ID)", True, "API correctly returned 400 for invalid product ID")
        else:
            self.log_test("Error Handling (Invalid ID)", False, f"Expected 400 but got {response['status_code']}")
        
        # Test unauthorized access
        old_token = self.access_token
        self.access_token = "invalid_token"
        
        response = self.make_request("GET", "/users/profile")
        
        if response["status_code"] in [401, 403]:
            self.log_test("Error Handling (Unauthorized)", True, f"API correctly returned {response['status_code']} for invalid token")
        else:
            self.log_test("Error Handling (Unauthorized)", False, f"Expected 401/403 but got {response['status_code']}")
        
        # Restore token
        self.access_token = old_token
        
        return True

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting EasyCart Backend API Tests")
        print("=" * 60)
        
        # Authentication Tests
        print("\n📝 Authentication Tests")
        print("-" * 30)
        self.test_auth_register()
        self.test_auth_login()
        self.test_auth_me()
        self.test_auth_logout()
        
        # Re-login for subsequent tests
        self.test_auth_login()
        
        # Product Tests
        print("\n🛍️ Product Tests")
        print("-" * 30)
        self.test_products_list()
        self.test_products_categories()
        self.test_products_search()
        self.test_products_filtering()
        self.test_product_detail()
        
        # User Tests
        print("\n👤 User Tests")
        print("-" * 30)
        self.test_user_profile()
        self.test_user_watchlist()
        self.test_user_orders()
        
        # Auction Tests
        print("\n🔨 Auction Tests")
        print("-" * 30)
        self.test_auction_bidding()
        
        # Order Tests
        print("\n📦 Order Tests")
        print("-" * 30)
        self.test_order_creation()
        
        # Error Handling Tests
        print("\n⚠️ Error Handling Tests")
        print("-" * 30)
        self.test_error_handling()
        
        # Summary
        print("\n📊 Test Summary")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test in self.test_results:
                if not test["success"]:
                    print(f"  - {test['test']}: {test['message']}")
        
        return passed_tests, failed_tests, self.test_results

def main():
    """Main test execution"""
    tester = EasyCartAPITester()
    passed, failed, results = tester.run_all_tests()
    
    # Save detailed results to file
    with open("/app/backend_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "total_tests": len(results),
                "passed": passed,
                "failed": failed,
                "success_rate": (passed/len(results))*100 if results else 0,
                "timestamp": datetime.now().isoformat()
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/backend_test_results.json")
    
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()