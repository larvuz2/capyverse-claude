"""Each wordmark on the round-18 Meadow capsule (main size), auto-placed clear of every character."""
import sys
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-r17")
import r18, r15
from r15 import C, os
from PIL import Image
HERE = "/home/user/capyverse-claude/work/logo-aaa"
W0 = {"1_gilt": 0.66, "2_oak_brass": 0.66, "3_tin_type": 0.50, "4_jet_badge": 0.66, "5_pure_ink": 0.66}
for name, wf in W0.items():
    r15.LOGO = f"{HERE}/out/{name}.png"
    glow = (255, 250, 225)
    r18.logo = lambda c, cx, cy, w, rot=0, glow=None, shadow=0.5, wf=wf, g=glow: r15.logo(c, cx, cy, wf * C.W, rot=0, glow=g, shadow=0.45)
    C.W, C.H = 2464, 1412; r15.OBST = None
    c, S = r18.build_1()
    c.grade(contrast=1.05, sat=1.07, vignette=0.2, bloom=0.05)
    os.makedirs(f"{HERE}/mock", exist_ok=True)
    c.canvas.convert("RGB").resize((1232, 706), Image.LANCZOS).save(f"{HERE}/mock/{name}.jpg", quality=93)
    print(name)
