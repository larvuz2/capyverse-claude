"""Round 15: three new hand-built capsules + the round-14 Cappy Solo, each built natively at every Steam store size.

  S  Round-14 Cappy Solo (night meadow, Cappy lower-right, Ophelia in the fire sky)
  D  Duel         Cappy (left) fires across a real lobby screenshot at a giant Ophelia (right)
  Q  Squad Burst  the four heroes on the brand yellow-orange sunburst, logo on the burst
  U  Close-Up     Cappy's face + gatling huge on teal (complement of his orange), popcorn in the foreground

Characters are the real Unreal renders (H_cappy, H_moody_matte, H_jim, H_ophelia_head); Axie is the matte-passed
solo render. No character goes through an image model here. Layouts are written in fractions of the canvas so the
same design re-flows for header 920x430, main 1232x706 and small 462x174.

python3 r15.py [S D Q U] [header main small]
"""
import sys, os, math, glob
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
import compose as C
from compose import load, arr, img, sparkle, popcorn_burst, disco_flares, confetti, sfx
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

HERE = "/home/user/capyverse-claude/work/capsules-r15"
LOGO = "/home/user/capyverse-claude/work/logo-tin/tin_hanging.png"
ENV = "/home/user/capyverse-claude/assets_src/env2/Lobby"
PLATE = "/home/user/capyverse-claude/work/capsules-r11/plate_nb_0.png"
SIZES = {"header": (920, 430, 2), "main": (1232, 706, 2), "small": (462, 174, 4)}
TIP = (2055, 95)                       # gatling muzzle in H_cappy pixels
THR = (895, 1017)                      # rear of Cappy's belt jet cylinder in H_cappy pixels


def ovl(): return Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))


# ---------- characters ----------
def cappy_img(width, flip=False):
    S = width / 2315
    im = load("layers/H_cappy.png"); im = im.resize((round(width), round(im.height * S)), Image.LANCZOS)
    tip = np.array(TIP) * S; thr = np.array(THR) * S
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT); tip[0] = width - tip[0]; thr[0] = width - thr[0]
    return im, tip, thr


def put_cappy(c, x, y, width, flip=False, rim=(255, 200, 120), rim_dir=(-1, -1), match=0.1, flame=True):
    im, tip, thr = cappy_img(width, flip)
    c.place("cappy", x, y, scale=1.0, src=im, match=match, wrap=0.3, rim=dict(color=rim, dir=rim_dir, width=max(3, width / 130), strength=0.7))
    if flame:
        c.flame(x + thr[0], y + thr[1], 6 if flip else 186, width * 0.34, width * 0.07)
        c.glow(x + thr[0], y + thr[1], width * 0.2, (255, 170, 80), 0.6)
    return (x + tip[0], y + tip[1])


def muzzle(c, p, size, ang, pop=7):
    c.glow(p[0], p[1], size, (255, 190, 80), 0.95)
    sparkle(c, p[0], p[1], size * 1.2, (255, 235, 160), 1.0, rot=12)
    if pop: popcorn_burst(c, p[0], p[1], size / 250, angle=ang, n=pop, dist=190, flare=False, seed=3)


def tracers(c, p0, ang, length, width, n=5, seed=3, spread=4):
    rnd = np.random.default_rng(seed); g = ovl(); d = ImageDraw.Draw(g)
    for i in range(n):
        a = math.radians(ang + rnd.uniform(-spread, spread)); r0 = length * rnd.uniform(0.08, 0.3); r1 = r0 + length * rnd.uniform(0.5, 1.0)
        pts = [(p0[0] + math.cos(a) * r, p0[1] - math.sin(a) * r) for r in (r0, r1)]
        d.line(pts, fill=(255, 150, 40, 150), width=int(width * 2.8)); d.line(pts, fill=(255, 240, 170, 255), width=int(width))
    c.screen(g.filter(ImageFilter.GaussianBlur(width * 0.6)))


