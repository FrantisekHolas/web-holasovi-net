#!/usr/bin/env python3
"""
Vygeneruje podnikatelské profily členů rodiny ve třech jazycích (čeština, angličtina, němčina):
  frantisek-profil-88722520/index.html, en/index.html, de/index.html
  vera-profil-06635971/index.html, en/index.html, de/index.html

Údaje jsou z veřejných rejstříků (ARES, živnostenský rejstřík, registr plátců DPH v ADIS,
seznam datových schránek) ke dni uvedenému u osoby (zdroj_datum). Po změně údajů nebo
textů upravte tento soubor a spusťte z kořene repozitáře:
  python3 nastroje/profily.py

Společný vzhled a skript jsou v assets/profil/ (profil.css, profil.js, písmo Inter),
ikony každého profilu v jeho složce ikony/ (lístek člena ze stromu s iniciálou).
"""
import json
import os

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = 'https://holasovi.net/'

# Společné odkazy na rejstříky
RZP = 'https://rzp.gov.cz/verejne-udaje/cs/udaje/vyber-subjektu;ico={ico}'
ADIS = 'https://adisspr.mfcr.cz/dpr/DphReg?id=1&pocet=1&fu=&OK=+Search+&ZPRAC=RDPHI1&dic={dic}'
VIES = 'https://ec.europa.eu/taxation_customs/vies/#/vat-validation'
DATOVKY = 'https://www.datovka.gov.cz/sds/detail?dbid={id}'
MAPY = 'https://www.google.com/maps/search/?api=1&query=Slez%C3%A1kova%20999%2F25%2C%20613%2000%20Brno'

# ---------- Čím se zabývá (místo předmětu podnikání z rejstříku) ----------
# Podle profilu na LinkedIn. Každá oblast: nadpis, popis (cs, en, de) a štítky s technologiemi
# (štítek je text, nebo trojice (cs, en, de), když se v jazycích liší).
CINNOST_FRANTISEK = {
    'nadpis': ('Čím se zabývám', 'What I do', 'Was ich mache'),
    'uvod': (
        'Komplexní řešení pro zákazníky v&nbsp;SAP – návrh architektury, vývoj, customizing, optimalizace, podpora a řešení nejrůznějších problémů.',
        'Complex customer solutions in SAP – architecture, development, customizing, optimization, support and the ability to solve all kinds of problems.',
        'Komplexe Kundenlösungen in SAP – Architektur, Entwicklung, Customizing, Optimierung, Support und die Lösung verschiedenster Probleme.',
    ),
    'oblasti': [
        {
            'nadpis': ('Vývoj v&nbsp;ABAP', 'ABAP development', 'ABAP-Entwicklung'),
            'popis': (
                'Procedurální i objektový přístup, modelování v&nbsp;HANA, enhancementy a modifikace, dynpra, reporty a vlastní komplexní řešení.',
                'Procedural and object-oriented programming, HANA modelling, enhancements and modifications, dynpros, reports and custom complex solutions.',
                'Prozedurale und objektorientierte Entwicklung, HANA-Modellierung, Erweiterungen und Modifikationen, Dynpros, Reports und eigene komplexe Lösungen.',
            ),
            'stitky': ['ABAP OO', 'HANA DB', 'S/4HANA', 'CDS', 'BOPF', 'BRF+', 'ALV', 'SALV', 'BDC'],
        },
        {
            'nadpis': ('Vývoj v&nbsp;SAP Fiori', 'SAP Fiori development', 'SAP-Fiori-Entwicklung'),
            'popis': (
                'Aplikace v&nbsp;SAPUI5 a Fiori Elements, hybridní aplikace, SAP Build a Fiori Launchpad.',
                'Apps in SAPUI5 and Fiori Elements, hybrid apps, SAP Build and the Fiori Launchpad.',
                'Anwendungen in SAPUI5 und Fiori Elements, hybride Apps, SAP Build und das Fiori Launchpad.',
            ),
            'stitky': ['SAPUI5', 'Fiori Elements', 'SAP Build', 'Fiori Launchpad'],
        },
        {
            'nadpis': ('Tiskové formuláře', 'Print forms', 'Druckformulare'),
            'popis': (
                'Specialista na tisk s&nbsp;hlubokou znalostí Adobe PDF Forms, včetně archivace a elektronického podepisování.',
                'Print specialist with deep knowledge of Adobe PDF Forms, including archiving and electronic signing.',
                'Druckspezialist mit fundierten Kenntnissen von Adobe PDF Forms, einschließlich Archivierung und elektronischer Signatur.',
            ),
            'stitky': ['Adobe PDF Forms', ('Archivace', 'Archiving', 'Archivierung'),
                       ('Elektronický podpis', 'Electronic signature', 'Elektronische Signatur')],
        },
        {
            'nadpis': ('Integrace', 'Integration', 'Integration'),
            'popis': (
                'Propojení SAP s&nbsp;dalšími systémy a podpora mnoha datových formátů.',
                'Connecting SAP with other systems and support for many data formats.',
                'Anbindung von SAP an andere Systeme und Unterstützung vieler Datenformate.',
            ),
            'stitky': ['RFC', 'SAP Proxy', 'IDoc', 'REST', 'SOAP', 'OData', 'XML', 'JSON', 'EDI', 'XLS', 'XLSX'],
        },
        {
            'nadpis': ('Integrační scénáře', 'Integration scenarios', 'Integrationsszenarien'),
            'popis': (
                'Bohaté zkušenosti s&nbsp;různými scénáři: Jungheinrich VNA/LRK/PRK, Kardex VNA, národní standard pro elektronický systém spisové služby ESSL/ISSD, EET&nbsp;2.0, veřejné rejstříky ADIS/ISIR/VIES a mnoho dalších.',
                'Strong experience with various integration scenarios: Jungheinrich VNA/LRK/PRK, Kardex VNA, the Czech national standard for electronic records management systems ESSL/ISSD, EET&nbsp;2.0 (Czech electronic sales records), Czech and EU public registers ADIS/ISIR/VIES and many others.',
                'Umfangreiche Erfahrung mit verschiedenen Integrationsszenarien: Jungheinrich VNA/LRK/PRK, Kardex VNA, tschechischer nationaler Standard für elektronische Aktenverwaltungssysteme ESSL/ISSD, EET&nbsp;2.0 (tschechische elektronische Umsatzerfassung), tschechische und EU-Register ADIS/ISIR/VIES und viele weitere.',
            ),
            # abecedně (ve všech třech jazycích stejné pořadí)
            'stitky': ['EET 2.0', 'ESSL/ISSD', 'Jungheinrich VNA/LRK/PRK', 'Kardex VNA',
                       ('Veřejné rejstříky ADIS/ISIR/VIES', 'Public registers ADIS/ISIR/VIES', 'Öffentliche Register ADIS/ISIR/VIES')],
        },
        {
            'nadpis': ('Komplexní aplikace', 'Complex applications', 'Komplexe Anwendungen'),
            'popis': (
                'Návrh a realizace komplexních aplikací: workflow, vlastní řešení ukládání dat se SAP Fiori a mnoho dalšího.',
                'Design and implementation of complex applications: workflows, custom storage solutions with SAP Fiori and many others.',
                'Konzeption und Umsetzung komplexer Anwendungen: Workflows, eigene Speicherlösungen mit SAP Fiori und vieles mehr.',
            ),
            'stitky': ['Workflow', 'SAP Fiori'],
        },
    ],
}

