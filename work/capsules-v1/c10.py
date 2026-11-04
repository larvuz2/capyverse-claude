from compose import *
# DISCO INFERNO — Moody gets the spotlight. Lasers, rainbow floor, a disco ball the size of a planet.
c = Comp("plates_used/up_10_disco_gpt_0_0.jpg", focus=(0.5, 0.5))
c.glow(1500, 900, 1000, (255, 60, 220), 0.25)
L1 = dict(color=(255, 120, 230), dir=(1, -1), width=8, strength=0.9)
L2 = dict(color=(120, 255, 170), dir=(-1, -1), width=6, strength=0.6)
T = dict(length=360, color=(255, 170, 240), opacity=0.32, angle=195)
c.place("cappy", 40, 820, scale=0.62, rim=L1, trail=dict(T, length=220), flames=True)
c.place("jim", 1800, 300, scale=1.0, rim=L2, trail=dict(T, length=200), flames=True)
c.place("axie", 1900, 720, scale=0.17, rim=L2, trail=dict(T, length=220), flames=True)
S = 2.35
mx, my = 760, 520
c.place("moody", mx, my, scale=S, rim=L1, trail=dict(T, length=420), flames=True,
        shadow=dict(dx=40, dy=260, blur=50, opacity=0.35, squash=0.25))
disco_flares(c, *anchor("moody", "moody_disco", mx, my, S), S * 0.8, seed=8)
confetti(c, *anchor("jim", "jim_bell", 1800, 300, 1.0), 0.9, angle=5, n=40, dist=260)
c.logo(600, 270, 900, glow=(255, 150, 240))
c.grade(contrast=1.07, sat=1.12, vignette=0.42, bloom=0.3)
c.save("10_disco_inferno", "out")
