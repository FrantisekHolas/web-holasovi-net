#!/usr/bin/env python3
"""
Vygeneruje podnikatelský profil Mgr. Františka Holase ve třech jazycích:
  frantisek-profil-88722520/index.html     (čeština)
  frantisek-profil-88722520/en/index.html  (angličtina)
  frantisek-profil-88722520/de/index.html  (němčina)

Údaje jsou z veřejných rejstříků (ARES, živnostenský rejstřík, registr plátců DPH v ADIS)
ke dni uvedenému v ZDROJ_DATUM. Po změně údajů nebo textů upravte tento soubor a spusťte:
  python3 nastroje/profil-frantisek.py

Vzhled a chování stránky jsou ve frantisek-profil-88722520/assets/ (profil.css, profil.js).
"""
import json
import os

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLOZKA = 'frantisek-profil-88722520'
ADRESA = 'https://holasovi.net/' + SLOZKA + '/'

# ---------- Údaje (z rejstříků) ----------
ICO = '88722520'
DIC = 'CZ8306023825'
JMENO = 'František Holas'
TITUL = 'Mgr.'
ULICE = 'Slezákova 999/25'
CAST = 'Husovice'
PSC = '613 00'
MESTO = 'Brno'
EMAIL = 'frantisek@holasovi.net'
TELEFON = '+420 776 280 026'
ZDROJ_DATUM = '2026-11-14'
UCTY = [
    # číslo účtu, IBAN, banka, BIC, zveřejněno v registru plátců DPH
    ('1037342017/3030', 'CZ72 3030 0000 0010 3734 2017', 'Air Bank a.s.', 'AIRACZPP', '2013-06-20'),
    ('1037342033/3030', 'CZ28 3030 0000 0010 3734 2033', 'Air Bank a.s.', 'AIRACZPP', '2021-12-10'),
]
ODKAZ_RZP = 'https://rzp.gov.cz/verejne-udaje/cs/udaje/vyber-subjektu;ico=' + ICO
ODKAZ_ADIS = 'https://adisspr.mfcr.cz/dpr/DphReg?id=1&pocet=1&fu=&OK=+Search+&ZPRAC=RDPHI1&dic=' + DIC[2:]
ODKAZ_VIES = 'https://ec.europa.eu/taxation_customs/vies/#/vat-validation'
ODKAZ_MAPY = 'https://www.google.com/maps/search/?api=1&query=Slez%C3%A1kova%20999%2F25%2C%20613%2000%20Brno'

