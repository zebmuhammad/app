import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Search, ShoppingCart, User, Heart, Menu, ChevronDown } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';
import { productsAPI } from '../services/api';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from './ui/dropdown-menu';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';
import { Label } from './ui/label';

const Header = () => {
  const { getTotalItems, watchlist } = useCart();
  const { user, login, register, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [categories, setCategories] = useState([]);
  const [showLoginDialog, setShowLoginDialog] = useState(false);
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const cats = await productsAPI.getCategories();
        setCategories(cats);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };
    fetchCategories();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}&category=${selectedCategory}`);
    }
  };

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    let result;
    
    if (isLoginMode) {
      result = await login(formData.email, formData.password);
    } else {
      result = await register(formData.name, formData.email, formData.password);
    }
    
    if (result.success) {
      setShowLoginDialog(false);
      setFormData({ name: '', email: '', password: '' });
    } else {
      alert(result.error || 'Authentication failed');
    }
  };

  return (
    <div className="bg-white border-b">
      {/* Top Bar */}
      <div className="px-4 py-2 text-xs bg-gray-50 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <span>Hi! 
            {isAuthenticated ? (
              <Link to="/profile" className="text-blue-600 hover:underline ml-1">
                {user.name}
              </Link>
            ) : (
              <>
                <button 
                  onClick={() => {
                    setIsLoginMode(true);
                    setShowLoginDialog(true);
                  }}
                  className="text-blue-600 hover:underline ml-1"
                >
                  Sign in
                </button>
                <span className="mx-1">or</span>
                <button 
                  onClick={() => {
                    setIsLoginMode(false);
                    setShowLoginDialog(true);
                  }}
                  className="text-blue-600 hover:underline"
                >
                  register
                </button>
              </>
            )}
          </span>
          <Link to="/deals" className="text-gray-600 hover:text-blue-600">Daily Deals</Link>
          <Link to="/outlet" className="text-gray-600 hover:text-blue-600">Brand Outlet</Link>
          <Link to="/help" className="text-gray-600 hover:text-blue-600">Help & Contact</Link>
        </div>
        <div className="flex items-center space-x-4">
          <Link to="/sell" className="text-gray-600 hover:text-blue-600">Sell</Link>
          <Link to="/watchlist" className="text-gray-600 hover:text-blue-600 flex items-center">
            Watchlist
            {watchlist.length > 0 && (
              <Badge variant="secondary" className="ml-1 text-xs">
                {watchlist.length}
              </Badge>
            )}
          </Link>
          <Link to="/myeasycart" className="text-gray-600 hover:text-blue-600">My EasyCart</Link>
        </div>
      </div>

      {/* Main Header */}
      <div className="px-4 py-3">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <div className="text-3xl font-bold">
              <span className="text-red-500">E</span>
              <span className="text-blue-500">a</span>
              <span className="text-yellow-500">s</span>
              <span className="text-green-500">y</span>
              <span className="text-purple-500">C</span>
              <span className="text-orange-500">a</span>
              <span className="text-pink-500">r</span>
              <span className="text-indigo-500">t</span>
            </div>
          </Link>

          {/* Search Bar */}
          <div className="flex-1 max-w-3xl mx-8">
            <form onSubmit={handleSearch} className="flex">
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" className="rounded-r-none border-r-0 min-w-[140px] justify-between">
                    <span className="truncate">{selectedCategory}</span>
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56">
                  <DropdownMenuItem onClick={() => setSelectedCategory('All Categories')}>
                    All Categories
                  </DropdownMenuItem>
                  {categories.map((category) => (
                    <DropdownMenuItem key={category} onClick={() => setSelectedCategory(category)}>
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
              
              <Input
                type="text"
                placeholder="Search for anything"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 rounded-none border-l-0 border-r-0"
              />
              
              <Button type="submit" className="rounded-l-none bg-blue-600 hover:bg-blue-700">
                <Search className="h-4 w-4 mr-2" />
                Search
              </Button>
            </form>
            <div className="text-xs text-gray-500 mt-1">Advanced</div>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            <Link to="/cart" className="relative">
              <ShoppingCart className="h-6 w-6 text-gray-600 hover:text-blue-600" />
              {getTotalItems() > 0 && (
                <Badge className="absolute -top-2 -right-2 bg-red-500 text-white text-xs">
                  {getTotalItems()}
                </Badge>
              )}
            </Link>
            
            {isAuthenticated && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="flex items-center space-x-2">
                    <img 
                      src={user.avatar} 
                      alt={user.name}
                      className="h-6 w-6 rounded-full"
                    />
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={() => navigate('/profile')}>
                    Profile
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate('/orders')}>
                    My Orders
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate('/selling')}>
                    Selling
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={logout}>
                    Sign Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>
        </div>
      </div>

      {/* Category Navigation */}
      <div className="bg-gray-50 px-4 py-2 border-t">
        <div className="flex items-center space-x-6 max-w-7xl mx-auto overflow-x-auto">
          {['electronics', 'sneakers', 'clothing', 'collectibles', 'home', 'toys'].map((category) => (
            <Link
              key={category}
              to={`/search?category=${category}`}
              className="text-sm text-gray-600 hover:text-blue-600 whitespace-nowrap py-1 capitalize"
            >
              {category}
            </Link>
          ))}
        </div>
      </div>

      {/* Auth Dialog */}
      <Dialog open={showLoginDialog} onOpenChange={setShowLoginDialog}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>
              {isLoginMode ? 'Sign In' : 'Create Account'}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleAuthSubmit} className="space-y-4">
            {!isLoginMode && (
              <div>
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required={!isLoginMode}
                />
              </div>
            )}
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>
            <Button type="submit" className="w-full">
              {isLoginMode ? 'Sign In' : 'Create Account'}
            </Button>
            <div className="text-center">
              <button
                type="button"
                onClick={() => setIsLoginMode(!isLoginMode)}
                className="text-sm text-blue-600 hover:underline"
              >
                {isLoginMode ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
              </button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Header;