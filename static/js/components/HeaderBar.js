function HeaderBar({ title, subtitle, appliedFilters }) {
  try {
    const filterText = (() => {
      try {
        const sd = window.Formatters.formatDateDDMMYYYY(appliedFilters.startDate);
        const ed = window.Formatters.formatDateDDMMYYYY(appliedFilters.endDate);
        return `${sd} → ${ed}`;
      } catch (error) {
        console.error('HeaderBar filterText error:', error);
        return '';
      }
    })();

    return (
      <div className="flex flex-col gap-4" data-name="headerbar" data-file="components/HeaderBar.js">
        <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4" data-name="headerbar-row" data-file="components/HeaderBar.js">
          <div data-name="headerbar-left" data-file="components/HeaderBar.js">
            <div className="flex items-center gap-3" data-name="brand" data-file="components/HeaderBar.js">
              <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center shadow-[0_16px_45px_var(--shadow-color)]" data-name="brand-icon-wrap" data-file="components/HeaderBar.js">
                <div className="icon-shirt text-2xl text-[var(--primary-color)]" data-name="brand-icon" data-file="components/HeaderBar.js"></div>
              </div>
              <div data-name="brand-text" data-file="components/HeaderBar.js">
                <div className="text-white text-2xl font-semibold tracking-tight" data-name="brand-title" data-file="components/HeaderBar.js">{title}</div>
                <div className="text-sm text-[var(--muted-text)]" data-name="brand-subtitle" data-file="components/HeaderBar.js">{subtitle}</div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 justify-start lg:justify-end" data-name="headerbar-right" data-file="components/HeaderBar.js">
            <span className="chip" data-name="chip-date" data-file="components/HeaderBar.js">
              <div className="icon-calendar text-xl text-white/90" data-name="chip-date-icon" data-file="components/HeaderBar.js"></div>
              <span className="text-white/90" data-name="chip-date-text" data-file="components/HeaderBar.js">{filterText}</span>
            </span>
            <span className="chip" data-name="chip-line" data-file="components/HeaderBar.js">
              <div className="icon-panel-bottom text-xl text-white/90" data-name="chip-line-icon" data-file="components/HeaderBar.js"></div>
              <span className="text-white/90" data-name="chip-line-text" data-file="components/HeaderBar.js">Line: {appliedFilters.line}</span>
            </span>
            <span className="chip" data-name="chip-shift" data-file="components/HeaderBar.js">
              <div className="icon-sun text-xl text-white/90" data-name="chip-shift-icon" data-file="components/HeaderBar.js"></div>
              <span className="text-white/90" data-name="chip-shift-text" data-file="components/HeaderBar.js">Shift: {appliedFilters.shift}</span>
            </span>

            <button
              className="btn-primary"
              onClick={() => window.AppNav.navigateToSection('summary')}
              data-name="header-jump-summary"
              data-file="components/HeaderBar.js"
            >
              <div className="icon-arrow-down text-xl text-white" data-name="jump-icon" data-file="components/HeaderBar.js"></div>
              <span data-name="jump-text" data-file="components/HeaderBar.js">Summary</span>
            </button>
          </div>
        </div>
      </div>
    );
  } catch (error) {
    console.error('HeaderBar component error:', error);
    return null;
  }
}