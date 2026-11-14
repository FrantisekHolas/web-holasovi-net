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

## Podnikatelský profil Františka

Na kartě Františka je odkaz **Podnikatelský profil** na stránku https://holasovi.net/frantisek-profil-88722520/ (anglicky `en/`, německy `de/`). Obsahuje údaje podle vzoru conceptual.cz: IČO, DIČ, plátcovství DPH, právní formu, místo a předmět podnikání, správce daně, bankovní účty zveřejněné v registru plátců DPH a kontakt včetně datové schránky, s odkazy do živnostenského rejstříku (RŽP), registru plátců DPH (ADIS), systému VIES a registru datových schránek.

- Stránka nemá logo a je černobílá. Světlý nebo tmavý režim se řídí prohlížečem, přepínač v záhlaví volbu změní a zapamatuje.
- Česká stránka pošle návštěvníka s anglickým nebo německým prohlížečem na jeho jazyk. Ruční volba jazyka se zapamatuje.
- IČO, DIČ, čísla účtů a IBAN jdou zkopírovat tlačítkem.
- Stránky se generují nástrojem [`nastroje/profil-frantisek.py`](nastroje/profil-frantisek.py) z údajů a překladů v něm; po změně stačí upravit tento soubor a spustit `python3 nastroje/profil-frantisek.py`. Vzhled a skript jsou ve `frantisek-profil-88722520/assets/`.
- Údaje jsou z ARES, živnostenského rejstříku a registru plátců DPH ke 14. 11. 2026.

## Motivy podle období

Malba stromu se mění podle ročního období a svátků, podobně jako sváteční logo Googlu. Lístky, jména i karty zůstávají na stejném místě, mění se jen obraz.

| Motiv | Kdy | Malba |
|---|---|---|
| jaro, léto, podzim, zima | astronomicky, od okamžiku rovnodennosti nebo slunovratu (kolem 20. 3., 21. 6., 23. 9. a 21. 12.) | všechna čtyři |
| Vánoce | 24.–26. 12. | ano (noční malba, v noci se už neztmavuje) |
| Silvestr a Nový rok | 31. 12.–1. 1., s ohňostrojem | zatím není (použije se zima v nočním režimu) |
| Velikonoce | Zelený čtvrtek – Velikonoční pondělí | zatím není (použije se jaro) |

Svátky mají přednost před ročním obdobím. Rozhoduje datum a čas v Česku. Dokud motiv nemá vlastní malbu, použije se malba ročního období a nakonec podzim.

Seznam motivů a jejich termíny jsou v [`assets/js/motivy.js`](assets/js/motivy.js). Nová malba se přidá takto:

1. V Gemini se upraví stávající podzimní malba (čtverec, na výšku i panorama zvlášť), aby kompozice, kmen a pět velkých lístků zůstaly na místě.
2. Nástroj [`nastroje/priprav-motiv.py`](nastroje/priprav-motiv.py) změří polohu lístků proti podzimní předloze, malby srovná a uloží do `assets/img/motivy/<motiv>/` ve všech velikostech (`ctverec.webp` 1500 × 1500, `ctverec-900.webp`, `pozadi.webp`, `vyska.webp` 1116 × 2000, `vyska-720.webp`, `panorama.webp` 2000 × 557, `panorama-1200.webp`). Malbu v jiném poměru stran (např. čtverec dodaný jako 3:2) převede podle lístků, jen bude méně ostrá. Když některý lístek nesedí, upozorní na to.
   ```
   python3 nastroje/priprav-motiv.py zima --ctverec ctverec.jpg --vyska vyska.jpg --panorama panorama.jpg
   ```
   Potřebuje Python 3 s balíčky pillow, numpy a opencv-python.
3. V `motivy.js` se u motivu doplní dodané verze, např. `obrazky: ['ctverec', 'vyska', 'panorama']`.

Vyzkoušet motiv předem jde přes adresu:

- `https://holasovi.net/?motiv=zima` ukáže zvolený motiv,
- `https://holasovi.net/?datum=2026-12-31T23:59:50` spustí stránku jako v daném okamžiku (český čas), včetně půlnočního ohňostroje.

**Den a noc:** večer se strom podle skutečného slunce nad Brnem postupně stmívá. Krajina potemní, obloha zmodrá a lístky svítí jako lucerny. Ráno se zase rozjasní. Soumrak začíná, když je slunce 2° nad obzorem, plná noc nastane při 8° pod obzorem (v listopadu zhruba 16:00–17:00). Otevřená stránka se přepočítává každou minutu. Místo je v `motivy.js` (`misto`). Motiv může mít `noc: 'vzdy'` (celý den noční režim) nebo `noc: 'malba'` (malba je sama noční, nic se neztmavuje). Vyzkoušení: `?noc=1` (noc), `?noc=0.5` (šero), `?noc=0` (den).

**Ohňostroj** (`assets/js/ohnostroj.js`): na Silvestra a na Nový rok celý den. Rakety v barvách lístků startují samy a klepnutí na oblohu mimo lístky vypustí další. O půlnoci na Nový rok přijde dvanáctivteřinové finále. Oba dny je strom v nočním režimu, aby ohňostroj vynikl. Při zapnutém omezení pohybu v systému startují rakety jen po klepnutí.

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
frantisek-profil-88722520/  podnikatelský profil Františka (cs, en/, de/)
nastroje/priprav-motiv.py  příprava maleb nového motivu (není součástí webu)
nastroje/profil-frantisek.py  generátor podnikatelského profilu (není součástí webu)
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
- Písma Cinzel, Cinzel Decorative, EB Garamond a Inter (podnikatelský profil) jsou šířena pod licencí [SIL Open Font License 1.1](https://openfontlicense.org).
