"""Direction B — GOING VIRAL.

The story in one mark: capybaras went viral, Ophelia took it personally.
- Rubik Black outlines, sheared forward like a fast-scrolling feed
- CAPY wears a blue "verified" check (capybaras are the famous ones now)
- the A's counter is a red play button (the viral video)
- ODYSSEY is a red notification pill; a heart reaction pops off the C
- flat colours, one hard offset shadow: reads at 32 px, works on any background
"""
from svglogo import *

INK = "#160f26"; WHITE = "#ffffff"; PINK = "#ff3d7f"; BLUE = "#2e8bff"; RED = "#ff2d4b"; YEL = "#ffd23f"
F = Font("Rubikwght900")
S = 230
gl, w = F.word("CAPYVERSE", S, tracking=-0.035)
W_, H_ = 1800, 640
OX, OY = (W_ - w) / 2 - 20, 330
SHEAR = -10

word = "".join(f'<path d="{d}" transform="translate({x},0)"/>' for _, d, x, _, _ in gl)
A = gl[1]; ax, ab = A[2], A[4]
# the A's counter (measured: centre 86,-81, 24x41) tinted red
play = f'<path d="M{ax + 86} {-104} L{ax + 99} {-60} L{ax + 73} {-60} Z" fill="{RED}"/>'

E = gl[-1]; ex = E[2] + E[4][2]


def badge(cx, cy, r):
    """Scalloped verified badge with a check."""
    import math
    pts = []
    for i in range(48):
        a = math.pi * 2 * i / 48
        rr = r * (1 + 0.09 * math.cos(a * 12))
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    shape = f'<polygon points="{" ".join(pts)}"/>'
    check = f'<path d="M{cx - r * 0.42} {cy + r * 0.02} L{cx - r * 0.1} {cy + r * 0.34} L{cx + r * 0.45} {cy - r * 0.3}" fill="none" stroke="{WHITE}" stroke-width="{r * 0.2}" stroke-linecap="round" stroke-linejoin="round"/>'
    return shape, check


bshape, bcheck = badge(ex + 70, -150, 52)
heart = 'M0 12 C-30 -10 -22 -38 0 -24 C22 -38 30 -10 0 12 Z'

gl2, w2 = F.word("DYSSEY", 92, tracking=0.16)
OD = 92 * 0.78  # play-button O diameter
PX = OX + w - w2 - 230; PY = OY + 50; PW = w2 + OD + 150; PH = 128
ody = "".join(f'<path d="{d}" transform="translate({PX + 60 + OD + 18 + x},{PY + PH / 2 + 34})"/>' for _, d, x, _, _ in gl2)
ocx, ocy = PX + 60 + OD / 2, PY + PH / 2
play_o = (f'<circle cx="{ocx}" cy="{ocy}" r="{OD / 2 + 4}" fill="{WHITE}"/>'
          f'<path d="M{ocx - 11} {ocy - 18} L{ocx + 19} {ocy} L{ocx - 11} {ocy + 18} Z" fill="{RED}" stroke="{RED}" stroke-width="6" stroke-linejoin="round"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}">
<g transform="translate({OX},{OY}) skewX({SHEAR})">
  <!-- hard offset shadow -->
  <g transform="translate(16,16)" fill="{PINK}" stroke="{PINK}" stroke-width="26" stroke-linejoin="round">{word}<g transform="translate(0,0)">{bshape}</g></g>
  <!-- outline + white fill -->
  <g fill="{INK}" stroke="{INK}" stroke-width="26" stroke-linejoin="round">{word}</g>
  <g fill="{WHITE}">{word}</g>
  {play}
  <!-- verified -->
  <g fill="{INK}" stroke="{INK}" stroke-width="16" stroke-linejoin="round">{bshape}</g>
  <g fill="{BLUE}">{bshape}</g>{bcheck}
  <!-- heart reaction popping off the C -->
  <g transform="translate(-30,-215) rotate(-14) scale(1.7)">
    <path d="{heart}" fill="{INK}" stroke="{INK}" stroke-width="9" stroke-linejoin="round" transform="translate(4,4)"/>
    <path d="{heart}" fill="{RED}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
    <circle cx="-8" cy="-14" r="4" fill="#fff"/>
  </g>
  <g fill="{YEL}" stroke="{INK}" stroke-width="5">
    <circle cx="-62" cy="-232" r="8"/><circle cx="38" cy="-262" r="6"/><circle cx="-40" cy="-290" r="5"/>
  </g>
</g>
<!-- ODYSSEY notification pill -->
<g transform="rotate(-4 {PX + PW / 2} {PY + PH / 2})">
  <rect x="{PX + 12}" y="{PY + 12}" width="{PW}" height="{PH}" rx="{PH / 2}" fill="{INK}"/>
  <rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="{PH / 2}" fill="{RED}" stroke="{INK}" stroke-width="12"/>
  <g fill="{WHITE}">{ody}</g>{play_o}
</g>
</svg>'''

if __name__ == "__main__":
    open("out/logo_b.svg", "w").write(svg)
    render("out/logo_b.svg", "out/logo_b.png", 1600)
