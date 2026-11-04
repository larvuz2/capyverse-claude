"""Directions D, E, F — Luckiest Guy, two rows: CAPYVERSE on top of ODYSSEY.

Shared builder: each row is placed letter by letter (optional arch, per-letter tilt and bounce), then drawn
as a layer stack: dark extrusion (stacked offsets) -> dark outline -> gradient fill -> top shine.
D  Toybox      both rows near-equal, warm cream/yellow, brown extrusion, gentle bounce (party-game sticker)
E  Stumble     Stumble Guys structure: small white tilted CAPYVERSE, huge yellow->orange ODYSSEY, navy 3D block
F  Arch        CAPYVERSE arched like a carnival marquee in Cappy orange, ODYSSEY straight in a white tag
"""
import math
from svglogo import *

F = Font("LuckiestGuy")


def row(text, size, cx, base, arch=0.0, tilt=None, bounce=None, tracking=0.0, squash=1.0):
    """Returns [(d, transform)] for one row, centred on cx. arch = radius in px (0 = straight, >0 arches up)."""
    gl, w = F.word(text, size, tracking)
    out = []
    for i, (ch, d, x, adv, b) in enumerate(gl):
        gx = x + (b[0] + b[2]) / 2 - w / 2          # glyph centre relative to row centre
        gy = (b[1] + b[3]) / 2
        ang = math.degrees(gx / arch) if arch else 0.0
        px = cx + (arch * math.sin(math.radians(ang)) if arch else gx)
        py = base + (arch * (1 - math.cos(math.radians(ang))) if arch else 0.0)
        rot = ang + (tilt[i % len(tilt)] if tilt else 0)
        dy = bounce[i % len(bounce)] if bounce else 0
        xf = (f"translate({px:.1f},{py + dy:.1f}) rotate({rot:.2f}) scale(1,{squash}) "
              f"translate({-(b[0] + b[2]) / 2:.1f},{-gy:.1f}) translate(0,{gy:.1f})")
        out.append((d, xf))
    return out


def paths(r):
    return "".join(f'<path d="{d}" transform="{xf}"/>' for d, xf in r)


def layer_stack(r, uid, fill_stops, ink, stroke, depth, top, bottom, shine=True, sticker=None, size=200):
    p = paths(r)
    top, bottom = -size * 0.74, 0  # gradients resolve in each glyph's local space
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in fill_stops)
    ext = "".join(f'<g transform="translate({k * 0.35:.1f},{k})">{p}</g>' for k in range(2, depth + 1, 2))
    stk = (f'<g fill="{sticker}" stroke="{sticker}" stroke-width="{stroke * 2.6}" stroke-linejoin="round">{p}'
           f'<g transform="translate({depth * 0.35:.1f},{depth})">{p}</g></g>') if sticker else ""
    return f'''
  <defs>
    <linearGradient id="g{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="{bottom}">{grad}</linearGradient>
    <linearGradient id="s{uid}" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="{bottom}">
      <stop offset="0" stop-color="#fff" stop-opacity="0.65"/><stop offset="0.38" stop-color="#fff" stop-opacity="0"/></linearGradient>
  </defs>
  {stk}
  <g fill="{ink}" stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">{ext}{p}</g>
  <g fill="url(#g{uid})">{p}</g>
  {f'<g fill="url(#s{uid})">{p}</g>' if shine else ""}'''


def svg(body, W, H):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{body}</svg>'


def logo_d():
    W, H = 1500, 760; INK = "#3a1c0c"
    r1 = row("CAPYVERSE", 230, W / 2, 330, tilt=[-5, 3, -2, 4, -3, 2, -4, 3, -2], bounce=[6, -8, 4, -10, 6, -6, 8, -4, 2])
    r2 = row("ODYSSEY", 190, W / 2 + 40, 560, tilt=[3, -3, 2, -2, 3, -2, 2], bounce=[-4, 6, -6, 4, -2, 6, -4], tracking=0.02)
    yel = [(0, "#fff8d8"), (0.5, "#ffe58a"), (1, "#ffb62e")]
    org = [(0, "#ffb760"), (1, "#e9601b")]
    body = (layer_stack(r1, "d1", yel, INK, 26, 22, 160, 340, sticker="#fff3dc", size=230)
            + layer_stack(r2, "d2", org, INK, 24, 20, 420, 570, sticker="#fff3dc", size=190))
    return svg(body, W, H)


def logo_e():
    W, H = 1500, 820; NAVY = "#1d1240"
    r1 = row("CAPYVERSE", 170, W / 2 - 40, 250, tilt=[-7], bounce=[0], tracking=0.01)
    # rotate whole first row a little, Stumble-style
    r1 = [(d, f"rotate(-5 {W / 2} 200) {xf}") for d, xf in r1]
    r2 = row("ODYSSEY", 300, W / 2, 610, tilt=[-4, 3, -3, 4, -2, 3, -3], bounce=[10, -6, 6, -10, 4, -6, 8], tracking=-0.04)
    white = [(0, "#ffffff"), (1, "#e9ecf5")]
    gold = [(0, "#fff16a"), (0.45, "#ffc21f"), (1, "#ff6f13")]
    body = (layer_stack(r2, "e2", gold, NAVY, 32, 40, 390, 620, size=300)
            + layer_stack(r1, "e1", white, NAVY, 24, 22, 120, 260, shine=False, size=170))
    return svg(body, W, H)


def logo_f():
    W, H = 1500, 800; INK = "#2a140d"
    r1 = row("CAPYVERSE", 210, W / 2, 330, arch=1150, tilt=[0], bounce=[0], tracking=0.0)
    org = [(0, "#ffd36a"), (0.5, "#ff9a2e"), (1, "#e2551a")]
    body = layer_stack(r1, "f1", org, INK, 26, 24, 150, 400, sticker="#fff3dc", size=210)
    # ODYSSEY in a white tag under the arch
    r2 = row("ODYSSEY", 110, W / 2, 610, tracking=0.12)
    tw, th = 760, 150
    body += f'''
  <g transform="rotate(-2 {W / 2} 560)">
    <rect x="{W / 2 - tw / 2 + 10}" y="{560 - th / 2 + 14}" width="{tw}" height="{th}" rx="30" fill="{INK}"/>
    <rect x="{W / 2 - tw / 2}" y="{560 - th / 2}" width="{tw}" height="{th}" rx="30" fill="#fff3dc" stroke="{INK}" stroke-width="16"/>
    <g fill="{INK}">{paths(r2)}</g>
    <circle cx="{W / 2 - tw / 2 + 38}" cy="560" r="12" fill="{INK}"/><circle cx="{W / 2 + tw / 2 - 38}" cy="560" r="12" fill="{INK}"/>
  </g>'''
    return svg(body, W, H)


if __name__ == "__main__":
    for n, fn in (("logo_d", logo_d), ("logo_e", logo_e), ("logo_f", logo_f)):
        open(f"out/{n}.svg", "w").write(fn()); render(f"out/{n}.svg", f"out/{n}.png", 1500)
