import React from 'react';
import Dashboard from '../components/Dashboard';
import VmTable from '../components/VmTable';
import Charts from '../components/Charts';
import RealtimeStatus from '../components/RealtimeStatus';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
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
  );
};

export default Home;
