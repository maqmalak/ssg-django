window.MockProductionData = (function () {
  const lines = Array.from({ length: 12 }).map((_, i) => `Line-${21 + i}`);

  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));

  const seededRand = (seed) => {
    let t = seed;
    return () => {
      t += 0x6D2B79F5;
      let x = Math.imul(t ^ (t >>> 15), 1 | t);
      x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
      return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
    };
  };

  const sum = (arr) => arr.reduce((a, b) => a + b, 0);

  const getLineOptions = () => {
    try {
      return Array.from({ length: 12 }).map((_, i) => `Line-${21 + i}`);
    } catch (error) {
      console.error('getLineOptions error:', error);
      return ['Line-21'];
    }
  };

  const buildDataBundle = () => {
    try {
      const r = seededRand(42);

      const lineRows = lines.map((line) => {
        const baseLoad = Math.floor(1800 + r() * 700);
        const offload = Math.floor(baseLoad * (0.96 + r() * 0.05));
        const wip = clamp(baseLoad - offload, 0, 1800);
        const target = Math.floor(1200 + r() * 450);
        const efficiency = Math.round((92 + r() * 10) * 10) / 10;
        const breakdown = Math.floor(r() * 18); // minutes
        const day = Math.floor(offload * (0.58 + r() * 0.10));
        const night = offload - day;

        // Workforce
        const activeEmployees = Math.floor(85 + r() * 35); // per line
        const attendancePct = 0.88 + r() * 0.11; // 88%..99%
        const presentEmployees = clamp(Math.round(activeEmployees * attendancePct), 0, activeEmployees);

        // Quality (per-line, illustrative)
        const defects = Math.floor(2 + r() * 10);

        return {
          line,
          loading: baseLoad,
          offloading: offload,
          wip,
          target,
          achieved: offload,
          efficiency,
          breakdownMin: breakdown,
          defects,
          shift: { day, night },
          workforce: { activeEmployees, presentEmployees },
        };
      });

      const summary = (() => {
        const totalLoading = sum(lineRows.map((x) => x.loading));
        const totalOffloading = sum(lineRows.map((x) => x.offloading));
        const totalWip = sum(lineRows.map((x) => x.wip));
        const totalTarget = sum(lineRows.map((x) => x.target));

        // Defects (still illustrative, but now we also show reason split)
        const defects = Math.floor(35 + seededRand(11)() * 25);
        const defectVariancePct = 0;

        const variance = totalOffloading - totalTarget;
        const variancePct = totalTarget > 0 ? (variance / totalTarget) * 100 : 0;
        const achievementPct = totalTarget > 0 ? (totalOffloading / totalTarget) * 100 : 0;
        const breakdownTimeMin = sum(lineRows.map((x) => x.breakdownMin));
        const efficiency = Math.round((sum(lineRows.map((x) => x.efficiency)) / lineRows.length) * 10) / 10;
        const activeLines = lineRows.length;

        // Workforce summary
        const totalActiveEmployees = sum(lineRows.map((x) => x.workforce.activeEmployees));
        const totalPresentEmployees = sum(lineRows.map((x) => x.workforce.presentEmployees));
        const attendancePct = totalActiveEmployees > 0 ? (totalPresentEmployees / totalActiveEmployees) * 100 : 0;

        return {
          totalLoading,
          totalOffloading,
          totalWip,
          defects,
          defectVariancePct,
          totalTarget,
          variance,
          variancePct,
          achievementPct,
          breakdownTimeMin,
          efficiency,
          activeLines,
          totalActiveEmployees,
          totalPresentEmployees,
          attendancePct,
        };
      })();

      const breakdownCategories = (() => {
        const r2 = seededRand(7);
        const cats = [
          { name: 'Mechanical', color: 'rgba(239,68,68,.85)' },
          { name: 'Electrical', color: 'rgba(245,158,11,.85)' },
          { name: 'Changeover', color: 'rgba(14,165,233,.85)' },
          { name: 'Quality', color: 'rgba(34,197,94,.85)' },
          { name: 'Material', color: 'rgba(148,163,184,.75)' },
        ];
        const values = cats.map(() => Math.floor(10 + r2() * 40));
        return { cats, values };
      })();

      const defectReasons = (() => {
        const r3 = seededRand(17);
        const reasons = [
          { name: 'Stitch Skipped', color: 'rgba(239,68,68,.85)' },
          { name: 'Stain', color: 'rgba(245,158,11,.85)' },
          { name: 'Shade Variation', color: 'rgba(14,165,233,.85)' },
          { name: 'Open Seam', color: 'rgba(34,197,94,.85)' },
          { name: 'Measurement Issue', color: 'rgba(148,163,184,.75)' },
        ];
        const values = reasons.map(() => Math.floor(6 + r3() * 22));
        return { reasons, values };
      })();

      return { lines, lineRows, summary, breakdownCategories, defectReasons };
    } catch (error) {
      console.error('buildDataBundle error:', error);
      return buildFallbackBundle();
    }
  };

  const buildFallbackBundle = () => {
    return {
      lines: ['Line-21'],
      lineRows: [{
        line: 'Line-21',
        loading: 1000,
        offloading: 950,
        wip: 50,
        target: 800,
        achieved: 950,
        efficiency: 98.0,
        breakdownMin: 10,
        shift: { day: 600, night: 350 },
        workforce: { activeEmployees: 100, presentEmployees: 95 },
      }],
      summary: {
        totalLoading: 26926,
        totalOffloading: 26385,
        totalWip: 541,
        defects: 48,
        defectVariancePct: 0,
        totalTarget: 17884,
        variance: 8501,
        variancePct: 47.5,
        achievementPct: 147.5,
        breakdownTimeMin: 120,
        efficiency: 98.0,
        activeLines: 12,
        totalActiveEmployees: 1220,
        totalPresentEmployees: 1148,
        attendancePct: 94.1,
      },
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
      },
    };
  };

  const applyFiltersToBundle = (bundle, filters) => {
    try {
      const { startDate, endDate, line, shift } = filters || {};
      const selectedLine = line && line !== 'All' ? line : null;

      const filteredLines = selectedLine ? bundle.lineRows.filter((x) => x.line === selectedLine) : bundle.lineRows.slice();

      const lineRows = filteredLines.map((row) => {
        if (shift === 'Day') {
          const ratio = row.shift.day / Math.max(1, row.shift.day + row.shift.night);
          return {
            ...row,
            offloading: Math.floor(row.offloading * ratio),
            loading: Math.floor(row.loading * ratio),
            wip: Math.floor(row.wip * ratio),
            achieved: Math.floor(row.achieved * ratio),
            target: Math.floor(row.target * ratio),
            breakdownMin: Math.floor(row.breakdownMin * 0.6),
            defects: Math.floor((row.defects || 0) * ratio),
            workforce: {
              activeEmployees: Math.floor(row.workforce.activeEmployees * 0.55),
              presentEmployees: Math.floor(row.workforce.presentEmployees * 0.55),
            },
          };
        }
        if (shift === 'Night') {
          const ratio = row.shift.night / Math.max(1, row.shift.day + row.shift.night);
          return {
            ...row,
            offloading: Math.floor(row.offloading * ratio),
            loading: Math.floor(row.loading * ratio),
            wip: Math.floor(row.wip * ratio),
            achieved: Math.floor(row.achieved * ratio),
            target: Math.floor(row.target * ratio),
            breakdownMin: Math.floor(row.breakdownMin * 0.4),
            defects: Math.floor((row.defects || 0) * ratio),
            workforce: {
              activeEmployees: Math.floor(row.workforce.activeEmployees * 0.45),
              presentEmployees: Math.floor(row.workforce.presentEmployees * 0.45),
            },
          };
        }
        return { ...row, defects: row.defects || 0 };
      });

      const sum = (arr) => arr.reduce((a, b) => a + b, 0);

      const summary = (() => {
        const totalLoading = sum(lineRows.map((x) => x.loading));
        const totalOffloading = sum(lineRows.map((x) => x.offloading));
        const totalWip = sum(lineRows.map((x) => x.wip));
        const totalTarget = sum(lineRows.map((x) => x.target));

        // Defects kept stable for UI; later comes from DB
        const defects = (bundle.summary && typeof bundle.summary.defects === 'number') ? bundle.summary.defects : 0;
        const defectVariancePct = 0;

        const variance = totalOffloading - totalTarget;
        const variancePct = totalTarget > 0 ? (variance / totalTarget) * 100 : 0;
        const achievementPct = totalTarget > 0 ? (totalOffloading / totalTarget) * 100 : 0;
        const breakdownTimeMin = sum(lineRows.map((x) => x.breakdownMin));
        const efficiency = Math.round((sum(lineRows.map((x) => x.efficiency)) / lineRows.length) * 10) / 10;
        const activeLines = lineRows.length;

        const totalActiveEmployees = sum(lineRows.map((x) => (x.workforce && x.workforce.activeEmployees) ? x.workforce.activeEmployees : 0));
        const totalPresentEmployees = sum(lineRows.map((x) => (x.workforce && x.workforce.presentEmployees) ? x.workforce.presentEmployees : 0));
        const attendancePct = totalActiveEmployees > 0 ? (totalPresentEmployees / totalActiveEmployees) * 100 : 0;

        return {
          totalLoading,
          totalOffloading,
          totalWip,
          defects,
          defectVariancePct,
          totalTarget,
          variance,
          variancePct,
          achievementPct,
          breakdownTimeMin,
          efficiency,
          activeLines,
          startDate,
          endDate,
          totalActiveEmployees,
          totalPresentEmployees,
          attendancePct,
        };
      })();

      const makeSpark = (seedBase) => {
        const r = seededRand(seedBase);
        return Array.from({ length: 14 }).map(() => Math.floor(30 + r() * 70));
      };

      const summaryCards = [
        { key: 'totalLoading', title: 'Total Loading', value: window.Formatters.formatNumber(summary.totalLoading), iconClass: 'icon-boxes', tone: 'neutral', footnote: 'Pieces loaded', spark: makeSpark(1) },
        { key: 'totalOffloading', title: 'Total Offloading', value: window.Formatters.formatNumber(summary.totalOffloading), iconClass: 'icon-package-check', tone: 'neutral', footnote: 'Pieces offloaded', spark: makeSpark(2) },
        { key: 'totalWip', title: 'Total WIP', value: window.Formatters.formatNumber(summary.totalWip), iconClass: 'icon-box', tone: summary.totalWip > 0 ? 'warning' : 'neutral', footnote: 'In-line inventory', spark: makeSpark(3) },

        { key: 'totalActiveEmployees', title: 'Total Active Employees', value: window.Formatters.formatNumber(summary.totalActiveEmployees), iconClass: 'icon-users', tone: 'neutral', footnote: 'Scheduled workforce', spark: makeSpark(12) },
        { key: 'totalPresentEmployees', title: 'Present Employees', value: window.Formatters.formatNumber(summary.totalPresentEmployees), iconClass: 'icon-user-check', tone: summary.attendancePct >= 95 ? 'positive' : summary.attendancePct >= 90 ? 'neutral' : 'negative', footnote: 'Checked-in workforce', spark: makeSpark(13) },
        { key: 'attendancePct', title: 'Attendance %', value: window.Formatters.formatPercent((summary.attendancePct || 0) / 100), iconClass: 'icon-clipboard-check', tone: summary.attendancePct >= 95 ? 'positive' : summary.attendancePct >= 90 ? 'neutral' : 'negative', footnote: 'Present / active', spark: makeSpark(14) },

        { key: 'totalDefects', title: 'Total Defects', value: window.Formatters.formatNumber(summary.defects), iconClass: 'icon-bug', tone: summary.defects > 0 ? 'negative' : 'positive', footnote: 'Quality issues', spark: makeSpark(4) },
        { key: 'defectVariance', title: 'Defect Variance', value: `${summary.defectVariancePct.toFixed(1)}%`, iconClass: 'icon-shield-alert', tone: summary.defectVariancePct > 0 ? 'negative' : 'positive', footnote: 'Vs baseline', spark: makeSpark(5) },
        { key: 'totalTarget', title: 'Total Target', value: window.Formatters.formatNumber(summary.totalTarget), iconClass: 'icon-target', tone: 'neutral', footnote: 'Planned output', spark: makeSpark(6) },
        { key: 'variance', title: 'Variance', value: window.Formatters.formatVariance(summary.variance, summary.variancePct), iconClass: 'icon-trending-up', tone: summary.variance >= 0 ? 'positive' : 'negative', footnote: 'Actual vs target', spark: makeSpark(7) },
        { key: 'achievement', title: 'Achievement %', value: window.Formatters.formatPercent(summary.achievementPct / 100), iconClass: 'icon-award', tone: summary.achievementPct >= 100 ? 'positive' : 'negative', footnote: 'Attainment', spark: makeSpark(8) },
        { key: 'breakdown', title: 'Breakdown Time', value: window.Formatters.formatMinutes(summary.breakdownTimeMin), iconClass: 'icon-clock-alert', tone: summary.breakdownTimeMin > 120 ? 'negative' : 'neutral', footnote: 'Downtime minutes', spark: makeSpark(9) },
        { key: 'efficiency', title: 'Efficiency', value: window.Formatters.formatPercent((summary.efficiency || 0) / 100), iconClass: 'icon-gauge', tone: summary.efficiency >= 95 ? 'positive' : 'warning', footnote: 'Average line efficiency', spark: makeSpark(10) },
        { key: 'activeLines', title: 'Active Lines', value: window.Formatters.formatNumber(summary.activeLines), iconClass: 'icon-factory', tone: 'neutral', footnote: 'Running lines', spark: makeSpark(11) },
      ];

      const top3By = (key) => {
        const copy = lineRows.slice().sort((a, b) => b[key] - a[key]).slice(0, 3);
        return copy;
      };

      const performanceCards = [
        (() => {
          const top = top3By('loading');
          const total = sum(lineRows.map((x) => x.loading));
          const topTotal = sum(top.map((x) => x.loading));
          const pct = total > 0 ? (topTotal / total) * 100 : 0;
          return {
            key: 'loadingByLine',
            title: 'Loading by Line',
            subtitle: `${top.map((x) => x.line).join(', ')}`,
            iconClass: 'icon-boxes',
            pct: pct,
            tone: 'neutral',
            primaryLabel: 'Top 3 Loading',
            primaryValue: window.Formatters.formatNumber(topTotal),
            secondaryLabel: 'Total Loading',
            secondaryValue: window.Formatters.formatNumber(total),
            progress: { label: 'Share of total', pct: pct, valueText: window.Formatters.formatPercent(pct / 100) },
          };
        })(),
        (() => {
          const top = top3By('offloading');
          const total = sum(lineRows.map((x) => x.offloading));
          const topTotal = sum(top.map((x) => x.offloading));
          const pct = total > 0 ? (topTotal / total) * 100 : 0;
          const avgEff = Math.round((sum(top.map((x) => x.efficiency)) / Math.max(1, top.length)) * 10) / 10;
          return {
            key: 'offloadingByLine',
            title: 'Offloading by Line',
            subtitle: `${top.map((x) => x.line).join(', ')}`,
            iconClass: 'icon-package-check',
            pct: pct,
            tone: avgEff >= 95 ? 'positive' : 'warning',
            primaryLabel: 'Top 3 Offloading',
            primaryValue: window.Formatters.formatNumber(topTotal),
            secondaryLabel: 'Avg Efficiency',
            secondaryValue: window.Formatters.formatPercent(avgEff / 100),
            variance: { tone: avgEff >= 95 ? 'positive' : 'warning', text: `${avgEff.toFixed(1)}% efficiency`, note: 'Across top 3 lines' },
          };
        })(),
        (() => {
          const top = top3By('wip');
          const total = sum(lineRows.map((x) => x.wip));
          const topTotal = sum(top.map((x) => x.wip));
          const pct = total > 0 ? (topTotal / total) * 100 : 0;
          return {
            key: 'wipByLine',
            title: 'WIP by Line',
            subtitle: `${top.map((x) => x.line).join(', ')}`,
            iconClass: 'icon-box',
            pct: pct,
            tone: total > 0 ? 'warning' : 'neutral',
            primaryLabel: 'Top 3 WIP',
            primaryValue: window.Formatters.formatNumber(topTotal),
            secondaryLabel: 'Total WIP',
            secondaryValue: window.Formatters.formatNumber(total),
            progress: { label: 'Share of WIP', pct: pct, valueText: window.Formatters.formatPercent(pct / 100) },
          };
        })(),
        (() => {
          const achieved = sum(lineRows.map((x) => x.achieved));
          const target = sum(lineRows.map((x) => x.target));
          const pct = target > 0 ? (achieved / target) * 100 : 0;
          const variance = achieved - target;
          const tone = variance >= 0 ? 'positive' : 'negative';
          return {
            key: 'targetVsAch',
            title: 'Target vs Achievement',
            subtitle: selectedLine ? 'Selected line view' : 'All active lines',
            iconClass: 'icon-target',
            pct: pct,
            tone: pct >= 100 ? 'positive' : 'negative',
            primaryLabel: 'Achieved / Target',
            primaryValue: `${window.Formatters.formatNumber(achieved)} / ${window.Formatters.formatNumber(target)}`,
            secondaryLabel: 'Achievement %',
            secondaryValue: window.Formatters.formatPercent(pct / 100),
            variance: { tone, text: window.Formatters.formatVariance(variance, target > 0 ? (variance / target) * 100 : 0), note: 'Color-coded variance' },
          };
        })(),
      ];

      const charts = (() => {
        const labels = lineRows.map((x) => x.line);
        const loading = lineRows.map((x) => x.loading);
        const offloading = lineRows.map((x) => x.offloading);
        const wip = lineRows.map((x) => x.wip);

        const stackedLineBar = {
          data: {
            labels,
            datasets: [
              { label: 'Loading', data: loading, backgroundColor: 'rgba(14,165,233,.85)', borderRadius: 10 },
              { label: 'Offloading', data: offloading, backgroundColor: 'rgba(34,197,94,.85)', borderRadius: 10 },
              { label: 'WIP', data: wip, backgroundColor: 'rgba(245,158,11,.85)', borderRadius: 10 },
            ],
          },
          footer: 'Stacked bars highlight where WIP builds up relative to throughput.',
        };

        const shiftTotals = (() => {
          const day = sum(lineRows.map((x) => x.shift.day));
          const night = sum(lineRows.map((x) => x.shift.night));
          return { day, night };
        })();

        const shiftBar = {
          data: {
            labels: ['Day', 'Night'],
            datasets: [
              { label: 'Production', data: [shiftTotals.day, shiftTotals.night], backgroundColor: ['rgba(14,165,233,.85)', 'rgba(148,163,184,.75)'], borderRadius: 10 },
            ],
          },
          footer: 'Use this to spot imbalance between shifts quickly.',
        };

        const prodPie = (() => {
          const total = sum(offloading);
          const buckets = [
            { name: 'High output lines', color: 'rgba(34,197,94,.85)' },
            { name: 'Medium output lines', color: 'rgba(14,165,233,.85)' },
            { name: 'Low output lines', color: 'rgba(245,158,11,.85)' },
          ];
          const sorted = lineRows.slice().sort((a, b) => b.offloading - a.offloading);
          const top = sorted.slice(0, Math.max(1, Math.floor(sorted.length / 3)));
          const mid = sorted.slice(Math.floor(sorted.length / 3), Math.floor((sorted.length * 2) / 3));
          const low = sorted.slice(Math.floor((sorted.length * 2) / 3));
          const vals = [sum(top.map((x) => x.offloading)), sum(mid.map((x) => x.offloading)), sum(low.map((x) => x.offloading))];
          return {
            data: {
              labels: buckets.map((b) => b.name),
              datasets: [{ data: vals, backgroundColor: buckets.map((b) => b.color), borderColor: 'rgba(255,255,255,.08)', borderWidth: 1 }],
            },
            footer: total > 0 ? `Total offloading: ${window.Formatters.formatNumber(total)}` : 'No production in current filter.',
          };
        })();

        const defectReasonPie = (() => {
          const reasons = (bundle.defectReasons && bundle.defectReasons.reasons) ? bundle.defectReasons.reasons : [];
          const values = (bundle.defectReasons && bundle.defectReasons.values) ? bundle.defectReasons.values : [];
          const total = sum(values);
          return {
            data: {
              labels: reasons.map((r) => r.name),
              datasets: [{ data: values, backgroundColor: reasons.map((r) => r.color), borderColor: 'rgba(255,255,255,.08)', borderWidth: 1 }],
            },
            footer: total > 0 ? `Total defects (reason-split): ${window.Formatters.formatNumber(total)}` : 'No defects in current filter.',
          };
        })();

        const breakdownCategoryPie = (() => {
          const cats = bundle.breakdownCategories.cats;
          const values = bundle.breakdownCategories.values;
          return {
            data: {
              labels: cats.map((c) => c.name),
              datasets: [{ data: values, backgroundColor: cats.map((c) => c.color), borderColor: 'rgba(255,255,255,.08)', borderWidth: 1 }],
            },
            footer: 'Focus improvement initiatives on the largest slices.',
          };
        })();

        const breakdownLinePie = (() => {
          const sorted = lineRows.slice().sort((a, b) => b.breakdownMin - a.breakdownMin).slice(0, Math.min(6, lineRows.length));
          return {
            data: {
              labels: sorted.map((x) => x.line),
              datasets: [{
                data: sorted.map((x) => x.breakdownMin),
                backgroundColor: [
                  'rgba(239,68,68,.85)',
                  'rgba(245,158,11,.85)',
                  'rgba(14,165,233,.85)',
                  'rgba(34,197,94,.85)',
                  'rgba(148,163,184,.75)',
                  'rgba(168,85,247,.75)',
                ].slice(0, sorted.length),
                borderColor: 'rgba(255,255,255,.08)',
                borderWidth: 1,
              }],
            },
            footer: 'Top lines by downtime minutes (filtered view).',
          };
        })();

        return { stackedLineBar, shiftBar, prodPie, defectReasonPie, breakdownCategoryPie, breakdownLinePie };
      })();

      const lineComparisonRows = (() => {
        try {
          return lineRows.map((r) => {
            const achieved = Number(r.achieved) || 0;
            const target = Number(r.target) || 0;
            const variance = achieved - target;
            const variancePct = target > 0 ? (variance / target) * 100 : 0;
            const achievementPct = target > 0 ? (achieved / target) * 100 : 0;

            const defects = Number(r.defects) || 0;
            const defectsPct = achieved > 0 ? (defects / achieved) * 100 : 0;

            const activeEmployees = r.workforce && r.workforce.activeEmployees ? r.workforce.activeEmployees : 0;
            const presentEmployees = r.workforce && r.workforce.presentEmployees ? r.workforce.presentEmployees : 0;
            const attendancePct = activeEmployees > 0 ? (presentEmployees / activeEmployees) * 100 : 0;

            return {
              line: r.line,
              loading: r.loading,
              offloading: r.offloading,
              wip: r.wip,
              target: r.target,
              achievementPct,
              variance,
              variancePct,
              efficiency: r.efficiency,
              defects,
              defectsPct,
              breakdownMin: r.breakdownMin,
              activeEmployees,
              presentEmployees,
              attendancePct,
            };
          });
        } catch (error) {
          console.error('lineComparisonRows error:', error);
          return [];
        }
      })();

      const lineComparisonTotals = (() => {
        try {
          const loading = sum(lineComparisonRows.map((x) => x.loading));
          const offloading = sum(lineComparisonRows.map((x) => x.offloading));
          const wip = sum(lineComparisonRows.map((x) => x.wip));
          const target = sum(lineComparisonRows.map((x) => x.target));
          const defects = sum(lineComparisonRows.map((x) => x.defects));
          const breakdownMin = sum(lineComparisonRows.map((x) => x.breakdownMin));
          const activeEmployees = sum(lineComparisonRows.map((x) => x.activeEmployees));
          const presentEmployees = sum(lineComparisonRows.map((x) => x.presentEmployees));

          const achieved = offloading;
          const variance = achieved - target;
          const variancePct = target > 0 ? (variance / target) * 100 : 0;
          const achievementPct = target > 0 ? (achieved / target) * 100 : 0;

          const defectsPct = achieved > 0 ? (defects / achieved) * 100 : 0;

          const effAvg = lineComparisonRows.length
            ? Math.round((sum(lineComparisonRows.map((x) => (Number(x.efficiency) || 0))) / lineComparisonRows.length) * 10) / 10
            : 0;

          const attendancePct = activeEmployees > 0 ? (presentEmployees / activeEmployees) * 100 : 0;

          return {
            loading,
            offloading,
            wip,
            target,
            achieved,
            achievementPct,
            variance,
            variancePct,
            efficiency: effAvg,
            defects,
            defectsPct,
            breakdownMin,
            activeEmployees,
            presentEmployees,
            attendancePct,
          };
        } catch (error) {
          console.error('lineComparisonTotals error:', error);
          return {};
        }
      })();

      return { lineRows, summary, summaryCards, performanceCards, charts, lineComparisonRows, lineComparisonTotals };
    } catch (error) {
      console.error('applyFiltersToBundle error:', error);
      return buildFallbackBundle();
    }
  };

  return {
    getLineOptions,
    buildDataBundle,
    buildFallbackBundle,
    applyFiltersToBundle,
  };
})();