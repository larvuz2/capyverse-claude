from compose import *
# ATTENTION KINGDOM — Ophelia owns the wall of screens; the squad flies in to switch her off.
c = Comp("plates_used/up_02_attention_kingdom_gpt_0_0.jpg", focus=(0.5, 0.5))
c.grade(contrast=1.0, sat=1.0, vignette=0.0)
c.glow(2050, 520, 1300, (255, 60, 140), 0.28)
S = 1.18
ox, oy = W - 613 * S + 20, H - 930 * S + 40
c.place("ophelia_head", ox, oy, scale=S, rim=dict(color=(255, 120, 190), dir=(-1, -1), width=9, strength=0.9), match=0.1)
for ex, ey in ((165, 520), (453, 496)):
    c.glow(ox + ex * S, oy + ey * S, 120, (255, 30, 40), 0.75)
RIM = dict(color=(190, 225, 255), dir=(1, -1), width=7, strength=0.9)
T = dict(length=320, color=(150, 200, 255), opacity=0.3, angle=192)
c.place("jim", 1210, 430, scale=1.0, rim=RIM, trail=dict(T, length=200), flames=True)
c.place("axie", 900, 690, scale=0.17, rim=RIM, trail=dict(T, length=220), flames=True)
c.place("moody", 1000, 920, scale=0.95, rim=RIM, trail=dict(T, length=220), flames=True)
c.place("cappy", -40, 560, scale=0.98, rim=RIM, trail=T, flames=True)
disco_flares(c, *anchor("moody", "moody_disco", 1000, 920, 0.95), 0.95)
c.logo(560, 290, 940, glow=(120, 170, 255))
c.grade(contrast=1.07, sat=1.1, vignette=0.45, bloom=0.25)
c.save("02_attention_kingdom", "out")
