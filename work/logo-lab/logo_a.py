"""Direction A — POPCORN POP.

Party-game wordmark (Fall Guys / Stumble Guys / Brotato family) made Capyverse-specific:
- Titan One outlines, every letter re-set by hand on a bouncing baseline with its own tilt
- capybara ears + eye grafted onto the first C, so the name starts with Cappy's head
- the O of ODYSSEY is a popcorn kernel (Cappy's ammo)
- ODYSSEY rides a red/white popcorn-bucket stripe band
- jetpack speed streaks trail behind the word (everybody gets a jetpack)
Layer stack (back to front): white sticker outline -> brown extrusion -> brown outline -> gradient fill -> shine.
"""
from svglogo import *
import math

INK = "#2a140d"      # outline / extrusion (dark capybara brown)
STICK = "#fff6e6"    # sticker outline (popcorn cream)
Y1, Y2 = "#fffaf0", "#ffc02e"   # fill gradient top/bottom
RED = "#ef3b3b"

F = Font("TitanOne"); F2 = Font("TitanOne")
SIZE = 220
gl, wtot = F.word("CAPYVERSE", SIZE, tracking=-0.02)

# hand-tuned per-letter bounce (dy px) and tilt (deg)
BOUNCE = [10, -14, 6, -18, 8, -10, 14, -8, 6]
TILT = [-7, 4, -3, 6, -4, 3, -5, 4, -2]
OX, OY = 245, 300  # word origin (baseline)


def letter_xf(i, x, b):
    cx = OX + x + (b[0] + b[2]) / 2; cy = OY + (b[1] + b[3]) / 2
    return f"translate({OX + x},{OY + BOUNCE[i]}) rotate({TILT[i]},{cx - OX - x},{cy - OY})"


letters = [(ch, d, letter_xf(i, x, b), x, b) for i, (ch, d, x, adv, b) in enumerate(gl)]

# --- Cappy ears + eye on the first C ---
c_ch, c_d, c_xf, c_x, c_b = letters[0]
ear_l = '<path d="M14 -136 C2 -170 30 -196 58 -178 C70 -170 70 -150 62 -140 Z"/>'
ear_r = ''
ears_fill = ear_l
inner_ears = '<path d="M26 -146 C22 -168 40 -180 52 -170 C58 -164 56 -152 50 -146 Z" fill="#7a3a16"/>'
eye = ('<ellipse cx="74" cy="-126" rx="19" ry="21" fill="#fff" stroke="#2a140d" stroke-width="5"/>'
       '<circle cx="80" cy="-124" r="12" fill="#7a3a12"/><circle cx="82" cy="-124" r="6.5" fill="#140805"/>'
       '<circle cx="76" cy="-130" r="4.5" fill="#fff"/>'
       '<path d="M52 -152 Q74 -160 96 -150" fill="none" stroke="#2a140d" stroke-width="7" stroke-linecap="round"/>'
       '<ellipse cx="128" cy="-120" rx="6" ry="8" fill="#2a140d" transform="rotate(20 128 -120)"/>')

# --- ODYSSEY on a popcorn-bucket band ---
gl2, w2 = F2.word("DYSSEY", 120, tracking=0.06)
BX, BY, BW, BH = 900 - 400, 372, 800, 156  # band box
band_rot = -3


def popcorn(cx, cy, s):
    """A popcorn kernel: an irregular ring of puffs around a core."""
    puffs = [(0, 0.05, 0.78), (-0.66, -0.12, 0.6), (0.66, -0.2, 0.62), (-0.3, -0.7, 0.58), (0.32, -0.74, 0.56),
             (-0.6, 0.5, 0.52), (0.62, 0.46, 0.55), (0.02, 0.72, 0.5)]
    return "".join(f'<circle cx="{cx + px * s:.1f}" cy="{cy + py * s:.1f}" r="{pr * s:.1f}"/>' for px, py, pr in puffs)


