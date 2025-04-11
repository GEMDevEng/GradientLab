import React from 'react';
import './ErrorMessage.css';

const ErrorMessage = ({ 
  message = 'An error occurred', 
  details = null, 
  onRetry = null,
  type = 'error' // 'error', 'warning', 'info'
}) => {
  return (
    <div className={`error-container error-${type}`}>
      <div className="error-icon">
        {type === 'error' && <span>❌</span>}
        {type === 'warning' && <span>⚠️</span>}
        {type === 'info' && <span>ℹ️</span>}
      </div>
      <div className="error-content">
        <h3 className="error-title">{message}</h3>
        {details && <p className="error-details">{details}</p>}
        {onRetry && (
          <button className="error-retry-button" onClick={onRetry}>
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;
