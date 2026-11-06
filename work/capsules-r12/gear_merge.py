"""Keep the true 3D render; take from the AI edit ONLY the pixels it added (gear), via a difference mask."""
import numpy as np, sys
from PIL import Image, ImageFilter
from scipy import ndimage
PICK = {"capy": "gear/nb_capy_0.png", "moody": "gear/nb_moody_0.png", "jim": "gear/nb_jim_1.png"}
for n, f in PICK.items():
    R = Image.open(f"renders/{n}.png").convert("RGBA"); S = R.size
    inp = np.asarray(Image.open(f"gear/in_{n}.png").convert("RGB")).astype(np.float32)
    ai = np.asarray(Image.open(f).convert("RGB").resize(S, Image.LANCZOS)).astype(np.float32)
    # small global colour drift correction measured on unchanged background
    ra = np.asarray(R)[..., 3]
    bgm = ra < 5
    ai = ai - (ai[bgm].mean(0) - inp[bgm].mean(0))
    diff = np.abs(ai - inp).sum(-1)
    m = diff > 70
    m = ndimage.binary_opening(m, iterations=2)
    body = ra > 200
    near = ndimage.binary_dilation(body, iterations=60)
    lab, k = ndimage.label(m)
    keep = np.zeros_like(m)
    for i in range(1, k + 1):
        comp = lab == i
        if comp.sum() > 400 and (comp & body).any():
            keep |= comp
    keep = ndimage.binary_closing(keep, iterations=4); keep = ndimage.binary_fill_holes(keep)
    soft = np.asarray(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
    r = np.asarray(R).astype(np.float32)
    out = r.copy()
    out[..., :3] = r[..., :3] * (1 - soft[..., None]) + np.clip(ai, 0, 255) * soft[..., None]
    out[..., 3] = np.maximum(r[..., 3], soft * 255)
    Image.fromarray(out.astype(np.uint8)).save(f"renders/{n}_gear.png")
    Image.fromarray((keep * 255).astype(np.uint8)).save(f"gear/mask_{n}.png")
    print(n, "gear px", int(keep.sum()), "body px", int(body.sum()))