CINNOST_VERA = {
    'nadpis': ('Čím se zabývám', 'What I do', 'Was ich mache'),
    'uvod': (
        'Tisková řešení a formuláře v&nbsp;SAP a vývoj v&nbsp;ABAP.',
        'Print solutions and forms in SAP, and ABAP development.',
        'Drucklösungen und Formulare in SAP sowie ABAP-Entwicklung.',
    ),
    'oblasti': [
        {
            'nadpis': ('Tisková řešení', 'Print solutions', 'Drucklösungen'),
            'popis': (
                'Tisková řešení v&nbsp;SAP: formuláře a tiskové výstupy.',
                'Print solutions in SAP: forms and print output.',
                'Drucklösungen in SAP: Formulare und Druckausgaben.',
            ),
            'stitky': [],
        },
        {
            'nadpis': ('Překlady a rebranding formulářů', 'Form translation and rebranding', 'Übersetzung und Rebranding von Formularen'),
            'popis': (
                'Podpora překladů formulářů do dalších jazyků a jejich rebrandingu, například po změně firemní identity.',
                'Support for translating forms into other languages and for rebranding them, for example after a change of corporate identity.',
                'Unterstützung bei der Übersetzung von Formularen in weitere Sprachen und bei ihrem Rebranding, zum Beispiel nach einer Änderung des Corporate Designs.',
            ),
            'stitky': [],
        },
        {
            'nadpis': ('Vývoj v&nbsp;SAP ABAP', 'SAP ABAP development', 'SAP-ABAP-Entwicklung'),
            'popis': (
                'Vývoj jednoduchých i&nbsp;složitějších řešení na míru.',
                'Development of simple as well as more complex custom solutions.',
                'Entwicklung einfacher wie auch komplexerer individueller Lösungen.',
            ),
            'stitky': [],
        },
    ],
}

