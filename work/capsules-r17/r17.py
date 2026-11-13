"""Round 17: hero-vs-enemy face-offs under the brand sunburst sky, with real ground (land + rocks).

Rules (checked by the script, see check()):
  1. every character fully visible: no character hides more than a few % of another
  2. clown pins are lowered so their bases are off-frame
  3. Ophelia is solid (no fade into the environment)
  4. sky = yellow/orange sunburst with rays; ground = keyed land-and-rocks layer
  5. nothing touches the logo; logo as big as the clear space allows

python3 r17.py [1 2 3]  ->  out/
"""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r15")
import r15
from r15 import *

D = "/home/user/capyverse-claude/work/capsules-r17"
SRC = {"moody": "layers/H_moody_matte.png", "jim": "layers/H_jim.png", "axie": "layers/L_axie_matte.png",
       "worm": "layers/H_worm_bandits.png", "golfer": "layers/H_golfer.png", "pin": "layers/L_pin.png"}


def ground(name, horizon_src, horizon, cut=None):
    """Keyed ground layer scaled to the canvas width, its horizon placed at `horizon` (fraction of canvas height)."""
    im = Image.open(f"{D}/g_{name}_0.png").convert("RGB"); a = np.asarray(im).astype(np.float32)
    p = np.minimum(a[..., 0], a[..., 2]) - a[..., 1]                    # magenta/purple-ness
    alpha = 1 - np.clip((p - 35) / 45, 0, 1)
    if cut:                                                             # drop the blurry backdrop some plates add
        for y0, x0, x1 in cut: alpha[: int(y0 * im.height), int(x0 * im.width): int(x1 * im.width)] = 0
    alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32) / 255
    a[..., 0] -= (1 - alpha) * 0; rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
    g = Image.fromarray(rgba); k = C.W / g.width; g = g.resize((C.W, round(g.height * k)), Image.LANCZOS)
    y = round(horizon * C.H - horizon_src * g.height)
    out = ovl(); out.alpha_composite(g, (0, y)) if y >= 0 else out.alpha_composite(g.crop((0, -y, g.width, g.height)), (0, 0))
    if y + g.height < C.H:                                              # extend the bottom row downward if short
        strip = g.crop((0, g.height - 4, g.width, g.height)).resize((C.W, C.H - (y + g.height)))
        out.alpha_composite(strip, (0, y + g.height))
    return out


