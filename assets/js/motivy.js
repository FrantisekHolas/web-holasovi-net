/*
  Motivy stromu podle ročního období a svátků.
  Lístky, jména i karty zůstávají stejné, mění se jen malba (a případně efekt).

  Roční období se střídají astronomicky, v okamžiku rovnodennosti a slunovratu
  (jaro kolem 20. 3., léto kolem 21. 6., podzim kolem 23. 9., zima kolem 21. 12.).
  Svátky mají přednost před ročním obdobím a platí celé dny podle českého času.
  Termín svátku: 'den. měsíc.' (např. '24. 12.'), 'Velikonoce' s posunem ve dnech
  od Velikonoční neděle (např. 'Velikonoce -3' = Zelený čtvrtek) nebo 'Advent'
  (1. adventní neděle, případně s posunem ve dnech, např. 'Advent +7').
  Vánoce platí od 1. adventní neděle do 30. 12., pak přijde Silvestr.
  Když na jeden den připadne víc svátků, platí ten, který je v seznamu dřív
  (narozeniny proto stojí před Vánocemi).

  Malby motivu jsou ve složce assets/img/motivy/<id>/ a do pole "obrazky" se zapíše,
  které verze má (všechny ve stejném výřezu a rozměrech jako podzim):
    'ctverec'  = ctverec.webp (1500 × 1500) + ctverec-900.webp + ctverec-2048.webp + pozadi.webp
    'vyska'    = vyska.webp (1116 × 2000) + vyska-720.webp + vyska-1536.webp
    'panorama' = panorama.webp (2000 × 557) + panorama-1200.webp + panorama-3904.webp
  (velké verze 2048, 1536 a 3904 px dostanou jen velké obrazovky; připraví je nastroje/priprav-motiv.py)
  Chybějící verzi nahradí malba ročního období, a není-li ani ta, výchozí motiv.

  Efekt (pole "efekt") je skript assets/js/<efekt>.js, např. 'ohnostroj'.
  Oslavenec (pole "oslavenec") je jméno člena z clenove.js, jehož písmeno je ten den růžové.

  Den a noc: malba se večer podle výšky slunce nad místem "misto" postupně setmí
  (od chvíle, kdy je slunce 2° nad obzorem, do plné noci při 8° pod obzorem) a ráno zase rozjasní.
  Pole "noc" u motivu to může změnit:
    noc: 'vzdy'   = motiv je celý den v nočním režimu (Silvestr kvůli ohňostroji)
    noc: 'malba'  = malba motivu je sama noční, nic se neztmavuje

  Vyzkoušení předem: holasovi.net/?motiv=zima, holasovi.net/?datum=2026-12-31T23:59:50,
  holasovi.net/?datum=2026-11-14T16:45 (soumrak) nebo holasovi.net/?noc=1 (0 = den, 0.5 = šero)
*/
window.HOLASOVI = window.HOLASOVI || {};
window.HOLASOVI.motivy = {
  vychozi: 'podzim',

  // místo, podle jehož slunce se střídá den a noc
  misto: { nazev: 'Brno', sirka: 49.195, delka: 16.608 },

  obdobi: {
    jaro:   { nazev: 'Jaro',   obrazky: ['ctverec', 'vyska', 'panorama'] },
    leto:   { nazev: 'Léto',   obrazky: ['ctverec', 'vyska', 'panorama'] },
    podzim: { nazev: 'Podzim', obrazky: ['ctverec', 'vyska', 'panorama'] },
    zima:   { nazev: 'Zima',   obrazky: ['ctverec', 'vyska', 'panorama'] }
  },

  svatky: [
    { id: 'narozeniny-kristyna', nazev: 'Narozeniny Kristýny', od: '14. 8.',        do: '14. 8.',        obrazky: ['ctverec', 'vyska', 'panorama'], oslavenec: 'Kristýna' },
    { id: 'narozeniny-lukas',    nazev: 'Narozeniny Lukáše',   od: '2. 9.',         do: '2. 9.',         obrazky: ['ctverec', 'vyska', 'panorama'], oslavenec: 'Lukáš' },
    { id: 'narozeniny-radim',    nazev: 'Narozeniny Radima',   od: '16. 11.',       do: '16. 11.',       obrazky: ['ctverec', 'vyska', 'panorama'], oslavenec: 'Radim' },
    { id: 'mikulas',             nazev: 'Mikuláš',             od: '5. 12.',        do: '5. 12.',        obrazky: ['ctverec', 'vyska', 'panorama'] },
    { id: 'narozeniny-vera',     nazev: 'Narozeniny Věrky',    od: '9. 12.',        do: '9. 12.',        obrazky: ['ctverec', 'vyska', 'panorama'], noc: 'malba', oslavenec: 'Věrka' },
    { id: 'vanoce',              nazev: 'Vánoce',              od: 'Advent',        do: '30. 12.',       obrazky: ['ctverec', 'vyska', 'panorama'], noc: 'malba' },
    { id: 'silvestr',            nazev: 'Silvestr a Nový rok', od: '31. 12.',       do: '1. 1.',         obrazky: [], efekt: 'ohnostroj', noc: 'vzdy' },
    { id: 'velikonoce',          nazev: 'Velikonoce',          od: 'Velikonoce -3', do: 'Velikonoce +1', obrazky: ['ctverec', 'vyska', 'panorama'] }
  ]
};
