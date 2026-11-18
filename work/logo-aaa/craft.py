"""Hand-built logo toolkit: font outlines -> shapely geometry -> hand edits -> a small material renderer.

Nothing here calls an image model. Letters are real font outlines (open-licence fonts in ./fonts), edited as
geometry (scaled, mirrored, notched, sliced), spaced optically, then shaded per pixel:

  distance-to-edge field  ->  bevel height  ->  surface normals  ->  light / metal reflection map
  + procedural textures (wood grain, brushed metal, enamel chips, rust) from layered value noise.

Units: "design px" (cap height of the main word is ~300). `Canvas(scale)` renders at scale x 2 and downsamples.
"""
import math, os
import numpy as np
import cv2
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from shapely.geometry import Polygon, MultiPolygon, box, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
F32 = np.float32


# ------------------------------------------------------------------ fonts -> geometry
class Face:
    def __init__(self, name):
        p = name if os.path.exists(name) else f"{HERE}/fonts/{name}.ttf"
        self.f = TTFont(p); self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        b = self._raw("H").bounds; self.cap = (b[3] - b[1]) / self.upm      # cap height in em

    def _raw(self, ch):
        """Glyph as shapely geometry in font units (y up), holes kept."""
        pen = DecomposingRecordingPen(self.gs); self.gs[self.cmap[ord(ch)]].draw(pen)
        rings, cur, last = [], [], (0, 0)
        for op, a in pen.value:
            if op == "moveTo":
                if cur: rings.append(cur)
                cur = [a[0]]; last = a[0]
            elif op == "lineTo": cur.append(a[0]); last = a[0]
            elif op in ("qCurveTo", "curveTo"):
                pts = [last] + list(a)
                if op == "qCurveTo" and len(pts) > 3:           # TrueType implied on-curve points
                    seq = [pts[0]]
                    for i in range(1, len(pts) - 2):
                        seq += [pts[i], ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)]
                    seq += [pts[-2], pts[-1]]
                    segs = [(seq[i], seq[i + 1], seq[i + 2]) for i in range(0, len(seq) - 2, 2)]
                else: segs = [tuple(pts)]
                for sg in segs:
                    for t in np.linspace(0, 1, 14)[1:]:
                        q = list(sg)
                        while len(q) > 1: q = [((1 - t) * u[0] + t * v[0], (1 - t) * u[1] + t * v[1]) for u, v in zip(q, q[1:])]
                        cur.append(q[0])
                last = a[-1]
            elif op in ("closePath", "endPath"):
                if cur: rings.append(cur); cur = []
        if cur: rings.append(cur)
        return nonzero(rings)

    def glyph(self, ch, cap_h):
        """(geometry, advance) with y DOWN, baseline at 0, scaled so the font's cap height = cap_h."""
        s = cap_h / (self.cap * self.upm)
        g = affinity.scale(self._raw(ch), s, -s, origin=(0, 0))
        return g, self.gs[self.cmap[ord(ch)]].width * s


def nonzero(rings):
    """Fill rule fonts actually use (non-zero winding), done exactly: split the plane along every contour, then keep
    each face whose winding number is not 0. Handles overlapping contours (variable fonts) and counters alike."""
    from shapely.ops import polygonize
    rs = [r for r in rings if len(r) > 2]
    area = lambda r: sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1])) / 2
    sg = [1 if area(r) > 0 else -1 for r in rs]
    ps = [Polygon(r).buffer(0) for r in rs]
    lines = unary_union([LineString(r + [r[0]]) for r in rs])
    keep = []
    for face in polygonize(lines):
        p = face.representative_point()
        if sum(s_ for s_, q in zip(sg, ps) if q.contains(p)) != 0: keep.append(face)
    return unary_union(keep).buffer(0)


def _profile(g, y0, y1, n=48):
    """Left and right ink edge of a glyph on n scanlines between y0 and y1 (nan where empty)."""
    L = np.full(n, np.nan); R = np.full(n, np.nan)
    x0, _, x1, _ = g.bounds
    for i, y in enumerate(np.linspace(y0 + 1e-3, y1 - 1e-3, n)):
        h = g.intersection(box(x0 - 1, y - 0.5, x1 + 1, y + 0.5))
        if not h.is_empty: L[i], R[i] = h.bounds[0], h.bounds[2]
    return L, R


