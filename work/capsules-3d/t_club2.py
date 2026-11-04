import sys, math; sys.path.insert(0, ".")
from scene import *
reset()
R=[(0,0,0),(90,0,0),(-90,0,0),(0,90,0),(0,-90,0),(180,0,0)]
for i,r in enumerate(R):
    g,a=add_golfer((i*1.3,0,0),frame=70,name=f"g{i}"); c=add_golf_club(a); c.rotation_euler=[math.radians(v) for v in r]; c.scale=(100,100,100)
camera((3.2,-11,1.2),(3.2,0,1.0),lens=40); sun(); area((-2,-5,4),(3,0,1),energy=900,size=8)
render("tests/club2.png",1800,600,samples=8)
