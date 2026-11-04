"""Round 7: five crafted compositions. Enemies packed into one mass on the right, heroes clustered on the left.
Each layout = actors + camera, then pack.tighten() closes gaps before rendering."""
import sys, math, random; sys.path.insert(0, "/home/user/capyverse-claude/work/capsules-3d")
from scene import *
from pack import tighten, frame_to

W, H = 2464, 1412


def lights(key=(55, 0, -35)):
    sun(rot=key, energy=3.4, color=(1, 0.93, 0.8), angle=6)
    area((-6, -10, 6), (3, 2, 1), energy=1800, size=10, color=(0.8, 0.88, 1.0))
    area((10, 8, 6), (4, 2, 1), energy=2200, size=6, color=(1, 0.75, 0.55))


def horde(cx, cy, n_pins=8, warboys=("punch", "point", "fist_up"), golfer=True, worm=True, spread=1.0, face=-30, seed=1):
    """A dense, varied enemy mass around (cx, cy). Returns all roots."""
    random.seed(seed); roots = []
    if worm: roots.append(add_worm((cx + 1.2 * spread, cy + 2.2 * spread, -0.4), rot_z=face - 30, scale=2.2, frame=35, anim="hit", name="worm"))
    for i, p in enumerate(warboys):
        a = i / max(1, len(warboys) - 1) - 0.5
        r, _ = add_warboy((cx + a * 2.4 * spread, cy + 0.6 * spread + random.uniform(-0.3, 0.3), 0), rot_z=face + random.uniform(-12, 12),
                          scale=1.05, pose=WARBOY_POSES[p], name=f"warboy{i}")
        roots.append(r)
    if golfer:
        g, _ = add_golfer((cx + 1.9 * spread, cy - 0.6 * spread, 0), rot_z=face - 20, scale=1.08, frame=70, name="golfer"); roots.append(g)
    for i in range(n_pins):
        ang = random.uniform(0, 2 * math.pi); rad = random.uniform(0.6, 2.2) * spread
        x, y = cx + math.cos(ang) * rad * 1.3, cy - 1.2 * spread + abs(math.sin(ang)) * rad * 0.6 - (i % 3) * 0.5
        roots.append(add_pin((x, y, 0), rot_z=face + random.uniform(-25, 25), scale=1.7 + random.uniform(-0.1, 0.15),
                             frame=random.choice([3, 8, 12, 16]), name=f"pin{i}"))
    return roots


# 1 CLASH — two walls meeting in the middle, Ophelia looming over her army, logo floats top-centre.
def C1():
    o = add_ophelia((5.0, 9.5, 0), rot_z=-20, scale=9.0)
    roots = horde(3.4, 2.0, n_pins=9, seed=11)
    camera((0.0, -10.0, 1.6), (1.4, 2.0, 2.4), lens=28)
    tighten(roots, (3.4, 1.8), target=0.32, keep=("worm",))
    frame_to(roots + [o], (0.40, 0.04, 0.99, 0.99))
    shadow_catcher(); lights()


# 2 KING OF THE HILL — enemies piled on a rising slope toward Ophelia at the summit; worm wraps the hill.
def C2():
    o = add_ophelia((3.4, 11.0, 1.4), rot_z=-10, scale=8.0)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=6, location=(3.0, 9.0, -4.2), segments=24, ring_count=12)
    hill = bpy.context.object; hill.scale = (1.3, 1.0, 1.0)
    hill_root = bpy.data.objects.new("hill_root", None); bpy.context.scene.collection.objects.link(hill_root); hill.parent = hill_root
    m = bpy.data.materials.new("hill"); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.55, 0.25, 0.1, 1)
    hill.data.materials.append(m)
    for p in hill.data.polygons: p.use_smooth = False
    roots = horde(2.6, 3.0, n_pins=10, warboys=("fist_up", "both_point", "punch", "taunt"), seed=22, spread=1.1)
    camera((-1.0, -9.0, 0.6), (1.6, 3.0, 2.8), lens=26)
    tighten(roots, (2.6, 2.8), target=0.32, keep=("worm",))
    frame_to(roots + [o], (0.42, 0.04, 0.99, 0.97))
    shadow_catcher(); lights(key=(40, 0, -50))


# 3 DIAGONAL CHARGE — enemy wave pours from top-right to bottom-centre along a diagonal; heroes break it.
def C3():
    o = add_ophelia((8.0, 12.0, 0), rot_z=-35, scale=9.5)
    roots = []
    random.seed(33)
    for i in range(12):
        t = i / 11; x = 1.2 + t * 6.0; y = -0.6 + t * 7.5
        roots.append(add_pin((x + random.uniform(-0.6, 0.6), y + random.uniform(-0.4, 0.4), 0), rot_z=-60 + random.uniform(-15, 15),
                             scale=1.75, frame=random.choice([3, 8, 12]), name=f"pin{i}"))
    for i, (t, p) in enumerate([(0.15, "punch"), (0.45, "point"), (0.7, "fist_up")]):
        r, _ = add_warboy((1.8 + t * 6.0, 0.4 + t * 7.5, 0), rot_z=-55, scale=1.05, pose=WARBOY_POSES[p], name=f"warboy{i}"); roots.append(r)
    g, _ = add_golfer((3.6, 0.2, 0), rot_z=-60, scale=1.1, frame=70, name="golfer"); roots.append(g)
    roots.append(add_worm((6.2, 6.8, -0.4), rot_z=-90, scale=2.6, frame=35, anim="hit", name="worm"))
    camera((-0.5, -8.5, 4.5), (2.6, 3.0, 0.8), lens=26)
    tighten(roots, (3.4, 2.6), target=0.36, keep=("worm",))
    frame_to(roots + [o], (0.30, 0.04, 0.97, 0.99))
    shadow_catcher(); lights(key=(60, 0, -20))


# 4 LOW HERO ANGLE — worm's-eye camera: the horde towers over the viewer, sky dominant for a huge logo.
def C4():
    o = add_ophelia((4.0, 10.0, 0), rot_z=-15, scale=10.0)
    roots = horde(3.0, 2.4, n_pins=7, warboys=("both_point", "punch"), seed=44, spread=0.9)
    camera((0.4, -5.5, 0.25), (2.0, 3.0, 2.6), lens=22)
    tighten(roots, (3.0, 2.2), target=0.32, keep=("worm",))
    frame_to(roots + [o], (0.42, 0.20, 0.99, 1.00))
    shadow_catcher(); lights(key=(35, 0, -25))


# 5 PHOTO BOMB — tight huddle around the golfer as if posing for a viral photo; Ophelia leans in.
def C5():
    o = add_ophelia((3.0, 6.5, 0), rot_z=-5, scale=7.0)
    roots = horde(2.8, 1.6, n_pins=8, warboys=("point", "fist_up", "both_point", "taunt"), seed=55, spread=0.75, face=-15)
    camera((1.2, -7.0, 1.7), (2.6, 2.0, 1.9), lens=30)
    tighten(roots, (2.8, 1.4), target=0.28, keep=("worm",))
    frame_to(roots + [o], (0.38, 0.06, 0.99, 0.99))
    shadow_catcher(); lights(key=(50, 0, -15))


if __name__ == "__main__":
    which = sys.argv[1]; samples = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    reset(); globals()[which]()
    render(f"/home/user/capyverse-claude/work/capsules-3d/renders/{which}_3d.png", W, H, samples=samples)
