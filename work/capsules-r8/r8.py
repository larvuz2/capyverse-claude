"""Round 8: three takes on Gus's composition (base.jpg). Characters stay exactly where he put them.
A = his background untouched; B = same gradient + low-poly desert floor; C = sunburst + mesas + desert.
Logo: auto-fitted as big as possible in the centre without overlapping any character (mask-based search)."""
import sys, os
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
from compose import *

R8 = "/home/user/capyverse-claude/work/capsules-r8"
LOGO = "/home/user/capyverse-claude/work/logo-lab/out/logo_e4_trim.png"
K = H / 1116; OXC = (2000 * K - W) / 2  # base -> canvas mapping (cover crop)


def P(x, y): return x * K - OXC, y * K


def cover_img(path):
    im = load(path); im = im.resize((round(im.width * K), H), Image.LANCZOS)
    return im.crop((round(OXC), 0, round(OXC) + W, H))


BASE = cover_img(f"{R8}/base.jpg")
CHARS = cover_img(f"{R8}/cut_0.png")


def recover_flames():
    """Pull the bluish-white jet flames (lost by the cutout) out of the original image as their own layer."""
    b = arr(BASE); c = arr(CHARS)
    r, g, bl = b[..., 0], b[..., 1], b[..., 2]
    flame = np.clip((bl - r + 0.25) * 4, 0, 1) * np.clip((b[..., :3].mean(-1) - 0.55) * 4, 0, 1) * (1 - c[..., 3])
    f = np.dstack([b[..., :3], flame]); return img(f)


FLAMES = recover_flames()


def char_mask(pad=40, extra=()):
    a = (np.asarray(CHARS.getchannel("A")) > 30)
    m = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(pad / 2))) > 8
    for x0, y0, x1, y1 in extra: m[int(y0):int(y1), int(x0):int(x1)] = True
    return m


def fit_logo(mask, region=(0.18, 0.02, 0.86, 0.75)):
    Lg = load(LOGO); la = np.asarray(Lg.getchannel("A")) > 20; ar = Lg.height / Lg.width
    best = None
    for w in range(1700, 600, -20):
        h = int(w * ar)
        small = np.asarray(Image.fromarray((la * 255).astype(np.uint8)).resize((w, h))) > 20
        for cy in range(int(H * region[1] + h / 2), int(H * region[3] - h / 2), 12):
            for cx in range(int(W * region[0] + w / 2), int(W * region[2] - w / 2), 12):
                x0, y0 = cx - w // 2, cy - h // 2
                if not (mask[y0:y0 + h, x0:x0 + w] & small).any():
                    d = abs(cx - W * 0.53) + abs(cy - H * 0.36) * 1.5
                    if best is None or d < best[3]: best = (cx, cy, w, d)
        if best: return best[:3]
    return W // 2, H // 3, 700


def logo(c, cx, cy, w, rot=-2, glow=(255, 240, 200), shadow=(70, 25, 5)):
    Lg = load(LOGO); h = round(Lg.height * w / Lg.width); Lg = Lg.resize((w, h), Image.LANCZOS).rotate(rot, Image.BICUBIC, expand=True)
    x, y = cx - Lg.width / 2, cy - Lg.height / 2
    if glow:
        p = 140; ga = Image.new("L", (Lg.width + 2 * p, Lg.height + 2 * p), 0); ga.paste(Lg.getchannel("A"), (p, p))
        g = Image.new("RGBA", ga.size, glow + (0,)); g.putalpha(ga.filter(ImageFilter.GaussianBlur(60)).point(lambda v: int(v * 0.75)))
        c.screen(g, x - p, y - p)
    c._shadow(Lg, x, y, dx=w * 0.01, dy=w * 0.028, blur=int(w * 0.018), opacity=0.5, color=shadow)
    c.canvas.alpha_composite(Lg, (int(x), int(y)))


def fx(c, sfx_on=True):
    # popcorn burst + muzzle flash from Cappy's gatling
    popcorn_burst(c, *P(738, 492), 1.25, angle=22, n=11, dist=420)
    # disco-ball flares on Moody's cannon
    disco_flares(c, *P(243, 262), 1.25, seed=9)
    # confetti from Jim's trumpet
    confetti(c, *P(500, 130), 1.3, angle=15, spread=32, n=45, dist=110, seed=7)
    # Ophelia's red eye glints + crown sparkle
    for ex, ey in ((1618, 545), (1880, 525)): c.glow(*P(ex, ey), 70, (255, 40, 40), 0.55)
    sparkle(c, *P(1715, 290), 150, (255, 250, 220), 0.9, rot=15)
    # golf ball streak + worm dust burst
    c.glow(*P(1465, 710), 60, (255, 255, 240), 0.6)
    c.particles(45, (*P(1070, 1000), *P(1420, 1116)), [(230, 190, 130), (210, 160, 100), (245, 215, 160)], size=(4, 14), seed=5, glow=False)
    if sfx_on:
        sfx(c, "WHOOSH!", *P(500, 320), 74, rot=-10, fill=(255, 230, 150))
        sfx(c, "BOOM!", *P(800, 600), 84, rot=12, fill=(255, 210, 90))
        sfx(c, "POW!", *P(1460, 600), 84, rot=-8, fill=(255, 230, 150))


