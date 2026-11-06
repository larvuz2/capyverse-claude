"""Round 13: round-12 logo + plate kept as is. Cappy = the round-11 2D Unreal render (not the new 3D model), BIG in the
lower-right corner. Jim = 3D model. Moody (3D) and Axie (2D) small and hazy in the background.

python3 r13.py [1_far_squad 2_diagonal 3_jim_front]  ->  out/
"""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r12")
import r12
from r12 import *
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageEnhance

SKY = np.array([70, 55, 115], np.float32)


def haze(im, h, blur=0.0):
    """Atmospheric perspective: lower contrast, tint toward the night sky, optional softness."""
    a = np.asarray(im).astype(np.float32)
    a[..., :3] = a[..., :3] * (1 - h) + SKY * h
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return out.filter(ImageFilter.GaussianBlur(blur)) if blur else out


def ophelia(c):
    O = fit(load("layers/H_ophelia_head.png"), 760)
    oa = np.asarray(O).astype(np.float32); hh = O.height
    red = (oa[..., 0] > 150) & (oa[..., 1] < 70) & (oa[..., 2] < 70) & (oa[..., 3] > 200); red[: int(hh * 0.3)] = False
    lab, n = ndimage.label(red); sz = ndimage.sum(red, lab, range(1, n + 1))
    eyes = [ndimage.center_of_mass(red, lab, i + 1) for i in np.argsort(sz)[-2:]]
    fade = np.clip((np.linspace(1, 0, hh) - 0.12) / 0.4, 0, 1) ** 1.3
    oa[..., 3] *= fade[:, None] * 0.9; oa[..., :3] = oa[..., :3] * np.array([0.95, 0.78, 0.72]) * 0.85
    O = Image.fromarray(np.clip(oa, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    ox, oy = 1740, -190
    c.glow(2100, 330, 1150, (255, 100, 25), 0.6)
    c.canvas.alpha_composite(O, (ox, oy))
    for ey, ex in eyes: c.glow(ox + ex, oy + ey, 90, (255, 30, 30), 0.85)


def moody_bg(c, x, bottom, width, h, ray=True):
    MO, _ = hero3d("moody", width); MO = haze(shade_shadow(MO), h, 0.6)
    my = bottom - MO.height
    gm = np.asarray(Image.open(f"{D12}/gear/mask_moody.png")) > 0; bbm = Image.open(f"{D12}/renders/moody_gear.png").getbbox()
    km = MO.width / (bbm[2] - bbm[0]); ys, xs = np.nonzero(gm); top = ys < ys.min() + (ys.max() - ys.min()) * 0.35
    i = np.argmin(np.where(top, xs, 99999)); tx, ty = x + (xs[i] - bbm[0]) * km, my + (ys[i] - bbm[1]) * km
    if ray: beam(c, (tx + 6, ty + 4), (max(-150, tx - 900), ty + 120), 40 * width / 480, 230 * width / 480)
    put(c, MO, x, my, rim=dict(color=(255, 160, 90), dir=(1, -1), width=4, strength=0.4), match=0.25)
    c.glow(tx + 6, ty + 4, 130 * width / 480, (255, 230, 255), 0.8)


def axie_bg(c, x, bottom, width, h):
    A = haze(fit(clean(f"{D11}/cut_axie_stand_0.png", flip=True), width), h, 0.6)
    contact(c, x + width * 0.52, bottom + 2, width * 0.9, 120)
    c.place("axie", x, bottom - A.height, scale=1.0, src=A, match=0.3, wrap=0.45, bright=0.92,
            rim=dict(color=(255, 140, 70), dir=(1, -1), width=5, strength=0.6))


def jim3d(c, x, bottom, width, h=0.0):
    JI, _ = hero3d("jim", width); JI = shade_shadow(JI)
    if h: JI = haze(JI, h, 0.4)
    put(c, JI, x, bottom - JI.height + 30 * width / 480, rim=dict(color=(255, 160, 90), dir=(1, -1), width=6, strength=0.5))


def cappy2d(c, x, y, width):
    """The round-11 Cappy: Unreal render H_cappy, flipped to face left, with belt flame + gatling fire."""
    S = width / 2315; k = 2315 / 1029
    Cp = load("layers/H_cappy.png"); Cp = Cp.resize((round(width), round(Cp.height * S)), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    gx, gy = C.PROPS["cappy_gatling"]; mzx, mzy = x + (2315 - gx * k) * S, y + gy * k * S
    return Cp, (mzx, mzy)


def cappy_draw(c, Cp, x, y, width, muzzle):
    S = width / 2315; k = 2315 / 1029
    c.place("cappy", x, y, scale=1.0, src=Cp, match=0.12, wrap=0.3, rim=dict(color=(255, 160, 80), dir=(1, -1), width=10, strength=0.7))
    tx, ty, ang = C.THRUSTERS["cappy"][0]
    fx, fy = x + (2315 - tx * k) * S, y + ty * k * S
    c.flame(fx, fy, 180 - ang, 190 * S * 2.25 * 2.0, 50 * S * 2.25 * 1.7); c.glow(fx, fy, 260 * S * 2.25, (255, 170, 80), 0.6)
    mzx, mzy = muzzle
    sparkle(c, mzx - 20, mzy, 300, (255, 230, 150), 1.0, rot=10)
    c.glow(mzx - 20, mzy, 300, (255, 180, 60), 0.9)


ARR = {
    # Cappy big lower-right; Jim running mid-ground; Moody + Axie tiny on the far meadow under the logo
    "1_far_squad": dict(cappy=(1290, 540, 1260), jim=(820, 1210, 400, 0.0),
                        moody=(170, 935, 230, 0.38), axie=(560, 925, 220, 0.38)),
    # the squad recedes on a diagonal behind Cappy toward the left horizon
    "2_diagonal": dict(cappy=(1290, 540, 1260), jim=(640, 1330, 440, 0.0),
                       moody=(60, 900, 200, 0.45), axie=(330, 1010, 260, 0.25)),
    # Jim in the foreground lower-left balancing Cappy; Moody + Axie far between them
    "3_jim_front": dict(cappy=(1290, 540, 1260), jim=(60, 1440, 520, 0.0),
                        moody=(700, 1010, 210, 0.42, False), axie=(980, 985, 230, 0.35)),
}


def build13(name):
    a = ARR[name]
    c = Comp(f"{D11}/plate_nb_0.png")
    ophelia(c)
    cx, cy, cw = a["cappy"]
    Cp, mz = cappy2d(c, cx, cy, cw)
    tracers(c, mz, 158)
    c.logo(770, 400, 1480, shadow=0.6, glow=(255, 200, 130), rot=3, path=r11.LOGO)     # same logo as round 12
    m, ax, j = a["moody"], a["axie"], a["jim"]
    # far to near
    for kind, p in sorted([("moody", m), ("axie", ax)], key=lambda t: t[1][1]):
        (moody_bg if kind == "moody" else axie_bg)(c, *p)
    jim3d(c, *j)
    cappy_draw(c, Cp, cx, cy, cw, mz)
    c.particles(70, (1500, 200, 2464, 1100), [(255, 170, 60), (255, 220, 120)], size=(3, 8), seed=4, shape="dot")
    c.particles(45, (0, 1000, 2464, 1400), [(200, 255, 150), (150, 240, 255)], size=(3, 7), seed=8, shape="dot")
    c.grade(contrast=1.05, sat=1.06, vignette=0.3, bloom=0.1)
    c.save(f"r13_{name}", f"{D12}/out13")


if __name__ == "__main__":
    for n in (sys.argv[1:] or ARR): build13(n)