# ---------- Osoby (údaje z rejstříků) ----------
OSOBY = [
    {
        'slozka': 'frantisek-profil-88722520',
        'titul': 'Mgr.', 'jmeno': 'František', 'prijmeni': 'Holas', 'zkratka': 'FH', 'zena': False,
        'ico': '88722520', 'dic': 'CZ8306023825',
        'od': '2012-04-13', 'dph_od': '2013-07-01',
        'ulice': 'Slezákova 999/25', 'cast': 'Husovice', 'psc': '613 00', 'mesto': 'Brno', 'mapy': MAPY,
        'email': 'frantisek@holasovi.net', 'telefon': '+420 776 280 026', 'datovka': 'ymkb6j4',
        # obory z rejstříku se na stránce nezobrazují, místo nich je sekce „Čím se zabývám“ (cinnost)
        'obory': ['vyzkum', 'zprostredkovani', 'jinde', 'obchod', 'poradenstvi', 'software'],
        'cinnost': CINNOST_FRANTISEK,
        'ucty': [
            # číslo účtu, IBAN, banka, BIC, zveřejněno v registru plátců DPH, měna (None = neuvádět)
            ('1037342017/3030', 'CZ72 3030 0000 0010 3734 2017', 'Air Bank a.s.', 'AIRACZPP', '2013-06-20', 'CZK'),
            ('1037342033/3030', 'CZ28 3030 0000 0010 3734 2033', 'Air Bank a.s.', 'AIRACZPP', '2021-12-10', 'EUR'),
        ],
        'zdroj_datum': '2026-11-14',
    },
    {
        'slozka': 'vera-profil-06635971',
        'titul': '', 'jmeno': 'Věra', 'prijmeni': 'Holasová', 'zkratka': 'VH', 'zena': True,
        'ico': '06635971', 'dic': 'CZ8362093960',
        'od': '2017-11-27', 'dph_od': '2019-09-01',
        'ulice': 'Slezákova 999/25', 'cast': 'Husovice', 'psc': '613 00', 'mesto': 'Brno', 'mapy': MAPY,
        'email': 'info@vera.holasovi.net', 'telefon': None, 'datovka': 'hfgwcpe',
        # obory z rejstříku se na stránce nezobrazují, místo nich je sekce „Čím se zabývám“ (cinnost)
        'obory': ['zprostredkovani', 'poradenstvi', 'reklama', 'obchod', 'jinde', 'software', 'vyzkum'],
        'cinnost': CINNOST_VERA,
        'ucty': [
            ('2701334897/2010', 'CZ73 2010 0000 0027 0133 4897', 'Fio banka, a.s.', 'FIOBCZPP', '2019-11-14', None),
        ],
        'zdroj_datum': '2026-11-14',
    },
]

# Obory činnosti volné živnosti (příloha č. 4 živnostenského zákona) v jazycích profilu
OBORY = {
    'vyzkum': ('Výzkum a vývoj v&nbsp;oblasti přírodních a technických věd nebo společenských věd',
               'Research and development in the natural and technical sciences or the social sciences',
               'Forschung und Entwicklung in den Natur- und Technikwissenschaften oder den Sozialwissenschaften'),
    'zprostredkovani': ('Zprostředkování obchodu a služeb',
                        'Intermediation of trade and services',
                        'Vermittlung von Handel und Dienstleistungen'),
    'jinde': ('Výroba, obchod a služby jinde nezařazené',
              'Production, trade and services not elsewhere classified',
              'Herstellung, Handel und Dienstleistungen, anderweitig nicht genannt'),
    'obchod': ('Velkoobchod a maloobchod',
               'Wholesale and retail trade',
               'Groß- und Einzelhandel'),
    'poradenstvi': ('Poradenská a konzultační činnost, zpracování odborných studií a posudků',
                    'Advisory and consulting services, preparation of expert studies and reports',
                    'Beratungs- und Konsultationstätigkeit, Erstellung von Fachstudien und Gutachten'),
    'software': ('Poskytování software, poradenství v&nbsp;oblasti informačních technologií, zpracování dat, hostingové a související činnosti a webové portály',
                 'Provision of software, IT consulting, data processing, hosting and related activities and web portals',
                 'Bereitstellung von Software, IT-Beratung, Datenverarbeitung, Hosting und damit verbundene Tätigkeiten sowie Webportale'),
    'reklama': ('Reklamní činnost, marketing, mediální zastoupení',
                'Advertising, marketing and media representation',
                'Werbung, Marketing, Medienvertretung'),
}
PORADI_JAZYKU = {'cs': 0, 'en': 1, 'de': 2}

MESICE = {
    'cs': ['ledna', 'února', 'března', 'dubna', 'května', 'června', 'července', 'srpna', 'září', 'října', 'listopadu', 'prosince'],
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'de': ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
}

