function SummaryCard({ title, value, iconClass, tone, footnote, spark }) {
  try {
    const toneChip = (() => {
      try {
        if (tone === 'positive') return { cls: 'badge-positive', icon: 'icon-trending-up' };
        if (tone === 'negative') return { cls: 'badge-negative', icon: 'icon-trending-down' };
        if (tone === 'warning') return { cls: 'badge-neutral', icon: 'icon-triangle-alert' };
        return { cls: 'badge-neutral', icon: 'icon-info' };
      } catch (error) {
        console.error('SummaryCard toneChip error:', error);
        return { cls: 'badge-neutral', icon: 'icon-info' };
      }
    })();

    const sparkPoints = (() => {
      try {
        if (!Array.isArray(spark) || spark.length < 2) return null;
        return spark;
      } catch (error) {
        console.error('SummaryCard sparkPoints error:', error);
        return null;
      }
    })();

    return (
      <div className="card p-5 hover-lift hover-outline" data-name="summary-card" data-file="components/SummaryCard.js">
        <div className="flex items-start justify-between gap-3" data-name="summary-top" data-file="components/SummaryCard.js">
          <div data-name="summary-left" data-file="components/SummaryCard.js">
            <div className="card-title" data-name="summary-title" data-file="components/SummaryCard.js">{title}</div>
            <div className="card-value" data-name="summary-value" data-file="components/SummaryCard.js">{value}</div>
          </div>

          <div className="flex flex-col items-end gap-2" data-name="summary-right" data-file="components/SummaryCard.js">
            <div className="w-11 h-11 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center" data-name="summary-icon-wrap" data-file="components/SummaryCard.js">
              <div className={`${iconClass} text-2xl text-[var(--primary-color)]`} data-name="summary-icon" data-file="components/SummaryCard.js"></div>
            </div>

            <span className={toneChip.cls} data-name="summary-badge" data-file="components/SummaryCard.js">
              <div className={`${toneChip.icon} text-xl`} data-name="summary-badge-icon" data-file="components/SummaryCard.js"></div>
              <span data-name="summary-badge-text" data-file="components/SummaryCard.js">{tone ? tone[0].toUpperCase() + tone.slice(1) : 'Neutral'}</span>
            </span>
          </div>
        </div>

        {footnote ? (
          <div className="mt-2 text-sm text-[var(--muted-text)]" data-name="summary-footnote" data-file="components/SummaryCard.js">{footnote}</div>
        ) : null}

        {sparkPoints ? (
          <div className="mt-4" data-name="summary-spark-wrap" data-file="components/SummaryCard.js">
            <div className="h-10 w-full rounded-xl bg-white/5 border border-white/10 p-2" data-name="spark-surface" data-file="components/SummaryCard.js">
              <svg viewBox="0 0 100 24" className="w-full h-full" preserveAspectRatio="none" data-name="spark-svg" data-file="components/SummaryCard.js">
                <path
                  d={window.Formatters.sparkPath(sparkPoints)}
                  fill="none"
                  stroke="rgba(14,165,233,.9)"
                  strokeWidth="2"
                  data-name="spark-path"
                  data-file="components/SummaryCard.js"
                />
                <path
                  d={window.Formatters.sparkAreaPath(sparkPoints)}
                  fill="rgba(14,165,233,.16)"
                  stroke="none"
                  data-name="spark-area"
                  data-file="components/SummaryCard.js"
                />
              </svg>
            </div>
          </div>
        ) : null}
      </div>
    );
  } catch (error) {
    console.error('SummaryCard component error:', error);
    return null;
  }
}