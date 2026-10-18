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

  /* Carrusel de viajes (sin JS sigue siendo deslizable con el dedo) */
  d.querySelectorAll('.carousel').forEach(function (car) {
    var track = car.querySelector('.carousel-track');
    var slides = car.querySelectorAll('.trip-slide');
    var dots = car.querySelectorAll('.car-dot');
    var btns = car.querySelectorAll('.car-btn');
    if (!track || slides.length < 2) { var c0 = car.querySelector('.carousel-ctrl'); if (c0) c0.style.display = 'none'; return; }
    function index() { return Math.max(0, Math.min(slides.length - 1, Math.round(track.scrollLeft / track.clientWidth))); }
    function go(i) { track.scrollTo({ left: i * track.clientWidth }); }
    function update() {
      var i = index();
      dots.forEach(function (x, n) { x.setAttribute('aria-current', n === i ? 'true' : 'false'); });
      btns[0].disabled = i === 0; btns[1].disabled = i === slides.length - 1;
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { go(index() + parseInt(b.getAttribute('data-dir'), 10)); }); });
    dots.forEach(function (x, n) { x.addEventListener('click', function () { go(n); }); });
    track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', function () { go(index()); });
    /* Enlace directo #viaje-islandia / #viaje-colombia */
    function fromHash() { var m = location.hash.match(/^#viaje-(.+)$/); if (!m) return; slides.forEach(function (s, n) { if (s.id === 'viaje-' + m[1]) go(n); }); }
    fromHash(); window.addEventListener('hashchange', fromHash);
    update();
  });

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
