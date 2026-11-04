import bpy, sys, glob, os
from mathutils import Vector
root = "/home/user/capyverse-claude/assets_src/Models&Animations/November2026"
for f in sorted(glob.glob(root + "/**/*.[fF][bB][xX]", recursive=True)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.fbx(filepath=f, automatic_bone_orientation=True)
    except Exception as e:
        print("FAIL", f, e); continue
    objs = bpy.context.scene.objects
    meshes = [o for o in objs if o.type == "MESH"]; arms = [o for o in objs if o.type == "ARMATURE"]
    pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    size = (max(p[i] for p in pts) - min(p[i] for p in pts) for i in range(3)) if pts else ()
    print(os.path.relpath(f, root), "| meshes", [(m.name, len(m.data.vertices), [s.material.name if s.material else None for s in m.material_slots]) for m in meshes],
          "| arms", [(a.name, len(a.data.bones)) for a in arms], "| actions", [(a.name, tuple(round(x) for x in a.frame_range)) for a in bpy.data.actions],
          "| size", tuple(round(s, 2) for s in size), "| imgs", [i.name for i in bpy.data.images])
