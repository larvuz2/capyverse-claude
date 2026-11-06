"""Round 9 capsules: Gus's round-12 capsule, keeping everything inside the director's red outline untouched
(Cappy, enemies, Ophelia, logo, popcorn/BOOM/POW), replacing the back heroes and the background.

- Back heroes: original Unreal renders (H_moody matte-passed, H_jim) + Axie (matte-passed); colour-matched to the new
  background, rim-lit by its light, belt-thruster flames, jet trails, a soft shadow on the ground below so they read as
  flying over the scene, not pasted on top.
- Backgrounds: real Capyverse lobby screenshots (Drive 'Lobby' folder), graded and slightly defocused for depth.
"""
import sys, os, math
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r8")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
import compose as C
from compose import *
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

R8 = "/home/user/capyverse-claude/work/capsules-r8"
ENV = "/home/user/capyverse-claude/assets_src/env2/Lobby"
LOGO = "/home/user/capyverse-claude/work/logo-tin/tin_hanging.png"
W, H = C.W, C.H                     # 2464 x 1412
K = H / 1116; OXC = (2000 * K - W) / 2


def P(x, y): return x * K - OXC, y * K


def cover_img(im):
    im = im.resize((round(im.width * K), H), Image.LANCZOS)
    return im.crop((round(OXC), 0, round(OXC) + W, H))


BASE = Image.open(f"{R8}/base.jpg").convert("RGBA")
CUT = Image.open(f"{R8}/cut_0.png").convert("RGBA")

# --- split the cut: drop the three back heroes (components 1=Jim, 3=Moody, 5=Axie), keep the rest exactly ---
a = np.array(CUT); m = a[..., 3] > 40
lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=2))
sizes = ndimage.sum(m, lab, range(1, n + 1)); objs = ndimage.find_objects(lab)
heroes = np.zeros_like(m)
for i, (sl, s) in enumerate(zip(objs, sizes), 1):
    if s < 3000: continue
    x0, x1, y0, y1 = sl[1].start, sl[1].stop, sl[0].start, sl[0].stop
    if x1 < 900 and y1 < 760: heroes |= lab == i          # Jim, Moody, Axie (Cappy reaches y~1107)
heroes = ndimage.binary_dilation(heroes, iterations=6)
keep = a.copy(); keep[..., 3] = np.where(heroes, 0, keep[..., 3])
KEEP = cover_img(Image.fromarray(keep))

# jet flames lost by the cutout: recover Cappy's only (the back heroes get new ones)
b = np.asarray(BASE).astype(np.float32) / 255; c = a.astype(np.float32) / 255
flame = np.clip((b[..., 2] - b[..., 0] + 0.25) * 4, 0, 1) * np.clip((b[..., :3].mean(-1) - 0.55) * 4, 0, 1) * (1 - c[..., 3])
yy, xx = np.mgrid[0:b.shape[0], 0:b.shape[1]]
flame *= ~((xx < 900) & (yy < 780))
FLAMES = cover_img(Image.fromarray((np.dstack([b[..., :3], flame]) * 255).astype(np.uint8)))
KMASK = np.asarray(KEEP.getchannel("A")) > 30


