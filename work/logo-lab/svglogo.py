"""Tiny SVG lettering toolkit: real font outlines -> editable SVG paths, laid out per glyph."""
import subprocess, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))


class Font:
    def __init__(self, name):
        self.f = TTFont(f"{HERE}/fonts/{name}.ttf")
        self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.asc = self.f["hhea"].ascent

    def glyph(self, ch, size):
        """SVG path d for one character, y-down, baseline at 0, scaled to `size` px em."""
        gn = self.cmap[ord(ch)]; g = self.gs[gn]; s = size / self.upm
        pen = SVGPathPen(self.gs)
        g.draw(TransformPen(pen, (s, 0, 0, -s, 0, 0)))
        bp = BoundsPen(self.gs); g.draw(TransformPen(bp, (s, 0, 0, -s, 0, 0)))
        return pen.getCommands(), g.width * s, bp.bounds  # bounds: xmin, ymin, xmax, ymax (y-down)

    def word(self, text, size, tracking=0.0):
        """[(char, d, x, advance, bounds)] laid out left to right."""
        out, x = [], 0.0
        for ch in text:
            if ch == " ": x += size * 0.3; continue
            d, adv, b = self.glyph(ch, size)
            out.append((ch, d, x, adv, b)); x += adv + tracking * size
        return out, x - tracking * size


def render(svg_path, png_path, width=2000, bg="transparent"):
    subprocess.run(["node", f"{HERE}/render.js", svg_path, png_path, str(width), bg], check=True, cwd=HERE)
