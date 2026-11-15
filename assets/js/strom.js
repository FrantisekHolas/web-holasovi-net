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
    web: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.8 3.9 5.8 3.9 9s-1.3 6.2-3.9 9c-2.6-2.8-3.9-5.8-3.9-9s1.3-6.2 3.9-9z"/>',
    firma: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    linkedin: '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    schranka: '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>'
  };
  var REGISTR_SCHRANEK = 'https://www.datovka.gov.cz/sds/detail?dbid=';
  var SIPKA = '<svg class="odkaz__sipka" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>';
  var DALE = '<svg class="odkaz__sipka" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>';

  if (!platno) return;

  // posun = [vodorovně, svisle] v procentech šířky lístku (záporné doleva / nahoru),
  // samotné číslo = jen vodorovně; posouvá se ve směru obrazovky, nezávisle na natočení
  function inicialaSvg(pismeno, natoceni, posun) {
    var svg = document.createElementNS(SVG, 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    var text = document.createElementNS(SVG, 'text');
    text.setAttribute('x', '50');
    text.setAttribute('y', '52');
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('dominant-baseline', 'central');
    var dx = Number(Array.isArray(posun) ? posun[0] : posun) || 0;
    var dy = Array.isArray(posun) ? Number(posun[1]) || 0 : 0;
    var transformace = [];
    if (dx || dy) transformace.push('translate(' + dx + ' ' + dy + ')');
    if (natoceni) transformace.push('rotate(' + natoceni + ' 50 50)');
    if (transformace.length) text.setAttribute('transform', transformace.join(' '));
    // Ozdobné patky písma přesahují šířku písmene (u L o 0,6 em vpravo). Safari kreslí zlatý
    // přechod jen v šířce textu, proto jsou kolem písmene mezery (3 × 0,25 em), na obě strany
    // stejně, aby písmeno zůstalo uprostřed.
    text.setAttributeNS('http://www.w3.org/XML/1998/namespace', 'xml:space', 'preserve');
    text.textContent = '   ' + pismeno + '   ';
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
      } else if (k.typ === 'datovka' && k.id) {
        // odkaz do veřejného seznamu datových schránek, jen pokud je schránka v seznamu dohledatelná
        polozky.push({ ikona: 'schranka', popis: k.popis || 'Datová schránka', text: k.id, url: k.overit === false ? null : REGISTR_SCHRANEK + encodeURIComponent(k.id), venku: true });
      }
    });
    (clen.odkazy || []).forEach(function (o) {
      if (!o.url) return;
      // odkaz na jiný web (s protokolem) do nové záložky, odkaz v rámci holasovi.net ve stejné
      var venku = /^[a-z][a-z0-9+.-]*:/i.test(o.url);
      polozky.push({ ikona: IKONY[o.ikona] ? o.ikona : 'web', popis: o.popis || 'Webová stránka', text: o.text || o.url, url: o.url, venku: venku, interni: !venku });
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
    if (data.motiv && data.motiv.ctverecMaly) kartaListek.style.backgroundImage = 'url("' + data.motiv.ctverecMaly + '")';
    kartaListek.style.backgroundSize = (900 * meritko) + 'px';
    kartaListek.style.backgroundPosition = (-(x - 60) * meritko) + 'px ' + (-(y - 60) * meritko) + 'px';
    kartaListek.replaceChildren(inicialaSvg(clen.inicial, 0, clen.posunPismene));

    kartaOdkazy.replaceChildren();
    var polozky = polozkyKarty(clen);
    kartaOdkazy.hidden = polozky.length === 0;
    polozky.forEach(function (p) {
      var li = document.createElement('li');
      // položka bez adresy (např. neověřitelná datová schránka) je jen text
      var a = document.createElement(p.url ? 'a' : 'div');
      a.className = p.url ? 'odkaz' : 'odkaz odkaz--text';
      if (p.url) {
        a.href = p.url;
        if (p.venku) {
          a.target = '_blank';
          a.rel = 'noopener';
        }
      }
      a.innerHTML =
        '<svg class="odkaz__ikona" viewBox="0 0 24 24" aria-hidden="true">' + IKONY[p.ikona] + '</svg>' +
        '<span class="odkaz__texty"><span class="odkaz__popis"></span><span class="odkaz__adresa"></span></span>' +
        (!p.url ? '' : p.venku ? SIPKA : p.interni ? DALE : '');
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

  // oslavenec motivu (např. narozeniny v motivy.js): jeho lístek a písmeno září
  var oslavenec = data.motiv && data.motiv.oslavenec;

  data.clenove.forEach(function (clen) {
    var el = document.createElement('button');
    el.type = 'button';
    el.className = clen.jmeno === oslavenec ? 'listek listek--oslavenec' : 'listek';
    el.setAttribute('aria-haspopup', 'dialog');
    el.setAttribute('aria-expanded', 'false');
    el.setAttribute('aria-label', clen.jmeno + (clen.jmeno === oslavenec ? ' (dnes slaví)' : '') + ' – zobrazit kontakt');
    nastavPolohu(el, clen.poloha);
    el.style.setProperty('--zare', clen.zare);
    el.appendChild(inicialaSvg(clen.inicial, clen.natoceni, clen.posunPismene));

    var jmeno = document.createElement('span');
    jmeno.className = 'listek__jmeno';
    jmeno.setAttribute('aria-hidden', 'true');
    jmeno.textContent = clen.jmeno;
    el.appendChild(jmeno);

    el.addEventListener('click', function () { otevriKartu(clen, el); });
    platno.appendChild(el);
  });
})();
