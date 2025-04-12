/**
 * API configuration for the GradientLab frontend.
 */

// Base API URL
// In development, use the local backend
// In production, use the Heroku backend
export const API_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://gradientlab-api.herokuapp.com/api'
    : 'http://localhost:5000/api');

// WebSocket URL
// In development, use the local backend
// In production, use the Heroku backend
export const WS_URL = process.env.REACT_APP_WS_URL || 
  (process.env.NODE_ENV === 'production'
    ? 'wss://gradientlab-api.herokuapp.com'
    : 'ws://localhost:5000');

// Default request timeout in milliseconds
export const REQUEST_TIMEOUT = 30000;

// Default headers for API requests
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
};

// Authentication token storage key
export const TOKEN_STORAGE_KEY = 'gradientlab_token';

// User storage key
export const USER_STORAGE_KEY = 'gradientlab_user';

// Function to get the authentication token from local storage
export const getToken = () => localStorage.getItem(TOKEN_STORAGE_KEY);

// Function to set the authentication token in local storage
export const setToken = (token) => localStorage.setItem(TOKEN_STORAGE_KEY, token);

// Function to remove the authentication token from local storage
export const removeToken = () => localStorage.removeItem(TOKEN_STORAGE_KEY);

// Function to get the user from local storage
export const getUser = () => {
  const user = localStorage.getItem(USER_STORAGE_KEY);
  return user ? JSON.parse(user) : null;
};

// Function to set the user in local storage
export const setUser = (user) => localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));

// Function to remove the user from local storage
export const removeUser = () => localStorage.removeItem(USER_STORAGE_KEY);
