"""Materials for the five wordmarks. Every pixel is computed here: bevels from the distance-to-edge field,
lighting from surface normals, textures from layered noise. No image model, no stock textures.

python3 render.py [1 2 3 4 5]   ->  out/<name>.png  (transparent, trimmed)
"""
import sys
from craft import *
import geom

OUT = f"{HERE}/out"
FINAL_W = 2600                               # px width of the finished PNG before trimming


def setup(G, keys, margin=70):
    parts = [g for _, g in G["main"] + G["sub"]] + [g for k in keys for g in (G.get(k) if isinstance(G.get(k), list) else [G.get(k)]) if g is not None]
    b = unary_union(parts).bounds
    c = Canvas(b[2] - b[0] + 2 * margin, b[3] - b[1] + 2 * margin, scale=FINAL_W / (b[2] - b[0] + 2 * margin))
    sh = lambda g: affinity.translate(g, margin - b[0], margin - b[1])
    return c, sh, (margin - b[0], margin - b[1])


def finish(c, m, outline=(30, 18, 10), ow=3.2, sh=(4, 9, 9, 0.5)):
    """Dark keyline + soft drop shadow so the mark holds on any capsule."""
    c.under(outline, grow(m, c.px(ow)))
    shadow(c, grow(m, c.px(ow)), sh[0], sh[1], sh[2], strength=sh[3])


GOLD = [(0, (36, 18, 4)), (0.2, (92, 54, 10)), (0.38, (158, 104, 22)), (0.52, (212, 160, 48)), (0.68, (242, 204, 100)), (0.86, (255, 236, 168)), (1, (255, 252, 232))]
BRASS = [(0, (46, 30, 10)), (0.25, (112, 80, 26)), (0.45, (170, 130, 50)), (0.6, (212, 174, 84)), (0.78, (238, 214, 136)), (1, (255, 248, 214))]
STEEL = [(0, (14, 18, 28)), (0.22, (58, 68, 86)), (0.42, (128, 140, 156)), (0.5, (64, 72, 90)), (0.62, (150, 162, 178)), (0.8, (222, 230, 238)), (1, (255, 255, 255))]


# ---------------------------------------------------------------- 1 GILT
def r1():
    G = geom.g1(); c, sh, _ = setup(G, ["rules"])
    m = c.mask(sh(unary_union([g for _, g in G["main"] + G["sub"]] + G["rules"])))
    d = dist_in(m)
    h = blur(d, c.px(0.5))                                              # V-cut: the ridge runs down the middle of every stroke
    h += (noise(m.shape, c.px(3.2), seed=4, octaves=2) - 0.5) * c.px(0.55)          # hand-hammered face
    n = normals(h, 1.45)
    col = metal(n, GOLD, tilt=0.38)
    col *= (0.93 + 0.14 * noise(m.shape, c.px(60), seed=8, octaves=3))[..., None]   # uneven polish
    col += specular(n, gloss=55)[..., None] * np.array([1.0, 0.95, 0.8], F32) * 0.35
    ridge = np.clip(1 - np.abs(np.gradient(d)[0]) - np.abs(np.gradient(d)[1]), 0, 1) * (d > c.px(3))   # catch-light on the ridge
    col += blur(ridge.astype(F32), c.px(0.6))[..., None] * 0.18
    c.over(np.clip(col, 0, 1), m)
    finish(c, m, outline=(34, 16, 4), ow=4.6, sh=(4, 10, 9, 0.6))
    return c


# ---------------------------------------------------------------- 2 OAK & BRASS
def wood(c, shape, seed, tone=0.0):
    """Quarter-sawn oak, grain running up each letter: long fine fibres, a slow 'figure', faint growth lines, pores."""
    fib = noise(shape, c.px(3.2), seed=seed, octaves=3, aniso=(1, 60))
    fig = noise(shape, c.px(26), seed=seed + 1, octaves=3, aniso=(1, 9))
    warp = noise(shape, c.px(150), seed=seed + 2, octaves=2, aniso=(1, 5))
    xx = np.arange(shape[1], dtype=F32)[None, :] / c.px(30)
    rings = 0.5 + 0.5 * np.sin((xx + warp * 5) * 2 * np.pi)
    v = np.clip(0.5 + 0.55 * (fib - 0.5) + 0.75 * (fig - 0.5) + 0.16 * (rings - 0.5) + tone, 0, 1)
    col = ramp(v, [(0, (50, 26, 10)), (0.3, (92, 52, 22)), (0.55, (132, 80, 38)), (0.8, (168, 110, 58)), (1, (198, 142, 84))])
    pores = noise(shape, c.px(1.8), seed=seed + 3, octaves=2, aniso=(1, 22))
    col *= (1 - 0.30 * np.clip((pores - 0.64) / 0.16, 0, 1))[..., None]
    return col, v