def chars(c):
    c.screen(FLAMES); c.canvas.alpha_composite(CHARS)


def gradient_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip(yy / H * 0.85 + np.hypot((xx - W * 0.5) / W, (yy - H * 0.05) / H) * 0.45, 0, 1)[..., None]
    top = np.array([252, 208, 4], np.float32); bot = np.array([243, 104, 14], np.float32)
    return Image.fromarray((top + (bot - top) * t).astype(np.uint8)).convert("RGBA")


def floor(c, y_top=0.70, warm=0.0):
    F = load(f"{R8}/floorkey0.png"); F = F.resize((W, round(F.height * W / F.width)), Image.LANCZOS)
    a = np.asarray(F.getchannel("A")); ys = np.nonzero(a.max(1) > 10)[0]; F = F.crop((0, ys.min(), W, ys.max() + 1))
    F = F.resize((W, int(H * (1 - y_top) + 60)), Image.LANCZOS)
    c.canvas.alpha_composite(F, (0, int(H * y_top)))
    # haze where the dunes meet the sky
    hz = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hz)
    for i in range(160):
        d.line([(0, H * y_top + i - 40), (W, H * y_top + i - 40)], fill=(255, 205, 120, int(130 * math.sin(math.pi * i / 160))))
    c.canvas.alpha_composite(hz.filter(ImageFilter.GaussianBlur(18)))


def contact_shadows(c):
    """Soft shadows on the sand under the grounded enemies and under Cappy (flying, so a faint offset blob)."""
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for x0, x1, y, a in [(1100, 1420, 1112, 120), (1500, 1640, 1112, 120), (1620, 2000, 1112, 130), (60, 760, 1105, 60)]:
        (X0, Y), (X1, _) = P(x0, y), P(x1, y)
        d.ellipse([X0, Y - 26, X1, Y + 26], fill=(70, 30, 5, a))
    c.canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))


def sunburst(c, cx, cy, rays=22, a=(255, 228, 90), b=(255, 170, 40), alpha=170):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); R = 3000
    for i in range(rays):
        t0, t1 = 2 * math.pi * i / rays, 2 * math.pi * (i + 0.5) / rays
        d.polygon([(cx, cy), (cx + R * math.cos(t0), cy + R * math.sin(t0)), (cx + R * math.cos(t1), cy + R * math.sin(t1))], fill=a + (alpha,))
    c.canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(2)))
    c.glow(cx, cy, 900, (255, 250, 210), 0.55)


def mesas(c, y_bottom):
    M = load("/home/user/capyverse-claude/work/capsules-3d/bg/canyon_mountains_cut_0.png")
    M = M.resize((int(W * 1.1), int(M.height * W * 1.1 / M.width)), Image.LANCZOS)
    a = np.asarray(M.getchannel("A")); ys = np.nonzero(a.max(1) > 10)[0]; M = M.crop((0, ys.min(), M.width, ys.max() + 1))
    m = arr(M); m[..., :3] = m[..., :3] * 0.55 + np.array([1.0, 0.72, 0.38]) * 0.45; M = img(m).filter(ImageFilter.GaussianBlur(1.5))
    c.canvas.alpha_composite(M, (int(-W * 0.05), int(y_bottom - M.height)))


def build(take):
    if take == "A":   # Gus's background untouched; logo + FX layers only
        c = Comp(BASE.copy())
        mask = char_mask(extra=[(*P(410, 280), *P(600, 370)), (*P(680, 390), *P(840, 480)), (*P(1400, 580), *P(1520, 660))])
        fx(c, sfx_on=False)
    elif take == "B":  # same gradient + low-poly desert floor, contact shadows, heat haze
        c = Comp(gradient_bg()); floor(c, 0.74); contact_shadows(c); chars(c); fx(c); mask = char_mask()
    else:              # C: sunburst from the logo, hazy mesas, desert floor
        c = Comp(gradient_bg()); mask = char_mask()
        cx, cy, w = fit_logo(mask); sunburst(c, cx, cy + 40)
        mesas(c, H * 0.80); floor(c, 0.78); contact_shadows(c); chars(c); fx(c)
        logo(c, cx, cy, w); c.grade(contrast=1.05, sat=1.06, vignette=0.32); c.save(f"r8_{take}", f"{R8}/out"); return w
    cx, cy, w = fit_logo(mask)
    logo(c, cx, cy, w)
    c.grade(contrast=1.04, sat=1.05, vignette=0.28 if take == "B" else 0.18)
    c.save(f"r8_{take}", f"{R8}/out")
    return w


if __name__ == "__main__":
    for t in (sys.argv[1:] or "ABC"): print(t, "logo width", build(t))
