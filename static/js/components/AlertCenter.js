function AlertCenter({ items, onDismiss }) {
  try {
    const toneStyles = (type) => {
      if (type === 'success') return { wrap: 'bg-[rgba(34,197,94,.12)] border-[rgba(34,197,94,.25)]', icon: 'icon-circle-check text-[rgb(134_239_172)]' };
      if (type === 'error') return { wrap: 'bg-[rgba(239,68,68,.12)] border-[rgba(239,68,68,.25)]', icon: 'icon-circle-alert text-[rgb(254_202_202)]' };
      if (type === 'info') return { wrap: 'bg-[rgba(14,165,233,.12)] border-[rgba(14,165,233,.25)]', icon: 'icon-circle-help text-[rgba(147,197,253,1)]' };
      return { wrap: 'bg-[rgba(148,163,184,.12)] border-[rgba(148,163,184,.22)]', icon: 'icon-info text-white/80' };
    };

    return (
      <div className="fixed bottom-4 right-4 z-50 w-[min(420px,calc(100vw-2rem))] space-y-2" data-name="alert-center" data-file="components/AlertCenter.js">
        {items.map((t) => {
          const s = toneStyles(t.type);
          return (
            <div key={t.id} className={`card px-4 py-3 border ${s.wrap}`} data-name="alert-item" data-file="components/AlertCenter.js">
              <div className="flex items-start gap-3" data-name="alert-row" data-file="components/AlertCenter.js">
                <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center border border-white/10" data-name="alert-icon-wrap" data-file="components/AlertCenter.js">
                  <div className={`${s.icon} text-xl`} data-name="alert-icon" data-file="components/AlertCenter.js"></div>
                </div>
                <div className="flex-1 min-w-0" data-name="alert-content" data-file="components/AlertCenter.js">
                  <div className="flex items-center justify-between gap-2" data-name="alert-head" data-file="components/AlertCenter.js">
                    <div className="text-sm font-semibold text-white" data-name="alert-title" data-file="components/AlertCenter.js">
                      {t.title || 'Notice'}
                    </div>
                    <button
                      className="btn-ghost px-2 py-1 rounded-lg"
                      onClick={() => onDismiss(t.id)}
                      data-name="alert-close"
                      data-file="components/AlertCenter.js"
                    >
                      <div className="icon-x text-xl text-white" data-name="alert-close-icon" data-file="components/AlertCenter.js"></div>
                    </button>
                  </div>
                  {t.message ? (
                    <div className="mt-1 text-sm text-[var(--muted-text)] leading-relaxed" data-name="alert-message" data-file="components/AlertCenter.js">
                      {t.message}
                    </div>
                  ) : null}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    );
  } catch (error) {
    console.error('AlertCenter component error:', error);
    return null;
  }
}