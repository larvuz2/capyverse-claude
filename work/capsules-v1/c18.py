from compose import *
import shaders
# NIGHT RUN (shader) — pixel art, Risk of Rain Returns style: the same scene as a 16-bit night raid.
c = Comp("plates_used/v2_night_canyon_nbp_0.jpg", focus=(0.5, 0.5))
MOON = dict(color=(170, 220, 255), dir=(-1, -1), width=8, strength=0.9)
c.place("worm_bandits", 1720, H - 659 * 1.2 + 30, scale=1.2, rim=MOON, match=0.3, bright=0.85,
        shadow=dict(dy=10, blur=20, opacity=0.4, squash=0.12))
c.place("golfer", 2180, H - 544 * 0.8 + 10, scale=0.8, rim=MOON, match=0.3, bright=0.85)
T = dict(length=300, color=(150, 210, 255), opacity=0.3, angle=195)
HR = dict(color=(170, 220, 255), dir=(-1, -1), width=7, strength=0.85)
moody(c, 1150, 420, 0.62, rim=HR, trail=T, match=0.2)
jim(c, 1350, 660, 0.82, rim=HR, trail=T, match=0.2)
axie(c, 1180, 900, 0.12, rim=HR, trail=T, match=0.2)
cappy(c, 60, 580, 1.35, rim=HR, trail=dict(T, length=380), match=0.2)
c.grade(contrast=1.1, sat=1.12, vignette=0.35, bloom=0.3)
c.canvas = shaders.pixel(c.canvas, width=320, colors=48)
# logo stays readable: pixelated at a finer grid than the scene
lg = load("layers/L_logo.png"); w0 = 880; h0 = round(lg.height * w0 / lg.width)
lg = lg.resize((w0 // 3, h0 // 3), Image.BOX).resize((w0, h0), Image.NEAREST)
lg.save("/tmp/_logo_px.png")
c.logo(620, 250, 880, path="/tmp/_logo_px.png", shadow=0.6)
c.save("18_night_run_pixel", "out")
