"""Round 3: six unified two-row lockups (D2, E2, F2, G, H, I).

Every lockup is built with lockup.py: letters auto-kerned until no two neighbours touch (4 px gap), the second row
auto-stacked as close as possible to the first (8 px between letters), and all rows drawn as one object.
"""
import math
from lockup import *
from svglogo import render

LG = "LuckiestGuy"


def autokern(make, gap=5.0, step=3.0, limit=60):
    kern = {}
    for _ in range(limit):
        r = make(kern); bad = r.check(gap)
        if not bad: return r, kern
        for i, *_ in bad: kern[i + 1] = kern.get(i + 1, 0) + step
    return r, kern


def stack(top, make_bottom, gap=8.0, start=-60, step=2.0):
    """Lower the bottom row from an overlapping start until its letters clear the top row by `gap` px."""
    from shapely.ops import unary_union
    U = unary_union([p for _, p in top.polys()]).buffer(gap)
    dy = start
    while True:
        b = make_bottom(dy)
        if not unary_union([p for _, p in b.polys()]).intersects(U): return b, dy
        dy += step


def centre_rows(rows, W, H):
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for r in rows for _, p in r.polys()]).bounds
    return (W - (x0 + x1)) / 2, (H - (y0 + y1)) / 2


def wrap(body, W, H, dx, dy):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><g transform="translate({dx:.1f},{dy:.1f})">{body}</g></svg>'


W, H = 1600, 760
INK_BROWN, NAVY, CREAM = "#3a1c0c", "#1d1240", "#fff3dc"
YEL = [(0, "#fff8d8"), (0.5, "#ffe58a"), (1, "#ffb62e")]
ORG = [(0, "#ffb760"), (1, "#e9601b")]
GOLD = [(0, "#fff16a"), (0.45, "#ffc21f"), (1, "#ff6f13")]
WHITE = [(0, "#ffffff"), (1, "#e6e9f4")]


# ---------- D2 Toybox: same look, rows fused, no collisions ----------
def d2():
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 230, 800, 300, tracking=0.0, kern=k,
                                    tilt=[-5, 3, -2, 3, -2, 2, -4, 3, -2], bounce=[6, -8, 4, -8, 6, -6, 8, -4, 2]))
    r2, dy = stack(r1, lambda dy: autokern(lambda k: Row("ODYSSEY", LG, 200, 830, 300 + 150 + dy, kern=k,
                   tilt=[3, -3, 2, -2, 3, -2, 2], bounce=[-4, 6, -6, 4, -2, 6, -4]))[0])
    body = draw([r1, r2], [YEL, ORG], INK_BROWN, 26, 22, sticker=CREAM)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), (k1,)


# ---------- E2 Stumble: CAPYVERSE big gold on top, ODYSSEY white below, one navy block ----------
def e2():
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 270, 800, 320, tracking=-0.02, kern=k, rot=-4,
                                    tilt=[-3, 3, -2, 3, -3, 2, -3, 3, -2], bounce=[8, -6, 6, -10, 4, -6, 8, -4, 6]))
    r2, _ = stack(r1, lambda dy: autokern(lambda k: Row("ODYSSEY", LG, 175, 860, 320 + 130 + dy, tracking=0.02, kern=k, rot=-4,
                                                         tilt=[-6], bounce=[0]))[0])
    body = draw([r1, r2], [GOLD, WHITE], NAVY, 32, 38)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), (k1,)


