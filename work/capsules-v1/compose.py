"""Capsule compositor: AI background plates + REAL in-engine character pixels + hand-made FX.

Characters are never regenerated. Each layer is the original Unreal render cut out of the gray base,
so what ships on Steam is the actual game model. Only backgrounds and Axie (missing from the base)
come from image models.
"""
import math
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance

W, H = 2464, 1412  # 2x the Steam main capsule (1232x706)
ROOT = __file__.rsplit("/", 1)[0]

# Belt-thruster nozzles in each layer's native pixels: (x, y, angle_deg). 180 = straight back (left).
THRUSTERS = {
    # rear end of the striped side-belt jetpack cylinder, pointing backward along its axis
    "cappy": [(398, 452, 186)],
    "moody": [(203, 170, 178)],
    "jim": [(140, 80, 170)],
    "axie": [(985, 535, 188)],
}


def load(path):
    return Image.open(path).convert("RGBA")


HD_K = 5760 / 2560  # H_ layers are cut from the full-res render


def layer(name):
    import os
    p = f"{ROOT}/layers/H_{name}.png"
    if os.path.exists(p): return load(p), HD_K
    return load(f"{ROOT}/layers/L_{name}.png"), 1.0


def debar(img, thr=10):
    """Crop black letterbox bars some image models add."""
    a = np.asarray(img.convert("L")).astype(np.float32)
    rows = a.mean(1); top = 0; bot = len(rows)
    while top < len(rows) // 4 and rows[top] < thr: top += 1
    while bot > len(rows) * 3 // 4 and rows[bot - 1] < thr: bot -= 1
    return img.crop((0, top, img.width, bot))


def cover(img, focus=(0.5, 0.5)):
    img = debar(img.convert("RGB"))
    s = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = round((img.width - W) * focus[0]); y = round((img.height - H) * focus[1])
    return img.crop((x, y, x + W, y + H)).convert("RGBA")


def arr(im):
    return np.asarray(im).astype(np.float32) / 255.0


def img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "RGBA")


def blur_a(alpha, r):
    return np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255.0


