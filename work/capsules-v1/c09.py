from compose import *
# COMIC VERSUS — the whole pitch in one read: wholesome crew vs. one very jealous cat.
yy, xx = np.mgrid[0:H, 0:W]
# diagonal split line from (1420, 0) to (1040, H)
def side(x, y): return (x - (1420 - 380 * y / H))
left = Image.new("RGBA", (W, H))
L = halftone((W, H), 26, (255, 140, 30), (255, 205, 40), lambda x, y: np.clip(0.15 + 0.9 * (np.hypot(x - 300, y - 1300) / 1900), 0, 1))
R = halftone((W, H), 26, (120, 20, 120), (215, 40, 120), lambda x, y: np.clip(0.15 + 0.9 * (np.hypot(x - 2300, y - 200) / 1900), 0, 1))
mask = Image.fromarray(((side(xx, yy) < 0) * 255).astype(np.uint8))
plate = Image.composite(L, R, mask)
d = ImageDraw.Draw(plate)
# jagged lightning seam
pts = []
for i in range(13):
    t = i / 12; x = 1420 - 380 * t; y = H * t
    pts.append((x + (40 if i % 2 else -40), y))
d.line(pts, fill=(20, 10, 30, 255), width=64, joint="curve")
d.line(pts, fill=(255, 255, 255, 255), width=34, joint="curve")
c = Comp(plate)
c.speed_lines(300, 1100, n=60, inner=0.3, color=(255, 255, 255), opacity=0.35, width=10, seed=21, sector=(250, 360))
INK = dict(color=(255, 255, 255), dir=(1, -1), width=8, strength=1.0)
INKR = dict(INK, dir=(-1, -1))
# villains
c.place("ophelia_pins", W - 613 * 1.05, H - 1216 * 1.05, scale=1.05, rim=INKR, match=0.05, wrap=0)
c.place("worm_bandits", 1380, H - 659 * 0.95, scale=0.95, rim=INKR, match=0.05, wrap=0)
c.place("golfer", 1700, H - 544 * 0.9, scale=0.9, rim=INKR, match=0.05, wrap=0)
# heroes
T = dict(length=280, color=(255, 255, 255), opacity=0.4, angle=200)
c.place("jim", 160, 110, scale=1.1, rim=INK, trail=dict(T, length=180), flames=True, match=0.05, wrap=0)
c.place("moody", 40, 330, scale=1.0, rim=INK, trail=dict(T, length=200), flames=True, match=0.05, wrap=0)
c.place("axie", 760, 590, scale=0.17, rim=INK, trail=dict(T, length=200), flames=True, match=0.05, wrap=0)
c.place("cappy", 10, 620, scale=0.96, rim=INK, trail=T, flames=True, match=0.05, wrap=0)
disco_flares(c, *anchor("moody", "moody_disco", 40, 330, 1.0), 1.0)
confetti(c, *anchor("jim", "jim_bell", 160, 110, 1.1), 1.0, angle=0, n=55, dist=320)
# VS badge
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf", 300)
badge = Image.new("RGBA", (700, 520), (0, 0, 0, 0)); bd = ImageDraw.Draw(badge)
star = [(350 + math.cos(math.radians(a)) * (300 if k % 2 == 0 else 190), 260 + math.sin(math.radians(a)) * (230 if k % 2 == 0 else 150)) for k, a in enumerate(range(0, 360, 20))]
bd.polygon(star, fill=(20, 10, 30, 255)); bd.polygon([(350 + (x - 350) * 0.88, 260 + (y - 260) * 0.88) for x, y in star], fill=(255, 235, 60, 255))
bd.text((350, 255), "VS", font=f, anchor="mm", fill=(230, 30, 60, 255), stroke_width=14, stroke_fill=(20, 10, 30, 255))
badge = badge.rotate(-8, Image.BICUBIC, expand=True).resize((560, 430), Image.LANCZOS)
c.canvas.alpha_composite(badge, (1232 - 280 - 20, 760))
c.logo(1232, 300, 900, shadow=0.7)
c.grade(contrast=1.05, sat=1.05, vignette=0.25)
c.save("09_comic_versus", "out")
