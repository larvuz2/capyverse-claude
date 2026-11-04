import sys, math; sys.path.insert(0, ".")
from scene import *
reset()
for i,(tx,rz) in enumerate([(0,0),(-90,0),(90,0),(0,180),(-90,180),(180,0)]):
    r = add_glb("oph3d/ophelia_trellis.glb", (i*3,0,1.5), 0, 1.8, tilt=0, name=f"o{i}")
    r.rotation_euler=(math.radians(tx),0,math.radians(rz))
camera((7.5,-16,1.5),(7.5,0,1.5),lens=40); sun(); area((7,-6,5),(7,0,1),energy=1200,size=10)
render("tests/oph.png",2000,500,samples=8)
