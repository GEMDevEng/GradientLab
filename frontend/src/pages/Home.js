import React, { useState, useEffect } from 'react';
import Dashboard from '../components/Dashboard';
import VmTable from '../components/VmTable';
import Charts from '../components/Charts';
import RealtimeStatus from '../components/RealtimeStatus';
import MobileDashboard from '../components/MobileDashboard';
import './Home.css';

const Home = () => {
  const [dashboardStats, setDashboardStats] = useState({
    totalVMs: 0,
    totalNodes: 0,
    totalPoints: 0,
    uptime: '0%',
    vms: [],
    nodes: [],
    rewards: []
  });

  // Fetch dashboard data
  useEffect(() => {
    // This would normally be an API call
    // For now, we'll use mock data
    const mockData = {
      totalVMs: 3,
      totalNodes: 5,
      totalPoints: 1250,
      uptime: '98.7%',
      vms: [
        { id: 1, name: 'VM-1', status: 'running', provider: 'AWS', region: 'us-east-1', ip_address: '192.168.1.1' },
        { id: 2, name: 'VM-2', status: 'stopped', provider: 'GCP', region: 'us-central1', ip_address: '192.168.1.2' },
        { id: 3, name: 'VM-3', status: 'provisioning', provider: 'Azure', region: 'eastus', ip_address: null }
      ],
      nodes: [
        { id: 1, name: 'Node-1', status: 'active', uptime_percentage: 99.8, vm_name: 'VM-1' },
        { id: 2, name: 'Node-2', status: 'active', uptime_percentage: 97.5, vm_name: 'VM-1' },
        { id: 3, name: 'Node-3', status: 'inactive', uptime_percentage: 0, vm_name: 'VM-2' },
        { id: 4, name: 'Node-4', status: 'active', uptime_percentage: 99.2, vm_name: 'VM-1' },
        { id: 5, name: 'Node-5', status: 'deploying', uptime_percentage: 0, vm_name: 'VM-3' }
      ],
      rewards: [
        { date: '2023-05-01', total_points: 150, poa_points: 100, poc_points: 50, referral_points: 0 },
        { date: '2023-05-02', total_points: 175, poa_points: 100, poc_points: 75, referral_points: 0 },
        { date: '2023-05-03', total_points: 200, poa_points: 100, poc_points: 75, referral_points: 25 }
      ]
    };

    setDashboardStats(mockData);
  }, []);

  return (
    <div className="home-container">
      {/* Desktop Dashboard */}
      <div className="desktop-dashboard">
        <Dashboard />
        <div className="home-layout">
          <div className="home-main">
            <div className="home-section">
              <VmTable />
            </div>
            <div className="home-section">
              <Charts />
            </div>
          </div>
          <div className="home-sidebar">
            <RealtimeStatus />
          </div>
        </div>
      </div>

      {/* Mobile Dashboard */}
      <MobileDashboard stats={dashboardStats} />
    </div>
  );
};

export default Home;
