const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3002;

// Direct PostgreSQL connection - lightweight proxy for browser
const pool = new Pool({
  host: '172.16.7.6',
  port: 5432,
  database: 'ssg',
  user: 'postgres',
  password: 'P@kistan12',
  schema: 'public',
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

app.use(cors({
  origin: ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:8001', 'http://127.0.0.1:8001', 'http://localhost:3000', 'http://127.0.0.1:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true
}));
app.use(express.json());

// Helper functions (same as original server.js)
const buildLineFilter = (line) => {
  if (!line || line === 'All' || line === '$__all') {
    return "('line-21','line-22','line-23','line-24','line-25','line-26','line-27','line-28','line-29','line-30','line-31','line-32')";
  }
  if (Array.isArray(line)) {
    return `(${line.map(l => `'${l}'`).join(',')})`;
  }
  return `('${line}')`;
};

const buildShiftFilter = (shift) => {
  if (!shift || shift === 'All' || shift === '$__all') {
    return "('Day','Night')";
  }
  if (Array.isArray(shift)) {
    return `(${shift.map(s => `'${s}'`).join(',')})`;
  }
  return `('${shift}')`;
};

const buildPOFilter = (po_id) => {
  if (!po_id || po_id === 'All' || po_id === '$__all') {
    return "IS NOT NULL";  // Allow all PO IDs when not specified
  }
  if (Array.isArray(po_id)) {
    return `IN (${po_id.map(po => `'${po}'`).join(',')})`;
  }
  return `= '${po_id}'`;
};

const buildSTIDFilter = (st_id) => {
  if (!st_id || st_id === 'All' || st_id === '$__all') {
    return "IS NOT NULL";  // Allow all ST IDs when not specified
  }
  if (Array.isArray(st_id)) {
    return `IN (${st_id.map(st => `'${st}'`).join(',')})`;
  }
  return `= '${st_id}'`;
};

// Test connection
app.get('/api/test', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ status: 'connected', timestamp: result.rows[0] });
  } catch (error) {
    console.error('Database connection error:', error);
    res.status(500).json({ error: 'Database connection failed', details: error.message });
  }
});

// Get distinct PO IDs
app.get('/api/po-ids', async (req, res) => {
  try {
    const { start_date, end_date } = req.query;
    const startDate = start_date || new Date().toISOString().split('T')[0];
    const endDate = end_date || new Date().toISOString().split('T')[0];

    const result = await pool.query(`
      SELECT DISTINCT odpd_lot_number::TEXT as po_id
      FROM operator_daily_performance
      WHERE odpd_lot_number like 'B%'
      and odp_date >= $1::date AND odp_date <= $2::date
      ORDER BY po_id
      LIMIT 1000
    `, [startDate, endDate]);
    res.json({ po_ids: result.rows.map(row => row.po_id) });
  } catch (error) {
    console.error('Error fetching PO IDs:', error);
    res.status(500).json({ error: 'Failed to fetch PO IDs', details: error.message });
  }
});

// Get distinct ST IDs
app.get('/api/st-ids', async (req, res) => {
  try {
    const { start_date, end_date } = req.query;
    const startDate = start_date || new Date().toISOString().split('T')[0];
    const endDate = end_date || new Date().toISOString().split('T')[0];

    const result = await pool.query(`
      SELECT DISTINCT st_id::TEXT as st_id
      FROM operator_daily_performance
      WHERE st_id IS NOT NULL AND LOWER(st_id) NOT LIKE '%test%'
      and odp_date >= $1::date AND odp_date <= $2::date
      ORDER BY st_id
      LIMIT 1000
    `, [startDate, endDate]);
    res.json({ st_ids: result.rows.map(row => row.st_id) });
  } catch (error) {
    console.error('Error fetching ST IDs:', error);
    res.status(500).json({ error: 'Failed to fetch ST IDs', details: error.message });
  }
});

