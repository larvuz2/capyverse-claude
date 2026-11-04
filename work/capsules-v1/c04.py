from compose import *
# DESERT RUN — the sandworm bursts out of the canyon floor; the squad strafes it at golden hour.
c = Comp("plates_used/up_04_desert_gpt_0_0.jpg", focus=(0.5, 0.6))
SUN = dict(color=(255, 215, 150), dir=(-1, -1), width=8, strength=0.85)
c.place("worm_bandits", 1560, H - 659 * 1.35 + 30, scale=1.35, rim=SUN, match=0.2,
        shadow=dict(dx=-60, dy=20, blur=25, opacity=0.4, squash=0.12))
c.place("golfer", 2150, H - 544 * 0.85 + 10, scale=0.85, rim=SUN, match=0.2,
        shadow=dict(dx=-50, dy=10, blur=20, opacity=0.4, squash=0.12))
c.particles(60, (1450, 900, 2400, 1400), [(200, 140, 80), (170, 110, 60), (230, 180, 120)], size=(4, 16), seed=9, glow=False)
HRIM = dict(color=(255, 210, 140), dir=(-1, -1), width=7, strength=0.8)
T = dict(length=360, color=(255, 230, 190), opacity=0.3, angle=195)
fly_shadow = dict(dx=40, dy=380, blur=40, opacity=0.28, squash=0.18)
c.place("moody", 1080, 380, scale=0.95, rim=HRIM, trail=dict(T, length=240), flames=True)
c.place("jim", 1260, 110, scale=1.0, rim=HRIM, trail=dict(T, length=220), flames=True)
c.place("axie", 1130, 820, scale=0.19, rim=HRIM, trail=dict(T, length=260), flames=True, shadow=dict(fly_shadow, dy=300))
c.place("cappy", 30, 640, scale=0.98, rim=HRIM, trail=T, flames=True)
disco_flares(c, *anchor("moody", "moody_disco", 1080, 380, 0.95), 0.95)
c.logo(600, 270, 920, glow=(255, 230, 170))
c.grade(contrast=1.08, sat=1.08, vignette=0.38, warm=0.03, bloom=0.2)
c.save("04_desert_run", "out")
