"""Round 14: no 3D models. Cappy = the round-11/13 Unreal render (H_cappy), big in the lower-right corner, muzzle flash
fixed on the real barrel tip. Moody, Jim and Axie re-posed FLYING with gpt-image-2.5 edit from their real images
(p_*.txt), cut with BiRefNet. Same plate + logo as rounds 12/13.

python3 r14.py [1_wingmen 2_depth 3_diagonal]  ->  out/
"""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r12")
import r13
from r13 import *
import numpy as np
from PIL import Image, ImageFilter

D14 = "/home/user/capyverse-claude/work/capsules-r14"
CUT = {"axie": "cut_axie_1_0.png", "jim": "cut_jim_0_0.png", "moody": "cut_moody_0_0.png"}
TIP = (2055, 95)
THR = {"axie": [(0.62, 0.36), (0.57, 0.24)], "jim": [(0.61, 0.33)], "moody": [(0.69, 0.35), (0.68, 0.25)]}          # gatling muzzle in H_cappy pixels (measured on the image)


def flyer(c, kind, x, y, width, h=0.0, rim=(255, 160, 80)):
    im = Image.open(f"{D14}/{CUT[kind]}").convert("RGBA"); im = im.crop(im.getbbox())
    k = width / im.width; im = im.resize((round(width), round(im.height * k)), Image.LANCZOS)
    a = np.asarray(im).astype(np.int32)
    # the jet flames GPT drew: hot orange pixels -> re-light them with real flames
    hot = (a[..., 0] > 225) & (a[..., 1] > 110) & (a[..., 1] < 215) & (a[..., 2] < 140) & (a[..., 3] > 100)
    if h: im = haze(im, h, 0.5)
    c.place(kind, x, y, scale=1.0, src=im, match=0.18 + h * 0.3, wrap=0.35,
            rim=dict(color=rim, dir=(1, -1), width=7, strength=0.7),
            trail=dict(length=width * 0.55, color=(255, 240, 225), opacity=0.1, angle=8))
    for fx, fy in THR[kind]:                     # thruster exits measured on the cutouts (fractions of width)
        px, py = x + fx * width, y + fy * width
        c.flame(px, py, -6, width * 0.45, width * 0.085); c.glow(px, py, width * 0.17, (255, 170, 80), 0.55)
    if kind == "moody":   # disco sparkle on the ball (top-right part of the gear)
        ys, xs = np.nonzero(a[..., 3] > 128); topy = ys.min()
        row = np.nonzero(a[topy + int(width * 0.05), :, 3] > 128)[0]
        disco_flares(c, x + row.mean(), y + topy + width * 0.06, width / 500, seed=9)
    return (x, y, x + im.width, y + im.height)


def cappy(c, x, y, width):
    S = width / 2315
    Cp = load("layers/H_cappy.png"); Cp = Cp.resize((round(width), round(Cp.height * S)), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    mz = (x + (2315 - TIP[0]) * S, y + TIP[1] * S)
    return Cp, mz


def cappy_fx(c, Cp, x, y, width, mz):
    S = width / 2315; k = 2315 / 1029
    c.place("cappy", x, y, scale=1.0, src=Cp, match=0.12, wrap=0.3, rim=dict(color=(255, 160, 80), dir=(1, -1), width=10, strength=0.7))
    tx, ty, ang = C.THRUSTERS["cappy"][0]
    fx, fy = x + (2315 - tx * k) * S, y + ty * k * S
    c.flame(fx, fy, 180 - ang, 190 * S * 2.25 * 2.0, 50 * S * 2.25 * 1.7); c.glow(fx, fy, 260 * S * 2.25, (255, 170, 80), 0.6)
    # muzzle flash ON the barrel tip, pointing out along the barrel (up-left)
    c.glow(mz[0] - 15, mz[1] - 5, 230, (255, 190, 80), 0.95)
    sparkle(c, mz[0] - 25, mz[1] - 8, 280, (255, 235, 160), 1.0, rot=12)
    popcorn_burst(c, mz[0] - 40, mz[1] - 10, 0.9, angle=150, n=6, dist=260, flare=False, seed=3)


ARR = {
    # tight staggered V right in front of Cappy, under the logo
    "1_wingmen": [("jim", 80, 720, 520, 0.0), ("moody", 640, 900, 500, 0.0), ("axie", 60, 1075, 560, 0.0)],
    # depth: Jim big and close lower-left, Moody mid, Axie small and far
    "2_depth": [("axie", 980, 760, 300, 0.3), ("moody", 560, 830, 420, 0.12), ("jim", 30, 950, 640, 0.0)],
    # diagonal: the squad streams down from the logo's right end toward the lower-left, growing as it nears the camera
    "3_diagonal": [("axie", 1000, 745, 330, 0.25), ("moody", 600, 880, 430, 0.1), ("jim", 90, 1030, 560, 0.0)],
    # Cappy alone: same frame as the others with the three heroes removed
    "4_solo": [],
}


def build14(name):
    c = Comp(f"{D11}/plate_nb_0.png")
    ophelia(c)
    cx, cy, cw = 1290, 540, 1260
    Cp, mz = cappy(c, cx, cy, cw)
    tracers(c, mz, 152)
    c.logo(770, 400, 1480, shadow=0.6, glow=(255, 200, 130), rot=3, path=r11.LOGO)
    for kind, x, y, w, h in ARR[name]:
        flyer(c, kind, x, y, w, h)
    cappy_fx(c, Cp, cx, cy, cw, mz)
    c.particles(70, (1500, 200, 2464, 1100), [(255, 170, 60), (255, 220, 120)], size=(3, 8), seed=4, shape="dot")
    c.particles(45, (0, 1000, 2464, 1400), [(200, 255, 150), (150, 240, 255)], size=(3, 7), seed=8, shape="dot")
    c.grade(contrast=1.05, sat=1.06, vignette=0.3, bloom=0.1)
    c.save(f"r14_{name}", f"{D14}/out")


if __name__ == "__main__":
    for n in (sys.argv[1:] or ARR): build14(n)
