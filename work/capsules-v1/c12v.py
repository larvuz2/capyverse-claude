from compose import *
import shaders, colorsys

# SHOWDOWN STACK — 5 variations of #12 (Gus's pick).
# Fixes for all: Cappy moved left so he no longer overlaps the worm, bigger side-belt thrusters,
# a detailed golf shot (ball struck off the tee, flying at Cappy), small comic onomatopoeias.
FL = dict(flame_len=1.9, flame_w=1.6)  # bigger thrusters, still from the side-belt jetpacks


def hue_shift(im, deg, sat=1.0):
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255
    import cv2
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    hsv[..., 0] = (hsv[..., 0] + deg) % 360; hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 1)
    return Image.fromarray((cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) * 255).astype(np.uint8)).convert("RGBA")


def build(name, plate_hue=0, horde=False, ink=False, sfx_set="classic", logo_w=900, oph_s=1.55, cap_s=1.28, grade=None):
    plate = load("plates_used/01_sunburst_gpt_0.jpg")
    if plate_hue: plate = hue_shift(plate, plate_hue, 1.05)
    c = Comp(plate, focus=(0.5, 0.3))
    rim_col = (255, 238, 190) if not plate_hue else (255, 200, 240)
    RR = dict(color=rim_col, dir=(-1, -1), width=7, strength=0.7)
    # Ophelia towers behind, anchored on the right edge
    ox, oy = W - 613 * oph_s + 40, -150 - (oph_s - 1.55) * 600
    c.place("ophelia_head", ox, oy, scale=oph_s, rim=RR, match=0.12)
    for ex, ey in ((165, 520), (453, 496)): c.glow(ox + ex * oph_s, oy + ey * oph_s, 110, (255, 40, 40), 0.65)
    if horde:  # extra crowd stacked between the worm and Ophelia
        rnd = np.random.default_rng(7)
        for x in np.linspace(1500, 2420, 7):
            sc = 0.12; c.place("pin", x - 635 * sc / 2 + rnd.uniform(-20, 20), H - 1553 * sc - 150, scale=sc, rim=RR, match=0.2, bright=0.85)
        c.place("worm_bandits", 1900, H - 659 * 0.75 - 90, scale=0.75, rim=RR, match=0.2, bright=0.85)
    ws = 1.15 if horde else 1.05
    c.place("worm_bandits", 1300, H - 659 * ws + 20, scale=ws, rim=RR, match=0.15)
    gx0, gy0, gs = 1660, H - 544 * 0.95 + 10, 0.95
    c.place("golfer", gx0, gy0, scale=gs, rim=RR, match=0.15)
    for x in np.linspace(1890, 2390, 5):
        sc = 0.17; c.place("pin", x - 635 * sc / 2, H - 1553 * sc + 30, scale=sc, rim=RR, match=0.15)
    # heroes: Cappy dominant on the left, the squad small above
    T = dict(length=260, color=(255, 250, 225), opacity=0.25, angle=195)
    moody(c, 1090, 60, 0.6, trail=dict(T, length=170), **FL)
    axie(c, 1230, 340, 0.11, trail=dict(T, length=170), **FL)
    jim(c, 40, 470, 0.8, trail=dict(T, length=150), **FL)
    cx, cy = 1190 - 1029 * cap_s, 560
    cappy(c, cx, cy, cap_s, trail=dict(T, length=360), flame_len=1.7, flame_w=1.5)
    # golf shot: struck off the tee at the golfer's feet, flying at Cappy
    tee = (gx0 + 70 * gs, H - 18)
    golf_shot(c, tee[0], tee[1], 1222, 690, r=34, bend=-520)
    if ink:
        c.canvas = shaders.ink_cel(c.canvas, colors=22, line=3)
        c.canvas = ImageEnhance.Color(c.canvas.convert("RGB")).enhance(1.25).convert("RGBA")
        c.speed_lines(300, 900, n=40, inner=0.35, color=(255, 255, 255), opacity=0.25, width=8, seed=61, sector=(150, 260))
    # onomatopoeias: small, next to the action that makes the sound
    gtx, gty = anchor("cappy", "cappy_gatling", cx, cy, cap_s)
    mx, my = anchor("moody", "moody_disco", 1090, 60, 0.6)
    k = 1.25 if ink else 1.0
    if sfx_set in ("classic", "loud"):
        sfx(c, "POP! POP!", gtx + 330, gty - 30, 74 * k, rot=-10, fill=(255, 245, 210))
        sfx(c, "FORE!", 1560, 560, 92 * k, rot=8, fill=(255, 230, 60))
        sfx(c, "WHOOSH!", 170, 700, 66 * k, rot=-14, fill=(130, 225, 255))
    if sfx_set == "loud":
        sfx(c, "CHOMP!", 1560, 860, 84, rot=12, fill=(255, 110, 80))
    if sfx_set == "tiny":
        sfx(c, "POP!", gtx + 300, gty - 20, 58, rot=-10, fill=(255, 245, 210))
        sfx(c, "FORE!", 1540, 570, 62, rot=8, fill=(255, 230, 60))
    c.logo(600, 270, logo_w, glow=(255, 250, 220) if not ink else None, shadow=0.6)
    c.grade(**(grade or dict(contrast=1.05, sat=1.07, vignette=0.4)))
    c.save(name, "out")


if __name__ == "__main__":
    import sys
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    V = {
        "a": lambda: build("12a_showdown_classic"),
        "b": lambda: build("12b_showdown_dusk", plate_hue=-38, grade=dict(contrast=1.07, sat=1.05, vignette=0.48, bloom=0.2)),
        "c": lambda: build("12c_showdown_horde", horde=True, sfx_set="loud"),
        "d": lambda: build("12d_showdown_ink", ink=True),
        "e": lambda: build("12e_showdown_clean", sfx_set="tiny", logo_w=1000, oph_s=1.7, grade=dict(contrast=1.07, sat=1.08, vignette=0.5)),
    }
    for k_, f in V.items():
        if which in ("all", k_): f()
