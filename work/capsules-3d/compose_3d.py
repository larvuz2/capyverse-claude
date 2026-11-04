"""Composite the Blender 3D enemy layer with the real Unreal hero renders, Ophelia, FX and the logo.

Stack (back to front): plate -> Ophelia (2D render, behind everything) -> Blender 3D layer (real enemy meshes,
Trellis Axie, contact shadows) -> heroes (real Unreal render cut-outs) -> FX -> onomatopoeias -> logo.
"""
import sys, os
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
from compose import *
from c12g import grad

HERE = "/home/user/capyverse-claude/work/capsules-3d"
LOGO = "/home/user/capyverse-claude/work/logo-lab/out/logo_e4_trim.png"


def ophelia(c, x, y, s, **kw):
    kw.setdefault("rim", dict(color=(255, 230, 200), dir=(-1, -1), width=8, strength=0.6)); kw.setdefault("match", 0.18)
    c.place("ophelia_head", x, y, scale=s, **kw)
    for ex, ey in ((165, 520), (453, 496)): c.glow(x + ex * s, y + ey * s, 110 * s / 1.5, (255, 40, 40), 0.65)


def layer3d(c, name):
    L = load(f"{HERE}/renders/{name}_3d.png")
    c.canvas.alpha_composite(L.resize((W, H), Image.LANCZOS))


T = dict(length=260, color=(255, 250, 225), opacity=0.25, angle=195)
FL = dict(flame_len=1.9, flame_w=1.6)

CFG = {
    "L1": dict(plate=("plate", "plates_used/01_sunburst_nbp_1.jpg", (0.5, 0.35)), oph=(W - 613 * 1.45 + 60, -110, 1.45),
               cappy=(-80, 600, 1.3), moody=(1180, 90, 0.55), jim=(30, 470, 0.62), logo=(600, 200, 900),
               sfx=[("POP! POP!", 1240, 520, 72, -10, (255, 245, 210)), ("CHOMP!", 1500, 380, 66, 8, (255, 110, 80))]),
    "L2": dict(plate=("plate", "plates_used/v2_canyon_colossus_nbp_0.jpg", (0.5, 0.5)), oph=None,
               cappy=(-60, 640, 1.3), moody=(1900, 80, 0.55, True), jim=(60, 300, 0.7), logo=(600, 210, 880),
               sfx=[("RUMBLE!", 1600, 980, 76, 6, (255, 200, 90)), ("POP!", 1220, 600, 64, -10, (255, 245, 210))]),
    "L3": dict(plate=("plate", "plates_used/06_strike_nbp_0.jpg", (0.5, 0.5)), oph=(W - 613 * 1.2 + 80, -60, 1.2, 0.85),
               cappy=(-40, 640, 1.25), moody=(1650, 40, 0.5, True), jim=(80, 260, 0.68), logo=(1232, 190, 820),
               sfx=[("STRIKE!", 1200, 560, 80, -6, (255, 230, 60)), ("FORE!", 2050, 560, 70, 8, (255, 230, 60))]),
    "L4": dict(plate=("grad", [(0, (255, 236, 120)), (0.45, (255, 212, 38)), (1, (255, 120, 20))], "radial"), oph=(1232 - 613 * 1.25 / 2, -150, 1.25, 0.9),
               cappy=(560, 520, 1.15), moody=(1900, 120, 0.5, True), jim=(120, 120, 0.62), logo=(560, 190, 760),
               sfx=[("SURROUNDED?!", 1232, 1290, 70, -3, (255, 245, 210))]),
    "L5": dict(plate=("plate", "plates_used/v2_dusk_dunes_nbp_0.jpg", (0.5, 0.5)), oph=(W - 613 * 1.5 + 40, 880 - 930 * 1.5, 1.5, 0.75),
               cappy=(1300, 620, 1.2, True), moody=(1450, 120, 0.5, True), jim=(1900, 380, 0.65, True), logo=(600, 210, 900),
               sfx=[("MARCH! MARCH!", 760, 1180, 62, -4, (255, 230, 200))]),
}


def build(name):
    cfg = CFG[name]
    kind = cfg["plate"][0]
    if kind == "plate":
        c = Comp(cfg["plate"][1], focus=cfg["plate"][2])
    else:
        c = Comp(grad(cfg["plate"][1], kind=cfg["plate"][2], center=(0.5, 0.35)))
    if cfg["oph"]:
        x, y, s, *rest = cfg["oph"]
        ophelia(c, x, y, s, bright=rest[0] if rest else 1.0)
    layer3d(c, name)
    # heroes: real Unreal render cut-outs, Cappy always the biggest
    mx, my, ms, *mf = cfg["moody"]; moody(c, mx, my, ms, flip=bool(mf and mf[0]), trail=dict(T, length=150, angle=-15 if mf and mf[0] else 195), **FL)
    jx, jy, js, *jf = cfg["jim"]; jim(c, jx, jy, js, flip=bool(jf and jf[0]), trail=dict(T, length=140, angle=-15 if jf and jf[0] else 195), **FL)
    cx, cy, cs, *cf = cfg["cappy"]; cappy(c, cx, cy, cs, flip=bool(cf and cf[0]), trail=dict(T, length=340, angle=-15 if cf and cf[0] else 195), flame_len=1.7, flame_w=1.5)
    for text, x, y, size, rot, col in cfg["sfx"]: sfx(c, text, x, y, size, rot=rot, fill=col)
    lx, ly, lw = cfg["logo"]; c.logo(lx, ly, lw, path=LOGO, shadow=0.5)
    c.grade(contrast=1.05, sat=1.06, vignette=0.32)
    c.save(f"cap3d_{name}", f"{HERE}/out")


if __name__ == "__main__":
    for n in (sys.argv[1:] or CFG): build(n)
