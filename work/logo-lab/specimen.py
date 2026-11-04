from svglogo import *
fonts = ["LuckiestGuy", "TitanOne", "LilitaOne", "Rubikwght900", "DelaGothicOne", "Baloo2wght800", "Chango", "BowlbyOne", "RammettoOne", "Bangers"]
rows = []
y = 0
for fn in fonts:
    F = Font(fn); gl, w = F.word("CAPYVERSE", 120)
    gl2, w2 = F.word("ODYSSEY", 60, 0.08)
    paths = "".join(f'<path d="{d}" transform="translate({x+40},{y+150})"/>' for _, d, x, _, _ in gl)
    paths += "".join(f'<path d="{d}" transform="translate({x+40+w+40},{y+150})" fill="#ffb52e"/>' for _, d, x, _, _ in gl2)
    rows.append(f'<g fill="#fff">{paths}</g><text x="1500" y="{y+150}" fill="#aaa" font-size="22" font-family="sans-serif">{fn}</text>')
    y += 170
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 {y+40}"><rect width="1800" height="{y+40}" fill="#2a2230"/>{"".join(rows)}</svg>'
open("specimen.svg", "w").write(svg); render("specimen.svg", "specimen.png", 1800)
