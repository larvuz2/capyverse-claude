import sys; sys.path.insert(0, ".")
from scene import *
reset()
V = [(0,0,70),(0,0,-70),(70,0,0),(-70,0,0),(0,70,0),(0,-70,0)]
for i, v in enumerate(V):
    add_warboy((i * 1.6, 0, 0), pose={"UpperArm_L": v, "UpperArm_R": v}, name=f"w{i}")
camera((4, -14, 1.2), (4, 0, 1.2), lens=45)
sun(); area((4, -6, 4), (4, 0, 1), energy=800, size=8)
render("tests/pose.png", 2000, 600, samples=10)