class Comp:
    def __init__(self, plate, focus=(0.5, 0.5)):
        self.canvas = cover(load(plate), focus) if isinstance(plate, str) else plate.convert("RGBA").resize((W, H))
        self.fx_over = []  # things drawn after all layers

    # ---------- placement ----------
    def place(self, name, x, y, scale=1.0, flip=False, match=0.15, wrap=0.35, rim=None,
              shadow=None, trail=None, flames=False, flame_len=1.0, flame_w=1.0, opacity=1.0, bright=1.0, sat=1.0, src=None):
        L, k = (src, 1.0) if src is not None else layer(name)
        if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT)
        L = L.resize((max(1, round(L.width * scale / k)), max(1, round(L.height * scale / k))), Image.LANCZOS)
        if bright != 1.0 or sat != 1.0:
            rgb = L.convert("RGB"); a_ = L.getchannel("A")
            rgb = ImageEnhance.Brightness(rgb).enhance(bright); rgb = ImageEnhance.Color(rgb).enhance(sat)
            L = rgb.convert("RGBA"); L.putalpha(a_)
        x, y = round(x), round(y)
        bg = self.canvas
        # region of canvas under the layer (clipped)
        box = (max(0, x), max(0, y), min(W, x + L.width), min(H, y + L.height))
        if box[2] <= box[0] or box[3] <= box[1]: return
        Lc = L.crop((box[0] - x, box[1] - y, box[2] - x, box[3] - y))
        la = arr(Lc); alpha = la[..., 3:4]
        under = arr(bg.crop(box))[..., :3]
        # trail (motion streak behind the character)
        if trail:
            self._trail(L, x, y, **trail)
            bg = self.canvas; under = arr(bg.crop(box))[..., :3]
        if shadow:
            self._shadow(L, x, y, **shadow)
            bg = self.canvas; under = arr(bg.crop(box))[..., :3]
        rgb = la[..., :3]
        # 1) colour match: tint toward the plate's ambient colour, keep luminance
        if match:
            bgblur = arr(bg.filter(ImageFilter.GaussianBlur(120)).crop(box))[..., :3]
            amb = (bgblur * alpha).sum((0, 1)) / max(alpha.sum(), 1)
            tint = amb / max(amb.mean(), 1e-3)
            rgb = rgb * (1 - match + match * tint)
        # 2) light wrap: blurred background bleeding onto the silhouette edges
        if wrap:
            a2 = alpha[..., 0]
            edge = np.clip(a2 - blur_a(a2, 10), 0, 1)[..., None] * 2.2
            bgsoft = arr(bg.filter(ImageFilter.GaussianBlur(25)).crop(box))[..., :3]
            rgb = rgb + (1 - rgb) * bgsoft * np.clip(edge * wrap, 0, 1)
        # 3) rim light from a direction
        if rim:
            col = np.array(rim.get("color", (255, 240, 200)), np.float32) / 255
            dx, dy = rim.get("dir", (-1, -1)); k = rim.get("width", 6)
            a2 = alpha[..., 0]
            sh = np.roll(np.roll(a2, int(-dx * k), 1), int(-dy * k), 0)
            rimm = np.clip(a2 - sh, 0, 1)
            rimm = blur_a(rimm, rim.get("soft", 3)) * a2
            rgb = rgb + (1 - rgb) * col * (rimm[..., None] * rim.get("strength", 0.8))
        out = np.concatenate([np.clip(rgb, 0, 1), alpha * opacity], -1)
        self.canvas.alpha_composite(img(out), (box[0], box[1]))
        if flames and name in THRUSTERS:
            for (fx, fy, ang) in THRUSTERS[name]:
                if flip: fx, ang = L.width / scale - fx, 180 - ang
                self.flame(x + fx * scale, y + fy * scale, ang, 190 * scale * flame_len, 50 * scale * flame_w)

    def _trail(self, L, x, y, length=300, color=(255, 255, 255), opacity=0.35, angle=180):
        a = L.getchannel("A")
        pad = int(length) + 20
        big = Image.new("L", (L.width + 2 * pad, L.height + 2 * pad), 0); big.paste(a, (pad, pad))
        acc = np.zeros((big.height, big.width), np.float32)
        steps = 24
        ba = np.asarray(big).astype(np.float32) / 255
        for i in range(1, steps + 1):
            d = length * i / steps
            dx = int(math.cos(math.radians(angle)) * d); dy = int(-math.sin(math.radians(angle)) * d)
            acc = np.maximum(acc, np.roll(np.roll(ba, dy, 0), dx, 1) * (1 - i / steps))
        acc = blur_a(np.clip(acc, 0, 1), 6) * opacity
        rgba = np.zeros((big.height, big.width, 4), np.float32)
        rgba[..., :3] = np.array(color, np.float32) / 255; rgba[..., 3] = acc
        self.screen(img(rgba), x - pad, y - pad)

    def _shadow(self, L, x, y, dx=0, dy=40, blur=30, opacity=0.45, squash=1.0, color=(0, 0, 0)):
        a = L.getchannel("A")
        if squash != 1.0: a = a.resize((a.width, max(1, int(a.height * squash))))
        pad = blur * 3
        big = Image.new("L", (a.width + 2 * pad, a.height + 2 * pad), 0); big.paste(a, (pad, pad))
        big = big.filter(ImageFilter.GaussianBlur(blur))
        sh = Image.new("RGBA", big.size, color + (0,)); sh.putalpha(big.point(lambda v: int(v * opacity)))
        oy = L.height - a.height
        self.canvas.alpha_composite(sh, (round(x + dx - pad), round(y + dy + oy - pad)))

    # ---------- FX ----------
    def screen(self, over, x=0, y=0):
        """Additive-ish screen blend of an RGBA overlay at (x, y)."""
        x, y = round(x), round(y)
        box = (max(0, x), max(0, y), min(W, x + over.width), min(H, y + over.height))
        if box[2] <= box[0] or box[3] <= box[1]: return
        o = arr(over.crop((box[0] - x, box[1] - y, box[2] - x, box[3] - y)))
        b = arr(self.canvas.crop(box))
        a = o[..., 3:4]
        b[..., :3] = 1 - (1 - b[..., :3]) * (1 - o[..., :3] * a)
        self.canvas.paste(img(b), box[:2])

    def flame(self, x, y, angle, length, width):
        size = int(length * 2 + width * 4)
        ov = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        cx = cy = size / 2
        ca, sa = math.cos(math.radians(angle)), -math.sin(math.radians(angle))
        nx, ny = -sa, ca
        def cone(L, w0, col):
            tip = (cx + ca * L, cy + sa * L)
            d.polygon([(cx + nx * w0, cy + ny * w0), tip, (cx - nx * w0, cy - ny * w0)], fill=col)
        # layered cones: outer orange haze -> blue body -> cyan -> white core
        cone(length * 1.00, width * 0.42, (255, 150, 60, 90))
        cone(length * 0.85, width * 0.36, (60, 140, 255, 170))
        cone(length * 0.55, width * 0.26, (120, 220, 255, 220))
        cone(length * 0.28, width * 0.15, (255, 255, 255, 255))
        d.ellipse([cx - width * 0.2, cy - width * 0.2, cx + width * 0.2, cy + width * 0.2], fill=(220, 245, 255, 255))
        ov = ov.filter(ImageFilter.GaussianBlur(max(1.5, width * 0.07)))
        halo = ov.filter(ImageFilter.GaussianBlur(width * 0.35)); ha = halo.getchannel("A").point(lambda v: int(v * 0.45)); halo.putalpha(ha)
        self.screen(halo, x - cx, y - cy); self.screen(ov, x - cx, y - cy)

    def glow(self, x, y, r, color, strength=0.8):
        s = int(r * 2.4)
        ov = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.ellipse([s / 2 - r / 2, s / 2 - r / 2, s / 2 + r / 2, s / 2 + r / 2], fill=color + (int(255 * strength),))
        ov = ov.filter(ImageFilter.GaussianBlur(r * 0.35))
        self.screen(ov, x - s / 2, y - s / 2)

    def logo(self, cx, cy, width, shadow=0.55, glow=None, rot=0, path=None):
        Lg = load(path or f"{ROOT}/layers/L_logo.png")
        h = round(Lg.height * width / Lg.width)
        Lg = Lg.resize((round(width), h), Image.LANCZOS)
        if rot: Lg = Lg.rotate(rot, Image.BICUBIC, expand=True)
        x, y = cx - Lg.width / 2, cy - Lg.height / 2
        if glow:
            p = 90
            ga = Image.new("L", (Lg.width + 2 * p, Lg.height + 2 * p), 0); ga.paste(Lg.getchannel("A"), (p, p))
            g = Image.new("RGBA", ga.size, glow + (0,)); g.putalpha(ga.filter(ImageFilter.GaussianBlur(34)).point(lambda v: int(v * 0.8)))
            self.screen(g, x - p, y - p)
        if shadow:
            self._shadow(Lg, x, y, dx=0, dy=width * 0.018, blur=int(width * 0.02), opacity=shadow)
        self.canvas.alpha_composite(Lg, (round(x), round(y)))

    def speed_lines(self, cx, cy, n=90, inner=0.35, color=(255, 255, 255), opacity=0.25, width=6, seed=1, sector=None):
        rnd = np.random.default_rng(seed)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        R = math.hypot(W, H)
        for _ in range(n):
            a = rnd.uniform(0, 2 * math.pi)
            if sector and not (sector[0] <= math.degrees(a) % 360 <= sector[1]): continue
            r0 = R * rnd.uniform(inner, inner + 0.25)
            w = rnd.uniform(width * 0.3, width)
            p0 = (cx + math.cos(a) * r0, cy + math.sin(a) * r0); p1 = (cx + math.cos(a) * R, cy + math.sin(a) * R)
            d.line([p0, p1], fill=color + (int(255 * opacity * rnd.uniform(0.4, 1)),), width=int(w))
        self.screen(ov.filter(ImageFilter.GaussianBlur(1.2)))

    def particles(self, n, box, colors, size=(4, 14), seed=2, glow=True, shape="rect"):
        rnd = np.random.default_rng(seed)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for _ in range(n):
            px, py = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3])
            s = rnd.uniform(*size); c = colors[rnd.integers(len(colors))]
            if shape == "rect":
                ang = rnd.uniform(0, math.pi)
                pts = [(px + math.cos(ang + k * math.pi / 2) * s * (1 if k % 2 == 0 else 0.5),
                        py + math.sin(ang + k * math.pi / 2) * s * (1 if k % 2 == 0 else 0.5)) for k in range(4)]
                d.polygon(pts, fill=c + (255,))
            else:
                d.ellipse([px - s, py - s, px + s, py + s], fill=c + (255,))
        if glow: self.screen(ov.filter(ImageFilter.GaussianBlur(6)))
        self.canvas.alpha_composite(ov)

    def grade(self, contrast=1.06, sat=1.08, vignette=0.35, warm=0.0, bloom=0.0):
        rgb = self.canvas.convert("RGB")
        if bloom:
            hi = rgb.point(lambda v: max(0, v - 170) * 3).filter(ImageFilter.GaussianBlur(40))
            a = arr(rgb.convert("RGBA")); h_ = arr(hi.convert("RGBA"))
            a[..., :3] = 1 - (1 - a[..., :3]) * (1 - h_[..., :3] * bloom)
            rgb = img(a).convert("RGB")
        rgb = ImageEnhance.Contrast(rgb).enhance(contrast); rgb = ImageEnhance.Color(rgb).enhance(sat)
        a = arr(rgb.convert("RGBA"))
        if warm: a[..., 0] *= 1 + warm; a[..., 2] *= 1 - warm
        if vignette:
            yy, xx = np.mgrid[0:H, 0:W]
            r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
            a[..., :3] *= (1 - vignette * np.clip(r - 0.55, 0, 1) ** 1.6)[..., None]
        self.canvas = img(a)

    def save(self, name, out_dir):
        import os
        os.makedirs(out_dir, exist_ok=True)
        full = self.canvas.convert("RGB")
        full.save(f"{out_dir}/{name}_full_2464x1412.jpg", quality=93)
        full.resize((1232, 706), Image.LANCZOS).save(f"{out_dir}/{name}_main_capsule_1232x706.jpg", quality=94)
        small = full.resize((462, 265), Image.LANCZOS)
        small.save(f"{out_dir}/{name}_thumb_test_462.jpg", quality=90)
        return full


