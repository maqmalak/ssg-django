# React JS Guide: Accessing Django Hangerline API Data

## Overview
This guide provides a complete setup for accessing the Django Hangerline API from a React JS application using basic authentication with credentials `apiuser:P@kistan12`.

## Prerequisites
- Node.js installed (v14 or higher)
- Basic React knowledge
- Django server running on `http://localhost:8001`

## 1. Setting Up React Application

```bash
# Create new React app
npx create-react-app hangerline-dashboard
cd hangerline-dashboard

# Install required dependencies
npm install axios react-chartjs-2 chart.js tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p
```

## 2. Styling Setup

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--primary-color)',
        secondary: 'var(--secondary-color)',
        surface: 'var(--surface-color)',
        muted: {
          surface: 'var(--muted-surface)',
          text: 'var(--muted-text)',
        },
        success: 'var(--success-color)',
        danger: 'var(--danger-color)',
        warning: 'var(--warning-color)',
      },
      boxShadow: {
        'soft': '0 18px 60px var(--shadow-color)',
      },
    },
  },
  plugins: [],
}
```

Update `src/index.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html, body, #root {
    @apply h-full;
  }

  body {
    @apply bg-[#050b18] text-gray-200 antialiased;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    font-feature-settings: "ss01" on, "cv01" on;
  }

  ::selection {
    @apply bg-teal-500/35;
  }

  /* Subtle scrollbars */
  *::-webkit-scrollbar {
    width: 10px;
    height: 10px;
  }
  *::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.22);
    border-radius: 999px;
    border: 2px solid rgba(2, 6, 23, 0.5);
  }
  *::-webkit-scrollbar-track {
    background: rgba(2, 6, 23, 0.35);
  }
}

