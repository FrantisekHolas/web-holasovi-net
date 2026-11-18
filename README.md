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

## Podnikatelské profily

Na kartách Františka a Věrky je odkaz **Podnikatelský profil**:

| Člen | Stránka |
|---|---|
| František | https://holasovi.net/frantisek-profil-88722520/ |
| Věrka | https://holasovi.net/vera-profil-06635971/ |

Každý profil je česky, anglicky (`en/`) a německy (`de/`). Obsahuje údaje podle vzoru conceptual.cz: IČO, DIČ, plátcovství DPH, právní formu, místo a předmět podnikání (místo něj je sekce „Čím se zabývám“, u Františka podle profilu na LinkedIn), správce daně, bankovní účty zveřejněné v registru plátců DPH a kontakt včetně datové schránky, s odkazy do živnostenského rejstříku (RŽP), registru plátců DPH (ADIS), systému VIES a registru datových schránek.

- Stránky nemají logo a jsou černobílé. Světlý nebo tmavý režim se řídí prohlížečem, přepínač v záhlaví volbu změní a zapamatuje.
- Česká stránka pošle návštěvníka s anglickým nebo německým prohlížečem na jeho jazyk. Ruční volba jazyka se zapamatuje.
- IČO, DIČ, čísla účtů, IBAN a ID datové schránky jdou zkopírovat tlačítkem.
- Stránky se generují nástrojem [`nastroje/profily.py`](nastroje/profily.py) z údajů a překladů v něm; po změně stačí upravit tento soubor a spustit `python3 nastroje/profily.py`. Společný vzhled a skript jsou v `assets/profil/`, ikona každého profilu (lístek se zlatou iniciálou) v jeho složce `ikony/`.
- Údaje jsou z ARES, živnostenského rejstříku, registru plátců DPH a seznamu datových schránek ke 14. 11. 2026.

V kartách na stromě jsou i osobní datové schránky (`{ typ: 'datovka', id: '…' }` v `clenove.js`). Odkaz do registru se ukáže jen u schránky, která je ve veřejném seznamu; jinak (`overit: false`) jen její ID.

## Motivy podle období

Malba stromu se mění podle ročního období a svátků, podobně jako sváteční logo Googlu. Lístky, jména i karty zůstávají na stejném místě, mění se jen obraz.

| Motiv | Kdy | Malba |
|---|---|---|
| jaro, léto, podzim, zima | astronomicky, od okamžiku rovnodennosti nebo slunovratu (kolem 20. 3., 21. 6., 23. 9. a 21. 12.) | všechna čtyři |
| Vánoce | od 1. adventní neděle do 30. 12. | ano (noční malba, v noci se už neztmavuje) |
| Silvestr a Nový rok | 31. 12.–1. 1., s ohňostrojem | vlastní není, použije se zima v nočním režimu |
| Velikonoce | Zelený čtvrtek – Velikonoční pondělí | ano (vajíčka, stužky a zajíci) |
| Narozeniny Kristýny | 14. 8. | ano (oslava s morčaty; panorama složené ze čtverce a letního panoramatu); Kristýnino písmeno K je růžové |
| Narozeniny Lukáše | 2. 9. | ano (rytíř se zajícem; panorama složené ze čtverce a letního panoramatu); Lukášovo písmeno L je růžové |
| Narozeniny Radima | 16. 11. | ano (oslava pod stromem); Radimovo písmeno R je růžové |
| Mikuláš | 5. 12. | čtverec a panorama (děti jako Mikuláš, anděl a čert, morčata s nadílkou); na výšku zatím podzim |
| Narozeniny Věrky | 9. 12. | ano (noční malba); Věrčino písmeno V je růžové |

**Chybějící malby** (doplnit nástrojem `nastroje/priprav-motiv.py`, pak do `obrazky` v `motivy.js`):

| Motiv | Chybí | Poznámka |
|---|---|---|
| Mikuláš (5. 12.) | výška | v Gemini ze zimní výšky a schváleného čtverce; Silvestr záměrně používá zimu |

**Panorama ze čtverce:** strom v panoramatu je strom ze čtverce zmenšený na výšku panoramatu (měřítko asi 0,371 × 0,381, čtverec vlevo na x ≈ 723 px v rozměru 2000 × 557; ve velké verzi 3904 × 1088 čtverec 2048 px zmenšený na 1086 × 1117 na x ≈ 1411). Když se panorama v Gemini nepovede, dá se složit: schválený čtverec doprostřed panoramatu ročního období s měkkým přechodem po stranách; lístky pak sedí do 1 %. Tak vznikla panoramata Narozenin Kristýny a Lukáše (z léta) a Mikuláše (ze zimy).

