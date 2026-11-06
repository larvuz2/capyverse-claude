"""Round 10 capsules: the five round-9 capsules with the SAME backgrounds, red-circle content and logo position.
Only the three back heroes (Jim, Moody, Axie) are rearranged, each take with its own grounding/lighting idea:

1 Squadron     tight V right behind Cappy, overlapping, one shared warm back-glow that binds them as a team
2 Portal Exit  they burst out of a glowing lobby portal in a diagonal, small/far to big/near; portal light rims them
3 Low Skim     Jim skims the ground in the gap before the worm (dust + hard shadow + thruster light on the grass)
4 Depth Stack  Moody big and close at the left edge (soft focus), Jim mid, Axie small and hazy far behind
5 Contrails    the squad trails Cappy along his flight arc, long glowing contrails tying them into his motion
"""
import sys, math, random
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r8")
import r9
from r9 import *          # KEEP, FLAMES, background, contact_shadows, fx_red, ground_shadow, P, W, H, C, ...
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

SIZE = {"moody": (432, 341), "jim": (293, 203), "axie": (2233, 1129)}
OUT = f"{R8}/r10"


def box(kind, x, y, s):
    w, h = SIZE[kind]; return (x, y, x + w * s, y + h * s)


def ovl(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def light_pool(c, cx, gy, w, col, a=0.55):
    """Thruster light spilling onto the ground below a hero (screen blend), plus a soft dark core."""
    g = ovl(); d = ImageDraw.Draw(g)
    d.ellipse([cx - w / 2, gy - w * 0.09, cx + w / 2, gy + w * 0.09], fill=col + (int(255 * a),))
    c.screen(g.filter(ImageFilter.GaussianBlur(w * 0.12)))


def hero(c, kind, x, y, s, rim, gy=None, shadow_a=80, match=0.28, bright=1.0, sat=1.0, haze=0.0, blur=0.0,
         trail_len=260, rim_dir=(-1, -1), rim_strength=0.75, pool=None, confetti=35, flames=True):
    """Like r9.hero, plus haze (atmospheric perspective), defocus, rim direction and a thruster light pool."""
    T = dict(length=trail_len, color=(255, 245, 230), opacity=0.22, angle=195) if trail_len else None
    kw = dict(rim=dict(color=rim, dir=rim_dir, width=7, strength=rim_strength), trail=T, match=match + haze * 0.5,
              wrap=0.4 + haze, bright=bright * (1 + haze * 0.25), sat=sat * (1 - haze * 0.45))
    if kind == "jim":
        L, k = C.layer("jim")
    else:
        L = load("layers/H_moody_matte.png" if kind == "moody" else "layers/L_axie_matte.png")
        k = 5760 / 2560 if kind == "moody" else 1.0
    L = L.resize((max(1, round(L.width * s / k)), max(1, round(L.height * s / k))), Image.LANCZOS)
    if blur: L = L.filter(ImageFilter.GaussianBlur(blur))
    c.place(kind, x, y, scale=1.0, src=L, **kw)
    if flames:
        for fx, fy, ang in C.THRUSTERS[kind]:
            c.flame(x + fx * s, y + fy * s, ang, 190 * s * 1.7, 50 * s * 1.5)
    if kind == "moody": disco_flares(c, *anchor("moody", "moody_disco", x, y, s), s, seed=9)
    if kind == "jim" and confetti:
        C.confetti(c, *anchor("jim", "jim_bell", x, y, s, lw=C.LW["jim"]), s * 0.8, angle=5, n=confetti, dist=240)
    b = box(kind, x, y, s); w = b[2] - b[0]
    if gy:
        ground_shadow(c, x + w * 0.55, gy, w * 0.75, shadow_a)
        if pool: light_pool(c, x + w * 0.35, gy, w * 0.9, pool, 0.35)
    return b


def back_glow(c, cx, cy, r, col, a=0.5):
    c.glow(cx, cy, r, col, a)


def portal(c, cx, cy, rx, ry, col):
    """Glowing portal ring (like the lobby portals) the squad flies out of."""
    g = ovl(); d = ImageDraw.Draw(g)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col + (110,))
    c.screen(g.filter(ImageFilter.GaussianBlur(rx * 0.35)))
    g = ovl(); d = ImageDraw.Draw(g)
    for wdt, a, blur in ((38, 200, 14), (14, 255, 3)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=col + (a,), width=wdt)
        c.screen(g.filter(ImageFilter.GaussianBlur(blur)))
    g = ovl(); d = ImageDraw.Draw(g)
    d.ellipse([cx - rx * 0.9, cy - ry * 0.9, cx + rx * 0.9, cy + ry * 0.9], fill=(255, 245, 255, 70))
    c.screen(g.filter(ImageFilter.GaussianBlur(rx * 0.25)))
    rnd = random.Random(3)
    for _ in range(40):  # sparks
        t = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(1.0, 1.35)
        c.glow(cx + math.cos(t) * rx * rr, cy + math.sin(t) * ry * rr, rnd.uniform(6, 16), (255, 230, 255), 0.8)