def background(name, focus=(0.5, 0.5), warm=0.0, lift=0.0, blur=2.0, sat=1.0, haze=None):
    bg = Image.open(f"{ENV}/{name}.png").convert("RGB")
    s = max(W / bg.width, H / bg.height); bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
    x = round((bg.width - W) * focus[0]); y = round((bg.height - H) * focus[1]); bg = bg.crop((x, y, x + W, y + H))
    if blur: bg = bg.filter(ImageFilter.GaussianBlur(blur))     # shallow depth of field: characters stay sharp
    bg = ImageEnhance.Color(bg).enhance(sat)
    arr_ = np.asarray(bg).astype(np.float32) / 255
    if lift: arr_ = arr_ * (1 - lift) + lift                   # open the shadows so sunlit characters fit
    if warm:  # golden-hour wash: screen a warm gradient, stronger at the top
        g = np.linspace(1, 0.35, H)[:, None, None] * np.array([1.0, 0.62, 0.22]) * warm
        arr_ = 1 - (1 - arr_) * (1 - g)
    if haze:  # atmospheric haze toward the horizon band
        col, amt, yc = haze
        hz = np.exp(-((np.arange(H) - yc * H) / (H * 0.22)) ** 2)[:, None, None] * amt
        arr_ = arr_ * (1 - hz) + np.array(col) / 255 * hz
    return Image.fromarray((np.clip(arr_, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def ground_shadow(c, cx, gy, w, alpha=90):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.ellipse([cx - w / 2, gy - w * 0.07, cx + w / 2, gy + w * 0.07], fill=(20, 10, 30, alpha))
    c.canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(w * 0.08)))


def contact_shadows(c):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    for x0, x1, y, a_ in [(1100, 1420, 1112, 120), (1500, 1640, 1112, 120), (1620, 2000, 1112, 130)]:
        (X0, Y), (X1, _) = P(x0, y), P(x1, y)
        d.ellipse([X0, Y - 34, X1, Y + 34], fill=(25, 12, 30, a_))
    c.canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))


def hero(c, kind, x, y, s, rim, trail_len=260, gy=None, shadow_a=80, match=0.28, bright=1.0):
    """Place one back hero; returns its screen bbox. Uses the matte-passed layers for Moody and Axie."""
    src = {"moody": "layers/L_moody_matte.png" if False else None}.get(kind)
    T = dict(length=trail_len, color=(255, 245, 230), opacity=0.22, angle=195)
    kw = dict(rim=dict(color=rim, dir=(-1, -1), width=7, strength=0.75), trail=T, match=match, wrap=0.4, bright=bright,
              flame_len=1.7, flame_w=1.5)
    if kind == "moody":
        L = load("layers/H_moody_matte.png"); kk = 5760 / 2560
        c.place("moody", x, y, scale=s, src=L.resize((max(1, round(L.width * s / kk)), max(1, round(L.height * s / kk))), Image.LANCZOS) if False else None, flames=True, **kw) if False else None
        Lr = L.resize((round(L.width * s / kk), round(L.height * s / kk)), Image.LANCZOS)
        c.place("moody", x, y, scale=1.0, src=Lr, **{k: v for k, v in kw.items() if k not in ("flame_len", "flame_w")})
        for fx, fy, ang in C.THRUSTERS["moody"]: c.flame(x + fx * s, y + fy * s, ang, 190 * s * 1.7, 50 * s * 1.5)
        disco_flares(c, *anchor("moody", "moody_disco", x, y, s), s, seed=9)
        w, h = 432 * s, 341 * s
    elif kind == "jim":
        jim(c, x, y, s, confetti_n=35, **kw); w, h = 293 * s, 203 * s
    else:
        L = load("layers/L_axie_matte.png")
        Lr = L.resize((round(L.width * s), round(L.height * s)), Image.LANCZOS)
        c.place("axie", x, y, scale=1.0, src=Lr, **{k: v for k, v in kw.items() if k not in ("flame_len", "flame_w")})
        for fx, fy, ang in C.THRUSTERS["axie"]: c.flame(x + fx * s, y + fy * s, ang, 190 * s * 1.7, 50 * s * 1.5)
        w, h = 2233 * s, 1129 * s
    if gy: ground_shadow(c, x + w * 0.55, gy, w * 0.75, shadow_a)
    return (x, y, x + w, y + h)


def fx_red(c):
    """FX inside the red outline, same as round 12: popcorn, Ophelia glints/crown, golf ball, BOOM/POW."""
    s = 1.0
    popcorn_burst(c, *P(738, 492), 1.25 * s, angle=22, n=11, dist=420)
    for ex, ey in ((1618, 545), (1880, 525)): c.glow(*P(ex, ey), 70, (255, 40, 40), 0.55)
    sparkle(c, *P(1715, 290), 150, (255, 250, 220), 0.9, rot=15)
    c.glow(*P(1465, 710), 60, (255, 255, 240), 0.6)
    sfx(c, "BOOM!", *P(800, 600), 84, rot=12, fill=(255, 210, 90))
    sfx(c, "POW!", *P(1460, 600), 84, rot=-8, fill=(255, 230, 150))


