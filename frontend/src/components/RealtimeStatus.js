import React from 'react';
import { useSocket } from '../contexts/SocketContext';
import './RealtimeStatus.css';

const RealtimeStatus = () => {
  const { connected, authenticated, rewardUpdates } = useSocket();
  
  return (
    <div className="realtime-status">
      <div className="status-header">
        <h3>Real-Time Status</h3>
        <div className={`connection-indicator ${connected ? 'connected' : 'disconnected'}`}>
          {connected ? 'Connected' : 'Disconnected'}
        </div>
      </div>
      
      {connected && !authenticated && (
        <div className="auth-status warning">
          <span className="status-icon">⚠️</span>
          <span>Not authenticated for real-time updates</span>
        </div>
      )}
      
      {connected && authenticated && (
        <div className="realtime-content">
          <div className="recent-rewards">
            <h4>Recent Rewards</h4>
            {rewardUpdates.length === 0 ? (
              <p className="no-data">No recent rewards</p>
            ) : (
              <ul className="rewards-list">
                {rewardUpdates.map((reward, index) => (
                  <li key={index} className="reward-item">
                    <div className="reward-time">
                      {new Date(reward.timestamp).toLocaleTimeString()}
                    </div>
                    <div className="reward-details">
                      <span className="reward-total">+{reward.total_points} points</span>
                      <div className="reward-breakdown">
                        <span className="poa">POA: {reward.poa_points}</span>
                        <span className="poc">POC: {reward.poc_points}</span>
                        <span className="referral">Ref: {reward.referral_points}</span>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
      
      {!connected && (
        <div className="connection-message">
          <p>Real-time updates are currently unavailable.</p>
          <p>Please check your connection and refresh the page.</p>
        </div>
      )}
    </div>
  );
};

export default RealtimeStatus;
