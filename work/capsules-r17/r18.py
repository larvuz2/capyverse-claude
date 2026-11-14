"""Round 18: round 17 with a much bigger Cappy in the lower-left corner, the other heroes re-fitted so nothing overlaps
(same automatic checks), and a subtle shade on the background (sky, ground, Ophelia) so the logo and Cappy pop.

python3 r18.py [1 2 3]  ->  out18/
"""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r17")
import r17
from r17 import *


def shade(c, amount=0.09, right=0.06):
    """Subtle: darken + cool the background a little, a touch more toward the enemy side and the edges."""
    a = np.asarray(c.canvas).astype(np.float32)
    yy, xx = np.mgrid[0:C.H, 0:C.W].astype(np.float32)
    k = 1 - amount - right * np.clip((xx / C.W - 0.45) / 0.55, 0, 1) - 0.08 * np.clip(np.hypot(xx / C.W - 0.4, (yy / C.H - 0.45)) - 0.35, 0, 1)
    a[..., :3] *= k[..., None] * np.array([0.98, 0.97, 1.03])
    c.canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def spot(c, fx, fy, r, s=0.35):
    c.glow(fx * C.W, fy * C.H, r * C.H, (255, 250, 215), s)


# 1 — meadow: Cappy huge in the corner; Moody + Axie in the pocket above his back, Jim over the gatling
def build_1():
    cw, ch = C.W, C.H; S = Scene(confetti=False)
    c = sky((0.40, 0.28))
    c.canvas.alpha_composite(ground("meadow", 0.50, 0.63, cut=[(0.475, 0.0, 0.88), (0.36, 0.0, 1.0)]))
    ophelia(c, 0.705, 0.04, 0.60); shade(c); spot(c, 0.33, 0.24, 1.1); spot(c, 0.22, 0.80, 0.9, 0.3)
    S.hero(c, "moody", 0.0, 0.468, 0.27, RIM); S.hero(c, "axie", 0.0, 0.70, 0.25, RIM); S.hero(c, "jim", 0.158, 0.452, 0.185, RIM)
    S.enemy(c, "worm", 0.585, 0.99, 0.48, RIM); S.enemy(c, "golfer", 0.775, 1.0, 0.36, RIM)
    pins(S, c, [0.885, 0.945], RIM)
    S.cappy(c, -0.012, 0.50, 0.92, RIM)
    logo(c, 0.345 * cw, 0.235 * ch, 0.63 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


# 2 — rock plateau: bigger heroes in a column up the left edge, Cappy huge below them, logo to the right
def build_2():
    cw, ch = C.W, C.H; S = Scene()
    c = sky((0.60, 0.26), inner=(255, 228, 90), outer=(236, 70, 30))
    c.canvas.alpha_composite(ground("rocks", 0.37, 0.60))
    ophelia(c, 0.775, 0.37, 0.46); shade(c); spot(c, 0.60, 0.22, 1.1); spot(c, 0.22, 0.80, 0.9, 0.3)
    S.hero(c, "jim", 0.015, 0.03, 0.27, RIM); S.hero(c, "moody", 0.0, 0.225, 0.35, RIM); S.hero(c, "axie", 0.0, 0.565, 0.26, RIM)
    S.enemy(c, "worm", 0.62, 0.99, 0.44, RIM); S.enemy(c, "golfer", 0.745, 1.02, 0.32, RIM)
    pins(S, c, [0.86, 0.915, 0.97], RIM, top=0.84, fh=0.30)
    S.cappy(c, -0.012, 0.51, 0.92, RIM)
    logo(c, 0.61 * cw, 0.225 * ch, 0.68 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


# 3 — arena: biggest Cappy, giant solid Ophelia behind the rocks; Axie + Moody in the pocket, Jim over the gatling
def build_3():
    cw, ch = C.W, C.H; S = Scene(confetti=False)
    c = sky((0.48, 0.38), inner=(255, 240, 110), outer=(245, 120, 20), rays=30)
    ophelia(c, 0.655, -0.10, 0.72)
    c.canvas.alpha_composite(ground("arena", 0.52, 0.64)); shade(c); spot(c, 0.32, 0.24, 1.1); spot(c, 0.24, 0.82, 0.9, 0.3)
    S.hero(c, "axie", 0.0, 0.475, 0.26, RIM); S.hero(c, "moody", 0.0, 0.625, 0.27, RIM); S.hero(c, "jim", 0.168, 0.462, 0.19, RIM)
    S.enemy(c, "worm", 0.60, 0.99, 0.44, RIM); S.enemy(c, "golfer", 0.775, 1.0, 0.34, RIM)
    pins(S, c, [0.875, 0.935], RIM, top=0.78, fh=0.34)
    S.cappy(c, -0.015, 0.51, 0.98, RIM)
    logo(c, 0.33 * cw, 0.235 * ch, 0.62 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


B18 = {"1": build_1, "2": build_2, "3": build_3}

def build_small(t):
    """462x174 thumbnail: same sky/ground/Ophelia per take, just Cappy + a big centred logo."""
    cw, ch = C.W, C.H; S = Scene(confetti=False)
    if t == "1":
        c = sky((0.48, 0.3)); c.canvas.alpha_composite(ground("meadow", 0.50, 0.66, cut=[(0.475, 0.0, 0.88), (0.36, 0.0, 1.0)]))
        ophelia(c, 0.755, 0.06, 0.86)
    elif t == "2":
        c = sky((0.5, 0.3), inner=(255, 228, 90), outer=(236, 70, 30)); c.canvas.alpha_composite(ground("rocks", 0.37, 0.62))
        ophelia(c, 0.76, 0.10, 0.84)
    else:
        c = sky((0.5, 0.4), inner=(255, 240, 110), outer=(245, 120, 20), rays=30)
        ophelia(c, 0.755, -0.02, 0.86); c.canvas.alpha_composite(ground("arena", 0.52, 0.74))
    shade(c); spot(c, 0.48, 0.45, 1.0)
    S.cappy(c, -0.01, 0.40, 0.82, RIM)
    logo(c, 0.47 * cw, 0.45 * ch, 0.50 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


SIZES = {"main": (1232, 706, 2), "header": (920, 430, 2), "small": (462, 174, 4)}

if __name__ == "__main__":
    tags = [a for a in sys.argv[1:] if a in B18] or list(B18)
    sizes = [a for a in sys.argv[1:] if a in SIZES] or ["main"]
    for t in tags:
        for sz in sizes:
            tw, th, k = SIZES[sz]; C.W, C.H = tw * k, th * k; r15.OBST = None
            print("capsule", t, sz)
            hero0, enemy0, pins0 = Scene.hero, Scene.enemy, r17.pins
            if sz == "small":      # thumbnail: only the logo, Cappy and Ophelia so it reads at 462x174
                Scene.hero = lambda *a, **k: None; Scene.enemy = lambda *a, **k: None
                globals()["pins"] = lambda *a, **k: None
            try:
                c, S = (build_small(t) if sz == "small" else B18[t]()); S.check()
            finally:
                Scene.hero, Scene.enemy = hero0, enemy0; globals()["pins"] = pins0
            c.grade(contrast=1.05, sat=1.07, vignette=0.2, bloom=0.05)
            os.makedirs(f"{D}/out18", exist_ok=True)
            c.canvas.convert("RGB").resize((tw, th), Image.LANCZOS).save(f"{D}/out18/{t}_{sz}_{tw}x{th}.jpg", quality=94)
