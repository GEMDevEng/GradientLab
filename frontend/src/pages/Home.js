import React from 'react';
import Dashboard from '../components/Dashboard';
import VmTable from '../components/VmTable';
import Charts from '../components/Charts';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <Dashboard />
      <div className="home-section">
        <VmTable />
      </div>
      <div className="home-section">
        <Charts />
      </div>
    </div>
  );
};

export default Home;
