/*
 * Podnikatelské profily: jazyk, světlý/tmavý režim a kopírování údajů.
 * Načítá se v <head>, aby se zvolený režim a jazyk uplatnily ještě před vykreslením.
 *
 * Jazyk (podle conceptual.cz):
 * - Volba jazyka v přepínači se zapamatuje (localStorage).
 * - Česká stránka (data-lang-auto) pošle návštěvníka na en/ nebo de/, když si ten jazyk
 *   dřív vybral, nebo při první návštěvě, když ho preferuje prohlížeč. Čeština, slovenština
 *   a ostatní jazyky zůstanou na češtině. Adresy en/ a de/ nepřesměrovávají nikdy.
 *
 * Režim: výchozí podle prohlížeče (prefers-color-scheme); přepínač nastaví
 * <html data-theme="light|dark"> a volbu si zapamatuje. <html data-vzhled> vždy nese
 * skutečně zobrazený režim (pro ikonu přepínače).
 */
(function () {
  'use strict';

  var root = document.documentElement;

  function nacti(klic) {
    try { return localStorage.getItem(klic); } catch (e) { return null; }
  }
  function uloz(klic, hodnota) {
    try {
      if (hodnota === null) localStorage.removeItem(klic);
      else localStorage.setItem(klic, hodnota);
    } catch (e) { /* úložiště blokované: volba platí jen pro tuto stránku */ }
  }

  // ---------- Světlý a tmavý režim ----------

  var tmavyProhlizec = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  var ulozenyRezim = nacti('vzhled');
  if (ulozenyRezim === 'light' || ulozenyRezim === 'dark') root.setAttribute('data-theme', ulozenyRezim);

  function zobrazenyRezim() {
    var t = root.getAttribute('data-theme');
    if (t === 'light' || t === 'dark') return t;
    return tmavyProhlizec && tmavyProhlizec.matches ? 'dark' : 'light';
  }
  function obnovIkonu() {
    var rezim = zobrazenyRezim();
    root.setAttribute('data-vzhled', rezim);
    var tlacitko = document.querySelector('.vzhled');
    if (tlacitko) {
      tlacitko.setAttribute('aria-pressed', rezim === 'dark' ? 'true' : 'false');
      tlacitko.setAttribute('title', tlacitko.getAttribute(rezim === 'dark' ? 'data-na-svetly' : 'data-na-tmavy'));
    }
  }
  obnovIkonu();
  if (tmavyProhlizec) {
    var zmena = function () { obnovIkonu(); };
    if (tmavyProhlizec.addEventListener) tmavyProhlizec.addEventListener('change', zmena);
    else if (tmavyProhlizec.addListener) tmavyProhlizec.addListener(zmena);
  }

  // ---------- Jazyk ----------

  var CESTY = { cs: '', en: 'en/', de: 'de/' };

  function jazykProhlizece() {
    var seznam = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    for (var i = 0; i < seznam.length; i++) {
      var hlavni = String(seznam[i]).toLowerCase().split('-')[0];
      if (hlavni === 'cs' || hlavni === 'sk') return 'cs';
      if (hlavni === 'en' || hlavni === 'de') return hlavni;
    }
    return 'cs';
  }

  if (root.hasAttribute('data-lang-auto') && !/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent)) {
    var ulozenyJazyk = nacti('jazyk');
    var jazyk = Object.prototype.hasOwnProperty.call(CESTY, ulozenyJazyk) ? ulozenyJazyk : jazykProhlizece();
    if (jazyk !== 'cs') {
      location.replace(CESTY[jazyk] + location.search + location.hash);
      return;
    }
  }

  // ---------- Kopírování ----------

  function zkopiruj(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (hotovo, chyba) {
      var pole = document.createElement('textarea');
      pole.value = text;
      pole.setAttribute('readonly', '');
      pole.style.position = 'fixed';
      pole.style.opacity = '0';
      document.body.appendChild(pole);
      pole.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(pole);
      if (ok) hotovo(); else chyba();
    });
  }

  // ---------- Kliknutí ----------

  document.addEventListener('click', function (udalost) {
    var cil = udalost.target;
    if (!cil.closest) return;

    var odkazJazyka = cil.closest('a[data-set-lang]');
    if (odkazJazyka) uloz('jazyk', odkazJazyka.getAttribute('data-set-lang'));

    if (cil.closest('.vzhled')) {
      var novy = zobrazenyRezim() === 'dark' ? 'light' : 'dark';
      var prohlizec = tmavyProhlizec && tmavyProhlizec.matches ? 'dark' : 'light';
      if (novy === prohlizec) {
        // shoda s prohlížečem: znovu se řídit prohlížečem
        root.removeAttribute('data-theme');
        uloz('vzhled', null);
      } else {
        root.setAttribute('data-theme', novy);
        uloz('vzhled', novy);
      }
      obnovIkonu();
    }

    var kopirovat = cil.closest('.kopirovat');
    if (kopirovat) {
      var popisek = kopirovat.querySelector('.kopirovat__text');
      var puvodni = kopirovat.getAttribute('data-text');
      zkopiruj(kopirovat.getAttribute('data-kopirovat')).then(function () {
        kopirovat.setAttribute('data-stav', 'hotovo');
        if (popisek) popisek.textContent = kopirovat.getAttribute('data-hotovo');
        clearTimeout(kopirovat._casovac);
        kopirovat._casovac = setTimeout(function () {
          kopirovat.removeAttribute('data-stav');
          if (popisek) popisek.textContent = puvodni;
        }, 1800);
      }, function () { /* kopírování nedovoleno: text lze označit ručně */ });
    }
  });

  document.addEventListener('DOMContentLoaded', obnovIkonu);
})();
