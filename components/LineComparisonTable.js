function LineComparisonTable({ rows, totals }) {
  try {
    const { useMemo, useState } = React;

    const columns = useMemo(() => {
      try {
        return [
          { key: 'line', label: 'Line', align: 'left', type: 'text', iconClass: 'icon-factory' },
          { key: 'loading', label: 'Loading', align: 'right', type: 'number', iconClass: 'icon-boxes' },
          { key: 'offloading', label: 'Offloading', align: 'right', type: 'number', iconClass: 'icon-package-check' },
          { key: 'wip', label: 'WIP', align: 'right', type: 'number', iconClass: 'icon-box' },
          { key: 'target', label: 'Target', align: 'right', type: 'number', iconClass: 'icon-target' },
          { key: 'achievementPct', label: 'Achieve %', align: 'right', type: 'percent', iconClass: 'icon-award' },
          { key: 'variance', label: 'Variance', align: 'right', type: 'variance', iconClass: 'icon-trending-up' },
          { key: 'efficiency', label: 'Efficiency', align: 'right', type: 'percentValue', iconClass: 'icon-gauge' },
          { key: 'defects', label: 'Defects', align: 'right', type: 'number', iconClass: 'icon-bug' },
          { key: 'defectsPct', label: 'Defects %', align: 'right', type: 'percentValue', iconClass: 'icon-shield-alert' },
          { key: 'breakdownMin', label: 'Breakdown Time', align: 'right', type: 'minutes', iconClass: 'icon-clock-alert' },
          { key: 'activeEmployees', label: 'Active Employee', align: 'right', type: 'number', iconClass: 'icon-users' },
          { key: 'presentEmployees', label: 'Present Employee', align: 'right', type: 'number', iconClass: 'icon-user-check' },
          { key: 'attendancePct', label: 'Attendance %', align: 'right', type: 'percentValue', iconClass: 'icon-clipboard-check' },
        ];
      } catch (error) {
        console.error('LineComparisonTable columns error:', error);
        return [];
      }
    }, []);

    const [sort, setSort] = useState(() => ({ key: 'offloading', dir: 'desc' }));

    const toggleSort = (key) => {
      try {
        setSort((prev) => {
          if (prev.key === key) return { key, dir: prev.dir === 'asc' ? 'desc' : 'asc' };
          return { key, dir: 'desc' };
        });
      } catch (error) {
        console.error('LineComparisonTable toggleSort error:', error);
      }
    };

    const sortedRows = useMemo(() => {
      try {
        const copy = Array.isArray(rows) ? rows.slice() : [];
        const { key, dir } = sort || {};
        const factor = dir === 'asc' ? 1 : -1;

        const numVal = (v) => {
          const x = Number(v);
          return Number.isFinite(x) ? x : 0;
        };

        copy.sort((a, b) => {
          const av = a ? a[key] : undefined;
          const bv = b ? b[key] : undefined;
          if (typeof av === 'string' && typeof bv === 'string') return av.localeCompare(bv) * factor;
          return (numVal(av) - numVal(bv)) * factor;
        });

        return copy;
      } catch (error) {
        console.error('LineComparisonTable sortedRows error:', error);
        return Array.isArray(rows) ? rows : [];
      }
    }, [rows, sort]);

    const cellValue = (r, col) => {
      try {
        if (!r) return '--';
        const v = r[col.key];

        if (col.type === 'number') return window.Formatters.formatNumber(v);
        if (col.type === 'minutes') return window.Formatters.formatMinutes(v);
        if (col.type === 'percent') return window.Formatters.formatPercent((Number(v) || 0) / 100);
        if (col.type === 'percentValue') return window.Formatters.formatPercent((Number(v) || 0) / 100);
        if (col.type === 'variance') return window.Formatters.formatVariance(r.variance, r.variancePct);

        return String(v ?? '--');
      } catch (error) {
        console.error('LineComparisonTable cellValue error:', error);
        return '--';
      }
    };

    const toneFor = (r) => {
      try {
        const variance = Number(r.variance) || 0;
        const ach = Number(r.achievementPct) || 0;
        const att = Number(r.attendancePct) || 0;

        if (variance < 0 || ach < 95 || att < 90) return 'negative';
        if (ach >= 100 && att >= 95) return 'positive';
        return 'neutral';
      } catch (error) {
        console.error('LineComparisonTable toneFor error:', error);
        return 'neutral';
      }
    };

    const toneCls = (tone) => {
      if (tone === 'positive') return 'text-[rgb(134_239_172)]';
      if (tone === 'negative') return 'text-[rgb(254_202_202)]';
      return 'text-white/90';
    };

    const sortIconClass = (colKey) => {
      try {
        if (!sort || sort.key !== colKey) return 'icon-arrow-up-down';
        return sort.dir === 'asc' ? 'icon-arrow-up' : 'icon-arrow-down';
      } catch (error) {
        console.error('LineComparisonTable sortIcon error:', error);
        return 'icon-arrow-up-down';
      }
    };

    const totalsSafe = totals || {};

    return (
      <div className="card p-5" data-name="line-comparison" data-file="components/LineComparisonTable.js">
        <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4" data-name="head" data-file="components/LineComparisonTable.js">
          <div data-name="head-left" data-file="components/LineComparisonTable.js">
            <div className="text-white font-semibold" data-name="title" data-file="components/LineComparisonTable.js">Line-wise Comparison</div>
            <div className="text-sm text-[var(--muted-text)]" data-name="subtitle" data-file="components/LineComparisonTable.js">
              Compare loading, offloading, WIP, target, achievement, variance, efficiency, defects, downtime, and workforce attendance by production line.
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2" data-name="head-right" data-file="components/LineComparisonTable.js">
            <span className="chip" data-name="totals-chip-1" data-file="components/LineComparisonTable.js">
              <div className="icon-target text-xl text-white/90" data-name="totals-chip-1-icon" data-file="components/LineComparisonTable.js"></div>
              <span className="text-white/90" data-name="totals-chip-1-text" data-file="components/LineComparisonTable.js">
                Total Target: {window.Formatters.formatNumber(totalsSafe.target)}
              </span>
            </span>
            <span className="chip" data-name="totals-chip-2" data-file="components/LineComparisonTable.js">
              <div className="icon-award text-xl text-white/90" data-name="totals-chip-2-icon" data-file="components/LineComparisonTable.js"></div>
              <span className="text-white/90" data-name="totals-chip-2-text" data-file="components/LineComparisonTable.js">
                Achievement: {window.Formatters.formatPercent(((totalsSafe.achievementPct || 0) / 100))}
              </span>
            </span>
            <span className="chip" data-name="totals-chip-3" data-file="components/LineComparisonTable.js">
              <div className="icon-users text-xl text-white/90" data-name="totals-chip-3-icon" data-file="components/LineComparisonTable.js"></div>
              <span className="text-white/90" data-name="totals-chip-3-text" data-file="components/LineComparisonTable.js">
                Attendance: {window.Formatters.formatPercent(((totalsSafe.attendancePct || 0) / 100))}
              </span>
            </span>
          </div>
        </div>

        <div className="mt-4 subtle-divider" data-name="divider" data-file="components/LineComparisonTable.js"></div>

        <div className="mt-4 overflow-x-auto" data-name="table-wrap" data-file="components/LineComparisonTable.js">
          <table className="min-w-[1200px] w-full border-separate border-spacing-y-2" data-name="table" data-file="components/LineComparisonTable.js">
            <thead data-name="thead" data-file="components/LineComparisonTable.js">
              <tr data-name="head-row" data-file="components/LineComparisonTable.js">
                {columns.map((c) => (
                  <th
                    key={c.key}
                    className={`text-xs font-semibold text-[var(--muted-text)] px-3 py-2 ${c.align === 'right' ? 'text-right' : 'text-left'}`}
                    data-name="th"
                    data-file="components/LineComparisonTable.js"
                  >
                    <button
                      className="inline-flex items-center gap-2 hover:text-white transition hover:translate-y-[-1px]"
                      onClick={() => toggleSort(c.key)}
                      data-name="th-btn"
                      data-file="components/LineComparisonTable.js"
                    >
                      <div className={`${c.iconClass} text-xl text-white/70`} data-name="th-icon" data-file="components/LineComparisonTable.js"></div>
                      <span data-name="th-label" data-file="components/LineComparisonTable.js">{c.label}</span>
                      <div className={`${sortIconClass(c.key)} text-xl text-white/60`} data-name="th-sort" data-file="components/LineComparisonTable.js"></div>
                    </button>
                  </th>
                ))}
              </tr>
            </thead>

            <tbody data-name="tbody" data-file="components/LineComparisonTable.js">
              {sortedRows.map((r) => {
                const tone = toneFor(r);
                return (
                  <tr
                    key={r.line}
                    className="bg-white/5 border border-white/10 hover:bg-white/8 transition"
                    data-name="row"
                    data-file="components/LineComparisonTable.js"
                  >
                    {columns.map((c) => (
                      <td
                        key={c.key}
                        className={`px-3 py-3 text-sm ${c.align === 'right' ? 'text-right' : 'text-left'} ${
                          c.key === 'line'
                            ? 'font-semibold text-white'
                            : (c.key === 'variance' || c.key === 'achievementPct' || c.key === 'attendancePct')
                              ? toneCls(tone)
                              : 'text-white/90'
                        }`}
                        data-name="cell"
                        data-file="components/LineComparisonTable.js"
                      >
                        {cellValue(r, c)}
                      </td>
                    ))}
                  </tr>
                );
              })}

              <tr className="bg-white/10 border border-white/10" data-name="totals-row" data-file="components/LineComparisonTable.js">
                <td className="px-3 py-3 text-sm font-semibold text-white" data-name="totals-label" data-file="components/LineComparisonTable.js">Totals</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-loading" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.loading)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-offloading" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.offloading)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-wip" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.wip)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-target" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.target)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-ach" data-file="components/LineComparisonTable.js">{window.Formatters.formatPercent(((totalsSafe.achievementPct || 0) / 100))}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-var" data-file="components/LineComparisonTable.js">{window.Formatters.formatVariance(totalsSafe.variance, totalsSafe.variancePct)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-eff" data-file="components/LineComparisonTable.js">{window.Formatters.formatPercent(((totalsSafe.efficiency || 0) / 100))}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-def" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.defects)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-defpct" data-file="components/LineComparisonTable.js">{window.Formatters.formatPercent(((totalsSafe.defectsPct || 0) / 100))}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-break" data-file="components/LineComparisonTable.js">{window.Formatters.formatMinutes(totalsSafe.breakdownMin)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-ae" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.activeEmployees)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-pe" data-file="components/LineComparisonTable.js">{window.Formatters.formatNumber(totalsSafe.presentEmployees)}</td>
                <td className="px-3 py-3 text-sm text-right text-white/90" data-name="totals-att" data-file="components/LineComparisonTable.js">{window.Formatters.formatPercent(((totalsSafe.attendancePct || 0) / 100))}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="mt-3 text-xs text-[var(--muted-text)]" data-name="hint" data-file="components/LineComparisonTable.js">
          Tip: click any column header to sort. Variance, achievement, and attendance are color-coded for fast scanning.
        </div>
      </div>
    );
  } catch (error) {
    console.error('LineComparisonTable component error:', error);
    return null;
  }
}