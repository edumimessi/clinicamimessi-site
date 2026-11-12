(function () {
  'use strict';
  const toggle = document.getElementById('hamburger');
  const links = document.getElementById('navLinks');
  if (!toggle || !links) return;

  const mobile = window.matchMedia('(max-width: 1200px)');
  const dropdowns = Array.from(links.querySelectorAll('.dropdown'));
  function closeDropdowns() {
    dropdowns.forEach(function (item) {
      item.classList.remove('open');
      item.querySelector('.dropdown-toggle').setAttribute('aria-expanded', 'false');
    });
  }
  function closeMenu() {
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    closeDropdowns();
  }
  toggle.addEventListener('click', function () {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    if (!open) closeDropdowns();
  });
  dropdowns.forEach(function (item) {
    const button = item.querySelector('.dropdown-toggle');
    button.addEventListener('click', function () {
      const open = !item.classList.contains('open');
      closeDropdowns();
      item.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
    });
  });
  links.addEventListener('click', function (event) {
    if (event.target.closest('a') && mobile.matches) closeMenu();
  });
  document.addEventListener('click', function (event) {
    if (!event.target.closest('.navbar')) closeMenu();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    const openDropdown = dropdowns.find(function (item) { return item.classList.contains('open'); });
    if (openDropdown) {
      closeDropdowns();
      openDropdown.querySelector('.dropdown-toggle').focus();
    } else if (links.classList.contains('open')) {
      closeMenu();
      toggle.focus();
    }
  });
  mobile.addEventListener('change', closeMenu);
})();
