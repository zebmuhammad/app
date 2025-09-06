from datetime import datetime, timedelta
import asyncio
from database import products_collection, users_collection
from models.user import User
from models.product import Product
from passlib.context import CryptContext
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample sellers
sellers_data = [
    {"name": "TechHub_Official", "email": "techhub@example.com", "rating": 4.9},
    {"name": "SneakerKing_Pro", "email": "sneakerking@example.com", "rating": 4.8},
    {"name": "FashionForward", "email": "fashion@example.com", "rating": 4.7},
    {"name": "CollectibleCorner", "email": "collectibles@example.com", "rating": 4.9},
    {"name": "HomeStyler", "email": "homestyler@example.com", "rating": 4.6},
    {"name": "GameZone_Store", "email": "gamezone@example.com", "rating": 4.8},
    {"name": "VintageFinds", "email": "vintage@example.com", "rating": 4.5},
    {"name": "LuxuryDeals", "email": "luxury@example.com", "rating": 4.9},
]

# Extensive product data by category
products_data = {
    "electronics": [
        # Smartphones
        {"name": "iPhone 15 Pro Max 256GB", "price": 1199.99, "original_price": 1299.99, "brand": "Apple", "condition": "New"},
        {"name": "Samsung Galaxy S24 Ultra 512GB", "price": 1299.99, "brand": "Samsung", "condition": "New"},
        {"name": "Google Pixel 8 Pro 128GB", "price": 899.99, "original_price": 999.99, "brand": "Google", "condition": "New"},
        {"name": "iPhone 14 Pro 128GB", "price": 999.99, "original_price": 1099.99, "brand": "Apple", "condition": "Used"},
        {"name": "OnePlus 12 256GB", "price": 799.99, "brand": "OnePlus", "condition": "New"},
        
        # Laptops
        {"name": "MacBook Pro 16-inch M3 Max", "price": 3499.99, "brand": "Apple", "condition": "New"},
        {"name": "Dell XPS 15 OLED Touch", "price": 2299.99, "brand": "Dell", "condition": "New"},
        {"name": "HP Spectre x360 14-inch", "price": 1699.99, "original_price": 1899.99, "brand": "HP", "condition": "New"},
        {"name": "Lenovo ThinkPad X1 Carbon", "price": 1899.99, "brand": "Lenovo", "condition": "New"},
        {"name": "MacBook Air M2 13-inch", "price": 1199.99, "original_price": 1299.99, "brand": "Apple", "condition": "Used"},
        
        # Gaming Consoles
        {"name": "PlayStation 5 Console", "price": 499.99, "brand": "Sony", "condition": "New"},
        {"name": "Xbox Series X Console", "price": 499.99, "brand": "Microsoft", "condition": "New"},
        {"name": "Nintendo Switch OLED", "price": 349.99, "brand": "Nintendo", "condition": "New"},
        {"name": "PlayStation 5 Digital Edition", "price": 399.99, "brand": "Sony", "condition": "New"},
        {"name": "Steam Deck 512GB OLED", "price": 649.99, "brand": "Valve", "condition": "New"},
        
        # Smart Watches
        {"name": "Apple Watch Series 9 45mm", "price": 429.99, "brand": "Apple", "condition": "New"},
        {"name": "Samsung Galaxy Watch 6 Classic", "price": 399.99, "brand": "Samsung", "condition": "New"},
        {"name": "Fitbit Versa 4", "price": 199.99, "original_price": 249.99, "brand": "Fitbit", "condition": "New"},
        {"name": "Garmin Forerunner 965", "price": 599.99, "brand": "Garmin", "condition": "New"},
        
        # Headphones
        {"name": "AirPods Pro 2nd Generation", "price": 249.99, "brand": "Apple", "condition": "New"},
        {"name": "Sony WH-1000XM5", "price": 399.99, "original_price": 449.99, "brand": "Sony", "condition": "New"},
        {"name": "Bose QuietComfort Ultra", "price": 429.99, "brand": "Bose", "condition": "New"},
        {"name": "AirPods Max", "price": 549.99, "brand": "Apple", "condition": "New"},
        
        # Tablets
        {"name": "iPad Pro 12.9-inch M2", "price": 1099.99, "brand": "Apple", "condition": "New"},
        {"name": "Samsung Galaxy Tab S9 Ultra", "price": 1199.99, "brand": "Samsung", "condition": "New"},
        {"name": "Microsoft Surface Pro 9", "price": 999.99, "brand": "Microsoft", "condition": "New"},
        {"name": "iPad Air 5th Generation", "price": 599.99, "brand": "Apple", "condition": "New"},
        
        # Cameras
        {"name": "Canon EOS R5 Mirrorless", "price": 3899.99, "brand": "Canon", "condition": "New"},
        {"name": "Sony A7 IV Full Frame", "price": 2499.99, "brand": "Sony", "condition": "New"},
        {"name": "Nikon Z9 Professional", "price": 5499.99, "brand": "Nikon", "condition": "New"},
        {"name": "Fujifilm X-T5 Mirrorless", "price": 1699.99, "brand": "Fujifilm", "condition": "New"},
    ],
    
    "sneakers": [
        # Nike Air Jordan
        {"name": "Air Jordan 1 Retro High OG Chicago", "price": 170.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 4 Retro Black Cat", "price": 210.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 11 Retro Bred", "price": 220.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 3 Retro White Cement", "price": 200.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 6 Retro Infrared", "price": 200.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 12 Retro Taxi", "price": 200.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 5 Retro Fire Red", "price": 190.00, "brand": "Nike", "condition": "New"},
        {"name": "Air Jordan 13 Retro He Got Game", "price": 200.00, "brand": "Nike", "condition": "New"},
        
        # Nike Dunk
        {"name": "Nike Dunk Low Panda", "price": 110.00, "brand": "Nike", "condition": "New"},
        {"name": "Nike Dunk High Syracuse", "price": 120.00, "brand": "Nike", "condition": "New"},
        {"name": "Nike Dunk Low Chicago", "price": 110.00, "brand": "Nike", "condition": "New"},
        {"name": "Nike Dunk Low UNC", "price": 110.00, "brand": "Nike", "condition": "New"},
        
        # Adidas Yeezy
        {"name": "Adidas Yeezy Boost 350 V2 Zebra", "price": 220.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Yeezy Boost 700 Wave Runner", "price": 300.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Yeezy 450 Cloud White", "price": 200.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Yeezy Foam Runner Onyx", "price": 80.00, "brand": "Adidas", "condition": "New"},
        
        # Adidas Originals
        {"name": "Adidas Stan Smith White Green", "price": 80.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Ultraboost 23", "price": 190.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Gazelle Bold Pink", "price": 90.00, "brand": "Adidas", "condition": "New"},
        {"name": "Adidas Campus 00s Black", "price": 90.00, "brand": "Adidas", "condition": "New"},
        
        # New Balance
        {"name": "New Balance 550 White Grey", "price": 110.00, "brand": "New Balance", "condition": "New"},
        {"name": "New Balance 990v5 Grey", "price": 185.00, "brand": "New Balance", "condition": "New"},
        {"name": "New Balance 574 Legacy", "price": 80.00, "brand": "New Balance", "condition": "New"},
        {"name": "New Balance 327 Casablanca", "price": 90.00, "brand": "New Balance", "condition": "New"},
        
        # Converse
        {"name": "Converse Chuck Taylor All Star Hi", "price": 55.00, "brand": "Converse", "condition": "New"},
        {"name": "Converse Chuck 70 High Top", "price": 75.00, "brand": "Converse", "condition": "New"},
        {"name": "Converse One Star Pro", "price": 75.00, "brand": "Converse", "condition": "New"},
        
        # Vans
        {"name": "Vans Old Skool Black White", "price": 65.00, "brand": "Vans", "condition": "New"},
        {"name": "Vans Sk8-Hi MTE-2", "price": 90.00, "brand": "Vans", "condition": "New"},
        {"name": "Vans Authentic Platform", "price": 60.00, "brand": "Vans", "condition": "New"},
    ],
    
    "clothing": [
        # Designer Brands
        {"name": "Gucci GG Marmont T-Shirt", "price": 590.00, "brand": "Gucci", "condition": "New"},
        {"name": "Louis Vuitton Monogram Hoodie", "price": 1850.00, "brand": "Louis Vuitton", "condition": "New"},
        {"name": "Prada Re-Edition 2005", "price": 1320.00, "brand": "Prada", "condition": "New"},
        {"name": "Balenciaga Triple S Sneakers", "price": 1090.00, "brand": "Balenciaga", "condition": "New"},
        
        # Streetwear
        {"name": "Supreme Box Logo Hoodie", "price": 800.00, "original_price": 168.00, "brand": "Supreme", "condition": "New"},
        {"name": "Off-White Diagonal Arrows T-Shirt", "price": 420.00, "brand": "Off-White", "condition": "New"},
        {"name": "Stussy Stock T-Shirt", "price": 45.00, "brand": "Stussy", "condition": "New"},
        {"name": "A Bathing Ape Shark Hoodie", "price": 320.00, "brand": "BAPE", "condition": "New"},
        
        # Men's Clothing
        {"name": "Ralph Lauren Polo Shirt", "price": 89.50, "brand": "Ralph Lauren", "condition": "New"},
        {"name": "Levi's 501 Original Jeans", "price": 69.50, "brand": "Levi's", "condition": "New"},
        {"name": "Nike Tech Fleece Joggers", "price": 100.00, "brand": "Nike", "condition": "New"},
        {"name": "Champion Reverse Weave Hoodie", "price": 60.00, "brand": "Champion", "condition": "New"},
        
        # Women's Clothing
        {"name": "Zara Midi Wrap Dress", "price": 49.90, "brand": "Zara", "condition": "New"},
        {"name": "H&M Oversized Blazer", "price": 59.99, "brand": "H&M", "condition": "New"},
        {"name": "Uniqlo Heattech Ultra Warm Crew", "price": 19.90, "brand": "Uniqlo", "condition": "New"},
        {"name": "Reformation Linen Mini Dress", "price": 148.00, "brand": "Reformation", "condition": "New"},
    ],
    
    "collectibles": [
        # Trading Cards
        {"name": "Pokemon Charizard Holo Base Set", "price": 3500.00, "brand": "Pokemon", "condition": "Used"},
        {"name": "Magic The Gathering Black Lotus", "price": 12000.00, "brand": "Wizards of the Coast", "condition": "Used"},
        {"name": "Michael Jordan Rookie Card PSA 10", "price": 8500.00, "brand": "Topps", "condition": "Used"},
        {"name": "Pokemon Booster Box Vintage", "price": 2200.00, "brand": "Pokemon", "condition": "New"},
        
        # Comic Books
        {"name": "Amazing Spider-Man #1 CGC 9.0", "price": 4200.00, "brand": "Marvel", "condition": "Used"},
        {"name": "Batman #1 CGC 8.5", "price": 15000.00, "brand": "DC Comics", "condition": "Used"},
        {"name": "X-Men #1 CGC 9.8", "price": 850.00, "brand": "Marvel", "condition": "Used"},
        {"name": "Superman #1 CGC 7.0", "price": 6800.00, "brand": "DC Comics", "condition": "Used"},
        
        # Vintage Toys
        {"name": "Hot Wheels Redline Pink Peeping Bomb", "price": 1200.00, "brand": "Hot Wheels", "condition": "Used"},
        {"name": "LEGO Creator Expert Taj Mahal", "price": 899.99, "brand": "LEGO", "condition": "New"},
        {"name": "Vintage Star Wars Luke Skywalker", "price": 2800.00, "brand": "Kenner", "condition": "Used"},
        {"name": "Beanie Baby Princess Bear", "price": 3000.00, "brand": "Ty", "condition": "Used"},
        
        # Antiques
        {"name": "Vintage Rolex Submariner 1960s", "price": 25000.00, "brand": "Rolex", "condition": "Used"},
        {"name": "Mid-Century Modern Eames Chair", "price": 1800.00, "brand": "Herman Miller", "condition": "Used"},
        {"name": "Vintage Gibson Les Paul 1959", "price": 85000.00, "brand": "Gibson", "condition": "Used"},
        {"name": "Art Deco Sterling Silver Tea Set", "price": 1200.00, "brand": "Tiffany & Co", "condition": "Used"},
    ],
    
    "home": [
        # Furniture
        {"name": "West Elm Mid-Century Sofa", "price": 1299.00, "brand": "West Elm", "condition": "New"},
        {"name": "IKEA HEMNES Daybed Frame", "price": 229.00, "brand": "IKEA", "condition": "New"},
        {"name": "CB2 Acrylic Coffee Table", "price": 399.00, "brand": "CB2", "condition": "New"},
        {"name": "Article Sven Sectional Sofa", "price": 1699.00, "brand": "Article", "condition": "New"},
        
        # Home Decor
        {"name": "Pottery Barn Table Lamp", "price": 199.00, "brand": "Pottery Barn", "condition": "New"},
        {"name": "Anthropologie Moroccan Rug", "price": 498.00, "brand": "Anthropologie", "condition": "New"},
        {"name": "Urban Outfitters Wall Mirror", "price": 89.00, "brand": "Urban Outfitters", "condition": "New"},
        {"name": "Target Project 62 Throw Pillows", "price": 29.99, "brand": "Target", "condition": "New"},
        
        # Kitchen Appliances
        {"name": "KitchenAid Stand Mixer", "price": 449.99, "brand": "KitchenAid", "condition": "New"},
        {"name": "Ninja Foodi Air Fryer", "price": 199.99, "brand": "Ninja", "condition": "New"},
        {"name": "Vitamix Professional Blender", "price": 499.95, "brand": "Vitamix", "condition": "New"},
        {"name": "Instant Pot Duo 7-in-1", "price": 99.95, "brand": "Instant Pot", "condition": "New"},
    ],
    
    "toys": [
        # Video Games
        {"name": "The Legend of Zelda: Tears of the Kingdom", "price": 59.99, "brand": "Nintendo", "condition": "New"},
        {"name": "God of War Ragnarök PS5", "price": 59.99, "brand": "Sony", "condition": "New"},
        {"name": "Elden Ring Collector's Edition", "price": 199.99, "brand": "Bandai Namco", "condition": "New"},
        {"name": "Super Mario Bros Wonder", "price": 59.99, "brand": "Nintendo", "condition": "New"},
        
        # Board Games
        {"name": "Settlers of Catan Board Game", "price": 49.99, "brand": "Catan Studio", "condition": "New"},
        {"name": "Monopoly Classic Edition", "price": 19.99, "brand": "Hasbro", "condition": "New"},
        {"name": "Wingspan Board Game", "price": 65.00, "brand": "Stonemaier Games", "condition": "New"},
        {"name": "Ticket to Ride Europe", "price": 54.99, "brand": "Days of Wonder", "condition": "New"},
        
        # Action Figures
        {"name": "Marvel Spider-Man Figure", "price": 24.99, "brand": "Hasbro", "condition": "New"},
        {"name": "Star Wars Black Series Vader", "price": 29.99, "brand": "Hasbro", "condition": "New"},
        {"name": "Funko Pop Batman", "price": 12.99, "brand": "Funko", "condition": "New"},
        {"name": "LEGO Creator Expert Big Ben", "price": 249.99, "brand": "LEGO", "condition": "New"},
    ]
}

async def create_sample_users():
    """Create sample seller users"""
    users = []
    for seller_data in sellers_data:
        hashed_password = pwd_context.hash("password123")
        user = User(
            name=seller_data["name"],
            email=seller_data["email"],
            password=hashed_password,
            rating=seller_data["rating"],
            is_verified=True,
            member_since=datetime.utcnow() - timedelta(days=random.randint(30, 1000))
        )
        users.append(user.dict(by_alias=True))
    
    try:
        result = await users_collection.insert_many(users)
        print(f"Created {len(result.inserted_ids)} sample users")
        return result.inserted_ids
    except Exception as e:
        print(f"Error creating users: {e}")
        return []

async def create_sample_products():
    """Create extensive sample products for all categories"""
    # Get all user IDs for sellers
    users = await users_collection.find().to_list(length=None)
    if not users:
        print("No users found. Creating users first...")
        user_ids = await create_sample_users()
        users = await users_collection.find().to_list(length=None)
    
    products = []
    base_images = {
        "electronics": [
            "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop"
        ],
        "sneakers": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&h=500&fit=crop"
        ],
        "clothing": [
            "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=500&h=500&fit=crop"
        ],
        "collectibles": [
            "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=500&h=500&fit=crop"
        ],
        "home": [
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=500&h=500&fit=crop"
        ],
        "toys": [
            "https://images.unsplash.com/photo-1560421683-6856ea585c78?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=500&h=500&fit=crop",
            "https://images.unsplash.com/photo-1594736797933-d0401ba42653?w=500&h=500&fit=crop"
        ]
    }
    
    for category, items in products_data.items():
        for item in items:
            seller = random.choice(users)
            
            # Determine if auction or buy it now
            is_auction = random.choice([True, False])
            listing_type = "Auction" if is_auction else "Buy It Now"
            
            product = Product(
                name=item["name"],
                description=f"Authentic {item['name']} in {item.get('condition', 'New')} condition. {random.choice(['Fast shipping!', 'Original packaging included.', 'Excellent quality guaranteed.', 'Trusted seller with high ratings.'])}",
                price=item["price"],
                original_price=item.get("original_price"),
                images=random.choices(base_images[category], k=3),
                category=category,
                condition=item.get("condition", "New"),
                listing_type=listing_type,
                seller=seller["_id"],
                seller_name=seller["name"],
                is_auction=is_auction,
                auction_end_time=datetime.utcnow() + timedelta(days=random.randint(1, 7)) if is_auction else None,
                current_bid=item["price"] - random.randint(10, 50) if is_auction else None,
                bid_count=random.randint(0, 25) if is_auction else 0,
                buy_it_now=not is_auction,
                quantity=random.randint(1, 10),
                brand=item.get("brand"),
                rating=round(random.uniform(4.0, 5.0), 1),
                review_count=random.randint(5, 500),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            products.append(product.dict(by_alias=True))
    
    try:
        result = await products_collection.insert_many(products)
        print(f"Created {len(result.inserted_ids)} sample products")
        return result.inserted_ids
    except Exception as e:
        print(f"Error creating products: {e}")
        return []

async def seed_database():
    """Seed the database with sample data"""
    print("Seeding database with sample data...")
    
    # Check if data already exists
    user_count = await users_collection.count_documents({})
    product_count = await products_collection.count_documents({})
    
    if user_count == 0:
        await create_sample_users()
    else:
        print(f"Found {user_count} existing users, skipping user creation")
    
    if product_count == 0:
        await create_sample_products()
    else:
        print(f"Found {product_count} existing products, skipping product creation")
    
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_database())