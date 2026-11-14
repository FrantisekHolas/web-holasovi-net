# holasovi.net

Rodinný rozcestník Holasových. Stránku tvoří jen malovaný strom: jeho koruna má pět barevných oblastí a v každé je jeden lístek s iniciálou člena rodiny.

| Lístek | Člen |
|---|---|
| modrozelený | František |
| červený | Věrka |
| zelený | Lukáš |
| žlutý | Radim |
| oranžový | Kristýna |

Po kliknutí na lístek se otevře karta se jménem, kontaktem a odkazy daného člena. Na kartě se ukáže jen to, co je vyplněné, takže například položka „Webová stránka“ se objeví až ve chvíli, kdy ji člen bude mít.

## Jak doplnit kontakt nebo odkaz

Všechno je v jediném souboru [`assets/js/clenove.js`](assets/js/clenove.js). U daného člena doplňte:

```js
kontakty: [
  { typ: 'email', uzivatel: 'lukas', domena: 'holasovi.net' },
  { typ: 'telefon', cislo: '+420 123 456 789' }
],
odkazy: [
  { popis: 'Webová stránka', text: 'lukas.holasovi.net', url: 'https://lukas.holasovi.net' }
]
```

E-mail je rozdělený na dvě části, aby ho roboti sbírající adresy hůř našli.

## Motivy podle období

Malba stromu se mění podle ročního období a svátků, podobně jako sváteční logo Googlu. Lístky, jména i karty zůstávají na stejném místě, mění se jen obraz.

| Motiv | Kdy | Malba |
|---|---|---|
| jaro, léto, podzim, zima | astronomicky, od okamžiku rovnodennosti nebo slunovratu (kolem 20. 3., 21. 6., 23. 9. a 21. 12.) | zatím jen podzim |
| Vánoce | 24.–26. 12. | zatím není |
| Silvestr a Nový rok | 31. 12.–1. 1., s ohňostrojem | zatím není |
| Velikonoce | Zelený čtvrtek – Velikonoční pondělí | zatím není |

Svátky mají přednost před ročním obdobím. Rozhoduje datum a čas v Česku. Dokud motiv nemá vlastní malbu, použije se malba ročního období a nakonec podzim.

Seznam motivů a jejich termíny jsou v [`assets/js/motivy.js`](assets/js/motivy.js). Nová malba se přidá takto:

1. V Gemini se upraví stávající podzimní malba (čtverec, na výšku i panorama zvlášť), aby kompozice, kmen a pět velkých lístků zůstaly na místě.
2. Malby se zarovnají na podzimní předlohu a uloží do `assets/img/motivy/<motiv>/` ve stejných rozměrech: `ctverec.webp` (1500 × 1500), `ctverec-900.webp`, `pozadi.webp` (48 px, rozmazané pozadí), `vyska.webp` (1116 × 2000), `vyska-720.webp`, `panorama.webp` (2000 × 557), `panorama-1200.webp`.
3. V `motivy.js` se u motivu doplní dodané verze, např. `obrazky: ['ctverec', 'vyska', 'panorama']`.

Vyzkoušet motiv předem jde přes adresu:

- `https://holasovi.net/?motiv=zima` ukáže zvolený motiv,
- `https://holasovi.net/?datum=2026-12-31T23:59:50` spustí stránku jako v daném okamžiku (český čas), včetně půlnočního ohňostroje.

**Ohňostroj** (`assets/js/ohnostroj.js`): rakety v barvách lístků startují samy a klepnutí na oblohu mimo lístky vypustí další. O půlnoci na Nový rok přijde dvanáctivteřinové finále. Dokud Silvestr nemá vlastní noční malbu, krajina se setmí a lístky svítí jako lucerny. Při zapnutém omezení pohybu v systému startují rakety jen po klepnutí.

## Jak web funguje

Statický web bez sestavování: HTML, CSS a malý skript. Nepoužívá cookies, měření návštěvnosti ani externí služby, písma jsou uložená přímo na webu.

Podle tvaru obrazovky se zobrazí jedna ze tří verzí malby:

| Obrazovka | Malba |
|---|---|
| mobil nebo tablet na výšku | `assets/img/motivy/<motiv>/vyska.webp` |
| notebook, běžný monitor, tablet na šířku | `assets/img/motivy/<motiv>/ctverec.webp`, okolí vyplní rozmazané pozadí |
| ultraširoký monitor (21:9, 32:9), mobil na šířku | `assets/img/motivy/<motiv>/panorama.webp` |

Polohy lístků pro každou verzi jsou v `assets/js/clenove.js` v procentech obrazu a platí pro všechny motivy. Při výměně celé malby je potřeba je přeměřit.

```
index.html              stránka
404.html                stránka „Tady nic neroste“
assets/css/styl.css     vzhled
assets/js/clenove.js    členové rodiny, kontakty a odkazy
assets/js/motivy.js     motivy podle ročního období a svátků
assets/js/obdobi.js     výběr motivu podle data (rovnodennosti, Velikonoce)
assets/js/ohnostroj.js  ohňostroj pro Silvestr a Nový rok
assets/js/strom.js      lístky a karta s kontaktem
assets/img/motivy/      malby stromu a pozadí pro jednotlivé motivy
assets/img/nahled.jpg   náhled pro sdílení odkazu
assets/fonts/           písma Cinzel, Cinzel Decorative a EB Garamond
```

## Zveřejnění na GitHub Pages

1. V repozitáři otevřete **Settings → Pages**.
2. V části **Build and deployment** zvolte **Source: Deploy from a branch**, vyberte větev s webem a složku **/ (root)**.
3. Web je hned k vyzkoušení na https://frantisekholas.github.io/web-holasovi-net/
4. Až bude nastavené DNS (níže), zadejte do **Custom domain** `holasovi.net` a uložte. GitHub tím do větve přidá soubor `CNAME`.
5. Jakmile GitHub ověří DNS, zapněte **Enforce HTTPS**.

GitHub Pages zdarma vyžaduje veřejný repozitář.

## Nastavení DNS u správce domény holasovi.net

Pro hlavní doménu `holasovi.net` (záznam `@`):

| Typ | Hodnota |
|---|---|
| A | 185.199.108.153 |
| A | 185.199.109.153 |
| A | 185.199.110.153 |
| A | 185.199.111.153 |
| AAAA | 2606:50c0:8000::153 |
| AAAA | 2606:50c0:8001::153 |
| AAAA | 2606:50c0:8002::153 |
| AAAA | 2606:50c0:8003::153 |

Pro `www.holasovi.net`: záznam **CNAME** s hodnotou `frantisekholas.github.io`.

Stávající záznamy pro `frantisek.holasovi.net` a pro e-mail (MX) nechte beze změny. Doporučujeme doménu ověřit v nastavení účtu GitHub (**Settings → Pages → Add a domain**), aby ji nemohl použít nikdo jiný.

## Původ obsahu

- Malby stromu byly vytvořeny v Google Gemini podle zadání rodiny.
- Písma Cinzel, Cinzel Decorative a EB Garamond jsou šířena pod licencí [SIL Open Font License 1.1](https://openfontlicense.org).
