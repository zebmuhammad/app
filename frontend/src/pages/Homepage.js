import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ChevronLeft, ChevronRight, ArrowRight, Clock, Star } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Card, CardContent } from '../components/ui/card';
import { useCart } from '../contexts/CartContext';
import { productsAPI } from '../services/api';

const Homepage = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addToCart, addToWatchlist } = useCart();

  const heroSlides = [
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

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await productsAPI.getProducts({ 
          limit: 20, 
          sort_by: 'created_at', 
          sort_order: 'desc' 
        });
        setProducts(response.products || []);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + heroSlides.length) % heroSlides.length);
  };

  const formatPrice = (price) => `$${price.toFixed(2)}`;

  const calculateTimeLeft = (endTime) => {
    if (!endTime) return null;
    const now = new Date();
    const end = new Date(endTime);
    const diff = end - now;
    
    if (diff <= 0) return 'Ended';
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    
    return `${days}d ${hours}h`;
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Carousel */}
      <div className="relative h-96 overflow-hidden">
        {heroSlides.map((slide, index) => (
          <div
            key={slide.id}
            className={`absolute inset-0 transition-transform duration-500 ease-in-out ${
              index === currentSlide ? 'translate-x-0' : 'translate-x-full'
            }`}
            style={{
              transform: `translateX(${(index - currentSlide) * 100}%)`,
            }}
          >
            <div 
              className="w-full h-full bg-cover bg-center relative"
              style={{ backgroundImage: `url(${slide.image})` }}
            >
              <div className="absolute inset-0 bg-black bg-opacity-40" />
              <div className="absolute inset-0 flex items-center justify-start px-16">
                <div className="text-white max-w-lg">
                  <h1 className="text-4xl font-bold mb-4">{slide.title}</h1>
                  <p className="text-lg mb-6 opacity-90">{slide.subtitle}</p>
                  <Link to={slide.buttonLink}>
                    <Button className="bg-white text-black hover:bg-gray-100 font-semibold px-8 py-3 rounded-full">
                      {slide.buttonText}
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {/* Navigation Buttons */}
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white p-2 rounded-full transition-all"
        >
          <ChevronLeft className="h-6 w-6" />
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white p-2 rounded-full transition-all"
        >
          <ChevronRight className="h-6 w-6" />
        </button>

        {/* Slide Indicators */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all ${
                index === currentSlide ? 'bg-white' : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Deal Section */}
        <div className="rounded-lg p-8 mb-12 text-white bg-green-700">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold mb-2">There's a deal for you, too</h2>
              <p className="text-lg opacity-90">Don't miss a chance to save on items you've been looking for.</p>
            </div>
            <Link to="/search">
              <Button className="bg-white text-black hover:bg-gray-100 font-semibold px-8 py-3 rounded-full">
                Explore now
              </Button>
            </Link>
          </div>
        </div>

        {/* Featured Products */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Featured Items</h2>
            <Link to="/search" className="flex items-center text-blue-600 hover:text-blue-800 font-medium">
              See all <ArrowRight className="h-4 w-4 ml-1" />
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
              {[...Array(12)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 h-48 rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
              {products.slice(0, 12).map((product) => (
                <Card key={product.id} className="group hover:shadow-lg transition-all duration-300 cursor-pointer">
                  <CardContent className="p-0">
                    <Link to={`/product/${product.id}`}>
                      <div className="relative">
                        <img
                          src={product.images[0] || 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop'}
                          alt={product.name}
                          className="w-full h-48 object-cover rounded-t-lg group-hover:scale-105 transition-transform duration-300"
                        />
                        {product.original_price && (
                          <Badge className="absolute top-2 left-2 bg-red-500 text-white">
                            Sale
                          </Badge>
                        )}
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            addToWatchlist(product);
                          }}
                          className="absolute top-2 right-2 p-2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full transition-all"
                        >
                          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                          </svg>
                        </button>
                      </div>
                    </Link>
                    
                    <div className="p-4">
                      <Link to={`/product/${product.id}`}>
                        <h3 className="font-medium text-sm text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600">
                          {product.name}
                        </h3>
                      </Link>
                      
                      <div className="flex items-center mb-2">
                        <div className="flex items-center">
                          <Star className="h-3 w-3 text-yellow-400 fill-current" />
                          <span className="text-xs text-gray-600 ml-1">{product.rating}</span>
                        </div>
                        <span className="text-xs text-gray-400 ml-2">({product.seller_name})</span>
                      </div>

                      {product.is_auction ? (
                        <div className="mb-2">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-semibold text-green-600">
                              {formatPrice(product.current_bid || product.price)}
                            </span>
                            <div className="flex items-center text-xs text-gray-500">
                              <Clock className="h-3 w-3 mr-1" />
                              {calculateTimeLeft(product.auction_end_time)}
                            </div>
                          </div>
                          <div className="text-xs text-gray-500">
                            {product.bid_count} bids
                          </div>
                        </div>
                      ) : (
                        <div className="mb-2">
                          <div className="flex items-center space-x-2">
                            <span className="text-sm font-semibold text-gray-900">
                              {formatPrice(product.price)}
                            </span>
                            {product.original_price && (
                              <span className="text-xs text-gray-500 line-through">
                                {formatPrice(product.original_price)}
                              </span>
                            )}
                          </div>
                          <div className="text-xs text-green-600 font-medium">
                            Buy It Now
                          </div>
                        </div>
                      )}

                      {product.buy_it_now && (
                        <Button
                          onClick={() => addToCart(product)}
                          size="sm"
                          className="w-full text-xs"
                        >
                          Add to Cart
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Category Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <Card className="group cursor-pointer hover:shadow-lg transition-all">
            <CardContent className="p-0">
              <div className="relative h-48 bg-gradient-to-r from-blue-500 to-purple-600 rounded-t-lg">
                <div className="absolute inset-0 bg-black bg-opacity-20 rounded-t-lg" />
                <div className="absolute inset-0 flex items-center justify-center text-white">
                  <div className="text-center">
                    <h3 className="text-xl font-bold mb-2">Electronics</h3>
                    <p className="text-sm opacity-90">Latest gadgets & tech</p>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <Link to="/search?category=electronics">
                  <Button variant="outline" className="w-full">
                    Shop Electronics
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card className="group cursor-pointer hover:shadow-lg transition-all">
            <CardContent className="p-0">
              <div className="relative h-48 bg-gradient-to-r from-green-500 to-teal-600 rounded-t-lg">
                <div className="absolute inset-0 bg-black bg-opacity-20 rounded-t-lg" />
                <div className="absolute inset-0 flex items-center justify-center text-white">
                  <div className="text-center">
                    <h3 className="text-xl font-bold mb-2">Collectibles</h3>
                    <p className="text-sm opacity-90">Rare finds & vintage items</p>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <Link to="/search?category=collectibles">
                  <Button variant="outline" className="w-full">
                    Explore Collectibles
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          <Card className="group cursor-pointer hover:shadow-lg transition-all">
            <CardContent className="p-0">
              <div className="relative h-48 bg-gradient-to-r from-orange-500 to-red-600 rounded-t-lg">
                <div className="absolute inset-0 bg-black bg-opacity-20 rounded-t-lg" />
                <div className="absolute inset-0 flex items-center justify-center text-white">
                  <div className="text-center">
                    <h3 className="text-xl font-bold mb-2">Fashion</h3>
                    <p className="text-sm opacity-90">Clothing & accessories</p>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <Link to="/search?category=clothing">
                  <Button variant="outline" className="w-full">
                    Shop Fashion
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Homepage;