# ---------- extra FX helpers ----------
# Prop anchor points in native layer pixels.
PROPS = {
    "moody_disco": (243, 52),   # centre of Moody's disco ball
    "jim_bell": (282, 72),      # Jim's trumpet bell opening
    "cappy_gatling": (722, 28), # tip of Cappy's popcorn gatling
}


def sparkle(c, x, y, size, color=(255, 255, 255), strength=1.0, rays=4, rot=0.0):
    s = int(size * 2.2)
    ov = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    cx = cy = s / 2
    for k in range(rays):
        a = math.radians(rot + k * 180 / rays)
        for w, L, al in ((size * 0.06, size, 200), (size * 0.025, size * 1.05, 255)):
            dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
            nx, ny = -math.sin(a) * w, math.cos(a) * w
            d.polygon([(cx - dx, cy - dy), (cx + nx, cy + ny), (cx + dx, cy + dy), (cx - nx, cy - ny)], fill=color + (int(al * strength),))
    d.ellipse([cx - size * .08, cy - size * .08, cx + size * .08, cy + size * .08], fill=(255, 255, 255, int(255 * strength)))
    c.screen(ov.filter(ImageFilter.GaussianBlur(1.5)), x - cx, y - cy)
    c.glow(x, y, size * 0.45, color, 0.6 * strength)


