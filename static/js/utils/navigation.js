window.AppNav = (function () {
  const isHome = () => {
    try {
      const p = window.location.pathname || '';
      return p.endsWith('/') || p.endsWith('/index.html') || p.endsWith('index.html') || !p.includes('.html');
    } catch (error) {
      console.error('isHome error:', error);
      return true;
    }
  };

  const navigateToSection = (sectionId) => {
    try {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      } else {
        const target = isHome() ? `#${sectionId}` : `index.html#${sectionId}`;
        window.location.href = target;
      }
    } catch (error) {
      console.error('navigateToSection error:', error);
    }
  };

  return { navigateToSection };
})();