def contrail(c, pts, col, width, a=0.6):
    """Long soft glowing curve through pts (list of (x, y)), fading toward the start."""
    g = ovl(); d = ImageDraw.Draw(g)
    n = len(pts)
    for i in range(n - 1):
        t = i / (n - 1)
        d.line([pts[i], pts[i + 1]], fill=col + (int(255 * a * t),), width=max(2, int(width * (0.35 + 0.65 * t))))
    c.screen(g.filter(ImageFilter.GaussianBlur(width * 0.45)))
    g2 = ovl(); d = ImageDraw.Draw(g2)
    for i in range(n - 1):
        t = i / (n - 1)
        d.line([pts[i], pts[i + 1]], fill=(255, 255, 255, int(200 * t * t)), width=max(1, int(width * 0.25)))
    c.screen(g2.filter(ImageFilter.GaussianBlur(2)))


def arc(p0, p1, bend, n=40):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + bend
    return [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1)
            for t in (i / (n - 1) for i in range(n))]


def dust(c, cx, gy, w, col=(235, 215, 185)):
    rnd = random.Random(7); g = ovl(); d = ImageDraw.Draw(g)
    for _ in range(70):
        x = cx - rnd.uniform(0, w); y = gy - rnd.uniform(0, 60) * (1 - (cx - x) / w * 0.5)
        r = rnd.uniform(10, 34) * (0.5 + (cx - x) / w)
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=col + (rnd.randint(40, 110),))
    c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(6)))


def r9_logo_boxes(name):
    cfg = r9.APPROACHES[name]
    return [box(k, x, y, s) for k, x, y, s in cfg["heroes"]]


# ---- the five arrangements (background + grade identical to round 9) ----
def thr(kind, x, y, s):
    fx, fy, _ = C.THRUSTERS[kind][0]; return x + fx * s, y + fy * s


def a1(c):  # Squadron: tight overlapping V, one shared warm back-glow
    rim = (255, 225, 170)
    back_glow(c, 300, 400, 900, (255, 185, 100), 0.55)
    b = [hero(c, "axie", 0, 175, 0.15, rim, gy=1330, confetti=0),
         hero(c, "jim", 300, 150, 0.95, rim, gy=1330, confetti=22),
         hero(c, "moody", 40, 300, 1.05, rim, gy=1330)]
    return b, ("WHOOSH!", 640, 470)


def a2(c):  # Portal Exit: the squad bursts out of a lobby portal, far/small to near/big
    rim = (225, 170, 255)
    portal(c, 170, 230, 175, 215, (205, 120, 255))
    portal(c, 170, 230, 175, 215, (205, 120, 255))
    b = [hero(c, "axie", 95, 205, 0.09, rim, rim_dir=(-1, 0), rim_strength=1.0, trail_len=0, haze=0.2, confetti=0),
         hero(c, "jim", 330, 215, 0.78, rim, rim_dir=(-1, 0), rim_strength=1.0, trail_len=0, haze=0.05, confetti=18),
         hero(c, "moody", 60, 420, 1.0, rim, rim_dir=(-1, -0.6), rim_strength=1.0, trail_len=0, gy=1330)]
    return b, ("WHOOSH!", 640, 470)


