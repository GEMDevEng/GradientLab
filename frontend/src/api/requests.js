import axios from 'axios';

// Base URL for API requests
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// VM API requests
export const getVMs = () => api.get('/vm/vms');
export const createVM = (vmData) => api.post('/vm/vms', vmData);
export const getVM = (id) => api.get(`/vm/vms/${id}`);
export const updateVM = (id, vmData) => api.put(`/vm/vms/${id}`, vmData);
export const deleteVM = (id) => api.delete(`/vm/vms/${id}`);
export const startVM = (id) => api.post(`/vm/vms/${id}/start`);
export const stopVM = (id) => api.post(`/vm/vms/${id}/stop`);
export const getProviders = () => api.get('/vm/providers');

// Node API requests
export const getNodes = () => api.get('/node/nodes');
export const createNode = (nodeData) => api.post('/node/nodes', nodeData);
export const getNode = (id) => api.get(`/node/nodes/${id}`);
export const updateNode = (id, nodeData) => api.put(`/node/nodes/${id}`, nodeData);
export const deleteNode = (id) => api.delete(`/node/nodes/${id}`);
export const startNode = (id) => api.post(`/node/nodes/${id}/start`);
export const stopNode = (id) => api.post(`/node/nodes/${id}/stop`);

// Data API requests
export const getRewards = () => api.get('/data/rewards');
export const getNodeRewards = (nodeId) => api.get(`/data/rewards/node/${nodeId}`);
export const createReward = (rewardData) => api.post('/data/rewards', rewardData);
export const simulateRewards = (nodeId, days) => api.post(`/data/rewards/simulate/${nodeId}`, { days });
export const getRewardStats = () => api.get('/data/rewards/stats');

// Referral API requests
export const getReferrals = () => api.get('/referral/referrals');
export const getNodeReferrals = (nodeId) => api.get(`/referral/referrals/node/${nodeId}`);
export const createReferral = (referralData) => api.post('/referral/referrals', referralData);
export const deleteReferral = (id) => api.delete(`/referral/referrals/${id}`);
export const getReferralStats = () => api.get('/referral/referrals/stats');

export default api;
