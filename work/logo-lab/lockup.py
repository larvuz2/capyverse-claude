"""Unified two-row lockup engine (round 3).

- Letters are placed with explicit 2D matrices, so every glyph's real outline is known as a polygon.
- `check()` uses those polygons to report any two letters in a row that touch or overlap (with a safety gap),
  so collisions like the old Y/V in Toybox are caught and fixed by kerning, not by eye.
- `draw()` renders all rows as ONE object: a single sticker silhouette, a single 3D extrusion and a single outline
  under every row, then each row's fill on top. Rows that sit close enough fuse into one shape.
"""
import math
import numpy as np
from fontTools.pens.recordingPen import DecomposingRecordingPen
from shapely.geometry import Polygon
from shapely.ops import unary_union
from svglogo import Font

FONTS = {}


def font(name):
    if name not in FONTS: FONTS[name] = Font(name)
    return FONTS[name]


def mat(a, b, c, d, e, f):
    return np.array([[a, c, e], [b, d, f], [0, 0, 1]], float)


def T(x, y): return mat(1, 0, 0, 1, x, y)
def R(deg):
    r = math.radians(deg); return mat(math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0)
def S(x, y): return mat(x, 0, 0, y, 0, 0)
def K(deg): return mat(1, 0, math.tan(math.radians(deg)), 1, 0, 0)  # skewX


def svgm(M):
    return f"matrix({M[0,0]:.5f},{M[1,0]:.5f},{M[0,1]:.5f},{M[1,1]:.5f},{M[0,2]:.2f},{M[1,2]:.2f})"


def glyph_poly(F, ch, size):
    """Glyph outline as a shapely polygon in the same px space as Font.glyph (y-down, baseline 0)."""
    gs, cmap = F.gs, F.cmap
    pen = DecomposingRecordingPen(gs); gs[cmap[ord(ch)]].draw(pen)
    s = size / F.upm; rings, cur = [], []
    last = (0, 0)
    for op, args in pen.value:
        if op == "moveTo":
            if cur: rings.append(cur)
            cur = [args[0]]; last = args[0]
        elif op == "lineTo":
            cur.append(args[0]); last = args[0]
        elif op in ("qCurveTo", "curveTo"):
            pts = [last] + list(args)
            for t in np.linspace(0, 1, 8)[1:]:  # coarse but fine for collision checks
                q = pts
                while len(q) > 1: q = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(q, q[1:])]
                cur.append(q[0])
            last = args[-1]
        elif op in ("closePath", "endPath"):
            if cur: rings.append(cur); cur = []
    polys = [Polygon([(x * s, -y * s) for x, y in r]).buffer(0) for r in rings if len(r) > 2]
    return unary_union(polys).buffer(0)


