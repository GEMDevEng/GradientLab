import React, { useState, useEffect } from 'react';
import './NodeTable.css';

const NodeTable = () => {
  const [nodes, setNodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('uptime');
  const [sortDirection, setSortDirection] = useState('desc');

  // Mock data for development (will be replaced with actual API calls)
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockNodes = [
        {
          id: 1,
          name: 'oracle-node-1',
          vm_id: 1,
          vm_name: 'oracle-vm-1',
          provider: 'oracle',
          region: 'us-west-1',
          status: 'good',
          uptime_percentage: 99.8,
          poa_points: 450,
          poc_points: 320,
          referral_points: 100,
          created_at: '2023-04-10T12:30:00Z'
        },
        {
          id: 2,
          name: 'oracle-node-2',
          vm_id: 2,
          vm_name: 'oracle-vm-2',
          provider: 'oracle',
          region: 'us-east-1',
          status: 'disconnected',
          uptime_percentage: 45.2,
          poa_points: 120,
          poc_points: 80,
          referral_points: 0,
          created_at: '2023-04-11T14:45:00Z'
        },
        {
          id: 3,
          name: 'google-node-1',
          vm_id: 3,
          vm_name: 'google-vm-1',
          provider: 'google',
          region: 'us-central1',
          status: 'good',
          uptime_percentage: 98.5,
          poa_points: 430,
          poc_points: 310,
          referral_points: 50,
          created_at: '2023-04-12T09:15:00Z'
        },
        {
          id: 4,
          name: 'azure-node-1',
          vm_id: 4,
          vm_name: 'azure-vm-1',
          provider: 'azure',
          region: 'eastus',
          status: 'unsupported',
          uptime_percentage: 72.3,
          poa_points: 250,
          poc_points: 180,
          referral_points: 0,
          created_at: '2023-04-13T16:45:00Z'
        },
        {
          id: 5,
          name: 'oracle-node-3',
          vm_id: 5,
          vm_name: 'oracle-vm-3',
          provider: 'oracle',
          region: 'eu-frankfurt-1',
          status: 'good',
          uptime_percentage: 97.9,
          poa_points: 420,
          poc_points: 300,
          referral_points: 75,
          created_at: '2023-04-14T11:30:00Z'
        },
        {
          id: 6,
          name: 'google-node-2',
          vm_id: 6,
          vm_name: 'google-vm-2',
          provider: 'google',
          region: 'europe-west1',
          status: 'good',
          uptime_percentage: 96.2,
          poa_points: 410,
          poc_points: 290,
          referral_points: 25,
          created_at: '2023-04-15T13:20:00Z'
        }
      ];
      
      setNodes(mockNodes);
      setLoading(false);
    }, 1000);
  }, []);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      // Toggle sort direction if clicking the same column
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Set new sort column and default to descending
      setSortBy(column);
      setSortDirection('desc');
    }
  };

  const filteredNodes = nodes.filter(node => {
    if (filter === 'all') return true;
    return node.status === filter;
  });

  const sortedNodes = [...filteredNodes].sort((a, b) => {
    let comparison = 0;
    
    switch (sortBy) {
      case 'name':
        comparison = a.name.localeCompare(b.name);
        break;
      case 'provider':
        comparison = a.provider.localeCompare(b.provider);
        break;
      case 'region':
        comparison = a.region.localeCompare(b.region);
        break;
      case 'status':
        comparison = a.status.localeCompare(b.status);
        break;
      case 'uptime':
        comparison = a.uptime_percentage - b.uptime_percentage;
        break;
      case 'poa':
        comparison = a.poa_points - b.poa_points;
        break;
      case 'poc':
        comparison = a.poc_points - b.poc_points;
        break;
      case 'referral':
        comparison = a.referral_points - b.referral_points;
        break;
      case 'total':
        comparison = (a.poa_points + a.poc_points + a.referral_points) - 
                     (b.poa_points + b.poc_points + b.referral_points);
        break;
      case 'created':
        comparison = new Date(a.created_at) - new Date(b.created_at);
        break;
      default:
        comparison = 0;
    }
    
    return sortDirection === 'asc' ? comparison : -comparison;
  });

  const getSortIndicator = (column) => {
    if (sortBy !== column) return null;
    return sortDirection === 'asc' ? '↑' : '↓';
  };

  const handleRestartNode = (id) => {
    console.log(`Restarting node with ID: ${id}`);
    // Update node status in the state
    setNodes(nodes.map(node => 
      node.id === id ? { ...node, status: 'good' } : node
    ));
  };

  const handleDeleteNode = (id) => {
    console.log(`Deleting node with ID: ${id}`);
    // Remove node from the state
    setNodes(nodes.filter(node => node.id !== id));
  };

  if (loading) {
    return <div className="loading">Loading nodes...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="node-table-container">
      <div className="table-header">
        <h2>Sentry Nodes</h2>
        <div className="table-controls">
          <div className="filter-control">
            <label htmlFor="statusFilter">Filter by Status:</label>
            <select 
              id="statusFilter" 
              value={filter} 
              onChange={handleFilterChange}
            >
              <option value="all">All Statuses</option>
              <option value="good">Good</option>
              <option value="disconnected">Disconnected</option>
              <option value="unsupported">Unsupported</option>
            </select>
          </div>
          <button className="create-button">Deploy New Node</button>
        </div>
      </div>
      
      {sortedNodes.length === 0 ? (
        <p>No nodes found matching the selected filter.</p>
      ) : (
        <div className="table-responsive">
          <table className="node-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('name')}>
                  Node Name {getSortIndicator('name')}
                </th>
                <th onClick={() => handleSort('provider')}>
                  Provider {getSortIndicator('provider')}
                </th>
                <th onClick={() => handleSort('region')}>
                  Region {getSortIndicator('region')}
                </th>
                <th onClick={() => handleSort('status')}>
                  Status {getSortIndicator('status')}
                </th>
                <th onClick={() => handleSort('uptime')}>
                  Uptime % {getSortIndicator('uptime')}
                </th>
                <th onClick={() => handleSort('poa')}>
                  POA Points {getSortIndicator('poa')}
                </th>
                <th onClick={() => handleSort('poc')}>
                  POC Points {getSortIndicator('poc')}
                </th>
                <th onClick={() => handleSort('referral')}>
                  Referral Points {getSortIndicator('referral')}
                </th>
                <th onClick={() => handleSort('total')}>
                  Total Points {getSortIndicator('total')}
                </th>
                <th onClick={() => handleSort('created')}>
                  Created {getSortIndicator('created')}
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedNodes.map(node => (
                <tr key={node.id}>
                  <td>{node.name}</td>
                  <td>{node.provider}</td>
                  <td>{node.region}</td>
                  <td>
                    <span className={`status-badge status-${node.status}`}>
                      {node.status}
                    </span>
                  </td>
                  <td>
                    <div className="uptime-bar">
                      <div 
                        className="uptime-fill" 
                        style={{ width: `${node.uptime_percentage}%` }}
                      ></div>
                      <span className="uptime-text">{node.uptime_percentage.toFixed(1)}%</span>
                    </div>
                  </td>
                  <td>{node.poa_points}</td>
                  <td>{node.poc_points}</td>
                  <td>{node.referral_points}</td>
                  <td>{node.poa_points + node.poc_points + node.referral_points}</td>
                  <td>{new Date(node.created_at).toLocaleDateString()}</td>
                  <td className="actions">
                    {node.status === 'disconnected' && (
                      <button 
                        className="action-button restart"
                        onClick={() => handleRestartNode(node.id)}
                      >
                        Restart
                      </button>
                    )}
                    <button 
                      className="action-button delete"
                      onClick={() => handleDeleteNode(node.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      <div className="node-stats">
        <div className="stat-item">
          <span className="stat-label">Total Nodes:</span>
          <span className="stat-value">{filteredNodes.length}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Good Nodes:</span>
          <span className="stat-value">{filteredNodes.filter(node => node.status === 'good').length}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Average Uptime:</span>
          <span className="stat-value">
            {(filteredNodes.reduce((sum, node) => sum + node.uptime_percentage, 0) / filteredNodes.length).toFixed(1)}%
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Total Points:</span>
          <span className="stat-value">
            {filteredNodes.reduce((sum, node) => sum + node.poa_points + node.poc_points + node.referral_points, 0)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default NodeTable;
