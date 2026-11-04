"""Round 5: E4 Stumble (only Y/V overlap) and the GPT Stumble version with a solid backing behind the letters."""
from lockup import *
from logo_v3 import stack, centre_rows, wrap, W, H, NAVY, GOLD, WHITE, LG
from svglogo import render


def selective_kern(make, overlap_pairs=(), lo=0.015, hi=0.035, gap_lo=3.0, gap_hi=9.0, step=2.0, limit=120):
    """Pairs in overlap_pairs overlap by lo..hi of the smaller glyph; every other pair sits gap_lo..gap_hi px apart."""
    kern = {}
    for _ in range(limit):
        r = make(kern); ps = r.polys(); changed = False
        for i in range(len(ps) - 1):
            a, b = ps[i][1], ps[i + 1][1]
            if i in overlap_pairs:
                ratio = a.intersection(b).area / min(a.area, b.area)
                if ratio > hi: kern[i + 1] = kern.get(i + 1, 0) + step; changed = True
                elif ratio < lo: kern[i + 1] = kern.get(i + 1, 0) - step; changed = True
            else:
                d = a.distance(b)
                if d < gap_lo: kern[i + 1] = kern.get(i + 1, 0) + step; changed = True
                elif d > gap_hi: kern[i + 1] = kern.get(i + 1, 0) - step; changed = True
        if not changed: return r, kern
    return r, kern


def e4():
    # CAPYVERSE: C0 A1 P2 Y3 V4 E5 R6 S7 E8 -> only pair 3 (Y/V) overlaps
    r1, k1 = selective_kern(lambda k: Row("CAPYVERSE", LG, 270, 800, 320, tracking=-0.02, kern=k, rot=-4,
                                          tilt=[-3, 3, -2, 3, -3, 2, -3, 3, -2], bounce=[8, -6, 6, -10, 4, -6, 8, -4, 6]),
                            overlap_pairs=(3,))
    r2, _ = stack(r1, lambda dy: selective_kern(lambda k: Row("ODYSSEY", LG, 175, 860, 320 + 130 + dy, tracking=0.0, kern=k, rot=-4,
                                                              tilt=[-6, -4, -6, -4, -6, -4, -6], bounce=[2, -2, 2, -2, 2, -2, 2]))[0], gap=-14)
    body = draw_layered([r1, r2], [GOLD, WHITE], NAVY, 30, 38)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), k1


if __name__ == "__main__":
    svg, k = e4(); open("out/logo_e4.svg", "w").write(svg); render("out/logo_e4.svg", "out/logo_e4.png", 1600); print("e4", k)
