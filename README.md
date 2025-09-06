# Here are your Instructions
EasyCart E-Commerce Platform Documentation
This documentation covers the architecture, features, and usage of the EasyCart full-stack e-commerce platform, based on your workspace structure and code.

Table of Contents
Overview
Architecture
Backend
Setup
API Endpoints
Database Models
Testing
Frontend
Setup
Main Features
Component Overview
Integration Steps
Development & Testing
References
Overview
EasyCart is a full-stack e-commerce web application supporting product listings, auctions, orders, user profiles, watchlists, and more. It is built with a Python backend (FastAPI) and a React frontend, with MongoDB as the database.

Architecture
Backend
Backend Setup
Install dependencies:

Environment variables:
Configure backend/.env for DB connection and secrets.

Seed database:
Run seed_data.py to populate users and products.

Start server:

API Endpoints
See contracts.md for full details. Key endpoints include:

Authentication

POST /api/auth/register — Register user
POST /api/auth/login — Login
GET /api/auth/me — Get current user
Products

GET /api/products — List products (filters, pagination)
GET /api/products/:id — Product details
GET /api/products/categories — List categories
GET /api/products/search — Search products
POST /api/products/:id/bid — Place auction bid
GET /api/products/:id/bids — Get bid history
Orders

POST /api/orders/create — Create order
GET /api/orders/:id — Order details
Users

GET /api/users/profile — Get profile
PUT /api/users/profile — Update profile
GET /api/users/orders — Order history
GET /api/users/watchlist — Watchlist
POST /api/users/watchlist/:productId — Add to watchlist
DELETE /api/users/watchlist/:productId — Remove from watchlist
Database Models
See contracts.md:

User: name, email, password, avatar, rating, watchlist, etc.
Product: name, description, price, images, category, auction info, etc.
Order: user, items, total, status, shipping, payment, etc.
Bid: product, user, amount, timestamp.
Backend Testing
Run comprehensive and focused tests:
See backend_test_results.json and test_result.md for results.
Frontend
Frontend Setup
Install dependencies:

Environment variables:
Configure frontend/.env for API base URL.

Start development server:

Access at http://localhost:3000.

Main Features
Homepage: Product carousel, featured items, category sections (src/pages/Homepage.js)
Product Search & Filters: Search, filter by category, price, brand, etc. (src/pages/SearchResults.js)
Product Detail: Images, description, bidding, add to cart/watchlist (src/pages/ProductDetail.js)
Cart: Add/remove/update items, checkout summary (src/pages/Cart.js)
Profile: User info, order history, watchlist (src/pages/Profile.js)
Watchlist: Add/remove products, view in profile and header (src/components/Header.js)
Component Overview
Header: Navigation, search, cart/watchlist indicators
Card: Product display
Badge: Sale, auction, buy now indicators
Tabs: Product details, reviews, shipping info
Integration Steps
See contracts.md:

Create MongoDB models and seed product data
Build API endpoints with validation
Update frontend branding to "EasyCart"
Replace mock data with API calls
Add authentication flow
Test all user flows with real data
Development & Testing
Backend: Python, FastAPI, MongoDB
Frontend: React, Tailwind CSS, Lucide icons
Testing: Python scripts in root directory
Continuous Integration: See .emergent/emergent.yml for agent config
References
contracts.md — API and data model contracts
seed_data.py — Data seeding
backend/routes/ — API route implementations
frontend/src/pages/ — Main React pages
frontend/src/components/ — UI components
backend_test.py, backend_test_final.py, backend_test_focused.py — Test scripts
For more details, see the referenced files above.
