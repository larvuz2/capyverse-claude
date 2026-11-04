from compose import *
# COMIC COVER — issue #1 cover: Cappy smashes out of the main panel; villains wait in the side panels.
yy, xx = np.mgrid[0:H, 0:W]
bg = halftone((W, H), 30, (255, 150, 40), (255, 214, 60), lambda x, y: np.clip(0.2 + 0.8 * np.hypot(x - 800, y - 700) / 1800, 0, 1))
c = Comp(bg)
ink = (25, 15, 30, 255)
def panel(box, plate_fn, draw_fn):
    sub = Comp(plate_fn()); draw_fn(sub)
    x0, y0, x1, y1 = box
    crop = sub.canvas.crop((x0, y0, x1, y1))
    d = ImageDraw.Draw(c.canvas)
    d.rectangle([x0 - 14, y0 - 14, x1 + 14, y1 + 14], fill=ink)
    c.canvas.paste(crop, (x0, y0))
main = (50, 50, 1600, 1362)
def main_plate():
    return halftone((W, H), 22, (40, 120, 220), (90, 190, 255), lambda x, y: np.clip(0.1 + 0.9 * np.hypot(x - 700, y - 400) / 1600, 0, 1))
def main_draw(s):
    s.speed_lines(1100, 500, n=90, inner=0.18, color=(255, 255, 255), opacity=0.35, width=10, seed=41)
    T = dict(length=200, color=(255, 255, 255), opacity=0.35, angle=195)
    INK = dict(color=(255, 255, 255), dir=(1, -1), width=7, strength=1.0)
    moody(s, 130, 960, 0.6, rim=INK, trail=T, match=0.05, wrap=0)
    jim(s, 170, 640, 0.8, rim=INK, trail=T, match=0.05, wrap=0)
    axie(s, 110, 800, 0.12, rim=INK, trail=T, match=0.05, wrap=0)
panel(main, main_plate, main_draw)
def p1_plate():
    return halftone((W, H), 22, (130, 20, 120), (225, 50, 130), lambda x, y: np.clip(0.2 + 0.8 * np.hypot(x - 2000, y - 300) / 1400, 0, 1))
def p1_draw(s):
    s.place("ophelia_head", 1660, 40, scale=1.15, rim=dict(color=(255, 255, 255), dir=(-1, -1), width=8, strength=1.0), match=0.05, wrap=0)
panel((1650, 50, 2414, 690), p1_plate, p1_draw)
def p2_plate():
    return halftone((W, H), 22, (200, 70, 20), (255, 140, 50), lambda x, y: np.clip(0.2 + 0.8 * np.hypot(x - 2000, y - 1000) / 1400, 0, 1))
def p2_draw(s):
    s.place("worm_bandits", 1700, 730, scale=0.95, rim=dict(color=(255, 255, 255), dir=(-1, -1), width=7, strength=1.0), match=0.05, wrap=0)
    s.place("golfer", 2150, 860, scale=0.85, rim=dict(color=(255, 255, 255), dir=(-1, -1), width=7, strength=1.0), match=0.05, wrap=0)
panel((1650, 722, 2414, 1362), p2_plate, p2_draw)
# Cappy breaks out of the main panel frame
INK = dict(color=(255, 255, 255), dir=(1, -1), width=9, strength=1.0)
cappy(c, 420, 470, 1.32, rim=INK, trail=dict(length=300, color=(255, 255, 255), opacity=0.35, angle=195), match=0.05, wrap=0)
# tiny onomatopoeia at the gatling
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/InterDisplay-BlackItalic.otf", 92)
gx, gy = anchor("cappy", "cappy_gatling", 420, 470, 1.32)
t = Image.new("RGBA", (420, 200), (0, 0, 0, 0)); td = ImageDraw.Draw(t)
td.text((210, 100), "POP!", font=f, anchor="mm", fill=(255, 240, 80, 255), stroke_width=9, stroke_fill=(25, 15, 30, 255))
c.canvas.alpha_composite(t.rotate(12, Image.BICUBIC, expand=True), (int(gx + 60), int(gy - 250)))
c.logo(620, 280, 900, shadow=0.75)
c.grade(contrast=1.04, sat=1.05, vignette=0.15)
c.save("15_comic_cover", "out")
