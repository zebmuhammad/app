# EasyCart Full-Stack Integration Contracts

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Products
- `GET /api/products` - Get all products with filters, search, pagination
- `GET /api/products/:id` - Get single product details
- `POST /api/products` - Create new product (seller)
- `PUT /api/products/:id` - Update product (seller)
- `DELETE /api/products/:id` - Delete product (seller)
- `GET /api/products/categories` - Get all categories
- `GET /api/products/search` - Advanced product search

### User Management
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile
- `GET /api/users/orders` - Get user order history
- `GET /api/users/watchlist` - Get user watchlist
- `POST /api/users/watchlist/:productId` - Add to watchlist
- `DELETE /api/users/watchlist/:productId` - Remove from watchlist

### Cart & Orders
- `GET /api/cart` - Get user's cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item quantity
- `DELETE /api/cart/remove/:productId` - Remove from cart
- `POST /api/orders/create` - Create new order
- `GET /api/orders/:id` - Get order details

### Bidding (Auction)
- `POST /api/products/:id/bid` - Place bid on auction item
- `GET /api/products/:id/bids` - Get bid history

## Database Models

### User
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (hashed),
  avatar: String,
  rating: Number,
  memberSince: Date,
  isVerified: Boolean,
  watchlist: [ObjectId] (product references),
  createdAt: Date,
  updatedAt: Date
}
```

### Product
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  price: Number,
  originalPrice: Number,
  images: [String],
  category: String,
  condition: String, // New, Used, Refurbished, For parts
  listingType: String, // Auction, Buy It Now, Best Offer
  seller: ObjectId (user reference),
  isAuction: Boolean,
  auctionEndTime: Date,
  currentBid: Number,
  bidCount: Number,
  buyItNow: Boolean,
  quantity: Number,
  brand: String,
  rating: Number,
  reviewCount: Number,
  isActive: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

### Order
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  items: [{
    productId: ObjectId,
    name: String,
    price: Number,
    quantity: Number,
    image: String
  }],
  totalAmount: Number,
  status: String, // Processing, In Transit, Delivered
  shippingAddress: Object,
  paymentMethod: String,
  createdAt: Date,
  updatedAt: Date
}
```

### Bid
```javascript
{
  _id: ObjectId,
  productId: ObjectId,
  userId: ObjectId,
  amount: Number,
  createdAt: Date
}
```

## Frontend Changes Needed

1. **Replace all "eBay" references with "EasyCart"**
   - Logo and branding
   - Page titles and descriptions
   - Header links and navigation

2. **Replace mock data usage with API calls**
   - Remove mockData.js imports
   - Add API service functions
   - Update context providers to use real data

3. **Add API integration**
   - Create services/api.js for all API calls
   - Update contexts to use real authentication
   - Add proper error handling

## Product Categories with Items

### Electronics (50+ items)
- Smartphones (iPhone, Samsung, Google Pixel)
- Laptops (MacBook, Dell, HP, Lenovo)
- Gaming consoles (PS5, Xbox, Nintendo Switch)
- Smart watches (Apple Watch, Fitbit)
- Headphones (AirPods, Sony, Bose)
- Tablets (iPad, Surface Pro)
- Cameras (Canon, Nikon, Sony)

### Sneakers & Footwear (100+ items)
- Nike (Air Jordan, Air Max, Dunk, Blazer)
- Adidas (Yeezy, Stan Smith, Ultraboost)
- New Balance (550, 990, 574)
- Converse (Chuck Taylor, One Star)
- Vans (Old Skool, Sk8-Hi)

### Clothing & Fashion (80+ items)
- Men's clothing (shirts, pants, jackets)
- Women's clothing (dresses, tops, jeans)
- Designer brands (Gucci, Louis Vuitton, Prada)
- Streetwear (Supreme, Off-White, Stussy)

### Collectibles (60+ items)
- Trading cards (Pokemon, Sports cards)
- Comic books (Marvel, DC)
- Vintage toys (Hot Wheels, LEGO)
- Antiques and vintage items

### Home & Garden (40+ items)
- Furniture (sofas, tables, chairs)
- Home decor (art, lighting, rugs)
- Kitchen appliances
- Garden tools and plants

### Toys & Games (30+ items)
- Video games (PS5, Xbox, Nintendo)
- Board games and puzzles
- Action figures and dolls
- Remote control toys

## Integration Steps

1. Create MongoDB models and seed extensive product data
2. Build all API endpoints with proper validation
3. Update frontend to use "EasyCart" branding
4. Replace mock data with API calls
5. Add proper authentication flow
6. Test all user flows with real data