class Scene:
    def __init__(self, confetti=True): self.items = []; self.confetti = confetti          # draw order: (name, image, x, y, draw_fn, check)

    def add(self, name, im, x, y, draw, check=True):
        self.items.append((name, im, round(x), round(y), draw, check)); reserve(im, x, y)

    def hero(self, c, kind, fx, fy, fw, rim):
        w = fw * C.H; im = load(SRC[kind]); im = im.resize((round(w), round(im.height * w / im.width)), Image.LANCZOS)
        x, y = fx * C.W, fy * C.H
        def draw():
            keep = r15.confetti
            if not self.confetti: r15.confetti = lambda *a, **k: None      # logo size beats confetti
            hero(c, kind, x, y, w, rim=rim); r15.confetti = keep
        self.add(kind, im, x, y, draw)
        if kind == "jim" and self.confetti:                        # ...and Jim's trumpet confetti
            reserve(Image.new("RGBA", (round(w * 0.75), round(w * 0.6)), (0, 0, 0, 255)), x + w * 0.9, y - w * 0.22)
        if kind == "moody":                      # keep the disco flares off the logo too
            reserve(Image.new("RGBA", (round(w * 0.5), round(w * 0.3)), (0, 0, 0, 255)), x + w * 0.35, y - w * 0.12)

    def enemy(self, c, kind, fx, bottom, fh, rim, name=None):
        h = fh * C.H; im = load(SRC[kind]); im = im.resize((round(im.width * h / im.height), round(h)), Image.LANCZOS)
        x, y = fx * C.W, bottom * C.H - h

        def draw():
            if bottom < 1.0:
                g = ovl(); d = ImageDraw.Draw(g); cx = x + im.width / 2; gy = bottom * C.H - h * 0.02; ww = im.width * 0.9
                d.ellipse([cx - ww / 2, gy - ww * 0.07, cx + ww / 2, gy + ww * 0.07], fill=(40, 20, 30, 140))
                c.canvas.alpha_composite(g.filter(ImageFilter.GaussianBlur(ww * 0.05)))
            c.place("enemy", x, y, scale=1.0, src=im, match=0.06, wrap=0.2, rim=dict(color=rim, dir=(-1, -1), width=max(3, h / 140), strength=0.5))
        self.add(name or kind, im, x, y, draw)

    def cappy(self, c, fx, fy, fw, rim, ang=16):
        x, y, w = fx * C.W, fy * C.H, fw * C.H
        im, tip, thr = cappy_img(w); mp = (x + tip[0] + w * 0.012, y + tip[1] - w * 0.004)
        reserve_muzzle(mp, w * 0.17, ang, 6)
        self.add("cappy", im, x, y, lambda: (put_cappy(c, x, y, w, rim=rim, match=0.05), muzzle(c, mp, w * 0.17, ang, pop=6)))

    def draw(self):
        for it in self.items: it[4]()

    def check(self):
        """Rule 1: how much of each character is covered by characters drawn after it."""
        full = []
        for name, im, x, y, _, chk in self.items:
            m = np.zeros((C.H, C.W), bool); a = np.asarray(im.getchannel("A")) > 128
            x0, y0, x1, y1 = max(0, x), max(0, y), min(C.W, x + im.width), min(C.H, y + im.height)
            if x1 > x0 and y1 > y0: m[y0:y1, x0:x1] = a[y0 - y:y1 - y, x0 - x:x1 - x]
            full.append((name, m, a.sum(), chk))
        ok = True
        for i, (name, m, tot, chk) in enumerate(full):
            later = np.zeros_like(m)
            for n2, m2, _, _ in full[i + 1:]:
                if not (name.startswith("pin") and n2.startswith("pin")): later |= m2
            hid = (m & later).sum() / max(m.sum(), 1); inframe = m.sum() / max(tot, 1)
            flag = "" if (hid < 0.06 or not chk) else "  <-- HIDDEN"
            if flag: ok = False
            print(f"   {name:8s} hidden {hid * 100:4.1f}%  in frame {inframe * 100:3.0f}%{flag}")
        return ok


def sky(center, inner=(255, 236, 80), outer=(243, 98, 14), rays=26, a=0.2):
    c = C.Comp(radial_bg(C.W, C.H, center, inner, outer, rays=rays, ray_a=a))
    c.glow(center[0] * C.W, center[1] * C.H, C.H * 1.0, (255, 255, 225), 0.5)
    c.speed_lines(center[0] * C.W, center[1] * C.H, n=60, inner=0.3, color=(255, 255, 255), opacity=0.14, width=C.H / 200, seed=3)
    return c


def ophelia(c, fx, fy, fw):
    """Solid Ophelia, no fade (rule 3)."""
    kw = dict(fade=False, tint=(1.0, 0.95, 0.9), dim=0.97, alpha=1.0)
    O, _ = ophelia_img(fw * C.H, **kw); a = np.asarray(O).copy(); a[..., 3] = np.where(a[..., 3] > 120, 255, 0)   # hard edge at the neck
    O = Image.fromarray(a); reserve(O, fx * C.W, fy * C.H)
    sh = ovl(); sh.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", O.size, (120, 40, 10)).split(), O.getchannel("A").point(lambda v: v // 3))), (round(fx * C.W - C.H * 0.012), round(fy * C.H + C.H * 0.008)))
    c.canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(C.H * 0.012)))
    c.canvas.alpha_composite(O, (round(fx * C.W), round(fy * C.H)))
    _, eyes = ophelia_img(fw * C.H, **kw)
    for ey, ex in eyes: c.glow(fx * C.W + ex, fy * C.H + ey, fw * C.H * 0.11, (255, 30, 30), 0.8)


def pins(S, c, xs, rim, top=0.76, fh=0.36):
    for i, fx in enumerate(xs):       # rule 2: bottoms pushed below the frame so we never see what they stand on
        S.enemy(c, "pin", fx, top + fh + 0.012 * (i % 2), fh, rim, name=f"pin{i}")