pc_cx, pc_cy, pc_s = 900 - (w2 + 130) / 2 + 52, BY + BH / 2 + 2, 50
pc_shape = popcorn(pc_cx, pc_cy, pc_s)
pc_butter = (f'<circle cx="{pc_cx + 0.66 * pc_s:.1f}" cy="{pc_cy - 0.2 * pc_s:.1f}" r="{0.36 * pc_s:.1f}" fill="#ffc52a"/>'
             f'<circle cx="{pc_cx - 0.6 * pc_s:.1f}" cy="{pc_cy + 0.5 * pc_s:.1f}" r="{0.3 * pc_s:.1f}" fill="#ffc52a"/>'
             f'<circle cx="{pc_cx + 0.2 * pc_s:.1f}" cy="{pc_cy + 0.25 * pc_s:.1f}" r="{0.2 * pc_s:.1f}" fill="#f2dfb4"/>'
             f'<circle cx="{pc_cx - 0.3 * pc_s:.1f}" cy="{pc_cy - 0.62 * pc_s:.1f}" r="{0.15 * pc_s:.1f}" fill="#fff"/>'
             f'<circle cx="{pc_cx - 0.05 * pc_s:.1f}" cy="{pc_cy - 0.12 * pc_s:.1f}" r="{0.12 * pc_s:.1f}" fill="#fff"/>')
ody_x0 = pc_cx + 72
ody = "".join(f'<path d="{d}" transform="translate({ody_x0 + x},{BY + BH / 2 + 44})"/>' for _, d, x, _, _ in gl2)
stripes = "".join(f'<rect x="{BX - 200 + i * 70}" y="{BY - 20}" width="34" height="{BH + 40}" transform="skewX(-18)"/>' for i in range(20))

# --- jetpack speed streaks behind the word ---
streaks = ""
for i, (y, l, w) in enumerate([(150, 150, 20), (200, 215, 24), (250, 170, 20)]):
    streaks += f'<rect x="{OX - l - 30}" y="{y}" width="{l}" height="{w}" rx="{w / 2}"/>'

word_paths = "".join(f'<path d="{d}" transform="{xf}"/>' for _, d, xf, _, _ in letters)
c_group = f'<g transform="{c_xf}">{ears_fill}</g>'

W_, H_ = 1800, 600
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}">
<defs>
  <linearGradient id="fillA" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{Y1}"/><stop offset="0.5" stop-color="#ffe9a8"/><stop offset="1" stop-color="{Y2}"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0.75"/><stop offset="0.42" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="fur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8763b"/><stop offset="1" stop-color="#8f4a1f"/></linearGradient>
  <clipPath id="pcclip">{pc_shape}</clipPath>
  <clipPath id="bandclip"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="40"/></clipPath>
</defs>
<g id="streaks" fill="{STICK}" stroke="{INK}" stroke-width="10" opacity="0.95">{streaks}</g>

<!-- 1. sticker outline (cream) around everything -->
<g fill="{STICK}" stroke="{STICK}" stroke-width="58" stroke-linejoin="round">
  {word_paths}{c_group}
  <g transform="translate(0,22)">{word_paths}</g>
  <g transform="rotate({band_rot} {BX + BW / 2} {BY + BH / 2})"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH + 18}" rx="40"/>{pc_shape}</g>
</g>
<!-- 2. extrusion -->
<g fill="{INK}" stroke="{INK}" stroke-width="22" stroke-linejoin="round">
  {"".join(f'<g transform="translate(0,{k})">{word_paths}{c_group}</g>' for k in range(2, 24, 3))}
  <g transform="rotate({band_rot} {BX + BW / 2} {BY + BH / 2}) translate(0,16)"><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="40"/></g>
</g>
<!-- 3. ODYSSEY band -->
<g transform="rotate({band_rot} {BX + BW / 2} {BY + BH / 2})">
  <rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="40" fill="#fff" stroke="{INK}" stroke-width="20"/>
  <g clip-path="url(#bandclip)" fill="{RED}">{stripes}</g>
  <rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="40" fill="none" stroke="{INK}" stroke-width="20"/>
  <g fill="#fff" stroke="{INK}" stroke-width="22" stroke-linejoin="round" paint-order="stroke">{ody}</g>
  <g fill="{INK}" stroke="{INK}" stroke-width="20" stroke-linejoin="round">{pc_shape}</g>
  <g fill="#fff4dc">{pc_shape}</g><g clip-path="url(#pcclip)">{pc_butter}</g>
</g>
<!-- 4. main word: outline, fill, shine -->
<g stroke="{INK}" stroke-width="22" stroke-linejoin="round" fill="{INK}">{c_group}{word_paths}</g>
<g transform="{c_xf}" fill="url(#fur)">{ears_fill}{inner_ears}</g>
<g fill="url(#fillA)">{word_paths}</g>
<g fill="url(#shine)">{word_paths}</g>
<g transform="{c_xf}">{eye}</g>
</svg>'''
open("out/logo_a.svg", "w").write(svg)

if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    open("out/logo_a.svg", "w").write(svg)
    render("out/logo_a.svg", "out/logo_a.png", 1600)
