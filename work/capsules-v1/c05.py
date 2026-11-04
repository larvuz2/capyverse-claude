from compose import *
# CARNIVAL HORDE — crowded: Ophelia rises over the night carnival like a moon, her horde floods the plaza.
c = Comp("plates_used/05_carnival_nbp_0.jpg", focus=(0.5, 0.5))
S = 1.3
ox, oy = W - 613 * S + 10, -40
c.place("ophelia_head", ox, oy, scale=S, bright=0.9, match=0.2,
        rim=dict(color=(140, 255, 160), dir=(-1, -1), width=10, strength=0.8))
for ex, ey in ((165, 520), (453, 496)):
    c.glow(ox + ex * S, oy + ey * S, 140, (255, 30, 40), 0.8)
NEON = dict(color=(160, 255, 170), dir=(0, -1), width=6, strength=0.7)
# horde: pins + bandit gangs receding into the plaza (back to front)
rnd = np.random.default_rng(11)
spots = []
for row, (yb, sc, n) in enumerate([(1030, 0.14, 9), (1110, 0.18, 8), (1210, 0.23, 7), (1330, 0.29, 6)]):
    xs = np.linspace(80, W - 80, n) + rnd.uniform(-60, 60, n)
    for x in xs: spots.append((row, x, yb, sc))
for row, x, yb, sc in spots:
    if x < 1250 and row >= 2: continue  # keep a lane open under the logo
    if rnd.random() < 0.7:
        c.place("pin", x - 635 * sc / 2, yb - 1553 * sc, scale=sc, rim=NEON, match=0.2,
                shadow=dict(dy=8, blur=10, opacity=0.4, squash=0.1))
    else:
        s2 = sc * 2.0
        c.place("worm_bandits", x - 467 * s2 / 2, yb - 659 * s2, scale=s2, rim=NEON, match=0.2,
                shadow=dict(dy=8, blur=12, opacity=0.4, squash=0.1))
c.place("golfer", 1500, H - 544 * 0.95, scale=0.95, rim=NEON, match=0.15, shadow=dict(dy=10, blur=16, opacity=0.4, squash=0.1))
RIM = dict(color=(255, 230, 160), dir=(1, -1), width=7, strength=0.85)
T = dict(length=300, color=(255, 240, 200), opacity=0.28, angle=195)
c.place("jim", 90, 300, scale=1.05, rim=RIM, trail=dict(T, length=200), flames=True)
c.place("moody", 1130, 600, scale=0.85, rim=RIM, trail=dict(T, length=200), flames=True)
c.place("axie", 980, 790, scale=0.17, rim=RIM, trail=dict(T, length=220), flames=True)
c.place("cappy", -40, 640, scale=0.92, rim=RIM, trail=T, flames=True)
disco_flares(c, *anchor("moody", "moody_disco", 1130, 600, 0.85), 0.85)
confetti(c, *anchor("jim", "jim_bell", 90, 300, 1.05), 0.9, angle=0, n=50, dist=320)
c.logo(1050, 290, 900, glow=(255, 230, 150))
c.grade(contrast=1.07, sat=1.12, vignette=0.42, bloom=0.3)
c.save("05_carnival_horde", "out")
