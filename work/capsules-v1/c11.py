from compose import *
# HERO BURST — Crab Champions energy: one giant Cappy firing popcorn out of the brand sunburst.
c = Comp("plates_used/01_sunburst_nbp_1.jpg", focus=(0.5, 0.35))
c.speed_lines(1700, 400, n=80, inner=0.3, color=(255, 250, 225), opacity=0.16, width=10, seed=31)
T = dict(length=260, color=(255, 250, 225), opacity=0.25, angle=195)
moody(c, 90, 840, 0.62, trail=dict(T, length=160))
axie(c, 470, 1020, 0.12, trail=dict(T, length=160))
jim(c, 330, 690, 0.85, trail=dict(T, length=140))
cappy(c, 820, 330, 1.45, trail=dict(T, length=420))
c.logo(560, 340, 960, glow=(255, 250, 220))
c.grade(contrast=1.05, sat=1.07, vignette=0.38)
c.save("11_hero_burst", "out")