def disco_flares(c, x, y, scale, seed=4):
    rnd = np.random.default_rng(seed)
    cols = [(255, 255, 255), (255, 150, 230), (140, 230, 255), (255, 240, 150)]
    c.glow(x, y, 140 * scale, (255, 220, 255), 0.55)
    for i in range(6):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(10, 60) * scale
        sparkle(c, x + math.cos(a) * r, y + math.sin(a) * r, rnd.uniform(50, 130) * scale, cols[i % 4], 0.9, rot=rnd.uniform(0, 45))


def confetti(c, x, y, scale, angle=10, spread=28, n=70, dist=420, seed=5):
    rnd = np.random.default_rng(seed)
    cols = [(255, 70, 90), (255, 210, 40), (70, 200, 255), (120, 230, 110), (240, 110, 255), (255, 255, 255)]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for _ in range(n):
        a = math.radians(angle + rnd.uniform(-spread, spread)); r = (0.04 + rnd.uniform(0, 1) ** 0.6) * dist * scale * 1.5
        px, py = x + math.cos(a) * r, y - math.sin(a) * r
        w_, h_ = rnd.uniform(4, 9) * scale * 1.8, rnd.uniform(2, 4) * scale * 1.8
        rot = rnd.uniform(0, math.pi)
        pts = [(px + math.cos(rot) * w_ - math.sin(rot) * h_, py + math.sin(rot) * w_ + math.cos(rot) * h_),
               (px - math.cos(rot) * w_ - math.sin(rot) * h_, py - math.sin(rot) * w_ + math.cos(rot) * h_),
               (px - math.cos(rot) * w_ + math.sin(rot) * h_, py - math.sin(rot) * w_ - math.cos(rot) * h_),
               (px + math.cos(rot) * w_ + math.sin(rot) * h_, py + math.sin(rot) * w_ - math.cos(rot) * h_)]
        d.polygon(pts, fill=cols[rnd.integers(len(cols))] + (255,))
    c.canvas.alpha_composite(ov)


