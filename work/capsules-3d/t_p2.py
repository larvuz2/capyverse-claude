import sys, math; sys.path.insert(0, ".")
from scene import *
reset()
for i, p in enumerate(["punch", "point", "both_point", "fist_up", "taunt"]):
    add_warboy((i * 1.5, 0, 0), rot_z=-30, pose=WARBOY_POSES[p], name=p)
o = add_ophelia((9.0, 1.5, 0), rot_z=150, scale=3.0)
mn, mx = bounds(o); print("oph", [round(v,2) for v in mn], [round(v,2) for v in mx])
shadow_catcher(); camera((5, -14, 2.2), (5, 0, 1.6), lens=35); sun(); area((0, -6, 5), (4, 0, 1), energy=1200, size=10)
render("tests/p2.png", 2000, 800, samples=10)