def a3(c):  # Low Skim: Jim skims the ground before the worm (dust, hard shadow, thruster light)
    rim = (170, 255, 225)
    gy = 1335
    dust(c, 1180, gy, 520)
    b = [hero(c, "jim", 990, 1030, 1.15, rim, gy=gy, shadow_a=190, pool=(255, 170, 80), trail_len=260, confetti=0),
         hero(c, "moody", 30, 250, 1.0, rim, gy=1300),
         hero(c, "axie", 300, 140, 0.13, rim, confetti=0)]
    return b, ("ZOOM!", 1110, 975)


def a4(c):  # Depth Stack: Moody big and close (soft focus), Jim mid, Axie small and hazy far
    rim = (255, 200, 140)
    b = [hero(c, "axie", 390, 250, 0.085, rim, haze=0.45, trail_len=110, confetti=0),
         hero(c, "jim", 375, 375, 0.8, rim, haze=0.12, trail_len=180, confetti=20),
         hero(c, "moody", -190, 60, 1.45, rim, blur=2.2, trail_len=300, gy=1330, shadow_a=110)]
    return b, None


def a5(c):  # Contrails: long glowing trails rising along Cappy's flight arc into each thruster
    rim = (220, 200, 255)
    col = (255, 215, 160)
    pos = [("jim", 110, 80, 0.95), ("moody", 40, 290, 1.0), ("axie", 0, 655, 0.15)]
    for k, x, y, s_ in pos:
        tx, ty = thr(k, x, y, s_)
        pts = arc((-140, ty + 110), (tx, ty), 35)
        g = ovl(); d = ImageDraw.Draw(g)       # darker orange halo, normal blend, so it reads on the pale sky
        for i in range(len(pts) - 1):
            t = i / (len(pts) - 1); d.line([pts[i], pts[i + 1]], fill=(255, 130, 50, int(90 + 140 * t)), width=int(40 + 50 * t))
        c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(9)))
        contrail(c, pts, col, 40, 1.0)
    b = [hero(c, k, x, y, s_, rim, trail_len=0, confetti=20 if k == "jim" else 0) for k, x, y, s_ in pos]
    return b, ("WHOOSH!", 640, 470)


R10 = {"1_squadron": ("1_golden_path", a1), "2_portal_exit": ("2_portal_night", a2), "3_low_skim": ("3_glow_tree", a3),
       "4_depth_stack": ("4_cave_glow", a4), "5_contrails": ("5_river_moon", a5)}


def logo_fixed(c, r9name):
    """Same logo position as round 9 (fitted against the round-9 hero boxes), so only the heroes change."""
    import r8_sizes as R
    mask = np.asarray(Image.fromarray((KMASK * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(7))) > 8
    mask = mask.copy()
    for x0, y0, x1, y1 in r9_logo_boxes(r9name): mask[max(0, int(y0)):int(y1), max(0, int(x0)):int(x1)] = True
    R.LOGO = LOGO
    cx, cy, w = R.fit_logo(mask, W, H, prefer=(0.52, 0.28), max_frac=0.9)
    R.logo(c, cx, cy, w, 1.0)
    return cx, cy, w


def build(name):
    r9name, fn = R10[name]
    cfg = r9.APPROACHES[r9name]
    c = Comp(background(cfg["bg"][0], cfg["bg"][1], **cfg["grade"]))
    contact_shadows(c)
    boxes, wh = fn(c)
    c.screen(FLAMES); c.canvas.alpha_composite(KEEP)
    fx_red(c)
    if wh: sfx(c, wh[0], wh[1], wh[2], 74, rot=-10, fill=(255, 230, 150))
    lg = logo_fixed(c, r9name)
    c.grade(contrast=1.04, sat=1.04, vignette=0.28)
    os.makedirs(OUT, exist_ok=True)
    c.save(f"r10_{name}", OUT)
    print(name, "logo", [round(v) for v in lg], "boxes", [[round(v) for v in b] for b in boxes])


if __name__ == "__main__":
    for n in (sys.argv[1:] or R10): build(n)
