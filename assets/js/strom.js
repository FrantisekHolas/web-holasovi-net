(function () {
  'use strict';

  var SVG = 'http://www.w3.org/2000/svg';
  var data = window.HOLASOVI || { clenove: [] };
  var platno = document.getElementById('platno');
  var karta = document.getElementById('karta');
  var kartaJmeno = document.getElementById('karta-jmeno');
  var kartaListek = document.getElementById('karta-listek');
  var kartaOdkazy = document.getElementById('karta-odkazy');
  var aktivni = null;

  var IKONY = {
    email: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    telefon: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    web: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.8 3.9 5.8 3.9 9s-1.3 6.2-3.9 9c-2.6-2.8-3.9-5.8-3.9-9s1.3-6.2 3.9-9z"/>'
  };
  var SIPKA = '<svg class="odkaz__sipka" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>';

  if (!platno) return;

  function inicialaSvg(pismeno, natoceni) {
    var svg = document.createElementNS(SVG, 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var text = document.createElementNS(SVG, 'text');
    text.setAttribute('x', '50');
    text.setAttribute('y', '52');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('dominant-baseline', 'central');
    if (natoceni) text.setAttribute('transform', 'rotate(' + natoceni + ' 50 50)');
    text.textContent = pismeno;
    svg.appendChild(text);
    return svg;
  }

  function nastavPolohu(el, poloha) {
    el.style.setProperty('--x-c', poloha.ctverec[0] + '%');
    el.style.setProperty('--y-c', poloha.ctverec[1] + '%');
    el.style.setProperty('--x-v', poloha.vyska[0] + '%');
    el.style.setProperty('--y-v', poloha.vyska[1] + '%');
    el.style.setProperty('--x-p', poloha.panorama[0] + '%');
    el.style.setProperty('--y-p', poloha.panorama[1] + '%');
  }

  // Kontakty a odkazy člena převede na jednotné položky karty.
  function polozkyKarty(clen) {
    var polozky = [];
    (clen.kontakty || []).forEach(function (k) {
      if (k.typ === 'email' && k.uzivatel && k.domena) {
        var adresa = k.uzivatel + '@' + k.domena;
        polozky.push({ ikona: 'email', popis: k.popis || 'E-mail', text: adresa, url: 'mailto:' + adresa, venku: false });
      } else if (k.typ === 'telefon' && k.cislo) {
        polozky.push({ ikona: 'telefon', popis: k.popis || 'Telefon', text: k.cislo, url: 'tel:' + k.cislo.replace(/[^+\d]/g, ''), venku: false });
      }
    });
    (clen.odkazy || []).forEach(function (o) {
      if (o.url) polozky.push({ ikona: 'web', popis: o.popis || 'Webová stránka', text: o.text || o.url, url: o.url, venku: true });
    });
    return polozky;
  }

  function otevriKartu(clen, tlacitko) {
    if (!karta || typeof karta.showModal !== 'function') return;
    kartaJmeno.textContent = clen.jmeno;

    // výřez lístku z čtvercové malby (900 px) jako miniatura 72 px
    var meritko = 72 / 120;
    var x = clen.poloha.ctverec[0] / 100 * 900;
    var y = clen.poloha.ctverec[1] / 100 * 900;
    kartaListek.style.backgroundSize = (900 * meritko) + 'px';
    kartaListek.style.backgroundPosition = (-(x - 60) * meritko) + 'px ' + (-(y - 60) * meritko) + 'px';
    kartaListek.replaceChildren(inicialaSvg(clen.inicial, 0));

    kartaOdkazy.replaceChildren();
    var polozky = polozkyKarty(clen);
    kartaOdkazy.hidden = polozky.length === 0;
    polozky.forEach(function (p) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'odkaz';
      a.href = p.url;
      if (p.venku) {
        a.target = '_blank';
        a.rel = 'noopener';
      }
      a.innerHTML =
        '<svg class="odkaz__ikona" viewBox="0 0 24 24" aria-hidden="true">' + IKONY[p.ikona] + '</svg>' +
        '<span class="odkaz__texty"><span class="odkaz__popis"></span><span class="odkaz__adresa"></span></span>' +
        (p.venku ? SIPKA : '');
      a.querySelector('.odkaz__popis').textContent = p.popis;
      a.querySelector('.odkaz__adresa').textContent = p.text;
      li.appendChild(a);
      kartaOdkazy.appendChild(li);
    });

    aktivni = tlacitko;
    tlacitko.setAttribute('aria-expanded', 'true');
    karta.showModal();
  }

  if (karta) {
    karta.addEventListener('close', function () {
      if (aktivni) aktivni.setAttribute('aria-expanded', 'false');
      aktivni = null;
    });
    // klik mimo kartu ji zavře
    karta.addEventListener('click', function (e) {
      if (e.target === karta) karta.close();
    });
    var zavrit = karta.querySelector('.karta__zavrit');
    if (zavrit) zavrit.addEventListener('click', function () { karta.close(); });
  }

  data.clenove.forEach(function (clen) {
    var el = document.createElement('button');
    el.type = 'button';
    el.className = 'listek';
    el.setAttribute('aria-haspopup', 'dialog');
    el.setAttribute('aria-expanded', 'false');
    el.setAttribute('aria-label', clen.jmeno + ' – zobrazit kontakt');
    nastavPolohu(el, clen.poloha);
    el.style.setProperty('--zare', clen.zare);
    el.appendChild(inicialaSvg(clen.inicial, clen.natoceni));

    var jmeno = document.createElement('span');
    jmeno.className = 'listek__jmeno';
    jmeno.setAttribute('aria-hidden', 'true');
    jmeno.textContent = clen.jmeno;
    el.appendChild(jmeno);

    el.addEventListener('click', function () { otevriKartu(clen, el); });
    platno.appendChild(el);
  });
})();
