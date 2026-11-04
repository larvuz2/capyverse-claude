import sys, math; sys.path.insert(0, ".")
from scene import *
reset(); g, a = add_golfer((0, 0, 0), frame=70); c = add_golf_club(a)
w, wa = add_warboy((1.4, 0, 0), pose=WARBOY_POSES["taunt"]); w2, _ = add_warboy((2.8, 0, 0), pose=WARBOY_POSES["fists"])
ax = add_axie((-1.5, 0, 1.2), rot_z=90, scale=1.2); shadow_catcher()
camera((0.8, -8, 1.3), (0.8, 0, 1.0), lens=40); sun(); area((-2, -5, 4), (0, 0, 1), energy=600, size=6)
render("tests/club.png", 1400, 600, samples=12)
