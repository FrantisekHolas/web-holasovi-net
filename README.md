# holasovi.net

Rodinný rozcestník Holasových. Stránku tvoří jen malovaný strom: jeho koruna má pět barevných oblastí a v každé je jeden lístek s iniciálou člena rodiny.

| Lístek | Člen |
|---|---|
| modrozelený | František |
| červený | Věrka |
| zelený | Lukáš |
| žlutý | Radim |
| oranžový | Kristýna |

Lístek, ke kterému patří odkaz, je klikací a otevře kartu s odkazy. Lístek bez odkazu je jen ozdobou.

## Jak přidat odkaz

Všechno je v jediném souboru [`assets/js/clenove.js`](assets/js/clenove.js). U daného člena doplňte do pole `odkazy` položku, například:

```js
odkazy: [
  { popis: 'Webová stránka', text: 'lukas.holasovi.net', url: 'https://lukas.holasovi.net' }
]
```

Jakmile má člen aspoň jeden odkaz, jeho lístek začne fungovat.

## Jak web funguje

Statický web bez sestavování: HTML, CSS a malý skript. Nepoužívá cookies, měření návštěvnosti ani externí služby, písma jsou uložená přímo na webu.

Podle tvaru obrazovky se zobrazí jedna ze tří verzí malby:

| Obrazovka | Malba |
|---|---|
| mobil nebo tablet na výšku | `assets/img/strom-na-vysku.webp` |
| notebook, běžný monitor, tablet na šířku | `assets/img/strom-ctverec.webp`, okolí vyplní rozmazané pozadí |
| ultraširoký monitor (21:9, 32:9), mobil na šířku | `assets/img/strom-panorama.webp` |

Polohy lístků pro každou verzi jsou v `assets/js/clenove.js` v procentech obrazu. Při výměně malby je potřeba je přeměřit.

```
index.html              stránka
404.html                stránka „Tady nic neroste“
assets/css/styl.css     vzhled
assets/js/clenove.js    členové rodiny a jejich odkazy
assets/js/strom.js      lístky a karta s odkazy
assets/img/             malby stromu, pozadí a náhled pro sdílení
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
