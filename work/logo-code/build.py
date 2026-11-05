"""Capyverse Odyssey — one logo, 100% code. No image model.
Concept: CAPYVERSE is carved out of ONE plank (the procedural grain runs continuously through every letter),
ODYSSEY is burned into a second plank whose O is a real knot in the wood, and a mandarin sits on the A
(the chill-capybara-with-an-orange joke). Wood = SVG feTurbulence stretched along the grain, banded into rings,
coloured, then lit with feDiffuseLighting for a carved bevel. Rendered with Chromium."""
import sys, math, random
sys.path.insert(0, "/home/user/capyverse-claude/work/logo-lab")
from lockup import Row, svgm
from logo_v5 import selective_kern
from logo_v3 import stack
from shapely.ops import unary_union
from svglogo import render

LG = "LuckiestGuy"
W, H = 1700, 820
INK = "#2b1608"; CREAM = "#fff1d8"

# --- letters: gentle hand-set bounce/tilt, auto-spaced so nothing collides ---
r1, _ = selective_kern(lambda k: Row("CAPYVERSE", LG, 270, 850, 360, tracking=0.0, kern=k,
                                     tilt=[-4, 3, -2, 3, -3, 2, -4, 3, -2], bounce=[8, -8, 4, -10, 6, -6, 10, -4, 4]),
                       overlap_pairs=(), gap_lo=6, gap_hi=12)
p1 = r1.svg_paths()
U = unary_union([p for _, p in r1.polys()])
x0, y0, x1, y1 = U.bounds

# --- plank for ODYSSEY ---
pw, ph = 760, 168
px, py = 850 - pw / 2, y1 + 6
from lockup import font
F2 = font("LuckiestGuy"); gl2, w2 = F2.word("DYSSEY", 112, 0.10)
kn = 104                                   # knot diameter (the O)
tx = 850 - (w2 + kn + 26) / 2
base2 = py + ph / 2 + 42
dys = "".join(f'<path d="{d}" transform="translate({tx + kn + 26 + x:.1f},{base2:.1f})"/>' for _, d, x, _, _ in gl2)
kx, ky = tx + kn / 2, base2 - 40

def plank_path(x, y, w, h, seed):
    rnd = random.Random(seed); pts = []
    for i in range(13): pts.append((x + w * i / 12, y + rnd.uniform(-4, 4)))
    pts.append((x + w + rnd.uniform(-3, 3), y + h / 2))
    for i in range(12, -1, -1): pts.append((x + w * i / 12, y + h + rnd.uniform(-4, 4)))
    pts.append((x + rnd.uniform(-3, 3), y + h / 2))
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "Z"

plank = plank_path(px, py, pw, ph, 3)

