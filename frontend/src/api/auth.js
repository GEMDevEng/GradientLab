import axios from 'axios';

// Base URL for authentication
const AUTH_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with auth headers
const authApi = axios.create({
  baseURL: AUTH_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add interceptor to include auth token in requests
authApi.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Login function
export const login = async (username, password) => {
  try {
    // For development/testing, allow mock login
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
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

        return mockUser;
      } else {
        // Simulate failed login
        throw new Error('Invalid username or password');
      }
    }

    // Real API call
    const response = await authApi.post('/auth/login', { username, password });

    if (response.data.status === 'success') {
      const { access_token, user } = response.data.data;

      // Store token and user info in localStorage
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));

      return user;
    } else {
      throw new Error(response.data.message || 'Authentication failed');
    }
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      throw new Error(error.response.data.message || 'Authentication failed');
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response from server. Please check your connection.');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw error;
    }
  }
};

// Logout function
export const logout = async () => {
  try {
    // Call logout API if not using mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH !== 'true') {
      await authApi.post('/auth/logout');
    }

    // Remove token and user info from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    return true;
  } catch (error) {
    console.error('Logout error:', error);

    // Still remove local storage items even if API call fails
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    return true;
  }
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
    try {
      return JSON.parse(userStr);
    } catch (e) {
      console.error('Error parsing user data:', e);
      return null;
    }
  }
  return null;
};

// Register function
export const register = async (userData) => {
  try {
    // For development/testing, allow mock registration
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      // Simulate successful registration
      return { username: userData.username };
    }

    // Real API call
    const response = await authApi.post('/auth/register', userData);

    if (response.data.status === 'success') {
      return response.data.data.user;
    } else {
      throw new Error(response.data.message || 'Registration failed');
    }
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message || 'Registration failed');
    } else if (error.request) {
      throw new Error('No response from server. Please check your connection.');
    } else {
      throw error;
    }
  }
};

// Change password function
export const changePassword = async (currentPassword, newPassword) => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      // Simulate password change
      if (currentPassword === 'password') {
        return true;
      } else {
        throw new Error('Current password is incorrect');
      }
    }

    // Real API call
    const response = await authApi.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword
    });

    if (response.data.status === 'success') {
      return true;
    } else {
      throw new Error(response.data.message || 'Password change failed');
    }
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message || 'Password change failed');
    } else if (error.request) {
      throw new Error('No response from server. Please check your connection.');
    } else {
      throw error;
    }
  }
};
