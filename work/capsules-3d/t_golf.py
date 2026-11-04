import sys; sys.path.insert(0, ".")
from scene import *
for f in [1, 30, 55, 70, 85, 100, 120, 140]:
    reset(); g, a = add_golfer((0, 0, 0), frame=f)
    camera((0, -6, 1.1), (0, 0, 1.0), lens=35); sun(); area((-2, -5, 4), (0, 0, 1), energy=600, size=6)
    render(f"tests/golf_{f:03d}.png", 400, 500, samples=8)
