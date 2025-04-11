import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './Charts.css';

const Charts = () => {
  const [rewardData, setRewardData] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock data for development (will be replaced with actual API calls)
  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const mockData = [
        {
          date: '2023-04-07',
          poa: 25,
          poc: 15,
          referral: 5
        },
        {
          date: '2023-04-08',
          poa: 30,
          poc: 18,
          referral: 8
        },
        {
          date: '2023-04-09',
          poa: 28,
          poc: 20,
          referral: 10
        },
        {
          date: '2023-04-10',
          poa: 35,
          poc: 22,
          referral: 12
        },
        {
          date: '2023-04-11',
          poa: 40,
          poc: 25,
          referral: 15
        },
        {
          date: '2023-04-12',
          poa: 45,
          poc: 30,
          referral: 20
        },
        {
          date: '2023-04-13',
          poa: 50,
          poc: 35,
          referral: 25
        }
      ];
      
      setRewardData(mockData);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <div className="loading">Loading charts...</div>;
  }

  return (
    <div className="charts-container">
      <h2>Reward Trends</h2>
      <div className="chart">
        <h3>Daily Rewards</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={rewardData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="poa" name="POA Points" fill="#8884d8" />
            <Bar dataKey="poc" name="POC Points" fill="#82ca9d" />
            <Bar dataKey="referral" name="Referral Points" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      <div className="chart-summary">
        <div className="summary-card">
          <h4>Total POA Points</h4>
          <p className="summary-value">{rewardData.reduce((sum, day) => sum + day.poa, 0)}</p>
        </div>
        <div className="summary-card">
          <h4>Total POC Points</h4>
          <p className="summary-value">{rewardData.reduce((sum, day) => sum + day.poc, 0)}</p>
        </div>
        <div className="summary-card">
          <h4>Total Referral Points</h4>
          <p className="summary-value">{rewardData.reduce((sum, day) => sum + day.referral, 0)}</p>
        </div>
        <div className="summary-card">
          <h4>Grand Total</h4>
          <p className="summary-value">
            {rewardData.reduce((sum, day) => sum + day.poa + day.poc + day.referral, 0)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default Charts;
