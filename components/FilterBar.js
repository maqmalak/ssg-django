function FilterBar({ filters, setFilters, onApply }) {
  try {
    const lineOptions = ['All'].concat(window.MockProductionData.getLineOptions());
    const shiftOptions = ['All', 'Day', 'Night'];

    const setField = (key, value) => {
      try {
        setFilters((prev) => ({ ...prev, [key]: value }));
      } catch (error) {
        console.error('FilterBar setField error:', error);
      }
    };

    return (
      <div className="card p-5 hover-outline" data-name="filterbar" data-file="components/FilterBar.js">
        <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4" data-name="filterbar-row" data-file="components/FilterBar.js">
          <div className="flex items-center gap-3" data-name="filterbar-titlewrap" data-file="components/FilterBar.js">
            <div className="w-11 h-11 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center" data-name="filterbar-iconwrap" data-file="components/FilterBar.js">
              <div className="icon-list-filter text-xl text-[var(--primary-color)]" data-name="filterbar-icon" data-file="components/FilterBar.js"></div>
            </div>
            <div data-name="filterbar-text" data-file="components/FilterBar.js">
              <div className="text-white font-semibold" data-name="filterbar-title" data-file="components/FilterBar.js">Top Filters</div>
              <div className="text-sm text-[var(--muted-text)]" data-name="filterbar-subtitle" data-file="components/FilterBar.js">
                Default is today, format <span className="text-white/80" data-name="date-format" data-file="components/FilterBar.js">dd/mm/yyyy</span>.
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-3 flex-1" data-name="filterbar-controls" data-file="components/FilterBar.js">
            <div data-name="start-date" data-file="components/FilterBar.js">
              <label className="text-xs text-[var(--muted-text)]" data-name="start-label" data-file="components/FilterBar.js">Start Date</label>
              <div className="mt-1" data-name="start-input-wrap" data-file="components/FilterBar.js">
                <input
                  type="date"
                  className="input"
                  value={filters.startDate}
                  onChange={(e) => setField('startDate', e.target.value)}
                  data-name="start-input"
                  data-file="components/FilterBar.js"
                />
                <div className="mt-1 text-xs text-[var(--muted-text)]" data-name="start-hint" data-file="components/FilterBar.js">
                  {window.Formatters.formatDateDDMMYYYY(filters.startDate)}
                </div>
              </div>
            </div>

            <div data-name="end-date" data-file="components/FilterBar.js">
              <label className="text-xs text-[var(--muted-text)]" data-name="end-label" data-file="components/FilterBar.js">End Date</label>
              <div className="mt-1" data-name="end-input-wrap" data-file="components/FilterBar.js">
                <input
                  type="date"
                  className="input"
                  value={filters.endDate}
                  onChange={(e) => setField('endDate', e.target.value)}
                  data-name="end-input"
                  data-file="components/FilterBar.js"
                />
                <div className="mt-1 text-xs text-[var(--muted-text)]" data-name="end-hint" data-file="components/FilterBar.js">
                  {window.Formatters.formatDateDDMMYYYY(filters.endDate)}
                </div>
              </div>
            </div>

            <div data-name="line-select" data-file="components/FilterBar.js">
              <label className="text-xs text-[var(--muted-text)]" data-name="line-label" data-file="components/FilterBar.js">Production Line</label>
              <div className="mt-1 relative" data-name="line-select-wrap" data-file="components/FilterBar.js">
                <select
                  className="select"
                  value={filters.line}
                  onChange={(e) => setField('line', e.target.value)}
                  data-name="line-select-input"
                  data-file="components/FilterBar.js"
                >
                  {lineOptions.map((l) => (
                    <option value={l} key={l} data-name="line-option" data-file="components/FilterBar.js">{l}</option>
                  ))}
                </select>
                <div className="pointer-events-none absolute right-3 top-[50%] -translate-y-1/2" data-name="line-caret" data-file="components/FilterBar.js">
                  <div className="icon-chevron-down text-xl text-white/70" data-name="line-caret-icon" data-file="components/FilterBar.js"></div>
                </div>
              </div>
            </div>

            <div data-name="shift-select" data-file="components/FilterBar.js">
              <label className="text-xs text-[var(--muted-text)]" data-name="shift-label" data-file="components/FilterBar.js">Shift</label>
              <div className="mt-1 relative" data-name="shift-select-wrap" data-file="components/FilterBar.js">
                <select
                  className="select"
                  value={filters.shift}
                  onChange={(e) => setField('shift', e.target.value)}
                  data-name="shift-select-input"
                  data-file="components/FilterBar.js"
                >
                  {shiftOptions.map((s) => (
                    <option value={s} key={s} data-name="shift-option" data-file="components/FilterBar.js">{s}</option>
                  ))}
                </select>
                <div className="pointer-events-none absolute right-3 top-[50%] -translate-y-1/2" data-name="shift-caret" data-file="components/FilterBar.js">
                  <div className="icon-chevron-down text-xl text-white/70" data-name="shift-caret-icon" data-file="components/FilterBar.js"></div>
                </div>
              </div>
            </div>

            <div className="flex items-end" data-name="apply-wrap" data-file="components/FilterBar.js">
              <button
                className="btn-primary w-full"
                onClick={onApply}
                data-name="apply-btn"
                data-file="components/FilterBar.js"
              >
                <div className="icon-list-filter text-xl text-white" data-name="apply-icon" data-file="components/FilterBar.js"></div>
                <span data-name="apply-text" data-file="components/FilterBar.js">Apply Filters</span>
              </button>
            </div>
          </div>
        </div>

        <div className="mt-4 subtle-divider" data-name="filterbar-divider" data-file="components/FilterBar.js"></div>

        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3" data-name="filterbar-extras" data-file="components/FilterBar.js">
          <div className="card px-4 py-3 bg-white/3 border border-white/10 rounded-2xl shadow-none" data-name="hint-1" data-file="components/FilterBar.js">
            <div className="flex items-center gap-3" data-name="hint-1-row" data-file="components/FilterBar.js">
              <div className="w-10 h-10 rounded-xl bg-[rgba(14,165,233,.12)] border border-[rgba(14,165,233,.25)] flex items-center justify-center" data-name="hint-1-iconwrap" data-file="components/FilterBar.js">
                <div className="icon-calendar-days text-xl text-[rgba(147,197,253,1)]" data-name="hint-1-icon" data-file="components/FilterBar.js"></div>
              </div>
              <div data-name="hint-1-text" data-file="components/FilterBar.js">
                <div className="text-sm font-semibold text-white" data-name="hint-1-title" data-file="components/FilterBar.js">Today is default</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="hint-1-desc" data-file="components/FilterBar.js">Pick dates to review historical shifts.</div>
              </div>
            </div>
          </div>

          <div className="card px-4 py-3 bg-white/3 border border-white/10 rounded-2xl shadow-none" data-name="hint-2" data-file="components/FilterBar.js">
            <div className="flex items-center gap-3" data-name="hint-2-row" data-file="components/FilterBar.js">
              <div className="w-10 h-10 rounded-xl bg-[rgba(34,197,94,.12)] border border-[rgba(34,197,94,.25)] flex items-center justify-center" data-name="hint-2-iconwrap" data-file="components/FilterBar.js">
                <div className="icon-sparkles text-xl text-[rgb(134_239_172)]" data-name="hint-2-icon" data-file="components/FilterBar.js"></div>
              </div>
              <div data-name="hint-2-text" data-file="components/FilterBar.js">
                <div className="text-sm font-semibold text-white" data-name="hint-2-title" data-file="components/FilterBar.js">Variance colors</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="hint-2-desc" data-file="components/FilterBar.js">Green is positive, red is negative.</div>
              </div>
            </div>
          </div>

          <div className="card px-4 py-3 bg-white/3 border border-white/10 rounded-2xl shadow-none" data-name="hint-3" data-file="components/FilterBar.js">
            <div className="flex items-center gap-3" data-name="hint-3-row" data-file="components/FilterBar.js">
              <div className="w-10 h-10 rounded-xl bg-[rgba(245,158,11,.12)] border border-[rgba(245,158,11,.25)] flex items-center justify-center" data-name="hint-3-iconwrap" data-file="components/FilterBar.js">
                <div className="icon-mouse-pointer-click text-xl text-[rgba(253,230,138,1)]" data-name="hint-3-icon" data-file="components/FilterBar.js"></div>
              </div>
              <div data-name="hint-3-text" data-file="components/FilterBar.js">
                <div className="text-sm font-semibold text-white" data-name="hint-3-title" data-file="components/FilterBar.js">Fast drill-down</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="hint-3-desc" data-file="components/FilterBar.js">Use line/shift filters to focus quickly.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  } catch (error) {
    console.error('FilterBar component error:', error);
    return null;
  }
}