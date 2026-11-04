"""Round 7 compositor: layered backgrounds, 3D enemy mass, a tight hero cluster, and a BIG logo blended into the scene.

Logo blending: the logo sits between depth layers (in front of Ophelia/sky, behind Cappy's gatling and FX), gets a
contact shadow on the scene, takes the scene's rim light and a light colour wrap, so it reads as part of the picture.
"""
import sys, os
sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-v1")
os.chdir("/home/user/capyverse-claude/work/capsules-v1")
from compose import *
from c12g import grad

HERE = "/home/user/capyverse-claude/work/capsules-3d"
LOGO = "/home/user/capyverse-claude/work/logo-lab/out/logo_e4_trim.png"
T = dict(length=260, color=(255, 250, 225), opacity=0.25, angle=195)
FL = dict(flame_len=1.9, flame_w=1.6)


def bg_layer(c, path, y_bottom, width=None, haze=None, blur=0, x=0, flip=False):
    L = load(path)
    if flip: L = L.transpose(Image.FLIP_LEFT_RIGHT)
    w = width or W; L = L.resize((int(w), int(L.height * w / L.width)), Image.LANCZOS)
    a = np.array(L).astype(np.float32); ys, xs = np.nonzero(a[..., 3] > 8)
    L = L.crop((0, ys.min(), L.width, ys.max() + 1))
    if haze:  # atmospheric perspective: tint toward the sky colour
        a = np.array(L).astype(np.float32); a[..., :3] = a[..., :3] * (1 - haze[1]) + np.array(haze[0], np.float32) * haze[1]
        L = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    if blur: L = L.filter(ImageFilter.GaussianBlur(blur))
    c.canvas.alpha_composite(L, (int(x), int(y_bottom - L.height)))


def layer3d(c, name, dx=0, dy=0):
    c.canvas.alpha_composite(load(f"{HERE}/renders/{name}_3d.png").resize((W, H), Image.LANCZOS), (dx, dy))


def logo_blended(c, cx, cy, width, rot=-3, rim=(255, 235, 190), shadow_col=(40, 20, 10)):
    Lg = load(LOGO); h = round(Lg.height * width / Lg.width); Lg = Lg.resize((int(width), h), Image.LANCZOS)
    if rot: Lg = Lg.rotate(rot, Image.BICUBIC, expand=True)
    x, y = cx - Lg.width / 2, cy - Lg.height / 2
    # soft drop shadow cast down-right onto the scene
    c._shadow(Lg, x, y, dx=width * 0.012, dy=width * 0.03, blur=int(width * 0.02), opacity=0.55, color=shadow_col)
    # warm rim light along the top-left edge so the logo sits in the scene's light
    a = np.asarray(Lg.getchannel("A")).astype(np.float32) / 255
    sh = np.roll(np.roll(a, 6, 0), 6, 1); rimm = np.clip(a - sh, 0, 1)
    la = arr(Lg); la[..., :3] = la[..., :3] + (1 - la[..., :3]) * np.array(rim, np.float32) / 255 * (rimm[..., None] * 0.7)
    c.canvas.alpha_composite(img(la), (int(x), int(y)))
    c.glow(cx, cy + h * 0.1, width * 0.9, rim, 0.12)


def heroes(c, base_x, base_y, s=1.0, mirror=False, front=1240):
    """Tight hero cluster: Cappy huge bottom-left; Moody, Axie and Jim stacked as a column at the front line
    (x≈front) right where Cappy's snout meets the enemy mass, drawn in front of him so the group reads as one."""
    f = mirror
    def X(x, w): return (W - x - w) if f else x
    ang = -15 if f else 195
    cappy(c, X(base_x - 80 * s, 1029 * 1.3 * s), base_y, 1.3 * s, flip=f, trail=dict(T, length=360, angle=ang), flame_len=1.7, flame_w=1.5)
    moody(c, X(front + 20, 432 * 0.6), base_y + 60, 0.6, flip=f, trail=dict(T, length=170, angle=ang), **FL)
    axie(c, X(front + 40, 2233 * 0.12), base_y + 300, 0.12, flip=f, trail=dict(T, length=170, angle=ang), **FL)
    jim(c, X(front + 10, 293 * 0.82), base_y + 500, 0.82, flip=f, trail=dict(T, length=160, angle=ang), **FL)


