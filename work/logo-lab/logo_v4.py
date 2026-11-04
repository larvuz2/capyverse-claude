"""Round 4: designed overlaps for D Toybox, E Stumble, H Viral Stumble (+ jetpack streaks)."""
import math
from lockup import *
from logo_v3 import stack, centre_rows, wrap, W, H, INK_BROWN, NAVY, CREAM, YEL, ORG, GOLD, WHITE, LG
from svglogo import render


def d3():
    r1, k1 = overlap_kern(lambda k: Row("CAPYVERSE", LG, 230, 800, 300, tracking=-0.05, kern=k,
                                        tilt=[-5, 3, -2, 3, -2, 2, -4, 3, -2], bounce=[6, -8, 4, -8, 6, -6, 8, -4, 2]))
    r2, _ = stack(r1, lambda dy: overlap_kern(lambda k: Row("ODYSSEY", LG, 200, 830, 300 + 150 + dy, tracking=-0.05, kern=k,
                  tilt=[3, -3, 2, -2, 3, -2, 2], bounce=[-4, 6, -6, 4, -2, 6, -4]))[0], gap=-12)
    body = draw_layered([r1, r2], [YEL, ORG], INK_BROWN, 24, 22, sticker=CREAM)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), k1


def e3():
    r1, k1 = overlap_kern(lambda k: Row("CAPYVERSE", LG, 270, 800, 320, tracking=-0.06, kern=k, rot=-4,
                                        tilt=[-3, 3, -2, 3, -3, 2, -3, 3, -2], bounce=[8, -6, 6, -10, 4, -6, 8, -4, 6]))
    r2, _ = stack(r1, lambda dy: overlap_kern(lambda k: Row("ODYSSEY", LG, 175, 860, 320 + 130 + dy, tracking=-0.04, kern=k, rot=-4,
                                                            tilt=[-6, -4, -6, -4, -6, -4, -6], bounce=[2, -2, 2, -2, 2, -2, 2]))[0], gap=-14)
    body = draw_layered([r1, r2], [GOLD, WHITE], NAVY, 30, 38)
    return wrap(body, W, H, *centre_rows([r1, r2], W, H)), k1


def h3():
    PINK, RED, BLUE = "#ff3d7f", "#ff2d4b", "#2e8bff"
    r1, k1 = overlap_kern(lambda k: Row("CAPYVERSE", LG, 260, 780, 320, tracking=-0.06, kern=k, rot=-3, skew=-6,
                                        tilt=[-2, 2, -2, 2, -2, 2, -2, 2, -2], bounce=[4, -4, 4, -6, 4, -4, 6, -4, 4]))
    from shapely.ops import unary_union
    x0, y0, x1, y1 = unary_union([p for _, p in r1.polys()]).bounds
    r2 = Row("DYSSEY", LG, 120, 0, 0, tracking=0.08); bw2 = r2.bbox()[2] - r2.bbox()[0]
    OD = 96; pw = bw2 + OD + 120; ph = 140
    px, py = x1 - pw + 10, y1 - 22
    r2 = Row("DYSSEY", LG, 120, px + 60 + OD + 18 + bw2 / 2, py + ph / 2 + 44, tracking=0.08)
    ocx, ocy = px + 60 + OD / 2, py + ph / 2
    pill = (f'<g transform="rotate(-3 {px + pw / 2} {py + ph / 2})">'
            f'<rect x="{px + 10}" y="{py + 14}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{NAVY}"/>'
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{ph / 2}" fill="{RED}" stroke="{NAVY}" stroke-width="14"/>'
            f'<g fill="#fff">{r2.svg_paths()}</g>'
            f'<circle cx="{ocx}" cy="{ocy}" r="{OD / 2}" fill="#fff"/>'
            f'<path d="M{ocx - 14} {ocy - 22} L{ocx + 24} {ocy} L{ocx - 14} {ocy + 22} Z" fill="{RED}" stroke="{RED}" stroke-width="7" stroke-linejoin="round"/></g>')
    bx, by, br = x1 + 40, y0 + 42, 54
    pts = " ".join(f"{bx + br * (1 + 0.09 * math.cos(a * 12)) * math.cos(a):.1f},{by + br * (1 + 0.09 * math.cos(a * 12)) * math.sin(a):.1f}"
                   for a in [2 * math.pi * i / 48 for i in range(48)])
    badge = (f'<polygon points="{pts}" fill="{NAVY}" stroke="{NAVY}" stroke-width="18" stroke-linejoin="round" transform="translate(6,8)"/>'
             f'<polygon points="{pts}" fill="{BLUE}" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
             f'<path d="M{bx - 22} {by + 1} L{bx - 5} {by + 18} L{bx + 24} {by - 16}" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>')
    # jetpack thruster streaks behind the C (same treatment as I Jetpack)
    jet = "".join(f'<g transform="translate({x0 + 14},{y0 + yy}) rotate(-3)"><path d="M0 -{t} L-{l} 0 L0 {t} Z" fill="#3fd4ff" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round"/>'
                  f'<path d="M0 -{t * 0.5} L-{l * 0.55} 0 L0 {t * 0.5} Z" fill="#fff"/></g>' for yy, l, t in [(95, 200, 24), (160, 150, 18), (215, 110, 13)])
    from shapely.ops import unary_union as uu
    allp = r1.svg_paths()
    shadow = f'<g transform="translate(16,20)" fill="{PINK}" stroke="{PINK}" stroke-width="30" stroke-linejoin="round">{allp}</g>'
    body = jet + shadow + draw_layered([r1], [WHITE], NAVY, 28, 18, shine=False) + pill + badge
    dx, dy = centre_rows([r1], W, H); dy -= 50
    return wrap(body, W, H, dx, dy), k1


ALL = {"logo_d3": d3, "logo_e3": e3, "logo_h3": h3}
if __name__ == "__main__":
    import sys
    for n in (sys.argv[1:] or ALL):
        svg, k = ALL[n](); open(f"out/{n}.svg", "w").write(svg); render(f"out/{n}.svg", f"out/{n}.png", 1600)
        print(n, k)
