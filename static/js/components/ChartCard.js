function ChartCard({ title, subtitle, chartType, chartKey, chartData }) {
  try {
    const canvasRef = React.useRef(null);
    const chartRef = React.useRef(null);

    const getCommonOptions = () => {
      try {
        const grid = 'rgba(148,163,184,.18)';
        const ticks = 'rgba(226,232,240,.75)';
        return {
          responsive: true,
          maintainAspectRatio: false,
          animation: { duration: 450 },
          plugins: { legend: { display: false }, tooltip: { enabled: true } },
          scales: {
            x: {
              stacked: chartKey === 'stackedLineBar',
              grid: { color: grid },
              ticks: { color: ticks },
            },
            y: {
              stacked: chartKey === 'stackedLineBar',
              grid: { color: grid },
              ticks: { color: ticks },
            },
          },
        };
      } catch (error) {
        console.error('ChartCard getCommonOptions error:', error);
        return { responsive: true };
      }
    };

    React.useEffect(() => {
      try {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        if (chartRef.current) {
          chartRef.current.destroy();
          chartRef.current = null;
        }

        const config = (() => {
          try {
            if (chartType === 'doughnut') {
              return {
                type: 'doughnut',
                data: chartData.data,
                options: {
                  responsive: true,
                  maintainAspectRatio: false,
                  cutout: '62%',
                  plugins: { legend: { display: false } },
                },
              };
            }

            // shiftBar should be horizontal
            if (chartKey === 'shiftBar') {
              return {
                type: 'bar',
                data: chartData.data,
                options: {
                  ...getCommonOptions(),
                  indexAxis: 'y',
                  scales: {
                    x: { grid: { color: 'rgba(148,163,184,.18)' }, ticks: { color: 'rgba(226,232,240,.75)' } },
                    y: { grid: { color: 'rgba(148,163,184,.10)' }, ticks: { color: 'rgba(226,232,240,.75)' } },
                  },
                },
              };
            }

            return {
              type: 'bar',
              data: chartData.data,
              options: getCommonOptions(),
            };
          } catch (error) {
            console.error('ChartCard config error:', error);
            return { type: 'bar', data: { labels: [], datasets: [] }, options: { responsive: true } };
          }
        })();

        chartRef.current = new ChartJS(ctx, config);
      } catch (error) {
        console.error('ChartCard render error:', error);
      }

      return () => {
        try {
          if (chartRef.current) {
            chartRef.current.destroy();
            chartRef.current = null;
          }
        } catch (error) {
          console.error('ChartCard cleanup error:', error);
        }
      };
    }, [chartType, chartKey, chartData]);

    return (
      <div className="card p-5 hover-outline" data-name="chart-card" data-file="components/ChartCard.js">
        <div className="flex items-start justify-between gap-3" data-name="chart-head" data-file="components/ChartCard.js">
          <div data-name="chart-left" data-file="components/ChartCard.js">
            <div className="text-white font-semibold" data-name="chart-title" data-file="components/ChartCard.js">{title}</div>
            <div className="text-sm text-[var(--muted-text)]" data-name="chart-subtitle" data-file="components/ChartCard.js">{subtitle}</div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center" data-name="chart-icon-wrap" data-file="components/ChartCard.js">
            <div className={`${chartType === 'doughnut' ? 'icon-chart-pie' : 'icon-chart-bar'} text-xl text-[var(--primary-color)]`} data-name="chart-icon" data-file="components/ChartCard.js"></div>
          </div>
        </div>

        <div className="mt-4 h-[280px] rounded-2xl bg-white/3 border border-white/10 p-3" data-name="chart-canvas-wrap" data-file="components/ChartCard.js">
          <canvas ref={canvasRef} data-name="chart-canvas" data-file="components/ChartCard.js"></canvas>
        </div>

        {chartData && chartData.footer ? (
          <div className="mt-3 text-sm text-[var(--muted-text)]" data-name="chart-footer" data-file="components/ChartCard.js">
            {chartData.footer}
          </div>
        ) : null}
      </div>
    );
  } catch (error) {
    console.error('ChartCard component error:', error);
    return null;
  }
}