def set_line(face, text, cap_h, gap, mods=None, min_gap=None, clip=None, extra=None):
    """Optically spaced line. `gap` = target average white space between letters (design px), measured only
    where the two letters actually face each other and clipped at `clip`, so AV / PY tuck in and HH do not.
    mods: {index: fn(geom) -> geom} applied before spacing. extra: {index: px added before that letter}.
    Returns [(char, geometry placed)], width."""
    mods = mods or {}; extra = extra or {}
    clip = clip if clip is not None else gap * 2.6; min_gap = min_gap if min_gap is not None else gap * 0.42
    gl = []
    for i, ch in enumerate(text):
        g, adv = face.glyph(ch, cap_h)
        if i in mods: g = mods[i](g)
        gl.append([ch, g])
    out, prev = [], None
    for i, (ch, g) in enumerate(gl):
        if prev is None:
            g = affinity.translate(g, -g.bounds[0], 0)
        else:
            _, Rp = _profile(prev, -cap_h, 0); Lc, _ = _profile(g, -cap_h, 0)
            both = ~np.isnan(Rp) & ~np.isnan(Lc)
            if both.sum() < 3:
                dx = prev.bounds[2] + gap - g.bounds[0]
            else:
                base = (Lc - Rp)[both]                       # gap per scanline if dx = 0
                lo, hi = -base.max() - 50, -base.min() + clip + 50
                for _ in range(40):
                    mid = (lo + hi) / 2
                    if np.clip(base + mid, None, clip).mean() < gap: lo = mid
                    else: hi = mid
                dx = max((lo + hi) / 2, min_gap - base.min())
            g = affinity.translate(g, dx + extra.get(i, 0), 0)
        out.append((ch, g)); prev = g
    w = out[-1][1].bounds[2]
    return out, w


def place(items, dx, dy):
    return [(c, affinity.translate(g, dx, dy)) for c, g in items]


def union(items):
    return unary_union([g for _, g in items])


def bounds(items):
    b = np.array([g.bounds for _, g in items]); return b[:, 0].min(), b[:, 1].min(), b[:, 2].max(), b[:, 3].max()


# ------------------------------------------------------------------ canvas + raster
class Canvas:
    SS = 2

    def __init__(self, w, h, scale=1.3):
        self.w, self.h, self.scale = w, h, scale
        self.k = scale * self.SS
        self.W, self.H = int(round(w * self.k)), int(round(h * self.k))
        self.rgb = np.zeros((self.H, self.W, 3), F32); self.a = np.zeros((self.H, self.W), F32)

    def px(self, v): return v * self.k                      # design px -> working px

    def mask(self, geom):
        """Rasterise shapely geometry to a float mask (working resolution, anti-aliased via 2x)."""
        im = Image.new("L", (self.W * 2, self.H * 2), 0); d = ImageDraw.Draw(im); k = self.k * 2
        geoms = [geom] if isinstance(geom, Polygon) else list(getattr(geom, "geoms", []))
        for p in sorted([q for q in geoms if isinstance(q, Polygon) and not q.is_empty], key=lambda q: -q.area):
            d.polygon([(x * k, y * k) for x, y in p.exterior.coords], fill=255)
            for r in p.interiors: d.polygon([(x * k, y * k) for x, y in r.coords], fill=0)
        return np.asarray(im.resize((self.W, self.H), Image.BOX)).astype(F32) / 255

    def over(self, rgb, alpha):
        """Composite a layer (rgb HxWx3 or colour tuple 0-255, alpha HxW) over the canvas."""
        if not isinstance(rgb, np.ndarray): rgb = np.broadcast_to(np.array(rgb, F32) / 255, self.rgb.shape)
        a = alpha[..., None]; out_a = a[..., 0] + self.a * (1 - a[..., 0])
        num = rgb * a + self.rgb * self.a[..., None] * (1 - a)
        self.rgb = np.where(out_a[..., None] > 1e-6, num / np.maximum(out_a[..., None], 1e-6), 0).astype(F32); self.a = out_a.astype(F32)

    def under(self, rgb, alpha):
        if not isinstance(rgb, np.ndarray): rgb = np.broadcast_to(np.array(rgb, F32) / 255, self.rgb.shape)
        a = alpha * (1 - self.a); out_a = self.a + a
        num = self.rgb * self.a[..., None] + rgb * a[..., None]
        self.rgb = np.where(out_a[..., None] > 1e-6, num / np.maximum(out_a[..., None], 1e-6), 0).astype(F32); self.a = out_a.astype(F32)

    def save(self, path, trim=True, pad=10):
        rgba = np.dstack([np.clip(self.rgb, 0, 1), np.clip(self.a, 0, 1)])
        im = Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA")
        im = im.resize((self.W // self.SS, self.H // self.SS), Image.LANCZOS)
        if trim:
            bb = im.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
            bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(im.width, bb[2] + pad), min(im.height, bb[3] + pad)); im = im.crop(bb)
        im.save(path); return im


# ------------------------------------------------------------------ fields
def dist_in(m):
    """Distance (working px) from each inside pixel to the edge."""
    return cv2.distanceTransform((m > 0.5).astype(np.uint8), cv2.DIST_L2, 5).astype(F32)


def dist_out(m):
    return cv2.distanceTransform((m <= 0.5).astype(np.uint8), cv2.DIST_L2, 5).astype(F32)


def blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), max(0.3, s)) if s > 0 else a