// Production trend endpoint - Returns 30-day daily aggregated data
app.get('/api/production-trend', async (req, res) => {
  try {
    const { end_date, line, shift, po_id, st_id } = req.query;
    
    // Calculate 30 days back from end_date (default to today)
    const endDate = end_date || new Date().toISOString().split('T')[0];
    const startDate = new Date(endDate);
    startDate.setDate(startDate.getDate() - 29); // 30 days including end_date
    const startDateStr = startDate.toISOString().split('T')[0];
    
    const lineFilter = buildLineFilter(line);
    const shiftFilter = buildShiftFilter(shift);
    const poFilter = buildPOFilter(po_id);
    const stidFilter = buildSTIDFilter(st_id);
    
    console.log('📈 Fetching 30-day trend data from', startDateStr, 'to', endDate);
    
    // Query daily aggregates for last 30 days (MUST match production-data query exactly)
    const result = await pool.query(`
      SELECT
        odp.odp_date::TEXT as date,
        SUM(CASE WHEN odp.oc_description = 'Loading/Panel Segregation' 
            THEN odp.odpd_quantity ELSE 0 END) AS loading,
        SUM(CASE WHEN odp.oc_description = 'Garment Insert in Poly Bag & Close' 
            THEN odp.odpd_quantity ELSE 0 END) AS offloading,
        SUM(CASE WHEN odp.oc_description = 'Loading/Panel Segregation' 
            THEN odp.odpd_quantity ELSE 0 END) - 
        SUM(CASE WHEN odp.oc_description = 'Garment Insert in Poly Bag & Close' 
            THEN odp.odpd_quantity ELSE 0 END) AS wip
      FROM operator_daily_performance odp
      WHERE odp.odp_date >= $1::date AND odp.odp_date <= $2::date
        AND odp.source_connection IN ${lineFilter.replace(/\$/g, '$$')}
        AND odp.shift IN ${shiftFilter.replace(/\$/g, '$$')}
        AND odp.odpd_lot_number ${poFilter.replace(/\$/g, '$$')}
        AND odp.st_id ${stidFilter.replace(/\$/g, '$$')}
        AND odp.oc_description IN ('Loading/Panel Segregation', 'Garment Insert in Poly Bag & Close')
      GROUP BY odp.odp_date
      ORDER BY odp.odp_date ASC
    `, [startDateStr, endDate]);
    
    console.log(`✅ Trend data fetched: ${result.rows.length} days`);
    
    res.json({ 
      trendData: result.rows,
      dateRange: { start: startDateStr, end: endDate },
      dataPoints: result.rows.length
    });
  } catch (error) {
    console.error('❌ Trend data error:', error);
    res.status(500).json({ error: 'Failed to fetch trend data', details: error.message });
  }
});

