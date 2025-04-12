import axios from 'axios';
import { API_URL, DEFAULT_HEADERS, getToken, setToken, setUser, removeToken, removeUser } from './config';

// Base URL for authentication
const AUTH_BASE_URL = `${API_URL}/auth`;

// Create axios instance with auth headers
const authApi = axios.create({
  baseURL: AUTH_BASE_URL,
  headers: DEFAULT_HEADERS
});

// Add interceptor to include auth token in requests
authApi.interceptors.request.use(
  config => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Login function
export const login = async (username, password, otpCode = null) => {
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
        setToken(mockToken);
        setUser(mockUser);

        return mockUser;
      } else {
        // Simulate failed login
        throw new Error('Invalid username or password');
      }
    }

    // Prepare payload
    const payload = { username, password };

    // Add OTP code if provided
    if (otpCode) {
      payload.otp_code = otpCode;
    }

    // Real API call
    const response = await authApi.post('/login', payload);

    if (response.data.status === 'success') {
      const { access_token, user } = response.data.data;

      // Store token and user info in localStorage
      setToken(access_token);
      setUser(user);

      return user;
    } else if (response.data.status === 'partial') {
      // Return partial authentication for 2FA
      return response.data.data;
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
      await authApi.post('/logout');
    }

    // Remove token and user info from localStorage
    removeToken();
    removeUser();

    return true;
  } catch (error) {
    console.error('Logout error:', error);

    // Still remove local storage items even if API call fails
    removeToken();
    removeUser();

    return true;
  }
};

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};

// Get current user
export const getCurrentUser = () => {
  return getUser();
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
    const response = await authApi.post('/register', userData);

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
    const response = await authApi.post('/change-password', {
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
