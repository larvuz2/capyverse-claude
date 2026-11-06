"""Round 11: Gus's reference composition (ref_composition.jpg) rebuilt with real project assets + the Tin hanging logo.

Reference layout (fractions of the frame):
  logo      left third, x .02-.42, y .28-.63, slightly tilted
  Cappy     centre, big (~32% wide), flying left, gatling firing up-left (muzzle flash + tracers over the logo)
  Moody     on the ground under the logo's right end, small, disco cannon firing a rainbow beam to the left
  Jim       ground, lower right, playful
  Axie      standing behind Jim, far right
  Ophelia   huge looming head in the sky, top right, lit by an orange fire glow
  world     starry purple night sky, orange glow upper right, meadow with glowing mushrooms, popcorn everywhere
Only the background plate is AI (painted empty). Characters are the project renders, cut out, never re-generated.
"""
import sys, os, math
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
import compose as C
from compose import *
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

D = "/home/user/capyverse-claude/work/capsules-r11"
LOGO = "/home/user/capyverse-claude/work/logo-tin/tin_hanging.png"
W, H = C.W, C.H


def clean(path, flip=False):
    """Cutout -> keep only the main body (drops sheet labels), trimmed to its bbox."""
    im = Image.open(path).convert("RGBA"); a = np.asarray(im)[..., 3] > 30
    lab, n = ndimage.label(ndimage.binary_dilation(a, iterations=4))
    big = 1 + np.argmax(ndimage.sum(a, lab, range(1, n + 1)))
    arr_ = np.asarray(im).copy(); arr_[..., 3] = np.where(lab == big, arr_[..., 3], 0)
    im = Image.fromarray(arr_); im = im.crop(im.getbbox())
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


def fit(im, width):
    return im.resize((round(width), round(im.height * width / im.width)), Image.LANCZOS)


def ovl(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def contact(c, cx, gy, w, a=150):
    g = ovl(); d = ImageDraw.Draw(g)
    d.ellipse([cx - w / 2, gy - w * 0.08, cx + w / 2, gy + w * 0.08], fill=(10, 5, 25, a))
    c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(w * 0.05)))


def beam(c, p0, p1, w0, w1):
    """Rainbow beam from the disco cannon (p0) widening toward p1."""
    cols = [(255, 70, 90), (255, 160, 40), (255, 235, 60), (90, 230, 110), (70, 190, 255), (180, 110, 255)]
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    g = ovl(); d = ImageDraw.Draw(g)
    for i, col in enumerate(cols):
        a0 = (i / len(cols) - 0.5) * w0, ((i + 1) / len(cols) - 0.5) * w0
        a1 = (i / len(cols) - 0.5) * w1, ((i + 1) / len(cols) - 0.5) * w1
        d.polygon([(x0 + nx * a0[0], y0 + ny * a0[0]), (x0 + nx * a0[1], y0 + ny * a0[1]),
                   (x1 + nx * a1[1], y1 + ny * a1[1]), (x1 + nx * a1[0], y1 + ny * a1[0])], fill=col + (235,))
    # fade toward the far end
    m = Image.new("L", (W, H), 0); md = ImageDraw.Draw(m)
    for k in range(40):
        t = k / 40; md.line([(x0 + (x1 - x0) * t - nx * w1, y0 + (y1 - y0) * t - ny * w1),
                             (x0 + (x1 - x0) * t + nx * w1, y0 + (y1 - y0) * t + ny * w1)], fill=int(255 * (1 - t) ** 0.7), width=int(L / 38) + 4)
    g.putalpha(Image.fromarray((np.asarray(g.getchannel("A")).astype(np.float32) * np.asarray(m.filter(ImageFilter.GaussianBlur(20))) / 255).astype(np.uint8)))
    c.screen(g.filter(ImageFilter.GaussianBlur(10)))
    c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).point(lambda v: v) if False else g.filter(ImageFilter.GaussianBlur(3)))
    core = ovl(); cd = ImageDraw.Draw(core)
    cd.line([p0, (x0 + (x1 - x0) * 0.6, y0 + (y1 - y0) * 0.6)], fill=(255, 255, 255, 200), width=int(w0 * 0.35))
    c.screen(core.filter(ImageFilter.GaussianBlur(12)))
    c.glow(x0, y0, w0 * 2.2, (255, 240, 255), 0.9)


