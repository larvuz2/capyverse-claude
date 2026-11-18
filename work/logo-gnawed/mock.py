"""Each Gnawed variant on the current capsule (round 18 · Meadow) at the three Steam sizes, logo auto-placed clear
of every character and as big as the free space allows."""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r17")
import r18, r15
from r15 import C, os
from PIL import Image
HERE = "/home/user/capyverse-claude/work/logo-gnawed"
NAMES = [a for a in sys.argv[1:] if a[0].isdigit()] or ["1_nibbled", "2_chewed", "3_devoured", "4_walnut", "5_painted"]
SIZES = [a for a in sys.argv[1:] if a in r18.SIZES] or ["main", "header", "small"]
os.makedirs(f"{HERE}/mock", exist_ok=True)
base_logo = r15.logo
for name in NAMES:
    r15.LOGO = f"{HERE}/out/{name}.png"
    r18.logo = lambda c, cx, cy, w, rot=0, glow=None, shadow=0.5: base_logo(c, cx, cy, w * 1.06, rot=rot, glow=glow, shadow=shadow)
    for sz in SIZES:
        tw, th, k = r18.SIZES[sz]; C.W, C.H = tw * k, th * k; r15.OBST = None
        print(name, sz)
        c, S = (r18.build_small("1") if sz == "small" else r18.build_1())
        c.grade(contrast=1.05, sat=1.07, vignette=0.2, bloom=0.05)
        c.canvas.convert("RGB").resize((tw, th), Image.LANCZOS).save(f"{HERE}/mock/{name}_{sz}_{tw}x{th}.jpg", quality=94)
