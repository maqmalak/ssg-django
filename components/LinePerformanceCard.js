function LinePerformanceCard({ card }) {
  try {
    const toneBadge = (tone) => {
      if (tone === 'positive') return 'badge-positive';
      if (tone === 'negative') return 'badge-negative';
      if (tone === 'warning') return 'badge-neutral';
      return 'badge-neutral';
    };

    const pct = (card.pct || 0);
    const pctSafe = Math.max(0, Math.min(100, pct));

    return (
      <div className="card p-5 hover-lift hover-outline" data-name="line-performance-card" data-file="components/LinePerformanceCard.js">
        <div className="flex items-start justify-between gap-3" data-name="lp-top" data-file="components/LinePerformanceCard.js">
          <div data-name="lp-left" data-file="components/LinePerformanceCard.js">
            <div className="flex items-center gap-3" data-name="lp-title-row" data-file="components/LinePerformanceCard.js">
              <div className="w-11 h-11 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center" data-name="lp-iconwrap" data-file="components/LinePerformanceCard.js">
                <div className={`${card.iconClass} text-2xl text-[var(--primary-color)]`} data-name="lp-icon" data-file="components/LinePerformanceCard.js"></div>
              </div>
              <div data-name="lp-titlewrap" data-file="components/LinePerformanceCard.js">
                <div className="text-white font-semibold" data-name="lp-title" data-file="components/LinePerformanceCard.js">{card.title}</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="lp-subtitle" data-file="components/LinePerformanceCard.js">{card.subtitle}</div>
              </div>
            </div>
          </div>

          <span className={`${toneBadge(card.tone)} whitespace-nowrap`} data-name="lp-badge" data-file="components/LinePerformanceCard.js">
            <div className="icon-activity text-xl" data-name="lp-badge-icon" data-file="components/LinePerformanceCard.js"></div>
            <span data-name="lp-badge-text" data-file="components/LinePerformanceCard.js">{window.Formatters.formatPercent(pct / 100)}</span>
          </span>
        </div>

        <div className="mt-4 grid grid-cols-2 gap-3" data-name="lp-stats" data-file="components/LinePerformanceCard.js">
          <div className="rounded-2xl bg-white/5 border border-white/10 p-3" data-name="lp-stat-1" data-file="components/LinePerformanceCard.js">
            <div className="text-xs text-[var(--muted-text)]" data-name="lp-stat-1-label" data-file="components/LinePerformanceCard.js">{card.primaryLabel}</div>
            <div className="text-lg font-semibold text-white mt-1" data-name="lp-stat-1-value" data-file="components/LinePerformanceCard.js">{card.primaryValue}</div>
          </div>
          <div className="rounded-2xl bg-white/5 border border-white/10 p-3" data-name="lp-stat-2" data-file="components/LinePerformanceCard.js">
            <div className="text-xs text-[var(--muted-text)]" data-name="lp-stat-2-label" data-file="components/LinePerformanceCard.js">{card.secondaryLabel}</div>
            <div className="text-lg font-semibold text-white mt-1" data-name="lp-stat-2-value" data-file="components/LinePerformanceCard.js">{card.secondaryValue}</div>
          </div>
        </div>

        {card.progress ? (
          <div className="mt-4" data-name="lp-progress" data-file="components/LinePerformanceCard.js">
            <div className="flex items-center justify-between text-xs text-[var(--muted-text)] mb-2" data-name="lp-progress-head" data-file="components/LinePerformanceCard.js">
              <span data-name="lp-progress-label" data-file="components/LinePerformanceCard.js">{card.progress.label}</span>
              <span className="text-white/80" data-name="lp-progress-value" data-file="components/LinePerformanceCard.js">{card.progress.valueText}</span>
            </div>
            <div className="progress-rail" data-name="lp-rail" data-file="components/LinePerformanceCard.js">
              <div className="progress-bar" style={{ width: `${Math.max(0, Math.min(100, card.progress.pct))}%` }} data-name="lp-bar" data-file="components/LinePerformanceCard.js"></div>
            </div>
          </div>
        ) : null}

        {card.variance ? (
          <div className="mt-4 flex flex-wrap items-center gap-2" data-name="lp-variance" data-file="components/LinePerformanceCard.js">
            <span className={`${card.variance.tone === 'positive' ? 'badge-positive' : card.variance.tone === 'negative' ? 'badge-negative' : 'badge-neutral'}`} data-name="lp-var-badge" data-file="components/LinePerformanceCard.js">
              <div className={`${card.variance.tone === 'positive' ? 'icon-trending-up' : card.variance.tone === 'negative' ? 'icon-trending-down' : 'icon-minus'} text-xl`} data-name="lp-var-icon" data-file="components/LinePerformanceCard.js"></div>
              <span data-name="lp-var-text" data-file="components/LinePerformanceCard.js">{card.variance.text}</span>
            </span>
            {card.variance.note ? (
              <span className="text-sm text-[var(--muted-text)]" data-name="lp-var-note" data-file="components/LinePerformanceCard.js">{card.variance.note}</span>
            ) : null}
          </div>
        ) : null}
      </div>
    );
  } catch (error) {
    console.error('LinePerformanceCard component error:', error);
    return null;
  }
}