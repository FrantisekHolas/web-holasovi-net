/*
  Členové rodiny Holasových a jejich odkazy.

  Jak přidat odkaz:
    Do pole "odkazy" u daného člena vložte položku, např.
      { popis: 'Webová stránka', text: 'lukas.holasovi.net', url: 'https://lukas.holasovi.net' }
    Lístek bez odkazů je jen ozdobou a nedá se na něj kliknout.
    Jakmile člen dostane první odkaz, jeho lístek začne fungovat sám.

  Polohy lístků jsou v procentech obrazu [vodorovně, svisle] pro tři verze malby:
    ctverec  = assets/img/strom-ctverec.webp  (notebooky, běžné monitory, tablety na šířku)
    vyska    = assets/img/strom-na-vysku.webp (mobily a tablety na výšku)
    panorama = assets/img/strom-panorama.webp (ultraširoké monitory 21:9 a 32:9)
  Polohy měňte jen tehdy, když se vymění obraz.
*/
window.HOLASOVI = {
  clenove: [
    {
      jmeno: 'František',
      inicial: 'F',
      listek: 'modrozelený',
      natoceni: 8,
      zare: 'rgba(140, 220, 230, 0.75)',
      poloha: { ctverec: [39.07, 23.33], vyska: [39.34, 25.95], panorama: [47.25, 22.98] },
      odkazy: [
        { popis: 'Webová stránka', text: 'frantisek.holasovi.net', url: 'https://frantisek.holasovi.net' }
      ]
    },
    {
      jmeno: 'Věrka',
      inicial: 'V',
      listek: 'červený',
      natoceni: -12,
      zare: 'rgba(255, 140, 120, 0.75)',
      poloha: { ctverec: [83.0, 48.53], vyska: [83.33, 42.5], panorama: [59.2, 49.37] },
      odkazy: []
    },
    {
      jmeno: 'Lukáš',
      inicial: 'L',
      listek: 'zelený',
      natoceni: 8,
      zare: 'rgba(190, 240, 140, 0.75)',
      poloha: { ctverec: [31.4, 43.2], vyska: [30.82, 38.15], panorama: [44.65, 42.55] },
      odkazy: []
    },
    {
      jmeno: 'Radim',
      inicial: 'R',
      listek: 'žlutý',
      natoceni: -6,
      zare: 'rgba(255, 228, 140, 0.75)',
      poloha: { ctverec: [52.07, 35.0], vyska: [52.24, 34.0], panorama: [50.65, 35.37] },
      odkazy: []
    },
    {
      jmeno: 'Kristýna',
      inicial: 'K',
      listek: 'oranžový',
      natoceni: -6,
      zare: 'rgba(255, 190, 110, 0.75)',
      poloha: { ctverec: [69.4, 35.07], vyska: [69.71, 34.0], panorama: [55.4, 35.01] },
      odkazy: []
    }
  ]
};
