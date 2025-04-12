import React, { useState, useEffect } from 'react';
import { setup2FA, verify2FA, disable2FA, get2FAStatus } from '../api/twoFactor';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import { useToast } from '../contexts/ToastContext';
import './TwoFactorSetup.css';

const TwoFactorSetup = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState({
    enabled: false,
    verified: false,
    hasBackupCodes: false
  });
  const [setupData, setSetupData] = useState(null);
  const [verificationCode, setVerificationCode] = useState('');
  const [backupCodes, setBackupCodes] = useState([]);
  const [disableCode, setDisableCode] = useState('');
  const [step, setStep] = useState('status');
  const toast = useToast();

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await get2FAStatus();
      setStatus(response.data);
      setStep(response.data.enabled ? 'enabled' : 'status');
    } catch (err) {
      setError(err.message || 'Failed to fetch 2FA status');
    } finally {
      setLoading(false);
    }
  };

  const handleSetup = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await setup2FA();
      setSetupData(response.data);
      setStep('setup');
    } catch (err) {
      setError(err.message || 'Failed to setup 2FA');
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async (e) => {
    e.preventDefault();
    
    if (!verificationCode) {
      setError('Please enter the verification code');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await verify2FA(verificationCode);
      setBackupCodes(response.data.backup_codes);
      setStep('backup_codes');
      toast.success('Two-factor authentication enabled successfully');
    } catch (err) {
      setError(err.message || 'Failed to verify code');
    } finally {
      setLoading(false);
    }
  };

  const handleDisable = async (e) => {
    e.preventDefault();
    
    if (!disableCode) {
      setError('Please enter the verification code');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      await disable2FA(disableCode);
      setStatus({
        enabled: false,
        verified: false,
        hasBackupCodes: false
      });
      setStep('status');
      toast.success('Two-factor authentication disabled successfully');
    } catch (err) {
      setError(err.message || 'Failed to disable 2FA');
    } finally {
      setLoading(false);
    }
  };

  const renderStatus = () => (
    <div className="tfa-status">
      <h3>Two-Factor Authentication</h3>
      <p>
        Two-factor authentication adds an extra layer of security to your account.
        When enabled, you'll need to provide a verification code from your
        authenticator app in addition to your password when signing in.
      </p>
      
      <div className="status-indicator">
        <span className={`status-badge ${status.enabled ? 'enabled' : 'disabled'}`}>
          {status.enabled ? 'Enabled' : 'Disabled'}
        </span>
      </div>
      
      {!status.enabled ? (
        <button 
          className="tfa-button setup"
          onClick={handleSetup}
          disabled={loading}
        >
          Enable Two-Factor Authentication
        </button>
      ) : (
        <button 
          className="tfa-button disable"
          onClick={() => setStep('disable')}
        >
          Disable Two-Factor Authentication
        </button>
      )}
    </div>
  );

  const renderSetup = () => (
    <div className="tfa-setup">
      <h3>Set Up Two-Factor Authentication</h3>
      
      <div className="setup-steps">
        <div className="setup-step">
          <div className="step-number">1</div>
          <div className="step-content">
            <h4>Install an authenticator app</h4>
            <p>
              Download and install an authenticator app on your mobile device.
              We recommend Google Authenticator, Authy, or Microsoft Authenticator.
            </p>
          </div>
        </div>
        
        <div className="setup-step">
          <div className="step-number">2</div>
          <div className="step-content">
            <h4>Scan the QR code</h4>
            <p>
              Open your authenticator app and scan the QR code below.
              Alternatively, you can manually enter the secret key.
            </p>
            
            <div className="qr-container">
              <img 
                src={`/api/2fa/qrcode?t=${new Date().getTime()}`} 
                alt="QR Code" 
                className="qr-code"
              />
            </div>
            
            <div className="secret-key">
              <p>Secret key: <code>{setupData?.secret}</code></p>
            </div>
          </div>
        </div>
        
        <div className="setup-step">
          <div className="step-number">3</div>
          <div className="step-content">
            <h4>Enter verification code</h4>
            <p>
              Enter the 6-digit verification code from your authenticator app.
            </p>
            
            <form onSubmit={handleVerify} className="verification-form">
              <div className="form-group">
                <input
                  type="text"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').substring(0, 6))}
                  placeholder="Enter 6-digit code"
                  maxLength="6"
                  pattern="[0-9]{6}"
                  required
                />
              </div>
              
              <div className="form-actions">
                <button 
                  type="button" 
                  className="tfa-button cancel"
                  onClick={() => setStep('status')}
                  disabled={loading}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="tfa-button verify"
                  disabled={loading || verificationCode.length !== 6}
                >
                  {loading ? 'Verifying...' : 'Verify'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );

  const renderBackupCodes = () => (
    <div className="tfa-backup-codes">
      <h3>Backup Codes</h3>
      <p>
        Save these backup codes in a secure location. Each code can only be used once
        to sign in if you don't have access to your authenticator app.
      </p>
      
      <div className="backup-codes-container">
        <div className="backup-codes-grid">
          {backupCodes.map((code, index) => (
            <div key={index} className="backup-code">
              {code}
            </div>
          ))}
        </div>
      </div>
      
      <div className="backup-codes-actions">
        <button 
          className="tfa-button done"
          onClick={() => {
            setStep('enabled');
            fetchStatus();
          }}
        >
          I've saved these codes
        </button>
      </div>
    </div>
  );

  const renderDisable = () => (
    <div className="tfa-disable">
      <h3>Disable Two-Factor Authentication</h3>
      <p>
        To disable two-factor authentication, please enter a verification code
        from your authenticator app or one of your backup codes.
      </p>
      
      <form onSubmit={handleDisable} className="disable-form">
        <div className="form-group">
          <input
            type="text"
            value={disableCode}
            onChange={(e) => setDisableCode(e.target.value)}
            placeholder="Enter verification code"
            required
          />
        </div>
        
        <div className="form-actions">
          <button 
            type="button" 
            className="tfa-button cancel"
            onClick={() => setStep('enabled')}
            disabled={loading}
          >
            Cancel
          </button>
          <button 
            type="submit" 
            className="tfa-button disable"
            disabled={loading || !disableCode}
          >
            {loading ? 'Disabling...' : 'Disable 2FA'}
          </button>
        </div>
      </form>
    </div>
  );

  if (loading && step === 'status') {
    return <LoadingSpinner text="Loading two-factor authentication status..." />;
  }

  return (
    <div className="two-factor-setup">
      {error && (
        <ErrorMessage 
          message="Two-Factor Authentication Error" 
          details={error} 
          type="error" 
          onRetry={() => fetchStatus()}
        />
      )}
      
      {step === 'status' && renderStatus()}
      {step === 'setup' && renderSetup()}
      {step === 'backup_codes' && renderBackupCodes()}
      {step === 'enabled' && renderStatus()}
      {step === 'disable' && renderDisable()}
    </div>
  );
};

export default TwoFactorSetup;
