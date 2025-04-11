import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  initSocket, 
  connectSocket, 
  disconnectSocket, 
  addEventListener, 
  removeEventListener,
  isSocketConnected,
  authenticateSocket,
  subscribeToNodeUpdates,
  unsubscribeFromNodeUpdates
} from '../api/socket';
import { useToast } from './ToastContext';

// Create context
const SocketContext = createContext();

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }) => {
  const [connected, setConnected] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);
  const [nodeUpdates, setNodeUpdates] = useState({});
  const [rewardUpdates, setRewardUpdates] = useState([]);
  const toast = useToast();
  
  useEffect(() => {
    // Initialize socket
    initSocket();
    
    // Connect to socket
    connectSocket();
    
    // Register event listeners
    const handleConnect = () => {
      setConnected(true);
    };
    
    const handleDisconnect = () => {
      setConnected(false);
      setAuthenticated(false);
    };
    
    const handleAuthenticated = (data) => {
      setAuthenticated(true);
      toast.success('Real-time connection established');
    };
    
    const handleAuthenticationError = (error) => {
      setAuthenticated(false);
      toast.error(`Real-time authentication failed: ${error.message}`);
    };
    
    const handleNodeStatusUpdate = (data) => {
      setNodeUpdates(prev => ({
        ...prev,
        [data.node_id]: data
      }));
    };
    
    const handleRewardUpdate = (data) => {
      setRewardUpdates(prev => [data, ...prev].slice(0, 10));
      toast.info(`Received ${data.total_points} new points!`);
    };
    
    // Add event listeners
    addEventListener('connect', handleConnect);
    addEventListener('disconnect', handleDisconnect);
    addEventListener('authenticated', handleAuthenticated);
    addEventListener('authentication_error', handleAuthenticationError);
    addEventListener('node_status_update', handleNodeStatusUpdate);
    addEventListener('reward_update', handleRewardUpdate);
    
    // Clean up on unmount
    return () => {
      removeEventListener('connect', handleConnect);
      removeEventListener('disconnect', handleDisconnect);
      removeEventListener('authenticated', handleAuthenticated);
      removeEventListener('authentication_error', handleAuthenticationError);
      removeEventListener('node_status_update', handleNodeStatusUpdate);
      removeEventListener('reward_update', handleRewardUpdate);
      disconnectSocket();
    };
  }, [toast]);
  
  // Subscribe to node updates
  const subscribeToNode = (nodeId) => {
    subscribeToNodeUpdates(nodeId);
  };
  
  // Unsubscribe from node updates
  const unsubscribeFromNode = (nodeId) => {
    unsubscribeFromNodeUpdates(nodeId);
  };
  
  // Get latest node status
  const getNodeStatus = (nodeId) => {
    return nodeUpdates[nodeId];
  };
  
  // Get recent reward updates
  const getRecentRewards = () => {
    return rewardUpdates;
  };
  
  // Context value
  const contextValue = {
    connected,
    authenticated,
    subscribeToNode,
    unsubscribeFromNode,
    getNodeStatus,
    getRecentRewards,
    nodeUpdates,
    rewardUpdates
  };
  
  return (
    <SocketContext.Provider value={contextValue}>
      {children}
    </SocketContext.Provider>
  );
};

export default SocketContext;
