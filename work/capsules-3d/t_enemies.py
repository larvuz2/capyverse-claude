import sys; sys.path.insert(0, ".")
from scene import *
reset()
p = add_pin((0, 0, 0), rot_z=0, scale=1, frame=5)
w = add_worm((2.2, 0, 0), rot_z=0, scale=1, frame=60)
g, ga = add_golfer((-2.0, 0, 0), rot_z=0, scale=1, frame=70)
wb, wa = add_warboy((-4.0, 0, 0), rot_z=0, scale=1)
for r in (p, w, g, wb):
    mn, mx = bounds(r); print(r.name, [round(v, 2) for v in mn], [round(v, 2) for v in mx])
camera((-1, -12, 1.4), (-1, 0, 1.0), lens=35)
sun(); area((-1, -6, 4), (-1, 0, 1), energy=600, size=6)
render("tests/enemies.png", 1600, 800, samples=24)