def tracers(c, p0, ang, n=5, seed=3):
    """Glowing popcorn tracer streaks leaving the gatling."""
    rnd = np.random.default_rng(seed); g = ovl(); d = ImageDraw.Draw(g)
    for i in range(n):
        a = math.radians(ang + rnd.uniform(-5, 5)); r0 = rnd.uniform(80, 260); r1 = r0 + rnd.uniform(500, 1000)
        x0, y0 = p0[0] + math.cos(a) * r0, p0[1] - math.sin(a) * r0
        x1, y1 = p0[0] + math.cos(a) * r1, p0[1] - math.sin(a) * r1
        for wdt, col in ((26, (255, 150, 40, 150)), (9, (255, 240, 170, 255))):
            d.line([(x0, y0), (x1, y1)], fill=col, width=wdt)
    c.screen(g.filter(ImageFilter.GaussianBlur(6)))
    c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(1.5)).point(lambda v: v // 2) if False else ovl())


def build(name, plate, ophelia_a=0.9):
    c = Comp(f"{D}/{plate}")
    # --- Ophelia looming in the sky (behind everything), lit by the fire glow
    O = fit(load("layers/H_ophelia_head.png"), 760)
    oa = np.asarray(O).astype(np.float32); hh = O.height
    red = (oa[..., 0] > 150) & (oa[..., 1] < 70) & (oa[..., 2] < 70) & (oa[..., 3] > 200)
    red[: int(hh * 0.3)] = False                                                  # skip the crown jewels
    lab, n = ndimage.label(red); sz = ndimage.sum(red, lab, range(1, n + 1))
    eyes = [ndimage.center_of_mass(red, lab, i + 1) for i in np.argsort(sz)[-2:]]
    fade = np.clip((np.linspace(1, 0, hh) - 0.12) / 0.4, 0, 1) ** 1.3             # dissolve her neck into the sky
    oa[..., 3] *= fade[:, None] * ophelia_a
    oa[..., :3] = oa[..., :3] * np.array([0.95, 0.78, 0.72]) * 0.85                # darker, warmed by the fire
    O = Image.fromarray(np.clip(oa, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    ox, oy = 1720, -170
    c.glow(2100, 330, 1150, (255, 100, 25), 0.6)
    c.canvas.alpha_composite(O, (ox, oy))
    for ey, ex in eyes: c.glow(ox + ex, oy + ey, 90, (255, 30, 30), 0.85)
    sparkle(c, ox + 0.5 * O.width, oy + 0.17 * hh, 150, (255, 240, 200), 0.9, rot=15)

    # --- logo, big on the left, slight tilt like the reference
    c.logo(560, 640, 1050, shadow=0.6, glow=(255, 200, 130), rot=3, path=LOGO)

    # --- Moody on the ground under the logo's right end, firing a rainbow beam left
    M = fit(clean(f"{D}/cut_moody_34_0.png"), 470)
    mx, my = 820, 1250 - M.height
    contact(c, mx + 250, 1255, 430)
    ma = np.asarray(M)[..., 3] > 40; rows = np.nonzero(ma.any(1))[0]
    top = ma[: int(M.height * 0.35)]; xs = np.nonzero(top.any(0))[0]; tipx = xs.min(); tipy = np.nonzero(top[:, tipx])[0].mean()
    beam(c, (mx + tipx + 10, my + tipy), (-80, my + tipy + 160), 34, 210)
    c.place("moody", mx, my, scale=1.0, src=M, match=0.18, wrap=0.35, rim=dict(color=(255, 170, 110), dir=(1, -1), width=6, strength=0.6))
    c.glow(mx + tipx + 10, my + tipy, 120, (255, 230, 255), 0.8)

    # --- Axie standing far right, Jim in front of him
    A = fit(clean(f"{D}/cut_axie_stand_0.png", flip=True), 520)
    ax, ay = 1930, 1230 - A.height
    contact(c, ax + 270, 1232, 470)
    c.place("axie", ax, ay, scale=1.0, src=A, match=0.2, wrap=0.35, rim=dict(color=(255, 150, 80), dir=(1, -1), width=7, strength=0.7))
    J = fit(clean(f"{D}/cut_jim_side_0.png", flip=True), 470)
    jx, jy = 1600, 1370 - J.height
    contact(c, jx + 240, 1372, 430, 170)
    c.place("jim", jx, jy, scale=1.0, src=J, match=0.18, wrap=0.35, rim=dict(color=(255, 160, 90), dir=(1, -1), width=6, strength=0.6))
    ja = np.asarray(J)[..., 3] > 40; top = ja[: int(J.height * 0.3)]; xs = np.nonzero(top.any(0))[0]
    bx, by = jx + xs.max(), jy + np.nonzero(top[:, xs.max()])[0].mean()       # trumpet bell (points back/right)
    pass

    # --- Cappy, big in the centre, flying left; gatling fires up-left over the logo
    S = 900 / 2315
    Cp = load("layers/H_cappy.png"); Cp = Cp.resize((900, round(Cp.height * S)), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    cx_, cy_ = 1010, 250
    c.place("cappy", cx_, cy_, scale=1.0, src=Cp, match=0.12, wrap=0.3,
            rim=dict(color=(255, 160, 80), dir=(1, -1), width=8, strength=0.7),
            trail=dict(length=220, color=(255, 230, 200), opacity=0.12, angle=-10))
    k = 2315 / 1029
    tx, ty, ang = C.THRUSTERS["cappy"][0]
    fx, fy = cx_ + (2315 - tx * k) * S, cy_ + ty * k * S
    c.flame(fx, fy, 180 - ang, 190 * 2.6, 50 * 2.2); c.glow(fx, fy, 160, (255, 170, 80), 0.7)
    gx, gy = C.PROPS["cappy_gatling"]
    mzx, mzy = cx_ + (2315 - gx * k) * S, cy_ + gy * k * S
    tracers(c, (mzx, mzy), 165)
    sparkle(c, mzx - 20, mzy, 260, (255, 230, 150), 1.0, rot=10)
    c.glow(mzx - 20, mzy, 260, (255, 180, 60), 0.9)
    popcorn_burst(c, mzx - 40, mzy + 10, 1.1, angle=175, n=12, dist=520)
    pass

    # --- atmosphere: embers drifting up from the fire side, fireflies over the meadow
    c.particles(70, (1500, 200, 2464, 1100), [(255, 170, 60), (255, 220, 120)], size=(3, 8), seed=4, shape="dot")
    c.particles(45, (0, 950, 2464, 1400), [(200, 255, 150), (150, 240, 255)], size=(3, 7), seed=8, shape="dot")
    c.grade(contrast=1.05, sat=1.06, vignette=0.32, bloom=0.12)
    c.save(f"r11_{name}", f"{D}/out")


if __name__ == "__main__":
    TAKES = {"A_meadow": "plate_nb_0.png", "B_milkyway": "plate_nb_1.png", "C_vivid": "plate_gpt_0.png"}
    for n in (sys.argv[1:] or TAKES): build(n, TAKES[n])