@layer components {
  .app-shell {
    @apply min-h-screen;
    background:
      radial-gradient(1000px 520px at 18% 0%, rgba(20,184,166,.18), transparent 55%),
      radial-gradient(920px 520px at 86% 12%, rgba(99,102,241,.10), transparent 50%),
      radial-gradient(920px 520px at 50% 100%, rgba(245,158,11,.07), transparent 55%),
      linear-gradient(180deg, #040914, #040914);
  }

  .glass {
    @apply bg-white/5 border border-white/10 backdrop-blur-xl;
  }

  .card {
    @apply glass rounded-2xl shadow-soft overflow-hidden;
  }

  /* Hover effects */
  .hover-lift {
    @apply transition-all duration-300;
    will-change: transform, filter;
  }
  .hover-lift:hover {
    transform: translateY(-10px);
    filter: brightness(1.08);
  }

  .hover-outline {
    @apply transition-all duration-300 border border-white/10;
  }
  .hover-outline:hover {
    @apply border-white/18;
    box-shadow: 0 0 0 4px rgba(20,184,166,.32), 0 18px 60px rgba(2,6,23,.4);
  }

  /* Form elements */
  .input {
    @apply w-full rounded-xl px-3 py-2 bg-white/5 border border-white/10 text-white placeholder:text-white/30 outline-none transition-all;
  }
  .input:focus {
    box-shadow: 0 0 0 4px rgba(20,184,166,.32);
    border-color: rgba(20,184,166,.55);
  }

  .btn {
    @apply inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold transition-all;
  }

  .btn-primary {
    @apply btn bg-teal-500 text-white hover:brightness-110 active:brightness-95;
    box-shadow: 0 10px 35px rgba(20,184,166,.32);
  }

  .btn-ghost {
    @apply btn bg-white/5 text-white border border-white/10 hover:bg-white/10 active:bg-white/5;
  }
  .btn-ghost:hover {
    box-shadow: 0 0 0 4px rgba(20,184,166,.32);
  }

  /* Status badges */
  .badge-positive {
    @apply inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs;
    background: rgba(34,197,94,.12);
    color: rgb(134 239 172);
    border: 1px solid rgba(34,197,94,.25);
  }

  .badge-negative {
    @apply inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs;
    background: rgba(239,68,68,.12);
    color: rgb(254 202 202);
    border: 1px solid rgba(239,68,68,.25);
  }

  .badge-neutral {
    @apply inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs;
    background: rgba(148,163,184,.12);
    color: rgb(226 232 240);
    border: 1px solid rgba(148,163,184,.22);
  }

  /* Progress bars */
  .progress-rail {
    @apply w-full h-2 rounded-full bg-white/10 overflow-hidden;
  }
  .progress-bar {
    @apply h-full rounded-full;
    background: linear-gradient(90deg, rgba(14,165,233,1), rgba(34,197,94,1));
  }
}

@layer utilities {
  .text-muted { @apply text-gray-400; }
}
```

Update `src/index.js` to use the app-shell class:

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div className="app-shell">
      <App />
    </div>
  </React.StrictMode>
);
```

## 3. API Configuration

Create `src/api/config.js`:

```javascript
const API_BASE_URL = 'http://116.58.15.14:8001/hangerline';
const API_CREDENTIALS = {
  username: 'apiuser',
  password: 'P@kistan12'
};

export { API_BASE_URL, API_CREDENTIALS };
```

## 3. API Service Module

Create `src/api/hangerlineApi.js`:

```javascript
import axios from 'axios';
import { API_BASE_URL, API_CREDENTIALS } from './config';

// Create axios instance with authentication
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  auth: API_CREDENTIALS,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints with their functions
export const hangerlineApi = {
  // Shift summary data (no staff auth required)
  getShiftData: (params = {}) =>
    apiClient.get('/api/chart/shift/', { params }),

  // Source connection summary (requires staff auth)
  getSourceData: (params = {}) =>
    apiClient.get('/api/chart/source/', { params }),

  // Production category summary (requires staff auth)
  getProductionData: (params = {}) =>
    apiClient.get('/api/chart/production/', { params }),

  // Daily trend line chart (requires staff auth)
  getLineData: (params = {}) =>
    apiClient.get('/api/chart/line/', { params }),

  // Line-wise offloading summary (requires staff auth)
  getLineOffloadingData: (params = {}) =>
    apiClient.get('/api/chart/line-offloading/', { params }),

  // Line-wise loading summary (requires staff auth)
  getLineLoadingData: (params = {}) =>
    apiClient.get('/api/chart/line-loading/', { params }),

  // Line target summary (requires staff auth)
  getLineTargetSummary: (params = {}) =>
    apiClient.get('/api/chart/line-target-summary/', { params }),

  // Line-wise targets (requires staff auth)
  getLineWiseTargets: (params = {}) =>
    apiClient.get('/api/chart/line-wise-targets/', { params }),
};

export default hangerlineApi;
```

## 4. React Component Examples

### Beautiful Dashboard Component

Create `src/components/Dashboard.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { hangerlineApi } from '../api/hangerlineApi';

const Dashboard = () => {
  const [shiftData, setShiftData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await hangerlineApi.getShiftData();
        setShiftData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-teal-400 text-lg">Loading dashboard...</div>
    </div>
  );

  if (error) return (
    <div className="card p-6 m-4 max-w-md mx-auto">
      <div className="text-red-400 text-center">
        <div className="text-lg font-semibold mb-2">Error Loading Data</div>
        <div className="text-sm text-muted">{error}</div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-light text-white mb-2">🏭 Production Dashboard</h1>
        <p className="text-gray-400 text-lg">Real-time production analytics & insights</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {shiftData && shiftData.datasets.map((dataset, index) => (
          <div key={index} className="card hover-lift p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="text-sm text-muted tracking-wide uppercase">
                {dataset.label}
              </div>
              <div className="text-2xl">
                {dataset.label === 'Loading' ? '📦' :
                 dataset.label === 'Offloading' ? '🚚' : '⚡'}
              </div>
            </div>
            <div className="text-3xl font-bold text-white mb-2">
              {dataset.data.reduce((a, b) => a + b, 0).toLocaleString()}
            </div>
            <div className="text-sm text-muted">
              Total across all shifts
            </div>
          </div>
        ))}
      </div>

      {/* Shift Breakdown */}
      <div className="card hover-lift p-6 mb-8">
        <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-3">
          🕐 Shift Performance Breakdown
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {shiftData.labels.map((shift, index) => (
            <div key={shift} className="hover-outline rounded-xl p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="text-lg font-semibold text-white">{shift} Shift</div>
                <div className="chip">
                  Active
                </div>
              </div>

              {shiftData.datasets.map((dataset, datasetIndex) => (
                <div key={datasetIndex} className="flex items-center justify-between py-2">
                  <span className="text-sm text-muted">{dataset.label}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-white font-medium">
                      {dataset.data[index]?.toLocaleString() || 0}
                    </span>
                    <div className="progress-rail w-20">
                      <div
                        className="progress-bar"
                        style={{
                          width: `${(dataset.data[index] || 0) / Math.max(...dataset.data) * 100}%`
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-4 justify-center">
        <button className="btn-primary">
          📊 View Detailed Reports
        </button>
        <button className="btn-ghost">
          🔄 Refresh Data
        </button>
        <button className="btn-ghost">
          📈 Export Analytics
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
```

### Component with Date Filtering

Create `src/components/LineChartWithFilter.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { hangerlineApi } from '../api/hangerlineApi';

const LineChartWithFilter = () => {
  const [chartData, setChartData] = useState(null);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const params = {};
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;

      const response = await hangerlineApi.getLineData(params);
      setChartData(response.data);
    } catch (err) {
      console.error('Error fetching line data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="line-chart-container">
      <h2>Line Chart with Date Filter</h2>
      <div className="filter-controls">
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          placeholder="Start Date"
        />
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          placeholder="End Date"
        />
        <button onClick={fetchData} disabled={loading}>
          {loading ? 'Loading...' : 'Fetch Data'}
        </button>
      </div>

      {chartData && (
        <div className="chart-data">
          <h3>Daily Production Trends</h3>
          <p>Dates: {chartData.labels.join(', ')}</p>
          {chartData.datasets.map((dataset, index) => (
            <div key={index}>
              <h4>{dataset.label}</h4>
              <p>Values: {dataset.data.join(', ')}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default LineChartWithFilter;
```

## 5. Chart.js Integration

### Bar Chart Component

Create `src/components/ShiftBarChart.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { hangerlineApi } from '../api/hangerlineApi';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ShiftBarChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await hangerlineApi.getShiftData();
        setChartData(response.data);
      } catch (err) {
        console.error('Error fetching shift data:', err);
      }
    };
    fetchData();
  }, []);

  if (!chartData) return <div>Loading chart...</div>;

  const data = {
    labels: chartData.labels,
    datasets: chartData.datasets.map(dataset => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || 'rgba(54, 162, 235, 0.8)',
    }))
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Shift Summary',
      },
    },
  };

  return (
    <div>
      <h2>Production by Shift</h2>
      <Bar data={data} options={options} />
    </div>
  );
};

export default ShiftBarChart;
```

### Line Chart Component

Create `src/components/DailyTrendChart.js`:

```javascript
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { hangerlineApi } from '../api/hangerlineApi';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const DailyTrendChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await hangerlineApi.getLineData();
        setChartData(response.data);
      } catch (err) {
        console.error('Error fetching line data:', err);
      }
    };
    fetchData();
  }, []);

  if (!chartData) return <div>Loading chart...</div>;

  const data = {
    labels: chartData.labels,
    datasets: chartData.datasets.map(dataset => ({
      ...dataset,
      borderColor: dataset.borderColor || 'rgba(54, 162, 235, 1)',
      backgroundColor: dataset.backgroundColor || 'rgba(54, 162, 235, 0.1)',
      fill: false,
    }))
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Daily Production Trends',
      },
    },
  };

  return (
    <div>
      <h2>Daily Trends (Last 30 Days)</h2>
      <Line data={data} options={options} />
    </div>
  );
};

export default DailyTrendChart;
```

## 6. Error Handling and Best Practices

### Enhanced Error Handling Hook

Create `src/hooks/useApi.js`:

```javascript
import { useState } from 'react';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = async (apiCall, params = {}) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiCall(params);
      return { data: response.data, error: null };
    } catch (error) {
      let errorMessage = 'An error occurred';

      if (error.response) {
        // Server responded with error status
        errorMessage = `Server error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`;
      } else if (error.request) {
        // Network error
        errorMessage = 'Network error - check server connection and CORS settings';
      } else {
        // Other error
        errorMessage = error.message;
      }

      setError(errorMessage);
      return { data: null, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  return { execute, loading, error };
};
```

### Usage with Custom Hook

```javascript
import React, { useEffect, useState } from 'react';
import { hangerlineApi } from '../api/hangerlineApi';
import { useApi } from '../hooks/useApi';

const ProductionChart = () => {
  const [chartData, setChartData] = useState(null);
  const { execute, loading, error } = useApi();

  const fetchData = async () => {
    const result = await execute(hangerlineApi.getProductionData);
    if (result.data) {
      setChartData(result.data);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div>Loading production data...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Production Categories</h2>
      {chartData && (
        <div>
          <p>Categories: {chartData.labels.join(', ')}</p>
          <p>Values: {chartData.datasets[0].data.join(', ')}</p>
        </div>
      )}
    </div>
  );
};

export default ProductionChart;
```

## 7. Django CORS Configuration

If you encounter CORS issues, add this to your Django `settings.py`:

```python
# settings.py
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

# Allow React development server
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# Or allow all origins (less secure, use only for development)
# CORS_ALLOW_ALL_ORIGINS = True
```

## 8. API Endpoints Summary

| Endpoint | Description | Auth Required | Parameters |
|----------|-------------|---------------|------------|
| `/api/chart/shift/` | Shift summary data | Basic Auth | `start_date`, `end_date` |
| `/api/chart/source/` | Source connection summary | Staff | `start_date`, `end_date` |
| `/api/chart/production/` | Production categories | Staff | `start_date`, `end_date` |
| `/api/chart/line/` | Daily trends | Staff | `start_date`, `end_date` |
| `/api/chart/line-offloading/` | Line offloading summary | Staff | `start_date`, `end_date` |
| `/api/chart/line-loading/` | Line loading summary | Staff | `start_date`, `end_date` |
| `/api/chart/line-target-summary/` | Target summary | Staff | `start_date`, `end_date` |
| `/api/chart/line-wise-targets/` | Line-wise targets | Staff | `start_date`, `end_date` |

## 9. Data Models Reference

Based on the Django migration file, the API interacts with:
- **LineTargetDetail** model with fields:
  - `stpo_key_id` (ForeignKey to StylePlannedOrder)
  - `pono` (PO Number)
  - `st_id` (Style ID)

## 10. Production Considerations

- **Authentication**: Consider implementing token-based authentication for production
- **Error Handling**: Implement comprehensive error boundaries in React
- **Loading States**: Always show loading indicators during API calls
- **Caching**: Consider implementing data caching for frequently accessed data
- **Rate Limiting**: Be aware of Django's rate limiting if implemented

## 11. Testing the Setup

1. Start your Django server: `python manage.py runserver 8001`
2. Start React app: `npm start`
3. Test API calls using browser developer tools
4. Verify authentication is working
5. Check CORS headers if accessing from different ports

This guide provides everything needed to integrate your React application with the Django Hangerline API.
