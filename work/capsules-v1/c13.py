from compose import *
# CANYON COLOSSUS — the sandworm erupts at giant scale; Cappy charges straight at it.
c = Comp("plates_used/v2_canyon_colossus_nbp_0.jpg", focus=(0.5, 0.5))
SUN = dict(color=(255, 225, 160), dir=(-1, -1), width=10, strength=0.9)
s = 2.7
c.place("worm_top", 1450 - 467 * s / 2, 1060 - 309 * s, scale=s, rim=SUN, match=0.25, bright=0.95)
c.particles(70, (1050, 750, 1900, 1150), [(200, 140, 80), (170, 110, 60), (230, 180, 120)], size=(5, 20), seed=13, glow=False)
c.glow(1450, 1000, 700, (255, 210, 150), 0.25)
T = dict(length=300, color=(255, 235, 200), opacity=0.25, angle=15)
HR = dict(color=(255, 225, 160), dir=(1, -1), width=7, strength=0.8)
moody(c, 1900, 380, 0.62, flip=True, rim=HR, trail=dict(T, length=180))
jim(c, 2080, 720, 0.85, flip=True, rim=HR, trail=dict(T, length=160))
axie(c, 1880, 930, 0.12, flip=True, rim=HR, trail=dict(T, length=180))
cappy(c, -80, 600, 1.35, trail=dict(length=380, color=(255, 235, 200), opacity=0.28, angle=195),
      shadow=dict(dx=60, dy=420, blur=45, opacity=0.25, squash=0.18))
c.logo(580, 260, 900, glow=(255, 235, 190))
c.grade(contrast=1.08, sat=1.08, vignette=0.4, warm=0.02, bloom=0.2)
c.save("13_canyon_colossus", "out")
