import React, { useState } from 'react';
import { Star, Package, Heart, Settings, User, CreditCard, MapPin } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../contexts/CartContext';

const Profile = () => {
  const { user } = useAuth();
  const { watchlist } = useCart();
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: 'Passionate collector and sneaker enthusiast. Always looking for rare finds and authentic pieces.',
    location: 'New York, NY',
    phone: '+1 (555) 123-4567'
  });

  // Mock order data
  const recentOrders = [
    {
      id: 'ORD-001',
      date: '2025-01-15',
      status: 'Delivered',
      total: 299.99,
      items: 1,
      image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=100&h=100&fit=crop'
    },
    {
      id: 'ORD-002',
      date: '2025-01-12',
      status: 'In Transit',
      total: 189.99,
      items: 1,
      image: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=100&h=100&fit=crop'
    },
    {
      id: 'ORD-003',
      date: '2025-01-08',
      status: 'Processing',
      total: 459.99,
      items: 1,
      image: 'https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?w=100&h=100&fit=crop'
    }
  ];

  const handleSave = () => {
    // In a real app, this would update the user profile via API
    setEditMode(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Delivered':
        return 'bg-green-100 text-green-800';
      case 'In Transit':
        return 'bg-blue-100 text-blue-800';
      case 'Processing':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (!user) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Please sign in to view your profile</h2>
          <p className="text-gray-600">You need to be logged in to access this page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Profile Sidebar */}
        <div className="lg:col-span-1">
          <Card>
            <CardContent className="p-6 text-center">
              <img
                src={user.avatar}
                alt={user.name}
                className="w-24 h-24 rounded-full mx-auto mb-4"
              />
              <h2 className="text-xl font-bold mb-2">{user.name}</h2>
              <p className="text-gray-600 mb-4">{user.email}</p>
              
              <div className="flex items-center justify-center mb-4">
                <div className="flex items-center">
                  <Star className="h-4 w-4 text-yellow-400 fill-current mr-1" />
                  <span className="font-medium">{user.rating}</span>
                </div>
                <span className="text-gray-400 mx-2">•</span>
                <span className="text-sm text-gray-600">Member since {user.memberSince}</span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="text-center">
                  <div className="font-bold text-lg">127</div>
                  <div className="text-xs text-gray-600">Purchases</div>
                </div>
                <div className="text-center">
                  <div className="font-bold text-lg">34</div>
                  <div className="text-xs text-gray-600">Sales</div>
                </div>
              </div>
              
              <Button
                variant={editMode ? "default" : "outline"}
                className="w-full"
                onClick={() => setEditMode(!editMode)}
              >
                <Settings className="h-4 w-4 mr-2" />
                {editMode ? 'Cancel Edit' : 'Edit Profile'}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-3">
          <Tabs defaultValue="overview" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="orders">Orders</TabsTrigger>
              <TabsTrigger value="watchlist">Watchlist</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>
            
            <TabsContent value="overview" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Account Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <Package className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <div className="font-bold text-2xl text-blue-600">3</div>
                      <div className="text-sm text-gray-600">Active Orders</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <Star className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <div className="font-bold text-2xl text-green-600">{user.rating}</div>
                      <div className="text-sm text-gray-600">Seller Rating</div>
                    </div>
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <Heart className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                      <div className="font-bold text-2xl text-purple-600">{watchlist.length}</div>
                      <div className="text-sm text-gray-600">Watched Items</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentOrders.slice(0, 3).map((order) => (
                      <div key={order.id} className="flex items-center space-x-4 p-4 border rounded-lg">
                        <img
                          src={order.image}
                          alt="Order item"
                          className="w-12 h-12 object-cover rounded"
                        />
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <div>
                              <div className="font-medium">Order {order.id}</div>
                              <div className="text-sm text-gray-600">{order.date}</div>
                            </div>
                            <div className="text-right">
                              <div className="font-medium">${order.total}</div>
                              <Badge className={getStatusColor(order.status)}>
                                {order.status}
                              </Badge>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="orders" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Order History</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentOrders.map((order) => (
                      <div key={order.id} className="flex items-center space-x-4 p-4 border rounded-lg">
                        <img
                          src={order.image}
                          alt="Order item"
                          className="w-16 h-16 object-cover rounded"
                        />
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <div>
                              <div className="font-medium text-lg">Order {order.id}</div>
                              <div className="text-sm text-gray-600">{order.date} • {order.items} item(s)</div>
                            </div>
                            <div className="text-right">
                              <div className="font-bold text-lg">${order.total}</div>
                              <Badge className={getStatusColor(order.status)}>
                                {order.status}
                              </Badge>
                            </div>
                          </div>
                          <div className="flex space-x-2 mt-3">
                            <Button size="sm" variant="outline">Track Order</Button>
                            <Button size="sm" variant="outline">View Details</Button>
                            {order.status === 'Delivered' && (
                              <Button size="sm" variant="outline">Leave Review</Button>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="watchlist" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Your Watchlist ({watchlist.length} items)</CardTitle>
                </CardHeader>
                <CardContent>
                  {watchlist.length === 0 ? (
                    <div className="text-center py-8">
                      <Heart className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                      <h3 className="text-lg font-medium mb-2">No items in your watchlist</h3>
                      <p className="text-gray-600">Start watching items to keep track of them here.</p>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {watchlist.map((item) => (
                        <div key={item.id} className="flex space-x-4 p-4 border rounded-lg">
                          <img
                            src={item.image}
                            alt={item.name}
                            className="w-16 h-16 object-cover rounded"
                          />
                          <div className="flex-1">
                            <h4 className="font-medium mb-1">{item.name}</h4>
                            <p className="text-lg font-bold text-green-600">${item.price}</p>
                            <div className="flex space-x-2 mt-2">
                              <Button size="sm">Buy Now</Button>
                              <Button size="sm" variant="outline">Remove</Button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
            
            <TabsContent value="settings" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Profile Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="name">Full Name</Label>
                      <Input
                        id="name"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                        disabled={!editMode}
                      />
                    </div>
                    <div>
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                        disabled={!editMode}
                      />
                    </div>
                    <div>
                      <Label htmlFor="phone">Phone</Label>
                      <Input
                        id="phone"
                        value={formData.phone}
                        onChange={(e) => setFormData({...formData, phone: e.target.value})}
                        disabled={!editMode}
                      />
                    </div>
                    <div>
                      <Label htmlFor="location">Location</Label>
                      <Input
                        id="location"
                        value={formData.location}
                        onChange={(e) => setFormData({...formData, location: e.target.value})}
                        disabled={!editMode}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="bio">Bio</Label>
                    <Textarea
                      id="bio"
                      value={formData.bio}
                      onChange={(e) => setFormData({...formData, bio: e.target.value})}
                      disabled={!editMode}
                      rows={3}
                    />
                  </div>
                  
                  {editMode && (
                    <div className="flex space-x-2">
                      <Button onClick={handleSave}>Save Changes</Button>
                      <Button variant="outline" onClick={() => setEditMode(false)}>
                        Cancel
                      </Button>
                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Profile;