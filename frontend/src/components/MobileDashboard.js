import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './MobileDashboard.css';

const MobileDashboard = ({ stats }) => {
  const [activeTab, setActiveTab] = useState('vms');
  
  return (
    <div className="mobile-dashboard">
      <div className="stats-cards">
        <div className="stat-card">
          <div className="stat-value">{stats.totalVMs || 0}</div>
          <div className="stat-label">VMs</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.totalNodes || 0}</div>
          <div className="stat-label">Nodes</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.totalPoints || 0}</div>
          <div className="stat-label">Points</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.uptime || '0%'}</div>
          <div className="stat-label">Uptime</div>
        </div>
      </div>
      
      <div className="action-buttons">
        <Link to="/vm/new" className="action-button primary">
          <span className="action-icon">+</span>
          New VM
        </Link>
        <Link to="/node/new" className="action-button secondary">
          <span className="action-icon">+</span>
          New Node
        </Link>
      </div>
      
      <div className="mobile-tabs">
        <button 
          className={`tab-button ${activeTab === 'vms' ? 'active' : ''}`}
          onClick={() => setActiveTab('vms')}
        >
          VMs
        </button>
        <button 
          className={`tab-button ${activeTab === 'nodes' ? 'active' : ''}`}
          onClick={() => setActiveTab('nodes')}
        >
          Nodes
        </button>
        <button 
          className={`tab-button ${activeTab === 'rewards' ? 'active' : ''}`}
          onClick={() => setActiveTab('rewards')}
        >
          Rewards
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'vms' && (
          <div className="vms-list">
            {stats.vms && stats.vms.length > 0 ? (
              stats.vms.map(vm => (
                <div key={vm.id} className="list-item">
                  <div className="item-main">
                    <div className="item-name">{vm.name}</div>
                    <div className="item-status" data-status={vm.status}>{vm.status}</div>
                  </div>
                  <div className="item-details">
                    <div className="detail-item">
                      <span className="detail-label">Provider:</span>
                      <span className="detail-value">{vm.provider}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Region:</span>
                      <span className="detail-value">{vm.region}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">IP:</span>
                      <span className="detail-value">{vm.ip_address || 'N/A'}</span>
                    </div>
                  </div>
                  <div className="item-actions">
                    <Link to={`/vm/${vm.id}`} className="item-action">
                      Details
                    </Link>
                    <button className="item-action">
                      {vm.status === 'running' ? 'Stop' : 'Start'}
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <p>No VMs found</p>
                <Link to="/vm/new" className="action-button primary">
                  Create VM
                </Link>
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'nodes' && (
          <div className="nodes-list">
            {stats.nodes && stats.nodes.length > 0 ? (
              stats.nodes.map(node => (
                <div key={node.id} className="list-item">
                  <div className="item-main">
                    <div className="item-name">{node.name}</div>
                    <div className="item-status" data-status={node.status}>{node.status}</div>
                  </div>
                  <div className="item-details">
                    <div className="detail-item">
                      <span className="detail-label">Uptime:</span>
                      <span className="detail-value">{node.uptime_percentage}%</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">VM:</span>
                      <span className="detail-value">{node.vm_name || 'Unknown'}</span>
                    </div>
                  </div>
                  <div className="item-actions">
                    <Link to={`/node/${node.id}`} className="item-action">
                      Details
                    </Link>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <p>No Nodes found</p>
                <Link to="/node/new" className="action-button primary">
                  Create Node
                </Link>
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'rewards' && (
          <div className="rewards-list">
            {stats.rewards && stats.rewards.length > 0 ? (
              stats.rewards.map((reward, index) => (
                <div key={index} className="list-item">
                  <div className="item-main">
                    <div className="item-name">
                      {new Date(reward.date).toLocaleDateString()}
                    </div>
                    <div className="item-points">+{reward.total_points} pts</div>
                  </div>
                  <div className="item-details">
                    <div className="detail-item">
                      <span className="detail-label">POA:</span>
                      <span className="detail-value">{reward.poa_points} pts</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">POC:</span>
                      <span className="detail-value">{reward.poc_points} pts</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Referral:</span>
                      <span className="detail-value">{reward.referral_points} pts</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="empty-state">
                <p>No rewards yet</p>
                <p className="empty-hint">
                  Rewards are earned by running nodes with high uptime
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default MobileDashboard;