// Direct PostgreSQL production data endpoint
app.get('/api/production-data', async (req, res) => {
  try {
    const { start_date, end_date, line, shift, po_id, st_id } = req.query;

    const startDate = start_date || new Date().toISOString().split('T')[0];
    const endDate = end_date || new Date().toISOString().split('T')[0];

    const lineFilter = buildLineFilter(line);
    const shiftFilter = buildShiftFilter(shift);
    const poFilter = buildPOFilter(po_id);
    const stidFilter = buildSTIDFilter(st_id);

    console.log('📊 Direct PostgreSQL query with date range:', { startDate, endDate, line, shift, po_id, st_id });
    console.log('🔍 Line filter:', lineFilter);
    console.log('🔍 Raw query parameters:', { start_date, end_date, line, shift, po_id, st_id });
    console.log('🔍 Total target query:', `
      SELECT SUM(total_target_qty) AS total_target
      FROM line_target
      WHERE target_date >= '${startDate}'::date AND target_date <= '${endDate}'::date
        AND source_connection IN ${lineFilter}
    `);

    // Execute all queries in parallel
    const [
      summaryResult,
      totalTargetResult,
      availableDatesResult,
      wipResult,
      defectsResult,
      efficiencyResult,
      attendanceResult,
      breakdownResult,
      breakdownCategoryResult,
      defectReasonsResult
    ] = await Promise.all([
      // Query 1: Summary
      pool.query(`
        SELECT
          odp.odp_date,
          odp.source_connection,
          odp.source_connection as line,
          odp.shift,
          target_qty AS target,
          SUM(CASE WHEN odp.oc_description = 'Loading/Panel Segregation' THEN odp.odpd_quantity ELSE 0 END) AS loading,
          SUM(CASE WHEN odp.oc_description = 'Garment Insert in Poly Bag & Close' THEN odp.odpd_quantity ELSE 0 END) AS offloading
        FROM operator_daily_performance odp
        LEFT JOIN (
          SELECT
            target_date,
            source_connection,
            SUM(total_target_qty) AS target_qty
          FROM line_target
          WHERE target_date >= $1::date AND target_date <= $2::date
            AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
            AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
          GROUP BY target_date, source_connection
        ) AS target ON target.source_connection = odp.source_connection
          AND target.target_date = odp.odp_date
        WHERE odp.odp_date >= $1::date AND odp.odp_date <= $2::date
          AND odp.source_connection IN ${lineFilter.replace(/\$/g, '$$')}
          AND odp.shift IN ${shiftFilter.replace(/\$/g, '$$')}
          AND odp.odpd_lot_number ${poFilter.replace(/\$/g, '$$')}
          AND odp.st_id ${stidFilter.replace(/\$/g, '$$')}
          AND odp.oc_description IN ('Loading/Panel Segregation', 'Garment Insert in Poly Bag & Close')
        GROUP BY odp.odp_date, odp.source_connection, odp.shift, target_qty
        ORDER BY 1 ASC
      `, [startDate, endDate]),

      // Query 1.5: Total Target from LineTarget model (matching Grafana query)
      pool.query(`
        SELECT SUM(total_target_qty) AS total_target
        FROM line_target
        WHERE target_date >= $1::date AND target_date <= $2::date
          AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
          AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
      `, [startDate, endDate]),

      // Query 1.6: Check all available target dates
      pool.query(`
        SELECT target_date, COUNT(*) as entries, SUM(total_target_qty) as daily_total
        FROM line_target
        GROUP BY target_date
        ORDER BY target_date DESC
        LIMIT 10
      `, []),

      // Query 2: WIP - Comprehensive CTE-based calculation with fixed start date
      pool.query(`
        WITH wip_data AS (
          SELECT
            source_connection,
            odpd_lot_number,
            st_id,
            MIN(odp_date) AS start_date,
            MAX(odp_date) AS end_date,
            SUM(loading_qty) AS todate_loading,
            SUM(unloading_qty) AS todate_unloading,
            GREATEST(SUM(NULLIF(loading_qty, 0)) - SUM(NULLIF(unloading_qty, 0)), 0) AS line_wip
          FROM operator_daily_performance
          WHERE odp_date > '2025-06-01' AND odp_date <= $2::date
            AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
            AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
            AND odpd_lot_number ${poFilter.replace(/\$/g, '$$')}
            AND st_id ${stidFilter.replace(/\$/g, '$$')}
            AND oc_description IN ('Loading/Panel Segregation', 'Garment Insert in Poly Bag & Close')
          GROUP BY source_connection, odpd_lot_number, st_id
        )
        SELECT
          odp.source_connection,
          odp.odpd_lot_number,
          odp.st_id,
          wip.start_date,
          wip.end_date,
          SUM(odp.loading_qty) AS ondate_loading,
          SUM(odp.unloading_qty) AS ondate_unloading,
          wip.todate_loading,
          wip.todate_unloading,
          wip.line_wip
        FROM operator_daily_performance odp
        INNER JOIN wip_data wip ON odp.source_connection = wip.source_connection
          AND odp.st_id = wip.st_id
          AND odp.odpd_lot_number = wip.odpd_lot_number
        WHERE odp.odp_date >= $1::date AND odp.odp_date <= $2::date
          AND odp.source_connection IN ${lineFilter.replace(/\$/g, '$$')}
          AND odp.shift IN ${shiftFilter.replace(/\$/g, '$$')}
          AND odp.odpd_lot_number ${poFilter.replace(/\$/g, '$$')}
          AND odp.st_id ${stidFilter.replace(/\$/g, '$$')}
          AND odp.oc_description IN ('Loading/Panel Segregation', 'Garment Insert in Poly Bag & Close')
        GROUP BY odp.source_connection, odp.odpd_lot_number, odp.st_id,
          wip.start_date, wip.end_date, wip.todate_loading, wip.todate_unloading, wip.line_wip
        ORDER BY odp.source_connection, odp.odpd_lot_number, odp.st_id
      `, [startDate, endDate]),

      // Query 3: Defects
      pool.query(`
        SELECT source_connection, SUM(qcr_defect_quantity) AS defect_quantity
        FROM quality_control_repair
        WHERE qcr_date >= $1::date AND qcr_date <= $2::date
          AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
          AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
        GROUP BY source_connection
      `, [startDate, endDate]),

      // Query 4: Efficiency
      pool.query(`
        WITH perf_data AS (
          SELECT
            odp_date, st_id, source_connection,
            MIN(REGEXP_REPLACE(st_id, '[-_].*', '')) AS article_prefix,
            SUM(odpd_quantity) FILTER (WHERE oc_description IN ('Loading/Panel Segregation')) AS ondate_loading,
            SUM(odpd_quantity) FILTER (WHERE oc_description IN ('Garment Insert in Poly Bag & Close')) AS ondate_unloading,
            COUNT(DISTINCT odp_em_key) FILTER (WHERE LEFT(odp_em_key::TEXT, 5) = '10613') AS emp_count
          FROM operator_daily_performance
          WHERE odp_date >= $1::date AND odp_date <= $2::date
            AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
            AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
            AND odpd_lot_number ${poFilter.replace(/\$/g, '$$')}
            AND st_id ${stidFilter.replace(/\$/g, '$$')}
          GROUP BY odp_date, st_id, source_connection
        ),
        latest_smv AS (
          SELECT articleno, totalsmv, conversionfactor
          FROM (SELECT articleno, totalsmv, conversionfactor,
                ROW_NUMBER() OVER (PARTITION BY articleno ORDER BY applicabledate DESC) AS rn
                FROM operationinformation WHERE applicabledate IS NOT NULL) ranked
          WHERE rn = 1
        )
        SELECT pd.odp_date, pd.source_connection, pd.st_id, pd.article_prefix,
          pd.ondate_loading, pd.ondate_unloading, smv.totalsmv,
          (smv.totalsmv * pd.ondate_unloading) AS total_produced_minutes,
          COALESCE(pd.emp_count, 0) AS emp_count,
          ROUND((CASE WHEN COALESCE(pd.emp_count, 0) = 0 THEN 0
            ELSE 100 * (smv.totalsmv * COALESCE(smv.conversionfactor, 1::NUMERIC) * pd.ondate_unloading) / (pd.emp_count * 480)
          END)::NUMERIC, 2) AS efficiency_percent
        FROM perf_data pd
        LEFT JOIN latest_smv smv ON pd.article_prefix = smv.articleno
        WHERE pd.st_id NOT ILIKE '%test%'
        ORDER BY pd.odp_date ASC
      `, [startDate, endDate]),

      // Query 5: Attendance
      pool.query(`
        WITH stats AS (
          SELECT COUNT(*) AS active FROM hangerline_emp
          WHERE line_desc IN ${lineFilter.replace(/\$/g, '$$')} AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
        ),
        present AS (
          SELECT COUNT(DISTINCT odp_em_key) AS present FROM operator_daily_performance
          WHERE odp_date >= $1::date AND odp_date <= $2::date
            AND LEFT(odp_em_key::TEXT, 5) = '10613'
            AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
            AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
            AND odp_em_key IN (SELECT id FROM hangerline_emp)
        )
        SELECT s.active AS active_employees, p.present AS present_employees,
          ROUND(100.0 * p.present / NULLIF(s.active, 0), 2) AS attendance_percent
        FROM stats s CROSS JOIN present p
      `, [startDate, endDate]),

      // Query 6: Breakdown
      pool.query(`
        SELECT SUM(EXTRACT(EPOCH FROM (b.time_end - b.time_start)) / 60) AS duration_minutes
        FROM breakdown b WHERE b.p_date >= '2026-12-01' AND b.p_date <= $1::date
      `, [endDate]),

      // Query 7: Breakdown by Category
      pool.query(`
        SELECT c.name AS category_name, SUM(EXTRACT(EPOCH FROM (b.time_end - b.time_start)) / 60) AS duration_minutes
        FROM breakdown b JOIN breakdown_category c ON b.breakdown_category_id = c.id
        WHERE b.p_date >= '2026-12-01' AND b.p_date <= $1::date
        GROUP BY c.name ORDER BY duration_minutes DESC
      `, [endDate]),

      // Query 8: Defect Reasons
      pool.query(`
        SELECT qcsc_description AS reason, SUM(qcr_defect_quantity) AS quantity
        FROM quality_control_repair
        WHERE qcr_date >= $1::date AND qcr_date <= $2::date
          AND source_connection IN ${lineFilter.replace(/\$/g, '$$')}
          AND shift IN ${shiftFilter.replace(/\$/g, '$$')}
        GROUP BY qcsc_description ORDER BY quantity DESC LIMIT 5
      `, [startDate, endDate])
    ]);

    // Process data (same logic as before)
    const summaryData = summaryResult.rows.reduce((acc, row) => {
      const line = row.line || row.source_connection;
      if (!acc[line]) acc[line] = { line, loading: 0, offloading: 0, target: 0, shift: { day: 0, night: 0 } };
      acc[line].loading += parseFloat(row.loading) || 0;
      acc[line].offloading += parseFloat(row.offloading) || 0;
      acc[line].target += parseFloat(row.target) || 0;
      if (row.shift === 'Day') acc[line].shift.day += parseFloat(row.offloading) || 0;
      else if (row.shift === 'Night') acc[line].shift.night += parseFloat(row.offloading) || 0;
      return acc;
    }, {});

    const wipData = wipResult.rows.reduce((acc, row) => {
      const line = row.source_connection;
      if (!acc[line]) acc[line] = { wip: 0 };
      acc[line].wip = Math.round(parseFloat(row.line_wip) || 0);
      return acc;
    }, {});

    const defectsData = defectsResult.rows.reduce((acc, row) => {
      acc[row.source_connection] = (acc[row.source_connection] || 0) + (parseInt(row.defect_quantity) || 0);
      return acc;
    }, {});

    const efficiencyData = efficiencyResult.rows.reduce((acc, row) => {
      const line = row.source_connection;
      if (!acc[line]) acc[line] = { efficiencies: [], empCount: 0 };
      acc[line].efficiencies.push(parseFloat(row.efficiency_percent) || 0);
      acc[line].empCount = Math.max(acc[line].empCount, parseInt(row.emp_count) || 0);
      return acc;
    }, {});

    const allLines = [...new Set([...Object.keys(summaryData), ...Object.keys(wipData), ...Object.keys(efficiencyData)])];

    const lineRows = allLines.map(line => {
      const summary = summaryData[line] || {};
      const wip = wipData[line] || {};
      const defects = defectsData[line] || 0;
      const efficiency = efficiencyData[line] || { efficiencies: [], empCount: 0 };
      const avgEfficiency = efficiency.efficiencies.length > 0 ? efficiency.efficiencies.reduce((a, b) => a + b, 0) / efficiency.efficiencies.length : 0;

      return {
        line,
        loading: Math.round(summary.loading || wip.loading || 0),
        offloading: Math.round(summary.offloading || wip.offloading || 0),
        wip: Math.round(wip.wip || 0),
        target: Math.round(summary.target || 0),
        achieved: Math.round(summary.offloading || wip.offloading || 0),
        efficiency: Math.round(avgEfficiency * 100) / 100,
        breakdownMin: Math.round((breakdownResult.rows[0]?.duration_minutes || 0) / allLines.length),
        defects: Math.round(defects),
        shift: { day: Math.round(summary.shift?.day || 0), night: Math.round(summary.shift?.night || 0) },
        workforce: {
          activeEmployees: Math.round(efficiency.empCount || 0),
          presentEmployees: Math.round((attendanceResult.rows[0]?.present_employees || 0) / allLines.length)
        }
      };
    });

    // Get total target from the single result row
    const totalTargetFromModel = Math.round(totalTargetResult.rows[0]?.total_target || 0);
    console.log('🎯 Total target query result:', totalTargetResult.rows[0]);
    console.log('🎯 Total target calculated:', totalTargetFromModel);

    const summary = {
      totalLoading: lineRows.reduce((sum, row) => sum + row.loading, 0),
      totalOffloading: lineRows.reduce((sum, row) => sum + row.offloading, 0),
      totalWip: lineRows.reduce((sum, row) => sum + row.wip, 0),
      totalTarget: totalTargetFromModel, // Use direct LineTarget query result
      defects: lineRows.reduce((sum, row) => sum + row.defects, 0),
      variance: lineRows.reduce((sum, row) => sum + row.offloading, 0) - totalTargetFromModel,
      breakdownTimeMin: Math.round(breakdownResult.rows[0]?.duration_minutes || 0),
      efficiency: lineRows.length > 0 ? lineRows.reduce((sum, row) => sum + row.efficiency, 0) / lineRows.length : 0,
      activeLines: allLines.length,
      totalActiveEmployees: Math.round(attendanceResult.rows[0]?.active_employees || 0),
      totalPresentEmployees: Math.round(attendanceResult.rows[0]?.present_employees || 0),
      attendancePct: parseFloat(attendanceResult.rows[0]?.attendance_percent || 0)
    };

    summary.variancePct = summary.totalTarget > 0 ? Number(((summary.variance / summary.totalTarget) * 100).toFixed(2)) : 0;
    summary.achievementPct = summary.totalTarget > 0 ? Number(((summary.totalOffloading / summary.totalTarget) * 100).toFixed(2)) : 0;

    const breakdownCategories = {
      cats: breakdownCategoryResult.rows.map((row, index) => ({
        name: row.category_name,
        color: ['rgba(239,68,68,.85)', 'rgba(245,158,11,.85)', 'rgba(14,165,233,.85)', 'rgba(34,197,94,.85)', 'rgba(148,163,184,.75)'][index % 5]
      })),
      values: breakdownCategoryResult.rows.map(row => Math.round(row.duration_minutes || 0))
    };

    const defectReasons = {
      reasons: defectReasonsResult.rows.map((row, index) => ({
        name: row.reason,
        color: ['rgba(239,68,68,.85)', 'rgba(245,158,11,.85)', 'rgba(14,165,233,.85)', 'rgba(34,197,94,.85)', 'rgba(148,163,184,.75)'][index % 5]
      })),
      values: defectReasonsResult.rows.map(row => Math.round(row.quantity || 0))
    };

    res.json({
      lines: allLines,
      lineRows,
      summary: {
        ...summary,
        _debug: {
          totalTargetQuery: {
            entries_found: totalTargetResult.rows.length,
            total_target_sum: totalTargetFromModel,
            target_entries: totalTargetResult.rows.slice(0, 10), // Show first 10 entries
            available_dates: availableDatesResult.rows.slice(0, 10) // Show dates with targets
          }
        }
      },
      breakdownCategories,
      defectReasons
    });

  } catch (error) {
    console.error('❌ Direct PostgreSQL query error:', error);
    res.status(500).json({ error: 'Database query failed', details: error.message });
  }
});

app.listen(port, () => {
  console.log(`🚀 Direct PostgreSQL API server running on port ${port}`);
  console.log('✅ Connected directly to PostgreSQL database at 172.16.7.6:5432/ssg');
  console.log('📊 All queries execute directly on PostgreSQL (no caching/API layer)');
  console.log('🔍 Date range filtering works directly in database queries');
});