CANYON = dict(sky=(f"{HERE}/bg/canyon_sky_0.png", (0.5, 0.3)), mid=f"{HERE}/bg/canyon_mountains_cut_0.png",
              fg=f"{HERE}/bg/canyon_rocks_cut_0.png", haze=(240, 205, 150))
WASTE = dict(sky=(f"{HERE}/bg/waste_sky_0.png", (0.5, 0.4)), mid=f"{HERE}/bg/waste_mid_cut_0.png",
             fg=f"{HERE}/bg/waste_rocks_cut_0.png", haze=(255, 150, 110))


def layered(world, horizon):
    c = Comp(world["sky"][0], focus=world["sky"][1])
    bg_layer(c, world["mid"], horizon, width=W * 1.15, x=-W * 0.07, haze=(world["haze"], 0.35), blur=1.5)
    return c


def build(name):
    if name == "C1":   # CLASH — canyon, layered: sky / mesas / rock ledge
        c = layered(CANYON, 830)
        bg_layer(c, CANYON["fg"], H + 160, width=W * 1.1, x=-W * 0.05)
        layer3d(c, "C1", dy=20)
        logo_blended(c, 760, 300, 1420)
        heroes(c, 40, 640, 1.0)
        sfx(c, "CLASH!", 1420, 620, 96, rot=-8, fill=(255, 230, 60))
    elif name == "C2":  # KING OF THE HILL — wasteland, layered: sky / scrap skyline / junk piles
        c = layered(WASTE, 800)
        bg_layer(c, WASTE["fg"], H + 30, width=W * 1.1, x=-W * 0.05)
        layer3d(c, "C2")
        logo_blended(c, 640, 270, 1180, rim=(255, 190, 150), shadow_col=(40, 10, 30))
        heroes(c, 40, 660, 1.0)
        sfx(c, "BOOM!", 1260, 640, 90, rot=-10, fill=(255, 120, 80))
    elif name == "C3":  # DIAGONAL CHARGE — brand sunburst, the wave pours diagonally at the heroes
        c = Comp("plates_used/01_sunburst_nbp_1.jpg", focus=(0.6, 0.35))
        c.speed_lines(2300, 120, n=60, inner=0.25, color=(255, 250, 225), opacity=0.16, width=10, seed=71)
        layer3d(c, "C3")
        logo_blended(c, 700, 250, 1300)
        heroes(c, 40, 680, 1.0)
        sfx(c, "INCOMING!", 1180, 1180, 84, rot=-6, fill=(255, 245, 210))
    elif name == "C4":  # LOW HERO ANGLE — big sky on the brand gradient, the horde towers from below
        c = Comp(grad([(0, (255, 236, 120)), (0.45, (255, 212, 38)), (1, (255, 120, 20))], kind="radial", center=(0.45, 0.3)))
        layer3d(c, "C4")
        logo_blended(c, 760, 330, 1500)
        heroes(c, 60, 720, 0.98)
        sfx(c, "UH-OH!", 1350, 760, 84, rot=8, fill=(255, 245, 210))
    elif name == "C5":  # PHOTO BOMB — Ophelia's crew huddles for a selfie, Cappy photobombs; canyon layers
        c = layered(CANYON, 860)
        bg_layer(c, CANYON["fg"], H + 330, width=W * 1.2, x=-W * 0.1)
        layer3d(c, "C5")
        logo_blended(c, 700, 280, 1260)
        heroes(c, 40, 650, 1.0)
        sfx(c, "SAY CHEESE!", 1600, 720, 72, rot=6, fill=(255, 245, 210))
    c.grade(contrast=1.05, sat=1.06, vignette=0.3)
    c.save(f"cap7_{name}", f"{HERE}/out")


if __name__ == "__main__":
    for n in (sys.argv[1:] or ["C1", "C2", "C3", "C4", "C5"]): build(n)
