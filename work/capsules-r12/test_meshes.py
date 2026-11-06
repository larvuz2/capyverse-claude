import bpy, math, sys
from mathutils import Vector
H="/home/user/capyverse-claude/assets_src/heroes3d/Heroes/"
T={"capy":H+"Textures/T_Capy_BaseColor.png","moody":H+"Textures/T_Moody_BaseColor.png","jim":H+"Textures/T_Jim_BaseColor.png"}
F={"capy":["SM_Capy.fbx","Animations/Anim_CapyWalk.fbx"],"moody":["SM_Moody.fbx","Animations/Anim_MoodyWalk.fbx"],"jim":["SM_Bulldog_Jim.fbx","Animations/Anim_JimSprint.fbx"]}
def mat(path):
    m=bpy.data.materials.new("M"); m.use_nodes=True; nt=m.node_tree; b=nt.nodes["Principled BSDF"]
    t=nt.nodes.new("ShaderNodeTexImage"); t.image=bpy.data.images.load(path,check_existing=True)
    nt.links.new(t.outputs["Color"],b.inputs["Base Color"]); b.inputs["Roughness"].default_value=0.6
    return m
for k,fs in F.items():
  for i,f in enumerate(fs):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc=bpy.context.scene; sc.render.engine="CYCLES"; sc.cycles.samples=16; sc.cycles.device="CPU"; sc.render.resolution_x=600; sc.render.resolution_y=450
    w=bpy.data.worlds.new("W"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.6,0.6,0.65,1)
    bpy.ops.import_scene.fbx(filepath=H+f, automatic_bone_orientation=False, use_anim=True)
    m=mat(T[k])
    meshes=[o for o in bpy.data.objects if o.type=="MESH"]
    for o in meshes:
        print(k,f,o.name,"uvs",[u.name for u in o.data.uv_layers])
        o.data.materials.clear(); o.data.materials.append(m)
    sc.frame_set(5)
    pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    mn=Vector([min(p[j] for p in pts) for j in range(3)]); mx=Vector([max(p[j] for p in pts) for j in range(3)]); ctr=(mn+mx)/2; sz=(mx-mn).length
    cam=bpy.data.objects.new("C",bpy.data.cameras.new("C")); sc.collection.objects.link(cam); sc.camera=cam
    d=Vector((1.0,-0.4,0.35)).normalized()*sz*1.6
    cam.location=ctr+d; cam.rotation_euler=(ctr-cam.location).to_track_quat('-Z','Y').to_euler()
    L=bpy.data.objects.new("L",bpy.data.lights.new("L","SUN")); L.data.energy=3; L.rotation_euler=(0.8,0.2,0.6); sc.collection.objects.link(L)
    sc.render.filepath=f"/tmp/claude-0/-home-user/5210da15-ba2c-5900-b8c2-dc38bd1a885e/scratchpad/t_{k}_{i}.png"
    bpy.ops.render.render(write_still=True)
