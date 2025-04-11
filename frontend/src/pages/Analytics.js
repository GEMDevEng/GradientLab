import React, { useState } from 'react';
import AdvancedCharts from '../components/AdvancedCharts';
import NodeTable from '../components/NodeTable';
import PredictiveAnalytics from '../components/PredictiveAnalytics';
import './Analytics.css';

const Analytics = () => {
  const [activeTab, setActiveTab] = useState('trends');

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="analytics-container">
      <h2>Analytics Dashboard</h2>

      <div className="analytics-tabs">
        <button
          className={`tab-button ${activeTab === 'trends' ? 'active' : ''}`}
          onClick={() => handleTabChange('trends')}
        >
          Reward Trends
        </button>
        <button
          className={`tab-button ${activeTab === 'predictions' ? 'active' : ''}`}
          onClick={() => handleTabChange('predictions')}
        >
          Predictive Analytics
        </button>
        <button
          className={`tab-button ${activeTab === 'nodes' ? 'active' : ''}`}
          onClick={() => handleTabChange('nodes')}
        >
          Node Performance
        </button>
      </div>

      {activeTab === 'trends' && (
        <div className="analytics-section">
          <h3>Reward Trends</h3>
          <AdvancedCharts />
        </div>
      )}

      {activeTab === 'predictions' && (
        <div className="analytics-section">
          <h3>Predictive Analytics</h3>
          <PredictiveAnalytics />
        </div>
      )}

      {activeTab === 'nodes' && (
        <div className="analytics-section">
          <h3>Node Performance</h3>
          <NodeTable />
        </div>
      )}
    </div>
  );
};

export default Analytics;
