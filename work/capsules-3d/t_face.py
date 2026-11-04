import sys, math; sys.path.insert(0, ".")
from scene import *
reset()
for i, rz in enumerate([0, 90, 180, -90]):
    add_pin((i * 2.2 - 3.3, 0, 0), rot_z=rz, scale=2.2, frame=5)
    add_warboy((i * 2.2 - 3.3, 3, 0), rot_z=rz, pose=WARBOY_POSES["arms_down"])
camera((0, -14, 2.0), (0, 1.5, 1.0), lens=35); sun(); area((-2, -6, 4), (0, 0, 1), energy=900, size=8)
render("tests/face.png", 1600, 700, samples=8)
