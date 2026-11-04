import bpy
R = "/home/user/capyverse-claude/assets_src/Models&Animations/November2026/"
for f in ["WastelandWarboy/SM_CatWarboy.FBX", "WastelandWarboy/Animation/standing_idle.FBX", "Golfer/Animation/SK_Gold_Anim02_Anim1.FBX"]:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.fbx(filepath=R + f, automatic_bone_orientation=True)
    a = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"][0]
    print(f, sorted(b.name for b in a.data.bones)[:60])
