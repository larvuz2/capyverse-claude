"""Capyverse Odyssey — 'Charred' logo, 100% code, no image model.
Tall Sancreek letters (stretched 1.45x) made of shou-sugi-ban burnt timber: procedural dark wood grain,
alligator char cracks glowing with embers (hotter toward the bottom), a cool top-edge highlight, and a bone keyline.
ODYSSEY in wide-spaced ember letters between two charred rules."""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/logo-lab")
from lockup import Row, font
from logo_v5 import selective_kern
from shapely.ops import unary_union
from svglogo import render

W, H = 1700, 900
SY = 1.45
r1, _ = selective_kern(lambda k: Row("CAPYVERSE", "Sancreek", 230, 850, 470, tracking=0.0, kern=k, scale_y=SY,
                                     tilt=[-1, 0.8, -0.6, 1, -0.8, 0.6, -1, 0.8, -0.6], bounce=[4, -3, 2, -5, 3, -3, 5, -2, 2]),
                       overlap_pairs=(), gap_lo=10, gap_hi=16)
p1 = r1.svg_paths()
x0, y0, x1, y1 = unary_union([p for _, p in r1.polys()]).bounds

F2 = font("BigShouldersDisplaywght900")
gl2, w2 = F2.word("ODYSSEY", 86, 0.55)
bx = 850 - w2 / 2; by = y1 + 120
ody = "".join(f'<path d="{d}" transform="translate({bx + x:.1f},{by:.1f})"/>' for _, d, x, _, _ in gl2)
ry = by - 32
rules = (f'<rect x="{x0 + 10:.0f}" y="{ry - 4:.0f}" width="{bx - 40 - x0:.0f}" height="8" rx="4"/>'
         f'<rect x="{bx + w2 + 30:.0f}" y="{ry - 4:.0f}" width="{x1 - 10 - (bx + w2 + 30):.0f}" height="8" rx="4"/>')

INK = "#0b0706"; BONE = "#e9dcc4"
ext = "".join(f'<g transform="translate({k * 0.3:.1f},{k})">{p1}</g>' for k in range(2, 22, 2))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  <filter id="char" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}" color-interpolation-filters="sRGB">
    <!-- burnt grain: stretched noise -> rings -> very dark brown/black -->
    <feTurbulence type="fractalNoise" baseFrequency="0.02 0.0035" numOctaves="4" seed="21" result="n"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.01 0.003" numOctaves="2" seed="4" result="warp"/>
    <feDisplacementMap in="n" in2="warp" scale="70" xChannelSelector="R" yChannelSelector="G" result="nw"/>
    <feColorMatrix in="nw" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="g"/>
    <feComponentTransfer in="g" result="rings">
      <feFuncR type="table" tableValues="0.1 0.6 0.2 0.9 0.15 0.7 0.3 1 0.2"/>
      <feFuncG type="table" tableValues="0.1 0.6 0.2 0.9 0.15 0.7 0.3 1 0.2"/>
      <feFuncB type="table" tableValues="0.1 0.6 0.2 0.9 0.15 0.7 0.3 1 0.2"/>
    </feComponentTransfer>
    <feComponentTransfer in="rings" result="wood">
      <feFuncR type="linear" slope="0.30" intercept="0.04"/><feFuncG type="linear" slope="0.18" intercept="0.03"/><feFuncB type="linear" slope="0.11" intercept="0.025"/>
    </feComponentTransfer>
    <!-- carved bevel, cool moonlight from top-left -->
    <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="bump"/>
    <feSpecularLighting in="bump" surfaceScale="6" specularConstant="0.28" specularExponent="34" lighting-color="#b9c4d6" result="spec">
      <feDistantLight azimuth="230" elevation="40"/></feSpecularLighting>
    <feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
    <feMerge result="all"><feMergeNode in="wood"/><feMergeNode in="specIn"/></feMerge>
    <feComposite in="all" in2="SourceAlpha" operator="in"/>
  </filter>
  <filter id="embers" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}" color-interpolation-filters="sRGB">
    <feTurbulence type="turbulence" baseFrequency="0.014 0.011" numOctaves="2" seed="13" result="cn"/>
    <feColorMatrix in="cn" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="ca"/>
    <feComponentTransfer in="ca" result="cracks"><feFuncA type="table" tableValues="0 0 0 0 0 0 0 0.9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"/></feComponentTransfer>
    <feFlood flood-color="#ff5a0a" result="hot"/><feComposite in="hot" in2="cracks" operator="in" result="emb"/>
    <feGaussianBlur in="emb" stdDeviation="2.5" result="g"/>
    <feFlood flood-color="#ffd27a"/><feComposite in2="cracks" operator="in" result="core"/>
    <feMerge result="m"><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="core"/><feMergeNode in="core"/></feMerge>
    <feComposite in="m" in2="SourceAlpha" operator="in"/>
  </filter>
  <linearGradient id="heatG" x1="0" y1="{y0:.0f}" x2="0" y2="{y1:.0f}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#111"/><stop offset="0.3" stop-color="#666"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <filter id="emberText" x="-10%" y="-40%" width="120%" height="180%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="6" result="b"/><feFlood flood-color="#ff6a12" flood-opacity="0.75"/>
    <feComposite in2="b" operator="in" result="glow"/><feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="emberFill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset="0.55" stop-color="#ff8a24"/><stop offset="1" stop-color="#e2420a"/></linearGradient>
</defs>
<!-- bone keyline around everything -->
<g fill="{BONE}" stroke="{BONE}" stroke-width="30" stroke-linejoin="round">{p1}<g transform="translate(6,20)">{p1}</g>{ody}{rules}</g>
<g fill="{INK}" stroke="{INK}" stroke-width="12" stroke-linejoin="round">{ody}{rules}</g>
<!-- extrusion + outline -->
<g fill="{INK}" stroke="{INK}" stroke-width="14" stroke-linejoin="round">{ext}{p1}</g>
<!-- charred timber with embers: the heat mask lives inside the filter via feImage-free trick: a gradient layer clipped -->
<g filter="url(#char)">{p1}</g>
<mask id="m" maskUnits="userSpaceOnUse" maskContentUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#heatG)"/></mask>
<g mask="url(#m)"><g filter="url(#embers)">{p1}</g></g>
<g fill="url(#emberFill)" filter="url(#emberText)">{ody}</g>
<g fill="#3a1a0a">{rules}</g>
</svg>'''
open("logo.svg", "w").write(svg)
render("/home/user/capyverse-claude/work/logo-code2/logo.svg", "/home/user/capyverse-claude/work/logo-code2/logo.png", 1700)
print("ok", round(x0), round(y0), round(x1), round(y1))