def ophelia_img(width, fade=True, tint=(0.95, 0.80, 0.74), dim=0.88, alpha=0.92):
    O = load("layers/H_ophelia_head.png"); O = O.resize((round(width), round(O.height * width / O.width)), Image.LANCZOS)
    oa = np.asarray(O).astype(np.float32); hh = O.height
    red = (oa[..., 0] > 150) & (oa[..., 1] < 70) & (oa[..., 2] < 70) & (oa[..., 3] > 200); red[: int(hh * 0.3)] = False
    lab, n = ndimage.label(red); sz = ndimage.sum(red, lab, range(1, n + 1))
    eyes = [ndimage.center_of_mass(red, lab, i + 1) for i in np.argsort(sz)[-2:]]
    if fade:
        f = np.clip((np.linspace(1, 0, hh) - 0.12) / 0.4, 0, 1) ** 1.3; oa[..., 3] *= f[:, None]
    oa[..., 3] *= alpha; oa[..., :3] = oa[..., :3] * np.array(tint) * dim
    return Image.fromarray(np.clip(oa, 0, 255).astype(np.uint8)), eyes


def put_ophelia(c, x, y, width, **kw):
    O, eyes = ophelia_img(width, **kw)
    c.canvas.alpha_composite(O, (round(x), round(y)))
    for ey, ex in eyes: c.glow(x + ex, y + ey, width * 0.12, (255, 30, 30), 0.85)
    return eyes


def hero(c, kind, x, y, width, rim=(255, 240, 200)):
    src = {"moody": "layers/H_moody_matte.png", "jim": "layers/H_jim.png", "axie": "layers/L_axie_matte.png"}[kind]
    im = load(src); k = width / im.width; im = im.resize((round(width), round(im.height * k)), Image.LANCZOS)
    c.place(kind, x, y, scale=1.0, src=im, match=0.06, wrap=0.2, rim=dict(color=rim, dir=(-1, -1), width=max(2, width / 90), strength=0.6),
            trail=dict(length=width * 0.5, color=(255, 255, 240), opacity=0.25, angle=190))
    lw = C.LW[kind]; s = width / lw
    for fx, fy, ang in C.THRUSTERS[kind]:
        c.flame(x + fx * s, y + fy * s, ang, 190 * s * 1.7, 50 * s * 1.5)
    if kind == "moody": disco_flares(c, x + 243 * s, y + 52 * s, s, seed=9)
    if kind == "jim": confetti(c, x + 282 * s, y + 72 * s, s * 0.8, angle=5, n=28, dist=220)


OBST = None      # everything the logo must stay clear of (Cappy + gatling, muzzle flash, popcorn, other heroes)


def reserve(im, x, y):
    global OBST
    if OBST is None: OBST = np.zeros((C.H, C.W), bool)
    a = np.asarray(im.getchannel("A")) > 40
    x, y = round(x), round(y)
    x0, y0, x1, y1 = max(0, x), max(0, y), min(C.W, x + im.width), min(C.H, y + im.height)
    if x1 > x0 and y1 > y0: OBST[y0:y1, x0:x1] |= a[y0 - y:y1 - y, x0 - x:x1 - x]


def reserve_muzzle(p, size, ang, pop):
    global OBST
    if OBST is None: OBST = np.zeros((C.H, C.W), bool)
    m = Image.new("L", (C.W, C.H), 0); d = ImageDraw.Draw(m); r = size * 0.5
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=255)
    if pop:
        a = math.radians(ang); q = (p[0] + math.cos(a) * size * 1.0, p[1] - math.sin(a) * size * 1.0)
        d.line([p, q], fill=255, width=int(size * 0.55))
    OBST |= np.asarray(m) > 0