# ---------- Texty ----------
# Dvojice (muž, žena) tam, kde se text liší podle rodu.
T = {
    'cs': {
        'locale': 'cs_CZ', 'nazev': '{cele} | {role}, Brno',
        'popis': '{cele}, {role}, IČO {ico}, DIČ {dic}, {ulice}, {psc} Brno. Údaje o podnikateli, bankovní účty a kontakt.',
        'og_popis': 'Údaje o podnikateli, bankovní účty a kontakt. IČO {ico}, Brno.',
        'role': ('podnikatel', 'podnikatelka'),
        'preskocit': 'Přejít na obsah', 'nav': 'Hlavní navigace', 'nav_udaje': 'Údaje', 'nav_ucty': 'Bankovní účty', 'nav_kontakt': 'Kontakt',
        'jazyk': 'Jazyk', 'na_tmavy': 'Přepnout na tmavý režim', 'na_svetly': 'Přepnout na světlý režim', 'rezim': 'Tmavý režim',
        'zacatek': 'na začátek stránky',
        'eyebrow': 'Brno, Česká republika · od roku {rok}',
        'lead': 'Podnikající fyzická osoba zapsaná v&nbsp;živnostenském rejstříku, plátce DPH.',
        'btn_vypis': 'Výpis ze živnostenského rejstříku',
        'h_udaje': ('Údaje o&nbsp;podnikateli', 'Údaje o&nbsp;podnikatelce'),
        'jmeno': 'Obchodní jméno', 'ico': 'IČO', 'ico_kratce': 'IČO', 'rzp': 'Živnostenský rejstřík', 'dic': 'DIČ',
        'adis': 'Registr plátců DPH (ADIS)', 'vies': 'Ověření ve VIES (EU)',
        'dic_pozn': 'V&nbsp;ADIS i&nbsp;VIES zadejte číslo {cislo} (ve VIES členský stát CZ).',
        'dph': 'Plátce DPH', 'dph_hodnota': 'ano, od {d}', 'dph_pozn': ('spolehlivý plátce (není veden jako nespolehlivý)', 'spolehlivý plátce (není vedena jako nespolehlivý plátce)'),
        'forma': 'Právní forma', 'forma_hodnota': 'Fyzická osoba podnikající dle živnostenského zákona',
        'vznik': 'Podnikání od', 'misto': 'Místo podnikání', 'stat': 'Česká republika', 'mapy': 'Zobrazit v&nbsp;Mapách <span class="nowrap">Google{ext}</span>',
        'predmet': 'Předmět podnikání',
        'predmet_hodnota': 'Výroba, obchod a služby neuvedené v&nbsp;přílohách 1 až 3 živnostenského zákona',
        'predmet_pozn': 'živnost volná', 'obory': 'Obory činnosti:',
        'spravce': 'Správce daně', 'spravce_hodnota': 'Finanční úřad pro Jihomoravský kraj', 'spravce_pozn': 'Územní pracoviště Brno III',
        'h_ucty': ('Bankovní účty', 'Bankovní účet'),
        'ucty_uvod': ('Účty zveřejněné správcem daně v&nbsp;registru plátců DPH.', 'Účet zveřejněný správcem daně v&nbsp;registru plátců DPH.'),
        'ucet': 'Účet', 'ucet_mena': 'Účet v&nbsp;{m}', 'cislo': 'Číslo účtu', 'banka': 'Banka', 'zverejneno': 'Zveřejněno',
        'zdroj': 'Aktuální stav ověříte v&nbsp;<a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">registru <span class="nowrap">ADIS{ext}</span></a>.',
        'kopirovat': 'Kopírovat', 'zkopirovano': 'Zkopírováno', 'kop_ico': 'Kopírovat IČO', 'kop_dic': 'Kopírovat DIČ',
        'kop_cislo': 'Kopírovat číslo účtu', 'kop_iban': 'Kopírovat IBAN',
        'h_kontakt': 'Kontakt', 'email': 'E-mail', 'telefon': 'Telefon',
        'datovka': 'Datová schránka', 'datovka_over': 'Ověřit v registru datových schránek', 'kop_datovka': 'Kopírovat ID datové schránky',
        'rodina': 'Rodinný strom Holasových',
    },
    'en': {
        'locale': 'en_US', 'nazev': '{cele} | {role}, Brno',
        'popis': '{cele}, sole trader, Business ID (IČO) {ico}, VAT ID {dic}, {ulice}, {psc} Brno, Czech Republic. Business details, bank accounts and contact.',
        'og_popis': 'Business details, bank accounts and contact. Business ID {ico}, Brno.',
        'role': ('Sole trader', 'Sole trader'),
        'preskocit': 'Skip to content', 'nav': 'Main navigation', 'nav_udaje': 'Details', 'nav_ucty': 'Bank accounts', 'nav_kontakt': 'Contact',
        'jazyk': 'Language', 'na_tmavy': 'Switch to dark mode', 'na_svetly': 'Switch to light mode', 'rezim': 'Dark mode',
        'zacatek': 'back to top',
        'eyebrow': 'Brno, Czech Republic · since {rok}',
        'lead': 'Self-employed person (sole trader) registered in the Czech Trade Register, VAT payer.',
        'btn_vypis': 'Trade Register extract',
        'h_udaje': 'Business details',
        'jmeno': 'Business name', 'ico': 'Business ID (IČO)', 'ico_kratce': 'Business ID', 'rzp': 'Trade Register (in Czech)', 'dic': 'VAT ID (DIČ)',
        'adis': 'Czech VAT register (ADIS, in Czech)', 'vies': 'Check in VIES (EU)',
        'dic_pozn': 'In ADIS and VIES, enter the number {cislo} (in VIES with Member State CZ).',
        'dph': 'VAT status', 'dph_hodnota': 'VAT payer since {d}', 'dph_pozn': ('reliable VAT payer (not listed as unreliable)', 'reliable VAT payer (not listed as unreliable)'),
        'forma': 'Legal form', 'forma_hodnota': 'Natural person doing business under the Czech Trade Licensing Act',
        'vznik': 'In business since', 'misto': 'Place of business', 'stat': 'Czech Republic', 'mapy': 'View on Google <span class="nowrap">Maps{ext}</span>',
        'predmet': 'Scope of business',
        'predmet_hodnota': 'Production, trade and services not listed in Annexes 1 to 3 of the Trade Licensing Act',
        'predmet_pozn': 'unregulated trade (živnost volná)', 'obory': 'Fields of activity:',
        'spravce': 'Tax office', 'spravce_hodnota': 'Tax Office for the South Moravian Region', 'spravce_pozn': 'Regional office Brno III (Finanční úřad pro Jihomoravský kraj, Územní pracoviště Brno III)',
        'h_ucty': ('Bank accounts', 'Bank account'),
        'ucty_uvod': ('Accounts published by the tax authority in the Czech VAT payer register.', 'Account published by the tax authority in the Czech VAT payer register.'),
        'ucet': 'Account', 'ucet_mena': '{m} account', 'cislo': 'Account number', 'banka': 'Bank', 'zverejneno': 'Published',
        'zdroj': 'Check the current status in the <a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">ADIS <span class="nowrap">register{ext}</span></a>.',
        'kopirovat': 'Copy', 'zkopirovano': 'Copied', 'kop_ico': 'Copy Business ID', 'kop_dic': 'Copy VAT ID',
        'kop_cislo': 'Copy account number', 'kop_iban': 'Copy IBAN',
        'h_kontakt': 'Contact', 'email': 'Email', 'telefon': 'Phone',
        'datovka': 'Data box (ISDS)', 'datovka_over': 'Verify in the Czech data box registry', 'kop_datovka': 'Copy data box ID',
        'rodina': 'Holas family tree',
    },
    'de': {
        'locale': 'de_DE', 'nazev': '{cele} | {role}, Brno',
        'popis': '{cele}, {role}, Ident.-Nr. (IČO) {ico}, USt-IdNr. {dic}, {ulice}, {psc} Brno, Tschechische Republik. Unternehmensangaben, Bankkonten und Kontakt.',
        'og_popis': 'Unternehmensangaben, Bankkonten und Kontakt. Ident.-Nr. {ico}, Brno.',
        'role': ('Einzelunternehmer', 'Einzelunternehmerin'),
        'preskocit': 'Zum Inhalt springen', 'nav': 'Hauptnavigation', 'nav_udaje': 'Angaben', 'nav_ucty': 'Bankkonten', 'nav_kontakt': 'Kontakt',
        'jazyk': 'Sprache', 'na_tmavy': 'Dunkles Design einschalten', 'na_svetly': 'Helles Design einschalten', 'rezim': 'Dunkles Design',
        'zacatek': 'zum Seitenanfang',
        'eyebrow': 'Brno, Tschechische Republik · seit {rok}',
        'lead': ('Selbständig tätige natürliche Person (Einzelunternehmer), eingetragen im tschechischen Gewerberegister, umsatzsteuerpflichtig.',
                 'Selbständig tätige natürliche Person (Einzelunternehmerin), eingetragen im tschechischen Gewerberegister, umsatzsteuerpflichtig.'),
        'btn_vypis': 'Gewerberegisterauszug',
        'h_udaje': 'Unternehmensangaben',
        'jmeno': 'Geschäftsname', 'ico': 'Ident.-Nr. (IČO)', 'ico_kratce': 'Ident.-Nr.', 'rzp': 'Gewerberegister (auf Tschechisch)', 'dic': 'USt-IdNr. (DIČ)',
        'adis': 'Tschechisches USt-Register (ADIS, auf Tschechisch)', 'vies': 'Prüfung in VIES (EU)',
        'dic_pozn': 'In ADIS und VIES die Nummer {cislo} eingeben (in VIES mit Mitgliedstaat CZ).',
        'dph': 'Umsatzsteuer', 'dph_hodnota': 'umsatzsteuerpflichtig seit {d}', 'dph_pozn': ('zuverlässiger Steuerzahler (nicht als unzuverlässig geführt)', 'zuverlässige Steuerzahlerin (nicht als unzuverlässig geführt)'),
        'forma': 'Rechtsform', 'forma_hodnota': 'Natürliche Person, gewerbetätig nach dem tschechischen Gewerbegesetz',
        'vznik': 'Geschäftstätig seit', 'misto': 'Ort der Geschäftstätigkeit', 'stat': 'Tschechische Republik', 'mapy': 'In Google Maps <span class="nowrap">anzeigen{ext}</span>',
        'predmet': 'Gegenstand der Tätigkeit',
        'predmet_hodnota': 'Herstellung, Handel und Dienstleistungen, die nicht in den Anlagen 1 bis 3 des Gewerbegesetzes aufgeführt sind',
        'predmet_pozn': 'freies Gewerbe (živnost volná)', 'obory': 'Tätigkeitsbereiche:',
        'spravce': 'Zuständiges Finanzamt', 'spravce_hodnota': 'Finanzamt für die Region Südmähren', 'spravce_pozn': 'Dienststelle Brno III (Finanční úřad pro Jihomoravský kraj, Územní pracoviště Brno III)',
        'h_ucty': ('Bankkonten', 'Bankkonto'),
        'ucty_uvod': ('Vom Finanzamt im tschechischen Register der Umsatzsteuerpflichtigen veröffentlichte Konten.', 'Vom Finanzamt im tschechischen Register der Umsatzsteuerpflichtigen veröffentlichtes Konto.'),
        'ucet': 'Konto', 'ucet_mena': '{m}-Konto', 'cislo': 'Kontonummer', 'banka': 'Bank', 'zverejneno': 'Veröffentlicht',
        'zdroj': 'Den aktuellen Stand prüfen Sie im <a class="ext" href="{adis}" target="_blank" rel="noopener" hreflang="cs">ADIS-<span class="nowrap">Register{ext}</span></a>.',
        'kopirovat': 'Kopieren', 'zkopirovano': 'Kopiert', 'kop_ico': 'Ident.-Nr. kopieren', 'kop_dic': 'USt-IdNr. kopieren',
        'kop_cislo': 'Kontonummer kopieren', 'kop_iban': 'IBAN kopieren',
        'h_kontakt': 'Kontakt', 'email': 'E-Mail', 'telefon': 'Telefon',
        'datovka': 'Datenbox (ISDS)', 'datovka_over': 'Im tschechischen Datenbox-Verzeichnis prüfen', 'kop_datovka': 'Datenbox-ID kopieren',
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
SCHRANKA = svg('<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>')
KOPIE = svg('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>')
MESIC = svg('<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>', 'ikona-mesic')
SLUNCE = svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>', 'ikona-slunce')


def datum(iso, jazyk):
    r, m, d = (int(x) for x in iso.split('-'))
    mesic = MESICE[jazyk][m - 1]
    if jazyk == 'en':
        return f'<time datetime="{iso}">{mesic}&nbsp;{d}, {r}</time>'
    return f'<time datetime="{iso}">{d}.&nbsp;{mesic} {r}</time>'


def nbsp(text):
    return text.replace(' ', '&nbsp;')


def stitek(st, ji):
    """Štítek technologie: společný text, nebo trojice (cs, en, de)."""
    return st[ji] if isinstance(st, tuple) else st


def rod(hodnota, osoba):
    """Text podle rodu: dvojice (muž, žena) nebo jeden společný text."""
    if isinstance(hodnota, tuple):
        return hodnota[1] if osoba['zena'] else hodnota[0]
    return hodnota


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


def stranka(o, jazyk):
    t = {k: rod(v, o) for k, v in T[jazyk].items()}
    adresa = WEB + o['slozka'] + '/'
    k = '' if jazyk == 'cs' else '../'          # cesta ke kořeni profilu
    s = k + '../'                               # cesta ke kořeni webu
    url = adresa + ('' if jazyk == 'cs' else jazyk + '/')
    jmeno = f'{o["jmeno"]} {o["prijmeni"]}'
    cele = f'{o["titul"]} {jmeno}'.strip()
    titul_html = f'<span class="titul">{o["titul"]}</span> ' if o['titul'] else ''
    dic_cislo = o['dic'][2:]
    odkaz_rzp = RZP.format(ico=o['ico'])
    odkaz_adis = ADIS.format(dic=dic_cislo)
    odkaz_datovky = DATOVKY.format(id=o['datovka'])
    pocet_uctu = len(o['ucty'])
    h_ucty = T[jazyk]['h_ucty'][0 if pocet_uctu > 1 else 1]
    ucty_uvod = T[jazyk]['ucty_uvod'][0 if pocet_uctu > 1 else 1]
    vars_ = dict(cele=cele, role=t['role'], ico=o['ico'], dic=o['dic'], ulice=o['ulice'], psc=o['psc'],
                 rok=o['od'][:4], cislo=dic_cislo)

    jazyky = [('cs', 'CS', 'Čeština'), ('en', 'EN', 'English'), ('de', 'DE', 'Deutsch')]
    prepinac = '\n'.join(
        f'          <a href="{"./" if j == jazyk else (k if j == "cs" else k + j + "/")}" hreflang="{j}" lang="{j}" '
        f'data-set-lang="{j}" aria-label="{nazev}" title="{nazev}"{AKTUALNI if j == jazyk else ""}>{zkr}</a>'
        for j, zkr, nazev in jazyky)
    alternativy = '\n'.join(f'  <link rel="alternate" hreflang="{j}" href="{adresa}{"" if j == "cs" else j + "/"}">' for j, _, _ in jazyky)
    obory = '\n'.join(f'                <li>{OBORY[ob][PORADI_JAZYKU[jazyk]]}</li>' for ob in o['obory'])
    ji = PORADI_JAZYKU[jazyk]
    cinnost = o.get('cinnost')
    # střídání pozadí oddílů: Čím se zabývám (je-li), Údaje, Bankovní účty, Kontakt
    tridy = (['block soft', 'block', 'block soft', 'block'] if cinnost else ['block soft', 'block', 'block soft'])
    if cinnost:
        oblasti = '\n'.join(
            f'''          <div class="card oblast">
            <h3>{ob["nadpis"][ji]}</h3>
            <p>{ob["popis"][ji]}</p>
            {('<ul class="stitky">' + "".join(f"<li>{stitek(st, ji)}</li>" for st in ob["stitky"]) + '</ul>') if ob["stitky"] else ''}
          </div>''' for ob in cinnost['oblasti'])
        cinnost_html = f'''
    <section class="{tridy.pop(0)}" id="cinnost" aria-labelledby="cinnost-h">
      <div class="wrap">
        <h2 id="cinnost-h">{cinnost["nadpis"][ji]}</h2>
        <p class="intro">{cinnost["uvod"][ji]}</p>
        <div class="oblasti">
{oblasti}
        </div>
      </div>
    </section>
'''
        nav_cinnost = f'<a href="#cinnost">{cinnost["nadpis"][ji]}</a>\n          '
        predmet_html = ''
    else:
        cinnost_html = nav_cinnost = ''
        predmet_html = f'''
          <div class="fact">
            <dt>{t["predmet"]}</dt>
            <dd>{t["predmet_hodnota"]} <span class="note">{t["predmet_pozn"]}</span>
              <span class="obory-nadpis">{t["obory"]}</span>
              <ul class="obory">
{obory}
              </ul>
            </dd>
          </div>'''

    ucty = []
    for i, (cislo, iban, banka, bic, zverejneno, mena) in enumerate(o['ucty'], 1):
        nadpis = t['ucet_mena'].format(m=mena) if mena else (f'{t["ucet"]} {i}' if pocet_uctu > 1 else t['ucet'])
        ucty.append(f'''          <div class="card ucet">
            <h3>{nadpis}</h3>
            <dl>
              <dt>{t["cislo"]}</dt>
              <dd><span class="num">{cislo}</span>{kopirovat(t, cislo, t["kop_cislo"])}</dd>
              <dt>IBAN</dt>
              <dd><span class="num">{nbsp(iban)}</span>{kopirovat(t, iban.replace(" ", ""), t["kop_iban"])}</dd>
              <dt>BIC (SWIFT)</dt>
              <dd>{bic}</dd>
              <dt>{t["banka"]}</dt>
              <dd class="slabe">{banka}</dd>
              <dt>{t["zverejneno"]}</dt>
              <dd class="slabe">{datum(zverejneno, jazyk)}</dd>
            </dl>
          </div>''')
    ucty = '\n'.join(ucty)

    telefon = ''
    if o['telefon']:
        telefon = f'''
            <li class="channel">
              <span class="icon" aria-hidden="true">{TELEFON_IKONA}</span>
              <div>
                <span class="label">{t["telefon"]}</span>
                <a class="value" href="tel:{o["telefon"].replace(" ", "")}">{nbsp(o["telefon"])}</a>
              </div>
            </li>'''

    ld = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': cele,
        'givenName': o['jmeno'],
        'familyName': o['prijmeni'],
        'url': url,
        'email': o['email'],
        'vatID': o['dic'],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'IČO', 'value': o['ico']},
        'address': {'@type': 'PostalAddress', 'streetAddress': o['ulice'], 'addressLocality': o['mesto'],
                    'postalCode': o['psc'], 'addressCountry': 'CZ'},
    }
    if o['titul']:
        ld['honorificPrefix'] = o['titul']
    if cinnost and any(ob['stitky'] for ob in cinnost['oblasti']):
        ld['knowsAbout'] = sorted({stitek(st, ji) for ob in cinnost['oblasti'] for st in ob['stitky']})
    if o['telefon']:
        ld['telephone'] = o['telefon'].replace(' ', '')
    ld = json.dumps(ld, ensure_ascii=False, indent=2).replace('\n', '\n  ')
    ext = EXT

    return f'''<!doctype html>
<html lang="{jazyk}"{" data-lang-auto" if jazyk == "cs" else ""}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- Vygenerováno nástrojem nastroje/profily.py – ručně neupravovat. -->
  <script src="{s}assets/profil/profil.js"></script>
  <title>{t["nazev"].format(**vars_)}</title>
  <meta name="description" content="{t["popis"].format(**vars_)}">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0f0f0f" media="(prefers-color-scheme: dark)">

{alternativy}
  <link rel="alternate" hreflang="x-default" href="{adresa}">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="profile">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{t["locale"]}">
  <meta property="og:title" content="{cele}">
  <meta property="og:description" content="{t["og_popis"].format(**vars_)}">

  <link rel="icon" type="image/png" sizes="32x32" href="{k}ikony/favicon-32.png">
  <link rel="icon" type="image/png" sizes="64x64" href="{k}ikony/favicon-64.png">
  <link rel="apple-touch-icon" href="{k}ikony/apple-touch-icon.png">
  <link rel="preload" href="{s}assets/profil/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="{s}assets/profil/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{s}assets/profil/profil.css">

  <script type="application/ld+json">
  {ld}
  </script>
</head>
<body>
  <a class="skip" href="#main">{t["preskocit"]}</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="#" aria-label="{cele}, {t["zacatek"]}">{jmeno}</a>
      <div class="header-end">
        <nav class="nav" aria-label="{t["nav"]}">
          {nav_cinnost}<a href="#udaje">{t["nav_udaje"]}</a>
          <a href="#ucty">{t["nav_ucty"] if pocet_uctu > 1 else h_ucty}</a>
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
        <p class="eyebrow">{t["eyebrow"].format(**vars_)}</p>
        <h1>{titul_html}{nbsp(jmeno)}</h1>
        <p class="lead">{t["lead"]}</p>
        <div class="actions">
          <a class="btn primary" href="#kontakt">
            {MAIL}
            {t["nav_kontakt"]}
          </a>
          <a class="btn" href="{odkaz_rzp}" target="_blank" rel="noopener" hreflang="cs">
            {t["btn_vypis"]}
            {EXT}
          </a>
        </div>
      </div>
    </section>
{cinnost_html}
    <section class="{tridy[0]}" id="udaje" aria-labelledby="udaje-h">
      <div class="wrap">
        <h2 id="udaje-h">{t["h_udaje"]}</h2>
        <dl class="card facts">
          <div class="fact">
            <dt>{t["jmeno"]}</dt>
            <dd>{nbsp(cele)}</dd>
          </div>
          <div class="fact">
            <dt>{t["ico"]}</dt>
            <dd class="num-row">
              <span class="num">{o["ico"]}</span>
              {kopirovat(t, o["ico"], t["kop_ico"])}
              {odkaz_ven(odkaz_rzp, t["rzp"])}
            </dd>
          </div>
          <div class="fact">
            <dt>{t["dic"]}</dt>
            <dd>
              <span class="num-row"><span class="num">{o["dic"]}</span>{kopirovat(t, o["dic"], t["kop_dic"])}</span>
              <span class="odkazy">{odkaz_ven(odkaz_adis, t["adis"])}{odkaz_ven(VIES, t["vies"], hreflang="")}</span>
              <span class="note">{t["dic_pozn"].format(**vars_)}</span>
            </dd>
          </div>
          <div class="fact">
            <dt>{t["dph"]}</dt>
            <dd>{t["dph_hodnota"].format(d=datum(o["dph_od"], jazyk))} <span class="note">{t["dph_pozn"]}</span></dd>
          </div>
          <div class="fact">
            <dt>{t["forma"]}</dt>
            <dd>{t["forma_hodnota"]}</dd>
          </div>
          <div class="fact">
            <dt>{t["vznik"]}</dt>
            <dd>{datum(o["od"], jazyk)}</dd>
          </div>
          <div class="fact">
            <dt>{t["misto"]}</dt>
            <dd><address>{o["ulice"]}, {o["cast"]}<br>{nbsp(o["psc"])} {o["mesto"]}<br><span class="country">{t["stat"]}</span></address>
              <a class="ext map-link" href="{o["mapy"].replace("&", "&amp;")}" target="_blank" rel="noopener">{t["mapy"].format(ext=ext)}</a>
            </dd>
          </div>{predmet_html}
          <div class="fact">
            <dt>{t["spravce"]}</dt>
            <dd>{t["spravce_hodnota"]} <span class="note">{t["spravce_pozn"]}</span></dd>
          </div>
        </dl>
      </div>
    </section>

    <section class="{tridy[1]}" id="ucty" aria-labelledby="ucty-h">
      <div class="wrap">
        <h2 id="ucty-h">{h_ucty}</h2>
        <p class="intro">{ucty_uvod}</p>
        <div class="ucty">
{ucty}
        </div>
        <p class="zdroj">{t["zdroj"].format(d=datum(o["zdroj_datum"], jazyk), adis=odkaz_adis.replace("&", "&amp;"), ext=ext)}</p>
      </div>
    </section>

    <section class="{tridy[2]}" id="kontakt" aria-labelledby="kontakt-h">
      <div class="wrap">
        <h2 id="kontakt-h">{t["h_kontakt"]}</h2>
        <div class="card contact">
          <div class="person">
            <div class="avatar" aria-hidden="true">{o["zkratka"]}</div>
            <div>
              <p class="name">{nbsp(cele)}</p>
              <p class="role">{t["role"]}</p>
            </div>
          </div>
          <ul class="channels">
            <li class="channel">
              <span class="icon" aria-hidden="true">{MAIL}</span>
              <div>
                <span class="label">{t["email"]}</span>
                <a class="value" href="mailto:{o["email"]}">{o["email"].replace("@", "@<wbr>")}</a>
              </div>
            </li>{telefon}
            <li class="channel">
              <span class="icon" aria-hidden="true">{SCHRANKA}</span>
              <div>
                <span class="label">{t["datovka"]}</span>
                <span class="num-row"><span class="value id">{o["datovka"]}</span>{kopirovat(t, o["datovka"], t["kop_datovka"])}</span>
                {odkaz_ven(odkaz_datovky, t["datovka_over"], trida="hint ext")}
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <span>© {nbsp(cele)} · {t["ico_kratce"]} {o["ico"]} · {o["ulice"]}, {nbsp(o["psc"])} {o["mesto"]}</span>
      <a href="{s}" lang="cs" title="{t["rodina"]}">holasovi.net</a>
    </div>
  </footer>
</body>
</html>
'''


def main():
    for osoba in OSOBY:
        for jazyk in ('cs', 'en', 'de'):
            cesta = os.path.join(KOREN, osoba['slozka'], '' if jazyk == 'cs' else jazyk, 'index.html')
            os.makedirs(os.path.dirname(cesta), exist_ok=True)
            with open(cesta, 'w', encoding='utf-8') as f:
                f.write(stranka(osoba, jazyk))
            print('zapsáno', os.path.relpath(cesta, KOREN))


if __name__ == '__main__':
    main()
