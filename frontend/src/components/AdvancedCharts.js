import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, Cell
} from 'recharts';
import './AdvancedCharts.css';

const AdvancedCharts = () => {
  const [timeRange, setTimeRange] = useState('week');
  const [chartType, setChartType] = useState('line');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [distributionData, setDistributionData] = useState([]);

  useEffect(() => {
    // Fetch data based on time range
    const fetchData = async () => {
      setLoading(true);
      
      // Simulate API call with different data based on time range
      setTimeout(() => {
        let mockData;
        
        if (timeRange === 'day') {
          // Hourly data for the last 24 hours
          mockData = Array.from({ length: 24 }, (_, i) => ({
            time: `${i}:00`,
            poa: Math.floor(Math.random() * 10) + 5,
            poc: Math.floor(Math.random() * 8) + 3,
            referral: Math.floor(Math.random() * 5)
          }));
        } else if (timeRange === 'week') {
          // Daily data for the last 7 days
          const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
          mockData = Array.from({ length: 7 }, (_, i) => ({
            time: days[i],
            poa: Math.floor(Math.random() * 50) + 20,
            poc: Math.floor(Math.random() * 40) + 15,
            referral: Math.floor(Math.random() * 25) + 5
          }));
        } else if (timeRange === 'month') {
          // Weekly data for the last 4 weeks
          mockData = Array.from({ length: 4 }, (_, i) => ({
            time: `Week ${i + 1}`,
            poa: Math.floor(Math.random() * 200) + 100,
            poc: Math.floor(Math.random() * 150) + 80,
            referral: Math.floor(Math.random() * 100) + 30
          }));
        } else {
          // Monthly data for the last 12 months
          const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
          mockData = Array.from({ length: 12 }, (_, i) => ({
            time: months[i],
            poa: Math.floor(Math.random() * 800) + 400,
            poc: Math.floor(Math.random() * 600) + 300,
            referral: Math.floor(Math.random() * 400) + 100
          }));
        }
        
        setData(mockData);
        
        // Generate distribution data
        const totalPoa = mockData.reduce((sum, item) => sum + item.poa, 0);
        const totalPoc = mockData.reduce((sum, item) => sum + item.poc, 0);
        const totalReferral = mockData.reduce((sum, item) => sum + item.referral, 0);
        
        setDistributionData([
          { name: 'POA', value: totalPoa },
          { name: 'POC', value: totalPoc },
          { name: 'Referral', value: totalReferral }
        ]);
        
        setLoading(false);
      }, 1000);
    };
    
    fetchData();
  }, [timeRange]);

  const handleTimeRangeChange = (e) => {
    setTimeRange(e.target.value);
  };

  const handleChartTypeChange = (e) => {
    setChartType(e.target.value);
  };

  const renderChart = () => {
    if (loading) {
      return <div className="loading">Loading chart data...</div>;
    }

    if (chartType === 'line') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="poa" name="POA Points" stroke="#8884d8" activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="poc" name="POC Points" stroke="#82ca9d" />
            <Line type="monotone" dataKey="referral" name="Referral Points" stroke="#ffc658" />
          </LineChart>
        </ResponsiveContainer>
      );
    } else if (chartType === 'bar') {
      return (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="poa" name="POA Points" fill="#8884d8" />
            <Bar dataKey="poc" name="POC Points" fill="#82ca9d" />
            <Bar dataKey="referral" name="Referral Points" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      );
    } else if (chartType === 'pie') {
      const COLORS = ['#8884d8', '#82ca9d', '#ffc658'];
      
      return (
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie
              data={distributionData}
              cx="50%"
              cy="50%"
              labelLine={true}
              outerRadius={150}
              fill="#8884d8"
              dataKey="value"
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            >
              {distributionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value} points`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      );
    }
    
    return null;
  };

  const calculateTotals = () => {
    if (loading || !data.length) return { poa: 0, poc: 0, referral: 0, total: 0 };
    
    const totalPoa = data.reduce((sum, item) => sum + item.poa, 0);
    const totalPoc = data.reduce((sum, item) => sum + item.poc, 0);
    const totalReferral = data.reduce((sum, item) => sum + item.referral, 0);
    
    return {
      poa: totalPoa,
      poc: totalPoc,
      referral: totalReferral,
      total: totalPoa + totalPoc + totalReferral
    };
  };

  const totals = calculateTotals();

  return (
    <div className="advanced-charts">
      <div className="chart-controls">
        <div className="control-group">
          <label htmlFor="timeRange">Time Range:</label>
          <select 
            id="timeRange" 
            value={timeRange} 
            onChange={handleTimeRangeChange}
          >
            <option value="day">Last 24 Hours</option>
            <option value="week">Last 7 Days</option>
            <option value="month">Last 4 Weeks</option>
            <option value="year">Last 12 Months</option>
          </select>
        </div>
        
        <div className="control-group">
          <label htmlFor="chartType">Chart Type:</label>
          <select 
            id="chartType" 
            value={chartType} 
            onChange={handleChartTypeChange}
          >
            <option value="line">Line Chart</option>
            <option value="bar">Bar Chart</option>
            <option value="pie">Pie Chart</option>
          </select>
        </div>
      </div>
      
      <div className="chart-container">
        {renderChart()}
      </div>
      
      <div className="stats-summary">
        <div className="stat-card">
          <h4>Total POA Points</h4>
          <p className="stat-value">{totals.poa}</p>
        </div>
        <div className="stat-card">
          <h4>Total POC Points</h4>
          <p className="stat-value">{totals.poc}</p>
        </div>
        <div className="stat-card">
          <h4>Total Referral Points</h4>
          <p className="stat-value">{totals.referral}</p>
        </div>
        <div className="stat-card total">
          <h4>Grand Total</h4>
          <p className="stat-value">{totals.total}</p>
        </div>
      </div>
      
      <div className="chart-insights">
        <h3>Insights</h3>
        <ul>
          <li>POA points make up {((totals.poa / totals.total) * 100).toFixed(1)}% of total rewards</li>
          <li>POC points make up {((totals.poc / totals.total) * 100).toFixed(1)}% of total rewards</li>
          <li>Referral points make up {((totals.referral / totals.total) * 100).toFixed(1)}% of total rewards</li>
          <li>Average daily points: {(totals.total / data.length).toFixed(1)}</li>
        </ul>
      </div>
    </div>
  );
};

export default AdvancedCharts;