def halftone(size, cell, color, bg, radius_fn):
    """radius_fn(x, y) -> 0..1 dot radius factor (numpy-vectorised over cell centres)."""
    im = Image.new("RGBA", size, bg + (255,)); d = ImageDraw.Draw(im)
    ys, xs = np.mgrid[cell / 2:size[1]:cell, cell / 2:size[0]:cell]
    xs = xs + (np.arange(xs.shape[0])[:, None] % 2) * cell / 2
    rr = radius_fn(xs, ys) * cell * 0.62
    for x, y, r in zip(xs.ravel(), ys.ravel(), rr.ravel()):
        if r > 0.6: d.ellipse([x - r, y - r, x + r, y + r], fill=color + (255,))
    return im


def anchor(name, prop, x, y, scale, flip=False, lw=None):
    px, py = PROPS[prop]
    if flip: px = lw - px
    return x + px * scale, y + py * scale


def popcorn_burst(c, x, y, scale, angle=18, n=9, dist=380, seed=6, flare=True):
    """Subtle popcorn kernels leaving Cappy's gatling muzzle + a small muzzle flare."""
    import glob
    rnd = np.random.default_rng(seed)
    pieces = sorted(glob.glob(f"{ROOT}/layers/popcorn/*.png"))
    if flare:
        c.glow(x, y, 150 * scale, (255, 235, 170), 0.7)
        sparkle(c, x, y, 150 * scale, (255, 245, 210), 0.9, rot=angle)
    for i in range(n):
        t = (i + rnd.uniform(0.2, 0.9)) / n
        a = math.radians(angle + rnd.uniform(-14, 14))
        d = (40 + t * dist) * scale
        px, py = x + math.cos(a) * d, y - math.sin(a) * d
        P = load(pieces[rnd.integers(len(pieces))]).rotate(rnd.uniform(0, 360), Image.BICUBIC, expand=True)
        s = (0.28 + 0.25 * t) * scale
        c.place("popcorn", px - P.width * s / 2, py - P.height * s / 2, scale=s, src=P, match=0.05, wrap=0.15)


# ---------- hero helpers: every hero carries its signature FX ----------
LW = {"cappy": 1029, "moody": 432, "jim": 293, "axie": 2233}


def cappy(c, x, y, s, flip=False, popcorn=True, **kw):
    kw.setdefault("rim", dict(color=(255, 238, 190), dir=(-1 if flip else 1, -1), width=8, strength=0.85))
    kw.setdefault("flame_len", 1.1)
    c.place("cappy", x, y, scale=s, flip=flip, flames=True, **kw)
    if popcorn:
        gx, gy = anchor("cappy", "cappy_gatling", x, y, s, flip=flip, lw=LW["cappy"])
        popcorn_burst(c, gx, gy, s * 0.85, angle=162 if flip else 18)


def moody(c, x, y, s, flip=False, **kw):
    c.place("moody", x, y, scale=s, flip=flip, flames=True, **kw)
    disco_flares(c, *anchor("moody", "moody_disco", x, y, s, flip=flip, lw=LW["moody"]), s)


def jim(c, x, y, s, flip=False, confetti_n=35, **kw):
    c.place("jim", x, y, scale=s, flip=flip, flames=True, **kw)
    if confetti_n:
        confetti(c, *anchor("jim", "jim_bell", x, y, s, flip=flip, lw=LW["jim"]), s * 0.8,
                 angle=175 if flip else 5, n=confetti_n, dist=240)


def axie(c, x, y, s, flip=False, **kw):
    c.place("axie", x, y, scale=s, flip=flip, flames=True, **kw)


# ---------- comic lettering + golf shot ----------
FONTS = {"bangers": f"{ROOT}/fonts/Bangers.ttf", "luckiest": f"{ROOT}/fonts/LuckiestGuy.ttf"}


