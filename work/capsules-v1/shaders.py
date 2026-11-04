"""Post 'shaders' that turn a finished composite into a different art style.

All of these run on the real render pixels (no image model), so the characters stay the game models,
just drawn differently. Apply before the logo, then place the logo on top so the brand stays crisp.
"""
import math
import numpy as np
import cv2
from PIL import Image, ImageFilter


def _np(im):
    return np.asarray(im.convert("RGB"))


def _pil(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


def ink_cel(im, colors=14, line=3, edge_lo=60, edge_hi=150, shadow_hatch=True):
    """Cel shading: flatten colour into bands, then ink the edges (Hades / Ravenswatch inked look)."""
    a = _np(im)
    sm = cv2.bilateralFilter(a, 9, 60, 60)
    sm = cv2.bilateralFilter(sm, 9, 60, 60)
    Z = sm.reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 12, 1.0)
    sample = Z[np.random.default_rng(0).choice(len(Z), 60000, replace=False)]
    _, _, centers = cv2.kmeans(sample, colors, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    d = ((Z[:, None, :] - centers[None]) ** 2).sum(-1)
    flat = centers[d.argmin(1)].reshape(a.shape)
    flat = cv2.medianBlur(flat.astype(np.uint8), 5).astype(np.float32)
    gray = cv2.cvtColor(sm, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, edge_lo, edge_hi)
    edges = cv2.dilate(edges, np.ones((line, line), np.uint8))
    edges = cv2.GaussianBlur(edges, (3, 3), 0).astype(np.float32) / 255
    ink = np.array([28, 18, 30], np.float32)
    out = flat * (1 - edges[..., None]) + ink * edges[..., None]
    if shadow_hatch:
        lum = gray.astype(np.float32) / 255
        h, w = lum.shape
        yy, xx = np.mgrid[0:h, 0:w]
        hatch = ((xx + yy) % 14 < 2).astype(np.float32) * (lum < 0.22)
        out = out * (1 - hatch[..., None] * 0.6) + ink * hatch[..., None] * 0.6
    return _pil(out)


def pixel(im, width=440, colors=40, outline=True):
    """Pixel art (Risk of Rain Returns / Dave the Diver): downsample, limited palette, nearest upscale."""
    W, H = im.size
    h = round(width * H / W)
    small = im.convert("RGB").resize((width, h), Image.BOX)
    small = Image.fromarray(cv2.bilateralFilter(np.asarray(small), 5, 40, 40))
    q = small.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).convert("RGB")
    if outline:
        a = np.asarray(q).astype(np.float32)
        lum = a.mean(-1)
        gx = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1])); gy = np.abs(np.diff(lum, axis=0, prepend=lum[:1]))
        e = ((gx + gy) > 70).astype(np.float32)[..., None]
        a = a * (1 - e * 0.55)
        q = Image.fromarray(a.astype(np.uint8))
    return q.resize((W, H), Image.NEAREST).convert("RGBA")


def _screen(chan, cell, angle_deg):
    """Amplitude-modulated halftone of a 0..1 coverage channel."""
    h, w = chan.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(angle_deg)
    u = (xx * math.cos(a) + yy * math.sin(a)) / cell
    v = (-xx * math.sin(a) + yy * math.cos(a)) / cell
    du, dv = u - np.round(u), v - np.round(v)
    dist = np.sqrt(du ** 2 + dv ** 2)  # 0 at dot centre, ~0.7 at corner
    r = np.sqrt(np.clip(chan, 0, 1) / math.pi) * 1.0
    return np.clip((r - dist) * cell * 0.9 + 0.5, 0, 1)


def riso(im, inks=((255, 72, 150), (255, 214, 0), (0, 120, 200)), paper=(246, 240, 226), cell=9, shift=4, grain=0.06):
    """Three-ink risograph print: separate, halftone each ink at its own angle, misregister, multiply on paper."""
    a = _np(im).astype(np.float32) / 255
    c, m, y = 1 - a[..., 0], 1 - a[..., 1], 1 - a[..., 2]
    k = np.minimum(np.minimum(c, m), y) * 0.6
    seps = [m - k * 0.3, y - k * 0.3, c - k * 0.2]  # pink<-magenta, yellow<-yellow, blue<-cyan
    out = np.ones_like(a) * (np.array(paper, np.float32) / 255)
    angles = (15, 0, 75)
    offs = ((0, 0), (shift, -shift // 2), (-shift, shift))
    for sep, ink, ang, (ox, oy) in zip(seps, inks, angles, offs):
        dots = _screen(np.clip(sep * 1.15, 0, 1), cell, ang)
        dots = np.roll(np.roll(dots, oy, 0), ox, 1)
        inkc = np.array(ink, np.float32) / 255
        out = out * (1 - dots[..., None] * (1 - inkc))
    rnd = np.random.default_rng(1)
    out = out * (1 - grain * rnd.random(out.shape[:2])[..., None])
    return _pil(out * 255)


def painted(im, wash=(242, 236, 228), wash_amt=0.18, sigma_s=50, sigma_r=0.35):
    """Painterly key art (Risk of Rain 2): edge-preserving stylization + pale atmospheric wash + paper grain."""
    a = _np(im)
    st = cv2.stylization(a, sigma_s=sigma_s, sigma_r=sigma_r).astype(np.float32)
    st = st * (1 - wash_amt) + np.array(wash, np.float32) * wash_amt
    rnd = np.random.default_rng(2)
    paper = cv2.GaussianBlur(rnd.random(a.shape[:2]).astype(np.float32), (0, 0), 1.2)
    st = st * (0.96 + 0.08 * paper[..., None])
    return _pil(st)
