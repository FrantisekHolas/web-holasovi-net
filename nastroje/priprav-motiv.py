#!/usr/bin/env python3
"""
Připraví malby nového motivu stromu pro web (viz assets/js/motivy.js).

Malby z Gemini se porovnají s podzimní předlohou: u každého z pěti lístků se změří
posun proti poloze v assets/js/clenove.js, malba se o průměrný posun srovná
a uloží ve všech velikostech do assets/img/motivy/<motiv>/.

Použití (z kořene repozitáře):
  python3 nastroje/priprav-motiv.py jaro --ctverec ctverec.jpg --vyska vyska.jpg --panorama panorama.jpg
  python3 nastroje/priprav-motiv.py jaro --ctverec ctverec.jpg --jen-kontrola

Potřebuje Python 3 s balíčky pillow, numpy a opencv-python.
Poté v assets/js/motivy.js doplnit u motivu dodané verze do pole "obrazky".
"""
import argparse
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTIVY = os.path.join(KOREN, 'assets', 'img', 'motivy')
PREDLOHA = 'podzim'
FORMATY = {
    # rozměr, menší verze, velikost lístku jako podíl šířky malby
    'ctverec': ((1500, 1500), 900, 0.12),
    'vyska': ((1116, 2000), 720, 0.16),
    'panorama': ((2000, 557), 1200, 0.04),
}
KVALITA = 85
MEZ_POSUNU = 0.04   # největší dovolený zbytkový posun lístku (podíl velikosti lístku)
MEZ_SHODY = 0.35    # nejmenší podobnost lístku s předlohou


def polohy_listku():
    """Načte polohy lístků z assets/js/clenove.js: {jmeno: {format: (x %, y %)}}."""
    text = open(os.path.join(KOREN, 'assets', 'js', 'clenove.js'), encoding='utf-8').read()
    vysledek = {}
    for m in re.finditer(r"jmeno:\s*'([^']+)'.*?poloha:\s*\{([^}]*)\}", text, re.S):
        vysledek[m.group(1)] = {f: (float(x), float(y)) for f, x, y in
                               re.findall(r"(\w+):\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*\]", m.group(2))}
    if len(vysledek) != 5:
        sys.exit('V clenove.js se nenašlo pět lístků s polohami.')
    return vysledek


def nacti(cesta, rozmer):
    im = Image.open(cesta).convert('RGB')
    if im.size != rozmer:
        # zachovat poměr stran: zmenšit na výšku/šířku cíle a oříznout přesah na střed
        meritko = max(rozmer[0] / im.width, rozmer[1] / im.height)
        im = im.resize((round(im.width * meritko), round(im.height * meritko)), Image.LANCZOS)
        x = (im.width - rozmer[0]) // 2
        y = (im.height - rozmer[1]) // 2
        im = im.crop((x, y, x + rozmer[0], y + rozmer[1]))
        print(f'  rozměr upraven na {rozmer[0]} × {rozmer[1]} (oříznutí na střed)')
    return im


def zmer_posuny(predloha, malba, format, polohy):
    """Posun každého lístku (dx, dy v px, podobnost) mezi předlohou a malbou."""
    a = np.asarray(predloha, dtype=np.float32)
    b = np.asarray(malba, dtype=np.float32)
    vyska, sirka = a.shape[:2]
    listek = FORMATY[format][2] * sirka
    vzor = int(listek * 0.8) // 2 * 2
    okraj = int(listek * 0.5)
    vysledek = {}
    for jmeno, poloha in polohy.items():
        cx = int(poloha[format][0] / 100 * sirka)
        cy = int(poloha[format][1] / 100 * vyska)
        x0, y0 = cx - vzor // 2, cy - vzor // 2
        t = a[y0:y0 + vzor, x0:x0 + vzor]
        ox, oy = max(0, x0 - okraj), max(0, y0 - okraj)
        okno = b[oy:y0 + vzor + okraj, ox:x0 + vzor + okraj]
        r = cv2.matchTemplate(okno, t, cv2.TM_CCOEFF_NORMED)
        _, nejlepsi, _, (mx, my) = cv2.minMaxLoc(r)

        def zpresni(v, p):  # parabola kolem maxima pro přesnost pod pixel
            if 0 < p < len(v) - 1:
                d = v[p - 1] - 2 * v[p] + v[p + 1]
                return p + (0.5 * (v[p - 1] - v[p + 1]) / d if d else 0)
            return p
        px = zpresni(r[my, :], mx)
        py = zpresni(r[:, mx], my)
        vysledek[jmeno] = (px - (x0 - ox), py - (y0 - oy), nejlepsi)
    return vysledek, FORMATY[format][2] * sirka


