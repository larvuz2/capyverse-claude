import bpy
H="/home/user/capyverse-claude/assets_src/heroes3d/Heroes/"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=H+"Animations/Anim_CapyWalk.fbx", automatic_bone_orientation=False, use_anim=True)
o=[o for o in bpy.data.objects if o.type=="MESH"][0]
me=o.data; uv=me.uv_layers[0].data
for mi,m in enumerate(me.materials):
    us=[];vs=[];n=0
    for p in me.polygons:
        if p.material_index==mi:
            n+=1
            for li in p.loop_indices: us.append(uv[li].uv[0]); vs.append(uv[li].uv[1])
    print(mi,m.name,n,"u",round(min(us),3),round(max(us),3),"v",round(min(vs),3),round(max(vs),3))
# dump eye uv points for plotting
import json
pts=[[uv[li].uv[0],uv[li].uv[1]] for p in me.polygons if me.materials[p.material_index].name.startswith("M_Capybara_Eyes") for li in p.loop_indices]
json.dump(pts,open("eye_uv.json","w"))
