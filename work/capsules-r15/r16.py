"""Round 16: three hero-vs-enemy face-offs. Heroes big on the left (Cappy in the lower-left corner), the round-10 enemy
crew on the right (worm + bandits, golfer, clown pins), giant Ophelia behind, ground + sky environment, logo as big as
the clear space allows (auto-placed so nothing touches it).

python3 r16.py [A B C]  ->  out16/
"""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r15")
import r15
from r15 import *

V1 = "/home/user/capyverse-claude/work/capsules-v1"


def bg(path, focus=(0.5, 0.5), blur=0, mul=1.0, tint=(1, 1, 1)):
    c = C.Comp(path, focus=focus)
    if blur: c.canvas = c.canvas.filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(c.canvas).astype(np.float32); a[..., :3] = np.clip(a[..., :3] * mul * np.array(tint), 0, 255)
    c.canvas = Image.fromarray(a.astype(np.uint8)); return c


def shadow(c, cx, gy, w, a=150):
    g = ovl(); d = ImageDraw.Draw(g)
    d.ellipse([cx - w / 2, gy - w * 0.07, cx + w / 2, gy + w * 0.07], fill=(15, 8, 25, a))
    c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(w * 0.05)))


def enemy(c, src, x, bottom, height, rim, flip=False, res=True, match=0.12):
    im = load(src); k = height / im.height; im = im.resize((round(im.width * k), round(height)), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    y = bottom - im.height
    shadow(c, x + im.width / 2, bottom - height * 0.02, im.width * 0.9)
    c.place("enemy", x, y, scale=1.0, src=im, match=match, wrap=0.3, rim=dict(color=rim, dir=(1, -1), width=max(3, height / 130), strength=0.6))
    if res: reserve(im, x, y)
    return im


def crew(c, x0, bottom, s, rim, pins=3):
    """Worm + bandits, golfer, clown pins; x0 = left edge of the worm, s = scale in canvas heights."""
    ch = C.H
    enemy(c, "layers/H_worm_bandits.png", x0, bottom, 0.60 * s * ch, rim)
    for i in range(pins):
        enemy(c, "layers/L_pin.png", x0 + (0.47 + 0.115 * i) * s * ch + 0.16 * s * ch, bottom - (0.012 * (i % 2)) * ch, (0.30 + 0.02 * (i % 2)) * s * ch, rim)
    enemy(c, "layers/H_golfer.png", x0 + 0.36 * s * ch, bottom + 0.01 * ch, 0.47 * s * ch, rim)


def squad(c, items, rim):
    for kind, fx, fy, fw in items:
        hw = fw * C.H
        reserve(Image.new("RGBA", (round(hw * 1.2), round(hw * 0.78)), (0, 0, 0, 255)), fx * C.W, fy * C.H - hw * 0.06)
        hero(c, kind, fx * C.W, fy * C.H, hw, rim=rim)


def reserve_squad(items):
    for kind, fx, fy, fw in items:
        hw = fw * C.H
        top = {"jim": 0.02, "moody": 0.12, "axie": 0.0}[kind]      # room above for the disco flares
        reserve(Image.new("RGBA", (round(hw * 1.1), round(hw * (0.6 + top))), (0, 0, 0, 255)), fx * C.W, fy * C.H - hw * top)


def cappy_front(c, fx, fy, fw, rim, ang=16):
    x, y, w = fx * C.W, fy * C.H, fw * C.H
    im, tip, thr = cappy_img(w); mp = (x + tip[0] + w * 0.012, y + tip[1] - w * 0.004)
    reserve(im, x, y); reserve_muzzle(mp, w * 0.17, ang, 6)
    return lambda: (put_cappy(c, x, y, w, rim=rim, match=0.08), muzzle(c, mp, w * 0.17, ang, pop=6))


def ophelia_res(c, fx, fy, fw, **kw):
    O, _ = ophelia_img(fw * C.H, **kw); reserve(O, fx * C.W, fy * C.H)
    put_ophelia(c, fx * C.W, fy * C.H, fw * C.H, **kw)


# A — night meadow: fire-lit Ophelia fading into the sky (as round 14), logo top-left
def build_A():
    cw, ch = C.W, C.H
    c = C.Comp(r15.PLATE, focus=(0.5, 0.62))
    c.glow(cw * 0.84, ch * 0.25, ch * 0.9, (255, 100, 25), 0.6)
    ophelia_res(c, 0.645, -0.07, 0.64)
    rim = (255, 160, 90)
    draw_cappy = cappy_front(c, 0.085, 0.625, 0.80, rim)
    items = [("jim", 0.01, 0.505, 0.31), ("moody", 0.155, 0.50, 0.40), ("axie", -0.005, 0.70, 0.34)]
    reserve_squad(items)
    crew(c, 0.60 * cw, 0.985 * ch, 0.78, rim)
    logo(c, 0.322 * cw, 0.245 * ch, 0.625 * cw)
    for kind, fx, fy, fw in items: hero(c, kind, fx * cw, fy * ch, fw * ch, rim=rim)
    draw_cappy()
    c.particles(60, (cw * 0.55, ch * 0.1, cw, ch * 0.8), [(255, 170, 60), (255, 220, 120)], size=(ch / 470, ch / 176), seed=4, shape="dot")
    return c, dict(vignette=0.3, bloom=0.1)


# B — desert canyon: biggest logo; Ophelia looms on the horizon behind her crew, fading into the dust
def build_B():
    cw, ch = C.W, C.H
    c = bg(f"{V1}/plates/04_desert_nbp_0.png", focus=(0.5, 0.55), blur=2)
    rim = (255, 235, 190)
    c.glow(cw * 0.87, ch * 0.42, ch * 0.8, (255, 225, 170), 0.5)
    ophelia_res(c, 0.79, 0.13, 0.50, tint=(1.0, 0.90, 0.80), dim=0.93, alpha=0.97)
    draw_cappy = cappy_front(c, 0.05, 0.64, 0.82, rim)
    items = [("jim", 0.005, 0.53, 0.31), ("moody", 0.135, 0.535, 0.40), ("axie", -0.01, 0.73, 0.34)]
    reserve_squad(items)
    crew(c, 0.645 * cw, 0.99 * ch, 0.74, rim)
    logo(c, 0.39 * cw, 0.25 * ch, 0.72 * cw, rot=-2, glow=(255, 250, 220), shadow=0.6)
    for kind, fx, fy, fw in items: hero(c, kind, fx * cw, fy * ch, fw * ch, rim=rim)
    draw_cappy()
    return c, dict(vignette=0.2, bloom=0.06, contrast=1.05)


# C — carnival night: Ophelia towers over the fairground, logo top-left
def build_C():
    cw, ch = C.W, C.H
    c = bg(f"{V1}/plates/05_carnival_nbp_0.png", focus=(0.5, 0.5), blur=2.5, mul=0.92)
    c.glow(cw * 0.82, ch * 0.3, ch * 0.9, (255, 60, 120), 0.4)
    rim = (255, 170, 220)
    ophelia_res(c, 0.655, -0.06, 0.62, tint=(1.0, 0.86, 0.95), dim=0.95, alpha=0.97)
    draw_cappy = cappy_front(c, 0.14, 0.64, 0.76, rim)
    items = [("axie", 0.0, 0.51, 0.33), ("jim", 0.19, 0.505, 0.30), ("moody", -0.005, 0.69, 0.42)]
    reserve_squad(items)
    crew(c, 0.61 * cw, 0.97 * ch, 0.76, rim)
    logo(c, 0.33 * cw, 0.245 * ch, 0.635 * cw, rot=-2, glow=(255, 200, 230))
    for kind, fx, fy, fw in items: hero(c, kind, fx * cw, fy * ch, fw * ch, rim=rim)
    draw_cappy()
    c.particles(50, (0, 0, cw, ch * 0.6), [(255, 220, 120), (255, 150, 220), (150, 220, 255)], size=(ch / 470, ch / 200), seed=6, shape="dot")
    return c, dict(vignette=0.3, bloom=0.12)


B16 = {"A": build_A, "B": build_B, "C": build_C}

if __name__ == "__main__":
    for t in ([a for a in sys.argv[1:] if a in B16] or list(B16)):
        C.W, C.H = 2464, 1412; r15.OBST = None
        c, g = B16[t]()
        c.grade(**{**dict(contrast=1.05, sat=1.06, vignette=0.28, bloom=0.08), **g})
        os.makedirs(f"{HERE}/out16", exist_ok=True)
        c.canvas.convert("RGB").resize((1232, 706), Image.LANCZOS).save(f"{HERE}/out16/{t}_main_1232x706.jpg", quality=94)
        print(t)
