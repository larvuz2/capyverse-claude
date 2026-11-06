"""Round 12: the round-11 reference layout with the REAL 3D hero models (Capy, Moody, Jim) rendered in Blender
(render_heroes.py), gear added by an image model and merged back so only the gear pixels are AI (gear_merge.py),
Axie kept 2D (no model). Logo much bigger.

python3 r12.py [A_meadow B_milkyway C_vivid]  ->  out/
"""
import sys, os, math
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r11")
import r11
from r11 import *            # Comp, load, fit, clean, contact, beam, tracers, sparkle, popcorn_burst, C, W, H, ...
import numpy as np
from scipy import ndimage
from PIL import Image, ImageFilter, ImageDraw

D12 = "/home/user/capyverse-claude/work/capsules-r12"
D11 = "/home/user/capyverse-claude/work/capsules-r11"


def hero3d(name, width):
    """3D render (with its shadow-catcher shadow) cropped to content and scaled so the CHARACTER is `width` wide."""
    im = Image.open(f"{D12}/renders/{name}_gear.png").convert("RGBA")
    a = np.asarray(im)[..., 3]
    solid = a > 230
    ys, xs = np.nonzero(solid); cx0, cx1 = xs.min(), xs.max()
    im = im.crop(im.getbbox()); bb = Image.open(f"{D12}/renders/{name}_gear.png").getbbox()
    k = width / (cx1 - cx0)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    # offsets of the character's solid bbox inside the cropped/scaled image
    off = ((cx0 - bb[0]) * k, (ys.min() - bb[1]) * k, (ys.max() - bb[1]) * k)
    return im, off


def shade_shadow(im):
    """Shadow-catcher alpha is black; tint it night-purple so it sits in the meadow."""
    a = np.asarray(im).astype(np.float32)
    dark = (a[..., :3].max(-1) < 12) & (a[..., 3] < 250)
    a[dark, 0], a[dark, 1], a[dark, 2] = 25, 12, 40
    return Image.fromarray(a.astype(np.uint8))


def put(c, im, x, y, rim=None, match=0.12):
    c.place("hero", x, y, scale=1.0, src=im, match=match, wrap=0.25, rim=rim)


def build(name, plate):
    c = Comp(f"{D11}/{plate}")
    # Ophelia looming top right (same treatment as round 11)
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

    # Cappy (3D) — placed first so we know where the muzzle is; tracers go behind the logo
    CP, (o_x, o_top, o_bot) = hero3d("capy", 700)
    cx_, cy_ = 1350, 255
    # muzzle = leftmost gear pixel in the top quarter of the cropped hero
    ga = np.asarray(Image.open(f"{D12}/gear/mask_capy.png")) > 0
    bb = Image.open(f"{D12}/renders/capy_gear.png").getbbox(); kk = CP.width / (bb[2] - bb[0])
    ys, xs = np.nonzero(ga); top = ys < ys.min() + (ys.max() - ys.min()) * 0.25
    mi = np.argmin(np.where(top, xs, 99999)); mzx, mzy = cx_ + (xs[mi] - bb[0]) * kk, cy_ + (ys[mi] - bb[1]) * kk
    tracers(c, (mzx, mzy), 160)

    # logo, WAY bigger: ~60% of the frame width, upper left
    c.logo(770, 400, 1480, shadow=0.6, glow=(255, 200, 130), rot=3, path=r11.LOGO)

    # Moody (3D) bottom left, rainbow beam to the left edge
    MO, _ = hero3d("moody", 480); MO = shade_shadow(MO)
    mx, my = 120, 1400 - MO.height + 40
    gm = np.asarray(Image.open(f"{D12}/gear/mask_moody.png")) > 0; bbm = Image.open(f"{D12}/renders/moody_gear.png").getbbox()
    km = MO.width / (bbm[2] - bbm[0]); ys, xs = np.nonzero(gm); top = ys < ys.min() + (ys.max() - ys.min()) * 0.35
    i = np.argmin(np.where(top, xs, 99999)); tx, ty = mx + (xs[i] - bbm[0]) * km, my + (ys[i] - bbm[1]) * km
    beam(c, (tx + 12, ty + 8), (-120, ty + 190), 40, 230)
    put(c, MO, mx, my, rim=dict(color=(255, 160, 90), dir=(1, -1), width=6, strength=0.5))
    c.glow(tx + 12, ty + 8, 130, (255, 230, 255), 0.8)

    # Axie (2D, no model) bottom right, warmed to the fire light
    A = fit(clean(f"{D11}/cut_axie_stand_0.png", flip=True), 500)
    ax, ay = 1950, 1290 - A.height
    contact(c, ax + 260, 1292, 460)
    c.place("axie", ax, ay, scale=1.0, src=A, match=0.25, wrap=0.4, bright=0.92,
            rim=dict(color=(255, 140, 70), dir=(1, -1), width=8, strength=0.85))

    # Jim (3D) running, bottom centre-right
    JI, _ = hero3d("jim", 480); JI = shade_shadow(JI)
    put(c, JI, 840, 1430 - JI.height + 30, rim=dict(color=(255, 160, 90), dir=(1, -1), width=6, strength=0.5))

    # Cappy on top
    fx, fy = cx_ + CP.width * 0.745, cy_ + CP.height * 0.565          # rear of the side-belt jet cylinder
    c.flame(fx, fy, -12, 190 * 2.2, 50 * 1.9); c.glow(fx, fy, 170, (255, 170, 80), 0.7)
    put(c, CP, cx_, cy_, rim=dict(color=(255, 150, 70), dir=(1, -1), width=8, strength=0.6), match=0.08)
    sparkle(c, mzx - 10, mzy, 240, (255, 230, 150), 1.0, rot=10)
    c.glow(mzx - 10, mzy, 240, (255, 180, 60), 0.9)

    c.particles(70, (1500, 200, 2464, 1100), [(255, 170, 60), (255, 220, 120)], size=(3, 8), seed=4, shape="dot")
    c.particles(45, (0, 1000, 2464, 1400), [(200, 255, 150), (150, 240, 255)], size=(3, 7), seed=8, shape="dot")
    c.grade(contrast=1.05, sat=1.06, vignette=0.3, bloom=0.1)
    c.save(f"r12_{name}", f"{D12}/out")


if __name__ == "__main__":
    TAKES = {"A_meadow": "plate_nb_0.png", "B_milkyway": "plate_nb_1.png", "C_vivid": "plate_gpt_0.png"}
    for n in (sys.argv[1:] or TAKES): build(n, TAKES[n])
