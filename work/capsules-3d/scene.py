"""Blender scene builder for Capyverse capsules: real enemy meshes, rigs, animations and textures.

Usage inside another script:  from scene import *;  reset(); pin = add_pin(...); render(...)
Units: metres, Z up, camera looks along +Y by default helpers.
"""
import bpy, math, os
from mathutils import Vector, Euler, Matrix

R = "/home/user/capyverse-claude/assets_src/Models&Animations/November2026/"
TEX = {
    "atlas": R + "BowlingPins/T_PolygonHorrorCarnival_Texture_01_A.PNG",
    "golfer_body": R + "Golfer/T_GolferCatBody_BaseColor.PNG",
    "golfer_head": R + "Golfer/T_CatGolferHead_BaseColor.PNG",
    "warboy_body": R + "WastelandWarboy/T_CatWarBoyBody_BaseColor.PNG",
    "warboy_head": R + "WastelandWarboy/T_CatWarBoyHead_BaseColor.PNG",
}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48
    sc.cycles.use_denoising = True; sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.6


def _import(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False, use_anim=True)
    return [o for o in bpy.data.objects if o not in before]


def tex_mat(name, img_path, emissive=0.0, rough=0.75):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(img_path, check_existing=True)
    t.interpolation = "Closest"  # low-poly atlas: keep the flat colour patches crisp
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    if emissive:
        nt.links.new(t.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = emissive
    return m


def _group(objs, name, loc, rot_z, scale):
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    for o in objs:
        if o.parent is None: o.parent = root
    root.location = loc; root.rotation_euler = (0, 0, math.radians(rot_z)); root.scale = (scale,) * 3
    return root


def _set_action_frame(objs, frame):
    for o in objs:
        if o.type == "ARMATURE" and o.animation_data and o.animation_data.action:
            bpy.context.scene.frame_set(int(frame))


def _attach_head(arm, head_path, tex, bone="head", offset=(0, 0, 0), rot=(-90, 0, 0), scale=1.0):
    new = _import(head_path)
    head = [o for o in new if o.type == "MESH"][0]
    for o in new:
        if o is not head: bpy.data.objects.remove(o)
    head.data.materials.clear(); head.data.materials.append(tex_mat("cathead", tex))
    head.parent = arm; head.parent_type = "BONE"; head.parent_bone = bone
    head.matrix_parent_inverse = Matrix.Identity(4)
    head.location = offset; head.rotation_euler = Euler([math.radians(a) for a in rot]); head.scale = (scale,) * 3
    return head


def add_pin(loc, rot_z=0, scale=1.0, frame=1, name="pin"):
    objs = _import(R + "BowlingPins/Animation/Bowling_Pin_Walking_Anim.FBX")
    atlas = tex_mat("pin", TEX["atlas"]); glow = tex_mat("pin_glow", TEX["atlas"], emissive=1.5)
    for o in objs:
        if o.type == "MESH":
            for i, s in enumerate(o.material_slots): s.material = glow if "Emmisive" in (s.material.name if s.material else "") else atlas
    bpy.context.scene.frame_set(frame)
    return _group(objs, name, loc, rot_z, scale)


def add_worm(loc, rot_z=0, scale=1.0, frame=60, anim="idle", name="worm"):
    f = {"idle": "Worm/Animation/A_WormMiniBoss_Idle_V3.fbx", "hit": "Worm/Animation/A_WormMiniBoss_HitGround.fbx"}[anim]
    objs = _import(R + f)
    m = bpy.data.materials.new("worm"); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.36, 0.26, 0.16, 1); b.inputs["Roughness"].default_value = 0.85
    for o in objs:
        if o.type == "MESH":
            o.data.materials.clear(); o.data.materials.append(m)
            for p in o.data.polygons: p.use_smooth = False
    bpy.context.scene.frame_set(frame)
    return _group(objs, name, loc, rot_z, scale)


def add_golfer(loc, rot_z=0, scale=1.0, frame=70, head=dict(), name="golfer", club=True):
    objs = _import(R + "Golfer/Animation/SK_Gold_Anim02_Anim1.FBX")
    arm = [o for o in objs if o.type == "ARMATURE"][0]
    for o in objs:
        if o.type == "MESH": o.data.materials.clear(); o.data.materials.append(tex_mat("golfer", TEX["golfer_body"]))
    _attach_head(arm, R + "Golfer/ST_CatHead.FBX", TEX["golfer_head"], **head)
    if club: add_golf_club(arm)
    bpy.context.scene.frame_set(frame)
    return _group(objs + [], name, loc, rot_z, scale), arm