def wood_filter(fid, freq, seed, lo, hi, bands="0.15 0.7 1 0.5 0.95 0.3 0.85 0.55 1 0.4", bevel=6, scale=7):
    """Procedural wood: stretched fractal noise -> ring bands -> brown ramp -> carved light."""
    (r0, g0, b0), (r1_, g1, b1) = lo, hi
    return f'''
  <filter id="{fid}" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="4" seed="{seed}" result="n"/>
    <feColorMatrix in="n" type="matrix" values="1 0 0 0 0  1 0 0 0 0  1 0 0 0 0  0 0 0 0 1" result="g"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.004 0.012" numOctaves="2" seed="{seed + 9}" result="warp"/>
    <feDisplacementMap in="g" in2="warp" scale="60" xChannelSelector="R" yChannelSelector="G" result="gw"/>
    <feComponentTransfer in="gw" result="rings">
      <feFuncR type="table" tableValues="{bands}"/><feFuncG type="table" tableValues="{bands}"/><feFuncB type="table" tableValues="{bands}"/>
    </feComponentTransfer>
    <feTurbulence type="fractalNoise" baseFrequency="0.006 0.35" numOctaves="2" seed="{seed + 5}" result="fib"/>
    <feColorMatrix in="fib" type="matrix" values="0.35 0 0 0 0.62  0.35 0 0 0 0.62  0.35 0 0 0 0.62  0 0 0 0 1" result="fibg"/>
    <feBlend in="rings" in2="fibg" mode="multiply" result="mix"/>
    <feComponentTransfer in="mix" result="col">
      <feFuncR type="linear" slope="{(r1_ - r0) * 2.2:.3f}" intercept="{r0:.3f}"/>
      <feFuncG type="linear" slope="{(g1 - g0) * 2.2:.3f}" intercept="{g0:.3f}"/>
      <feFuncB type="linear" slope="{(b1 - b0) * 2.2:.3f}" intercept="{b0:.3f}"/>
    </feComponentTransfer>
    <feGaussianBlur in="SourceAlpha" stdDeviation="{bevel}" result="bump"/>
    <feDiffuseLighting in="bump" surfaceScale="{scale}" diffuseConstant="1.05" lighting-color="#fff4e0" result="light">
      <feDistantLight azimuth="235" elevation="52"/>
    </feDiffuseLighting>
    <feSpecularLighting in="bump" surfaceScale="{scale}" specularConstant="0.35" specularExponent="18" lighting-color="#fff6e6" result="spec">
      <feDistantLight azimuth="235" elevation="52"/>
    </feSpecularLighting>
    <feComposite in="col" in2="light" operator="arithmetic" k1="1.25" k2="0" k3="0" k4="0" result="lit"/>
    <feComposite in="spec" in2="SourceAlpha" operator="in" result="specIn"/>
    <feComposite in="lit" in2="specIn" operator="arithmetic" k1="0" k2="1" k3="0.55" k4="0" result="all"/>
    <feComposite in="all" in2="SourceAlpha" operator="in"/>
  </filter>'''

# --- nails: a couple per letter, placed inside the glyph near top/bottom ---
random.seed(11)
nails = ""
for ch, d, M, P in r1.items:
    from shapely.affinity import affine_transform
    poly = affine_transform(P, [M[0, 0], M[0, 1], M[1, 0], M[1, 1], M[0, 2], M[1, 2]])
    bx0, by0, bx1, by1 = poly.bounds
    for fy in (0.16, 0.84):
        for _ in range(40):
            x = random.uniform(bx0 + 18, bx1 - 18); y = by0 + (by1 - by0) * fy + random.uniform(-6, 6)
            from shapely.geometry import Point
            if poly.buffer(-16).contains(Point(x, y)):
                nails += f'<g transform="translate({x:.1f},{y:.1f})"><circle r="9" fill="#3a3330"/><circle r="7" fill="url(#nail)"/><path d="M-4,-1 L4,1" stroke="#2a2422" stroke-width="1.6"/></g>'
                break

# --- mandarin on top of the A ---
A = [it for it in r1.items if it[0] == "A"][0]
from shapely.affinity import affine_transform
pa = affine_transform(A[3], [A[2][0, 0], A[2][0, 1], A[2][1, 0], A[2][1, 1], A[2][0, 2], A[2][1, 2]])
ax0, ay0, ax1, ay1 = pa.bounds
mx, my, mr = (ax0 + ax1) / 2 + 6, ay0 - 30, 40
mandarin = f'''
  <g>
    <ellipse cx="{mx + 6:.1f}" cy="{my + mr - 4:.1f}" rx="{mr * 0.9:.1f}" ry="8" fill="#000" opacity="0.25"/>
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr + 7}" fill="{INK}"/>
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr}" fill="url(#orange)" filter="url(#peel)"/>
    <circle cx="{mx - 13:.1f}" cy="{my - 14:.1f}" r="9" fill="#fff" opacity="0.45"/>
    <path d="M{mx + 2:.1f},{my - mr + 2:.1f} c6,-16 26,-22 40,-14 c-8,14 -26,20 -40,14z" fill="#3fa65a" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M{mx + 4:.1f},{my - mr + 1:.1f} l-4,-10" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
  </g>'''

