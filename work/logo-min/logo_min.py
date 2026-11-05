"""Round 11 — three minimalist agency-style wordmarks, built by hand as true vectors (font outlines -> SVG paths).
Each comes in two colourways: 'ink' (for the orange capsule / light) and 'cream' (for dark store backgrounds).
"""
import math
from svglogo import Font, render

INK, CREAM, ORANGE, LEAF = "#1c1530", "#fff4e2", "#ff7a1a", "#3bb36a"


def word(F, text, size, x0, base, tracking=0.0):
    gl, w = F.word(text, size, tracking)
    return [(ch, d, x0 + x, b) for ch, d, x, adv, b in gl], w


def paths(gl, fill, base, dy=0):
    return "".join(f'<path d="{d}" transform="translate({x:.1f},{base + dy:.1f})" fill="{fill}"/>' for _, d, x, _ in gl)


def svg(body, W, H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{body}</svg>'


# 1 — THE MANDARIN: one clean grotesk wordmark; the O of ODYSSEY is a mandarin (the capybara-with-an-orange meme).
def mandarin(col):
    F = Font("BricolageGrotesqueopszwght96800")
    W, H = 1600, 560
    S1 = 230
    _, w1 = F.word("CAPYVERSE", S1, -0.035)
    x1 = (W - w1) / 2; b1 = 270
    g1, _ = word(F, "CAPYVERSE", S1, x1, b1, -0.035)
    S2 = 96; tr = 0.28
    _, w2 = F.word("DYSSEY", S2, tr)
    od = S2 * 0.74  # mandarin diameter ~ cap height
    gap = S2 * 0.28
    total = od + gap + w2
    x2 = x1 + w1 - total; b2 = b1 + 150   # right-aligned to the end of CAPYVERSE
    g2, _ = word(F, "DYSSEY", S2, x2 + od + gap, b2, tr)
    cx, cy, r = x2 + od / 2, b2 - S2 * 0.36, od / 2
    leaf = (f'<path d="M{cx + r * 0.05:.1f},{cy - r * 0.95:.1f} c{r * 0.15:.1f},{-r * 0.55:.1f} {r * 0.75:.1f},{-r * 0.7:.1f} {r * 1.05:.1f},{-r * 0.5:.1f} '
            f'c{-r * 0.2:.1f},{r * 0.45:.1f} {-r * 0.7:.1f},{r * 0.6:.1f} {-r * 1.05:.1f},{r * 0.5:.1f}z" fill="{LEAF}"/>')
    body = (paths(g1, col, b1) + paths(g2, col, b2) +
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{ORANGE}"/>' + leaf +
            f'<circle cx="{cx - r * 0.32:.1f}" cy="{cy - r * 0.3:.1f}" r="{r * 0.16:.1f}" fill="#ffffff" fill-opacity="0.55"/>')
    return svg(body, W, H)


# 2 — FLIGHT LINE: wide Syne wordmark; the Y's stem drops and becomes one continuous jetpack line that underlines the name.
def flight(col):
    F = Font("Synewght800")
    S1 = 200
    _, w1 = F.word("CAPYVERSE", S1, -0.01)
    W, H = int(w1 + 260), 520
    x1 = (W - w1) / 2 + 40; b1 = 250
    g1, _ = word(F, "CAPYVERSE", S1, x1, b1, -0.01)
    ch, d, xy, b = [g for g in g1 if g[0] == "Y"][0]
    yx = xy + (b[0] + b[2]) / 2   # centre of the Y stem
    sw = S1 * 0.11                # line weight ~ stroke weight
    ly = b1 + 70                  # line height
    path = (f'M{x1 + 10:.1f},{ly:.1f} L{yx - 70:.1f},{ly:.1f} C{yx - 25:.1f},{ly:.1f} {yx:.1f},{ly - 20:.1f} {yx:.1f},{ly - 60:.1f} L{yx:.1f},{b1 - 30:.1f}')
    line = f'<path d="{path}" fill="none" stroke="{ORANGE}" stroke-width="{sw:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    puffs = "".join(f'<circle cx="{x1 + 10 - k * sw * 1.15:.1f}" cy="{ly:.1f}" r="{sw * (0.42 - k * 0.12):.1f}" fill="{ORANGE}" fill-opacity="{0.8 - k * 0.25:.2f}"/>' for k in range(1, 3))
    S2 = 70
    _, w2 = F.word("ODYSSEY", S2, 0.42)
    g2, _ = word(F, "ODYSSEY", S2, x1 + w1 - w2, b1 + 165, 0.42)
    body = line + puffs + paths(g1, col, b1) + paths(g2, col, b1 + 165)
    return svg(body, W, H)


# 3 — SWISS STACK: CAPY over VERSE, both set to the same width, ODYSSEY running vertically up the right edge in orange.
def stack(col):
    F = Font("ArchivoBlack")
    _, wv = F.word("VERSE", 200, -0.03)
    _, wc = F.word("CAPY", 200, -0.03)
    sv = 200; sc = 200 * wv / wc            # scale CAPY so both lines are exactly the same width
    capH = lambda s: s * 0.72
    x0 = 60; top = 50
    bc = top + capH(sc); gap = sc * 0.06
    bv = bc + gap + capH(sv)
    gc, _ = word(F, "CAPY", sc, x0, bc, -0.03)
    gv, _ = word(F, "VERSE", sv, x0, bv, -0.03)
    blockH = bv - top
    S2 = 64; tr = 0.30
    _, w2 = F.word("ODYSSEY", S2, tr)
    s2 = S2 * min(1.0, blockH / w2)
    _, w2 = F.word("ODYSSEY", s2, tr)
    g2, _ = word(F, "ODYSSEY", s2, 0, 0, tr)
    xr = x0 + wv + 34
    rot = "".join(f'<path d="{d}" fill="{ORANGE}" transform="translate({xr + capH(s2):.1f},{bv:.1f}) rotate(-90) translate({x:.1f},0)"/>' for _, d, x, _ in g2)
    W, H = int(xr + capH(s2) + 60), int(bv + 50)
    body = paths(gc, col, bc) + paths(gv, col, bv) + rot
    return svg(body, W, H)


ALL = {"1_mandarin": mandarin, "2_flight": flight, "3_stack": stack}

if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    for n, fn in ALL.items():
        for cw, col in (("ink", INK), ("cream", CREAM)):
            open(f"out/{n}_{cw}.svg", "w").write(fn(col))
            render(f"out/{n}_{cw}.svg", f"out/{n}_{cw}.png", 1800)
