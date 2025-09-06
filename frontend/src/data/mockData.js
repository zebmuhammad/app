// Mock data for eBay clone

export const categories = [
  'eBay Live', 'Saved', 'Motors', 'Electronics', 'Collectibles', 
  'Home & Garden', 'Clothing, Shoes & Accessories', 'Toys', 
  'Sporting Goods', 'Business & Industrial', 'Jewelry & Watches', 'Refurbished'
];

export const heroSlides = [
  {
    id: 1,
    title: "From essentials to exclusives",
    subtitle: "Shop pre-loved sneakers for an everyday fit or a major flex.",
    image: "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=1200&h=400&fit=crop",
    buttonText: "Check 'em out",
    buttonLink: "/search?category=sneakers"
  },
  {
    id: 2,
    title: "Tech deals you can't miss",
    subtitle: "Discover the latest gadgets at unbeatable prices.",
    image: "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=1200&h=400&fit=crop",
    buttonText: "Shop now",
    buttonLink: "/search?category=electronics"
  },
  {
    id: 3,
    title: "Vintage treasures await",
    subtitle: "Find unique collectibles from decades past.",
    image: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=1200&h=400&fit=crop",
    buttonText: "Explore",
    buttonLink: "/search?category=collectibles"
  }
];

export const trendingProducts = [
  {
    id: 1,
    name: "Undefeated x Jordan 4 Retro 2025",
    price: 299.99,
    originalPrice: 399.99,
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
    seller: "SneakerHead_Pro",
    rating: 4.8,
    bids: 12,
    timeLeft: "2d 14h",
    isAuction: true,
    category: "sneakers"
  },
  {
    id: 2,
    name: "Jordan 5 Retro OG Metallic Reimagined",
    price: 189.99,
    image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=300&h=300&fit=crop",
    seller: "KickCollection",
    rating: 4.9,
    buyItNow: true,
    category: "sneakers"
  },
  {
    id: 3,
    name: "Nigel Sylvester x Jordan 1 OG Low Better With Time",
    price: 459.99,
    image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=300&h=300&fit=crop",
    seller: "Elite_Sneakers",
    rating: 4.7,
    bids: 8,
    timeLeft: "1d 8h",
    isAuction: true,
    category: "sneakers"
  },
  {
    id: 4,
    name: "Nike Kobe 6 Protro Dodgers",
    price: 329.99,
    image: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=300&h=300&fit=crop",
    seller: "CourtKings",
    rating: 4.6,
    buyItNow: true,
    category: "sneakers"
  },
  {
    id: 5,
    name: "Jordan 10 Retro Steel 2025",
    price: 199.99,
    originalPrice: 239.99,
    image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=300&h=300&fit=crop",
    seller: "JordanLegacy",
    rating: 4.8,
    bids: 15,
    timeLeft: "3d 2h",
    isAuction: true,
    category: "sneakers"
  },
  {
    id: 6,
    name: "Jordan 4 Retro White Cement 2025",
    price: 249.99,
    image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=300&h=300&fit=crop",
    seller: "RetroSole",
    rating: 4.9,
    buyItNow: true,
    category: "sneakers"
  },
  {
    id: 7,
    name: "Nike Kobe 6 Protro Total Orange",
    price: 389.99,
    image: "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=300&h=300&fit=crop",
    seller: "MambaMentality",
    rating: 4.7,
    bids: 6,
    timeLeft: "4d 12h",
    isAuction: true,
    category: "sneakers"
  }
];

export const dealSection = {
  title: "There's a deal for you, too",
  subtitle: "Don't miss a chance to save on items you've been looking for.",
  buttonText: "Explore now",
  backgroundColor: "#2d7a2d"
};

export const searchSuggestions = [
  "iPhone 15", "Gaming laptop", "Vintage watches", "Designer bags", 
  "Pokemon cards", "Nike shoes", "MacBook Pro", "Camera lens"
];

export const userProfile = {
  id: 1,
  name: "John Doe",
  email: "john.doe@example.com",
  rating: 4.9,
  totalTransactions: 127,
  memberSince: "2019",
  avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop&crop=face"
};

export const sampleReviews = [
  {
    id: 1,
    user: "Sarah M.",
    rating: 5,
    comment: "Excellent seller! Item exactly as described and shipped quickly.",
    date: "2025-01-15"
  },
  {
    id: 2,
    user: "Mike R.",
    rating: 4,
    comment: "Good quality product, fair price. Would buy again.",
    date: "2025-01-10"
  },
  {
    id: 3,
    user: "Lisa K.",
    rating: 5,
    comment: "Amazing condition for a used item. Very satisfied!",
    date: "2025-01-08"
  }
];