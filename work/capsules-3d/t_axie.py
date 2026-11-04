import sys, math; sys.path.insert(0, ".")
from scene import *
reset()
bpy.ops.import_scene.gltf(filepath="axie3d/axie_trellis.glb")
objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
print([(o.name, len(o.data.vertices), tuple(round(d, 2) for d in o.dimensions)) for o in objs])
root = bpy.data.objects.new("axie", None); bpy.context.scene.collection.objects.link(root)
for o in bpy.context.scene.objects:
    if o.parent is None and o is not root: o.parent = root
for i, rz in enumerate([0, 90, 180, 270]):
    pass
camera((0, -4, 0.3), (0, 0, 0), lens=50); sun(); area((-2, -3, 3), (0, 0, 0), energy=400, size=4)
for i, rz in enumerate([0, 90, 180, -90]):
    root.rotation_euler = (0, 0, math.radians(rz)); render(f"tests/axie_{i}.png", 600, 450, samples=12)
