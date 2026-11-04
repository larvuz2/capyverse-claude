"""Composition check: project every actor's mesh into the camera, measure coverage and gaps, and pull actors
toward a cluster centre until the enemy mass is tight (no empty holes between them)."""
import bpy, numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view


def silhouettes(roots, W=616, H=353):
    """Rasterise each actor's projected vertices (convex-ish via splatting) into a low-res mask."""
    sc = bpy.context.scene; cam = sc.camera; dg = bpy.context.evaluated_depsgraph_get()
    masks = {}
    for r in roots:
        m = np.zeros((H, W), bool)
        for o in r.children_recursive:
            if o.type != "MESH": continue
            e = o.evaluated_get(dg); mw = e.matrix_world
            for v in e.data.vertices:
                p = world_to_camera_view(sc, cam, mw @ v.co)
                x, y = int(p.x * W), int((1 - p.y) * H)
                if 0 <= x < W and 0 <= y < H and p.z > 0: m[max(0, y - 2):y + 3, max(0, x - 2):x + 3] = True
        masks[r.name] = m
    return masks


def gap_report(roots):
    """Fraction of the enemy cluster's bounding box that is empty, plus each actor's screen bbox."""
    ms = silhouettes(roots); union = np.zeros_like(next(iter(ms.values())))
    for m in ms.values(): union |= m
    ys, xs = np.nonzero(union)
    if not len(xs): return 1.0, {}
    box = union[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    from scipy import ndimage
    filled = ndimage.binary_closing(box, iterations=6)
    empty = 1 - box.sum() / max(filled.sum(), 1)
    return empty, {k: (np.nonzero(m)[1].min(), np.nonzero(m)[0].min(), np.nonzero(m)[1].max(), np.nonzero(m)[0].max()) for k, m in ms.items() if m.any()}


def tighten(roots, centre, target=0.35, step=0.08, iters=12, keep=()):
    """Move actors toward `centre` (world XY) until the empty share of the cluster drops below target."""
    c = Vector((centre[0], centre[1], 0))
    for i in range(iters):
        bpy.context.view_layer.update()
        empty, _ = gap_report(roots)
        print(f"  pack iter {i}: empty={empty:.2f}")
        if empty <= target: break
        for r in roots:
            if r.name in keep: continue
            d = c - Vector((r.location.x, r.location.y, 0))
            if d.length > 0.6: r.location += d * step
    return empty


def frame_to(roots, region, iters=6):
    """Zoom (lens) + sensor shift so the roots' screen bbox fills `region` = (x0, y0, x1, y1) in 0..1 (y down)."""
    cam = bpy.context.scene.camera; cd = cam.data
    sc = bpy.context.scene; aspect = sc.render.resolution_x / sc.render.resolution_y
    for _ in range(iters):
        bpy.context.view_layer.update()
        _, boxes = gap_report(roots)
        if not boxes: return
        W, H = 616, 353
        x0 = min(b[0] for b in boxes.values()) / W; y0 = min(b[1] for b in boxes.values()) / H
        x1 = max(b[2] for b in boxes.values()) / W; y1 = max(b[3] for b in boxes.values()) / H
        k = min((region[2] - region[0]) / max(x1 - x0, 1e-3), (region[3] - region[1]) / max(y1 - y0, 1e-3))
        cd.lens *= max(0.5, min(2.5, k))
        bpy.context.view_layer.update(); _, boxes = gap_report(roots)
        x0 = min(b[0] for b in boxes.values()) / W; y0 = min(b[1] for b in boxes.values()) / H
        x1 = max(b[2] for b in boxes.values()) / W; y1 = max(b[3] for b in boxes.values()) / H
        # anchor right edge and bottom edge of the region
        cd.shift_x += (x1 - region[2])
        cd.shift_y -= (y1 - region[3]) / aspect
