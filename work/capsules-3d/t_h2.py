import sys; sys.path.insert(0, ".")
from scene import *
reset()
for i, r in enumerate([(0,0,0),(90,0,0),(-90,0,0),(90,0,180),(-90,0,180),(90,180,0)]):
    add_warboy((i * 1.6, 0, 0), pose={"UpperArm_L": (0,0,-70), "UpperArm_R": (0,0,-70)}, head=dict(rot=r), name=f"w{i}")
camera((4, -14, 1.2), (4, 0, 1.2), lens=45)
sun(); area((4, -6, 4), (4, 0, 1), energy=800, size=8)
render("tests/h2.png", 2000, 600, samples=10)