def logo(c, extra_boxes):
    import r8_sizes as R
    mask = np.asarray(Image.fromarray((KMASK * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(7))) > 8
    mask = mask.copy()
    for x0, y0, x1, y1 in extra_boxes: mask[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)] = True
    R.LOGO = LOGO
    cx, cy, w = R.fit_logo(mask, W, H, prefer=(0.52, 0.28), max_frac=0.9)
    R.logo(c, cx, cy, w, 1.0)
    return cx, cy, w


# five approaches: background + where the back heroes fly + how they are integrated
APPROACHES = {
    "1_golden_path": dict(bg=("Capyverse_Lobby_ (3)", (0.5, 0.6)), grade=dict(warm=0.55, lift=0.10, blur=2.5, sat=1.05),
        rim=(255, 225, 170), heroes=[("moody", 30, 300, 0.95), ("jim", 330, 150, 1.0), ("axie", 0, 690, 0.15)], gy=1330, whoosh=(560, 420)),
    "2_portal_night": dict(bg=("Capyverse_Lobby_ (2)", (0.5, 0.55)), grade=dict(warm=0.25, lift=0.14, blur=2.5, sat=1.1),
        rim=(200, 170, 255), heroes=[("jim", 380, 110, 0.8), ("moody", 20, 260, 1.1), ("axie", 0, 700, 0.15)], gy=1330, whoosh=(600, 470)),
    "3_glow_tree": dict(bg=("CapsuleScreenshot_ (9)", (0.35, 0.6)), grade=dict(warm=0.35, lift=0.12, blur=3.0, sat=1.05, haze=((255, 200, 160), 0.18, 0.62)),
        rim=(170, 255, 225), heroes=[("moody", 120, 250, 0.78), ("jim", 400, 140, 0.82), ("axie", 40, 620, 0.13)], gy=1300, whoosh=(560, 380)),
    "4_cave_glow": dict(bg=("CapsuleScreenshot_ (6)", (0.5, 0.6)), grade=dict(warm=0.40, lift=0.10, blur=2.5, sat=1.05),
        rim=(255, 200, 140), heroes=[("jim", 40, 170, 1.05), ("moody", 120, 380, 1.0), ("axie", 10, 700, 0.15)], gy=1330, whoosh=None),
    "5_river_moon": dict(bg=("Capyverse_Lobby_ (4)", (0.5, 0.5)), grade=dict(warm=0.30, lift=0.12, blur=2.5, sat=1.1, haze=((230, 190, 255), 0.15, 0.55)),
        rim=(220, 200, 255), heroes=[("moody", 40, 30, 0.72), ("jim", 20, 300, 1.15), ("axie", 0, 690, 0.15)], gy=1330, whoosh=(560, 470)),
}


def build(name):
    cfg = APPROACHES[name]
    c = Comp(background(cfg["bg"][0], cfg["bg"][1], **cfg["grade"]))
    contact_shadows(c)
    boxes = [hero(c, k, x, y, s, cfg["rim"], gy=cfg["gy"]) for k, x, y, s in cfg["heroes"]]
    c.screen(FLAMES); c.canvas.alpha_composite(KEEP)          # the red-outline content, untouched
    fx_red(c)
    if cfg["whoosh"]: sfx(c, "WHOOSH!", *cfg["whoosh"], 74, rot=-10, fill=(255, 230, 150))
    logo(c, boxes)
    c.grade(contrast=1.04, sat=1.04, vignette=0.28)
    c.save(f"r9_{name}", f"{R8}/r9")


if __name__ == "__main__":
    for n in (sys.argv[1:] or APPROACHES): build(n)
