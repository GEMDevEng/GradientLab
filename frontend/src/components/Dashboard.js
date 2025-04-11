import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    vms: 0,
    nodes: 0,
    totalPoints: 0,
    averagePointsPerNode: 0
  });

  // Mock data for development (will be replaced with actual API calls)
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setStats({
        vms: 4,
        nodes: 6,
        totalPoints: 1250,
        averagePointsPerNode: 208.33
      });
    }, 1000);
  }, []);

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats-container">
        <div className="stat-card">
          <h3>VMs</h3>
          <p className="stat-value">{stats.vms}</p>
        </div>
        <div className="stat-card">
          <h3>Nodes</h3>
          <p className="stat-value">{stats.nodes}</p>
        </div>
        <div className="stat-card">
          <h3>Total Points</h3>
          <p className="stat-value">{stats.totalPoints}</p>
        </div>
        <div className="stat-card">
          <h3>Avg. Points/Node</h3>
          <p className="stat-value">{stats.averagePointsPerNode.toFixed(2)}</p>
        </div>
      </div>
      <div className="dashboard-section">
        <h3>Recent Activity</h3>
        <p>No recent activity to display.</p>
      </div>
    </div>
  );
};

export default Dashboard;
