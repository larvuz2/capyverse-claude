"""Round 8 takes A/B/C rebuilt natively at every Steam store capsule size.

Heroes (left half of Gus's composition) stay anchored to the left edge, enemies + Ophelia (right half) to the right
edge, both height-fitted; backgrounds are procedural/layered so they extend to any width; the logo is auto-fitted
into whatever free space each size leaves. Rendered at 2x and downsampled.
"""
import sys, os, math
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
import compose as C
from compose import load, arr, img, popcorn_burst, disco_flares, confetti, sparkle, sfx
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

R8 = "/home/user/capyverse-claude/work/capsules-r8"
LOGO = "/home/user/capyverse-claude/work/logo-lab/out/logo_e4_trim.png"
SIZES = {"header": (920, 430), "main": (1232, 706), "small": (462, 174), "vertical": (748, 896)}
CUT = load(f"{R8}/cut_0.png"); BASE = load(f"{R8}/base.jpg")
SPLIT = 1000  # x in base: heroes left of it, enemies right


def recover_flames():
    b = arr(BASE); c = arr(CUT)
    r, bl = b[..., 0], b[..., 2]
    flame = np.clip((bl - r + 0.25) * 4, 0, 1) * np.clip((b[..., :3].mean(-1) - 0.55) * 4, 0, 1) * (1 - c[..., 3])
    return img(np.dstack([b[..., :3], flame]))


FLAMES = recover_flames()


class Layout:
    """Maps base-image coordinates of each group onto the target canvas."""
    def __init__(self, cw, ch, hero_scale=1.0, enemy_scale=1.0, vertical=False):
        self.cw, self.ch = cw, ch
        s = ch / 1116
        self.sl, self.sr = s * hero_scale, s * enemy_scale
        if vertical:  # narrow formats: shrink groups so both fit, enemies bottom-right, heroes bottom-left
            self.sl = self.sr = min(s, cw / 1350) * 1.0
        self.oyl = ch - 1116 * self.sl; self.oyr = ch - 1116 * self.sr

    def L(self, x, y): return x * self.sl, y * self.sl + self.oyl
    def Rt(self, x, y): return self.cw - (2000 - x) * self.sr, y * self.sr + self.oyr
    def P(self, x, y): return self.L(x, y) if x < SPLIT else self.Rt(x, y)


def group(src, x0, x1):
    g = Image.new("RGBA", src.size, (0, 0, 0, 0)); g.paste(src.crop((x0, 0, x1, src.height)), (x0, 0)); return g


def place_groups(c, lay, src):
    left = group(src, 0, SPLIT).crop((0, 0, SPLIT, 1116)); right = group(src, SPLIT, 2000).crop((SPLIT, 0, 2000, 1116))
    l = left.resize((max(1, round(SPLIT * lay.sl)), max(1, round(1116 * lay.sl))), Image.LANCZOS)
    r = right.resize((max(1, round(1000 * lay.sr)), max(1, round(1116 * lay.sr))), Image.LANCZOS)
    c.canvas.alpha_composite(r, (round(lay.cw - r.width), round(lay.oyr)))
    c.canvas.alpha_composite(l, (0, round(lay.oyl)))


def char_mask(lay, pad):
    m = Image.new("L", (lay.cw, lay.ch), 0)
    a = CUT.getchannel("A")
    l = a.crop((0, 0, SPLIT, 1116)).resize((max(1, round(SPLIT * lay.sl)), max(1, round(1116 * lay.sl))))
    r = a.crop((SPLIT, 0, 2000, 1116)).resize((max(1, round(1000 * lay.sr)), max(1, round(1116 * lay.sr))))
    m.paste(r, (round(lay.cw - r.width), round(lay.oyr)), r); m.paste(l, (0, round(lay.oyl)), l)
    return np.asarray(m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(pad / 2))) > 8


