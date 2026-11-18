"""Letter geometry for the five wordmarks: font outlines, hand edits and optical spacing. No rendering here."""
import random
from craft import *


def fit_gap(face, text, cap, width, lo=2, hi=400, **kw):
    """Find the letter gap that makes the line exactly `width` wide (for justified subtitles)."""
    for _ in range(30):
        mid = (lo + hi) / 2; _, w = set_line(face, text, cap, mid, **kw)
        lo, hi = (mid, hi) if w < width else (lo, mid)
    return set_line(face, text, cap, (lo + hi) / 2, **kw)


def needle(x0, x1, y, t):
    """Thin tapered rule: full thickness t at x1, a point at x0."""
    return Polygon([(x0, y), (x1, y - t / 2), (x1, y + t / 2)])


def center_on(items, i, axis):
    """Shift a line so letter i is centred on x = axis."""
    b = items[i][1].bounds; return place(items, axis - (b[0] + b[2]) / 2, 0)


# 1 — GILT: Roman capitals, the middle V is a tall wedge that drops through the rule and points at ODYSSEY
def g1():
    F, FV, F2 = Face("Cinzel-Black"), Face("Cinzel-Bold"), Face("Cinzel-Bold")
    cap, kv = 300, 1.40
    bigV = lambda g: affinity.scale(FV.glyph("V", cap)[0], kv, kv, origin=((FV.glyph("V", cap)[0].bounds[0] + FV.glyph("V", cap)[0].bounds[2]) / 2, -cap))
    row, w = set_line(F, "CAPYVERSE", cap, 30, mods={4: bigV})
    V = row[4][1]; tip_y = V.bounds[3]; low = V.intersection(box(-1e4, tip_y - 6, 1e4, tip_y + 1)); axis = (low.bounds[0] + low.bounds[2]) / 2
    x0, _, x1, _ = bounds(row); dl, dr = axis - x0, x1 - axis          # balance the two halves around the V
    extra = {i: (dr - dl) / 4 for i in (1, 2, 3, 4)} if dr > dl else {i: (dl - dr) / 4 for i in (5, 6, 7, 8)}
    row, w = set_line(F, "CAPYVERSE", cap, 30, mods={4: bigV}, extra=extra)
    V = row[4][1]; low = V.intersection(box(-1e4, tip_y - 6, 1e4, tip_y + 1)); axis = (low.bounds[0] + low.bounds[2]) / 2
    x0, _, x1, _ = bounds(row)
    sub, w2 = fit_gap(F2, "ODYSSEY", 90, (x1 - x0) * 0.62)
    sub = place(center_on(sub, 3, axis), 0, tip_y + 44 + 90)
    ry = 64; cut = V.intersection(box(-1e4, ry - 8, 1e4, ry + 8)).bounds
    rules = [needle(x0 + 4, cut[0] - 30, ry, 7), needle(x1 - 4, cut[2] + 30, ry, 7)]
    return dict(main=row, sub=sub, rules=rules, cap=cap)


# 2 — OAK & BRASS: fat slab letters, each its own block of oak, a brass wire inlaid along every stroke
def g2():
    F = Face("AlfaSlabOne"); cap = 290
    row, w = set_line(F, "CAPYVERSE", cap, 17)
    x0, _, x1, _ = bounds(row)
    sub, _ = fit_gap(F, "ODYSSEY", 74, (x1 - x0) * 0.56)
    sb = bounds(sub); sub = place(sub, (x0 + x1) / 2 - (sb[0] + sb[2]) / 2, 74 + 62)
    inlay = []
    for ch, g in row:
        ring = g.buffer(-27, join_style=1).difference(g.buffer(-35, join_style=1))
        if not ring.is_empty: inlay.append(ring)
    sb = bounds(sub); ym = (sb[1] + sb[3]) / 2
    studs = [Point(sb[0] - 46, ym).buffer(11), Point(sb[2] + 46, ym).buffer(11)]
    bars = [needle(x0 + 6, sb[0] - 76, ym, 8), needle(x1 - 6, sb[2] + 76, ym, 8)]
    return dict(main=row, sub=sub, inlay=unary_union(inlay), studs=studs, bars=bars, cap=cap)