def sfx(c, text, x, y, size, rot=-8, fill=(255, 230, 60), stroke=(30, 15, 35), font="bangers", stroke_w=None, shadow=True):
    """Small comic onomatopoeia centred at (x, y)."""
    f = ImageFont.truetype(FONTS[font], int(size))
    sw = stroke_w or max(3, int(size * 0.09))
    pad = int(size * 0.8)
    tw = int(f.getlength(text)) + 2 * pad
    t = Image.new("RGBA", (tw, int(size * 1.6) + pad), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    if shadow:
        d.text((tw / 2 + size * 0.05, t.height / 2 + size * 0.06), text, font=f, anchor="mm", fill=stroke + (255,),
               stroke_width=sw, stroke_fill=stroke + (255,))
    d.text((tw / 2, t.height / 2), text, font=f, anchor="mm", fill=fill + (255,), stroke_width=sw, stroke_fill=stroke + (255,))
    t = t.rotate(rot, Image.BICUBIC, expand=True)
    c.canvas.alpha_composite(t, (int(x - t.width / 2), int(y - t.height / 2)))


def golf_ball_sprite(r):
    """A shaded golf ball with dimples, 4x supersampled."""
    S = int(r * 2 * 4 + 8); R = r * 4
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    cx = cy = S / 2
    dx, dy = (xx - cx) / R, (yy - cy) / R
    rr = dx ** 2 + dy ** 2
    inside = rr <= 1
    dz = np.sqrt(np.clip(1 - rr, 0, 1))
    L = np.array([-0.45, -0.55, 0.7]); L = L / np.linalg.norm(L)
    lam = np.clip(dx * L[0] + dy * L[1] + dz * L[2], 0, 1)
    # dimples: hex-ish grid on the sphere's projected surface
    u, v = dx / (dz + 0.35), dy / (dz + 0.35)
    g = 7.0
    du = (u * g) - np.round(u * g); dv = (v * g + 0.5 * (np.round(u * g) % 2)) - np.round(v * g + 0.5 * (np.round(u * g) % 2))
    dimple = np.clip(1 - np.sqrt(du ** 2 + dv ** 2) / 0.42, 0, 1) * dz
    shade = 0.55 + 0.45 * lam - 0.18 * dimple
    spec = np.clip(lam, 0, 1) ** 40 * 0.9
    col = np.clip(shade + spec, 0, 1)
    rgb = np.dstack([col * 252, col * 250, col * 244])
    edge = np.clip((1 - np.sqrt(rr)) * R / 1.5, 0, 1)
    a = (inside * edge * 255)
    im = Image.fromarray(np.dstack([rgb, a]).astype(np.uint8), "RGBA")
    return im.resize((S // 4, S // 4), Image.LANCZOS)


def golf_shot(c, x0, y0, x1, y1, r=26, bend=-160, trail=(255, 255, 255)):
    """Ball struck at (x0, y0) flying to (x1, y1) on a curved arc with a speed trail and an impact puff."""
    # impact puff at the tee
    for i, (rr, a) in enumerate(((70, 0.55), (45, 0.8))):
        c.glow(x0, y0, rr * 2, (255, 250, 230), a)
    sparkle(c, x0, y0, 120, (255, 255, 240), 0.9, rot=20)
    rnd = np.random.default_rng(3)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(10):  # little turf/dust chips kicked up
        a = math.radians(rnd.uniform(100, 170)); dd = rnd.uniform(25, 80)
        px, py = x0 + math.cos(a) * dd, y0 - math.sin(a) * dd * 0.6
        s_ = rnd.uniform(4, 9); d.ellipse([px - s_, py - s_, px + s_, py + s_], fill=(225, 205, 160, 220))
    c.canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(1)))
    # quadratic arc
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + bend
    pts = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * y1)
           for t in np.linspace(0, 1, 60)]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(len(pts) - 1):
        t = i / (len(pts) - 1)
        w = max(1, int(r * 1.5 * t ** 1.4)); a = int(220 * t ** 1.2)
        d.line([pts[i], pts[i + 1]], fill=trail + (a,), width=w)
    c.screen(ov.filter(ImageFilter.GaussianBlur(3)))
    c.canvas.alpha_composite(ov.filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: v) if False else ov.filter(ImageFilter.GaussianBlur(2)))
    c.glow(x1, y1, r * 4, (255, 255, 235), 0.6)
    b = golf_ball_sprite(r)
    c._shadow(b, x1 - b.width / 2, y1 - b.height / 2, dx=4, dy=6, blur=5, opacity=0.4)
    c.canvas.alpha_composite(b, (int(x1 - b.width / 2), int(y1 - b.height / 2)))
