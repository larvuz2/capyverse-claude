from compose import *
import shaders
# BLEACHED SUN (shader) — Risk of Rain 2 painted key art: pale haze, a huge red sun, Cappy as the one bright shape.
c = Comp("plates_used/v2_pale_sun_nbp_1.jpg", focus=(0.5, 0.5))
FOG = dict(color=(255, 245, 235), dir=(1, -1), width=9, strength=0.8)
c.place("worm_top", 2050, 760, scale=1.1, bright=1.25, sat=0.4, opacity=0.55, match=0.5)
T = dict(length=280, color=(255, 240, 230), opacity=0.25, angle=195)
moody(c, 110, 560, 0.5, rim=FOG, trail=T, bright=1.1, sat=0.75, match=0.35)
jim(c, 1000, 330, 0.7, rim=FOG, trail=T, bright=1.1, sat=0.75, match=0.35, confetti_n=0)
axie(c, 300, 600, 0.1, rim=FOG, trail=T, bright=1.1, sat=0.75, match=0.35)
cappy(c, 520, 560, 1.38, rim=dict(color=(255, 150, 120), dir=(1, -1), width=10, strength=0.9), trail=dict(T, length=360),
      match=0.15, shadow=dict(dx=60, dy=420, blur=55, opacity=0.18, squash=0.18))
c.canvas = shaders.painted(c.canvas, wash_amt=0.12)
c.logo(560, 250, 860, shadow=0.35)
c.grade(contrast=1.03, sat=1.02, vignette=0.2)
c.save("20_bleached_sun_painted", "out")
