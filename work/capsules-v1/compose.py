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
    "cappy": [(262, 402, 196)],
    "moody": [(256, 186, 192)],
    "jim": [(166, 128, 190)],
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


def cover(img, focus=(0.5, 0.5)):
    img = img.convert("RGB")
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
              shadow=None, trail=None, flames=False, flame_len=1.0, opacity=1.0, bright=1.0, sat=1.0, src=None):
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
                self.flame(x + fx * scale, y + fy * scale, ang, 330 * scale * flame_len, 70 * scale)

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