def r2():
    G = geom.g2(); c, sh, _ = setup(G, ["studs", "bars"])
    mall = np.zeros((c.H, c.W), F32)
    for i, (ch, g) in enumerate(G["main"]):                              # each letter is its own block of oak
        m = c.mask(sh(g)); d = dist_in(m)
        col, v = wood(c, m.shape, seed=20 + i * 7, tone=[0.02, -0.05, 0.05, -0.02, 0.03, -0.06, 0.04, 0.0, -0.04][i])
        h = bevel(d, c.px(10), "round") * c.px(6.5) + v * c.px(0.9)
        n = normals(blur(h, c.px(0.4)), 1.0)
        lit = 0.42 + 0.78 * lambert(n)
        col = col * lit[..., None] + specular(n, gloss=24)[..., None] * 0.16
        col *= (0.62 + 0.38 * np.clip(d / c.px(7), 0, 1))[..., None]               # darkened, handled edges
        c.over(np.clip(col, 0, 1), m); mall = np.maximum(mall, m)
    # brass wire let into a groove that follows every stroke
    mi = c.mask(sh(G["inlay"])); di = dist_in(mi)
    groove = np.clip(grow(mi, c.px(2.2)) - mi, 0, 1)
    c.over((24, 12, 4), groove * 0.75 * mall)
    hi = bevel(di, c.px(4), "round") * c.px(4.2)
    ni = normals(hi, 1.2)
    bc = metal(ni, BRASS, tilt=0.35) + specular(ni, gloss=50)[..., None] * 0.5
    c.over(np.clip(bc, 0, 1), mi)
    # ODYSSEY, studs and rules in solid brass
    ms = c.mask(sh(unary_union([g for _, g in G["sub"]] + G["studs"] + G["bars"]))); ds = dist_in(ms)
    hs = bevel(ds, c.px(7), "round") * c.px(6) + (noise(ms.shape, c.px(2.4), seed=3, octaves=2, aniso=(18, 1)) - 0.5) * c.px(0.7)
    ns = normals(blur(hs, c.px(0.4)), 1.1)
    sc = metal(ns, BRASS, tilt=0.35) + specular(ns, gloss=45)[..., None] * 0.45
    c.over(np.clip(sc, 0, 1), ms)
    m = np.maximum(mall, ms)
    finish(c, m, outline=(26, 12, 4), ow=4.6, sh=(4, 10, 9, 0.6))
    return c