RIM = (255, 245, 205)


# 1 — meadow: big standing Ophelia on the right, heroes in a row over Cappy
def build_1():
    cw, ch = C.W, C.H; S = Scene(confetti=False)
    c = sky((0.42, 0.30))
    c.canvas.alpha_composite(ground("meadow", 0.50, 0.63, cut=[(0.475, 0.0, 0.88), (0.36, 0.0, 1.0)]))
    ophelia(c, 0.705, 0.04, 0.60)
    S.hero(c, "moody", 0.008, 0.505, 0.36, RIM); S.hero(c, "jim", 0.245, 0.468, 0.27, RIM); S.hero(c, "axie", 0.0, 0.80, 0.30, RIM)
    S.enemy(c, "worm", 0.565, 0.99, 0.50, RIM); S.enemy(c, "golfer", 0.775, 1.0, 0.36, RIM)
    pins(S, c, [0.885, 0.945], RIM)
    S.cappy(c, 0.19, 0.60, 0.66, RIM)
    logo(c, 0.345 * cw, 0.235 * ch, 0.63 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


# 2 — rock plateau: big hero column on the left, logo fills the sky, Ophelia behind her crew lower right
def build_2():
    cw, ch = C.W, C.H; S = Scene()
    c = sky((0.60, 0.26), inner=(255, 228, 90), outer=(236, 70, 30))
    c.canvas.alpha_composite(ground("rocks", 0.37, 0.60))
    ophelia(c, 0.775, 0.37, 0.46)
    S.hero(c, "jim", 0.02, 0.04, 0.34, RIM); S.hero(c, "moody", 0.004, 0.275, 0.44, RIM); S.hero(c, "axie", 0.0, 0.80, 0.33, RIM)
    S.enemy(c, "worm", 0.60, 0.99, 0.44, RIM); S.enemy(c, "golfer", 0.735, 1.02, 0.32, RIM)
    pins(S, c, [0.85, 0.905, 0.96], RIM, top=0.84, fh=0.30)
    S.cappy(c, 0.215, 0.56, 0.70, RIM)
    logo(c, 0.625 * cw, 0.225 * ch, 0.68 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


# 3 — arena: giant Ophelia rises behind the ground top-right (as in round 14, but solid), heroes fan out low
def build_3():
    cw, ch = C.W, C.H; S = Scene(confetti=False)
    c = sky((0.50, 0.40), inner=(255, 240, 110), outer=(245, 120, 20), rays=30)
    ophelia(c, 0.655, -0.10, 0.72)
    c.canvas.alpha_composite(ground("arena", 0.52, 0.64))
    S.hero(c, "axie", 0.01, 0.50, 0.32, RIM); S.hero(c, "jim", 0.235, 0.468, 0.27, RIM); S.hero(c, "moody", 0.0, 0.715, 0.34, RIM)
    S.enemy(c, "worm", 0.575, 0.99, 0.44, RIM); S.enemy(c, "golfer", 0.775, 1.0, 0.34, RIM)
    pins(S, c, [0.875, 0.935], RIM, top=0.78, fh=0.34)
    S.cappy(c, 0.20, 0.60, 0.66, RIM)
    logo(c, 0.33 * cw, 0.235 * ch, 0.62 * cw, rot=-2, glow=(255, 255, 230), shadow=0.5)
    S.draw(); return c, S


B17 = {"1": build_1, "2": build_2, "3": build_3}

if __name__ == "__main__":
    for t in ([a for a in sys.argv[1:] if a in B17] or list(B17)):
        C.W, C.H = 2464, 1412; r15.OBST = None
        print("capsule", t)
        c, S = B17[t](); S.check()
        c.grade(contrast=1.05, sat=1.07, vignette=0.16, bloom=0.05)
        os.makedirs(f"{D}/out", exist_ok=True)
        c.canvas.convert("RGB").resize((1232, 706), Image.LANCZOS).save(f"{D}/out/{t}_main_1232x706.jpg", quality=94)
