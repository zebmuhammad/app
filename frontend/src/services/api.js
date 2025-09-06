import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  login: async (email, password) => {
    const response = await apiClient.post('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (name, email, password) => {
    const response = await apiClient.post('/auth/register', { name, email, password });
    return response.data;
  },
  
  logout: async () => {
    await apiClient.post('/auth/logout');
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },
  
  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  }
};

// Products API
export const productsAPI = {
  getProducts: async (params = {}) => {
    const response = await apiClient.get('/products', { params });
    return response.data;
  },
  
  getProduct: async (id) => {
    const response = await apiClient.get(`/products/${id}`);
    return response.data;
  },
  
  searchProducts: async (query, params = {}) => {
    const response = await apiClient.get('/products/search', { 
      params: { q: query, ...params } 
    });
    return response.data;
  },
  
  getCategories: async () => {
    const response = await apiClient.get('/products/categories');
    return response.data;
  },
  
  placeBid: async (productId, bidAmount) => {
    const response = await apiClient.post(`/products/${productId}/bid`, null, {
      params: { bid_amount: bidAmount }
    });
    return response.data;
  },
  
  getBidHistory: async (productId) => {
    const response = await apiClient.get(`/products/${productId}/bids`);
    return response.data;
  }
};

// Users API
export const usersAPI = {
  getProfile: async () => {
    const response = await apiClient.get('/users/profile');
    return response.data;
  },
  
  updateProfile: async (data) => {
    const response = await apiClient.put('/users/profile', data);
    return response.data;
  },
  
  getOrders: async () => {
    const response = await apiClient.get('/users/orders');
    return response.data;
  },
  
  getWatchlist: async () => {
    const response = await apiClient.get('/users/watchlist');
    return response.data;
  },
  
  addToWatchlist: async (productId) => {
    const response = await apiClient.post(`/users/watchlist/${productId}`);
    return response.data;
  },
  
  removeFromWatchlist: async (productId) => {
    const response = await apiClient.delete(`/users/watchlist/${productId}`);
    return response.data;
  }
};

// Orders API
export const ordersAPI = {
  createOrder: async (orderData) => {
    const response = await apiClient.post('/orders/create', orderData);
    return response.data;
  },
  
  getOrder: async (orderId) => {
    const response = await apiClient.get(`/orders/${orderId}`);
    return response.data;
  }
};

export default apiClient;