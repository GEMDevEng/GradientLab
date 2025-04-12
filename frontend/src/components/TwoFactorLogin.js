import React, { useState } from 'react';
import { login } from '../api/auth';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import './TwoFactorLogin.css';

const TwoFactorLogin = ({ username, onSuccess, onCancel }) => {
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!code) {
      setError('Please enter the verification code');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      // Call login API with username, password, and OTP code
      const result = await login(username, null, code);
      
      if (onSuccess) {
        onSuccess(result);
      }
    } catch (err) {
      setError(err.message || 'Invalid verification code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="two-factor-login">
      <h2>Two-Factor Authentication</h2>
      <p className="login-subtitle">
        Enter the verification code from your authenticator app
      </p>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="tfa-form">
        <div className="form-group">
          <label htmlFor="code">Verification Code</label>
          <input
            type="text"
            id="code"
            name="code"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, '').substring(0, 6))}
            placeholder="Enter 6-digit code"
            maxLength="6"
            pattern="[0-9]{6}"
            autoFocus
            required
          />
          <div className="code-hint">
            You can also use a backup code
          </div>
        </div>
        
        <div className="form-actions">
          <button 
            type="button" 
            className="cancel-button"
            onClick={onCancel}
            disabled={loading}
          >
            Back
          </button>
          <button 
            type="submit" 
            className="submit-button"
            disabled={loading || code.length < 6}
          >
            {loading ? (
              <>
                <span className="spinner-icon"></span>
                Verifying...
              </>
            ) : (
              'Verify'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TwoFactorLogin;
