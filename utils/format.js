window.Formatters = (function () {
  const safeNumber = (n) => {
    try {
      const x = Number(n);
      return Number.isFinite(x) ? x : 0;
    } catch (error) {
      console.error('safeNumber error:', error);
      return 0;
    }
  };

  const formatNumber = (n) => {
    try {
      return new Intl.NumberFormat('en-US').format(safeNumber(n));
    } catch (error) {
      console.error('formatNumber error:', error);
      return String(n);
    }
  };

  const formatPercent = (p) => {
    try {
      const v = safeNumber(p) * 100;
      return `${v.toFixed(1)}%`;
    } catch (error) {
      console.error('formatPercent error:', error);
      return `${p}%`;
    }
  };

  const formatMinutes = (m) => {
    try {
      return `${formatNumber(m)} min`;
    } catch (error) {
      console.error('formatMinutes error:', error);
      return `${m} min`;
    }
  };

  const formatDateDDMMYYYY = (isoDate) => {
    try {
      if (!isoDate) return '--/--/----';
      const d = new Date(isoDate);
      if (Number.isNaN(d.getTime())) return '--/--/----';
      const dd = String(d.getDate()).padStart(2, '0');
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const yyyy = String(d.getFullYear());
      return `${dd}/${mm}/${yyyy}`;
    } catch (error) {
      console.error('formatDateDDMMYYYY error:', error);
      return '--/--/----';
    }
  };

  const formatVariance = (variance, variancePct) => {
    try {
      const v = safeNumber(variance);
      const s = v >= 0 ? '+' : '−';
      const abs = Math.abs(v);
      const pct = safeNumber(variancePct);
      const pctSign = pct >= 0 ? '+' : '−';
      return `${s}${formatNumber(abs)} / ${pctSign}${Math.abs(pct).toFixed(1)}%`;
    } catch (error) {
      console.error('formatVariance error:', error);
      return String(variance);
    }
  };

  // Sparkline: accepts array of numbers 0..100 range or any positive range
  const normalize = (arr) => {
    try {
      const values = arr.map(safeNumber);
      const min = Math.min(...values);
      const max = Math.max(...values);
      const span = Math.max(1e-6, max - min);
      return values.map((v) => (v - min) / span);
    } catch (error) {
      console.error('normalize error:', error);
      return [];
    }
  };

  const sparkPath = (arr) => {
    try {
      const n = normalize(arr);
      if (!n.length) return 'M0,12 L100,12';
      const step = 100 / (n.length - 1);
      return n.map((v, i) => {
        const x = i * step;
        const y = 22 - v * 20;
        return `${i === 0 ? 'M' : 'L'}${x.toFixed(2)},${y.toFixed(2)}`;
      }).join(' ');
    } catch (error) {
      console.error('sparkPath error:', error);
      return 'M0,12 L100,12';
    }
  };

  const sparkAreaPath = (arr) => {
    try {
      const line = sparkPath(arr);
      return `${line} L100,24 L0,24 Z`;
    } catch (error) {
      console.error('sparkAreaPath error:', error);
      return 'M0,24 L100,24 Z';
    }
  };

  return {
    formatNumber,
    formatPercent,
    formatMinutes,
    formatDateDDMMYYYY,
    formatVariance,
    sparkPath,
    sparkAreaPath,
  };
})();