# ---------- Texty ----------
MESICE = {
    'cs': ['ledna', 'února', 'března', 'dubna', 'května', 'června', 'července', 'srpna', 'září', 'října', 'listopadu', 'prosince'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
}

T = {
    'cs': {
        'locale': 'cs_CZ', 'nazev': 'Mgr. František Holas | podnikatel, Brno',
        'popis': 'Mgr. František Holas, podnikatel, IČO 88722520, DIČ CZ8306023825, Slezákova 999/25, 613 00 Brno. Údaje o podnikateli, bankovní účty a kontakt.',
        'og_popis': 'Údaje o podnikateli, bankovní účty a kontakt. IČO 88722520, Brno.',
        'preskocit': 'Přejít na obsah', 'nav': 'Hlavní navigace', 'nav_udaje': 'Údaje', 'nav_ucty': 'Bankovní účty', 'nav_kontakt': 'Kontakt',
        'jazyk': 'Jazyk', 'na_tmavy': 'Přepnout na tmavý režim', 'na_svetly': 'Přepnout na světlý režim', 'rezim': 'Tmavý režim',
        'zacatek': 'na začátek stránky',
        'eyebrow': 'Brno, Česká republika · od roku 2012',
        'lead': 'Podnikající fyzická osoba zapsaná v&nbsp;živnostenském rejstříku, plátce DPH.',
        'btn_vypis': 'Výpis ze živnostenského rejstříku',
        'h_udaje': 'Údaje o&nbsp;podnikateli',
        'jmeno': 'Obchodní jméno', 'ico': 'IČO', 'rzp': 'Živnostenský rejstřík', 'dic': 'DIČ',
        'adis': 'Registr plátců DPH (ADIS)', 'vies': 'Ověření ve VIES (EU)',
        'dic_pozn': 'V&nbsp;ADIS i&nbsp;VIES zadejte číslo 8306023825 (ve VIES členský stát CZ).',
        'dph': 'Plátce DPH', 'dph_hodnota': 'ano, od {d}', 'dph_pozn': 'spolehlivý plátce (není veden jako nespolehlivý)',
        'forma': 'Právní forma', 'forma_hodnota': 'Fyzická osoba podnikající dle živnostenského zákona',
        'vznik': 'Podnikání od', 'misto': 'Místo podnikání', 'stat': 'Česká republika', 'mapy': 'Zobrazit v&nbsp;Mapách <span class="nowrap">Google{ext}</span>',
        'predmet': 'Předmět podnikání',
        'predmet_hodnota': 'Výroba, obchod a služby neuvedené v&nbsp;přílohách 1 až 3 živnostenského zákona',
        'predmet_pozn': 'živnost volná', 'obory': 'Obory činnosti:',
        'obory_seznam': [
            'Výzkum a vývoj v&nbsp;oblasti přírodních a technických věd nebo společenských věd',
            'Zprostředkování obchodu a služeb',
            'Výroba, obchod a služby jinde nezařazené',
            'Velkoobchod a maloobchod',
            'Poradenská a konzultační činnost, zpracování odborných studií a posudků',
            'Poskytování software, poradenství v&nbsp;oblasti informačních technologií, zpracování dat, hostingové a související činnosti a webové portály',
        ],
        'spravce': 'Správce daně', 'spravce_hodnota': 'Finanční úřad pro Jihomoravský kraj', 'spravce_pozn': 'Územní pracoviště Brno III',
        'h_ucty': 'Bankovní účty',
        'ucty_uvod': 'Účty zveřejněné správcem daně v&nbsp;registru plátců DPH.',
        'ucet': 'Účet', 'cislo': 'Číslo účtu', 'banka': 'Banka', 'zverejneno': 'Zveřejněno',
        'zdroj': 'Podle registru plátců DPH ke dni {d}. Aktuální stav ověříte v&nbsp;<a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">registru <span class="nowrap">ADIS{ext}</span></a>.',
        'kopirovat': 'Kopírovat', 'zkopirovano': 'Zkopírováno', 'kop_ico': 'Kopírovat IČO', 'kop_dic': 'Kopírovat DIČ',
        'kop_cislo': 'Kopírovat číslo účtu', 'kop_iban': 'Kopírovat IBAN',
        'h_kontakt': 'Kontakt', 'role': 'podnikatel', 'email': 'E-mail', 'telefon': 'Telefon',
        'rodina': 'Rodinný strom Holasových',
    },
    'en': {
        'locale': 'en_US', 'nazev': 'Mgr. František Holas | Sole trader, Brno',
        'popis': 'Mgr. František Holas, sole trader, Business ID (IČO) 88722520, VAT ID CZ8306023825, Slezákova 999/25, 613 00 Brno, Czech Republic. Business details, bank accounts and contact.',
        'og_popis': 'Business details, bank accounts and contact. Business ID 88722520, Brno.',
        'preskocit': 'Skip to content', 'nav': 'Main navigation', 'nav_udaje': 'Details', 'nav_ucty': 'Bank accounts', 'nav_kontakt': 'Contact',
        'jazyk': 'Language', 'na_tmavy': 'Switch to dark mode', 'na_svetly': 'Switch to light mode', 'rezim': 'Dark mode',
        'zacatek': 'back to top',
        'eyebrow': 'Brno, Czech Republic · since 2012',
        'lead': 'Self-employed person (sole trader) registered in the Czech Trade Register, VAT payer.',
        'btn_vypis': 'Trade Register extract',
        'h_udaje': 'Business details',
        'jmeno': 'Business name', 'ico': 'Business ID (IČO)', 'rzp': 'Trade Register (in Czech)', 'dic': 'VAT ID (DIČ)',
        'adis': 'Czech VAT register (ADIS, in Czech)', 'vies': 'Check in VIES (EU)',
        'dic_pozn': 'In ADIS and VIES, enter the number 8306023825 (in VIES with Member State CZ).',
        'dph': 'VAT status', 'dph_hodnota': 'VAT payer since {d}', 'dph_pozn': 'reliable VAT payer (not listed as unreliable)',
        'forma': 'Legal form', 'forma_hodnota': 'Natural person doing business under the Czech Trade Licensing Act',
        'vznik': 'In business since', 'misto': 'Place of business', 'stat': 'Czech Republic', 'mapy': 'View on Google <span class="nowrap">Maps{ext}</span>',
        'predmet': 'Scope of business',
        'predmet_hodnota': 'Production, trade and services not listed in Annexes 1 to 3 of the Trade Licensing Act',
        'predmet_pozn': 'unregulated trade (živnost volná)', 'obory': 'Fields of activity:',
        'obory_seznam': [
            'Research and development in the natural and technical sciences or the social sciences',
            'Intermediation of trade and services',
            'Production, trade and services not elsewhere classified',
            'Wholesale and retail trade',
            'Advisory and consulting services, preparation of expert studies and reports',
            'Provision of software, IT consulting, data processing, hosting and related activities and web portals',
        ],
        'spravce': 'Tax office', 'spravce_hodnota': 'Tax Office for the South Moravian Region', 'spravce_pozn': 'Regional office Brno III (Finanční úřad pro Jihomoravský kraj, Územní pracoviště Brno III)',
        'h_ucty': 'Bank accounts',
        'ucty_uvod': 'Accounts published by the tax authority in the Czech VAT payer register.',
        'ucet': 'Account', 'cislo': 'Account number', 'banka': 'Bank', 'zverejneno': 'Published',
        'zdroj': 'According to the Czech VAT payer register as of {d}. Check the current status in the <a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">ADIS <span class="nowrap">register{ext}</span></a>.',
        'kopirovat': 'Copy', 'zkopirovano': 'Copied', 'kop_ico': 'Copy Business ID', 'kop_dic': 'Copy VAT ID',
        'kop_cislo': 'Copy account number', 'kop_iban': 'Copy IBAN',
        'h_kontakt': 'Contact', 'role': 'Sole trader', 'email': 'Email', 'telefon': 'Phone',
        'rodina': 'Holas family tree',
    },
    'de': {
        'locale': 'de_DE', 'nazev': 'Mgr. František Holas | Einzelunternehmer, Brno',
        'popis': 'Mgr. František Holas, Einzelunternehmer, Ident.-Nr. (IČO) 88722520, USt-IdNr. CZ8306023825, Slezákova 999/25, 613 00 Brno, Tschechische Republik. Unternehmensangaben, Bankkonten und Kontakt.',
        'og_popis': 'Unternehmensangaben, Bankkonten und Kontakt. Ident.-Nr. 88722520, Brno.',
        'preskocit': 'Zum Inhalt springen', 'nav': 'Hauptnavigation', 'nav_udaje': 'Angaben', 'nav_ucty': 'Bankkonten', 'nav_kontakt': 'Kontakt',
        'jazyk': 'Sprache', 'na_tmavy': 'Dunkles Design einschalten', 'na_svetly': 'Helles Design einschalten', 'rezim': 'Dunkles Design',
        'zacatek': 'zum Seitenanfang',
        'eyebrow': 'Brno, Tschechische Republik · seit 2012',
        'lead': 'Selbständig tätige natürliche Person (Einzelunternehmer), eingetragen im tschechischen Gewerberegister, umsatzsteuerpflichtig.',
        'btn_vypis': 'Gewerberegisterauszug',
        'h_udaje': 'Unternehmensangaben',
        'jmeno': 'Geschäftsname', 'ico': 'Ident.-Nr. (IČO)', 'rzp': 'Gewerberegister (auf Tschechisch)', 'dic': 'USt-IdNr. (DIČ)',
        'adis': 'Tschechisches USt-Register (ADIS, auf Tschechisch)', 'vies': 'Prüfung in VIES (EU)',
        'dic_pozn': 'In ADIS und VIES die Nummer 8306023825 eingeben (in VIES mit Mitgliedstaat CZ).',
        'dph': 'Umsatzsteuer', 'dph_hodnota': 'umsatzsteuerpflichtig seit {d}', 'dph_pozn': 'zuverlässiger Steuerzahler (nicht als unzuverlässig geführt)',
        'forma': 'Rechtsform', 'forma_hodnota': 'Natürliche Person, gewerbetätig nach dem tschechischen Gewerbegesetz',
        'vznik': 'Geschäftstätig seit', 'misto': 'Ort der Geschäftstätigkeit', 'stat': 'Tschechische Republik', 'mapy': 'In Google Maps <span class="nowrap">anzeigen{ext}</span>',
        'predmet': 'Gegenstand der Tätigkeit',
        'predmet_hodnota': 'Herstellung, Handel und Dienstleistungen, die nicht in den Anlagen 1 bis 3 des Gewerbegesetzes aufgeführt sind',
        'predmet_pozn': 'freies Gewerbe (živnost volná)', 'obory': 'Tätigkeitsbereiche:',
        'obory_seznam': [
            'Forschung und Entwicklung in den Natur- und Technikwissenschaften oder den Sozialwissenschaften',
            'Vermittlung von Handel und Dienstleistungen',
            'Herstellung, Handel und Dienstleistungen, anderweitig nicht genannt',
            'Groß- und Einzelhandel',
            'Beratungs- und Konsultationstätigkeit, Erstellung von Fachstudien und Gutachten',
            'Bereitstellung von Software, IT-Beratung, Datenverarbeitung, Hosting und damit verbundene Tätigkeiten sowie Webportale',
        ],
        'spravce': 'Zuständiges Finanzamt', 'spravce_hodnota': 'Finanzamt für die Region Südmähren', 'spravce_pozn': 'Dienststelle Brno III (Finanční úřad pro Jihomoravský kraj, Územní pracoviště Brno III)',
        'h_ucty': 'Bankkonten',
        'ucty_uvod': 'Vom Finanzamt im tschechischen Register der Umsatzsteuerpflichtigen veröffentlichte Konten.',
        'ucet': 'Konto', 'cislo': 'Kontonummer', 'banka': 'Bank', 'zverejneno': 'Veröffentlicht',
        'zdroj': 'Laut tschechischem Register der Umsatzsteuerpflichtigen, Stand {d}. Den aktuellen Stand prüfen Sie im <a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">ADIS-<span class="nowrap">Register{ext}</span></a>.',
        'kopirovat': 'Kopieren', 'zkopirovano': 'Kopiert', 'kop_ico': 'Ident.-Nr. kopieren', 'kop_dic': 'USt-IdNr. kopieren',
        'kop_cislo': 'Kontonummer kopieren', 'kop_iban': 'IBAN kopieren',
        'h_kontakt': 'Kontakt', 'role': 'Einzelunternehmer', 'email': 'E-Mail', 'telefon': 'Telefon',
        'rodina': 'Stammbaum der Familie Holas',
    },
}

AKTUALNI = ' aria-current="page"'

# ---------- Ikony ----------
def svg(obsah, trida=''):
    t = f' class="{trida}"' if trida else ''
    return (f'<svg{t} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{obsah}</svg>')

EXT = svg('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>')
MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="2"/><polyline points="3 7 12 13 21 7"/>')
TELEFON_IKONA = svg('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>')
KOPIE = svg('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>')
MESIC = svg('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>', 'ikona-mesic')
SLUNCE = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>', 'ikona-slunce')


def datum(iso, jazyk):
    r, m, d = (int(x) for x in iso.split('-'))
    mesic = MESICE[jazyk][m - 1]
    if jazyk == 'en':
        return f'<time datetime="{iso}">{mesic}&nbsp;{d}, {r}</time>'
    return f'<time datetime="{iso}">{d}.&nbsp;{mesic} {r}</time>'


def kopirovat(t, hodnota, popis):
    return (f'<button class="kopirovat" type="button" data-kopirovat="{hodnota}" data-text="{t["kopirovat"]}" '
            f'data-hotovo="{t["zkopirovano"]}" aria-label="{popis}">{KOPIE}<span class="kopirovat__text">{t["kopirovat"]}</span></button>')


def odkaz_ven(href, text, trida='ext', hreflang='cs'):
    # poslední slovo spolu s ikonou nezalomit
    slova = text.rsplit(' ', 1)
    if len(slova) == 2:
        text = f'{slova[0]} <span class="nowrap">{slova[1]}{EXT}</span>'
    else:
        text = f'<span class="nowrap">{text}{EXT}</span>'
    jazyk = f' hreflang="{hreflang}"' if hreflang else ''
    return f'<a class="{trida}" href="{href.replace("&", "&amp;")}" target="_blank" rel="noopener"{jazyk}>{text}</a>'


def stranka(jazyk):
    t = T[jazyk]
    k = '' if jazyk == 'cs' else '../'          # cesta ke kořeni profilu
    url = ADRESA + ('' if jazyk == 'cs' else jazyk + '/')
    jazyky = [('cs', 'CS', 'Čeština'), ('en', 'EN', 'English'), ('de', 'DE', 'Deutsch')]
    prepinac = '\n'.join(
        f'          <a href="{"./" if j == jazyk else (k if j == "cs" else k + j + "/")}" hreflang="{j}" lang="{j}" '
        f'data-set-lang="{j}" aria-label="{nazev}" title="{nazev}"{AKTUALNI if j == jazyk else ""}>{zkr}</a>'
        for j, zkr, nazev in jazyky)
    alternativy = '\n'.join(f'  <link rel="alternate" hreflang="{j}" href="{ADRESA}{"" if j == "cs" else j + "/"}">' for j, _, _ in jazyky)
    obory = '\n'.join(f'                <li>{o}</li>' for o in t['obory_seznam'])

    ucty = []
    for i, (cislo, iban, banka, bic, zverejneno) in enumerate(UCTY, 1):
        ucty.append(f'''          <div class="card ucet">
            <h3>{t["ucet"]} {i}</h3>
            <dl>
              <dt>{t["cislo"]}</dt>
              <dd><span class="num">{cislo}</span>{kopirovat(t, cislo, t["kop_cislo"])}</dd>
              <dt>IBAN</dt>
              <dd><span class="num">{iban.replace(" ", "&nbsp;")}</span>{kopirovat(t, iban.replace(" ", ""), t["kop_iban"])}</dd>
              <dt>BIC (SWIFT)</dt>
              <dd>{bic}</dd>
              <dt>{t["banka"]}</dt>
              <dd class="slabe">{banka}</dd>
              <dt>{t["zverejneno"]}</dt>
              <dd class="slabe">{datum(zverejneno, jazyk)}</dd>
            </dl>
          </div>''')
    ucty = '\n'.join(ucty)

    ld = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': f'{TITUL} {JMENO}',
        'honorificPrefix': TITUL,
        'givenName': 'František',
        'familyName': 'Holas',
        'url': url,
        'email': EMAIL,
        'telephone': TELEFON.replace(' ', ''),
        'vatID': DIC,
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'IČO', 'value': ICO},
        'address': {'@type': 'PostalAddress', 'streetAddress': ULICE, 'addressLocality': MESTO,
                    'postalCode': PSC, 'addressCountry': 'CZ'},
    }
    ld = json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n  ')
    ext = EXT

    return f'''<!doctype html>
<html lang="{jazyk}"{" data-lang-auto" if jazyk == "cs" else ""}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Vygenerováno nástrojem nastroje/profil-frantisek.py – ručně neupravovat. -->
  <script src="{k}assets/profil.js"></script>
  <title>{t["nazev"]}</title>
  <meta name="description" content="{t["popis"]}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f0f0f" media="(prefers-color-scheme: dark)">

{alternativy}
  <link rel="alternate" hreflang="x-default" href="{ADRESA}">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="profile">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{t["locale"]}">
  <meta property="og:title" content="{TITUL} {JMENO}">
  <meta property="og:description" content="{t["og_popis"]}">

  <link rel="icon" type="image/png" sizes="32x32" href="{k}assets/favicon-32.png">
  <link rel="icon" type="image/png" sizes="64x64" href="{k}assets/favicon-64.png">
  <link rel="apple-touch-icon" href="{k}assets/apple-touch-icon.png">
  <link rel="preload" href="{k}assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{k}assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{k}assets/profil.css">

  <script type="application/ld+json">
  {ld}
  </script>
</head>
<body>
  <a class="skip" href="#main">{t["preskocit"]}</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="#" aria-label="{TITUL} {JMENO}, {t["zacatek"]}">{JMENO}</a>
      <div class="header-end">
        <nav class="nav" aria-label="{t["nav"]}">
          <a href="#udaje">{t["nav_udaje"]}</a>
          <a href="#ucty">{t["nav_ucty"]}</a>
          <a href="#kontakt">{t["nav_kontakt"]}</a>
        </nav>
        <nav class="lang" aria-label="{t["jazyk"]}">
{prepinac}
        </nav>
        <button class="vzhled" type="button" aria-label="{t["rezim"]}" aria-pressed="false" data-na-tmavy="{t["na_tmavy"]}" data-na-svetly="{t["na_svetly"]}" title="{t["na_tmavy"]}">
          {MESIC}
          {SLUNCE}
        </button>
      </div>
    </div>
  </header>

  <main id="main">
    <section class="hero">
      <div class="wrap">
        <p class="eyebrow">{t["eyebrow"]}</p>
        <h1><span class="titul">{TITUL}</span> {JMENO.replace(" ", "&nbsp;")}</h1>
        <p class="lead">{t["lead"]}</p>
        <div class="actions">
          <a class="btn primary" href="#kontakt">
            {MAIL}
            {t["nav_kontakt"]}
          </a>
          <a class="btn" href="{ODKAZ_RZP}" target="_blank" rel="noopener" hreflang="cs">
            {t["btn_vypis"]}
            {EXT}
          </a>
        </div>
      </div>
    </section>

    <section class="block soft" id="udaje" aria-labelledby="udaje-h">
      <div class="wrap">
        <h2 id="udaje-h">{t["h_udaje"]}</h2>
        <dl class="card facts">
          <div class="fact">
            <dt>{t["jmeno"]}</dt>
            <dd>{TITUL}&nbsp;{JMENO.replace(" ", "&nbsp;")}</dd>
          </div>
          <div class="fact">
            <dt>{t["ico"]}</dt>
            <dd class="num-row">
              <span class="num">{ICO}</span>
              {kopirovat(t, ICO, t["kop_ico"])}
              {odkaz_ven(ODKAZ_RZP, t["rzp"])}
            </dd>
          </div>
          <div class="fact">
            <dt>{t["dic"]}</dt>
            <dd>
              <span class="num-row"><span class="num">{DIC}</span>{kopirovat(t, DIC, t["kop_dic"])}</span>
              <span class="odkazy">{odkaz_ven(ODKAZ_ADIS, t["adis"])}{odkaz_ven(ODKAZ_VIES, t["vies"], hreflang="")}</span>
              <span class="note">{t["dic_pozn"]}</span>
            </dd>
          </div>
          <div class="fact">
            <dt>{t["dph"]}</dt>
            <dd>{t["dph_hodnota"].format(d=datum("2013-07-01", jazyk))} <span class="note">{t["dph_pozn"]}</span></dd>
          </div>
          <div class="fact">
            <dt>{t["forma"]}</dt>
            <dd>{t["forma_hodnota"]}</dd>
          </div>
          <div class="fact">
            <dt>{t["vznik"]}</dt>
            <dd>{datum("2012-04-13", jazyk)}</dd>
          </div>
          <div class="fact">
            <dt>{t["misto"]}</dt>
            <dd><address>{ULICE}, {CAST}<br>{PSC.replace(" ", "&nbsp;")} {MESTO}<br><span class="country">{t["stat"]}</span></address>
              <a class="ext map-link" href="{ODKAZ_MAPY.replace("&", "&amp;")}" target="_blank" rel="noopener">{t["mapy"].format(ext=ext)}</a>
            </dd>
          </div>
          <div class="fact">
            <dt>{t["predmet"]}</dt>
            <dd>{t["predmet_hodnota"]} <span class="note">{t["predmet_pozn"]}</span>
              <span class="obory-nadpis">{t["obory"]}</span>
              <ul class="obory">
{obory}
              </ul>
            </dd>
          </div>
          <div class="fact">
            <dt>{t["spravce"]}</dt>
            <dd>{t["spravce_hodnota"]} <span class="note">{t["spravce_pozn"]}</span></dd>
          </div>
        </dl>
      </div>
    </section>

    <section class="block" id="ucty" aria-labelledby="ucty-h">
      <div class="wrap">
        <h2 id="ucty-h">{t["h_ucty"]}</h2>
        <p class="intro">{t["ucty_uvod"]}</p>
        <div class="ucty">
{ucty}
        </div>
        <p class="zdroj">{t["zdroj"].format(d=datum(ZDROJ_DATUM, jazyk), adis=ODKAZ_ADIS.replace("&", "&amp;"), ext=ext)}</p>
      </div>
    </section>

    <section class="block soft" id="kontakt" aria-labelledby="kontakt-h">
      <div class="wrap">
        <h2 id="kontakt-h">{t["h_kontakt"]}</h2>
        <div class="card contact">
          <div class="person">
            <div class="avatar" aria-hidden="true">FH</div>
            <div>
              <p class="name">{TITUL}&nbsp;{JMENO.replace(" ", "&nbsp;")}</p>
              <p class="role">{t["role"]}</p>
            </div>
          </div>
          <ul class="channels">
            <li class="channel">
              <span class="icon" aria-hidden="true">{MAIL}</span>
              <div>
                <span class="label">{t["email"]}</span>
                <a class="value" href="mailto:{EMAIL}">{EMAIL.replace("@", "@<wbr>")}</a>
              </div>
            </li>
            <li class="channel">
              <span class="icon" aria-hidden="true">{TELEFON_IKONA}</span>
              <div>
                <span class="label">{t["telefon"]}</span>
                <a class="value" href="tel:{TELEFON.replace(" ", "")}">{TELEFON.replace(" ", "&nbsp;")}</a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <span>© {TITUL}&nbsp;{JMENO.replace(" ", "&nbsp;")} · {t["ico"].split(" (")[0]} {ICO} · {ULICE}, {PSC.replace(" ", "&nbsp;")} {MESTO}</span>
      <a href="{k}../" lang="cs" title="{t["rodina"]}">holasovi.net</a>
    </div>
  </footer>
</body>
</html>
'''


def main():
    for jazyk in ('cs', 'en', 'de'):
        cesta = os.path.join(KOREN, SLOZKA, '' if jazyk == 'cs' else jazyk, 'index.html')
        os.makedirs(os.path.dirname(cesta), exist_ok=True)
        with open(cesta, 'w', encoding='utf-8') as f:
            f.write(stranka(jazyk))
        print('zapsáno', os.path.relpath(cesta, KOREN))


if __name__ == '__main__':
    main()