# --- the knot (O of ODYSSEY) ---
knot = f'''
  <g transform="translate({kx:.1f},{ky:.1f}) rotate(-8)">
    <ellipse rx="{kn / 2:.1f}" ry="{kn / 2 * 0.86:.1f}" fill="#4a2410"/>
    {''.join(f'<ellipse rx="{kn / 2 * s:.1f}" ry="{kn / 2 * 0.86 * s:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>' for s, c, w in [(0.92, "#2a1206", 6), (0.74, "#7a3e18", 5), (0.56, "#2a1206", 5), (0.4, "#8a4a1f", 4), (0.24, "#2a1206", 6)])}
    <ellipse rx="{kn / 2 * 0.12:.1f}" ry="{kn / 2 * 0.1:.1f}" fill="#160803"/>
    <path d="M{kn * 0.18:.1f},{-kn * 0.06:.1f} l{kn * 0.3:.1f},{-kn * 0.04:.1f}" stroke="#160803" stroke-width="3" stroke-linecap="round"/>
  </g>'''

ext = "".join(f'<g transform="translate({k * 0.4:.1f},{k})">{p1}</g>' for k in range(2, 26, 2))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">
<defs>
  {wood_filter("woodA", "0.0022 0.045", 7, (0.26, 0.13, 0.05), (0.70, 0.43, 0.20))}
  {wood_filter("woodB", "0.003 0.06", 19, (0.20, 0.09, 0.03), (0.52, 0.30, 0.13), bevel=4, scale=4)}
  <filter id="burn" x="-5%" y="-5%" width="110%" height="110%">
    <feGaussianBlur stdDeviation="0.8" result="b"/>
    <feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d"/><feGaussianBlur in="d" stdDeviation="3" result="halo"/>
    <feFlood flood-color="#5a2a0e" flood-opacity="0.7"/><feComposite in2="halo" operator="in" result="scorch"/>
    <feMerge><feMergeNode in="scorch"/><feMergeNode in="b"/></feMerge>
  </filter>
  <filter id="peel"><feTurbulence type="fractalNoise" baseFrequency="0.35" numOctaves="2" seed="3"/>
    <feDisplacementMap in="SourceGraphic" scale="1.5"/></filter>
  <radialGradient id="nail" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#e4e0da"/><stop offset="0.55" stop-color="#8d8780"/><stop offset="1" stop-color="#4a4440"/></radialGradient>
  <radialGradient id="orange" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#ffb347"/><stop offset="0.55" stop-color="#ff7a12"/><stop offset="1" stop-color="#c94a00"/></radialGradient>
</defs>
<!-- keyline -->
<g fill="{CREAM}" stroke="{CREAM}" stroke-width="54" stroke-linejoin="round">{p1}<g transform="translate(10,24)">{p1}</g>
  <path d="{plank}" transform="rotate(-2 850 {py + ph / 2:.0f})"/><path d="{plank}" transform="translate(6,16) rotate(-2 850 {py + ph / 2:.0f})"/>
  <circle cx="{mx:.1f}" cy="{my:.1f}" r="{mr + 10}"/></g>
<!-- ODYSSEY plank, tucked under -->
<g transform="rotate(-2 850 {py + ph / 2:.0f})">
  <path d="{plank}" transform="translate(6,16)" fill="{INK}"/>
  <path d="{plank}" fill="{INK}" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>
  <path d="{plank}" fill="#000" filter="url(#woodB)"/>
  <g fill="#2a1206" filter="url(#burn)">{dys}</g>
  {knot}
  <g><circle cx="{px + 30:.1f}" cy="{py + ph / 2:.1f}" r="9" fill="#3a3330"/><circle cx="{px + 30:.1f}" cy="{py + ph / 2:.1f}" r="7" fill="url(#nail)"/>
     <circle cx="{px + pw - 30:.1f}" cy="{py + ph / 2:.1f}" r="9" fill="#3a3330"/><circle cx="{px + pw - 30:.1f}" cy="{py + ph / 2:.1f}" r="7" fill="url(#nail)"/></g>
</g>
<!-- CAPYVERSE: one plank, continuous grain -->
<g fill="{INK}" stroke="{INK}" stroke-width="22" stroke-linejoin="round">{ext}{p1}</g>
<g fill="#000" filter="url(#woodA)">{p1}</g>
{nails}
{mandarin}
</svg>'''
open("logo.svg", "w").write(svg)
render("/home/user/capyverse-claude/work/logo-code/logo.svg", "/home/user/capyverse-claude/work/logo-code/logo.png", 1700)
print("ok", round(x0), round(y0), round(x1), round(y1))
