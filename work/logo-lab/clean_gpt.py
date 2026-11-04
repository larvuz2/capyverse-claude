"""Manual clean-up of the GPT 2.5 Stumble-style logo.

The model fills every gap between letters and rows with pure black, so the outline pools into blobs.
This rebuilds the outline from the letters themselves:
1. split pixels into background (flood-filled from the border), black outline, and letters
2. new outline = letters grown by a fixed radius, plus the same shape shifted down-right as one 3D block
3. old black outside the new outline becomes transparent; the outline is recoloured to brand navy
Result: an even outline, small gaps still fused (one object), big black blobs gone, transparent PNG.
"""
import sys
import numpy as np
import cv2
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
R = int(sys.argv[3]) if len(sys.argv) > 3 else 22          # outline radius in px
EX = (int(sys.argv[4]) if len(sys.argv) > 4 else 16, int(sys.argv[5]) if len(sys.argv) > 5 else 26)  # 3D offset
NAVY = np.array([29, 18, 64], np.float32)

im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
h, w = im.shape[:2]
lum = im @ np.array([0.299, 0.587, 0.114])
dark = (lum < 70).astype(np.uint8)

# background = everything light that connects to the image border
light = (1 - dark).astype(np.uint8)
n, lab = cv2.connectedComponents(light, connectivity=4)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
bg = np.isin(lab, [b for b in border if b != 0]) & (light == 1)
letters = (~bg) & (dark == 0)
# drop specks
nl, ll, st, _ = cv2.connectedComponentsWithStats(letters.astype(np.uint8), connectivity=8)
keep = np.zeros_like(letters)
for i in range(1, nl):
    if st[i, cv2.CC_STAT_AREA] > 400: keep |= ll == i
letters = keep

disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * R + 1, 2 * R + 1))
grown = cv2.dilate(letters.astype(np.uint8), disk)
# close small gaps so neighbouring letters fuse into one shape, without flooding big areas
grown = cv2.morphologyEx(grown, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (R + 1, R + 1)))
M = np.float32([[1, 0, EX[0]], [0, 1, EX[1]]])
block = np.maximum(grown, cv2.warpAffine(grown, M, (w, h)))
for k in np.linspace(0, 1, 6)[1:-1]:  # fill the extrusion sweep
    Mk = np.float32([[1, 0, EX[0] * k], [0, 1, EX[1] * k]])
    block = np.maximum(block, cv2.warpAffine(grown, Mk, (w, h)))

shape = np.maximum(block, letters.astype(np.uint8))
alpha = cv2.GaussianBlur(shape.astype(np.float32), (0, 0), 1.1)
rgb = im.copy()
outline_px = (shape == 1) & (~letters)
rgb[outline_px] = NAVY
# letter edge pixels that were dark-ish anti-aliasing: blend toward navy instead of black
edge = letters & (lum < 110)
rgb[edge] = rgb[edge] * 0.4 + NAVY * 0.6
rgba = np.dstack([rgb, alpha * 255]).clip(0, 255).astype(np.uint8)
ys, xs = np.nonzero(alpha > 0.02)
Image.fromarray(rgba).crop((xs.min() - 4, ys.min() - 4, xs.max() + 5, ys.max() + 5)).save(out)
print("letters px", int(letters.sum()), "saved", out)
