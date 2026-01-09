window.ApiData = (function () {
  const DJANGO_BASE_URL = 'http://116.58.15.14:8001/hangerline/api/chart';
  const AUTH_HEADERS = {
    'Authorization': 'Basic ' + btoa('apiuser:P@kistan12')
  };

  // Transform Django API data to match our dashboard format
  const transformDjangoData = (djangoData, filters = {}) => {
    console.log('Transforming Django API data:', djangoData);

    // If we have Chart.js format data, transform it to dashboard format
    if (djangoData.labels && djangoData.datasets) {
      // This is Chart.js format - transform to dashboard data structure
      const lines = ['Line-21', 'Line-22', 'Line-23', 'Line-24', 'Line-25', 'Line-26',
                    'Line-27', 'Line-28', 'Line-29', 'Line-30', 'Line-31', 'Line-32'];

      // Create mock line data based on Chart.js data
      const lineRows = lines.map((line, index) => {
        const baseMultiplier = 1 + (index * 0.1); // Vary data by line
        return {
          line,
          loading: Math.floor(djangoData.datasets[0]?.data[0] * baseMultiplier / 12) || 1800,
          offloading: Math.floor(djangoData.datasets[1]?.data[0] * baseMultiplier / 12) || 1700,
          wip: Math.floor(djangoData.datasets[2]?.data[0] * baseMultiplier / 12) || 100,
          target: Math.floor(1900 * baseMultiplier),
          achieved: Math.floor(1700 * baseMultiplier),
          efficiency: 95 + Math.random() * 5,
          breakdownMin: Math.floor(Math.random() * 20),
          defects: Math.floor(Math.random() * 15),
          shift: {
            day: Math.floor(djangoData.datasets[0]?.data[0] * baseMultiplier / 24) || 900,
            night: Math.floor(djangoData.datasets[0]?.data[1] * baseMultiplier / 24) || 800
          },
          workforce: {
            activeEmployees: 85 + Math.floor(Math.random() * 35),
            presentEmployees: 80 + Math.floor(Math.random() * 30)
          }
        };
      });

      // Calculate summary
      const summary = {
        totalLoading: lineRows.reduce((sum, row) => sum + row.loading, 0),
        totalOffloading: lineRows.reduce((sum, row) => sum + row.offloading, 0),
        totalWip: lineRows.reduce((sum, row) => sum + row.wip, 0),
        totalTarget: lineRows.reduce((sum, row) => sum + row.target, 0),
        defects: lineRows.reduce((sum, row) => sum + row.defects, 0),
        defectVariancePct: 0,
        variance: lineRows.reduce((sum, row) => sum + row.offloading, 0) - lineRows.reduce((sum, row) => sum + row.target, 0),
        variancePct: 0,
        achievementPct: 0,
        breakdownTimeMin: lineRows.reduce((sum, row) => sum + row.breakdownMin, 0),
        efficiency: lineRows.reduce((sum, row) => sum + row.efficiency, 0) / lineRows.length,
        activeLines: lineRows.length,
        totalActiveEmployees: lineRows.reduce((sum, row) => sum + row.workforce.activeEmployees, 0),
        totalPresentEmployees: lineRows.reduce((sum, row) => sum + row.workforce.presentEmployees, 0),
        attendancePct: 0
      };

      // Calculate percentages
      summary.variancePct = summary.totalTarget > 0 ? (summary.variance / summary.totalTarget) * 100 : 0;
      summary.achievementPct = summary.totalTarget > 0 ? (summary.totalOffloading / summary.totalTarget) * 100 : 0;
      summary.attendancePct = summary.totalActiveEmployees > 0 ? (summary.totalPresentEmployees / summary.totalActiveEmployees) * 100 : 0;

      return {
        lines,
        lineRows,
        summary,
        breakdownCategories: {
          cats: [
            { name: 'Mechanical', color: 'rgba(239,68,68,.85)' },
            { name: 'Electrical', color: 'rgba(245,158,11,.85)' },
            { name: 'Changeover', color: 'rgba(14,165,233,.85)' },
            { name: 'Quality', color: 'rgba(34,197,94,.85)' },
            { name: 'Material', color: 'rgba(148,163,184,.75)' },
          ],
          values: [35, 20, 25, 10, 10],
        },
        defectReasons: {
          reasons: [
            { name: 'Stitch Skipped', color: 'rgba(239,68,68,.85)' },
            { name: 'Stain', color: 'rgba(245,158,11,.85)' },
            { name: 'Shade Variation', color: 'rgba(14,165,233,.85)' },
            { name: 'Open Seam', color: 'rgba(34,197,94,.85)' },
            { name: 'Measurement Issue', color: 'rgba(148,163,184,.75)' },
          ],
          values: [14, 11, 9, 8, 6],
        }
      };
    }

    // Fallback to mock data
    return window.MockProductionData.buildDataBundle();
  };

  // Helper function to fetch from API endpoint
  const fetchFromEndpoint = async (endpoint, params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const urlSuffix = queryString ? `?${queryString}` : '';

    const response = await fetch(`${DJANGO_BASE_URL}/${endpoint}/${urlSuffix}`, {
      headers: AUTH_HEADERS
    });

    if (response.ok) {
      return await response.json();
    }
    return null;
  };

  const fetchProductionData = async (filters = {}) => {
    try {
      // Prepare common parameters
      const params = {};
      if (filters.startDate) params.start_date = filters.startDate;
      if (filters.endDate) params.end_date = filters.endDate;
      if (filters.line && filters.line !== 'All') params.line = filters.line;
      if (filters.shift && filters.shift !== 'All') params.shift = filters.shift;

      console.log('Fetching data with filters:', filters);

      // Try to fetch from multiple endpoints for comprehensive data
      const endpoints = [
        'shift',           // Basic shift data (no staff auth required)
        'production',      // Production categories
        'line',            // Daily trends
        'line-offloading', // Line offloading summary
        'line-loading',    // Line loading summary
        'line-target-summary', // Target summary
        'line-wise-targets'   // Line-wise targets
      ];

      let combinedData = null;

      // Try endpoints in order of preference
      for (const endpoint of endpoints) {
        try {
          const data = await fetchFromEndpoint(endpoint, params);
          if (data) {
            console.log(`✅ ${endpoint} data:`, data);
            combinedData = data;
            break; // Use first successful endpoint
          }
        } catch (endpointError) {
          console.warn(`❌ ${endpoint} endpoint failed:`, endpointError.message);
        }
      }

      if (combinedData) {
        // Transform Django data to our dashboard format
        return transformDjangoData(combinedData, filters);
      } else {
        console.warn('All Django API endpoints failed, falling back to mock data');
        return window.MockProductionData.buildDataBundle();
      }
    } catch (error) {
      console.error('Error fetching data from Django API:', error);
      // Fallback to mock data if Django API fails
      console.warn('Falling back to mock data due to Django API error');
      return window.MockProductionData.buildDataBundle();
    }
  };

  const applyFiltersToBundle = async (bundle, filters) => {
    // Use mock data with proper filtering instead of API fetch
    return window.MockProductionData.applyFiltersToBundle(window.MockProductionData.buildDataBundle(), filters);
  };

  const getLineOptions = () => {
    // Return the standard line options
    return Array.from({ length: 12 }).map((_, i) => `Line-${21 + i}`);
  };

  // Test Django API connection
  const testConnection = async () => {
    try {
      const response = await fetch(`${DJANGO_BASE_URL}/shift/`, {
        headers: AUTH_HEADERS
      });
      if (!response.ok) {
        throw new Error(`Django API connection test failed: ${response.status}`);
      }
      const data = await response.json();
      console.log('Django API connection successful:', data);
      return true;
    } catch (error) {
      console.error('Django API connection failed:', error);
      return false;
    }
  };

  return {
    fetchProductionData,
    applyFiltersToBundle,
    getLineOptions,
    testConnection,
  };
})();
