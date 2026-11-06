"""Matte pass: pull bright, low-saturation specular hotspots back toward the local surface colour."""
import numpy as np, cv2
from PIL import Image

def degloss(im, strength=0.85, rad=21, thr=0.10):
    a = np.asarray(im.convert("RGBA")).astype(np.float32) / 255
    rgb, al = a[..., :3], a[..., 3]
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    L = lab[..., 0] / 100
    # local surface luminance estimate, ignoring transparent pixels
    w = (al > 0.5).astype(np.float32)
    Lm = cv2.GaussianBlur(L * w, (0, 0), rad) / np.maximum(cv2.GaussianBlur(w, (0, 0), rad), 1e-3)
    chroma = np.hypot(lab[..., 1], lab[..., 2]) / 60
    spec = np.clip((L - Lm - thr) / 0.15, 0, 1) * np.clip(1.2 - chroma, 0, 1) * w
    spec = cv2.GaussianBlur(spec, (0, 0), 2)
    lab[..., 0] = (L - (L - Lm) * spec * strength) * 100
    # restore some chroma where the highlight bleached it
    am = cv2.GaussianBlur(lab[..., 1] * w, (0, 0), rad) / np.maximum(cv2.GaussianBlur(w, (0, 0), rad), 1e-3)
    bm = cv2.GaussianBlur(lab[..., 2] * w, (0, 0), rad) / np.maximum(cv2.GaussianBlur(w, (0, 0), rad), 1e-3)
    lab[..., 1] += (am - lab[..., 1]) * spec * strength * 0.7
    lab[..., 2] += (bm - lab[..., 2]) * spec * strength * 0.7
    out = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    return Image.fromarray((np.dstack([np.clip(out, 0, 1), al]) * 255).astype(np.uint8), "RGBA")
