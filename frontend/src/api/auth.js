import axios from 'axios';

// Base URL for authentication
const AUTH_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Login function
export const login = async (username, password) => {
  try {
    // This is a mock implementation since we don't have a real auth endpoint yet
    // In a real app, you would make an API call to authenticate
    if (username === 'admin' && password === 'password') {
      // Simulate successful login
      const mockToken = 'mock-jwt-token';
      const mockUser = {
        id: 1,
        username: 'admin',
        name: 'Admin User',
        role: 'admin'
      };
      
      // Store token and user info in localStorage
      localStorage.setItem('token', mockToken);
      localStorage.setItem('user', JSON.stringify(mockUser));
      
      return {
        success: true,
        token: mockToken,
        user: mockUser
      };
    } else {
      // Simulate failed login
      return {
        success: false,
        message: 'Invalid username or password'
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error.response?.data?.message || 'Authentication failed'
    };
  }
};

// Logout function
export const logout = () => {
  // Remove token and user info from localStorage
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  
  return {
    success: true
  };
};

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  return !!token;
};

// Get current user
export const getCurrentUser = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    return JSON.parse(userStr);
  }
  return null;
};

// Register function (for future use)
export const register = async (userData) => {
  try {
    // This is a mock implementation
    // In a real app, you would make an API call to register
    return {
      success: true,
      message: 'Registration successful'
    };
  } catch (error) {
    return {
      success: false,
      message: error.response?.data?.message || 'Registration failed'
    };
  }
};
