import React from 'react';
import AdvancedCharts from '../components/AdvancedCharts';
import NodeTable from '../components/NodeTable';
import './Analytics.css';

const Analytics = () => {
  return (
    <div className="analytics-container">
      <h2>Analytics Dashboard</h2>
      
      <div className="analytics-section">
        <h3>Reward Trends</h3>
        <AdvancedCharts />
      </div>
      
      <div className="analytics-section">
        <h3>Node Performance</h3>
        <NodeTable />
      </div>
    </div>
  );
};

export default Analytics;
