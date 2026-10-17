"""Faces: eyes that look and blink, brows that bend, and a mouth with a shape key per expression.

  * `eye()`    an eyeball on its own bone (it turns to look), textured by `mat.iris` through a front
               projection; an upper and a lower lid, hemispherical shells just outside it on bones of their
               own that rotate shut; a lash line on the upper lid; and two catchlights fixed to the head,
               which therefore stay put as the eye turns (as a real highlight does) and vanish under the lid.
  * `brow()`   a tapered bar laid on the face along a curve, skinned smoothly across three bones (inner,
               middle, outer), so the page can raise it, knit it or arch it.
  * `mouth()`  a decal laid onto the face: a dark opening between two lip curves and a band of teeth under
               the top one. Every expression is the same grid of vertices placed differently, so each is a
               shape key on one small mesh: `rest` is the basis, the rest are keys the page blends.

Shapes are expressed in the face's own 2D frame, metres across (+X, the character's left) and up (+Z) from
the mouth's centre, and projected onto the head shell through `geo.Surface`.
"""
from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

from . import geo
from .geo import TAU, basis, lerp, mesh_object, part


# ------------------------------------------------------------------------------------------------ eyes
def _sphere_cap(name, r, mat, phi0, phi1, segs=40, rings=12):
    """A piece of sphere about local +Y (up): polar angle phi0..phi1 from the +Y pole, as a lathe."""
    prof = []
    for i in range(rings + 1):
        p = lerp(phi0, phi1, i / rings)
        prof.append((r * math.sin(p), r * math.cos(p)))
    return geo.lathe(name, prof, mat, (0, 0, 0), axis=(0, 1, 0), segs=segs, y_hint=(0, 0, 1), caps=False)


def eye(prefix, side, centre, r, look, rig_bones, iris_mat, lid_mat, lash_mat, glint_mat, lid_r=1.07,
        lash=0.12, lash_flick=0.0, lower=True, glint=(0.42, 0.42), glint_size=0.17, res=10, lid_roll=0.0,
        up_open=40.0, lo_open=45.0):
    """Build one eye at `centre`, gazing along `look`. `rig_bones` names the bones:
    dict(eye=, lid_up=, lid_lo=, head=). The lids are hemispheres, built rolled `up_open` degrees up and
    `lo_open` down from meeting at the eye's equator, so the rest pose is the open eye and a blink is the
    lid bones turning back by those angles. `lid_roll` tilts both lid lines (degrees, outer corner down for
    positive). Returns the parts and the eye's frame."""
    c = Vector(centre)
    R = basis(look, (0, 0, 1))            # local: z = gaze, y = up, x = across (character's left)
    R4 = R.to_4x4()
    parts = []

    ball = geo.superquad(f"{prefix}-ball", (r, r, r), iris_mat, (0, 0, 0), n=2.0, res=res)
    me = ball.data
    me.uv_layers.new(name="UVMap")
    uv = me.uv_layers.active.data
    for li, loop in enumerate(me.loops):
        p = me.vertices[loop.vertex_index].co
        # geo.superquad builds about the origin with z as its own axis: the gaze is +z here.
        uv[li].uv = (0.5 + p.x / (2 * r), 0.5 + p.y / (2 * r))
    geo.transform(ball, Matrix.Translation(c) @ R4)
    parts.append(part(ball, rig_bones["eye"]))

    # Lids: shells about the eye's centre. In the lid's own frame +Y is up and +Z the gaze; the upper lid is
    # the upper hemisphere and the lower the lower one, and their bones rotate them about local X.
    rl = r * lid_r
    roll = Matrix.Rotation(math.radians(lid_roll * side), 4, "Z")

    up_rot = Matrix.Rotation(-math.radians(up_open), 4, "X")
    lo_rot = Matrix.Rotation(math.radians(lo_open), 4, "X")

    def lid(tag, upper, bone):
        phi0, phi1 = (0.0, math.pi / 2 + 0.02) if upper else (math.pi / 2 - 0.02, math.pi)
        cap = _sphere_cap(f"{prefix}-{tag}", rl, lid_mat, phi0, phi1)
        # _sphere_cap is built about +Y = up; the eye's frame has y = up and z = gaze as well, so only the
        # eye's own orientation, the roll and the opening remain.
        geo.transform(cap, Matrix.Translation(c) @ R4 @ roll @ (up_rot if upper else lo_rot))
        parts.append(part(cap, bone))
        return cap

    lid("lid-up", True, rig_bones["lid_up"])
    if lower:
        lid("lid-lo", False, rig_bones["lid_lo"])

    # The lash line: along the upper lid's rim across the front, thickest at the outer corner.
    pts, rad = [], []
    n = 28
    for i in range(n + 1):
        a = lerp(-1.75, 1.75, i / n)              # radians either side of straight ahead
        # rim of the upper hemisphere (y=0 in lid frame): (sin a, 0, cos a) * rl
        p = Vector((math.sin(a) * rl * 1.01, 0.0, math.cos(a) * rl * 1.01))
        outer = (a * side) > 0                    # towards the character's own outside
        t = abs(a) / 1.75
        w = lash * r * (0.35 + 0.65 * math.sin(math.pi * min(1.0, (i / n)))) * (1.0 + (0.5 * t if outer else 0))
        pts.append(p)
        rad.append(max(w, lash * r * 0.15))
    if lash_flick:
        # a short flick past the outer corner, up and out
        last = pts[-1] if side > 0 else pts[0]
        flick = last + Vector((side * lash_flick * r, lash_flick * r * 0.55, -lash_flick * r * 0.3))
        if side > 0:
            pts.append(flick)
            rad.append(rad[-1] * 0.3)
        else:
            pts.insert(0, flick)
            rad.insert(0, rad[0] * 0.3)
    # thin radially (half_w lies along the eye's radius here), tall vertically (half_h along "up")
    lashes = geo.sweep(f"{prefix}-lash", pts, [x * 0.55 for x in rad], rad, lash_mat, segs=8, up=(0, 1, 0))
    geo.transform(lashes, Matrix.Translation(c) @ R4 @ roll @ up_rot)
    parts.append(part(lashes, rig_bones["lid_up"]))

    # Catchlights: on the eyeball's surface, up and to the light (character's left, viewer's right).
    for k, (gx, gy, s) in enumerate(((glint[0], glint[1], glint_size), (glint[0] * 0.25 - 0.1, glint[1] * 0.35 - 0.33, glint_size * 0.45))):
        d = Vector((gx, gy, 1.0)).normalized()
        g = geo.disc(f"{prefix}-glint{k}", r * s, r * 0.02, glint_mat, (0, 0, 0), (0, 0, 1), bevel_r=r * 0.008,
                     segs=16)
        M = Matrix.Translation(c) @ R4 @ basis(d, (0, 1, 0)).to_4x4() @ Matrix.Translation((0, 0, r * 1.012))
        geo.transform(g, M)
        parts.append(part(g, rig_bones["head"]))
    return parts, R



