import sys; sys.path.insert(0, ".")
from scene import *
reset()
rots = [(0,0,0),(90,0,0),(-90,0,0),(0,0,90),(0,0,-90),(0,90,0),(0,-90,0),(90,0,90),(90,0,-90),(-90,0,90),(-90,0,-90),(180,0,0)]
for i, r in enumerate(rots):
    add_warboy((i * 1.2, 0, 0), head=dict(rot=r), name=f"w{i}")
camera((6.6, -16, 1.75), (6.6, 0, 1.75), lens=50)
sun(); area((6, -6, 4), (6, 0, 1), energy=800, size=8)
render("tests/heads.png", 2400, 500, samples=12)
