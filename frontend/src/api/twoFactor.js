import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const TFA_URL = `${API_URL}/2fa`;

// Create axios instance with auth headers
const tfaApi = axios.create({
  baseURL: TFA_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add interceptor to include auth token in requests
tfaApi.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

/**
 * Get two-factor authentication status
 * @returns {Promise} - Promise with 2FA status
 */
export const get2FAStatus = async () => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return {
        data: {
          enabled: false,
          verified: false,
          hasBackupCodes: false
        }
      };
    }
    
    const response = await tfaApi.get('/status');
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to get 2FA status');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Set up two-factor authentication
 * @returns {Promise} - Promise with setup data
 */
export const setup2FA = async () => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return {
        data: {
          secret: 'ABCDEFGHIJKLMNOP',
          uri: 'otpauth://totp/GradientLab:user@example.com?secret=ABCDEFGHIJKLMNOP&issuer=GradientLab'
        }
      };
    }
    
    const response = await tfaApi.post('/setup');
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to set up 2FA');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Verify two-factor authentication code
 * @param {string} code - Verification code
 * @returns {Promise} - Promise with verification result
 */
export const verify2FA = async (code) => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return {
        data: {
          backup_codes: [
            'ABCDE12345',
            'FGHIJ67890',
            'KLMNO12345',
            'PQRST67890',
            'UVWXY12345',
            'ZABCD67890',
            'EFGHI12345',
            'JKLMN67890'
          ]
        }
      };
    }
    
    const response = await tfaApi.post('/verify', { code });
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to verify 2FA code');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Disable two-factor authentication
 * @param {string} code - Verification code
 * @returns {Promise} - Promise with disable result
 */
export const disable2FA = async (code) => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return { success: true };
    }
    
    const response = await tfaApi.post('/disable', { code });
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to disable 2FA');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Get backup codes
 * @returns {Promise} - Promise with backup codes
 */
export const getBackupCodes = async () => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return {
        data: {
          backup_codes: [
            'ABCDE12345',
            'FGHIJ67890',
            'KLMNO12345',
            'PQRST67890',
            'UVWXY12345',
            'ZABCD67890',
            'EFGHI12345',
            'JKLMN67890'
          ]
        }
      };
    }
    
    const response = await tfaApi.get('/backup-codes');
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to get backup codes');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Regenerate backup codes
 * @param {string} code - Verification code
 * @returns {Promise} - Promise with new backup codes
 */
export const regenerateBackupCodes = async (code) => {
  try {
    // For development/testing with mock auth
    if (process.env.REACT_APP_USE_MOCK_AUTH === 'true') {
      return {
        data: {
          backup_codes: [
            'NEWAB12345',
            'NEWCD67890',
            'NEWEF12345',
            'NEWGH67890',
            'NEWIJ12345',
            'NEWKL67890',
            'NEWMN12345',
            'NEWOP67890'
          ]
        }
      };
    }
    
    const response = await tfaApi.post('/backup-codes/regenerate', { code });
    
    if (response.data.status === 'success') {
      return response.data;
    } else {
      throw new Error(response.data.message || 'Failed to regenerate backup codes');
    }
  } catch (error) {
    handleApiError(error);
  }
};

/**
 * Handle API error
 * @param {Error} error - Error object
 */
const handleApiError = (error) => {
  if (error.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    throw new Error(error.response.data.message || 'API request failed');
  } else if (error.request) {
    // The request was made but no response was received
    throw new Error('No response from server. Please check your connection.');
  } else {
    // Something happened in setting up the request that triggered an Error
    throw error;
  }
};
