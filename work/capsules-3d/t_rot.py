import sys, math; sys.path.insert(0, ".")
from scene import *
reset(); p = add_pin((0, 0, 0), rot_z=90, scale=2)
for o in p.children_recursive: print(o.name, o.type, o.parent.name if o.parent else None, [round(v,2) for v in o.matrix_world.to_euler()], o.animation_data.action.name if o.animation_data and o.animation_data.action else None)
print("root", [round(v,2) for v in p.rotation_euler])
bpy.context.view_layer.update(); bpy.context.scene.frame_set(5)
for o in p.children_recursive: print("AFTER", o.name, [round(v,2) for v in o.matrix_world.to_euler()], o.parent.name)
a=[o for o in p.children_recursive if o.type=="ARMATURE"][0]
print("fcurves", sorted({fc.data_path for fc in a.animation_data.action.fcurves})[:10] if hasattr(a.animation_data.action,'fcurves') else 'layered')