# ---------- F2 Marquee: arched CAPYVERSE, ODYSSEY tag tucked under the arch, one sticker ----------
def f2():
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 230, 800, 330, arch=1050, kern=k, tilt=[0], bounce=[0]))
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for _, p in r1.polys()]).bounds
    r2 = Row("ODYSSEY", LG, 112, 800, 0, tracking=0.12)
    bw = r2.bbox()[2] - r2.bbox()[0] + 140; bh = 150
    # tag top sits 6 px under the middle letters' baseline (the arch leaves room there)
    mid_bottom = max(p.bounds[3] for ch, p in r1.polys()[3:6])
    ty = mid_bottom + 6; r2 = Row("ODYSSEY", LG, 112, 800, ty + bh / 2 + 40, tracking=0.12)
    tag = f'<rect x="{800 - bw / 2}" y="{ty}" width="{bw}" height="{bh}" rx="34"/>'
    under = tag
    over = (f'<rect x="{800 - bw / 2}" y="{ty}" width="{bw}" height="{bh}" rx="34" fill="{CREAM}" stroke="{INK_BROWN}" stroke-width="16"/>'
            f'<g fill="{INK_BROWN}">{r2.svg_paths()}</g>'
            f'<circle cx="{800 - bw / 2 + 36}" cy="{ty + bh / 2}" r="11" fill="{INK_BROWN}"/><circle cx="{800 + bw / 2 - 36}" cy="{ty + bh / 2}" r="11" fill="{INK_BROWN}"/>')
    ext_tag = f'<g fill="{INK_BROWN}"><rect x="{800 - bw / 2 + 8}" y="{ty + 14}" width="{bw}" height="{bh}" rx="34"/></g>'
    from shapely.geometry import box as _box
    body = draw([r1], [ORG], INK_BROWN, 26, 24, sticker=CREAM, extra_under=under, extra_over=ext_tag + over,
                sil_extra=_box(800 - bw / 2 + 20, ty - 4, 800 + bw / 2 - 20, ty + 40))
    rows_box = [r1]
    dx, dy = centre_rows(rows_box, W, H); dy -= 40
    return wrap(body, W, H, dx, dy), (k1,)


# ---------- G Popcorn Band: CAPYVERSE + ODYSSEY on a popcorn-bucket stripe, fused ----------
def g():
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 250, 800, 320, kern=k, tilt=[-3, 2, -2, 2, -2, 2, -3, 2, -2], bounce=[4, -4, 2, -6, 4, -2, 6, -2, 2]))
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for _, p in r1.polys()]).bounds
    bh, bw = 140, 860; by = y1 - 18  # band tucks 18 px under the letters
    r2 = Row("ODYSSEY", LG, 120, 800, by + bh / 2 + 44, tracking=0.12)
    stripes = "".join(f'<rect x="{800 - bw / 2 - 200 + i * 62}" y="{by - 10}" width="30" height="{bh + 20}" transform="skewX(-20)"/>' for i in range(24))
    band_shape = f'<rect x="{800 - bw / 2}" y="{by}" width="{bw}" height="{bh}" rx="40"/>'
    under = band_shape
    band = (f'<defs><clipPath id="bc">{band_shape}</clipPath></defs>'
            f'<g fill="{INK_BROWN}"><rect x="{800 - bw / 2 + 6}" y="{by + 16}" width="{bw}" height="{bh}" rx="40"/></g>'
            f'<rect x="{800 - bw / 2}" y="{by}" width="{bw}" height="{bh}" rx="40" fill="#fff"/>'
            f'<g clip-path="url(#bc)" fill="#ef3b3b">{stripes}</g>'
            f'<rect x="{800 - bw / 2}" y="{by}" width="{bw}" height="{bh}" rx="40" fill="none" stroke="{INK_BROWN}" stroke-width="16"/>'
            f'<g fill="#fff" stroke="{INK_BROWN}" stroke-width="18" stroke-linejoin="round" paint-order="stroke">{r2.svg_paths()}</g>')
    from shapely.geometry import box as _box
    band_top = ''
    # band is drawn first, the big word sits on top of it (letters overlap the band edge = one object)
    allp = r1.svg_paths()
    body = (f'<g fill="{CREAM}" stroke="{CREAM}" stroke-width="68" stroke-linejoin="round">{allp}<g transform="translate(8,24)">{allp}</g>{under}</g>'
            + draw([r1], [YEL], INK_BROWN, 26, 22, sil_extra=_box(800 - bw / 2 + 20, by - 4, 800 + bw / 2 - 20, by + 30)) + band)
    dx, dy = centre_rows([r1], W, H); dy -= 60
    return wrap(body, W, H, dx, dy), (k1,)


