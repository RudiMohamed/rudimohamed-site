// app.js — interactivity for rudi-website
(function () {
  'use strict';

  // Year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Mobile menu
  var menuBtn = document.getElementById('mobile-menu-btn');
  var nav = document.getElementById('primary-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Theme toggle (default dark; user choice persists in memory only)
  var themeToggle = document.getElementById('theme-toggle');
  var root = document.documentElement;
  var iconMoon = document.querySelector('.icon-moon');
  var iconSun = document.querySelector('.icon-sun');

  function setTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (iconMoon && iconSun) {
      iconMoon.style.display = theme === 'dark' ? 'none' : 'block';
      iconSun.style.display = theme === 'dark' ? 'block' : 'none';
    }
  }

  // Start dark (brand default)
  setTheme('dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var current = root.getAttribute('data-theme') || 'dark';
      setTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  // Scroll reveal
  if ('IntersectionObserver' in window) {
    var revealEls = document.querySelectorAll('[data-reveal]');
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(function (el, i) {
      el.style.transitionDelay = (i % 3) * 80 + 'ms';
      io.observe(el);
    });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function (el) {
      el.classList.add('is-visible');
    });
  }
})();
