import sys; sys.path.insert(0, ".")
from scene import *
fr=[("idle",20),("idle",60),("idle",100),("idle",140),("hit",15),("hit",35),("hit",55),("hit",80)]
for i,(a,f) in enumerate(fr):
    reset(); w=add_worm((0,0,0),frame=f,anim=a); mn,mx=bounds(w); print(a,f,[round(v,2) for v in mn],[round(v,2) for v in mx])
    camera((-6,-7,1.2),(0,0,0.6),lens=35); sun(); area((-3,-5,4),(0,0,1),energy=600,size=6)
    render(f"tests/worm_{a}{f}.png",500,500,samples=8)