# ---------------------------------------------------------------- 3 TIN TYPE
def enamel(c, m, paint, seed, chip=0.74, nails=()):
    """Painted sheet tin: rolled edge, slightly wavy sheet, paint chipped back to rust mostly along the edges."""
    d = dist_in(m); shape = m.shape
    chipn = noise(shape, c.px(15), seed=seed, octaves=4)
    edge = np.exp(-d / c.px(13))
    fine = noise(shape, c.px(4), seed=seed + 1, octaves=3)
    chips = ((chipn + edge * 0.44 > chip) | ((fine > 0.84) & (chipn > 0.66))) & (m > 0.5)
    for (x, y, r) in nails:                                              # paint always fails around a nail first
        yy, xx = np.ogrid[:shape[0], :shape[1]]
        chips |= ((xx - x) ** 2 + (yy - y) ** 2 < (r * (1.15 + 1.1 * (chipn - 0.3))) ** 2) & (m > 0.5)
    chips_f = blur(chips.astype(F32), c.px(0.5))
    wav = (noise(shape, c.px(85), seed=seed + 2, octaves=2) - 0.5) * c.px(4)       # the sheet is not perfectly flat
    h = bevel(d, c.px(5), "round") * c.px(3.6) + wav + (1 - chips_f) * c.px(1.5)    # paint has thickness
    n = normals(blur(h, c.px(0.5)), 1.0)
    lit = 0.5 + 0.7 * lambert(n)
    pcol = np.array(paint, F32) / 255
    paintc = pcol * (0.9 + 0.16 * noise(shape, c.px(40), seed=seed + 3, octaves=3))[..., None]
    paintc *= (0.97 + 0.06 * noise(shape, c.px(2.5), seed=seed + 4, octaves=2, aniso=(1, 14)))[..., None]   # brush marks
    rust = ramp(noise(shape, c.px(7), seed=seed + 5, octaves=4), [(0, (58, 26, 12)), (0.4, (116, 52, 20)), (0.7, (164, 84, 32)), (1, (204, 132, 62))])
    # rust weeping downward out of every chip
    stain = cv2.blur(chips.astype(F32), (max(1, int(c.px(3))), max(1, int(c.px(46)))))
    stain = np.roll(stain, int(c.px(20)), 0) * (1 - chips_f)
    st = 0.42 * np.clip(stain * 2.0, 0, 1)
    paintc = paintc * (1 - st[..., None]) + np.array([150, 78, 30], F32) / 255 * st[..., None]
    col = paintc * (1 - chips_f[..., None]) + rust * chips_f[..., None]
    col = col * lit[..., None] + specular(n, gloss=30)[..., None] * 0.22 * (1 - chips_f)[..., None]
    rim = np.clip(1 - d / c.px(2.4), 0, 1)                               # bare metal on the cut edge
    col = col * (1 - rim[..., None] * 0.75) + np.array([120, 112, 104], F32) / 255 * (rim * 0.75 * lit)[..., None]
    return np.clip(col, 0, 1)


def nail(c, x, y, r):
    """One steel nail head, lit from the upper left."""
    R = int(r * 2.2); yy, xx = np.mgrid[-R:R + 1, -R:R + 1].astype(F32); rr = np.hypot(xx, yy)
    dome = np.sqrt(np.clip(1 - (rr / r) ** 2, 0, 1)) * r * 0.55
    n = normals(dome, 1.0); col = metal(n, STEEL, tilt=0.4) * 0.9 + specular(n, gloss=30)[..., None] * 0.5
    a = np.clip(r - rr + 0.5, 0, 1); ring = np.clip(r * 1.22 - rr + 0.5, 0, 1)
    x, y = int(x), int(y); sl = (slice(y - R, y + R + 1), slice(x - R, x + R + 1))
    for alpha, colr in ((ring * 0.7, np.broadcast_to(np.array([30, 16, 8], F32) / 255, col.shape)), (a, np.clip(col, 0, 1))):
        dst = c.rgb[sl]; c.rgb[sl] = dst * (1 - alpha[..., None]) + colr * alpha[..., None]


def r3():
    G = geom.g3(); c, sh, off = setup(G, [])
    mm = c.mask(sh(union(G["main"]))); ms = c.mask(sh(union(G["sub"])))
    nails = [(c.px(x + off[0]), c.px(y + off[1]), c.px(6.5)) for x, y in G["nails"]]
    c.over(enamel(c, mm, (240, 226, 192), seed=31, chip=0.965, nails=nails), mm)
    c.over(enamel(c, ms, (190, 50, 28), seed=57, chip=1.03), ms)
    for x, y, r in nails: nail(c, x, y, r)
    m = np.maximum(mm, ms)
    finish(c, m, outline=(30, 22, 16), ow=3.2, sh=(4, 10, 9, 0.55))
    return c


