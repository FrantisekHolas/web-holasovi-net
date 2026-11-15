/*
  Členové rodiny Holasových, jejich kontakty a odkazy.
  Po kliknutí na lístek se otevře karta se jménem, kontakty a odkazy.
  Na kartě se ukáže jen to, co je vyplněné.

  Kontakty (pole "kontakty"):
    { typ: 'email', uzivatel: 'jmeno', domena: 'holasovi.net' }   -> jmeno@holasovi.net
    { typ: 'telefon', cislo: '+420 123 456 789' }
    { typ: 'datovka', id: 'abc1234' }   -> odkaz do veřejného seznamu datových schránek;
                                          overit: false = jen ID bez odkazu (schránka v seznamu není)
  E-mail je rozdělený na dvě části, aby ho roboti sbírající adresy hůř našli.
  Volitelně lze u kontaktu změnit popisek, např. popis: 'Pracovní e-mail'.

  Odkazy (pole "odkazy"), např. až bude mít člen vlastní web:
    { popis: 'Webová stránka', text: 'lukas.holasovi.net', url: 'https://lukas.holasovi.net' }
  Odkaz na jiný web se otevře v nové záložce, odkaz v rámci holasovi.net (adresa bez https://)
  ve stejné. Volitelně lze změnit ikonu: ikona: 'web' (výchozí), 'firma' nebo 'linkedin'.

  Polohy lístků jsou v procentech obrazu [vodorovně, svisle] pro tři verze malby
  (assets/img/motivy/<motiv>/..., platí pro všechny motivy, viz assets/js/motivy.js):
    ctverec  = ctverec.webp  (notebooky, běžné monitory, tablety na šířku)
    vyska    = vyska.webp    (mobily a tablety na výšku)
    panorama = panorama.webp (ultraširoké monitory a mobily na šířku)
  Polohy měňte jen tehdy, když se vymění celá malba.

  Písmeno je uprostřed lístku. Nesedí-li tam opticky (např. L s dlouhou patkou), lze ho posunout:
  posunPismene: [vodorovně, svisle] v procentech šířky lístku, záporné hodnoty doleva a nahoru.
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
      kontakty: [
        { typ: 'email', uzivatel: 'frantisek', domena: 'holasovi.net' },
        { typ: 'datovka', id: 'vefda5d' },
        { typ: 'telefon', cislo: '+420 776 280 026' }
      ],
      odkazy: [
        { popis: 'Webová stránka', text: 'frantisek.holasovi.net', url: 'https://frantisek.holasovi.net' },
        { popis: 'LinkedIn', text: 'František Holas', url: 'https://cz.linkedin.com/in/franti%C5%A1ek-holas-5353041b', ikona: 'linkedin' },
        { popis: 'Podnikatelský profil', text: 'IČO 88722520', url: 'frantisek-profil-88722520/', ikona: 'firma' }
      ]
    },
    {
      jmeno: 'Věrka',
      inicial: 'V',
      listek: 'červený',
      natoceni: -12,
      posunPismene: [0, 10],
      zare: 'rgba(255, 140, 120, 0.75)',
      poloha: { ctverec: [83.0, 48.53], vyska: [83.33, 42.5], panorama: [59.2, 49.37] },
      kontakty: [
        { typ: 'email', uzivatel: 'veruska', domena: 'holasovi.net' },
        { typ: 'datovka', id: '26ycu7i' }
      ],
      odkazy: [
        { popis: 'Podnikatelský profil', text: 'IČO 06635971', url: 'vera-profil-06635971/', ikona: 'firma' }
      ]
    },
    {
      jmeno: 'Lukáš',
      inicial: 'L',
      listek: 'zelený',
      natoceni: 8,
      posunPismene: [-12, 0],
      zare: 'rgba(190, 240, 140, 0.75)',
      poloha: { ctverec: [31.4, 43.2], vyska: [30.82, 38.15], panorama: [44.65, 42.55] },
      kontakty: [
        { typ: 'email', uzivatel: 'lukas', domena: 'holasovi.net' }
      ],
      odkazy: []
    },
    {
      jmeno: 'Radim',
      inicial: 'R',
      listek: 'žlutý',
      natoceni: -6,
      zare: 'rgba(255, 228, 140, 0.75)',
      poloha: { ctverec: [52.07, 35.0], vyska: [52.24, 34.0], panorama: [50.65, 35.37] },
      kontakty: [
        { typ: 'email', uzivatel: 'radim', domena: 'holasovi.net' }
      ],
      odkazy: []
    },
    {
      jmeno: 'Kristýna',
      inicial: 'K',
      listek: 'oranžový',
      natoceni: -6,
      zare: 'rgba(255, 190, 110, 0.75)',
      poloha: { ctverec: [69.4, 35.07], vyska: [69.71, 34.0], panorama: [55.4, 35.01] },
      kontakty: [
        { typ: 'email', uzivatel: 'kristyna', domena: 'holasovi.net' }
      ],
      odkazy: []
    }
  ]
};
