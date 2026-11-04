from compose import *
# PORTAL LOBBY — the run starts: the squad blasts out of the lobby portal in every direction.
c = Comp("plates_used/up_07_portal_gpt_0_0.jpg", focus=(0.5, 0.5))
px, py = 1232, 620
c.glow(px, py, 900, (120, 255, 210), 0.45)
c.speed_lines(px, py, n=120, inner=0.12, color=(190, 255, 235), opacity=0.25, width=8, seed=12)
RIM = dict(color=(170, 255, 225), dir=(1, -1), width=8, strength=1.0)
RIMF = dict(RIM, dir=(-1, -1))
T = dict(length=420, color=(160, 255, 220), opacity=0.35, angle=180)
c.place("jim", 1720, 420, scale=1.05, rim=RIMF, trail=dict(T, angle=200, length=280), flames=True)
c.place("axie", 300, 330, scale=0.19, flip=True, rim=RIM, trail=dict(T, angle=-20, length=300), flames=True)
c.place("moody", 1700, 760, scale=1.15, rim=RIMF, trail=dict(T, angle=170, length=280), flames=True)
c.place("cappy", 60, 600, scale=1.08, flip=True, rim=RIM, trail=dict(T, angle=-10), flames=True)
disco_flares(c, *anchor("moody", "moody_disco", 1700, 760, 1.15), 1.15)
confetti(c, *anchor("jim", "jim_bell", 1720, 420, 1.05), 0.9, angle=10, n=40, dist=260)
c.logo(1232, 300, 900, glow=(170, 255, 220))
c.grade(contrast=1.06, sat=1.1, vignette=0.45, bloom=0.3)
c.save("07_portal_lobby", "out")