# ----------------------------------------------------------------------------------------------- brows
def brow(prefix, side, surf: geo.Surface, pts2d, half_h, half_d, mat, bones, offset=0.004, taper=(0.55, 1.0, 0.35),
         segs=10):
    """A brow along `pts2d` [(x, z), ...] (front-projected onto `surf`), running from the inner end to the
    outer. Its height on the face is `half_h` (scaled along it by a smooth curve through `taper` =
    (inner, middle, outer)), its thickness off the face `half_d`. Skinned across `bones` = (inner, mid,
    outer)."""
    pts = []
    for x, z in pts2d:
        p = surf.front(x, z, offset=offset + half_d * 0.6)
        if p is None:
            raise ValueError(f"brow point ({x:.3f}, {z:.3f}) misses the face")
        pts.append(p)
    m = len(pts)
    hw = []
    for i in range(m):
        t = i / (m - 1)
        a, b, c = taper
        v = (a * (1 - t) * (1 - t) + 2 * b * t * (1 - t) * 1.15 + c * t * t)
        hw.append(half_h * v)
    hd = [half_d * (0.6 + 0.4 * (w / half_h)) for w in hw]
    ob = geo.sweep(f"{prefix}", pts, hw, hd, mat, segs=segs, up=(0, -1, 0))
    # weights by where along the brow each vertex is
    seglen = [0.0]
    for a, b in zip(pts, pts[1:]):
        seglen.append(seglen[-1] + (b - a).length)
    L = seglen[-1]
    vgs = [ob.vertex_groups.new(name=b) for b in bones]
    for v in ob.data.vertices:
        best, bi = 1e9, 0
        for i in range(m - 1):
            a, b = pts[i], pts[i + 1]
            ab = b - a
            t = max(0.0, min(1.0, (v.co - a).dot(ab) / max(ab.length_squared, 1e-12)))
            d = (a + ab * t - v.co).length
            if d < best:
                best, bi, bt = d, i, t
        s = (seglen[bi] + (seglen[bi + 1] - seglen[bi]) * bt) / L
        w_in = max(0.0, 1 - 2 * s) ** 1.0
        w_out = max(0.0, 2 * s - 1) ** 1.0
        w_mid = 1 - w_in - w_out
        for vg, w in zip(vgs, (w_in, w_mid, w_out)):
            if w > 1e-4:
                vg.add([v.index], w, "REPLACE")
    ob["mesh"] = "body"                 # bent by its bones, so it needs no shape keys: the body mesh
    return ob


# ---------------------------------------------------------------------------------------------- mouth
DEFAULT = dict(w=0.1, smile=0.02, lift_L=0.0, lift_R=0.0, top=0.0, bot=0.0, round=0.0, teeth=0.0,
               low_teeth=0.0, thick=0.008, dx=0.0, dz=0.0, pinch=0.0)


