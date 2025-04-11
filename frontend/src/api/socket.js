import { io } from 'socket.io-client';
import { isAuthenticated } from './auth';

// Socket.io instance
let socket = null;

// Event listeners
const listeners = {
  'node_status_update': [],
  'reward_update': [],
  'authenticated': [],
  'authentication_error': [],
  'connect': [],
  'disconnect': [],
  'error': []
};

/**
 * Initialize WebSocket connection
 * @returns {Object} - Socket instance
 */
export const initSocket = () => {
  if (socket) {
    // Socket already initialized
    return socket;
  }
  
  const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';
  
  // Create socket instance
  socket = io(SOCKET_URL, {
    autoConnect: false,
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    timeout: 20000,
    transports: ['websocket', 'polling']
  });
  
  // Register event handlers
  socket.on('connect', () => {
    console.log('Socket connected');
    notifyListeners('connect');
    
    // Authenticate if user is logged in
    if (isAuthenticated()) {
      authenticateSocket();
    }
  });
  
  socket.on('disconnect', () => {
    console.log('Socket disconnected');
    notifyListeners('disconnect');
  });
  
  socket.on('error', (error) => {
    console.error('Socket error:', error);
    notifyListeners('error', error);
  });
  
  socket.on('node_status_update', (data) => {
    console.log('Node status update:', data);
    notifyListeners('node_status_update', data);
  });
  
  socket.on('reward_update', (data) => {
    console.log('Reward update:', data);
    notifyListeners('reward_update', data);
  });
  
  socket.on('authenticated', (data) => {
    console.log('Socket authenticated:', data);
    notifyListeners('authenticated', data);
  });
  
  socket.on('authentication_error', (error) => {
    console.error('Socket authentication error:', error);
    notifyListeners('authentication_error', error);
  });
  
  return socket;
};

/**
 * Connect to WebSocket server
 */
export const connectSocket = () => {
  if (!socket) {
    initSocket();
  }
  
  if (!socket.connected) {
    socket.connect();
  }
};

/**
 * Disconnect from WebSocket server
 */
export const disconnectSocket = () => {
  if (socket && socket.connected) {
    socket.disconnect();
  }
};

/**
 * Authenticate socket connection
 */
export const authenticateSocket = () => {
  if (!socket || !socket.connected) {
    console.error('Socket not connected');
    return;
  }
  
  const token = localStorage.getItem('token');
  if (!token) {
    console.error('No token available for socket authentication');
    return;
  }
  
  socket.emit('authenticate', { token });
};

/**
 * Subscribe to node status updates
 * @param {number} nodeId - Node ID to subscribe to
 */
export const subscribeToNodeUpdates = (nodeId) => {
  if (!socket || !socket.connected) {
    console.error('Socket not connected');
    return;
  }
  
  socket.emit('subscribe_node_updates', { node_id: nodeId });
};

/**
 * Unsubscribe from node status updates
 * @param {number} nodeId - Node ID to unsubscribe from
 */
export const unsubscribeFromNodeUpdates = (nodeId) => {
  if (!socket || !socket.connected) {
    console.error('Socket not connected');
    return;
  }
  
  socket.emit('unsubscribe_node_updates', { node_id: nodeId });
};

/**
 * Add event listener
 * @param {string} event - Event name
 * @param {Function} callback - Callback function
 */
export const addEventListener = (event, callback) => {
  if (!listeners[event]) {
    listeners[event] = [];
  }
  
  listeners[event].push(callback);
};

/**
 * Remove event listener
 * @param {string} event - Event name
 * @param {Function} callback - Callback function
 */
export const removeEventListener = (event, callback) => {
  if (!listeners[event]) {
    return;
  }
  
  listeners[event] = listeners[event].filter(cb => cb !== callback);
};

/**
 * Notify all listeners of an event
 * @param {string} event - Event name
 * @param {*} data - Event data
 */
const notifyListeners = (event, data) => {
  if (!listeners[event]) {
    return;
  }
  
  listeners[event].forEach(callback => {
    try {
      callback(data);
    } catch (error) {
      console.error(`Error in ${event} listener:`, error);
    }
  });
};

/**
 * Get socket connection status
 * @returns {boolean} - Whether socket is connected
 */
export const isSocketConnected = () => {
  return socket && socket.connected;
};
