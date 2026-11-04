from compose import *
import shaders
# SATURDAY MORNING (shader) — the real render, cel-shaded and inked like a cartoon key frame.
c = Comp("plates_used/01_sunburst_gpt_0.jpg", focus=(0.5, 0.3))
RR = dict(color=(255, 238, 190), dir=(-1, -1), width=7, strength=0.7)
c.place("worm_bandits", 1700, H - 659 * 1.05 + 20, scale=1.05, rim=RR)
for x in np.linspace(2000, 2400, 4):
    sc = 0.15; c.place("pin", x - 635 * sc / 2, H - 1553 * sc + 30, scale=sc, rim=RR)
T = dict(length=240, color=(255, 250, 225), opacity=0.25, angle=195)
moody(c, 60, 640, 0.6, trail=T)
jim(c, 120, 980, 0.8, trail=T)
axie(c, 1560, 140, 0.12, trail=T)
cappy(c, 330, 470, 1.38, trail=dict(T, length=360))
c.grade(contrast=1.08, sat=1.15, vignette=0.3)
c.canvas = shaders.ink_cel(c.canvas, colors=20, line=3)
c.canvas = ImageEnhance.Color(c.canvas.convert("RGB")).enhance(1.25).convert("RGBA")
c.logo(600, 250, 860, shadow=0.7)
c.save("17_saturday_morning_cel", "out")