def noise(shape, cell, seed=0, octaves=4, aniso=(1.0, 1.0), gain=0.5):
    """Layered value noise in 0..1. cell = feature size in working px; aniso stretches it (x, y)."""
    H, W = shape; rng = np.random.default_rng(seed); out = np.zeros(shape, F32); amp, tot = 1.0, 0.0
    for o in range(octaves):
        cx = max(1.0, cell * aniso[0] / 2 ** o); cy = max(1.0, cell * aniso[1] / 2 ** o)
        g = rng.random((int(H / cy) + 3, int(W / cx) + 3), dtype=F32)
        big = cv2.resize(g, (int(g.shape[1] * cx), int(g.shape[0] * cy)), interpolation=cv2.INTER_CUBIC)
        oy, ox = rng.integers(0, max(1, int(cy))), rng.integers(0, max(1, int(cx)))
        out += big[oy:oy + H, ox:ox + W] * amp; tot += amp; amp *= gain
    return np.clip(out / tot, 0, 1)


def normals(h, strength=1.0):
    gy, gx = np.gradient(h.astype(F32))
    n = np.dstack([-gx * strength, -gy * strength, np.ones_like(h)])
    return n / np.linalg.norm(n, axis=2, keepdims=True)


def lambert(n, L=(-0.48, -0.62, 0.62)):
    L = np.array(L, F32); L /= np.linalg.norm(L); return np.clip((n * L).sum(2), 0, 1)


def specular(n, L=(-0.48, -0.62, 0.62), gloss=40):
    L = np.array(L, F32); L /= np.linalg.norm(L); Hv = L + np.array([0, 0, 1], F32); Hv /= np.linalg.norm(Hv)
    return np.clip((n * Hv).sum(2), 0, 1) ** gloss


def ramp(t, stops):
    """Map t (0..1) through colour stops [(pos, (r,g,b) 0-255), ...] -> HxWx3 float 0..1."""
    t = np.clip(t, 0, 1); pos = np.array([p for p, _ in stops], F32); cols = np.array([c for _, c in stops], F32) / 255
    return np.dstack([np.interp(t, pos, cols[:, i]) for i in range(3)]).astype(F32)


def metal(n, stops, tilt=0.25):
    """Reflection-map look: what a polished surface facing direction n would mirror (sky above, ground below)."""
    t = 0.5 - 0.5 * (n[..., 1] * (1 - tilt) + n[..., 0] * tilt)          # up-left facets brightest
    return ramp(t, stops)


def bevel(d, width, profile="round"):
    """Edge profile from the distance field: 0 at the edge -> 1 on the flat top."""
    t = np.clip(d / max(width, 1e-6), 0, 1)
    if profile == "chisel": return t
    if profile == "round": return np.sqrt(1 - (1 - t) ** 2)
    if profile == "soft": return t * t * (3 - 2 * t)
    return t


def grow(m, r):
    """Dilate a mask by r working px (round)."""
    if r <= 0: return m
    return np.clip(1 - (dist_out(m) - r), 0, 1) if r > 0 else m


def shadow(c, m, dx, dy, soft, color=(20, 12, 8), strength=0.55):
    sh = blur(np.roll(np.roll(m, int(c.px(dy)), 0), int(c.px(dx)), 1), c.px(soft)) * strength
    c.under(color, sh)
