"""Five capsule layouts: 3D layer = real enemies (+ Trellis Axie). Heroes/Ophelia/logo are composited after (compose_3d.py)."""
import sys, math, random; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-3d")
from scene import *

W, H = 2464, 1412


def lights(key=(55, 0, -35), warm=(1, 0.93, 0.8), fill=(0.75, 0.85, 1.0)):
    sun(rot=key, energy=3.2, color=warm, angle=6)
    area((-6, -10, 6), (2, 2, 1), energy=1800, size=10, color=fill)   # soft front fill
    area((8, 6, 5), (2, 2, 1), energy=1400, size=6, color=(1, 0.8, 0.6))  # warm rim from behind-right


def pin_rack(cx, cy, scale, rows=4, spacing=0.75, rot=0, frame=5):
    for r in range(rows):
        for i in range(r + 1):
            x = cx + (i - r / 2) * spacing * scale; y = cy + r * spacing * scale * 0.9
            add_pin((x, y, 0), rot_z=rot + random.uniform(-8, 8), scale=scale, frame=frame)


def L1():  # SHOWDOWN: horde on the right charging left, Cappy (2D) dominates the left
    random.seed(1)
    add_worm((5.4, 6.0, -0.3), rot_z=-60, scale=2.4, frame=35, anim="hit")
    add_golfer((8.6, -2.2, 0), rot_z=-45, scale=1.1, frame=70)
    add_warboy((5.0, 0.4, 0), rot_z=-25, scale=1.05, pose=WARBOY_POSES["fists"])
    add_warboy((6.6, 2.6, 0), rot_z=-30, scale=1.05, pose=WARBOY_POSES["taunt"])
    for x, y, s in [(2.2, -3.4, 1.9), (3.7, -3.9, 1.9), (5.3, -3.2, 1.9), (7.0, -3.7, 1.9), (3.0, -1.0, 1.75), (6.2, -0.8, 1.75), (7.8, 0.8, 1.7), (4.8, 2.6, 1.7)]:
        add_pin((x, y, 0), rot_z=-30 + random.uniform(-12, 12), scale=s, frame=random.choice([3, 8, 12]))
    add_axie((0.6, -2.0, 3.9), rot_z=80, scale=1.5, tilt=-8)
    shadow_catcher(); lights()
    camera((1.6, -11.5, 1.3), (3.4, 0.5, 1.7), lens=33)


def L2():  # CANYON COLOSSUS: one giant worm erupting centre-right, pins scattering
    random.seed(2)
    add_worm((2.6, 5.5, -0.6), rot_z=-75, scale=3.2, frame=35, anim="hit")
    for x, y in [(0.9, 0.4), (4.4, 0.9), (5.6, -0.8), (3.1, -1.8), (6.4, 2.2), (1.8, 2.8)]:
        add_pin((x, y, 0), rot_z=random.uniform(-70, 20), scale=1.8, frame=random.choice([3, 8, 12]))
    add_golfer((7.2, 1.0, 0), rot_z=-40, scale=1.0, frame=55)
    add_axie((-2.4, 0.5, 4.2), rot_z=70, scale=1.6, tilt=-12)
    shadow_catcher(); lights(key=(60, 0, -20))
    camera((1.4, -9.0, 0.9), (2.8, 3.0, 2.9), lens=27)


def L3():  # STRIKE: real bowling-pin rack down the lane, golfer foreground, warboys flanking
    random.seed(3)
    pin_rack(1.2, 7.0, 1.8, rows=4, spacing=0.8, rot=0, frame=1)
    add_golfer((3.6, -0.4, 0), rot_z=-55, scale=1.15, frame=70)
    add_warboy((-3.6, 6.5, 0), rot_z=20, scale=1.0, pose=WARBOY_POSES["cheer"])
    add_warboy((6.0, 7.5, 0), rot_z=-20, scale=1.0, pose=WARBOY_POSES["fists"])
    add_worm((6.8, 12.0, -0.5), rot_z=-90, scale=1.8, frame=60, anim="idle")
    add_axie((-2.0, 1.5, 3.6), rot_z=60, scale=1.4, tilt=-15)
    shadow_catcher(); lights(key=(50, 0, 0))
    camera((0.8, -6.0, 2.1), (1.4, 6, 1.0), lens=30)


def L4():  # SURROUNDED: enemies in an arc around an empty centre where Cappy lands (2D)
    random.seed(4)
    ring = [(-4.0, 1.4), (-3.2, 3.4), (-1.4, 4.6), (2.8, 4.2), (4.2, 2.2), (4.8, 0.0), (-4.6, -0.8)]
    for x, y in ring:
        add_pin((x, y, 0), rot_z=math.degrees(math.atan2(-y, -x)) - 90 + random.uniform(-10, 10), scale=1.8, frame=random.choice([3, 8, 12]))
    add_worm((-1.8, 6.6, 0), rot_z=-70, scale=2.6, frame=35, anim="hit")
    add_warboy((-2.4, 0.6, 0), rot_z=35, scale=1.05, pose=WARBOY_POSES["taunt"])
    add_warboy((2.6, 1.0, 0), rot_z=-35, scale=1.05, pose=WARBOY_POSES["fists"])
    add_golfer((3.6, 5.6, 0), rot_z=-30, scale=1.0, frame=70)
    add_axie((3.4, -1.5, 3.6), rot_z=140, scale=1.3, tilt=-10)
    shadow_catcher(); lights(key=(55, 0, -10))
    camera((0, -8.6, 3.8), (0, 2.0, 1.0), lens=27)


def L5():  # THE MARCH: Ophelia's crew in a single file marching left in profile, shrinking into depth
    random.seed(5)
    seq = [("pin", 1.7), ("warboy", 1.05), ("pin", 1.7), ("golfer", 1.05), ("pin", 1.7), ("warboy", 1.05), ("pin", 1.7)]
    x, y = 0.6, -0.4
    for i, (kind, sc) in enumerate(seq):
        rz = -90 + random.uniform(-6, 6)
        if kind == "pin": add_pin((x, y, 0), rot_z=rz, scale=sc, frame=[3, 8, 12][i % 3])
        elif kind == "warboy": add_warboy((x, y, 0), rot_z=rz, scale=sc, pose=WARBOY_POSES["arms_down"] if i < 3 else WARBOY_POSES["cheer"])
        else: add_golfer((x, y, 0), rot_z=rz, scale=sc, frame=55)
        x += 1.35; y += 1.25
    add_worm((7.0, 9.0, 0), rot_z=-90, scale=2.4, frame=60, anim="idle")
    add_axie((-1.2, -2.4, 2.9), rot_z=95, scale=1.2, tilt=-5)
    shadow_catcher(); lights(key=(45, 0, -60))
    camera((0.2, -8.2, 1.2), (2.8, 3.0, 1.6), lens=30)


if __name__ == "__main__":
    which = sys.argv[1]; samples = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    reset(); globals()[which]()
    render(f"/home/user/capyverse-claude/work/capsules-3d/renders/{which}_3d.png", W, H, samples=samples)
