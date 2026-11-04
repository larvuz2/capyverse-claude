from compose import *
# FACE-OFF — comic versus, one-on-one: Cappy vs. Ophelia, nose to nose.
yy, xx = np.mgrid[0:H, 0:W]
def side(x, y): return (x - (1380 - 300 * y / H))
L = halftone((W, H), 26, (255, 140, 30), (255, 205, 40), lambda x, y: np.clip(0.15 + 0.9 * (np.hypot(x - 300, y - 1300) / 1900), 0, 1))
R = halftone((W, H), 26, (90, 20, 130), (200, 40, 140), lambda x, y: np.clip(0.15 + 0.9 * (np.hypot(x - 2300, y - 200) / 1900), 0, 1))
plate = Image.composite(L, R, Image.fromarray(((side(xx, yy) < 0) * 255).astype(np.uint8)))
d = ImageDraw.Draw(plate)
pts = [(1380 - 300 * t / 12 + (40 if t % 2 else -40), H * t / 12) for t in range(13)]
d.line(pts, fill=(20, 10, 30, 255), width=64, joint="curve"); d.line(pts, fill=(255, 255, 255, 255), width=34, joint="curve")
c = Comp(plate)
c.speed_lines(200, 1000, n=50, inner=0.3, color=(255, 255, 255), opacity=0.3, width=10, seed=51, sector=(250, 360))
INKR = dict(color=(255, 255, 255), dir=(-1, -1), width=9, strength=1.0)
S = 1.62
c.place("ophelia_head", W - 613 * S + 60, H - 930 * S + 120, scale=S, rim=INKR, match=0.05, wrap=0)
INK = dict(color=(255, 255, 255), dir=(1, -1), width=9, strength=1.0)
T = dict(length=200, color=(255, 255, 255), opacity=0.4, angle=200)
moody(c, 60, 200, 0.5, rim=INK, trail=T, match=0.05, wrap=0)
jim(c, 330, 90, 0.7, rim=INK, trail=T, match=0.05, wrap=0)
axie(c, 470, 330, 0.1, rim=INK, trail=T, match=0.05, wrap=0)
cappy(c, -60, 560, 1.42, rim=INK, trail=dict(T, length=320), match=0.05, wrap=0)
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf", 300)
badge = Image.new("RGBA", (700, 520), (0, 0, 0, 0)); bd = ImageDraw.Draw(badge)
star = [(350 + math.cos(math.radians(a)) * (300 if k % 2 == 0 else 190), 260 + math.sin(math.radians(a)) * (230 if k % 2 == 0 else 150)) for k, a in enumerate(range(0, 360, 20))]
bd.polygon(star, fill=(20, 10, 30, 255)); bd.polygon([(350 + (x - 350) * 0.88, 260 + (y - 260) * 0.88) for x, y in star], fill=(255, 235, 60, 255))
bd.text((350, 255), "VS", font=f, anchor="mm", fill=(230, 30, 60, 255), stroke_width=14, stroke_fill=(20, 10, 30, 255))
badge = badge.rotate(-8, Image.BICUBIC, expand=True).resize((440, 340), Image.LANCZOS)
c.canvas.alpha_composite(badge, (1210 - 220, 1010))
c.logo(1232, 250, 860, shadow=0.7)
c.grade(contrast=1.05, sat=1.05, vignette=0.22)
c.save("16_face_off", "out")
