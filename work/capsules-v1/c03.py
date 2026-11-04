from compose import *
# CAPYVERSE PLANET — the squad skims low orbit over the worlds of the run.
c = Comp("plates_used/up_03_planet_gpt_0_0.jpg", focus=(0.5, 0.55))
RIM = dict(color=(150, 230, 255), dir=(0, 1), width=7, strength=0.9)   # planet glow from below
RIM2 = dict(color=(255, 230, 255), dir=(1, -1), width=5, strength=0.5)
T = dict(length=420, color=(140, 220, 255), opacity=0.32, angle=200)
c.place("jim", 140, 300, scale=1.05, rim=RIM, trail=dict(T, length=260), flames=True)
c.place("moody", 1700, 560, scale=0.95, rim=RIM, trail=dict(T, length=280), flames=True)
c.place("axie", 160, 720, scale=0.2, rim=RIM, trail=dict(T, length=300), flames=True)
c.place("cappy", 560, 520, scale=1.0, rim=RIM, trail=T, flames=True)
disco_flares(c, *anchor("moody", "moody_disco", 1700, 560, 0.95), 0.95)
confetti(c, *anchor("jim", "jim_bell", 140, 300, 1.05), 0.9, angle=15, n=45, dist=300)
c.logo(1232, 250, 900, glow=(160, 200, 255))
c.grade(contrast=1.06, sat=1.1, vignette=0.4, bloom=0.2)
c.save("03_capyverse_planet", "out")