# ---------- H Viral Stumble: E's two-row build + B's verified badge, notification pill and play button ----------
def h():
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 260, 780, 320, kern=k, rot=-3, skew=-6,
                                    tilt=[-2, 2, -2, 2, -2, 2, -2, 2, -2], bounce=[4, -4, 4, -6, 4, -4, 6, -4, 4]))
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for _, p in r1.polys()]).bounds
    PINK, RED, BLUE = "#ff3d7f", "#ff2d4b", "#2e8bff"
    r2 = Row("DYSSEY", LG, 120, 0, 0, tracking=0.1); bw2 = r2.bbox()[2] - r2.bbox()[0]
    OD = 96; pw = bw2 + OD + 120; ph = 140
    px, py = x1 - pw + 10, y1 - 14
    r2 = Row("DYSSEY", LG, 120, px + 60 + OD + 18 + bw2 / 2, py + ph / 2 + 44, tracking=0.1)
    ocx, ocy = px + 60 + OD / 2, py + ph / 2
    pill = (f'<g transform="rotate(-3 {px + pw / 2} {py + ph / 2})">'
            f'<rect x="{px + 10}" y="{py + 14}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{NAVY}"/>'
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{RED}" stroke="{NAVY}" stroke-width="14"/>'
            f'<g fill="#fff">{r2.svg_paths()}</g>'
            f'<circle cx="{ocx}" cy="{ocy}" r="{OD / 2}" fill="#fff"/>'
            f'<path d="M{ocx - 14} {ocy - 22} L{ocx + 24} {ocy} L{ocx - 14} {ocy + 22} Z" fill="{RED}" stroke="{RED}" stroke-width="7" stroke-linejoin="round"/></g>')
    # verified badge after the last letter
    bx, by, br = x1 + 46, y0 + 40, 54
    pts = " ".join(f"{bx + br * (1 + 0.09 * math.cos(a * 12)) * math.cos(a):.1f},{by + br * (1 + 0.09 * math.cos(a * 12)) * math.sin(a):.1f}"
                   for a in [2 * math.pi * i / 48 for i in range(48)])
    badge = (f'<polygon points="{pts}" fill="{NAVY}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round" transform="translate(6,8)"/>'
             f'<polygon points="{pts}" fill="{BLUE}" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
             f'<path d="M{bx - 22} {by + 1} L{bx - 5} {by + 18} L{bx + 24} {by - 16}" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    allp = r1.svg_paths()
    shadow = f'<g transform="translate(16,20)" fill="{PINK}" stroke="{PINK}" stroke-width="32" stroke-linejoin="round">{allp}</g>'
    body = shadow + draw([r1], [WHITE], NAVY, 30, 18, shine=False) + pill + badge
    dx, dy = centre_rows([r1], W, H); dy -= 50; dx -= 40
    return wrap(body, W, H, dx, dy), (k1,)


# ---------- I Jetpack: CAPYVERSE takes off up a ramp, speed cuts on the left, ODYSSEY trails underneath ----------
def i_():
    n = 9
    r1, k1 = autokern(lambda k: Row("CAPYVERSE", LG, 250, 800, 330, kern=k, skew=-12, rot=-6,
                                    tilt=[0], bounce=[24 - 6 * j for j in range(n)]))
    r2, _ = stack(r1, lambda dy: autokern(lambda k: Row("ODYSSEY", LG, 150, 960, 330 + 120 + dy, kern=k, skew=-12, rot=-6,
                                                        tracking=0.06, tilt=[0], bounce=[12 - 3 * j for j in range(7)]))[0], gap=8)
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for r in (r1, r2) for _, p in r.polys()]).bounds
    flame = "".join(f'<g transform="translate({x0 + 10},{y0 + yy}) rotate(-6)"><path d="M0 -{t} L-{l} 0 L0 {t} Z" fill="#3fd4ff" stroke="{NAVY}" stroke-width="8" stroke-linejoin="round"/>'
                    f'<path d="M0 -{t * 0.5} L-{l * 0.55} 0 L0 {t * 0.5} Z" fill="#fff"/></g>' for yy, l, t in [(110, 190, 22), (175, 140, 16)])
    mask = ""
    body = flame + draw([r1, r2], [GOLD, WHITE], NAVY, 30, 30, sticker=CREAM, sticker_w=2.2)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), (k1,)


ALL = {"logo_d2": d2, "logo_e2": e2, "logo_f2": f2, "logo_g": g, "logo_h": h, "logo_i": i_}

if __name__ == "__main__":
    import sys
    for name in (sys.argv[1:] or ALL):
        svg, info = ALL[name]()
        open(f"out/{name}.svg", "w").write(svg); render(f"out/{name}.svg", f"out/{name}.png", 1600)
        print(name, "kerning added:", info)
