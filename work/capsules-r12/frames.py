import bpy, sys
from mathutils import Vector
H="/home/user/capyverse-claude/assets_src/heroes3d/Heroes/"
k,f,frames=sys.argv[-3],sys.argv[-2],[int(x) for x in sys.argv[-1].split(",")]
T={"capy":"T_Capy","moody":"T_Moody","jim":"T_Jim"}[k]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene; sc.render.engine="CYCLES"; sc.cycles.samples=8; sc.render.resolution_x=360; sc.render.resolution_y=300
w=bpy.data.worlds.new("W"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.6,0.6,0.65,1)
bpy.ops.import_scene.fbx(filepath=H+f, automatic_bone_orientation=False, use_anim=True)
m=bpy.data.materials.new("M"); m.use_nodes=True; t=m.node_tree.nodes.new("ShaderNodeTexImage"); t.image=bpy.data.images.load(H+f"Textures/{T}_BaseColor.png")
m.node_tree.links.new(t.outputs["Color"],m.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
meshes=[o for o in bpy.data.objects if o.type=="MESH"]
for o in meshes: o.data.materials.clear(); o.data.materials.append(m)
cam=bpy.data.objects.new("C",bpy.data.cameras.new("C")); sc.collection.objects.link(cam); sc.camera=cam
ctr=Vector((0,0,0.4)); cam.location=ctr+Vector((2.6,-0.2,0.5)); cam.rotation_euler=(ctr-cam.location).to_track_quat('-Z','Y').to_euler()
L=bpy.data.objects.new("L",bpy.data.lights.new("L","SUN")); L.data.energy=3; L.rotation_euler=(0.8,0.2,0.6); sc.collection.objects.link(L)
for fr in frames:
    sc.frame_set(fr); sc.render.filepath=f"/tmp/claude-0/-home-user/5210da15-ba2c-5900-b8c2-dc38bd1a885e/scratchpad/fr_{k}_{fr:02d}.png"; bpy.ops.render.render(write_still=True)
