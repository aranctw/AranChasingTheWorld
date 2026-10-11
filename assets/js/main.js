(function () {
  'use strict';
  var d = document;
  var header = d.getElementById('header');
  var toggle = d.querySelector('.nav-toggle');
  var nav = d.getElementById('site-nav');

  /* Menú móvil: el selector de idioma vive FUERA del menú y siempre se ve */
  function setMenu(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? toggle.getAttribute('data-close') : toggle.getAttribute('data-open'));
    d.body.classList.toggle('menu-open', open);
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); toggle.focus(); } });
    window.matchMedia('(min-width:960px)').addEventListener('change', function (m) { if (m.matches) setMenu(false); });
  }

  /* Sombra del header al hacer scroll */
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  /* Entrada suave (solo con JS) */
  var items = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  /* Formularios (Formspree) */
  d.querySelectorAll('form[data-ajax]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type="submit"]');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var label = btn.textContent;
      btn.disabled = true; btn.textContent = form.getAttribute('data-sending');
      status.className = 'form-status'; status.textContent = '';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('bad');
          status.textContent = form.getAttribute('data-ok'); status.className = 'form-status ok'; form.reset();
        })
        .catch(function () { status.textContent = form.getAttribute('data-err'); status.className = 'form-status err'; })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();
