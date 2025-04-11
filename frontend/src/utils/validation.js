/**
 * Form validation utilities
 */

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} - True if email is valid
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email);
};

/**
 * Validate username format
 * @param {string} username - Username to validate
 * @returns {boolean} - True if username is valid
 */
export const isValidUsername = (username) => {
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
  return usernameRegex.test(username);
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} - Validation result with isValid and message
 */
export const validatePassword = (password) => {
  if (!password || password.length < 8) {
    return {
      isValid: false,
      message: 'Password must be at least 8 characters long'
    };
  }
  
  if (!/[A-Z]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one uppercase letter'
    };
  }
  
  if (!/[a-z]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one lowercase letter'
    };
  }
  
  if (!/[0-9]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one digit'
    };
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    return {
      isValid: false,
      message: 'Password must contain at least one special character'
    };
  }
  
  return {
    isValid: true,
    message: 'Password is strong'
  };
};

/**
 * Calculate password strength score (0-100)
 * @param {string} password - Password to evaluate
 * @returns {number} - Strength score from 0 to 100
 */
export const getPasswordStrength = (password) => {
  if (!password) return 0;
  
  let score = 0;
  
  // Length
  if (password.length >= 8) score += 20;
  if (password.length >= 12) score += 10;
  
  // Complexity
  if (/[A-Z]/.test(password)) score += 15;
  if (/[a-z]/.test(password)) score += 15;
  if (/[0-9]/.test(password)) score += 15;
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 15;
  
  // Variety
  const uniqueChars = new Set(password).size;
  score += Math.min(10, uniqueChars / password.length * 10);
  
  return Math.min(100, score);
};

/**
 * Validate form fields
 * @param {Object} fields - Form fields to validate
 * @param {Object} validations - Validation rules for each field
 * @returns {Object} - Validation errors for each field
 */
export const validateForm = (fields, validations) => {
  const errors = {};
  
  Object.keys(validations).forEach(fieldName => {
    const value = fields[fieldName];
    const validation = validations[fieldName];
    
    if (validation.required && (!value || value.trim() === '')) {
      errors[fieldName] = `${validation.label || fieldName} is required`;
    } else if (value && validation.minLength && value.length < validation.minLength) {
      errors[fieldName] = `${validation.label || fieldName} must be at least ${validation.minLength} characters`;
    } else if (value && validation.maxLength && value.length > validation.maxLength) {
      errors[fieldName] = `${validation.label || fieldName} must be less than ${validation.maxLength} characters`;
    } else if (value && validation.pattern && !validation.pattern.test(value)) {
      errors[fieldName] = validation.message || `${validation.label || fieldName} is invalid`;
    } else if (value && validation.custom) {
      const customError = validation.custom(value, fields);
      if (customError) {
        errors[fieldName] = customError;
      }
    }
  });
  
  return errors;
};
