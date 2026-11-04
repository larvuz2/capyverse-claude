from compose import *
import glob
# JUST CAPPY — minimal. One hero, one colour, one joke: the popcorn gatling.
yy, xx = np.mgrid[0:H, 0:W]
r = np.hypot((xx - 1750) / W, (yy - 650) / H)
base = np.array([28, 170, 168], np.float32) / 255; hi = np.array([110, 225, 210], np.float32) / 255
rgb = base + (hi - base) * np.clip(1 - r * 2.2, 0, 1)[..., None]
plate = Image.fromarray((np.dstack([rgb, np.ones((H, W))]) * 255).astype(np.uint8), "RGBA")
c = Comp(plate)
S = 1.3
cx, cy = 820, 520
gx, gy = anchor("cappy", "cappy_gatling", cx, cy, S)
# popcorn bursting out of the gatling toward the upper right
rnd = np.random.default_rng(3)
pieces = sorted(glob.glob("layers/popcorn/*.png"))
for i, p in enumerate(pieces):
    t = rnd.uniform(0.1, 1.0)
    a = math.radians(rnd.uniform(0, 62))
    d = 60 + t * 820
    x, y = gx + math.cos(a) * d, gy - math.sin(a) * d * 0.9
    sc = 0.7 + t * 1.0
    P = load(p)
    if x > W - 20 or y < -60: continue
    c.place("popcorn", x - P.width * sc / 2, y - P.height * sc / 2, scale=sc, src=P, match=0.05, wrap=0.2, rim=None)
c.glow(gx, gy, 260, (255, 240, 200), 0.8)
c.place("cappy", cx, cy, scale=S, rim=dict(color=(220, 255, 250), dir=(1, -1), width=9, strength=0.7),
        flames=True, flame_len=0.9, shadow=dict(dx=-30, dy=60, blur=50, opacity=0.25))
c.logo(600, 330, 960)
c.grade(contrast=1.04, sat=1.05, vignette=0.28)
c.save("08_just_cappy", "out")
