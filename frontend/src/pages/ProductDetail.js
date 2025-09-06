import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Star, Heart, Share2, Clock, User, Shield, 
  ChevronLeft, ChevronRight, Plus, Minus 
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Separator } from '../components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { trendingProducts, sampleReviews } from '../data/mockData';
import { useCart } from '../contexts/CartContext';
import { useToast } from '../hooks/use-toast';

const ProductDetail = () => {
  const { id } = useParams();
  const { addToCart, addToWatchlist } = useCart();
  const { toast } = useToast();
  const [product, setProduct] = useState(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [bidAmount, setBidAmount] = useState('');
  const [timeLeft, setTimeLeft] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });

  // Mock product images
  const productImages = [
    product?.image,
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop",
    "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop",
    "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=600&h=600&fit=crop"
  ].filter(Boolean);

  useEffect(() => {
    // Find product by ID
    const foundProduct = trendingProducts.find(p => p.id === parseInt(id));
    if (foundProduct) {
      setProduct(foundProduct);
      if (foundProduct.isAuction) {
        setBidAmount((foundProduct.price + 5).toFixed(2));
      }
    }
  }, [id]);

  useEffect(() => {
    if (product?.isAuction && product?.timeLeft) {
      const timer = setInterval(() => {
        // Mock countdown timer
        setTimeLeft(prev => {
          if (prev.seconds > 0) {
            return { ...prev, seconds: prev.seconds - 1 };
          } else if (prev.minutes > 0) {
            return { ...prev, minutes: prev.minutes - 1, seconds: 59 };
          } else if (prev.hours > 0) {
            return { ...prev, hours: prev.hours - 1, minutes: 59, seconds: 59 };
          } else if (prev.days > 0) {
            return { ...prev, days: prev.days - 1, hours: 23, minutes: 59, seconds: 59 };
          }
          return prev;
        });
      }, 1000);

      // Initialize timer based on timeLeft string
      const [days, hours] = product.timeLeft.split(' ');
      setTimeLeft({
        days: parseInt(days) || 0,
        hours: parseInt(hours) || 0,
        minutes: Math.floor(Math.random() * 60),
        seconds: Math.floor(Math.random() * 60)
      });

      return () => clearInterval(timer);
    }
  }, [product]);

  const handleAddToCart = () => {
    addToCart({ ...product, quantity });
    toast({
      title: "Added to cart",
      description: `${product.name} has been added to your cart.`,
    });
  };

  const handleAddToWatchlist = () => {
    addToWatchlist(product);
    toast({
      title: "Added to watchlist",
      description: `${product.name} has been added to your watchlist.`,
    });
  };

  const handlePlaceBid = () => {
    toast({
      title: "Bid placed successfully!",
      description: `Your bid of $${bidAmount} has been placed.`,
    });
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % productImages.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + productImages.length) % productImages.length);
  };

  if (!product) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Product not found</h2>
          <p className="text-gray-600 mb-4">The product you're looking for doesn't exist.</p>
          <Link to="/">
            <Button>Back to Home</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center space-x-2 text-sm text-gray-600 mb-6">
        <Link to="/" className="hover:text-blue-600">Home</Link>
        <span>/</span>
        <Link to={`/search?category=${product.category}`} className="hover:text-blue-600 capitalize">
          {product.category}
        </Link>
        <span>/</span>
        <span className="text-gray-900">{product.name}</span>
      </nav>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Product Images */}
        <div className="space-y-4">
          <div className="relative">
            <img
              src={productImages[currentImageIndex]}
              alt={product.name}
              className="w-full h-96 object-cover rounded-lg"
            />
            {productImages.length > 1 && (
              <>
                <button
                  onClick={prevImage}
                  className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 p-2 rounded-full"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                <button
                  onClick={nextImage}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 p-2 rounded-full"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </>
            )}
          </div>
          
          {productImages.length > 1 && (
            <div className="flex space-x-2 overflow-x-auto">
              {productImages.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentImageIndex(index)}
                  className={`flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 ${
                    index === currentImageIndex ? 'border-blue-600' : 'border-gray-200'
                  }`}
                >
                  <img src={image} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{product.name}</h1>
            <div className="flex items-center space-x-4 mb-4">
              <div className="flex items-center">
                <Star className="h-4 w-4 text-yellow-400 fill-current" />
                <span className="text-sm text-gray-600 ml-1">{product.rating}</span>
                <span className="text-sm text-gray-400 ml-1">(127 reviews)</span>
              </div>
              <div className="flex items-center space-x-2">
                <Button variant="ghost" size="sm" onClick={handleAddToWatchlist}>
                  <Heart className="h-4 w-4 mr-1" />
                  Watch
                </Button>
                <Button variant="ghost" size="sm">
                  <Share2 className="h-4 w-4 mr-1" />
                  Share
                </Button>
              </div>
            </div>
          </div>

          {/* Price and Bidding */}
          {product.isAuction ? (
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      ${product.price.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-600">{product.bids} bids</div>
                  </div>
                  <div className="text-right">
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <Clock className="h-4 w-4 mr-1" />
                      Time left
                    </div>
                    <div className="text-lg font-semibold text-red-600">
                      {timeLeft.days}d {timeLeft.hours}h {timeLeft.minutes}m {timeLeft.seconds}s
                    </div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Input
                      type="number"
                      value={bidAmount}
                      onChange={(e) => setBidAmount(e.target.value)}
                      placeholder="Enter bid amount"
                      className="flex-1"
                      step="0.01"
                      min={product.price + 0.01}
                    />
                    <Button onClick={handlePlaceBid} className="px-6">
                      Place Bid
                    </Button>
                  </div>
                  <div className="text-xs text-gray-500">
                    Minimum bid: ${(product.price + 0.01).toFixed(2)}
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-2xl font-bold text-gray-900 mb-1">
                      ${product.price.toFixed(2)}
                    </div>
                    {product.originalPrice && (
                      <div className="text-sm text-gray-500 line-through">
                        ${product.originalPrice.toFixed(2)}
                      </div>
                    )}
                    <Badge className="bg-green-100 text-green-800 mt-2">Buy It Now</Badge>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <label className="text-sm font-medium">Quantity:</label>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setQuantity(Math.max(1, quantity - 1))}
                      >
                        <Minus className="h-3 w-3" />
                      </Button>
                      <span className="w-8 text-center">{quantity}</span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setQuantity(quantity + 1)}
                      >
                        <Plus className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <Button onClick={handleAddToCart} className="flex-1">
                      Add to Cart
                    </Button>
                    <Button variant="outline" className="flex-1">
                      Buy It Now
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Seller Info */}
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                  <User className="h-6 w-6 text-gray-500" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold">{product.seller}</h3>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Star className="h-3 w-3 text-yellow-400 fill-current mr-1" />
                      {product.rating} (1,234 reviews)
                    </div>
                    <span>•</span>
                    <span>99.2% positive feedback</span>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  Contact Seller
                </Button>
              </div>
              
              <Separator className="my-4" />
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div className="flex items-center space-x-2">
                  <Shield className="h-4 w-4 text-green-600" />
                  <span>eBay Money Back Guarantee</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Shield className="h-4 w-4 text-blue-600" />
                  <span>Fast & Free Shipping</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Product Details Tabs */}
      <Tabs defaultValue="description" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="description">Description</TabsTrigger>
          <TabsTrigger value="shipping">Shipping & Returns</TabsTrigger>
          <TabsTrigger value="reviews">Reviews (127)</TabsTrigger>
        </TabsList>
        
        <TabsContent value="description" className="mt-6">
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-4">Product Description</h3>
              <div className="prose prose-sm max-w-none">
                <p>
                  This authentic {product.name} is in excellent condition and comes from a trusted seller. 
                  Perfect for collectors and enthusiasts alike.
                </p>
                <ul className="mt-4 space-y-2">
                  <li>• Authentic and verified</li>
                  <li>• Excellent condition</li>
                  <li>• Comes with original packaging</li>
                  <li>• Fast and secure shipping</li>
                  <li>• 30-day return policy</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="shipping" className="mt-6">
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-4">Shipping & Returns</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-2">Shipping Options</h4>
                  <ul className="space-y-2 text-sm">
                    <li>• Standard Shipping: 3-5 business days - $9.99</li>
                    <li>• Express Shipping: 1-2 business days - $19.99</li>
                    <li>• Overnight Shipping: Next business day - $29.99</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Returns</h4>
                  <ul className="space-y-2 text-sm">
                    <li>• 30-day return policy</li>
                    <li>• Buyer pays return shipping</li>
                    <li>• Item must be in original condition</li>
                    <li>• Full refund upon return</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="reviews" className="mt-6">
          <Card>
            <CardContent className="p-6">
              <h3 className="font-semibold mb-4">Customer Reviews</h3>
              <div className="space-y-6">
                {sampleReviews.map((review) => (
                  <div key={review.id} className="border-b last:border-b-0 pb-4 last:pb-0">
                    <div className="flex items-center space-x-2 mb-2">
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${
                              i < review.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                      <span className="font-medium">{review.user}</span>
                      <span className="text-sm text-gray-500">{review.date}</span>
                    </div>
                    <p className="text-gray-700">{review.comment}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProductDetail;