// Theme: dark by default; a saved choice wins. Loaded (blocking) in <head> so there's no flash.
(function () {
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  root.setAttribute('data-theme', saved === 'light' ? 'light' : 'dark');

  function next() { return root.getAttribute('data-theme') === 'light' ? 'dark' : 'light'; }

  // label names the theme a click switches to
  function label() {
    var n = next();
    document.querySelectorAll('.theme-toggle').forEach(function (btn) {
      btn.querySelector('.tt-label').textContent = n;
      btn.setAttribute('title', 'Switch to ' + n + ' theme');
      btn.setAttribute('aria-label', 'Switch to ' + n + ' theme');
    });
  }

  // delegated, so it works no matter when the header is parsed
  document.addEventListener('click', function (e) {
    if (!e.target.closest || !e.target.closest('.theme-toggle')) return;
    var theme = next();
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem('theme', theme); } catch (err) {}
    label();
    document.dispatchEvent(new CustomEvent('themechange', { detail: theme }));
  });

  document.addEventListener('DOMContentLoaded', label);
})();
