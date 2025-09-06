import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Filter, Grid, List, Star, Clock, Heart } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Separator } from '../components/ui/separator';
import { Checkbox } from '../components/ui/checkbox';
import { Slider } from '../components/ui/slider';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { trendingProducts } from '../data/mockData';
import { useCart } from '../contexts/CartContext';

const SearchResults = () => {
  const [searchParams] = useSearchParams();
  const { addToCart, addToWatchlist } = useCart();
  const [products, setProducts] = useState([]);
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('relevance');
  const [priceRange, setPriceRange] = useState([0, 1000]);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    condition: [],
    listingType: [],
    brand: [],
    location: []
  });

  const query = searchParams.get('q') || '';
  const category = searchParams.get('category') || '';

  useEffect(() => {
    // Mock search functionality
    let filteredProducts = [...trendingProducts];
    
    if (query) {
      filteredProducts = filteredProducts.filter(product =>
        product.name.toLowerCase().includes(query.toLowerCase())
      );
    }
    
    if (category && category !== 'All Categories') {
      filteredProducts = filteredProducts.filter(product =>
        product.category === category.toLowerCase()
      );
    }

    // Apply price filter
    filteredProducts = filteredProducts.filter(product =>
      product.price >= priceRange[0] && product.price <= priceRange[1]
    );

    // Apply sorting
    switch (sortBy) {
      case 'price-low':
        filteredProducts.sort((a, b) => a.price - b.price);
        break;
      case 'price-high':
        filteredProducts.sort((a, b) => b.price - a.price);
        break;
      case 'ending-soon':
        filteredProducts.sort((a, b) => {
          if (!a.isAuction && !b.isAuction) return 0;
          if (!a.isAuction) return 1;
          if (!b.isAuction) return -1;
          return a.timeLeft.localeCompare(b.timeLeft);
        });
        break;
      default:
        // Keep original order for relevance
        break;
    }

    setProducts(filteredProducts);
  }, [query, category, priceRange, sortBy]);

  const formatPrice = (price) => `$${price.toFixed(2)}`;

  const ProductCard = ({ product, isListView = false }) => (
    <Card className={`group hover:shadow-lg transition-all duration-300 ${isListView ? 'mb-4' : ''}`}>
      <CardContent className="p-0">
        <div className={`${isListView ? 'flex' : ''}`}>
          <div className={`relative ${isListView ? 'w-48 flex-shrink-0' : ''}`}>
            <Link to={`/product/${product.id}`}>
              <img
                src={product.image}
                alt={product.name}
                className={`w-full object-cover group-hover:scale-105 transition-transform duration-300 ${
                  isListView ? 'h-32 rounded-l-lg' : 'h-48 rounded-t-lg'
                }`}
              />
            </Link>
            {product.originalPrice && (
              <Badge className="absolute top-2 left-2 bg-red-500 text-white">
                Sale
              </Badge>
            )}
            <button
              onClick={() => addToWatchlist(product)}
              className="absolute top-2 right-2 p-2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full transition-all"
            >
              <Heart className="h-4 w-4" />
            </button>
          </div>
          
          <div className={`p-4 ${isListView ? 'flex-1' : ''}`}>
            <Link to={`/product/${product.id}`}>
              <h3 className={`font-medium text-gray-900 mb-2 group-hover:text-blue-600 ${
                isListView ? 'text-base' : 'text-sm line-clamp-2'
              }`}>
                {product.name}
              </h3>
            </Link>
            
            <div className="flex items-center mb-2">
              <div className="flex items-center">
                <Star className="h-3 w-3 text-yellow-400 fill-current" />
                <span className="text-xs text-gray-600 ml-1">{product.rating}</span>
              </div>
              <span className="text-xs text-gray-400 ml-2">({product.seller})</span>
            </div>

            {product.isAuction ? (
              <div className="mb-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-green-600">
                    {formatPrice(product.price)}
                  </span>
                  <div className="flex items-center text-xs text-gray-500">
                    <Clock className="h-3 w-3 mr-1" />
                    {product.timeLeft}
                  </div>
                </div>
                <div className="text-xs text-gray-500">
                  {product.bids} bids
                </div>
              </div>
            ) : (
              <div className="mb-2">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-semibold text-gray-900">
                    {formatPrice(product.price)}
                  </span>
                  {product.originalPrice && (
                    <span className="text-xs text-gray-500 line-through">
                      {formatPrice(product.originalPrice)}
                    </span>
                  )}
                </div>
                <div className="text-xs text-green-600 font-medium">
                  Buy It Now
                </div>
              </div>
            )}

            {product.buyItNow && !isListView && (
              <Button
                onClick={() => addToCart(product)}
                size="sm"
                className="w-full text-xs"
              >
                Add to Cart
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Search Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2">
          {query ? `Search results for "${query}"` : `${category || 'All'} items`}
        </h1>
        <p className="text-gray-600">{products.length} results found</p>
      </div>

      <div className="flex gap-6">
        {/* Filters Sidebar */}
        <div className={`w-64 space-y-6 ${showFilters ? 'block' : 'hidden lg:block'}`}>
          <Card>
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Price Range</h3>
              <div className="space-y-4">
                <Slider
                  value={priceRange}
                  onValueChange={setPriceRange}
                  max={1000}
                  step={10}
                  className="w-full"
                />
                <div className="flex justify-between text-sm text-gray-600">
                  <span>${priceRange[0]}</span>
                  <span>${priceRange[1]}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Condition</h3>
              <div className="space-y-2">
                {['New', 'Used', 'Refurbished', 'For parts'].map((condition) => (
                  <div key={condition} className="flex items-center space-x-2">
                    <Checkbox
                      id={condition}
                      checked={filters.condition.includes(condition)}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          setFilters(prev => ({
                            ...prev,
                            condition: [...prev.condition, condition]
                          }));
                        } else {
                          setFilters(prev => ({
                            ...prev,
                            condition: prev.condition.filter(c => c !== condition)
                          }));
                        }
                      }}
                    />
                    <label htmlFor={condition} className="text-sm">
                      {condition}
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Listing Type</h3>
              <div className="space-y-2">
                {['Auction', 'Buy It Now', 'Best Offer'].map((type) => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={type}
                      checked={filters.listingType.includes(type)}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          setFilters(prev => ({
                            ...prev,
                            listingType: [...prev.listingType, type]
                          }));
                        } else {
                          setFilters(prev => ({
                            ...prev,
                            listingType: prev.listingType.filter(t => t !== type)
                          }));
                        }
                      }}
                    />
                    <label htmlFor={type} className="text-sm">
                      {type}
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <h3 className="font-semibold mb-4">Brand</h3>
              <div className="space-y-2">
                {['Nike', 'Jordan', 'Adidas', 'Puma', 'New Balance'].map((brand) => (
                  <div key={brand} className="flex items-center space-x-2">
                    <Checkbox
                      id={brand}
                      checked={filters.brand.includes(brand)}
                      onCheckedChange={(checked) => {
                        if (checked) {
                          setFilters(prev => ({
                            ...prev,
                            brand: [...prev.brand, brand]
                          }));
                        } else {
                          setFilters(prev => ({
                            ...prev,
                            brand: prev.brand.filter(b => b !== brand)
                          }));
                        }
                      }}
                    />
                    <label htmlFor={brand} className="text-sm">
                      {brand}
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {/* Controls */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="lg:hidden"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filters
              </Button>
              
              <div className="flex items-center space-x-2">
                <Button
                  variant={viewMode === 'grid' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="relevance">Best Match</SelectItem>
                <SelectItem value="price-low">Price: Low to High</SelectItem>
                <SelectItem value="price-high">Price: High to Low</SelectItem>
                <SelectItem value="ending-soon">Ending Soonest</SelectItem>
                <SelectItem value="newest">Newly Listed</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Results */}
          {products.length === 0 ? (
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold mb-2">No results found</h3>
              <p className="text-gray-600 mb-4">Try adjusting your search or filters</p>
              <Link to="/">
                <Button>Back to Home</Button>
              </Link>
            </div>
          ) : (
            <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4' : 'space-y-4'}>
              {products.map((product) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  isListView={viewMode === 'list'}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchResults;