/*
  Motivy stromu podle ročního období a svátků.
  Lístky, jména i karty zůstávají stejné, mění se jen malba (a případně efekt).

  Roční období se střídají astronomicky, v okamžiku rovnodennosti a slunovratu
  (jaro kolem 20. 3., léto kolem 21. 6., podzim kolem 23. 9., zima kolem 21. 12.).
  Svátky mají přednost před ročním obdobím a platí celé dny podle českého času.
  Termín svátku: 'den. měsíc.' (např. '24. 12.') nebo 'Velikonoce' s posunem ve dnech
  od Velikonoční neděle (např. 'Velikonoce -3' = Zelený čtvrtek).

  Malby motivu jsou ve složce assets/img/motivy/<id>/ a do pole "obrazky" se zapíše,
  které verze má (všechny ve stejném výřezu a rozměrech jako podzim):
    'ctverec'  = ctverec.webp (1500 × 1500) + ctverec-900.webp + pozadi.webp
    'vyska'    = vyska.webp (1116 × 2000) + vyska-720.webp
    'panorama' = panorama.webp (2000 × 557) + panorama-1200.webp
  Chybějící verzi nahradí malba ročního období, a není-li ani ta, výchozí motiv.

  Efekt (pole "efekt") je skript assets/js/<efekt>.js, např. 'ohnostroj'.

  Vyzkoušení předem: holasovi.net/?motiv=zima nebo holasovi.net/?datum=2026-12-31T23:59:50
*/
window.HOLASOVI = window.HOLASOVI || {};
window.HOLASOVI.motivy = {
  vychozi: 'podzim',

  obdobi: {
    jaro:   { nazev: 'Jaro',   obrazky: [] },
    leto:   { nazev: 'Léto',   obrazky: [] },
    podzim: { nazev: 'Podzim', obrazky: ['ctverec', 'vyska', 'panorama'] },
    zima:   { nazev: 'Zima',   obrazky: [] }
  },

  svatky: [
    { id: 'vanoce',     nazev: 'Vánoce',              od: '24. 12.',        do: '26. 12.',       obrazky: [] },
    { id: 'silvestr',   nazev: 'Silvestr a Nový rok', od: '31. 12.',        do: '1. 1.',         obrazky: [], efekt: 'ohnostroj' },
    { id: 'velikonoce', nazev: 'Velikonoce',          od: 'Velikonoce -3',  do: 'Velikonoce +1', obrazky: [] }
  ]
};
