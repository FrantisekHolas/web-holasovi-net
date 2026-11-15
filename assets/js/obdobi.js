/*
  Výběr motivu stromu podle data a času v Česku (motivy jsou v assets/js/motivy.js).
  Nastaví malbu pro všechny tři tvary obrazovky, rozmazané pozadí a načte efekt motivu.
*/
(function () {
  'use strict';

  var H = window.HOLASOVI = window.HOLASOVI || {};
  var nastaveni = H.motivy || {};
  var obdobi = nastaveni.obdobi || {};
  var svatky = nastaveni.svatky || [];
  var VYCHOZI = nastaveni.vychozi || 'podzim';
  var ADRESAR = 'assets/img/motivy/';
  var FORMATY = {
    ctverec:  { male: 900,  velke: 1500 },
    vyska:    { male: 720,  velke: 1116 },
    panorama: { male: 1200, velke: 2000 }
  };
  var ROCNI_OBDOBI = ['jaro', 'leto', 'podzim', 'zima'];

  // ---------- Kalendář ----------

  // Rovnodennosti a slunovraty podle J. Meeuse (Astronomical Algorithms, kap. 27),
  // přesnost zhruba na minutu. Platí pro roky 2000–3000.
  var SEZONY = [
    [2451623.80984, 365242.37404, 0.05169, -0.00411, -0.00057],  // jarní rovnodennost
    [2451716.56767, 365241.62603, 0.00325, 0.00888, -0.00030],   // letní slunovrat
    [2451810.21715, 365242.01767, -0.11575, 0.00337, 0.00078],   // podzimní rovnodennost
    [2451900.05952, 365242.74049, -0.06223, -0.00823, 0.00032]   // zimní slunovrat
  ];
  var CLENY = [
    [485, 324.96, 1934.136], [203, 337.23, 32964.467], [199, 342.08, 20.186], [182, 27.85, 445267.112],
    [156, 73.14, 45036.886], [136, 171.52, 22518.443], [77, 222.54, 65928.934], [74, 296.72, 3034.906],
    [70, 243.58, 9037.513], [58, 119.81, 33718.147], [52, 297.17, 150.678], [50, 21.02, 2281.226],
    [45, 247.54, 29929.562], [44, 325.15, 31555.956], [29, 60.93, 4443.417], [18, 155.12, 67555.328],
    [17, 288.79, 4562.452], [16, 198.04, 62894.029], [14, 199.76, 31436.921], [12, 95.39, 14577.848],
    [12, 287.11, 31931.756], [12, 320.81, 34777.259], [9, 227.73, 1222.114], [8, 15.45, 16859.074]
  ];
  var STUPEN = Math.PI / 180;

  // Okamžik začátku ročního období (0 jaro … 3 zima) v daném roce, v ms od 1. 1. 1970 UTC.
  function zacatekObdobi(rok, i) {
    var Y = (rok - 2000) / 1000;
    var k = SEZONY[i];
    var jde0 = k[0] + Y * (k[1] + Y * (k[2] + Y * (k[3] + Y * k[4])));
    var T = (jde0 - 2451545) / 36525;
    var W = (35999.373 * T - 2.47) * STUPEN;
    var dl = 1 + 0.0334 * Math.cos(W) + 0.0007 * Math.cos(2 * W);
    var S = 0;
    for (var j = 0; j < CLENY.length; j++) S += CLENY[j][0] * Math.cos((CLENY[j][1] + CLENY[j][2] * T) * STUPEN);
    var jde = jde0 + 0.00001 * S / dl;
    return Math.round((jde - 2440587.5) * 86400000) - 69000;  // dynamický čas → světový (ΔT ≈ 69 s)
  }

  function rocniObdobi(cas) {
    var rok = new Date(cas).getUTCFullYear();
    var vysledek = 'zima';
    for (var i = 0; i < 4; i++) if (cas >= zacatekObdobi(rok, i)) vysledek = ROCNI_OBDOBI[i];
    return vysledek;
  }

  // Velikonoční neděle (gregoriánský kalendář) → [měsíc, den].
  function velikonocniNedele(rok) {
    var a = rok % 19, b = Math.floor(rok / 100), c = rok % 100;
    var d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3);
    var h = (19 * a + b - d - g + 15) % 30;
    var i = Math.floor(c / 4), k = c % 4;
    var l = (32 + 2 * e + 2 * i - h - k) % 7;
    var m = Math.floor((a + 11 * h + 22 * l) / 451);
    var n = h + l - 7 * m + 114;
    return [Math.floor(n / 31), (n % 31) + 1];
  }

  // Datum a čas v Česku pro okamžik v ms.
  var formatPraha = null;
  try {
    formatPraha = new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Prague', hourCycle: 'h23',
      year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
    });
  } catch (e) { /* bez časových pásem: použije se čas zařízení */ }

  function casVPraze(cas) {
    if (formatPraha) {
      var c = {};
      formatPraha.formatToParts(new Date(cas)).forEach(function (p) { if (p.type !== 'literal') c[p.type] = +p.value; });
      return { rok: c.year, mesic: c.month, den: c.day, hodina: c.hour, minuta: c.minute, sekunda: c.second };
    }
    var d = new Date(cas);
    return { rok: d.getFullYear(), mesic: d.getMonth() + 1, den: d.getDate(), hodina: d.getHours(), minuta: d.getMinutes(), sekunda: d.getSeconds() };
  }

  // Čas v Česku (rok, měsíc, den, hodina, minuta, sekunda) → ms od 1. 1. 1970 UTC.
  function casZPrahy(r, mes, d, h, min, s) {
    var cil = Date.UTC(r, mes - 1, d, h || 0, min || 0, s || 0);
    var odhad = cil;
    for (var i = 0; i < 3; i++) {
      var p = casVPraze(odhad);
      odhad = cil - (Date.UTC(p.rok, p.mesic - 1, p.den, p.hodina, p.minuta, p.sekunda) - odhad);
    }
    return odhad;
  }

  // První adventní neděle → [měsíc, den]: čtvrtá neděle před Božím hodem (27. 11. – 3. 12.).
  function prvniAdventniNedele(rok) {
    var stedryDen = new Date(Date.UTC(rok, 11, 24));
    var ctvrta = 24 - stedryDen.getUTCDay();          // neděle 18. – 24. 12.
    var d = new Date(Date.UTC(rok, 11, ctvrta - 21));
    return [d.getUTCMonth() + 1, d.getUTCDate()];
  }

  // Text termínu ('24. 12.', 'Velikonoce -3' nebo 'Advent') → měsíc * 100 + den v daném roce.
  function klicTerminu(text, rok) {
    var m = /^\s*(\d{1,2})\s*\.\s*(\d{1,2})\s*\.?\s*$/.exec(text);
    if (m) return +m[2] * 100 + +m[1];
    m = /^\s*(velikonoce|advent)\s*(?:([+-])\s*(\d+))?\s*$/i.exec(text);
    if (m) {
      var v = m[1].toLowerCase() === 'advent' ? prvniAdventniNedele(rok) : velikonocniNedele(rok);
      var posun = m[3] ? (m[2] === '-' ? -1 : 1) * +m[3] : 0;
      var d = new Date(Date.UTC(rok, v[0] - 1, v[1] + posun));
      return (d.getUTCMonth() + 1) * 100 + d.getUTCDate();
    }
    return null;
  }

  function svatekDne(p) {
    var dnes = p.mesic * 100 + p.den;
    for (var i = 0; i < svatky.length; i++) {
      var s = svatky[i];
      var od = klicTerminu(String(s.od), p.rok);
      var doKdy = klicTerminu(String(s.do), p.rok);
      if (od === null || doKdy === null) {
        console.warn('Motiv „' + s.id + '“ má neplatný termín (od: ' + s.od + ', do: ' + s.do + ').');
        continue;
      }
      // termín přes přelom roku (31. 12. – 1. 1.)
      if (od <= doKdy ? (dnes >= od && dnes <= doKdy) : (dnes >= od || dnes <= doKdy)) return s;
    }
    return null;
  }

  function najdiMotiv(id) {
    if (obdobi[id]) return obdobi[id];
    for (var i = 0; i < svatky.length; i++) if (svatky[i].id === id) return svatky[i];
    return null;
  }

  function maObrazek(id, format) {
    var m = najdiMotiv(id);
    return !!(m && m.obrazky && m.obrazky.indexOf(format) >= 0);
  }

  // Motiv pro okamžik; vynucenyMotiv (z adresy ?motiv=) má přednost.
  function vyberMotiv(cas, vynucenyMotiv) {
    var sezona = rocniObdobi(cas);
    var svatek = svatekDne(casVPraze(cas));
    if (vynucenyMotiv) {
      if (obdobi[vynucenyMotiv]) {
        sezona = vynucenyMotiv;
        svatek = null;
      } else if (najdiMotiv(vynucenyMotiv)) {
        svatek = najdiMotiv(vynucenyMotiv);
      } else {
        console.warn('Motiv „' + vynucenyMotiv + '“ neexistuje.');
      }
    }
    var id = svatek ? svatek.id : sezona;
    var motiv = najdiMotiv(id) || {};
    var poradi = [svatek && svatek.id, sezona, VYCHOZI];
    var zdroje = {};
    Object.keys(FORMATY).forEach(function (format) {
      zdroje[format] = VYCHOZI;
      for (var i = 0; i < poradi.length; i++) {
        if (poradi[i] && maObrazek(poradi[i], format)) { zdroje[format] = poradi[i]; break; }
      }
    });
    return {
      id: id,
      nazev: motiv.nazev || id,
      sezona: sezona,
      svatek: svatek ? svatek.id : null,
      efekt: motiv.efekt || null,
      noc: motiv.noc || null,
      vlastniObrazky: !!(motiv.obrazky && motiv.obrazky.length),
      zdroje: zdroje
    };
  }

  // ---------- Den a noc ----------

  var MISTO = nastaveni.misto || { sirka: 49.195, delka: 16.608 };

  // Výška slunce nad obzorem ve stupních (zjednodušený výpočet, přesnost asi 0,2°).
  function vyskaSlunce(cas, sirka, delka) {
    var d = cas / 86400000 - 10957.5;  // dny od 1. 1. 2000 12:00 UTC
    var M = (357.5291 + 0.98560028 * d) * STUPEN;
    var C = (1.9148 * Math.sin(M) + 0.02 * Math.sin(2 * M) + 0.0003 * Math.sin(3 * M)) * STUPEN;
    var L = M + C + (180 + 102.9372) * STUPEN;
    var e = 23.4397 * STUPEN;
    var dekl = Math.asin(Math.sin(L) * Math.sin(e));
    var rekt = Math.atan2(Math.sin(L) * Math.cos(e), Math.cos(L));
    var hodinovyUhel = (280.16 + 360.9856235 * d + delka) * STUPEN - rekt;
    var fi = sirka * STUPEN;
    return Math.asin(Math.sin(fi) * Math.sin(dekl) + Math.cos(fi) * Math.cos(dekl) * Math.cos(hodinovyUhel)) / STUPEN;
  }

  // 0 = den (slunce výš než 2° nad obzorem), 1 = noc (slunce níž než 8° pod obzorem), mezi tím soumrak.
  function miraNoci(cas) {
    var t = Math.min(1, Math.max(0, (2 - vyskaSlunce(cas, MISTO.sirka, MISTO.delka)) / 10));
    return t * t * (3 - 2 * t);
  }

  // ---------- Parametry adresy pro vyzkoušení ----------

  var parametry = {};
  location.search.replace(/^\?/, '').split('&').forEach(function (cast) {
    var kv = cast.split('=');
    if (kv[0]) parametry[decodeURIComponent(kv[0])] = decodeURIComponent((kv[1] || '').replace(/\+/g, ' '));
  });

  // ?datum=2026-12-31 nebo ?datum=2026-12-31T23:59:50 (český čas): hodiny běží od tohoto okamžiku
  var posunHodin = 0;
  var datum = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?$/.exec(parametry.datum || '');
  if (datum) {
    posunHodin = casZPrahy(+datum[1], +datum[2], +datum[3], +(datum[4] || 12), +(datum[5] || 0), +(datum[6] || 0)) - Date.now();
  }

  H.ted = function () { return Date.now() + posunHodin; };
  H.kalendar = {
    zacatekObdobi: zacatekObdobi,
    rocniObdobi: rocniObdobi,
    velikonocniNedele: velikonocniNedele,
    prvniAdventniNedele: prvniAdventniNedele,
    casVPraze: casVPraze,
    casZPrahy: casZPrahy,
    vyberMotiv: vyberMotiv,
    vyskaSlunce: vyskaSlunce,
    miraNoci: miraNoci
  };

  // ---------- Malba ----------

  function cesta(id, soubor) { return ADRESAR + id + '/' + soubor; }

  function srcset(id, format) {
    var f = FORMATY[format];
    return cesta(id, format + '-' + f.male + '.webp') + ' ' + f.male + 'w, ' + cesta(id, format + '.webp') + ' ' + f.velke + 'w';
  }

  var motiv;
  try {
    motiv = vyberMotiv(H.ted(), parametry.motiv);
  } catch (e) {
    console.error('Motiv se nepodařilo vybrat, použije se výchozí.', e);
    motiv = { id: VYCHOZI, nazev: VYCHOZI, sezona: VYCHOZI, svatek: null, efekt: null, vlastniObrazky: true,
              zdroje: { ctverec: VYCHOZI, vyska: VYCHOZI, panorama: VYCHOZI } };
  }
  motiv.ctverecMaly = cesta(motiv.zdroje.ctverec, 'ctverec-900.webp');
  H.motiv = motiv;

  var root = document.documentElement;
  root.setAttribute('data-motiv', motiv.id);
  root.setAttribute('data-obdobi', motiv.sezona);

  var obraz = document.getElementById('obraz');
  if (obraz) {
    // nejdřív zdroje pro výšku a panorama, obrázek až nakonec (aby se nestahoval zbytečně čtverec)
    Array.prototype.forEach.call(obraz.querySelectorAll('source[data-format]'), function (zdroj) {
      var format = zdroj.getAttribute('data-format');
      if (FORMATY[format]) zdroj.setAttribute('srcset', srcset(motiv.zdroje[format], format));
    });
    var img = obraz.querySelector('img');
    if (img) {
      img.setAttribute('srcset', srcset(motiv.zdroje.ctverec, 'ctverec'));
      img.setAttribute('src', cesta(motiv.zdroje.ctverec, 'ctverec.webp'));
    }
  }

  var pozadi = document.querySelector('.scena__pozadi');
  if (pozadi) pozadi.style.backgroundImage = 'url("' + cesta(motiv.zdroje.ctverec, 'pozadi.webp') + '")';

  // Noc: krajina potemní, obloha zmodrá a lístky svítí (styly v assets/css/styl.css, část Den a noc).
  // Přepočítává se každou minutu, takže otevřená stránka se večer pomalu stmívá.
  var vynucenaNoc = parseFloat(parametry.noc);
  var minulaNoc = null;
  // tvar obrazovky podle stejných podmínek jako <source media> v index.html
  var DOTAZY = { vyska: '(max-aspect-ratio: 3/4)', panorama: '(min-aspect-ratio: 21/10)' };
  function zobrazenyFormat() {
    if (!window.matchMedia) return 'ctverec';
    if (window.matchMedia(DOTAZY.vyska).matches) return 'vyska';
    if (window.matchMedia(DOTAZY.panorama).matches) return 'panorama';
    return 'ctverec';
  }
  function nastavNoc() {
    var noc;
    if (!isNaN(vynucenaNoc)) noc = Math.min(1, Math.max(0, vynucenaNoc));
    else if (motiv.noc === 'vzdy') noc = 1;
    // noční malba se neztmavuje; záložní malba jiného motivu (chybí-li daný tvar) se řídí sluncem
    else if (motiv.noc === 'malba' && motiv.zdroje[zobrazenyFormat()] === motiv.id) noc = 0;
    else {
      try { noc = miraNoci(H.ted()); } catch (e) { noc = 0; }
    }
    noc = Math.round(noc * 100) / 100;
    if (noc === minulaNoc) return;
    minulaNoc = noc;
    H.noc = noc;
    root.setAttribute('data-den', noc >= 0.5 ? 'noc' : 'den');
    if (!noc) {
      ['--noc', '--zare-noc', '--filtr-malby', '--filtr-pozadi'].forEach(function (v) { root.style.removeProperty(v); });
      return;
    }
    root.style.setProperty('--noc', noc);
    root.style.setProperty('--zare-noc', (0.7 * noc).toFixed(3));
    root.style.setProperty('--filtr-malby',
      'brightness(' + (1 - 0.6 * noc).toFixed(3) + ') saturate(' + (1 - 0.2 * noc).toFixed(3) + ') contrast(' + (1 + 0.05 * noc).toFixed(3) + ')');
    root.style.setProperty('--filtr-pozadi',
      'blur(30px) saturate(' + (1.15 - 0.05 * noc).toFixed(3) + ') brightness(' + (0.78 - 0.48 * noc).toFixed(3) + ')');
  }
  nastavNoc();
  setInterval(nastavNoc, 60000);
  if (motiv.noc === 'malba' && window.matchMedia) {
    Object.keys(DOTAZY).forEach(function (f) {
      var mq = window.matchMedia(DOTAZY[f]);
      if (mq.addEventListener) mq.addEventListener('change', nastavNoc);
      else if (mq.addListener) mq.addListener(nastavNoc);
    });
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden) nastavNoc(); });

  if (motiv.efekt && /^[a-z0-9-]+$/.test(motiv.efekt)) {
    var skript = document.createElement('script');
    skript.src = 'assets/js/' + motiv.efekt + '.js';
    document.body.appendChild(skript);
  }
})();
