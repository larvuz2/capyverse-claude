from compose import *
# SHOWDOWN STACK — Roboquest-style: Cappy huge in front, Ophelia's whole crew stacked up behind him.
c = Comp("plates_used/01_sunburst_gpt_0.jpg", focus=(0.5, 0.3))
RR = dict(color=(255, 238, 190), dir=(-1, -1), width=7, strength=0.7)
S = 1.55
ox, oy = W - 613 * S + 40, -150
c.place("ophelia_head", ox, oy, scale=S, rim=RR, match=0.12)
for ex, ey in ((165, 520), (453, 496)): c.glow(ox + ex * S, oy + ey * S, 110, (255, 40, 40), 0.6)
c.place("worm_bandits", 1260, H - 659 * 1.05 + 20, scale=1.05, rim=RR, match=0.15)
c.place("golfer", 1640, H - 544 * 0.95 + 10, scale=0.95, rim=RR, match=0.15)
for i, x in enumerate(np.linspace(1880, 2380, 5)):
    sc = 0.17
    c.place("pin", x - 635 * sc / 2, H - 1553 * sc + 30, scale=sc, rim=RR, match=0.15)
T = dict(length=260, color=(255, 250, 225), opacity=0.25, angle=195)
moody(c, 1090, 70, 0.6, trail=dict(T, length=160))
axie(c, 1240, 360, 0.11, trail=dict(T, length=160))
jim(c, 30, 520, 0.8, trail=dict(T, length=140))
cappy(c, 120, 560, 1.32, trail=dict(T, length=360))
c.logo(600, 270, 900, glow=(255, 250, 220))
c.grade(contrast=1.05, sat=1.07, vignette=0.4)
c.save("12_showdown_stack", "out")
