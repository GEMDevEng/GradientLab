import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, ReferenceLine
} from 'recharts';
import './PredictiveAnalytics.css';

const PredictiveAnalytics = () => {
  const [historicalData, setHistoricalData] = useState([]);
  const [predictedData, setPredictedData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [predictionDays, setPredictionDays] = useState(30);
  const [confidenceInterval, setConfidenceInterval] = useState(0.95);
  const [selectedMetric, setSelectedMetric] = useState('total');

  useEffect(() => {
    // Fetch historical data and generate predictions
    fetchDataAndPredict();
  }, [predictionDays, confidenceInterval, selectedMetric]);

  const fetchDataAndPredict = () => {
    setLoading(true);
    
    // Simulate API call to get historical data
    setTimeout(() => {
      // Generate mock historical data - last 90 days
      const mockHistorical = generateMockHistoricalData(90);
      setHistoricalData(mockHistorical);
      
      // Generate predictions based on historical data
      const mockPredictions = generatePredictions(mockHistorical, predictionDays);
      setPredictedData(mockPredictions);
      
      setLoading(false);
    }, 1000);
  };

  const generateMockHistoricalData = (days) => {
    const data = [];
    const today = new Date();
    
    // Base values and trend factors for different metrics
    const baseValues = {
      poa: 50,
      poc: 30,
      referral: 10,
      total: 90
    };
    
    const trendFactors = {
      poa: 0.8,
      poc: 0.5,
      referral: 0.2,
      total: 1.5
    };
    
    // Generate data for each day
    for (let i = days; i > 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      
      // Add some randomness and trend
      const dayFactor = 1 + (Math.sin(i / 7) * 0.2); // Weekly pattern
      const trendFactor = 1 + ((days - i) / days) * 0.5; // Upward trend over time
      
      const poa = Math.round(baseValues.poa * dayFactor * trendFactor * (1 + (Math.random() * 0.3 - 0.15)));
      const poc = Math.round(baseValues.poc * dayFactor * trendFactor * (1 + (Math.random() * 0.3 - 0.15)));
      const referral = Math.round(baseValues.referral * dayFactor * trendFactor * (1 + (Math.random() * 0.4 - 0.2)));
      const total = poa + poc + referral;
      
      data.push({
        date: date.toISOString().split('T')[0],
        poa,
        poc,
        referral,
        total
      });
    }
    
    return data;
  };

  const generatePredictions = (historicalData, days) => {
    if (!historicalData.length) return [];
    
    const predictions = [];
    const lastDate = new Date(historicalData[historicalData.length - 1].date);
    
    // Simple linear regression for prediction
    // Calculate slope and intercept based on historical data
    const xValues = historicalData.map((_, index) => index);
    const yValues = historicalData.map(item => item[selectedMetric]);
    
    const { slope, intercept } = linearRegression(xValues, yValues);
    
    // Calculate standard error for confidence intervals
    const yPredicted = xValues.map(x => slope * x + intercept);
    const squaredErrors = yValues.map((y, i) => Math.pow(y - yPredicted[i], 2));
    const mse = squaredErrors.reduce((sum, val) => sum + val, 0) / squaredErrors.length;
    const stdError = Math.sqrt(mse);
    
    // Z-score for confidence interval (95% = 1.96)
    const zScore = confidenceInterval === 0.99 ? 2.576 : 
                  confidenceInterval === 0.95 ? 1.96 : 
                  confidenceInterval === 0.90 ? 1.645 : 1.96;
    
    // Generate predictions
    for (let i = 1; i <= days; i++) {
      const date = new Date(lastDate);
      date.setDate(date.getDate() + i);
      
      const x = historicalData.length + i - 1;
      const predictedValue = slope * x + intercept;
      const marginOfError = zScore * stdError * Math.sqrt(1 + (1 / historicalData.length) + 
                           (Math.pow(x - xValues.reduce((sum, val) => sum + val, 0) / xValues.length, 2) / 
                           (xValues.reduce((sum, val) => sum + Math.pow(val - xValues.reduce((sum, val) => sum + val, 0) / xValues.length, 2), 0))));
      
      predictions.push({
        date: date.toISOString().split('T')[0],
        [selectedMetric]: Math.round(predictedValue),
        [`${selectedMetric}Upper`]: Math.round(predictedValue + marginOfError),
        [`${selectedMetric}Lower`]: Math.max(0, Math.round(predictedValue - marginOfError))
      });
    }
    
    return predictions;
  };

  const linearRegression = (xValues, yValues) => {
    const n = xValues.length;
    
    // Calculate means
    const xMean = xValues.reduce((sum, val) => sum + val, 0) / n;
    const yMean = yValues.reduce((sum, val) => sum + val, 0) / n;
    
    // Calculate slope and intercept
    let numerator = 0;
    let denominator = 0;
    
    for (let i = 0; i < n; i++) {
      numerator += (xValues[i] - xMean) * (yValues[i] - yMean);
      denominator += Math.pow(xValues[i] - xMean, 2);
    }
    
    const slope = numerator / denominator;
    const intercept = yMean - (slope * xMean);
    
    return { slope, intercept };
  };

  const handlePredictionDaysChange = (e) => {
    setPredictionDays(parseInt(e.target.value));
  };

  const handleConfidenceIntervalChange = (e) => {
    setConfidenceInterval(parseFloat(e.target.value));
  };

  const handleMetricChange = (e) => {
    setSelectedMetric(e.target.value);
  };

  const exportData = (format) => {
    // Combine historical and predicted data
    const combinedData = [...historicalData, ...predictedData];
    
    if (format === 'csv') {
      // Create CSV content
      const headers = ['date', selectedMetric];
      if (predictedData.length > 0) {
        headers.push(`${selectedMetric}Upper`, `${selectedMetric}Lower`);
      }
      
      let csvContent = headers.join(',') + '\n';
      
      combinedData.forEach(row => {
        const values = headers.map(header => row[header] !== undefined ? row[header] : '');
        csvContent += values.join(',') + '\n';
      });
      
      // Create and download the file
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `gradient_predictions_${new Date().toISOString().split('T')[0]}.csv`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } else if (format === 'json') {
      // Create JSON content
      const jsonContent = JSON.stringify(combinedData, null, 2);
      
      // Create and download the file
      const blob = new Blob([jsonContent], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `gradient_predictions_${new Date().toISOString().split('T')[0]}.json`);
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const getMetricColor = (metric) => {
    const colors = {
      poa: '#8884d8',
      poc: '#82ca9d',
      referral: '#ffc658',
      total: '#ff7300'
    };
    return colors[metric] || '#8884d8';
  };

  const combinedData = [...historicalData, ...predictedData];
  
  return (
    <div className="predictive-analytics">
      <div className="controls-panel">
        <div className="control-group">
          <label htmlFor="metricSelect">Metric:</label>
          <select 
            id="metricSelect" 
            value={selectedMetric} 
            onChange={handleMetricChange}
          >
            <option value="poa">POA Points</option>
            <option value="poc">POC Points</option>
            <option value="referral">Referral Points</option>
            <option value="total">Total Points</option>
          </select>
        </div>
        
        <div className="control-group">
          <label htmlFor="predictionDays">Prediction Days:</label>
          <select 
            id="predictionDays" 
            value={predictionDays} 
            onChange={handlePredictionDaysChange}
          >
            <option value="7">7 Days</option>
            <option value="14">14 Days</option>
            <option value="30">30 Days</option>
            <option value="60">60 Days</option>
            <option value="90">90 Days</option>
          </select>
        </div>
        
        <div className="control-group">
          <label htmlFor="confidenceInterval">Confidence:</label>
          <select 
            id="confidenceInterval" 
            value={confidenceInterval} 
            onChange={handleConfidenceIntervalChange}
          >
            <option value="0.90">90%</option>
            <option value="0.95">95%</option>
            <option value="0.99">99%</option>
          </select>
        </div>
        
        <div className="export-buttons">
          <button onClick={() => exportData('csv')} className="export-button">
            Export CSV
          </button>
          <button onClick={() => exportData('json')} className="export-button">
            Export JSON
          </button>
        </div>
      </div>
      
      <div className="chart-container">
        {loading ? (
          <div className="loading">Loading predictions...</div>
        ) : (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={combinedData} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }} 
                tickFormatter={(value) => {
                  const date = new Date(value);
                  return `${date.getMonth() + 1}/${date.getDate()}`;
                }}
              />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => {
                  if (name === `${selectedMetric}Upper`) return [`${value} (Upper Bound)`, 'Confidence Interval'];
                  if (name === `${selectedMetric}Lower`) return [`${value} (Lower Bound)`, 'Confidence Interval'];
                  return [value, name === selectedMetric ? `${selectedMetric.toUpperCase()} Points` : name];
                }}
                labelFormatter={(label) => {
                  const date = new Date(label);
                  return date.toLocaleDateString();
                }}
              />
              <Legend />
              
              {/* Historical data line */}
              <Line 
                type="monotone" 
                dataKey={selectedMetric} 
                name={`${selectedMetric.toUpperCase()} Points (Historical)`}
                data={historicalData}
                stroke={getMetricColor(selectedMetric)} 
                strokeWidth={2}
                dot={{ r: 1 }}
                activeDot={{ r: 5 }}
              />
              
              {/* Prediction line */}
              <Line 
                type="monotone" 
                dataKey={selectedMetric} 
                name={`${selectedMetric.toUpperCase()} Points (Predicted)`}
                data={predictedData}
                stroke={getMetricColor(selectedMetric)} 
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ r: 1 }}
                activeDot={{ r: 5 }}
              />
              
              {/* Confidence interval upper bound */}
              <Line 
                type="monotone" 
                dataKey={`${selectedMetric}Upper`} 
                name="Upper Bound"
                data={predictedData}
                stroke="#ccc" 
                strokeWidth={1}
                strokeDasharray="3 3"
                dot={false}
              />
              
              {/* Confidence interval lower bound */}
              <Line 
                type="monotone" 
                dataKey={`${selectedMetric}Lower`} 
                name="Lower Bound"
                data={predictedData}
                stroke="#ccc" 
                strokeWidth={1}
                strokeDasharray="3 3"
                dot={false}
              />
              
              {/* Reference line for today */}
              <ReferenceLine 
                x={historicalData.length > 0 ? historicalData[historicalData.length - 1].date : null} 
                stroke="#666" 
                strokeDasharray="3 3"
                label={{ value: 'Today', position: 'insideTopRight' }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
      
      <div className="prediction-insights">
        <h3>Prediction Insights</h3>
        {!loading && predictedData.length > 0 && (
          <div className="insights-content">
            <div className="insight-item">
              <span className="insight-label">Current {selectedMetric.toUpperCase()} Points:</span>
              <span className="insight-value">
                {historicalData.length > 0 ? historicalData[historicalData.length - 1][selectedMetric] : 'N/A'}
              </span>
            </div>
            
            <div className="insight-item">
              <span className="insight-label">Predicted {selectedMetric.toUpperCase()} Points (in {predictionDays} days):</span>
              <span className="insight-value">
                {predictedData.length > 0 ? predictedData[predictedData.length - 1][selectedMetric] : 'N/A'}
              </span>
            </div>
            
            <div className="insight-item">
              <span className="insight-label">Confidence Interval ({Math.round(confidenceInterval * 100)}%):</span>
              <span className="insight-value">
                {predictedData.length > 0 ? 
                  `${predictedData[predictedData.length - 1][`${selectedMetric}Lower`]} - ${predictedData[predictedData.length - 1][`${selectedMetric}Upper`]}` : 
                  'N/A'}
              </span>
            </div>
            
            <div className="insight-item">
              <span className="insight-label">Projected Growth:</span>
              <span className="insight-value">
                {historicalData.length > 0 && predictedData.length > 0 ? 
                  `${Math.round((predictedData[predictedData.length - 1][selectedMetric] / historicalData[historicalData.length - 1][selectedMetric] - 1) * 100)}%` : 
                  'N/A'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictiveAnalytics;