# 3 — TIN TYPE: tall condensed letters snipped from sheet tin, each nailed up slightly out of true
def g3():
    F = Face("Anton"); cap = 330; rnd = random.Random(7)
    row, w = set_line(F, "CAPYVERSE", cap, 20)
    out = []
    for i, (ch, g) in enumerate(row):
        b = g.bounds; cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        clip = box(b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1)
        for (px, py, sx, sy) in rnd.sample([(b[0], b[1], 1, 1), (b[2], b[1], -1, 1), (b[0], b[3], 1, -1), (b[2], b[3], -1, -1)], 2):
            s = rnd.uniform(13, 24)                                        # tin-snip the corner
            clip = clip.difference(Polygon([(px - sx, py - sy), (px + sx * s, py - sy), (px - sx, py + sy * s)]))
        g = g.intersection(clip)
        g = affinity.rotate(g, rnd.uniform(-1.5, 1.5), origin=(cx, cy)); g = affinity.translate(g, 0, rnd.uniform(-5, 5))
        out.append((ch, g))
    x0, _, x1, _ = bounds(out)
    sub, _ = fit_gap(F, "ODYSSEY", 98, (x1 - x0) * 0.60)
    sb = bounds(sub); sub = place(sub, (x0 + x1) / 2 - (sb[0] + sb[2]) / 2, 98 + 56)
    nails = []
    for ch, g in out:                                                     # two nail positions per letter, inside the metal
        b = g.bounds; core = g.buffer(-17)
        for fy in (0.11, 0.89):
            y = b[1] + (b[3] - b[1]) * fy; line = core.intersection(box(b[0], y - 3, b[2], y + 3))
            if line.is_empty: continue
            parts = list(getattr(line, "geoms", [line])); p = max(parts, key=lambda q: q.area)
            nails.append(((p.bounds[0] + p.bounds[2]) / 2, y))
    return dict(main=out, sub=sub, nails=nails, cap=cap)


# 4 — JET BADGE: heavy italic, three speed slits cut into the leading letters, a needle trail leading to ODYSSEY
def g4():
    F = Face("Kanit-BlackItalic"); cap = 285
    row, w = set_line(F, "CAPYVERSE", cap, 13)
    x0, _, x1, _ = bounds(row); W = x1 - x0; sl = 0.21                    # italic slope (dx per dy)
    cuts = []
    for fy, fl in ((0.30, 0.20), (0.50, 0.33), (0.70, 0.145)):
        y = -cap * (1 - fy); L = W * fl; t = 11
        cuts.append(Polygon([(x0 - 40, y - t / 2), (x0 + L + sl * t / 2, y - t / 2), (x0 + L - sl * t / 2, y + t / 2), (x0 - 40, y + t / 2)]))
    cutU = unary_union(cuts)
    row = [(ch, g.difference(cutU)) for ch, g in row]
    sub, w2 = set_line(F, "ODYSSEY", 70, 36)
    sub = place(sub, x1 - w2 - 6 - 70 * sl, 70 + 54)
    sb = bounds(sub); ym = (sb[1] + sb[3]) / 2
    trail = [Polygon([(x0 - 20, ym), (sb[0] - 30 + 5 * sl, ym - 5), (sb[0] - 30 - 5 * sl, ym + 5)])]
    return dict(main=row, sub=sub, trail=trail, cap=cap)


# 5 — PURE: wide geometric letters only. The A is the V turned upside down; the O of ODYSSEY is a solid disc
def g5():
    F, F2 = Face("Unbounded-Black"), Face("Unbounded-Bold"); cap = 250
    V = F.glyph("V", cap)[0]
    flipV = lambda g: affinity.scale(V, 1, -1, origin=(0, -cap / 2))
    row, w = set_line(F, "CAPYVERSE", cap, 31, mods={1: flipV})
    x0, _, x1, _ = bounds(row)
    solid = lambda g: unary_union([Polygon(p.exterior) for p in getattr(g, "geoms", [g])])
    sub, _ = fit_gap(F2, "ODYSSEY", 78, (x1 - x0) * 0.56, mods={0: solid})
    sub = place(sub, x0 - bounds(sub)[0] + 6, 78 + 52)
    return dict(main=row, sub=sub, cap=cap)


ALL = {"1_gilt": g1, "2_oak_brass": g2, "3_tin_type": g3, "4_jet_badge": g4, "5_pure": g5}

if __name__ == "__main__":
    # flat proof of the typography (no materials)
    for name, fn in ALL.items():
        G = fn(); items = G["main"] + G["sub"]
        extra = [g for k in ("rules", "studs", "bars", "trail") for g in G.get(k, [])]
        allg = unary_union([g for _, g in items] + extra); b = allg.bounds; m = 50
        c = Canvas(b[2] - b[0] + 2 * m, b[3] - b[1] + 2 * m, scale=0.6)
        sh = lambda g: affinity.translate(g, m - b[0], m - b[1])
        c.over((245, 236, 214), c.mask(sh(allg)))
        if "inlay" in G: c.over((200, 140, 40), c.mask(sh(G["inlay"])))
        if "nails" in G:
            c.over((60, 50, 45), c.mask(sh(unary_union([Point(x, y).buffer(7) for x, y in G["nails"]]))))
        bg = np.zeros_like(c.rgb) + np.array([0.12, 0.11, 0.15], F32)
        c.under(bg, np.ones_like(c.a))
        c.save(f"/tmp/claude-0/-home-user/5210da15-ba2c-5900-b8c2-dc38bd1a885e/scratchpad/flat_{name}.png", trim=False)
        print(name, [round(v) for v in b])
