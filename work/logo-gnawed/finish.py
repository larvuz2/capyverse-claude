"""Final PNGs for the five Gnawed variants. Cutouts are trimmed; on the walnut variant the ODYSSEY row is separated
from CAPYVERSE by hand (letter bodies -> two groups by height, every other pixel joins the nearest group) and enlarged."""
import numpy as np
from PIL import Image
from scipy import ndimage

BIG_ODYSSEY = {"4_walnut": 1.42}
os_ = __import__("os"); os_.makedirs("out", exist_ok=True)


def split_rows(im):
    a = np.asarray(im).astype(np.float32); al = a[..., 3] > 128
    mx, mn = a[..., :3].max(-1), a[..., :3].min(-1); sat = (mx - mn) / np.maximum(mx, 1)
    body = al & ~((mx > 225) & (sat < 0.22))                       # letters, not the cream keyline
    body = ndimage.binary_opening(body, iterations=3)
    lab, n = ndimage.label(body); sizes = ndimage.sum(body, lab, range(1, n + 1)); cy = ndimage.center_of_mass(body, lab, range(1, n + 1))
    H = im.height; grp = np.zeros(n + 1, np.uint8)
    for i in range(n):
        if sizes[i] > 2500: grp[i + 1] = 2 if cy[i][0] > H * 0.60 else 1
    g = grp[lab]
    idx = ndimage.distance_transform_edt(g == 0, return_distances=False, return_indices=True)
    near = g[idx[0], idx[1]]
    return near == 2                                                # True where the pixel belongs to ODYSSEY


for name in ["1_nibbled", "2_chewed", "3_devoured", "4_walnut", "5_painted"]:
    im = Image.open(f"cut/{name}_0.png").convert("RGBA"); im = im.crop(im.getbbox())
    if name in BIG_ODYSSEY:
        s = BIG_ODYSSEY[name]; a = np.asarray(im).copy(); ody = split_rows(im)
        top = a.copy(); top[ody, 3] = 0; bot = a.copy(); bot[~ody, 3] = 0
        T = Image.fromarray(top); B = Image.fromarray(bot); bb = B.getbbox(); B = B.crop(bb)
        B2 = B.resize((round(B.width * s), round(B.height * s)), Image.LANCZOS)
        tb = T.getbbox(); cx = (tb[0] + tb[2]) / 2
        W = max(im.width, B2.width + 40); Hh = bb[1] + B2.height + 20
        out = Image.new("RGBA", (W, Hh), (0, 0, 0, 0)); ox = (W - im.width) // 2
        out.alpha_composite(B2, (round(ox + cx - B2.width / 2), bb[1] + 4))
        out.alpha_composite(T, (ox, 0)); im = out.crop(out.getbbox())
    im.save(f"out/{name}.png"); print(name, im.size)
