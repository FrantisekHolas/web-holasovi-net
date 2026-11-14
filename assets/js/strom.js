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

  function otevriKartu(clen, tlacitko) {
    if (!karta || typeof karta.showModal !== 'function') {
      window.location.href = clen.odkazy[0].url;
      return;
    }
    kartaJmeno.textContent = clen.jmeno;

    // výřez lístku z čtvercové malby (900 px) jako miniatura 72 px
    var meritko = 72 / 120;
    var x = clen.poloha.ctverec[0] / 100 * 900;
    var y = clen.poloha.ctverec[1] / 100 * 900;
    kartaListek.style.backgroundSize = (900 * meritko) + 'px';
    kartaListek.style.backgroundPosition = (-(x - 60) * meritko) + 'px ' + (-(y - 60) * meritko) + 'px';
    kartaListek.replaceChildren(inicialaSvg(clen.inicial, 0));

    kartaOdkazy.replaceChildren();
    clen.odkazy.forEach(function (o) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'odkaz';
      a.href = o.url;
      a.target = '_blank';
      a.rel = 'noopener';
      a.innerHTML =
        '<svg class="odkaz__ikona" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.8 3.9 5.8 3.9 9s-1.3 6.2-3.9 9c-2.6-2.8-3.9-5.8-3.9-9s1.3-6.2 3.9-9z"/></svg>' +
        '<span class="odkaz__texty"><span class="odkaz__popis"></span><span class="odkaz__adresa"></span></span>' +
        '<svg class="odkaz__sipka" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>';
      a.querySelector('.odkaz__popis').textContent = o.popis;
      a.querySelector('.odkaz__adresa').textContent = o.text;
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
    var maOdkazy = Array.isArray(clen.odkazy) && clen.odkazy.length > 0;
    var el = document.createElement(maOdkazy ? 'button' : 'span');
    el.className = 'listek';
    nastavPolohu(el, clen.poloha);
    el.style.setProperty('--zare', clen.zare);
    el.appendChild(inicialaSvg(clen.inicial, clen.natoceni));

    if (maOdkazy) {
      el.type = 'button';
      el.setAttribute('aria-haspopup', 'dialog');
      el.setAttribute('aria-expanded', 'false');
      el.setAttribute('aria-label', clen.jmeno + ' – zobrazit odkazy');
      var jmeno = document.createElement('span');
      jmeno.className = 'listek__jmeno';
      jmeno.setAttribute('aria-hidden', 'true');
      jmeno.textContent = clen.jmeno;
      el.appendChild(jmeno);
      el.addEventListener('click', function () { otevriKartu(clen, el); });
    } else {
      el.setAttribute('role', 'img');
      el.setAttribute('aria-label', clen.jmeno);
    }
    platno.appendChild(el);
  });
})();
