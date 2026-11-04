from compose import *
# STRIKE! — Cappy is the bowling ball. The squad bombs down the cosmic lane at a full rack of clown pins.
c = Comp("plates_used/06_strike_nbp_0.jpg", focus=(0.5, 0.5))
vx, vy = 1232, 700   # rack position near the lane's vanishing area
rack = [(0, 0)] + [(i, r) for r in range(1, 4) for i in range(r + 1)]
rows = {0: [(0, 0)], 1: [(-0.5, 1), (0.5, 1)], 2: [(-1, 2), (0, 2), (1, 2)], 3: [(-1.5, 3), (-0.5, 3), (0.5, 3), (1.5, 3)]}
PINRIM = dict(color=(255, 200, 120), dir=(0, 1), width=5, strength=0.6)
for r in (3, 2, 1, 0):  # back row first
    for dx, _ in rows[r]:
        sc = 0.13 - r * 0.01
        x = vx + dx * 96 - 635 * sc / 2
        yb = vy + 130 - r * 16
        c.place("pin", x, yb - 1553 * sc, scale=sc, rim=PINRIM, match=0.15, shadow=dict(dy=6, blur=8, opacity=0.45, squash=0.08))
c.speed_lines(vx, vy, n=110, inner=0.28, color=(255, 230, 200), opacity=0.22, width=9, seed=7)
RIM = dict(color=(255, 210, 150), dir=(0, 1), width=7, strength=0.8)
T = dict(length=380, color=(255, 220, 180), opacity=0.32, angle=210)
c.place("jim", 120, 230, scale=1.0, rim=RIM, trail=dict(T, length=220), flames=True)
c.place("moody", 1750, 330, scale=0.95, flip=True, rim=RIM, trail=dict(T, angle=-30, length=240), flames=True)
c.place("axie", 1650, 700, scale=0.19, flip=True, rim=RIM, trail=dict(T, angle=-30, length=260), flames=True)
c.place("cappy", 40, 680, scale=0.95, rim=RIM, trail=T, flames=True, shadow=dict(dx=60, dy=420, blur=40, opacity=0.3, squash=0.15))
disco_flares(c, *anchor("moody", "moody_disco", 1750, 330, 0.95, flip=True, lw=432), 0.95)
confetti(c, *anchor("jim", "jim_bell", 120, 230, 1.0), 0.9, angle=-5, n=45, dist=300)
c.logo(1232, 250, 860, glow=(255, 200, 140))
c.grade(contrast=1.07, sat=1.1, vignette=0.42, bloom=0.25)
c.save("06_strike", "out")