def add_warboy(loc, rot_z=0, scale=1.0, pose=None, head=dict(), name="warboy"):
    objs = _import(R + "WastelandWarboy/SM_CatWarboy.FBX")
    arm = [o for o in objs if o.type == "ARMATURE"][0]
    for o in objs:
        if o.type == "MESH": o.data.materials.clear(); o.data.materials.append(tex_mat("warboy", TEX["warboy_body"]))
    _attach_head(arm, R + "WastelandWarboy/ST_CatHead.FBX", TEX["warboy_head"], **head)
    for bone, (rx, ry, rz) in (pose or {}).items():
        pb = arm.pose.bones.get(bone)
        if pb: pb.rotation_mode = "XYZ"; pb.rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    return _group(objs, name, loc, rot_z, scale), arm


def bounds(root):
    pts = []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in root.children_recursive:
        if o.type == "MESH":
            e = o.evaluated_get(dg)
            pts += [e.matrix_world @ v.co for v in e.data.vertices]
    mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
    return mn, mx


def camera(loc, look_at, lens=50, name="cam"):
    c = bpy.data.cameras.new(name); c.lens = lens
    o = bpy.data.objects.new(name, c); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    d = Vector(look_at) - Vector(loc); o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = o
    return o


def sun(rot=(50, 0, 30), energy=3.0, color=(1, 0.95, 0.85), angle=8):
    l = bpy.data.lights.new("sun", "SUN"); l.energy = energy; l.color = color; l.angle = math.radians(angle)
    o = bpy.data.objects.new("sun", l); bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = Euler([math.radians(a) for a in rot])
    return o


def area(loc, look_at, energy=300, size=3, color=(1, 1, 1)):
    l = bpy.data.lights.new("area", "AREA"); l.energy = energy; l.size = size; l.color = color
    o = bpy.data.objects.new("area", l); bpy.context.scene.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (Vector(look_at) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


def render(path, w=2464, h=1412, samples=None):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = w, h; sc.render.resolution_percentage = 100
    if samples: sc.cycles.samples = samples
    sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
    sc.render.filepath = path; bpy.ops.render.render(write_still=True)


def add_axie(loc, rot_z=90, scale=1.0, tilt=0, name="axie"):
    """Axie: image-to-3D (fal Trellis) from the matched render; the game has no Axie model yet."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.dirname(os.path.abspath(__file__)) + "/axie3d/axie_trellis.glb")
    objs = [o for o in bpy.data.objects if o not in before]
    root = _group(objs, name, loc, rot_z, scale)
    root.rotation_euler = (math.radians(tilt), 0, math.radians(rot_z))
    return root


def add_golf_club(arm, bone="Hand_R", length=1.0):
    """A simple low-poly golf club (shaft + grip + iron head) parented to the golfer's hand."""
    def mat(name, col, metal=0.0, rough=0.5):
        m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = col; b.inputs["Metallic"].default_value = metal; b.inputs["Roughness"].default_value = rough
        return m
    steel = mat("shaft", (0.75, 0.76, 0.78, 1), 0.9, 0.35); black = mat("grip", (0.02, 0.02, 0.02, 1))
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.012, depth=length, location=(0, 0, -length / 2))
    shaft = bpy.context.object; shaft.data.materials.append(steel)
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.018, depth=0.22, location=(0, 0, -0.08))
    grip = bpy.context.object; grip.data.materials.append(black)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.04, 0, -length))
    head = bpy.context.object; head.scale = (0.11, 0.03, 0.05); head.data.materials.append(steel)
    club = bpy.data.objects.new("club", None); bpy.context.scene.collection.objects.link(club)
    for o in (shaft, grip, head): o.parent = club
    club.parent = arm; club.parent_type = "BONE"; club.parent_bone = bone
    club.matrix_parent_inverse = Matrix.Identity(4)
    club.rotation_euler = (0, math.radians(90), 0); club.scale = (100, 100, 100)  # hand bone is in cm space
    return club


def shadow_catcher(size=60, z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z))
    p = bpy.context.object; p.is_shadow_catcher = True
    return p


WARBOY_POSES = {
    "arms_down": {"UpperArm_L": (0, 0, -70), "UpperArm_R": (0, 0, -70)},
    "taunt": {"UpperArm_L": (0, 0, -70), "UpperArm_R": (0, 0, 75), "lowerarm_r": (0, 0, 40)},
    "cheer": {"UpperArm_L": (0, 0, 70), "UpperArm_R": (0, 0, 70)},
    "fists": {"UpperArm_L": (0, 0, -55), "UpperArm_R": (0, 0, -55), "lowerarm_l": (0, 0, -60), "lowerarm_r": (0, 0, -60)},
}
