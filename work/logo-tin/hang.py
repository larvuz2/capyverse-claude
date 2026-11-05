"""Hand edit of the Tin-on-Wood logo: ODYSSEY plank hangs from two short iron chains.
(No image model: FAL balance was exhausted.) Steps: upscale -> key out grey bg -> split plank/blocks ->
move + enlarge plank -> draw chains and screw-eyes -> rebuild cream keyline -> transparent PNG."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

K = 2.5
src = Image.open("src.png").convert("RGB")
src = src.resize((int(src.width * K), int(src.height * K)), Image.LANCZOS)
a = np.asarray(src).astype(np.int32)

# 1. key out the flat grey background (flood from the border)
bgc = np.median(a[:30].reshape(-1, 3), axis=0)
near = np.abs(a - bgc).sum(-1) < 22
lab, _ = ndimage.label(near)
edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
fg = ~np.isin(lab, list(edge))
fg = ndimage.binary_opening(fg, iterations=1)
alpha = ndimage.gaussian_filter(fg.astype(np.float32), 0.8)
# strip the original cream keyline everywhere; a new one is rebuilt at the end
creamk = (a[..., 0] > 228) & (a[..., 1] > 214) & (a[..., 2] > 190) & (np.abs(a[..., 0] - a[..., 2]) > 12)
edge_band = fg & ~ndimage.binary_erosion(fg, iterations=int(9 * K))
alpha[creamk & edge_band] = 0
rgba = np.dstack([a, alpha * 255]).astype(np.uint8)

# 2. split: plank = region below the block line, inside the plank's x span
PX0, PX1, PTOP, PBOT = int(352 * K), int(748 * K), int(347 * K), int(446 * K)
PLANK_TOP = int(352 * K)  # plank face starts a few px below the block line
plank = rgba.copy(); plank[..., 3] = 0
plank[PTOP:PBOT, PX0:PX1] = rgba[PTOP:PBOT, PX0:PX1]
blocks = rgba.copy(); blocks[PTOP:, PX0:PX1, 3] = 0
# drop the old cream keyline strip that hugged the plank top between blocks
P = Image.fromarray(plank).crop((PX0, PLANK_TOP, PX1, PBOT))
pa = np.asarray(P).copy()
cream = (pa[..., 0] > 225) & (pa[..., 1] > 210) & (pa[..., 2] > 185)
pa[..., 3][cream] = 0
# keep only the plank's own solid body (drops slivers of block bottoms caught in the crop)
m = pa[..., 3] > 40
m = ndimage.binary_opening(m, iterations=14)
lb, n = ndimage.label(m)
if n:
    big_id = 1 + np.argmax(ndimage.sum(m, lb, range(1, n + 1)))
    keep = ndimage.binary_dilation(lb == big_id, iterations=10) & (pa[..., 3] > 0)
    pa[..., 3] = np.where(keep, pa[..., 3], 0)
P = Image.fromarray(pa)
B = Image.fromarray(blocks)

# 3. new layout: enlarge plank 1.2x, hang it with a gap for the chains, tilt 2 degrees
S = 1.2
P = P.resize((int(P.width * S), int(P.height * S)), Image.LANCZOS)
gap = int(120)
W, H = B.width, B.height + int(P.height * 0.6) + gap
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.alpha_composite(B)
cx = (PX0 + PX1) / 2
px, py = int(cx - P.width / 2), PTOP + gap + 10
Pr = P.rotate(-2, Image.BICUBIC, expand=True)
# chain anchors: under the 2nd and 2nd-last block over the plank, down to the plank's top corners
ax = [cx - P.width * 0.36, cx + P.width * 0.36]
top_y = PTOP - 6
bot_y = [py + 2 + P.width * 0.36 * math.sin(math.radians(2)) * (-1 if i == 0 else 1) + (Pr_h_off := 0) for i in range(2)]

d = ImageDraw.Draw(canvas)
IRON, HI, DARK = (58, 54, 52, 255), (140, 136, 130, 255), (28, 26, 25, 255)


def eye(x, y, r=13):
    d.ellipse([x - r, y - r, x + r, y + r], outline=DARK, width=11)
    d.ellipse([x - r + 3, y - r + 3, x + r - 3, y + r - 3], outline=IRON, width=5)
    d.arc([x - r + 3, y - r + 3, x + r - 3, y + r - 3], 200, 250, fill=HI, width=3)


def chain(x, y0, y1):
    n = 4; L = (y1 - y0) / n
    for k in range(n):
        yc = y0 + L * (k + 0.5)
        if k % 2 == 0:   # face-on oval link
            d.ellipse([x - 19, yc - L * 0.64, x + 19, yc + L * 0.64], outline=DARK, width=14)
            d.ellipse([x - 17, yc - L * 0.61, x + 17, yc + L * 0.61], outline=IRON, width=8)
            d.arc([x - 14, yc - L * 0.57, x + 14, yc + L * 0.57], 200, 260, fill=HI, width=4)
        else:            # edge-on link
            d.rounded_rectangle([x - 9, yc - L * 0.64, x + 9, yc + L * 0.64], radius=9, fill=DARK)
            d.rounded_rectangle([x - 5, yc - L * 0.6, x + 5, yc + L * 0.6], radius=5, fill=IRON)


for i in range(2):
    chain(ax[i], top_y + 10, bot_y[i] + 4)
canvas.alpha_composite(Pr, (px - (Pr.width - P.width) // 2, py - (Pr.height - P.height) // 2))
d = ImageDraw.Draw(canvas)
for i in range(2):
    eye(ax[i], top_y + 8, 16); eye(ax[i], bot_y[i] + 12, 15)

# 4. rebuild one cream keyline around everything
al = canvas.getchannel("A")
pad = 30
big = Image.new("RGBA", (W + 2 * pad, H + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(canvas, (pad, pad))
ka = big.getchannel("A").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.2))
key = Image.new("RGBA", big.size, (253, 243, 226, 0)); key.putalpha(ka)
key.alpha_composite(big)
arr = np.asarray(key)[..., 3]; ys, xs = np.nonzero(arr > 8)
out = key.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
out.save("tin_hanging.png"); print(out.size)