def fit_logo(mask, cw, ch, prefer=(0.52, 0.36), max_frac=0.78):
    Lg = load(LOGO); la = Lg.getchannel("A"); ar = Lg.height / Lg.width
    step = max(4, cw // 120)
    for w in np.linspace(cw * max_frac, cw * 0.2, 60).astype(int):
        h = int(w * ar); small = np.asarray(la.resize((w, h))) > 20; best = None
        for cy in range(h // 2 + step, ch - h // 2 - step, step):
            for cx in range(w // 2 + step, cw - w // 2 - step, step):
                if not (mask[cy - h // 2:cy - h // 2 + h, cx - w // 2:cx - w // 2 + w] & small).any():
                    d = abs(cx - cw * prefer[0]) / cw + abs(cy - ch * prefer[1]) / ch * 1.5
                    if best is None or d < best[2]: best = (cx, cy, d)
        if best: return best[0], best[1], w
    return cw // 2, ch // 3, int(cw * 0.3)


def logo(c, cx, cy, w, k):
    Lg = load(LOGO); h = round(Lg.height * w / Lg.width); Lg = Lg.resize((w, h), Image.LANCZOS).rotate(-2, Image.BICUBIC, expand=True)
    x, y = cx - Lg.width / 2, cy - Lg.height / 2
    p = int(140 * k); ga = Image.new("L", (Lg.width + 2 * p, Lg.height + 2 * p), 0); ga.paste(Lg.getchannel("A"), (p, p))
    g = Image.new("RGBA", ga.size, (255, 240, 200, 0)); g.putalpha(ga.filter(ImageFilter.GaussianBlur(max(2, 60 * k))).point(lambda v: int(v * 0.75)))
    c.screen(g, x - p, y - p)
    c._shadow(Lg, x, y, dx=w * 0.01, dy=w * 0.028, blur=max(2, int(w * 0.018)), opacity=0.5, color=(70, 25, 5))
    c.canvas.alpha_composite(Lg, (int(x), int(y)))


def gradient_bg(cw, ch):
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    t = np.clip(yy / ch * 0.85 + np.hypot((xx - cw * 0.5) / cw, (yy - ch * 0.05) / ch) * 0.45, 0, 1)[..., None]
    top = np.array([252, 208, 4], np.float32); bot = np.array([243, 104, 14], np.float32)
    return Image.fromarray((top + (bot - top) * t).astype(np.uint8)).convert("RGBA")


def floor(c, cw, ch, y_top):
    F = load(f"{R8}/floorkey0.png"); a = np.asarray(F.getchannel("A")); ys = np.nonzero(a.max(1) > 10)[0]
    F = F.crop((0, ys.min(), F.width, ys.max() + 1))
    hgt = int(ch * (1 - y_top) + ch * 0.05); wid = max(cw, int(F.width * hgt / F.height))
    F = F.resize((wid, hgt), Image.LANCZOS)
    c.canvas.alpha_composite(F, ((cw - wid) // 2, int(ch * y_top)))
    hz = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(hz); band = max(20, int(ch * 0.11))
    for i in range(band):
        d.line([(0, ch * y_top + i - band / 4), (cw, ch * y_top + i - band / 4)], fill=(255, 205, 120, int(130 * math.sin(math.pi * i / band))))
    c.canvas.alpha_composite(hz.filter(ImageFilter.GaussianBlur(max(2, ch * 0.013))))


def mesas(c, cw, ch, y_bottom):
    M = load("/home/user/capyverse-claude/work/capsules-3d/bg/canyon_mountains_cut_0.png")
    a = np.asarray(M.getchannel("A")); ys = np.nonzero(a.max(1) > 10)[0]; M = M.crop((0, ys.min(), M.width, ys.max() + 1))
    hgt = int(ch * 0.2); wid = max(int(cw * 1.1), int(M.width * hgt / M.height)); M = M.resize((wid, hgt), Image.LANCZOS)
    m = arr(M); m[..., :3] = m[..., :3] * 0.55 + np.array([1.0, 0.72, 0.38]) * 0.45
    c.canvas.alpha_composite(img(m).filter(ImageFilter.GaussianBlur(max(1, ch * 0.001))), ((cw - wid) // 2, int(y_bottom - hgt)))


def sunburst(c, cw, ch, cx, cy, rays=22):
    ov = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); R = cw * 2
    for i in range(rays):
        t0, t1 = 2 * math.pi * i / rays, 2 * math.pi * (i + 0.5) / rays
        d.polygon([(cx, cy), (cx + R * math.cos(t0), cy + R * math.sin(t0)), (cx + R * math.cos(t1), cy + R * math.sin(t1))], fill=(255, 228, 90, 170))
    c.canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(2)))
    c.glow(cx, cy, cw * 0.37, (255, 250, 210), 0.55)


def contact_shadows(c, lay):
    sh = Image.new("RGBA", (lay.cw, lay.ch), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for x0, x1, y, a in [(1100, 1420, 1112, 120), (1500, 1640, 1112, 120), (1620, 2000, 1112, 130), (60, 760, 1105, 60)]:
        (X0, Y), (X1, _) = lay.P(x0, y), lay.P(x1, y); r = 26 * lay.sr
        d.ellipse([X0, Y - r, X1, Y + r], fill=(70, 30, 5, a))
    c.canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(2, 22 * lay.sr))))


def fx(c, lay, k, sfx_on=True):
    s = lay.sl / (1412 / 1116)  # relative to the 2464x1412 tuning
    popcorn_burst(c, *lay.P(738, 492), 1.25 * s, angle=22, n=11, dist=420)
    disco_flares(c, *lay.P(243, 262), 1.25 * s, seed=9)
    confetti(c, *lay.P(500, 130), 1.3 * s, angle=15, spread=32, n=45, dist=110, seed=7)
    for ex, ey in ((1618, 545), (1880, 525)): c.glow(*lay.P(ex, ey), 70 * s, (255, 40, 40), 0.55)
    sparkle(c, *lay.P(1715, 290), 150 * s, (255, 250, 220), 0.9, rot=15)
    c.glow(*lay.P(1465, 710), 60 * s, (255, 255, 240), 0.6)
    if sfx_on and lay.cw >= 900:
        sfx(c, "WHOOSH!", *lay.P(500, 320), 74 * s, rot=-10, fill=(255, 230, 150))
        sfx(c, "BOOM!", *lay.P(800, 600), 84 * s, rot=12, fill=(255, 210, 90))
        sfx(c, "POW!", *lay.P(1460, 600), 84 * s, rot=-8, fill=(255, 230, 150))


def build(take, size, out_dir=f"{R8}/sizes"):
    tw, th = SIZES[size]; k = 2; cw, ch = tw * k, th * k
    C.W, C.H = cw, ch
    vertical = th > tw
    lay = Layout(cw, ch, vertical=vertical)
    c = C.Comp(gradient_bg(cw, ch))
    mask = char_mask(lay, pad=max(6, int(40 * lay.sl)))
    prefer = (0.5, 0.22) if vertical else (0.52, 0.36)
    lx, ly, lw = fit_logo(mask, cw, ch, prefer=prefer, max_frac=0.9 if vertical else 0.78)
    if take == "C":
        sunburst(c, cw, ch, lx, ly + int(20 * k)); mesas(c, cw, ch, ch * 0.80)
    if take in "BC":
        floor(c, cw, ch, 0.74 if take == "B" else 0.78); contact_shadows(c, lay)
    c.screen(Image.new("RGBA", (cw, ch)))  # no-op keeps API symmetric
    fl = FLAMES.crop((0, 0, 2000, 1116))
    place_groups(c, lay, fl); place_groups(c, lay, CUT)
    fx(c, lay, k)
    logo(c, lx, ly, lw, lay.sl)
    c.grade(contrast=1.04, sat=1.05, vignette=0.22)
    os.makedirs(out_dir, exist_ok=True)
    c.canvas.convert("RGB").resize((tw, th), Image.LANCZOS).save(f"{out_dir}/{take}_{size}_{tw}x{th}.jpg", quality=93)
    return lw / cw


if __name__ == "__main__":
    takes = sys.argv[1] if len(sys.argv) > 1 else "ABC"; sizes = sys.argv[2:] or list(SIZES)
    for t in takes:
        for sz in sizes: print(t, sz, "logo frac %.2f" % build(t, sz))
