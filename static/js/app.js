// Important: DO NOT remove this `ErrorBoundary` component.
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50" data-name="error" data-file="app.js">
          <div className="text-center" data-name="error-content" data-file="app.js">
            <h1 className="text-2xl font-bold text-gray-900 mb-4" data-name="error-title" data-file="app.js">Something went wrong</h1>
            <p className="text-gray-600 mb-4" data-name="error-desc" data-file="app.js">We're sorry, but something unexpected happened.</p>
            <button
              onClick={() => window.location.reload()}
              className="btn btn-black"
              data-name="error-reload"
              data-file="app.js"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  try {
    const { useMemo, useEffect, useState } = React;

    const todayISO = useMemo(() => {
      const d = new Date();
      d.setHours(0, 0, 0, 0);
      return d.toISOString().slice(0, 10);
    }, []);

    const [filters, setFilters] = useState(() => ({
      startDate: todayISO,
      endDate: todayISO,
      line: 'All',
      shift: 'All',
    }));

    const [appliedFilters, setAppliedFilters] = useState(filters);
    const [toastItems, setToastItems] = useState([]);

    const addToast = React.useCallback((item) => {
      try {
        setToastItems((prev) => {
          const next = prev.concat([{ ...item, id: `${Date.now()}-${Math.random()}` }]);
          return next.slice(-4);
        });
      } catch (error) {
        console.error('addToast error:', error);
      }
    }, []);

    const dismissToast = React.useCallback((id) => {
      try {
        setToastItems((prev) => prev.filter((t) => t.id !== id));
      } catch (error) {
        console.error('dismissToast error:', error);
      }
    }, []);

    const [dataBundle, setDataBundle] = useState(null);
    const [loading, setLoading] = useState(true);

    // Load data on mount and when filters change
    useEffect(() => {
      const loadData = async () => {
        try {
          setLoading(true);
          const data = await window.ApiData.applyFiltersToBundle(null, appliedFilters);
          setDataBundle(data);
        } catch (error) {
          console.error('Data loading error:', error);
          // Fallback to mock data
          setDataBundle(window.MockProductionData.buildDataBundle());
        } finally {
          setLoading(false);
        }
      };

      loadData();
    }, [appliedFilters]);

    const derived = useMemo(() => {
      try {
        if (!dataBundle) {
          return window.MockProductionData.buildFallbackBundle();
        }

        // For API data, the filtering is already done server-side
        // But we still need to apply the same transformations as the mock data
        return window.MockProductionData.applyFiltersToBundle(dataBundle, appliedFilters);
      } catch (error) {
        console.error('applyFiltersToBundle error:', error);
        return window.MockProductionData.buildFallbackBundle();
      }
    }, [dataBundle, appliedFilters]);

    useEffect(() => {
      try {
        const hash = window.location.hash ? window.location.hash.replace('#', '') : '';
        if (!hash) return;
        const el = document.getElementById(hash);
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } catch (error) {
        console.error('hash scroll error:', error);
      }
    }, []);

    const onApplyFilters = () => {
      try {
        const { startDate, endDate } = filters;
        if (!startDate || !endDate) {
          addToast({ type: 'error', title: 'Missing dates', message: 'Please select both a start date and an end date.' });
          return;
        }
        if (new Date(startDate) > new Date(endDate)) {
          addToast({ type: 'error', title: 'Date range invalid', message: 'Start date cannot be after end date.' });
          return;
        }
        setAppliedFilters(filters);
        addToast({ type: 'success', title: 'Filters applied', message: 'Dashboard has been refreshed.' });
      } catch (error) {
        console.error('onApplyFilters error:', error);
      }
    };

    const pageTitle = 'Hanger Line Apparel';
    const subtitle = 'Production Dashboard';

    return (
      <div className="app-shell" data-name="app-shell" data-file="app.js">
        <div className="max-w-7xl mx-auto px-4 py-6" data-name="container" data-file="app.js">
          <HeaderBar
            title={pageTitle}
            subtitle={subtitle}
            appliedFilters={appliedFilters}
            data-file="app.js"
          />

          <div className="mt-5" data-name="filters-wrap" data-file="app.js">
            <FilterBar
              filters={filters}
              setFilters={setFilters}
              onApply={onApplyFilters}
              data-file="app.js"
            />
          </div>

          <div className="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-4" data-name="tiles" data-file="app.js">
            <div className="lg:col-span-12" data-name="dashboard-tile" data-file="app.js">
              <div className="tile p-5 hover-lift hover-outline" data-name="tile-inner" data-file="app.js">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4" data-name="tile-top" data-file="app.js">
                  <div data-name="tile-copy" data-file="app.js">
                    <div className="flex items-center gap-3" data-name="tile-heading" data-file="app.js">
                      <div className="w-11 h-11 rounded-2xl bg-[var(--primary-color)] flex items-center justify-center shadow-[0_14px_40px_rgba(14,165,233,.35)]" data-name="tile-icon-wrap" data-file="app.js">
                        <div className="icon-chart-bar text-xl text-white" data-name="tile-icon" data-file="app.js"></div>
                      </div>
                      <div data-name="tile-text" data-file="app.js">
                        <div className="text-white text-lg font-semibold" data-name="tile-title" data-file="app.js">Production Snapshot</div>
                        <div className="text-sm text-[var(--muted-text)]" data-name="tile-subtitle" data-file="app.js">
                          Today-focused overview with apparel-ready widgets and high-contrast indicators.
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2" data-name="tile-chips" data-file="app.js">
                    <span className="chip" data-name="chip-lines" data-file="app.js">
                      <div className="icon-factory text-xl text-white/90" data-name="chip-icon-1" data-file="app.js"></div>
                      <span className="text-white/90" data-name="chip-text-1" data-file="app.js">{derived.summary.activeLines} Active Lines</span>
                    </span>
                    <span className="chip" data-name="chip-eff" data-file="app.js">
                      <div className="icon-gauge text-xl text-white/90" data-name="chip-icon-2" data-file="app.js"></div>
                      <span className="text-white/90" data-name="chip-text-2" data-file="app.js">{window.Formatters.formatPercent(derived.summary.efficiency / 100)} Efficiency</span>
                    </span>
                    <span className="chip" data-name="chip-breakdown" data-file="app.js">
                      <div className="icon-clock text-xl text-white/90" data-name="chip-icon-3" data-file="app.js"></div>
                      <span className="text-white/90" data-name="chip-text-3" data-file="app.js">{derived.summary.breakdownTimeMin} min Breakdown</span>
                    </span>
                    <span className="chip" data-name="chip-attendance" data-file="app.js">
                      <div className="icon-users text-xl text-white/90" data-name="chip-icon-4" data-file="app.js"></div>
                      <span className="text-white/90" data-name="chip-text-4" data-file="app.js">{window.Formatters.formatPercent((derived.summary.attendancePct || 0) / 100)} Attendance</span>
                    </span>
                  </div>
                </div>

                <div className="mt-4 subtle-divider" data-name="tile-divider" data-file="app.js"></div>

                <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4" data-name="tile-stats" data-file="app.js">
                  <SummaryCard
                    title="Variance"
                    value={window.Formatters.formatVariance(derived.summary.variance, derived.summary.variancePct)}
                    iconClass="icon-trending-up"
                    tone={derived.summary.variance >= 0 ? 'positive' : 'negative'}
                    footnote="Against total target"
                    data-file="app.js"
                  />
                  <SummaryCard
                    title="Attendance %"
                    value={window.Formatters.formatPercent((derived.summary.attendancePct || 0) / 100)}
                    iconClass="icon-users"
                    tone={(derived.summary.attendancePct || 0) >= 95 ? 'positive' : (derived.summary.attendancePct || 0) >= 90 ? 'neutral' : 'negative'}
                    footnote="Present vs active employees"
                    data-file="app.js"
                  />
                  <SummaryCard
                    title="Total WIP"
                    value={window.Formatters.formatNumber(derived.summary.totalWip)}
                    iconClass="icon-box"
                    tone={derived.summary.totalWip > 0 ? 'warning' : 'neutral'}
                    footnote="Work in progress"
                    data-file="app.js"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6" id="summary" data-name="summary-section" data-file="app.js">
            <div className="flex items-center justify-between gap-4 mb-3" data-name="summary-head" data-file="app.js">
              <div data-name="summary-left" data-file="app.js">
                <div className="text-white font-semibold" data-name="summary-title" data-file="app.js">Total Summary</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="summary-subtitle" data-file="app.js">Operations + workforce metrics designed for a clean, apparel-ready control room view.</div>
              </div>
              <a
                href="#analytics"
                onClick={(e) => { e.preventDefault(); window.AppNav.navigateToSection('analytics'); }}
                className="btn-ghost"
                data-name="jump-analytics"
                data-file="app.js"
              >
                <span data-name="jump-text" data-file="app.js">View Analytics</span>
                <div className="icon-arrow-right text-xl text-white" data-name="jump-icon" data-file="app.js"></div>
              </a>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4" data-name="summary-grid" data-file="app.js">
              {derived.summaryCards.map((c) => (
                <SummaryCard
                  key={c.key}
                  title={c.title}
                  value={c.value}
                  iconClass={c.iconClass}
                  tone={c.tone}
                  footnote={c.footnote}
                  spark={c.spark}
                  data-file="app.js"
                />
              ))}
            </div>
          </div>

          <div className="mt-8" id="linewise" data-name="linewise-section" data-file="app.js">
            <div className="flex items-end justify-between gap-4 mb-3" data-name="linewise-head" data-file="app.js">
              <div data-name="linewise-left" data-file="app.js">
                <div className="text-white font-semibold" data-name="linewise-title" data-file="app.js">Line-wise Performance</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="linewise-subtitle" data-file="app.js">Quick comparisons with progress, efficiency, and variance color coding.</div>
              </div>
              <div className="flex items-center gap-2" data-name="linewise-right" data-file="app.js">
                <span className="chip" data-name="chip-target" data-file="app.js">
                  <div className="icon-target text-xl text-white/90" data-name="chip-target-icon" data-file="app.js"></div>
                  <span className="text-white/90" data-name="chip-target-text" data-file="app.js">{window.Formatters.formatNumber(derived.summary.totalTarget)} Total Target</span>
                </span>
                <span className="chip" data-name="chip-load" data-file="app.js">
                  <div className="icon-boxes text-xl text-white/90" data-name="chip-load-icon" data-file="app.js"></div>
                  <span className="text-white/90" data-name="chip-load-text" data-file="app.js">{window.Formatters.formatNumber(derived.summary.totalLoading)} Loaded</span>
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4" data-name="linewise-grid" data-file="app.js">
              {derived.performanceCards.map((pc) => (
                <LinePerformanceCard key={pc.key} card={pc} data-file="app.js" />
              ))}
            </div>
          </div>

          <div className="mt-8" id="comparison" data-name="comparison-section" data-file="app.js">
            <div className="flex items-end justify-between gap-4 mb-3" data-name="comparison-head" data-file="app.js">
              <div data-name="comparison-left" data-file="app.js">
                <div className="text-white font-semibold" data-name="comparison-title" data-file="app.js">Line-wise Comparison</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="comparison-subtitle" data-file="app.js">
                  Total loading, offloading, WIP, target, achievement, variance, efficiency, defects, downtime, and attendance by line.
                </div>
              </div>
              <a
                href="#analytics"
                onClick={(e) => { e.preventDefault(); window.AppNav.navigateToSection('analytics'); }}
                className="btn-ghost"
                data-name="comparison-jump-analytics"
                data-file="app.js"
              >
                <span data-name="comparison-jump-text" data-file="app.js">Analytics</span>
                <div className="icon-arrow-right text-xl text-white" data-name="comparison-jump-icon" data-file="app.js"></div>
              </a>
            </div>

            <LineComparisonTable
              rows={derived.lineComparisonRows}
              totals={derived.lineComparisonTotals}
              data-file="app.js"
            />
          </div>

          <div className="mt-8" id="analytics" data-name="analytics-section" data-file="app.js">
            <div className="flex items-center justify-between gap-4 mb-3" data-name="analytics-head" data-file="app.js">
              <div data-name="analytics-left" data-file="app.js">
                <div className="text-white font-semibold" data-name="analytics-title" data-file="app.js">Visual Analytics</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="analytics-subtitle" data-file="app.js">Now includes defect reasons and breakdowns for better actionability.</div>
              </div>
              <button
                className="btn-ghost"
                onClick={() => { addToast({ type: 'info', title: 'Tip', message: 'Hover on charts to view exact values. Use filters to refresh instantly.' }); }}
                data-name="analytics-tip"
                data-file="app.js"
              >
                <div className="icon-circle-help text-xl text-white" data-name="analytics-tip-icon" data-file="app.js"></div>
                <span data-name="analytics-tip-text" data-file="app.js">How to read</span>
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4" data-name="charts-grid" data-file="app.js">
              <div className="lg:col-span-12" data-name="chart-1-wrap" data-file="app.js">
                <ChartCard
                  title="Loading / Offloading / WIP per Line"
                  subtitle="Stacked view to see throughput and WIP pressure."
                  chartType="bar"
                  chartKey="stackedLineBar"
                  chartData={derived.charts.stackedLineBar}
                  data-file="app.js"
                />
              </div>

              <div className="lg:col-span-6" data-name="chart-2-wrap" data-file="app.js">
                <ChartCard
                  title="Shift-wise Production"
                  subtitle="Day vs Night output comparison."
                  chartType="bar"
                  chartKey="shiftBar"
                  chartData={derived.charts.shiftBar}
                  data-file="app.js"
                />
              </div>

              <div className="lg:col-span-6" data-name="chart-3-wrap" data-file="app.js">
                <ChartCard
                  title="Production Distribution"
                  subtitle="Share by output bucket."
                  chartType="doughnut"
                  chartKey="prodPie"
                  chartData={derived.charts.prodPie}
                  data-file="app.js"
                />
              </div>

              <div className="lg:col-span-6" data-name="chart-4-wrap" data-file="app.js">
                <ChartCard
                  title="Defect Qty by Reason"
                  subtitle="Top quality reasons contributing to defects."
                  chartType="doughnut"
                  chartKey="defectReasonPie"
                  chartData={derived.charts.defectReasonPie}
                  data-file="app.js"
                />
              </div>

              <div className="lg:col-span-6" data-name="chart-5-wrap" data-file="app.js">
                <ChartCard
                  title="Breakdown by Category"
                  subtitle="Where time is going."
                  chartType="doughnut"
                  chartKey="breakdownCategoryPie"
                  chartData={derived.charts.breakdownCategoryPie}
                  data-file="app.js"
                />
              </div>

              <div className="lg:col-span-6" data-name="chart-6-wrap" data-file="app.js">
                <ChartCard
                  title="Breakdown by Line"
                  subtitle="Top contributing lines to downtime."
                  chartType="doughnut"
                  chartKey="breakdownLinePie"
                  chartData={derived.charts.breakdownLinePie}
                  data-file="app.js"
                />
              </div>
            </div>
          </div>

          <div className="mt-10 pb-10" data-name="footer-wrap" data-file="app.js">
            <div className="card px-5 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3 hover-outline" data-name="footer-card" data-file="app.js">
              <div className="text-sm text-[var(--muted-text)]" data-name="footer-left" data-file="app.js">
                <span className="text-white/90" data-name="footer-brand" data-file="app.js">Hanger Line Apparel</span>
                <span data-name="footer-sep" data-file="app.js"> · </span>
                <span data-name="footer-copy" data-file="app.js">© 2026 Production Dashboard</span>
              </div>
              <div className="flex items-center gap-2" data-name="footer-right" data-file="app.js">
                <span className="chip" data-name="footer-chip-1" data-file="app.js">
                  <div className="icon-shield text-xl text-white/90" data-name="footer-icon-1" data-file="app.js"></div>
                  <span className="text-white/90" data-name="footer-text-1" data-file="app.js">Data is illustrative</span>
                </span>
                <span className="chip" data-name="footer-chip-2" data-file="app.js">
                  <div className="icon-refresh-cw text-xl text-white/90" data-name="footer-icon-2" data-file="app.js"></div>
                  <span className="text-white/90" data-name="footer-text-2" data-file="app.js">Instant refresh</span>
                </span>
              </div>
            </div>
          </div>
        </div>

        <AlertCenter items={toastItems} onDismiss={dismissToast} data-file="app.js" />
      </div>
    );
  } catch (error) {
    console.error('App component error:', error);
    return null;
  }
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <ErrorBoundary>
    <App />
  </ErrorBoundary>
);
