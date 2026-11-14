/*
  Ohňostroj pro motiv Silvestr a Nový rok (načítá ho assets/js/obdobi.js).
  Rakety startují samy; klepnutí nebo kliknutí na oblohu mimo lístky vypustí další.
  O půlnoci na Nový rok (český čas) přijde velké finále.
  Kdo má v systému zapnuté omezení pohybu, uvidí rakety jen po klepnutí.
  Barvy odpovídají lístkům rodiny.
*/
(function () {
  'use strict';

  var H = window.HOLASOVI || {};
  var motiv = H.motiv || {};
  var scena = document.querySelector('.scena');
  if (!scena) return;

  var platno = document.createElement('canvas');
  platno.className = 'ohnostroj';
  platno.setAttribute('aria-hidden', 'true');
  var ctx = platno.getContext && platno.getContext('2d');
  if (!ctx) return;
  scena.appendChild(platno);

  // bez vlastní noční malby se krajina setmí
  if (!motiv.vlastniObrazky) scena.classList.add('scena--noc');

  var klid = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var ted = H.ted || function () { return Date.now(); };

  // modrozelená, červená, zelená, žlutá, oranžová (lístky) a zlatobílá
  var BARVY = [[110, 225, 240], [255, 95, 80], [150, 240, 100], [255, 222, 90], [255, 150, 60], [255, 240, 200]];
  var ZLATA = [255, 196, 110];
  var MAX_JISKER = 2600;

  var sirka = 0, vyska = 0, dpr = 1, polomer = 100, meritko = 1;
  var rakety = [], jiskry = [], zablesky = [];
  var doDalsi = 0.6, finale = 0, finaleHotovo = false, bezi = false, posledni = 0, prazdno = 0;

  function zmenVelikost() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    sirka = scena.clientWidth;
    vyska = scena.clientHeight;
    platno.width = Math.round(sirka * dpr);
    platno.height = Math.round(vyska * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    polomer = Math.max(65, Math.min(240, 0.15 * Math.sqrt(sirka * vyska)));
    meritko = Math.max(0.9, Math.min(1.6, polomer / 120));
  }

  function nahodne(a, b) { return a + Math.random() * (b - a); }
  function vyber(pole) { return pole[Math.floor(Math.random() * pole.length)]; }

  // ---------- Rakety a výbuchy ----------

  function vypust(cilX, cilY, typ) {
    var startX = Math.min(sirka * 0.95, Math.max(sirka * 0.05, cilX + nahodne(-0.08, 0.08) * sirka));
    rakety.push({
      sx: startX, sy: vyska + 8,
      x: startX, y: vyska + 8,
      cx: cilX, cy: Math.min(cilY, vyska * 0.85),
      t: 0, trvani: nahodne(0.75, 1.15) * Math.min(1.3, Math.max(0.55, (vyska - cilY) / 500)),
      kmit: nahodne(0, 6), typ: typ || nahodnyTyp()
    });
    spust();
  }

  function vypustNahodne(typ) {
    vypust(nahodne(0.12, 0.88) * sirka, nahodne(0.1, 0.42) * vyska, typ);
  }

  function nahodnyTyp() {
    var r = Math.random();
    return r < 0.38 ? 'koule' : r < 0.56 ? 'dvoubarevna' : r < 0.7 ? 'kruh' : r < 0.85 ? 'vrba' : 'trpytka';
  }

  function jiskra(x, y, uhel, rychlost, barva, o) {
    if (jiskry.length >= MAX_JISKER) return;
    jiskry.push({
      x: x, y: y,
      vx: Math.cos(uhel) * rychlost, vy: Math.sin(uhel) * rychlost,
      barva: barva, vek: 0, zivot: o.zivot * nahodne(0.8, 1.15),
      odpor: o.odpor, tize: o.tize, velikost: o.velikost, trpyt: !!o.trpyt
    });
  }

  function vybuch(x, y, typ) {
    var R = polomer * nahodne(0.8, 1.15);
    var barva = vyber(BARVY), druha = vyber(BARVY);
    var zaklad = { zivot: 1.6, odpor: 1.7, tize: 0.45 * polomer, velikost: 1.5 };
    var n, i, z, uhel;
    zablesky.push({ x: x, y: y, r: R * 1.7, vek: 0, barva: typ === 'vrba' ? ZLATA : barva });

    if (typ === 'kruh') {
      n = 64;
      var natoceni = nahodne(0, Math.PI), zplosteni = nahodne(0.45, 1);
      for (i = 0; i < n; i++) {
        uhel = i / n * Math.PI * 2;
        var px = Math.cos(uhel), py = Math.sin(uhel) * zplosteni;
        var rx = px * Math.cos(natoceni) - py * Math.sin(natoceni);
        var ry = px * Math.sin(natoceni) + py * Math.cos(natoceni);
        jiskra(x, y, Math.atan2(ry, rx), R * zaklad.odpor * Math.sqrt(rx * rx + ry * ry), barva, zaklad);
      }
      for (i = 0; i < 24; i++) jiskra(x, y, nahodne(0, 7), R * 0.35 * zaklad.odpor * Math.random(), druha, zaklad);
      return;
    }

    var o = zaklad;
    if (typ === 'vrba') o = { zivot: 2.8, odpor: 2.3, tize: 0.7 * polomer, velikost: 1.2 };
    if (typ === 'trpytka') o = { zivot: 1.9, odpor: 1.7, tize: 0.45 * polomer, velikost: 1.4, trpyt: true };
    n = typ === 'vrba' ? 90 : 110;
    for (i = 0; i < n; i++) {
      // bod na kouli promítnutý do roviny: hustší okraj jako u skutečné pumy
      z = nahodne(-1, 1);
      uhel = nahodne(0, Math.PI * 2);
      var r = Math.sqrt(1 - z * z);
      var b = typ === 'vrba' ? ZLATA : typ === 'trpytka' ? [255, 238, 205] : (typ === 'dvoubarevna' && r < 0.75 ? druha : barva);
      jiskra(x, y, uhel, R * o.odpor * r, b, o);
    }
  }

  // ---------- Kreslení ----------

  function snimek(cas) {
    var dt = posledni ? Math.min((cas - posledni) / 1000, 0.05) : 1 / 60;
    posledni = cas;

    // samočinné rakety a finále
    if (!klid && !finaleHotovo && motiv.svatek === 'silvestr' && ted() >= pulnoc && ted() < pulnoc + 120000) spustFinale();
    if (!klid || finale > 0) {
      doDalsi -= dt;
      if (doDalsi <= 0) {
        if (finale > 0) {
          vypustNahodne(Math.random() < 0.3 ? 'vrba' : Math.random() < 0.3 ? 'trpytka' : null);
          doDalsi = nahodne(0.08, 0.28);
        } else {
          var salva = Math.random() < 0.25 ? 2 + Math.floor(Math.random() * 2) : 1;
          for (var s = 0; s < salva; s++) vypustNahodne();
          doDalsi = nahodne(0.9, 2.6);
        }
      }
      if (finale > 0) {
        finale -= dt;
        if (finale <= 0) for (var f = 0; f < 6; f++) vypust((0.15 + f * 0.14) * sirka, nahodne(0.12, 0.3) * vyska, 'vrba');
      }
    }

    // stopy pomalu mizí
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = 'rgba(0, 0, 0, ' + (1 - Math.pow(0.8, dt * 60)) + ')';
    ctx.fillRect(0, 0, sirka, vyska);
    ctx.globalCompositeOperation = 'lighter';

    var i, j, a;
    for (i = zablesky.length - 1; i >= 0; i--) {
      var z = zablesky[i];
      z.vek += dt;
      a = 0.22 * (1 - z.vek / 0.3);
      if (a <= 0) { zablesky.splice(i, 1); continue; }
      var g = ctx.createRadialGradient(z.x, z.y, 0, z.x, z.y, z.r);
      g.addColorStop(0, 'rgba(' + z.barva[0] + ',' + z.barva[1] + ',' + z.barva[2] + ',' + a + ')');
      g.addColorStop(1, 'rgba(' + z.barva[0] + ',' + z.barva[1] + ',' + z.barva[2] + ',0)');
      ctx.fillStyle = g;
      ctx.fillRect(z.x - z.r, z.y - z.r, z.r * 2, z.r * 2);
    }

    for (i = rakety.length - 1; i >= 0; i--) {
      var k = rakety[i];
      k.t += dt;
      var u = Math.min(1, k.t / k.trvani);
      var e = 1 - (1 - u) * (1 - u);
      k.x = k.sx + (k.cx - k.sx) * e + Math.sin(k.kmit + k.t * 9) * 1.2;
      k.y = k.sy + (k.cy - k.sy) * e;
      jiskra(k.x, k.y, nahodne(1.2, 1.9), nahodne(10, 40), ZLATA, { zivot: 0.45, odpor: 3, tize: 0.3 * polomer, velikost: 1 });
      ctx.fillStyle = 'rgba(255, 236, 200, 0.95)';
      ctx.beginPath();
      ctx.arc(k.x, k.y, 1.8, 0, Math.PI * 2);
      ctx.fill();
      if (u >= 1) {
        rakety.splice(i, 1);
        vybuch(k.x, k.y, k.typ);
      }
    }

    for (i = jiskry.length - 1; i >= 0; i--) {
      var p = jiskry[i];
      p.vek += dt;
      if (p.vek >= p.zivot) {
        jiskry[i] = jiskry[jiskry.length - 1];
        jiskry.pop();
        continue;
      }
      var tlum = Math.exp(-p.odpor * dt);
      p.vx *= tlum;
      p.vy = p.vy * tlum + p.tize * dt;
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      a = Math.pow(1 - p.vek / p.zivot, 1.4);
      if (p.trpyt && p.vek > p.zivot * 0.45 && Math.random() < 0.55) a *= 0.15;
      ctx.fillStyle = 'rgba(' + p.barva[0] + ',' + p.barva[1] + ',' + p.barva[2] + ',' + a + ')';
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.velikost * meritko, 0, Math.PI * 2);
      ctx.fill();
      // bílé jádro u čerstvých jisker
      if (p.vek < p.zivot * 0.35 && p.velikost > 1.1) {
        ctx.fillStyle = 'rgba(255, 255, 255, ' + (a * 0.5) + ')';
        ctx.fillRect(p.x - 0.6, p.y - 0.6, 1.2, 1.2);
      }
    }
    j = jiskry.length + rakety.length + zablesky.length;

    // v klidovém režimu se smyčka zastaví, jakmile vše dohoří
    prazdno = j ? 0 : prazdno + dt;
    if (klid && finale <= 0 && prazdno > 1.5) {
      ctx.clearRect(0, 0, sirka, vyska);
      bezi = false;
      posledni = 0;
      return;
    }
    requestAnimationFrame(snimek);
  }

  function spust() {
    if (bezi) return;
    bezi = true;
    prazdno = 0;
    requestAnimationFrame(snimek);
  }

  // ---------- Půlnoc na Nový rok ----------

  // 1. 1. v 0:00 českého času = 31. 12. ve 23:00 UTC
  var dnes = H.kalendar ? H.kalendar.casVPraze(ted()) : { rok: new Date().getFullYear(), mesic: 1 };
  var pulnoc = Date.UTC(dnes.mesic === 12 ? dnes.rok + 1 : dnes.rok, 0, 1) - 3600000;

  function spustFinale() {
    finaleHotovo = true;
    finale = 12;
    doDalsi = 0;
    spust();
  }

  // ---------- Klepnutí na oblohu ----------

  scena.addEventListener('pointerdown', function (e) {
    if (e.button > 0 || !e.isPrimary) return;
    if (e.target.closest && e.target.closest('.listek, .karta')) return;
    vypust(e.clientX, e.clientY);
  });

  window.addEventListener('resize', zmenVelikost);
  zmenVelikost();
  if (!klid) spust();

  H.ohnostroj = {
    vypust: vypust,
    finale: spustFinale,
    stav: function () { return { rakety: rakety.length, jiskry: jiskry.length, finale: finale, bezi: bezi }; }
  };
})();