class Row:
    def __init__(self, text, fontname, size, cx, base, tracking=0.0, tilt=None, bounce=None, kern=None,
                 arch=0.0, skew=0.0, scale_y=1.0, rot=0.0):
        F = font(fontname); self.F = F; self.size = size
        gl, _ = F.word(text, size, tracking)
        kern = kern or {}
        # apply kerning (cumulative shift from index i onward)
        shift, xs = 0.0, []
        for i, g in enumerate(gl):
            shift += kern.get(i, 0); xs.append(g[2] + shift)
        last = gl[-1]; w = xs[-1] + last[4][2]
        self.items = []
        for i, ((ch, d, x, adv, b), xk) in enumerate(zip(gl, xs)):
            gcx, gcy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            rel = xk + gcx - w / 2
            ang = math.degrees(rel / arch) if arch else 0.0
            px = cx + (arch * math.sin(math.radians(ang)) if arch else rel)
            py = base + (arch * (1 - math.cos(math.radians(ang))) if arch else 0.0) + (bounce[i % len(bounce)] if bounce else 0)
            tl = (tilt[i % len(tilt)] if tilt else 0)
            M = (T(cx, base) @ R(rot) @ T(-cx, -base) @ T(px, py) @ R(ang + tl) @ K(skew) @ S(1, scale_y) @ T(-gcx, -gcy) @ T(0, gcy) @ T(0, -gcy))
            # pivot at the glyph centre; final translate keeps glyph centred on (px, py + gcy-offset)
            M = M @ T(0, gcy)
            self.items.append((ch, d, M, glyph_poly(F, ch, size)))

    def svg_paths(self):
        return "".join(f'<path d="{d}" transform="{svgm(M)}"/>' for _, d, M, _ in self.items)

    def polys(self):
        out = []
        for ch, _, M, P in self.items:
            a, b, c, d, e, f = M[0, 0], M[1, 0], M[0, 1], M[1, 1], M[0, 2], M[1, 2]
            from shapely.affinity import affine_transform
            out.append((ch, affine_transform(P, [a, c, b, d, e, f])))
        return out

    def check(self, gap=4.0):
        """Return [(i, ch_i, ch_j, overlap_area)] for neighbours closer than `gap` px."""
        ps = self.polys(); bad = []
        for i in range(len(ps) - 1):
            (c1, p1), (c2, p2) = ps[i], ps[i + 1]
            if p1.buffer(gap / 2).intersects(p2.buffer(gap / 2)):
                bad.append((i, c1, c2, round(p1.buffer(gap / 2).intersection(p2.buffer(gap / 2)).area, 1)))
        return bad

    def bbox(self):
        return unary_union([p for _, p in self.polys()]).bounds


def draw(rows, fills, ink, stroke, depth, sticker=None, sticker_w=2.6, shine=True, extra_under="", extra_over="",
         depth_dx=0.35, sil_extra=None):
    """rows: [Row]; fills: per-row list of (offset, colour) stops. Everything under the fills is shared."""
    allp = "".join(r.svg_paths() for r in rows)
    # one solid silhouette under all letters: closes any gap between neighbours so the outline never shows holes
    from shapely.geometry import Polygon as _P
    U = unary_union([p for r in rows for _, p in r.polys()] + ([sil_extra] if sil_extra is not None else []))
    sil = U.buffer(stroke * 1.9, join_style=1).buffer(-stroke * 1.45, join_style=1)
    geoms = getattr(sil, "geoms", [sil])
    sil_d = "".join("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in g.exterior.coords) + "Z" for g in geoms)
    allp = f'<path d="{sil_d}" stroke="none"/>' + allp
    defs, fill_layers = [], []
    for k, (r, stops) in enumerate(zip(rows, fills)):
        g = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        top = -r.size * 0.74
        defs.append(f'<linearGradient id="r{k}" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="0">{g}</linearGradient>')
        fill_layers.append(f'<g fill="url(#r{k})">{r.svg_paths()}</g>')
        if shine:
            defs.append(f'<linearGradient id="h{k}" gradientUnits="userSpaceOnUse" x1="0" y1="{top}" x2="0" y2="0">'
                        f'<stop offset="0" stop-color="#fff" stop-opacity="0.6"/><stop offset="0.36" stop-color="#fff" stop-opacity="0"/></linearGradient>')
            fill_layers.append(f'<g fill="url(#h{k})">{r.svg_paths()}</g>')
    ext = "".join(f'<g transform="translate({k * depth_dx:.1f},{k})">{allp}</g>' for k in range(2, depth + 1, 2))
    stk = ""
    if sticker:
        stk = (f'<g fill="{sticker}" stroke="{sticker}" stroke-width="{stroke * sticker_w}" stroke-linejoin="round">'
               f'{allp}<g transform="translate({depth * depth_dx:.1f},{depth})">{allp}</g>{extra_under}</g>')
    return (f'<defs>{"".join(defs)}</defs>{stk}'
            f'<g fill="{ink}" stroke="{ink}" stroke-width="{stroke}" stroke-linejoin="round">{ext}{allp}</g>'
            f'{"".join(fill_layers)}{extra_over}')