**Originály maleb** (z Gemini v plném rozlišení: čtverec 2048 × 2048, výška 1536 × 2752, panorama 3904 × 1088) jsou v soukromém repozitáři `FrantisekHolas/my-cloud`, složka `web-holasovi-net/`. Do tohoto veřejného repozitáře se nenahrávají. Přes chat se obrázky zmenšují, proto se malby zpracovávají z originálů. Ruční retuše (druhé slunce v letním panoramatu, čtvrtý sob na Vánocích a u Narozenin Věrky na výšku) se při novém zpracování přenášejí z dosavadní malby.

Svátky mají přednost před ročním obdobím. Když se termíny překrývají (narozeniny 9. 12. v Adventu), platí motiv, který je v `motivy.js` výš. Rozhoduje datum a čas v Česku. Dokud motiv nemá vlastní malbu, použije se malba ročního období a nakonec podzim.

**Oslavenec:** motiv může mít `oslavenec: 'Věrka'` (jméno z `clenove.js`). Ten den je písmeno na lístku oslavence růžové místo zlatého (barva je v `index.html`, `pismo-oslavence`). Vyzkoušení: `https://holasovi.net/?datum=2026-12-09`.

Seznam motivů a jejich termíny jsou v [`assets/js/motivy.js`](assets/js/motivy.js). Nová malba se přidá takto:

1. V Gemini se upraví stávající podzimní malba (čtverec, na výšku i panorama zvlášť), aby kompozice, kmen a pět velkých lístků zůstaly na místě.
2. Nástroj [`nastroje/priprav-motiv.py`](nastroje/priprav-motiv.py) změří polohu lístků proti podzimní předloze, malby srovná a uloží do `assets/img/motivy/<motiv>/` ve všech velikostech (`ctverec.webp` 1500 × 1500, `ctverec-900.webp`, `ctverec-2048.webp`, `pozadi.webp`, `vyska.webp` 1116 × 2000, `vyska-720.webp`, `vyska-1536.webp`, `panorama.webp` 2000 × 557, `panorama-1200.webp`, `panorama-3904.webp`). Všechny velikosti počítá z dodané malby jediným převzorkováním, proto je nejlepší originál v plném rozlišení. Malbu v jiném poměru stran (např. čtverec dodaný jako 3:2) převede podle lístků, jen bude méně ostrá. Když některý lístek nesedí nebo by se velká verze musela zvětšovat, upozorní na to.
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

Každá verze je ve třech velikostech a prohlížeč si vybere podle velikosti a jemnosti obrazovky. Velkou verzi (`ctverec-2048`, `vyska-1536`, `panorama-3904`) dostanou jen velké obrazovky: čtverec notebook s jemným displejem nebo velký monitor, výška tablet na výšku (od šířky 700 px), panorama monitor od šířky 1200 px. Mobil stahuje dál základní velikost.

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
vera-profil-06635971/       podnikatelský profil Věrky (cs, en/, de/)
assets/profil/              společný vzhled, skript a písmo Inter profilů
nastroje/priprav-motiv.py  příprava maleb nového motivu (není součástí webu)
nastroje/profily.py        generátor podnikatelských profilů (není součástí webu)
.github/workflows/zverejneni.yml  zveřejnění webu na GitHub Pages (jen soubory webu)
```

## Zveřejnění na GitHub Pages

Web zveřejňuje úloha GitHub Actions `.github/workflows/zverejneni.yml` po každém nahrání do `main` (ručně: záložka **Actions → Zveřejnění webu → Run workflow**). Zveřejní jen soubory webu: `README.md`, složka `nastroje/` a nastavení repozitáře (`.github`, `.gitignore`) na webu nejsou. Co se nezveřejňuje, je v úloze v seznamu `VYNECHAT`; nový soubor, který na web nepatří, je potřeba do seznamu doplnit.

1. V repozitáři otevřete **Settings → Pages**.
2. V části **Build and deployment** zvolte **Source: GitHub Actions**.
3. Až bude nastavené DNS (níže), zadejte do **Custom domain** `holasovi.net` a uložte (soubor `CNAME` v repozitáři je jen pro přehled).
4. Jakmile GitHub ověří DNS, zapněte **Enforce HTTPS**.

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
