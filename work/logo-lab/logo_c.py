"""Direction C — CAPY PLANET.

An emblem + wordmark system (Untitled Goose Game / Content Warning logic): a mark that works alone at
16-64 px (favicon, Discord, small capsule), plus a wordmark for the big spaces.
- The mark: Cappy's head drawn as a planet ("Capy-verse"): a round capybara profile with a jetpack-flame
  orbit ring crossing in front of the snout and behind the head.
- The wordmark: Chango (very wide, chunky, slightly goofy), tightened and re-spaced by hand, two lines.
Palette: space navy, Cappy orange, popcorn cream, thruster cyan.
"""
from svglogo import *

NAVY = "#1b1440"; ORANGE = "#f28a22"; ORANGE_D = "#c4601a"; CREAM = "#fff3dc"; CYAN = "#3fd4ff"; BROWN = "#7a3a16"


def mark(cx, cy, R, outline=12):
    """Capybara-head planet. Built in a 400x400 unit box centred on 200,200, scaled to radius R."""
    s = R / 170
    head = ("M58 252 C40 205 50 145 98 118 C118 106 140 100 168 98 L300 96 C336 96 356 120 356 156 "
            "L356 206 C356 236 338 252 306 254 L210 262 C160 292 98 292 58 252 Z")
    ear = "M150 104 C140 70 172 56 190 76 C198 86 194 98 186 104 Z"
    ear_in = "M158 98 C152 80 170 70 182 82 C186 88 183 96 179 99 Z"
    nostril = '<ellipse cx="342" cy="150" rx="7" ry="10" transform="rotate(18 342 150)" fill="#3a1608"/>'
    eye = ('<circle cx="238" cy="140" r="17" fill="#fff"/><circle cx="243" cy="142" r="11" fill="#3a1608"/>'
           '<circle cx="239" cy="137" r="4" fill="#fff"/>')
    brow = '<path d="M214 114 Q238 104 262 114" fill="none" stroke="#3a1608" stroke-width="7" stroke-linecap="round"/>'
    mouth = '<path d="M318 236 Q332 244 346 234" fill="none" stroke="#3a1608" stroke-width="6" stroke-linecap="round"/>'
    cheek = '<ellipse cx="280" cy="198" rx="26" ry="16" fill="#ff9d6b" opacity="0.55"/>'
    # orbit ring: an ellipse; back half drawn before the head, front half after
    ring = lambda part: (f'<path d="{"M18 250 A192 56 -12 0 1 382 168" if part == "back" else "M382 168 A192 56 -12 0 1 18 250"}" '
                         f'fill="none" stroke="{{c}}" stroke-width="{{w}}" stroke-linecap="round"/>')
    # planet disc behind the head
    disc = f'<circle cx="200" cy="200" r="170" fill="{NAVY}"/><circle cx="200" cy="200" r="170" fill="url(#planetGlow)"/>'
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/>' for x, y, r in [(90, 90, 4), (300, 300, 5), (330, 70, 3), (70, 180, 3), (250, 330, 3)])
    body = f'''
    <g transform="translate({cx - 200 * s},{cy - 200 * s}) scale({s})">
      <circle cx="200" cy="200" r="{170 + outline}" fill="{CREAM}"/>
      {disc}{stars}
      {ring("back").replace("{c}", NAVY).replace("{w}", "34")}
      {ring("back").replace("{c}", CYAN).replace("{w}", "18")}
      <g stroke="{NAVY}" stroke-width="{outline * 1.4}" stroke-linejoin="round"><path d="{head}"/><path d="{ear}"/></g>
      <path d="{ear}" fill="{ORANGE_D}"/><path d="{ear_in}" fill="{BROWN}"/>
      <path d="{head}" fill="url(#fur)"/>
      <path d="M90 140 C120 112 170 106 230 106" fill="none" stroke="#ffd09a" stroke-width="10" stroke-linecap="round" opacity="0.8"/>
      {cheek}{eye}{brow}{nostril}{mouth}
      {ring("front").replace("{c}", NAVY).replace("{w}", "34")}
      {ring("front").replace("{c}", CYAN).replace("{w}", "18")}
      <path d="M394 160 L416 142 M398 176 L424 174" stroke="{CYAN}" stroke-width="8" stroke-linecap="round"/>
    </g>'''
    return body


DEFS = f'''<defs>
  <radialGradient id="planetGlow" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#5a3fb0" stop-opacity="0.9"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></radialGradient>
  <linearGradient id="fur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7a043"/><stop offset="1" stop-color="{ORANGE_D}"/></linearGradient>
  <linearGradient id="wm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb347"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
</defs>'''

F = Font("Chango")
gl, w = F.word("CAPYVERSE", 150, tracking=-0.045)
gl2, w2 = F.word("ODYSSEY", 86, tracking=0.12)


def wordmark(x0, y0, scale=1.0):
    k = scale
    top = "".join(f'<path d="{d}" transform="translate({x0 + x * k},{y0}) scale({k})"/>' for _, d, x, _, _ in gl)
    bx = x0 + (w - w2) * k / 2
    bot = "".join(f'<path d="{d}" transform="translate({bx + x * k},{y0 + 112 * k}) scale({k})"/>' for _, d, x, _, _ in gl2)
    rule_y = y0 + 64 * k
    return f'''
    <g stroke="{NAVY}" stroke-width="{22 * k}" stroke-linejoin="round" fill="{NAVY}">{top}{bot}</g>
    <g fill="url(#wm)">{top}</g><g fill="{CREAM}">{bot}</g>
    <g stroke="{CYAN}" stroke-width="{9 * k}" stroke-linecap="round">
      <line x1="{x0}" y1="{rule_y}" x2="{bx - 26 * k}" y2="{rule_y}"/><line x1="{bx + w2 * k + 26 * k}" y1="{rule_y}" x2="{x0 + w * k}" y2="{rule_y}"/>
    </g>'''


def lockup_horizontal():
    W_, H_ = 1900, 520
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}">{DEFS}
    {mark(260, 260, 200)}
    {wordmark(520, 240, 1.0)}
    </svg>'''


def lockup_stacked():
    W_, H_ = 1400, 960
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}">{DEFS}
    {mark(700, 285, 245)}
    {wordmark((W_ - w * 1.0) / 2, 700, 1.0)}
    </svg>'''


def wordmark_only():
    W_, H_ = 1400, 420
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_} {H_}">{DEFS}
    {wordmark((W_ - w * 1.0) / 2, 210, 1.0)}
    </svg>'''


def icon():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{DEFS}{mark(256, 256, 215)}</svg>'''


if __name__ == "__main__":
    for name, fn, wpx in (("logo_c_word", wordmark_only, 1400), ("logo_c", lockup_horizontal, 1900), ("logo_c_stacked", lockup_stacked, 1400), ("logo_c_icon", icon, 512)):
        open(f"out/{name}.svg", "w").write(fn()); render(f"out/{name}.svg", f"out/{name}.png", wpx)