def _outline(P, u):
    P = {**DEFAULT, **P}
    w = P["w"] * (1 - P["pinch"] * (1 - u * u) * 0.0)
    x = u * w + P["dx"]
    zc = P["smile"] * u * u + (P["lift_L"] if u > 0 else P["lift_R"]) * abs(u) ** 2.5 + P["dz"]
    p = lerp(1.0, 0.5, P["round"])
    prof = max(0.0, 1 - u * u) ** p
    th = P["thick"] * max(0.0, 1 - u * u) ** 0.5 * 0.5 + P["thick"] * 0.12
    up = zc + P["top"] * prof + th
    lo = zc - P["bot"] * prof - th
    open_ = (P["top"] + P["bot"]) * prof
    t_bot = max(lo + th * 0.5, up - P["teeth"] * open_ - th * 0.3) if P["teeth"] > 0 else up - th * 0.4
    lt_top = min(up - th * 0.5, lo + P["low_teeth"] * open_ + th * 0.3) if P["low_teeth"] > 0 else lo + th * 0.4
    return x, up, lo, t_bot, lt_top


def _vertex_coloured(name, like):
    """A material whose base colour is the mesh's vertex colour "Col", otherwise like `like`."""
    import bpy
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    src = like.node_tree.nodes["Principled BSDF"]
    for k in ("Roughness", "Metallic", "Specular IOR Level", "Coat Weight", "Coat Roughness"):
        b.inputs[k].default_value = src.inputs[k].default_value
    vc = nt.nodes.new("ShaderNodeVertexColor")
    vc.layer_name = "Col"
    nt.links.new(vc.outputs["Color"], b.inputs["Base Color"])
    m.use_backface_culling = True
    return m


def mouth(name, surf: geo.Surface, centre2d, shapes: dict, mats, cols=28, rows=5, trows=2, offset=0.0025,
          bone="head"):
    """A mouth decal with one shape key per entry of `shapes` (entry "rest" is the basis). `mats` =
    (inside, teeth). `centre2d` = (x, z) of the mouth's centre on the face (front projection)."""
    cx, cz = centre2d
    inside, teeth = mats

    def layout(P):
        """Every vertex's 2D position for shape P: interior grid, then the upper teeth, then the lower."""
        pts = []
        us = [-1 + 2 * i / cols for i in range(cols + 1)]
        # cosine spacing towards the corners, where the outline turns fastest
        us = [math.copysign(abs(u) ** 0.85, u) for u in us]
        O = [_outline(P, u) for u in us]
        for j in range(rows + 1):
            for (x, up, lo, tb, lt) in O:
                pts.append((x, lerp(lo, up, j / rows), 0))
        for j in range(trows + 1):
            for (x, up, lo, tb, lt) in O:
                pts.append((x, lerp(tb, up - (up - lo) * 0.04, j / trows), 1))
        for j in range(trows + 1):
            for (x, up, lo, tb, lt) in O:
                pts.append((x, lerp(lo + (up - lo) * 0.04, lt, j / trows), 1))
        return pts

    def project(pts):
        out = []
        for x, z, layer in pts:
            p = surf.front(cx + x, cz + z, offset=offset + layer * offset * 0.8)
            if p is None:
                raise ValueError(f"mouth point ({cx + x:.3f}, {cz + z:.3f}) misses the face")
            out.append(p)
        return out

    rest = project(layout(shapes["rest"]))
    bm = bmesh.new()
    vs = [bm.verts.new(p) for p in rest]
    W = cols + 1

    def grid(start, nrows, mat_index):
        for j in range(nrows):
            for i in range(cols):
                a = start + j * W + i
                f = bm.faces.new((vs[a], vs[a + 1], vs[a + W + 1], vs[a + W]))
                f.material_index = mat_index

    grid(0, rows, 0)
    grid((rows + 1) * W, trows, 1)
    grid((rows + 1) * W + (trows + 1) * W, trows, 1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    # the decal faces out of the face (towards -Y)
    for f in bm.faces:
        if f.normal.y > 0:
            f.normal_flip()
    ob = mesh_object(name, bm, None, smooth_=True)
    # One material, the inside and the teeth told apart by vertex colour: a single primitive, so three.js
    # loads the face as one mesh, named as the node is, and a clip file's `weights` tracks (which name that
    # node) bind to it (see kit/proxy.py). The teeth lose only a little gloss.
    me = ob.data
    col = me.color_attributes.new(name="Col", type="FLOAT_COLOR", domain="CORNER")
    tones = [tuple(m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value) for m in (inside, teeth)]
    for poly in me.polygons:
        for li in poly.loop_indices:
            col.data[li].color = tones[poly.material_index]
        poly.material_index = 0
    me.materials.append(_vertex_coloured(name + "-mat", inside))
    ob.shape_key_add(name="rest", from_mix=False)
    for key, P in shapes.items():
        if key == "rest":
            continue
        kb = ob.shape_key_add(name=key, from_mix=False)
        kb.value = 0.0                    # a new key starts at 1 in Blender 5
        for i, p in enumerate(project(layout(P))):
            kb.data[i].co = p
    ob["mesh"] = "face"
    vg = ob.vertex_groups.new(name=bone)
    vg.add(list(range(len(ob.data.vertices))), 1.0, "REPLACE")
    return ob