def logo(c, cx, cy, width, rot=3, glow=(255, 200, 130), shadow=0.6):
    """Place the logo at (cx, cy); if any part would touch a reserved shape, nudge it (then shrink it) until it is clear."""
    global OBST
    if OBST is not None and OBST.any():
        q = 4; ob = np.asarray(Image.fromarray(OBST).resize((C.W // q, C.H // q)).convert("L").filter(ImageFilter.MaxFilter(2 * max(1, int(C.H * 0.012 / q)) + 1))) > 0
        la = load(LOGO).getchannel("A"); best = None
        for sc in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6):
            w = width * sc
            m = la.resize((max(1, round(w / q)), max(1, round(la.height * w / la.width / q)))).rotate(rot, expand=True)
            m = np.asarray(m) > 30; mh, mw = m.shape; mar = C.H * 0.02 / q
            for dy in np.arange(-0.16, 0.161, 0.01) * C.H:
                for dx in np.arange(-0.12, 0.121, 0.008) * C.W:
                    x0 = int((cx + dx) / q - mw / 2); y0 = int((cy + dy) / q - mh / 2)
                    if x0 < mar or y0 < mar or x0 + mw > C.W / q - mar or y0 + mh > C.H / q - mar: continue
                    if (ob[y0:y0 + mh, x0:x0 + mw] & m).any(): continue
                    d = math.hypot(dx / C.W, dy / C.H * 1.3)
                    if best is None or d < best[0]: best = (d, cx + dx, cy + dy, w)
            if best: break
        if best:
            if best[0] > 1e-6 or best[3] != width: print("   logo moved %.0f,%.0f  scale %.2f" % (best[1] - cx, best[2] - cy, best[3] / width))
            _, cx, cy, width = best
        else: print("   !! no clear logo spot")
    OBST = None
    c.logo(cx, cy, width, shadow=shadow, glow=glow, rot=rot, path=LOGO)


# ---------- backgrounds ----------
def radial_bg(cw, ch, center, inner, outer, rays=28, ray_a=0.16, power=0.9):
    yy, xx = np.mgrid[0:ch, 0:cw].astype(np.float32)
    cx, cy = center[0] * cw, center[1] * ch
    r = np.clip(np.hypot((xx - cx) / cw, (yy - cy) / cw) / 0.62, 0, 1) ** power
    rgb = np.array(inner, np.float32) + (np.array(outer, np.float32) - np.array(inner, np.float32)) * r[..., None]
    ang = np.arctan2(yy - cy, xx - cx)
    wedge = (np.sin(ang * rays) > 0).astype(np.float32)
    wedge = np.asarray(Image.fromarray((wedge * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(ch / 500))).astype(np.float32) / 255
    rgb = rgb + (255 - rgb) * (wedge * ray_a * np.clip(r * 1.6, 0.15, 1))[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")


def halftone(c, color, a=0.14, step=None, corner=(1, 1)):
    cw, ch = C.W, C.H; step = step or ch // 34
    g = ovl(); d = ImageDraw.Draw(g)
    for j, y in enumerate(range(0, ch + step, step)):
        for x in range(-step, cw + step, step):
            xx = x + (step // 2 if j % 2 else 0)
            t = np.clip(1.35 - math.hypot((xx / cw - corner[0]), (y / ch - corner[1]) * ch / cw) * 2.0, 0, 1)
            r = step * 0.42 * t
            if r > 1: d.ellipse([xx - r, y - r, xx + r, y + r], fill=color + (int(255 * a),))
    c.canvas.alpha_composite(g)


def big_popcorn(c, spots, seed=5):
    """Large out-of-focus kernels in the foreground (depth)."""
    rnd = np.random.default_rng(seed); pieces = sorted(glob.glob("layers/popcorn/*.png"))
    for (fx, fy, fs, blur) in spots:
        P = load(pieces[rnd.integers(len(pieces))]).rotate(rnd.uniform(0, 360), Image.BICUBIC, expand=True)
        w = fs * C.H; P = P.resize((round(w), round(P.height * w / P.width)), Image.LANCZOS)
        if blur: P = P.filter(ImageFilter.GaussianBlur(blur * C.H / 1412))
        c.canvas.alpha_composite(P, (round(fx * C.W - P.width / 2), round(fy * C.H - P.height / 2)))


def finish(c, tag, size, tw, th, **grade):
    c.grade(**{**dict(contrast=1.05, sat=1.06, vignette=0.28, bloom=0.08), **grade})
    os.makedirs(f"{HERE}/out", exist_ok=True)
    c.canvas.convert("RGB").resize((tw, th), Image.LANCZOS).save(f"{HERE}/out/{tag}_{size}_{tw}x{th}.jpg", quality=94)


# ---------- S: round-14 Cappy Solo ----------
def build_S(size, cw, ch):
    c = C.Comp(PLATE, focus=(0.5, 0.62))
    L = {"main": dict(o=(0.705, -0.135, 0.54), cap=(0.524, 0.382, 0.892), lg=(0.3125, 0.283, 0.60)),
         "header": dict(o=(0.74, -0.2, 0.62), cap=(0.60, 0.36, 0.95), lg=(0.31, 0.36, 0.58)),
         "small": dict(o=(0.80, -0.3, 0.7), cap=(0.70, 0.30, 1.15), lg=(0.335, 0.5, 0.64))}[size]
    ox, oy, ow = L["o"]; c.glow(cw * 0.85, ch * 0.25, ch * 0.8, (255, 100, 25), 0.6)
    put_ophelia(c, ox * cw, oy * ch, ow * ch)
    x, y, w = L["cap"]; w *= ch; x *= cw; y *= ch
    im, tip, thr = cappy_img(w, True)
    tracers(c, (x + tip[0], y + tip[1]), 152, ch * 0.7, ch / 160)
    mp = (x + tip[0] - w * 0.015, y + tip[1] - w * 0.005); pop = 6 if size != "small" else 3
    reserve(im, x, y); reserve_muzzle(mp, w * 0.2, 150, pop)
    lx, ly, lw = L["lg"]; logo(c, lx * cw, ly * ch, lw * cw)
    put_cappy(c, x, y, w, flip=True, rim=(255, 160, 80), rim_dir=(1, -1), match=0.12)
    muzzle(c, mp, w * 0.2, 150, pop=pop)
    c.particles(60, (cw * 0.6, ch * 0.1, cw, ch * 0.8), [(255, 170, 60), (255, 220, 120)], size=(ch / 470, ch / 176), seed=4, shape="dot")
    c.particles(40, (0, ch * 0.7, cw, ch), [(200, 255, 150), (150, 240, 255)], size=(ch / 470, ch / 200), seed=8, shape="dot")
    return c, dict(vignette=0.3, bloom=0.1)


# ---------- D: Duel ----------
def build_D(size, cw, ch):
    bg = Image.open(f"{ENV}/Capyverse_Lobby_ (2).png").convert("RGB").filter(ImageFilter.GaussianBlur(2))
    c = C.Comp(bg.convert("RGBA").resize((10, 10)))            # placeholder, replaced below
    s = max(cw / bg.width, ch / bg.height); b2 = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
    x0, y0 = (b2.width - cw) // 2, int((b2.height - ch) * 0.55); b2 = b2.crop((x0, y0, x0 + cw, y0 + ch)).filter(ImageFilter.GaussianBlur(ch / 350))
    a = np.asarray(b2).astype(np.float32) / 255
    a = a * 0.74 * np.array([0.92, 0.85, 1.12])                                   # push to deep night purple
    grad = np.linspace(0, 1, cw)[None, :, None]
    a = a * (1 - grad * 0.35) + grad * 0.35 * np.array([0.42, 0.05, 0.10])        # blood-red toward Ophelia's side
    c.canvas = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    L = {"main": dict(o=(0.62, -0.06, 0.82), cap=(-0.05, 0.43, 0.94), lg=(0.40, 0.185, 0.50), rot=-2),
         "header": dict(o=(0.68, -0.08, 0.86), cap=(-0.03, 0.42, 0.96), lg=(0.42, 0.20, 0.42), rot=-2),
         "small": dict(o=(0.80, -0.12, 0.95), cap=(-0.02, 0.45, 0.95), lg=(0.55, 0.47, 0.46), rot=0)}[size]
    ox, oy, ow = L["o"]
    c.glow(cw * (ox + 0.2), ch * 0.4, ch * 1.3, (255, 40, 60), 0.55)
    c.glow(cw * 0.16, ch * 0.72, ch * 1.2, (255, 170, 60), 0.45)                  # warm pool behind the hero
    put_ophelia(c, ox * cw, oy * ch, ow * ch, fade=False, tint=(1.0, 0.86, 0.9), dim=0.9, alpha=1.0)
    x, y, w = L["cap"]; x *= cw; y *= ch; w *= ch
    im, tip, thr = cappy_img(w)
    p = (x + tip[0], y + tip[1])
    if size != "small":
        tracers(c, p, 12, ch * 0.3, ch / 150, n=5, spread=6)
    mp = (p[0] + w * 0.012, p[1] - w * 0.004); pop = 7 if size != "small" else 0
    reserve(im, x, y); reserve_muzzle(mp, w * 0.19, 14, pop)
    lx, ly, lw = L["lg"]; logo(c, lx * cw, ly * ch, lw * cw, rot=L["rot"], glow=(255, 190, 120))
    put_cappy(c, x, y, w, rim=(255, 120, 110), rim_dir=(1, -1), match=0.1)
    muzzle(c, mp, w * 0.19, 14, pop=pop)
    c.particles(70, (cw * 0.3, 0, cw, ch), [(255, 120, 60), (255, 200, 120)], size=(ch / 470, ch / 190), seed=4, shape="dot")
    return c, dict(vignette=0.34, bloom=0.12, contrast=1.08)


# ---------- Q: Squad Burst ----------
def build_Q(size, cw, ch):
    L = {"main": dict(burst=(0.66, 0.28), lg=(0.66, 0.245, 0.60), cap=(0.16, 0.49, 0.98),
                      sq=[("jim", 0.05, 0.10, 0.36), ("moody", 0.015, 0.33, 0.50), ("axie", -0.01, 0.64, 0.40)]),
         "header": dict(burst=(0.68, 0.28), lg=(0.69, 0.25, 0.52), cap=(0.17, 0.49, 0.98),
                        sq=[("jim", 0.045, 0.07, 0.38), ("moody", 0.01, 0.31, 0.52), ("axie", -0.01, 0.64, 0.42)]),
         "small": dict(burst=(0.64, 0.5), lg=(0.64, 0.5, 0.58), cap=(-0.01, 0.42, 0.95),
                       sq=[])}[size]
    c = C.Comp(radial_bg(cw, ch, L["burst"], (255, 232, 70), (242, 96, 14), rays=26, ray_a=0.2))
    halftone(c, (255, 250, 200), a=0.13, corner=(0, 1))
    c.glow(L["burst"][0] * cw, L["burst"][1] * ch, ch * 1.1, (255, 255, 220), 0.5)
    c.speed_lines(L["burst"][0] * cw, L["burst"][1] * ch, n=70, inner=0.3, color=(255, 255, 255), opacity=0.16, width=ch / 200, seed=3)
    for kind, fx, fy, fw in L["sq"]: hero(c, kind, fx * cw, fy * ch, fw * ch)
    x, y, w = L["cap"]; x *= cw; y *= ch; w *= ch
    im, tip, thr = cappy_img(w); mp = (x + tip[0] + w * 0.012, y + tip[1] - w * 0.004)
    reserve(im, x, y)
    if size != "small": reserve_muzzle(mp, w * 0.16, 16, 7)
    for kind, fx, fy, fw in L["sq"]:      # squad boxes (incl. Jim's confetti and the disco flares)
        hw = fw * ch; reserve(Image.new("RGBA", (round(hw * 1.25), round(hw * 0.8)), (0, 0, 0, 255)), fx * cw, fy * ch - hw * 0.08)
    lx, ly, lw = L["lg"]; logo(c, lx * cw, ly * ch, lw * cw, rot=-3, glow=(255, 255, 230), shadow=0.5)
    put_cappy(c, x, y, w, rim=(255, 250, 210), match=0.04)
    if size != "small":
        muzzle(c, mp, w * 0.16, 16, pop=7)
        big_popcorn(c, [(0.94, 0.82, 0.17, 5), (0.80, 0.94, 0.11, 3), (0.99, 0.56, 0.08, 2), (0.86, 0.66, 0.05, 0)])
    return c, dict(vignette=0.16, bloom=0.05, contrast=1.04, sat=1.08)


# ---------- U: Close-Up ----------
def build_U(size, cw, ch):
    L = {"main": dict(c0=(0.68, 0.62), lg=(0.295, 0.29, 0.53), cap=(0.42, 0.34, 1.42)),
         "header": dict(c0=(0.70, 0.62), lg=(0.30, 0.34, 0.54), cap=(0.46, 0.27, 1.55)),
         "small": dict(c0=(0.75, 0.6), lg=(0.33, 0.5, 0.62), cap=(0.62, 0.16, 1.9))}[size]
    c = C.Comp(radial_bg(cw, ch, L["c0"], (70, 225, 205), (8, 78, 112), rays=22, ray_a=0.10))
    halftone(c, (180, 255, 240), a=0.10, corner=(0, 0))
    c.glow(L["c0"][0] * cw, L["c0"][1] * ch, ch * 1.2, (200, 255, 235), 0.4)
    x, y, w = L["cap"]; x *= cw; y *= ch; w *= ch
    im, tip, thr = cappy_img(w, True)
    p = (x + tip[0], y + tip[1])
    tracers(c, p, 155, ch * 0.9, ch / 130, n=5, spread=5)
    mp = (p[0] - w * 0.012, p[1] - w * 0.004)
    reserve(im, x, y); reserve_muzzle(mp, w * 0.15, 152, 0)
    lx, ly, lw = L["lg"]; logo(c, lx * cw, ly * ch, lw * cw, rot=3, glow=(220, 255, 240), shadow=0.55)
    put_cappy(c, x, y, w, flip=True, rim=(200, 255, 240), rim_dir=(-1, -1), match=0.03, flame=False)
    muzzle(c, mp, w * 0.15, 152, pop=0)
    if size != "small":
        big_popcorn(c, [(0.05, 0.86, 0.20, 6), (0.21, 0.95, 0.13, 3), (0.36, 0.80, 0.085, 1), (0.13, 0.66, 0.06, 0), (0.44, 0.93, 0.07, 1), (0.30, 0.66, 0.045, 0)], seed=9)
    else:
        big_popcorn(c, [(0.04, 0.85, 0.3, 4), (0.56, 0.9, 0.2, 2)], seed=9)
    return c, dict(vignette=0.22, bloom=0.05, contrast=1.05, sat=1.08)


BUILD = {"S": build_S, "D": build_D, "Q": build_Q, "U": build_U}

if __name__ == "__main__":
    tags = [a for a in sys.argv[1:] if a in BUILD] or list(BUILD)
    sizes = [a for a in sys.argv[1:] if a in SIZES] or list(SIZES)
    for t in tags:
        for sz in sizes:
            tw, th, k = SIZES[sz]; C.W, C.H = tw * k, th * k
            c, g = BUILD[t](sz, C.W, C.H)
            finish(c, t, sz, tw, th, **g)
            print(t, sz)