def kontrolni_obrazek(predloha, malba, format, polohy, cesta):
    sirka, vyska = predloha.size
    r = FORMATY[format][2] * sirka * 0.62
    radky = []
    for zdroj in (predloha, malba):
        radek = Image.new('RGB', (5 * 160, 160))
        for i, poloha in enumerate(polohy.values()):
            cx, cy = poloha[format][0] / 100 * sirka, poloha[format][1] / 100 * vyska
            vyrez = zdroj.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((160, 160))
            d = ImageDraw.Draw(vyrez)
            d.line((72, 80, 88, 80), fill='white')
            d.line((80, 72, 80, 88), fill='white')
            radek.paste(vyrez, (i * 160, 0))
        radky.append(radek)
    obr = Image.new('RGB', (800, 325), 'white')
    obr.paste(radky[0], (0, 0))
    obr.paste(radky[1], (0, 165))
    obr.save(cesta)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('motiv', help='název složky motivu, např. jaro, leto, zima, vanoce, silvestr, velikonoce')
    for f in FORMATY:
        p.add_argument('--' + f, metavar='SOUBOR', help=f'malba ve formátu {f}')
    p.add_argument('--jen-kontrola', action='store_true', help='jen změřit, nic neukládat')
    p.add_argument('--kontrola', metavar='SLOŽKA', help='uložit sem obrázky s výřezy lístků pro kontrolu')
    arg = p.parse_args()

    if not re.fullmatch(r'[a-z0-9-]+', arg.motiv) or arg.motiv == PREDLOHA:
        sys.exit('Neplatný název motivu.')
    zadane = [f for f in FORMATY if getattr(arg, f)]
    if not zadane:
        sys.exit('Zadejte aspoň jednu malbu (--ctverec, --vyska, --panorama).')

    polohy = polohy_listku()
    cil = os.path.join(MOTIVY, arg.motiv)
    chyba = False
    for format in zadane:
        rozmer, male, _ = FORMATY[format]
        print(f'{format}: {getattr(arg, format)}')
        predloha = Image.open(os.path.join(MOTIVY, PREDLOHA, format + '.webp')).convert('RGB')
        malba = nacti(getattr(arg, format), rozmer)

        posuny, listek = zmer_posuny(predloha, malba, format, polohy)
        dx = float(np.mean([v[0] for v in posuny.values()]))
        dy = float(np.mean([v[1] for v in posuny.values()]))
        if abs(dx) >= 0.5 or abs(dy) >= 0.5:
            print(f'  srovnání malby o {-dx:+.1f} px vodorovně a {-dy:+.1f} px svisle')
            m = np.float32([[1, 0, -dx], [0, 1, -dy]])
            malba = Image.fromarray(cv2.warpAffine(np.asarray(malba), m, rozmer, flags=cv2.INTER_LANCZOS4,
                                                   borderMode=cv2.BORDER_REPLICATE))
            posuny, listek = zmer_posuny(predloha, malba, format, polohy)
        for jmeno, (x, y, shoda) in posuny.items():
            odchylka = (x * x + y * y) ** 0.5 / listek
            v_poradku = odchylka <= MEZ_POSUNU and shoda >= MEZ_SHODY
            chyba |= not v_poradku
            print(f'  {"OK   " if v_poradku else "POZOR"} {jmeno:10} posun {x:+5.1f} {y:+5.1f} px '
                  f'({odchylka * 100:.1f} % lístku), podobnost {shoda:.2f}')
        if arg.kontrola:
            os.makedirs(arg.kontrola, exist_ok=True)
            kontrolni_obrazek(predloha, malba, format, polohy, os.path.join(arg.kontrola, f'{arg.motiv}-{format}.png'))

        if arg.jen_kontrola:
            continue
        os.makedirs(cil, exist_ok=True)
        malba.save(os.path.join(cil, format + '.webp'), quality=KVALITA, method=6)
        mensi = (male, round(rozmer[1] * male / rozmer[0]))
        malba.resize(mensi, Image.LANCZOS).save(os.path.join(cil, f'{format}-{male}.webp'), quality=KVALITA, method=6)
        if format == 'ctverec':
            malba.resize((48, 48), Image.LANCZOS).save(os.path.join(cil, 'pozadi.webp'), quality=KVALITA, method=6)
        print(f'  uloženo do assets/img/motivy/{arg.motiv}/')

    if chyba:
        print('\nNěkterý lístek nesedí. Malbu je potřeba zkontrolovat, případně nechat v Gemini upravit znovu.')
        sys.exit(1)
    if not arg.jen_kontrola:
        print(f"\nV assets/js/motivy.js doplňte u motivu {arg.motiv}: obrazky: {zadane}")


if __name__ == '__main__':
    main()