# ---------------------------------------------------------------- 4 JET BADGE
def r4():
    G = geom.g4(); c, sh, off = setup(G, ["trail"])
    m = c.mask(sh(union(G["main"]))); d = dist_in(m); bw = c.px(11)
    hb = bevel(d, bw, "chisel") * bw * 0.95
    n = normals(blur(hb, c.px(0.5)), 1.0)
    chrome = metal(n, STEEL, tilt=0.3) + specular(n, gloss=60)[..., None] * 0.5
    ys = np.nonzero(m.max(1) > 0.5)[0]; y0, y1 = ys.min(), ys.max()
    t = np.clip((np.arange(c.H, dtype=F32)[:, None] - y0) / (y1 - y0), 0, 1) * np.ones((1, c.W), F32)
    face = ramp(t, [(0, (255, 228, 96)), (0.34, (255, 176, 34)), (0.47, (252, 136, 20)), (0.57, (232, 92, 14)), (1, (178, 42, 12))])   # hard horizon, like baked enamel under a strip light
    face *= (0.95 + 0.1 * noise(m.shape, c.px(1.6), seed=5, octaves=2))[..., None]                       # metal flake
    gloss = np.clip(1 - np.abs(t - 0.2) / 0.16, 0, 1) ** 2 * 0.28
    face = face + gloss[..., None]
    inner = np.clip((d - bw) / c.px(4), 0, 1)                            # soft shadow where the enamel meets the rim
    face *= (0.72 + 0.28 * inner)[..., None]
    isface = np.clip((d - bw) / 1.5 + 0.5, 0, 1)[..., None]
    c.over(np.clip(chrome * (1 - isface) + face * isface, 0, 1), m)
    # ODYSSEY + trail: brushed steel
    ms = c.mask(sh(unary_union([g for _, g in G["sub"]] + G["trail"]))); ds = dist_in(ms)
    hs = bevel(ds, c.px(5), "chisel") * c.px(4.5) + (noise(ms.shape, c.px(2.2), seed=9, octaves=2, aniso=(22, 1)) - 0.5) * c.px(0.8)
    ns = normals(blur(hs, c.px(0.4)), 1.0)
    sc = metal(ns, STEEL, tilt=0.3) * 0.6 + np.array([226, 232, 240], F32) / 255 * 0.5 * np.clip(ds / c.px(5), 0, 1)[..., None] + specular(ns, gloss=40)[..., None] * 0.4
    c.over(np.clip(sc, 0, 1), ms)
    mall = np.maximum(m, ms)
    finish(c, mall, outline=(12, 14, 22), ow=3.6, sh=(5, 10, 8, 0.55))
    return c


# ---------------------------------------------------------------- 5 PURE
def r5(ink=False):
    G = geom.g5(); c, sh, _ = setup(G, [], margin=40)
    disc = G["sub"][0][1]
    m = c.mask(sh(unary_union([g for _, g in G["main"] + G["sub"][1:]])))
    c.over((28, 21, 48) if ink else (247, 239, 222), m)
    c.over((255, 128, 24), c.mask(sh(disc)))
    return c


def svg5(path, ink=False):
    """The flat mark as true vector paths."""
    G = geom.g5(); allg = unary_union([g for _, g in G["main"] + G["sub"]]); b = allg.bounds; mrg = 40
    def d(g):
        out = ""
        for p in getattr(g, "geoms", [g]):
            for ring in [p.exterior] + list(p.interiors):
                pts = list(ring.coords); out += "M" + " L".join(f"{x - b[0] + mrg:.1f},{y - b[1] + mrg:.1f}" for x, y in pts) + "Z"
        return out
    col = "#1c1530" if ink else "#f7efde"
    body = "".join(f'<path d="{d(g)}" fill="{col}" fill-rule="evenodd"/>' for _, g in G["main"] + G["sub"][1:])
    body += f'<path d="{d(G["sub"][0][1])}" fill="#ff8018"/>'
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {b[2] - b[0] + 2 * mrg:.0f} {b[3] - b[1] + 2 * mrg:.0f}">{body}</svg>')


R = {"1": ("1_gilt", r1), "2": ("2_oak_brass", r2), "3": ("3_tin_type", r3), "4": ("4_jet_badge", r4), "5": ("5_pure", r5)}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k in ([a for a in sys.argv[1:] if a in R] or list(R)):
        name, fn = R[k]; c = fn(); im = c.save(f"{OUT}/{name}.png"); print(name, im.size)
        if k == "5":
            r5(ink=True).save(f"{OUT}/5_pure_ink.png"); svg5(f"{OUT}/5_pure.svg"); svg5(f"{OUT}/5_pure_ink.svg", ink=True)
