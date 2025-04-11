import React, { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    oracleApiKey: '',
    googleApiKey: '',
    azureApiKey: '',
    enableNotifications: true,
    dataRefreshInterval: 5
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Settings saved:', settings);
    // Here you would typically save the settings to an API or localStorage
    alert('Settings saved successfully!');
  };

  return (
    <div className="settings-container">
      <h2>Settings</h2>
      <form onSubmit={handleSubmit} className="settings-form">
        <div className="settings-section">
          <h3>Cloud Provider Credentials</h3>
          <div className="form-group">
            <label htmlFor="oracleApiKey">Oracle Cloud API Key</label>
            <input
              type="password"
              id="oracleApiKey"
              name="oracleApiKey"
              value={settings.oracleApiKey}
              onChange={handleChange}
              placeholder="Enter Oracle Cloud API Key"
            />
          </div>
          <div className="form-group">
            <label htmlFor="googleApiKey">Google Cloud API Key</label>
            <input
              type="password"
              id="googleApiKey"
              name="googleApiKey"
              value={settings.googleApiKey}
              onChange={handleChange}
              placeholder="Enter Google Cloud API Key"
            />
          </div>
          <div className="form-group">
            <label htmlFor="azureApiKey">Microsoft Azure API Key</label>
            <input
              type="password"
              id="azureApiKey"
              name="azureApiKey"
              value={settings.azureApiKey}
              onChange={handleChange}
              placeholder="Enter Microsoft Azure API Key"
            />
          </div>
        </div>

        <div className="settings-section">
          <h3>Application Settings</h3>
          <div className="form-group checkbox">
            <input
              type="checkbox"
              id="enableNotifications"
              name="enableNotifications"
              checked={settings.enableNotifications}
              onChange={handleChange}
            />
            <label htmlFor="enableNotifications">Enable Notifications</label>
          </div>
          <div className="form-group">
            <label htmlFor="dataRefreshInterval">Data Refresh Interval (minutes)</label>
            <input
              type="number"
              id="dataRefreshInterval"
              name="dataRefreshInterval"
              value={settings.dataRefreshInterval}
              onChange={handleChange}
              min="1"
              max="60"
            />
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="save-button">Save Settings</button>
          <button type="button" className="cancel-button">Cancel</button>
        </div>
      </form>
    </div>
  );
};

export default Settings;
