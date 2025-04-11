import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import './Login.css';

// Import components
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

// Import utilities
import { isValidUsername } from '../utils/validation';
import { useToast } from '../contexts/ToastContext';
import { login } from '../api/auth';

const Login = ({ setAuthenticated }) => {
  const history = useHistory();
  const toast = useToast();

  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [loginError, setLoginError] = useState(null);

  const validateForm = () => {
    const newErrors = {};

    // Validate username
    if (!credentials.username) {
      newErrors.username = 'Username is required';
    } else if (!isValidUsername(credentials.username)) {
      newErrors.username = 'Invalid username format';
    }

    // Validate password
    if (!credentials.password) {
      newErrors.password = 'Password is required';
    } else if (credentials.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials({
      ...credentials,
      [name]: value
    });

    // Clear error for this field when user types
    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: ''
      });
    }

    // Clear login error when user changes input
    if (loginError) {
      setLoginError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setLoginError(null);

    try {
      // Call login API
      const response = await login(credentials.username, credentials.password);

      // Set authenticated state
      setAuthenticated(true);

      // Show success toast
      toast.success('Login successful');

      // Redirect to home page
      history.push('/');
    } catch (error) {
      console.error('Login error:', error);
      setLoginError(error.message || 'Invalid username or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>GradientLab</h2>
        <p className="login-subtitle">Sign in to your account</p>

        {loginError && (
          <ErrorMessage
            message="Login Failed"
            details={loginError}
            type="error"
          />
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className={`form-group ${errors.username ? 'has-error' : ''}`}>
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={credentials.username}
              onChange={handleChange}
              placeholder="Enter your username"
              disabled={isLoading}
            />
            {errors.username && <div className="field-error">{errors.username}</div>}
          </div>

          <div className={`form-group ${errors.password ? 'has-error' : ''}`}>
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={credentials.password}
              onChange={handleChange}
              placeholder="Enter your password"
              disabled={isLoading}
            />
            {errors.password && <div className="field-error">{errors.password}</div>}
          </div>

          <button
            type="submit"
            className="login-button"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner-icon"></span>
                Signing In...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>

        <div className="login-footer">
          <p>Don't have an account? Contact your administrator.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
