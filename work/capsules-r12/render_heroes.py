"""Render the real in-game hero meshes (Capy, Moody, Jim) posed from their own animations, lit to match the
round-11 meadow plate: warm orange key from the fire (upper right), cool purple sky fill (upper left), soft front
fill so faces read at thumbnail size, and a shadow catcher under the ground characters.

python3 render_heroes.py [capy moody jim]   ->  renders/<name>.png  (RGBA, shadow in alpha)
"""
import bpy, math, sys, os
from mathutils import Vector, Euler

H = "/home/user/capyverse-claude/assets_src/heroes3d/Heroes/"
OUT = "/home/user/capyverse-claude/work/capsules-r12/renders"

CFG = {
    # anim fbx, texture, frame, pitch (deg, + = nose up), camera dir from subject, ground shadow, roughness
    "capy":  dict(fbx="Animations/Anim_CapyWalk.fbx", tex="T_Capy", frame=9, pitch=9, roll=-4, cam=(2.3, -1.15, 0.15), ground=False, rough=0.82),
    "moody": dict(fbx="Animations/Anim_MoodyWalk.fbx", tex="T_Moody", frame=9, pitch=0, roll=0, cam=(2.3, -1.35, 0.75), ground=True, rough=0.62),
    "jim":   dict(fbx="Animations/Anim_JimSprint.fbx", tex="T_Jim", frame=24, pitch=0, roll=0, cam=(2.3, -1.35, 0.65), ground=True, rough=0.7),
}


def material(tex, rough):
    m = bpy.data.materials.new(tex); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(H + f"Textures/{tex}_BaseColor.png", check_existing=True)
    nt.links.new(t.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = 0.3        # no wet/plastic sheen (the director's 'AI look' note)
    return m


def eye_material(mesh):
    """Capy's eye texture is not in the folder: paint the eyeballs procedurally via vertex colours
    (white sclera, brown iris, black pupil) aimed outward-forward like the in-game screenshots."""
    me = mesh.data
    eye_idx = [i for i, m in enumerate(me.materials) if "Eye" in m.name]
    if not eye_idx: return
    ei = eye_idx[0]
    verts = {v for p in me.polygons if p.material_index == ei for v in p.vertices}
    sides = {}
    for v in verts:
        co = me.vertices[v].co; sides.setdefault(co.x > 0, []).append(v)
    attr = me.color_attributes.new("eye", "FLOAT_COLOR", "POINT")
    for v in range(len(me.vertices)): attr.data[v].color = (1, 1, 1, 1)
    for side, vs in sides.items():
        c = sum((me.vertices[v].co for v in vs), Vector()) / len(vs)
        look = Vector(((1 if side else -1) * 0.75, -1.0, 0.35)).normalized()
        for v in vs:
            d = (me.vertices[v].co - c).normalized().dot(look)
            col = (0.02, 0.015, 0.01) if d > 0.9 else (0.42, 0.22, 0.08) if d > 0.72 else (0.95, 0.94, 0.9)
            if 0.94 < d: col = (0.02, 0.015, 0.01)
            attr.data[v].color = (*col, 1)
    m = bpy.data.materials.new("Eye"); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    a = nt.nodes.new("ShaderNodeVertexColor"); a.layer_name = "eye"
    nt.links.new(a.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.15
    b.inputs["Coat Weight"].default_value = 0.6                # wet eye highlight
    me.materials[ei] = m


def sun(name, rot, energy, color, angle=0.1):
    L = bpy.data.objects.new(name, bpy.data.lights.new(name, "SUN")); L.data.energy = energy; L.data.color = color
    L.data.angle = angle; L.rotation_euler = Euler(rot); bpy.context.scene.collection.objects.link(L); return L


def look_at(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def render(name, res=1800, samples=96):
    c = CFG[name]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.render.film_transparent = True; sc.view_settings.view_transform = "Standard"
    sc.render.resolution_x = sc.render.resolution_y = res
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.36, 0.30, 0.55, 1)   # purple night ambient
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    bpy.ops.import_scene.fbx(filepath=H + c["fbx"], automatic_bone_orientation=False, use_anim=True)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    arm = [o for o in bpy.data.objects if o.type == "ARMATURE"][0]
    mat = material(c["tex"], c["rough"])
    for o in meshes:
        if not o.data.materials: o.data.materials.append(mat)
        for i, m in enumerate(o.data.materials):
            if not (m and "Eye" in m.name): o.data.materials[i] = mat
        eye_material(o)
    sc.frame_set(c["frame"])
    # tilt the whole body (characters face -Y): negative X rotation lifts the nose
    arm.rotation_euler.x += math.radians(-c["pitch"]); arm.rotation_euler.y += math.radians(c["roll"])
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in meshes:
        e = o.evaluated_get(dg); me = e.to_mesh()
        pts += [e.matrix_world @ v.co for v in me.vertices]; e.to_mesh_clear()
    mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
    ctr = (mn + mx) / 2; size = (mx - mn).length
    if c["ground"]:
        bpy.ops.mesh.primitive_plane_add(size=size * 6, location=(ctr.x, ctr.y, mn.z))
        bpy.context.object.is_shadow_catcher = True
    cam = bpy.data.objects.new("C", bpy.data.cameras.new("C")); sc.collection.objects.link(cam); sc.camera = cam
    cam.data.lens = 70
    cam.location = ctr + Vector(c["cam"]).normalized() * size * 2.6; look_at(cam, ctr)
    # lights: fire key (behind-right, warm), sky fill (upper-left, cool), soft front fill, rim from the fire side
    sun("fire", (math.radians(42), 0, math.radians(-125)), 3.6, (1.0, 0.55, 0.25), 0.2)
    sun("sky", (math.radians(45), 0, math.radians(120)), 1.1, (0.55, 0.55, 1.0), 0.4)
    sun("front", (math.radians(55), 0, math.radians(30)), 1.6, (1.0, 0.92, 0.85), 0.6)
    os.makedirs(OUT, exist_ok=True)
    sc.render.filepath = f"{OUT}/{name}.png"; bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a in CFG] or list(CFG)
    for n in args: render(n)
