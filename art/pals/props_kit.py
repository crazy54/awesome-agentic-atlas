"""The props' own kit, on top of `kit`: the shared palette, the `Prop` builder (parts, bones, clips, export,
render), flat text, rounded plates with a texturable face, bendable sheets and bone chains.

A prop is built in world space with its origin where it is held or stands (see props.py for the table),
metres, Z up, its front facing -Y like the cast. A prop that moves is a little armature: a `root` bone at the
origin carries everything that does not move, and each moving part rides its own bone (names with
underscores, so three.js keeps them). A prop that does not move is one mesh, plus a named child node for any
part the page needs to reach (a beam it makes additive, a face it textures).

Clips are functions of time returning, per bone, a turn about world axes (through the bone's head, as the
bone sat at rest), a move along world axes and a scale in the bone's own frame (Y along the bone). `bake`
samples them at 30 fps into one action per clip on an NLA track of the clip's name, which the exporter turns
into one glTF animation each; slim.mjs then drops what never moves and the keys a straight line reproduces.
"""
from __future__ import annotations

import math
import os
import subprocess
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kit import anim, export, geo, mat, rig, studio  # noqa: E402
from kit.geo import V, lerp  # noqa: E402

TAU = math.tau
HOME = Path(os.environ.get("PALS_HOME", "E:/Development Workspaces/Archie and Pals"))
SITE_PROPS = HERE.parent.parent / "docs" / "assets" / "pals" / "props"     # where the stage's s.prop() looks
# Geist (the site's face, docs/assets/fonts/geist.woff2) as a static 800-weight TTF, made outside the repo:
#   python -c "from fontTools.ttLib import TTFont; from fontTools.varLib import instancer;
#              f=TTFont('docs/assets/fonts/geist.woff2'); f.flavor=None;
#              instancer.instantiateVariableFont(f, {'wght': 800}).save('<HOME>/tools/fonts/geist-800.ttf')"
FONTS = [HOME / "tools/fonts/geist-800.ttf", Path("C:/Windows/Fonts/arialbd.ttf")]


# ------------------------------------------------------------------------------------------ palette
# One small palette for every prop: the cast's own colours (Archie's ceramic, graphite and lime, Zip's violet
# and mint, Brick's orange and cream, as archie.py, zip.py and brick.py set them) and a few the gags need. Glossy and toy-like, as the pals are.
SWATCHES = dict(
    ceramic=("#ebe5da", dict(rough=0.24, coat=0.85, coat_rough=0.07)),
    graphite=("#2b2a29", dict(rough=0.42, coat=0.35, coat_rough=0.25, spec=0.45)),
    rubber=("#1c1b1b", dict(rough=0.78, spec=0.3)),
    lime=("#a4c812", dict(rough=0.26, coat=0.85, coat_rough=0.05)),
    violet=("#7440b8", dict(rough=0.2, coat=0.9, coat_rough=0.05)),
    mint=("#72d3a4", dict(rough=0.22, coat=0.85, coat_rough=0.05)),
    orange=("#e5671d", dict(rough=0.24, coat=0.8, coat_rough=0.07)),
    cream=("#e8d0b8", dict(rough=0.3, coat=0.6, coat_rough=0.1)),
    steel=("#a9a6a2", dict(metal=1.0, rough=0.28)),
    brass=("#b8893f", dict(metal=1.0, rough=0.32)),
    chrome=("#e4e4e6", dict(metal=1.0, rough=0.1)),
    gold=("#f2b630", dict(metal=0.35, rough=0.22, coat=1.0, coat_rough=0.04)),
    red=("#e0362c", dict(rough=0.24, coat=0.85, coat_rough=0.05)),
    yellow=("#f8c81c", dict(rough=0.24, coat=0.85, coat_rough=0.05)),
    cone=("#ff5a1c", dict(rough=0.3, coat=0.6, coat_rough=0.1)),
    white=("#f6f4ef", dict(rough=0.22, coat=0.8)),
    paper=("#f8f3e6", dict(rough=0.72, spec=0.35)),
    ink=("#2b2a29", dict(rough=0.6, spec=0.3)),
    redink=("#cf3328", dict(rough=0.55, spec=0.3)),
    wood=("#c98f55", dict(rough=0.42, coat=0.55, coat_rough=0.12)),
    canvas=("#f3ecdc", dict(rough=0.6, spec=0.35)),
    velvet=("#8c1024", dict(rough=0.72, spec=0.35)),
    potato=("#a97a47", dict(rough=0.68, spec=0.35)),
    fluff=("#8f8984", dict(rough=0.95, spec=0.15)),
    fluff_dark=("#6d6863", dict(rough=0.95, spec=0.15)),
    black=("#141414", dict(rough=0.45, spec=0.3)),
    lens=("#121416", dict(rough=0.08, coat=1.0, coat_rough=0.02, spec=0.8)),
    glass=("#d8eef4", dict(rough=0.04, spec=0.6, alpha=0.35)),
    sky=("#4fb6e8", dict(rough=0.24, coat=0.85)),
    pink=("#ff7eb6", dict(rough=0.22, coat=0.9)),
    rope=("#d7b27a", dict(rough=0.7, spec=0.3)),
    cork=("#b98a5a", dict(rough=0.65, spec=0.3)),
    juice=("#ff8a3d", dict(rough=0.15, coat=1.0, coat_rough=0.03)),
    # Glowing and beam-like parts: the page finds them by the `holo` prefix (additive, faded, pulsed).
    holo_beam=("#fff1c4", dict(emit="#fff1c4", strength=1.0, alpha=0.15, rough=1.0, spec=0.0)),
    holo_lamp=("#fff6dc", dict(emit="#fff3cf", strength=8.0, rough=0.3)),
    holo_red=("#ff3b30", dict(emit="#ff3b30", strength=4.0, rough=0.3)),
    holo_lime=("#c8f53a", dict(emit="#b7e82a", strength=1.2, rough=0.3)),
    holo_land=("#6fc23a", dict(emit="#7ee040", strength=0.8, rough=0.5)),
    holo_amber=("#ffb02e", dict(emit="#ff9f1a", strength=3.0, rough=0.3)),
    holo_soft=("#ffffff", dict(emit="#fff6ea", strength=2.5, rough=0.5)),
    holo_door=("#e9fbff", dict(emit="#d9f6ff", strength=0.6, alpha=0.18, rough=0.1)),
    smoke=("#e6e3df", dict(rough=1.0, spec=0.1, alpha=0.85)),
    # a lit screen that reads on either theme (not `holo`: the page would add it as light, and on the light
    # theme added blue is white)
    screen_blue=("#1a43b0", dict(emit="#1f55d6", strength=0.9, rough=0.55, spec=0.3)),
    screen_ink=("#f4f7ff", dict(emit="#f4f7ff", strength=1.2, rough=0.4)),
)


class Palette(dict):
    """Materials made on first use, so a prop's file carries only the ones it uses. Keys use underscores;
    material names use hyphens (`holo_beam` -> `holo-beam`)."""

    ALIAS = {"rubber": "graphite"}               # near enough at a prop's size; one material fewer

    def __missing__(self, key):
        if key in self.ALIAS:
            self[key] = self[self.ALIAS[key]]
            return self[key]
        hex_, kw = SWATCHES[key]
        m = mat.principled(key.replace("_", "-"), hex_, **kw)
        if key.startswith("holo") and kw.get("alpha", 1.0) < 1.0:
            m.use_backface_culling = False          # beams and glass are seen from inside as well
        self[key] = m
        return m


# ------------------------------------------------------------------------------------------- shapes
def rrect(w, h, r, seg=4):
    """A rounded rectangle's outline, counter-clockwise in (u, v), centred on 0."""
    r = max(1e-4, min(r, w / 2 - 1e-5, h / 2 - 1e-5))
    out = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180),
                       (w / 2 - r, -h / 2 + r, 270)):
        for i in range(seg + 1):
            a = math.radians(a0 + 90 * i / seg)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def outline_mesh(name, outlines, depth, m, bevel=None, steps=2, face=None, back=None, M=None, sharp=60):
    """A prism: `outlines(inset)` gives the 2D outline (u -> X, v -> Z) shrunk by `inset`, extruded along Y
    from -depth/2 (the front) to +depth/2, its edges rounded by `bevel`. `face`, a material, goes on the
    front cap with UVs filling it 0..1 (u left to right, v bottom to top as seen from the front); `back` on
    the back cap likewise (mirrored, so it reads from behind). The caps are flat-shaded, the rounded rim
    smooth (and split where the outline itself turns more than `sharp` degrees)."""
    b = depth * 0.3 if bevel is None else bevel
    b = min(b, depth / 2 - 1e-5)
    bm = bmesh.new()
    rings = []
    prof = []
    for k in range(steps + 1):                                  # front rim
        th = (math.pi / 2) * k / steps
        prof.append((b * (1 - math.sin(th)), -depth / 2 + b * (1 - math.cos(th))))
    for k in range(steps + 1):                                  # back rim
        th = (math.pi / 2) * (1 - k / steps)
        prof.append((b * (1 - math.sin(th)), depth / 2 - b * (1 - math.cos(th))))
    if b <= 1e-5:
        prof = [(0.0, -depth / 2), (0.0, depth / 2)]
    for inset, y in prof:
        pts = outlines(inset)
        rings.append([bm.verts.new((u, y, v)) for u, v in pts])
    n = len(rings[0])
    for r0, r1 in zip(rings, rings[1:]):
        for j in range(n):
            bm.faces.new((r0[j], r1[j], r1[(j + 1) % n], r0[(j + 1) % n]))
    front = bm.faces.new(rings[0][::-1])
    backf = bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mats = [m]
    if face is not None:
        mats.append(face)
        front.material_index = 1
    if back is not None:
        mats.append(back)
        backf.material_index = len(mats) - 1
    uvl = bm.loops.layers.uv.new("UVMap")
    for f, mirror_u in ((front, False), (backf, True)):
        us = [v.co.x for v in f.verts]
        vs = [v.co.z for v in f.verts]
        u0, u1, v0, v1 = min(us), max(us), min(vs), max(vs)
        for lp in f.loops:
            u = (lp.vert.co.x - u0) / (u1 - u0)
            lp[uvl].uv = (1 - u if mirror_u else u, (lp.vert.co.z - v0) / (v1 - v0))
    for f in (front, backf):
        for e in f.edges:
            e.smooth = False
    sharp_rad = math.radians(sharp)
    for e in bm.edges:
        if e.smooth and len(e.link_faces) == 2 and e.calc_face_angle(0.0) > sharp_rad:
            e.smooth = False
    for f in bm.faces:
        f.smooth = True
    bmesh.ops.triangulate(bm, faces=[front, backf])
    ob = geo.mesh_object(name, bm, None, smooth_=False)
    for mm in mats:
        ob.data.materials.append(mm)
    if M is not None:
        geo.transform(ob, M)
    return ob


def plate(name, w, h, d, m, center=(0, 0, 0), r=None, bevel=None, seg=3, face=None, back=None, rot=None,
          steps=2):
    """A rounded-rectangle slab w x h (X, Z) and d deep (Y), its front at -Y: signs, cards, screens."""
    r = min(w, h) * 0.12 if r is None else r
    bv = d * 0.3 if bevel is None else bevel
    M = Matrix.Translation(V(*center)) @ (rot.to_4x4() if rot is not None else Matrix.Identity(4))
    return outline_mesh(name, lambda i: rrect(w - 2 * i, h - 2 * i, max(r - i, 1e-4), seg), d, m, bv, steps,
                        face, back, M)


def offset_poly(pts, d):
    """A closed counter-clockwise polygon pushed out by `d` (in by -d), corners mitred (capped at 3x)."""
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        e0 = (p1[0] - p0[0], p1[1] - p0[1])
        e1 = (p2[0] - p1[0], p2[1] - p1[1])
        l0, l1 = math.hypot(*e0) or 1.0, math.hypot(*e1) or 1.0
        n0 = (e0[1] / l0, -e0[0] / l0)                      # outward normal of a CCW edge
        n1 = (e1[1] / l1, -e1[0] / l1)
        m = (n0[0] + n1[0], n0[1] + n1[1])
        ml = math.hypot(*m) or 1.0
        m = (m[0] / ml, m[1] / ml)
        c = max(1 / 3, m[0] * n1[0] + m[1] * n1[1])
        out.append((p1[0] + m[0] * d / c, p1[1] + m[1] * d / c))
    return out


def ccw(pts):
    """The outline, turned counter-clockwise if it was not."""
    area = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))
    return list(pts) if area > 0 else list(pts)[::-1]


def poly_mesh(name, pts2d, depth, m, center=(0, 0, 0), bevel=None, rot=None, steps=2, sharp=60, face=None):
    """A prism of any simple outline (u -> X, v -> Z), its rim rounded by `bevel`."""
    pts2d = ccw(pts2d)
    M = Matrix.Translation(V(*center)) @ (rot.to_4x4() if rot is not None else Matrix.Identity(4))
    return outline_mesh(name, lambda i: offset_poly(pts2d, -i), depth, m, bevel, steps, face, None, M, sharp=sharp)


def pillow(name, radius, thick, m, center=(0, 0, 0), n=50, rings=5, power=2.5, rot=None):
    """A puffy flat shape: the outline `radius(a)` (polar, a = 0 along +X, counter-clockwise seen from the
    front) in the XZ plane, `thick` deep at its middle (Y), rounding to its rim like a cushion."""
    bm = bmesh.new()
    def z(f):
        return thick / 2 * max(0.0, 1 - f ** power) ** (1 / power)
    R = [radius(TAU * j / n) for j in range(n)]
    rim = [bm.verts.new((R[j] * math.cos(TAU * j / n), 0.0, R[j] * math.sin(TAU * j / n))) for j in range(n)]
    sides = []
    for s_ in (-1, 1):
        rows = []
        for k in range(1, rings):
            f = 1 - k / rings
            rows.append([bm.verts.new((f * R[j] * math.cos(TAU * j / n), s_ * z(f), f * R[j] * math.sin(TAU * j / n)))
                         for j in range(n)])
        c = bm.verts.new((0.0, s_ * thick / 2, 0.0))
        rings_ = [rim] + rows
        for r0, r1 in zip(rings_, rings_[1:]):
            for j in range(n):
                bm.faces.new((r0[j], r0[(j + 1) % n], r1[(j + 1) % n], r1[j]))
        last = rings_[-1]
        for j in range(n):
            bm.faces.new((last[j], last[(j + 1) % n], c))
        sides.append(rows)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    ob = geo.mesh_object(name, bm, m)
    M = Matrix.Translation(V(*center)) @ (rot.to_4x4() if rot is not None else Matrix.Identity(4))
    return geo.transform(ob, M)


def polar(poly):
    """The polar outline r(a) of a closed polygon that is star-shaped about the origin."""
    edges = list(zip(poly, poly[1:] + poly[:1]))

    def f(a):
        d = (math.cos(a), math.sin(a))
        best = 0.0
        for (x0, y0), (x1, y1) in edges:
            ex, ey = x1 - x0, y1 - y0
            den = d[0] * ey - d[1] * ex
            if abs(den) < 1e-12:
                continue
            t = (x0 * ey - y0 * ex) / den                  # distance along the ray
            u = (x0 * d[1] - y0 * d[0]) / den              # where along the edge
            if t > 0 and -1e-9 <= u <= 1 + 1e-9:
                best = max(best, t)
        return best
    return f


def star_radius(R, r, points=5, fillet=0.22, steps=4):
    """A classic star (straight edges, a point straight up) with its points and notches rounded, as a
    polar outline."""
    corners = []
    for k in range(2 * points):
        a = math.pi / 2 + math.pi * k / points
        rad = R if k % 2 == 0 else r
        corners.append(V(rad * math.cos(a), rad * math.sin(a), 0))
    poly = []
    n = len(corners)
    for k in range(n):
        p0, p1, p2 = corners[k - 1], corners[k], corners[(k + 1) % n]
        f = fillet if k % 2 == 0 else fillet * 0.6
        a, b = p1.lerp(p0, f), p1.lerp(p2, f)
        for j in range(steps + 1):                         # a quadratic Bezier round the corner
            t = j / steps
            q = a * (1 - t) ** 2 + p1 * 2 * t * (1 - t) + b * t * t
            poly.append((q.x, q.y))
    return polar(poly)


def patch(name, pts, m, toward, smooth_=False):
    """A flat fan from pts[0] (the middle) round pts[1:] (a closed ring), facing `toward`."""
    pts = [V(*q) for q in pts]
    n = len(pts) - 1
    faces = [(0, 1 + j, 1 + (j + 1) % n) for j in range(n)]
    nrm = (pts[1] - pts[0]).cross(pts[2] - pts[0])
    if nrm.dot(V(*toward)) < 0:
        faces = [f[::-1] for f in faces]
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(q) for q in pts], [], faces)
    ob = bpy.data.objects.new(name, me)
    geo.link(ob)
    me.materials.append(m)
    if smooth_:
        me.shade_smooth()
    return ob


def patch_rings(name, mid, rings, m, toward):
    """A curved patch: a fan from `mid` to the first ring, then quads ring to ring (each ring the same
    length, closed), smooth-shaded, facing `toward`."""
    verts = [tuple(mid)] + [tuple(q) for row in rings for q in row]
    n = len(rings[0])
    faces = [(0, 1 + j, 1 + (j + 1) % n) for j in range(n)]
    for r in range(len(rings) - 1):
        a, b = 1 + r * n, 1 + (r + 1) * n
        faces += [(a + j, b + j, b + (j + 1) % n, a + (j + 1) % n) for j in range(n)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    if me.polygons[0].normal.dot(V(*toward)) < 0:
        me.flip_normals()
    ob = bpy.data.objects.new(name, me)
    geo.link(ob)
    me.materials.append(m)
    me.shade_smooth()
    return ob


def capsule(name, a, b, r, m, segs=10, rings=3, r2=None):
    """A capsule from `a` to `b` (the centres of its round ends), radius `r` (easing to `r2` at b)."""
    a, b = V(*a), V(*b)
    ln = (b - a).length
    r2 = r if r2 is None else r2
    prof = [(0.0, -r)]
    for k in range(1, rings + 1):
        th = -math.pi / 2 + (math.pi / 2) * k / rings
        prof.append((r * math.cos(th), r * math.sin(th)))
    for k in range(rings):
        th = (math.pi / 2) * k / rings
        prof.append((r2 * math.cos(th), ln + r2 * math.sin(th)))
    prof.append((0.0, ln + r2))
    return geo.lathe(name, prof, m, a, b - a, segs=segs, caps=False)


def sharpen(ob, angle=35):
    me = ob.data
    me.shade_smooth()
    try:
        me.set_sharp_from_angle(angle=math.radians(angle))
    except (AttributeError, TypeError):
        pass
    return ob


def crisp(ob, flat=0.9999):
    """Smooth shading, with hard edges round the faces that lie flat along a main axis (a bevelled box's
    six faces), so a rounded edge shades smooth and a flat face stays flat."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for f in bm.faces:
        f.smooth = True
        n = f.normal
        if max(abs(n.x), abs(n.y), abs(n.z)) > flat:
            for e in f.edges:
                e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()
    return ob


def box(name, half, m, center=(0, 0, 0), bevel=0.0, segs=2, rot=None):
    """A box of half-sizes `half`, its edges bevelled by `bevel` (a single chamfer on small boxes)."""
    if max(half) < 0.04:
        segs = 1
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.scale(bm, vec=V(*half), verts=bm.verts)
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=bm.verts[:] + bm.edges[:], offset=bevel, segments=segs, profile=0.5,
                        affect="EDGES")
    ob = geo.mesh_object(name, bm, m)
    if bevel > 0:
        crisp(ob)
    else:
        sharpen(ob)
    M = Matrix.Translation(V(*center)) @ (rot.to_4x4() if rot is not None else Matrix.Identity(4))
    return geo.transform(ob, M)


def cyl(name, r, a, b, m, segs=16, bevel=None, r2=None, steps=2):
    """A cylinder (or a frustum, to `r2`) from point `a` to point `b`, its rims rounded by `bevel`, its end
    faces flat-shaded."""
    a, b = V(*a), V(*b)
    ln = (b - a).length
    r2 = r if r2 is None else r2
    bv = min(r, r2, ln / 2) * 0.25 if bevel is None else bevel
    prof = [(0.0, 0.0)]
    for k in range(steps + 1):
        th = (math.pi / 2) * k / steps
        prof.append((r - bv + bv * math.sin(th), bv - bv * math.cos(th)))
    for k in range(steps + 1):
        th = (math.pi / 2) * (1 - k / steps)
        prof.append((r2 - bv + bv * math.sin(th), ln - bv + bv * math.cos(th)))
    prof.append((0.0, ln))
    ob = geo.lathe(name, prof, m, (0, 0, 0), (0, 0, 1), segs=segs, caps=False)
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    for f in bm.faces:
        f.smooth = True
        if abs(f.normal.z) > 0.9999:
            for e in f.edges:
                e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()
    return geo.transform(ob, Matrix.Translation(a) @ geo.basis(b - a).to_4x4())


def ball(name, r, m, center=(0, 0, 0), res=5, scale=(1, 1, 1)):
    """A sphere (or ellipsoid), its grid no finer than its size needs: a knob or an eye does not need the
    300 triangles a fist-sized ball does."""
    res = max(1, min(res, 1 + int(r * max(scale) / 0.012)))
    return geo.superquad(name, (r * scale[0], r * scale[1], r * scale[2]), m, center, n=2.0, res=res)


def sheet(name, w, h, t, m, nx=1, nz=8, center=(0, 0, 0)):
    """A thin closed card w x h (X, Z), t thick, subdivided `nz` times up its height (and `nx` across) so
    it can bend on a bone chain; the front faces -Y."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(w, t, h), verts=bm.verts)
    # cut the long faces into strips
    for axis, cuts in ((2, nz), (0, nx)):
        for k in range(1, cuts):
            co = (-0.5 + k / cuts) * (h if axis == 2 else w)
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            no = V(0, 0, 1) if axis == 2 else V(1, 0, 0)
            p = no * co
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=p, plane_no=no)
    ob = geo.mesh_object(name, bm, m)
    sharpen(ob, 40)
    return geo.transform(ob, Matrix.Translation(V(*center)))


# --------------------------------------------------------------------------------------------- text
def font():
    path = next((p for p in FONTS if p.exists()), None)
    return bpy.data.fonts.load(str(path), check_existing=True) if path else bpy.data.fonts["Bfont"]


def text(name, body, size, m, M=None, fit=None, align="CENTER", res=2, spacing=1.0, line=1.0):
    """Flat text, as a mesh, in the XY plane facing +Z (centred on 0), then put in place by `M`. `fit`
    (width, height) shrinks it to fit. Returns the object."""
    cu = bpy.data.curves.new(name, type="FONT")
    cu.body = body
    cu.font = font()
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.resolution_u = res
    cu.space_character = spacing
    cu.space_line = line
    tmp = bpy.data.objects.new(name + "-curve", cu)
    bpy.context.scene.collection.objects.link(tmp)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp)
    bpy.data.curves.remove(cu)
    me.name = name
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    k = 1.0
    if fit:
        k = min(1.0, fit[0] / w if w else 1.0, fit[1] / h if h and len(fit) > 1 else 1.0)
    me.transform(Matrix.Scale(k, 4) @ Matrix.Translation((-cx if align == "CENTER" else 0, -cy, 0)))
    ob = bpy.data.objects.new(name, me)
    geo.link(ob)
    me.materials.append(m)
    for p in me.polygons:
        p.use_smooth = True                   # flat anyway: smooth keeps vertices shared
    ob["size"] = (w * k, h * k)
    if M is not None:
        geo.transform(ob, M)
    return ob


def facing(normal, up=(0, 0, 1)):
    """A rotation taking text's +Z (its face) to `normal` and its +Y (its up) towards `up`."""
    z = V(*normal).normalized()
    y = V(*up)
    y = (y - z * y.dot(z)).normalized()
    x = y.cross(z)
    return Matrix((x, y, z)).transposed().to_4x4()


def on_front(center, up=(0, 0, 1)):
    """Text facing -Y at `center` (the front of a sign)."""
    return Matrix.Translation(V(*center)) @ facing((0, -1, 0), up)


def on_back(center, up=(0, 0, 1)):
    return Matrix.Translation(V(*center)) @ facing((0, 1, 0), up)


# --------------------------------------------------------------------------------------------- chains
def skin_chain(ob, names, pts, blend=0.35):
    """Weight `ob`'s vertices along a chain of bones: bone i runs pts[i] -> pts[i+1]. Each vertex goes to
    the segment it projects onto, shared with the neighbour across a joint within `blend` of a segment."""
    pts = [V(*p) for p in pts]
    vgs = [ob.vertex_groups.get(n) or ob.vertex_groups.new(name=n) for n in names]
    segs = len(names)
    for v in ob.data.vertices:
        best, bs = None, 0.0
        for i in range(segs):
            a, b = pts[i], pts[i + 1]
            ab = b - a
            t = max(0.0, min(1.0, (v.co - a).dot(ab) / ab.length_squared))
            d = (a + ab * t - v.co).length
            if best is None or d < best[0] - 1e-9:
                best, bs = (d, i), t
        i = best[1]
        s = i + bs                                             # 0..segs along the chain
        w = {}
        j = int(min(segs - 1, math.floor(s)))
        f = s - j
        w[j] = 1.0
        if f > 1 - blend and j + 1 < segs:
            x = (f - (1 - blend)) / (2 * blend)
            w = {j: 1 - x, j + 1: x}
        elif f < blend and j > 0:
            x = (blend - f) / (2 * blend)
            w = {j: 1 - x, j - 1: x}
        for k, x in w.items():
            if x > 1e-4:
                vgs[k].add([v.index], x, "REPLACE")
    return ob


def polyline(pts, n):
    """`n`+1 points evenly spaced along a polyline."""
    pts = [V(*p) for p in pts]
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + (b - a).length)
    out = []
    for k in range(n + 1):
        s = L[-1] * k / n
        i = max(0, min(len(pts) - 2, next((j for j in range(len(L) - 1) if L[j + 1] >= s), len(pts) - 2)))
        t = (s - L[i]) / max(1e-9, L[i + 1] - L[i])
        out.append(pts[i].lerp(pts[i + 1], t))
    return out


# ---------------------------------------------------------------------------------------------- prop
REGISTRY = {}


def prop(name, bits, origin, **info):
    """Register a builder: `name` is the GLB's kebab-case name, `bits` the gags that use it, `origin` where
    its origin sits and which way it faces."""
    def deco(fn):
        REGISTRY[name] = dict(fn=fn, bits=bits, origin=origin, **info)
        return fn
    return deco


class Prop:
    def __init__(self, name):
        self.name = name
        self.P = Palette()
        self.parts = []
        self.R = None
        self.clips = []
        self.show = Matrix.Identity(4)             # where the render puts it (renders only)
        self.display = None                        # (clip name, seconds) to pose it in for the render
        self.view = dict(az=35.0, el=18.0)
        self.root = None
        self.objs = []

    # ---- parts and bones ----
    def add(self, ob, bone="root", node=None, mesh=None):
        for o in (ob if isinstance(ob, (list, tuple)) else [ob]):
            if o is None:
                continue
            if bone and not o.vertex_groups:
                o["bone"] = bone
            if node:
                o["node"] = node
            if mesh:
                o["mesh"] = mesh
            self.parts.append(o)
        return ob

    def bone(self, name, head, tail, parent="root", z=(0, -1, 0)):
        if self.R is None:
            self.R = rig.Rig(self.name)
            if name != "root":
                self.R.bone("root", (0, 0, 0), (0, 0, 0.1), None, z=(0, -1, 0))
        self.R.bone(name, head, tail, parent if name != "root" else None, z=z)
        return name

    def chain(self, prefix, pts, parent="root", z=(0, -1, 0)):
        names = []
        for i in range(len(pts) - 1):
            names.append(self.bone(f"{prefix}_{i + 1}", pts[i], pts[i + 1], names[-1] if names else parent, z=z))
        return names

    def clip(self, name, seconds, fn, loop=False):
        """`fn(t)` -> {bone: dict(turn=[(axis, deg), ...] | (axis, deg), move=(x, y, z), scale=(x, y, z))}."""
        self.clips.append((name, seconds, fn, loop))

    def pose_clip(self, clip):
        """A kit.anim `Clip` of `Pose`s (bone-frame rotations, the pals' own clip language), for props built
        on a pal's skeleton; baked with kit.anim.bake."""
        self.clips.append((clip.name, clip.seconds, ("anim", clip), clip.loop))

    # ---- evaluation ----
    def local(self, bone, spec):
        B = self.R.ob.data.bones[bone].matrix_local.to_3x3()
        Bi = B.inverted()
        q = Quaternion()
        turns = spec.get("turn") or []
        if len(turns) == 2 and isinstance(turns[1], (int, float)):
            turns = [turns]
        for axis, deg in turns:
            q = Quaternion(V(*axis).normalized(), math.radians(deg)) @ q
        ql = (Bi @ q.to_matrix() @ B).to_quaternion()
        mv = spec.get("move")
        lv = Bi @ V(*mv) if mv else Vector()
        sc = V(*spec["scale"]) if spec.get("scale") else V(1, 1, 1)
        return ql, lv, sc

    def pose(self, frame_spec):
        for pb in self.R.ob.pose.bones:
            pb.rotation_mode = "QUATERNION"
            pb.rotation_quaternion = Quaternion()
            pb.location = (0, 0, 0)
            pb.scale = (1, 1, 1)
        for bn, spec in frame_spec.items():
            q, l, s = self.local(bn, spec)
            pb = self.R.ob.pose.bones[bn]
            pb.rotation_quaternion, pb.location, pb.scale = q, l, s
        bpy.context.view_layer.update()

    def bake(self, fps=30):
        arm = self.R.ob
        for name, seconds, fn, loop in self.clips:
            if isinstance(fn, tuple):
                anim.bake(fn[1], anim.Skeleton(arm))
                continue
            # a loop keeps its closing frame too (the same pose as its first): without it the clip is a
            # frame short, so it runs fast and drifts against a pal's loop of the same length
            n = int(round(seconds * fps)) + 1
            frames = [1 + i for i in range(n)]
            samples = [fn(i / fps) for i in range(n)]
            bones = [b.name for b in arm.data.bones if any(b.name in s for s in samples)]
            act = bpy.data.actions.new(f"{name}@{arm.name}")
            slot = act.slots.new(id_type="OBJECT", name=arm.name)
            bag = anim._fcurves_for(act, slot)
            for bn in bones:
                qs, ls, ss = [], [], []
                for s in samples:
                    q, l, sc = self.local(bn, s.get(bn, {}))
                    qs.append(q)
                    ls.append(l)
                    ss.append(sc)
                for i in range(1, len(qs)):
                    if qs[i].dot(qs[i - 1]) < 0:
                        qs[i] = -qs[i]
                path = f'pose.bones["{bn}"]'
                for i in range(4):
                    anim._write(bag, path + ".rotation_quaternion", i, frames, [q[i] for q in qs], bn)
                if any(l.length > 1e-7 for l in ls):
                    for i in range(3):
                        anim._write(bag, path + ".location", i, frames, [l[i] for l in ls], bn)
                if any((s - V(1, 1, 1)).length > 1e-7 for s in ss):
                    for i in range(3):
                        anim._write(bag, path + ".scale", i, frames, [s[i] for s in ss], bn)
            anim._push(arm, act, slot, name, 1)

    # ---- finishing ----
    def finish(self):
        """Join the parts into the prop's objects; returns the objects to export."""
        if os.environ.get("PROPS_PARTS"):
            rows = sorted(((sum(len(f.vertices) - 2 for f in o.data.polygons), o.name) for o in self.parts),
                          reverse=True)
            print("PARTS", self.name, rows[:12])
        if self.R is not None:
            return self._finish_rigged()
        groups = {}
        for ob in self.parts:
            groups.setdefault(ob.get("node", ""), []).append(ob)
        out = {tag: _join(obs, tag or self.name) for tag, obs in groups.items()}
        if "" not in out:
            e = bpy.data.objects.new(self.name, None)
            geo.link(e)
            out[""] = e
        self.root = out[""]
        for tag, j in out.items():
            if tag:
                j.parent = self.root
        self.objs = list(out.values())
        return self.objs

    def _finish_rigged(self):
        """Two ways to attach the parts, chosen by what the file will cost (each mesh primitive is a few
        accessors and buffer views of glTF JSON, about a kilobyte): rigid parts as one mesh per bone,
        parented to that bone (three accessors a primitive, one primitive per material per bone), or every
        part skinned into one mesh, rigid parts at weight 1 on their bone (five accessors a primitive, one
        per material). Parts that bend are always skinned; `self.skin` forces a choice."""
        self.R.build()
        arm = self.R.ob
        skin = getattr(self, "skin", None)
        if skin is None:
            def mats(obs):
                return {m.name for o in obs for m in o.data.materials if m}
            per_bone = {}
            for ob in self.parts:
                if not ob.vertex_groups:
                    per_bone.setdefault((ob.get("bone", "root"), ob.get("node", "")), []).append(ob)
            bent = [o for o in self.parts if o.vertex_groups]
            rigid_cost = 3 * sum(len(mats(obs)) for obs in per_bone.values()) + 5 * len(mats(bent)) \
                + 2 * len(per_bone)
            skin = 5 * len(mats(self.parts)) < rigid_cost
        if skin:
            for ob in self.parts:
                if ob.get("node") and "mesh" not in ob:
                    ob["mesh"] = ob["node"]
            self.objs = [arm, *self.R.finalize(self.parts).values()]
            self.bake()
            self.root = arm
            return self.objs
        rigid, skinned = {}, []
        for ob in self.parts:
            if ob.vertex_groups:
                skinned.append(ob)
            else:
                b = ob.get("bone", "root")
                rigid.setdefault((b, ob.get("node", "")), []).append(ob)
        self.objs = [arm]
        if skinned:
            self.objs += list(self.R.finalize(skinned).values())
        for (b, node), obs in rigid.items():
            j = _join(obs, f"{self.name}-{node or b}")
            if b == "root":
                j.parent = arm
                j.matrix_parent_inverse = Matrix.Identity(4)
            else:
                bn = arm.data.bones[b]
                j.parent = arm
                j.parent_type = "BONE"
                j.parent_bone = b
                # parent-bone space is the bone's tail; keep the mesh where it was built
                j.matrix_parent_inverse = (bn.matrix_local @ Matrix.Translation((0, bn.length, 0))).inverted()
            self.objs.append(j)
        bpy.context.view_layer.update()
        self.bake()
        self.root = arm
        return self.objs

    def tris(self):
        return sum(len(p.vertices) - 2 for o in self.objs if o.type == "MESH" for p in o.data.polygons)

    def export(self, out_dir, raw_dir):
        raw = Path(raw_dir) / f"{self.name}.raw.glb"
        export.glb(raw, self.objs, animations=bool(self.clips))
        dst = Path(out_dir) / f"{self.name}.glb"
        export.compress(raw, dst, tolerance=0.001)
        tidy(dst)
        return dst

    # ---- rendering ----
    def _pose_at(self, clip=None, t=0.0):
        """Pose the prop (NLA muted) at `t` seconds into `clip`, or at rest."""
        if self.R is None:
            return
        ad = self.R.ob.animation_data
        for tr in (ad.nla_tracks if ad else []):
            tr.mute = True
        spec = {}
        if clip:
            fn = next(c[2] for c in self.clips if c[0] == clip)
            if isinstance(fn, tuple):
                self.pose({})
                anim.apply(fn[1], anim.Skeleton(self.R.ob), t)
                return
            spec = fn(t)
        self.pose(spec)

    def _stage(self, lo, hi, res, samples):
        """Camera (three-quarter, from self.view), lights, a shadow-catching floor and render settings
        framing the box lo..hi."""
        centre = (lo + hi) / 2
        radius = max(0.02, (hi - lo).length / 2)
        az, el = math.radians(self.view["az"]), math.radians(self.view["el"])
        d = V(math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el))
        lens = 60
        tan = 18 / lens
        right = (-d).cross(V(0, 0, 1)).normalized()
        up = right.cross(-d)
        dist = 0.0
        for c in (V(x, y, z) for x in (lo.x, hi.x) for y in (lo.y, hi.y) for z in (lo.z, hi.z)):
            o = c - centre
            dist = max(dist, o.dot(d) + max(abs(o.dot(right)), abs(o.dot(up))) * 1.15 / tan)
        cam_d = bpy.data.cameras.new("cam")
        cam_d.lens = lens
        cam_d.clip_start = dist * 0.01
        cam_d.clip_end = dist * 10
        cam = bpy.data.objects.new("cam", cam_d)
        geo.link(cam)
        cam.location = centre + d * dist
        studio.aim(cam, centre)
        bpy.context.scene.camera = cam
        studio.sheet_lights(centre, max(0.25, radius * 1.2))
        studio.world((0.5, 0.5, 0.5), 0.35)
        studio.floor(lo.z, size=radius * 40, color=(0.5, 0.5, 0.5))
        studio.settings(res=(res, res), samples=samples, engine="CYCLES", view="Standard", exposure=-0.9)

    def _framed(self):
        return [o for o in self.objs if not o.name.endswith("beam")]

    def render(self, path, samples=32, res=600):
        """The prop in its display pose (`self.display`), placed by `self.show`."""
        self._pose_at(*(self.display or (None,)))
        self.root.matrix_world = self.show @ self.root.matrix_world
        bpy.context.view_layer.update()
        self._stage(*bounds(self._framed()), res, samples)
        studio.render(path)
        return path

    def strip(self, out_dir, samples=16, res=280):
        """A still per quarter of each clip, one camera framing them all; returns the image paths in rows
        (one row per clip)."""
        self.root.matrix_world = self.show @ self.root.matrix_world
        rows, lo, hi = [], V(1e9, 1e9, 1e9), V(-1e9, -1e9, -1e9)
        shots = [[(c[0], c[1] * k / 4) for k in range(5)] for c in self.clips]
        for row in shots:
            for clip, t in row:
                self._pose_at(clip, t)
                a, b = bounds(self._framed())
                lo = V(min(lo.x, a.x), min(lo.y, a.y), min(lo.z, a.z))
                hi = V(max(hi.x, b.x), max(hi.y, b.y), max(hi.z, b.z))
        self._stage(lo, hi, res, samples)
        for row in shots:
            paths = []
            for clip, t in row:
                self._pose_at(clip, t)
                paths.append(studio.render(Path(out_dir) / f"{self.name}--{clip}--{t:.2f}.png"))
            rows.append(paths)
        return rows


def tidy(path):
    """Shrink a GLB's JSON chunk without changing what it says: floats to 7 significant digits (they are
    float32), the clear-coat extension Blender writes at factor 0 dropped, default accessor fields dropped.
    On a small prop the JSON is often half the file."""
    import json
    import struct
    b = Path(path).read_bytes()
    jl = struct.unpack("<I", b[12:16])[0]
    js = json.loads(b[20:20 + jl])
    rest = b[20 + jl:]

    def walk(v):
        if isinstance(v, float):
            r = float(f"{v:.7g}")
            return int(r) if r == int(r) and abs(r) < 1e15 else r
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, dict):
            return {k: walk(x) for k, x in v.items()}
        return v

    for m in js.get("materials", []):
        ext = m.get("extensions", {})
        if ext.get("KHR_materials_clearcoat", {}).get("clearcoatFactor", 0) == 0:
            ext.pop("KHR_materials_clearcoat", None)
        if not ext:
            m.pop("extensions", None)
    if not any("KHR_materials_clearcoat" in m.get("extensions", {}) for m in js.get("materials", [])):
        js["extensionsUsed"] = [e for e in js.get("extensionsUsed", []) if e != "KHR_materials_clearcoat"]
    for a in js.get("accessors", []):
        if a.get("normalized") is False:
            del a["normalized"]
        if a.get("byteOffset") == 0:
            del a["byteOffset"]
    body = json.dumps(walk(js), separators=(",", ":")).encode()
    body += b" " * (-len(body) % 4)
    Path(path).write_bytes(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(body) + len(rest)) +
                           struct.pack("<II", len(body), 0x4E4F534A) + body + rest)
    return path


def _join(obs, name):
    view = bpy.context.view_layer
    for o in list(bpy.context.selected_objects):
        o.select_set(False)
    for o in obs:
        geo.apply_modifiers(o)
        o.select_set(True)
    view.objects.active = obs[0]
    if len(obs) > 1:
        bpy.ops.object.join()
    j = view.objects.active
    j.name = j.data.name = name
    for k in ("bone", "node", "mesh", "size"):
        if k in j:
            del j[k]
    return j


def bounds(objs):
    dg = bpy.context.evaluated_depsgraph_get()
    lo = V(1e9, 1e9, 1e9)
    hi = V(-1e9, -1e9, -1e9)
    for o in objs:
        if o.type != "MESH":
            continue
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        for v in me.vertices:
            p = ev.matrix_world @ v.co
            lo = V(min(lo.x, p.x), min(lo.y, p.y), min(lo.z, p.z))
            hi = V(max(hi.x, p.x), max(hi.y, p.y), max(hi.z, p.z))
        ev.to_mesh_clear()
    return lo, hi


# ------------------------------------------------------------------------------------- clip helpers
def wobble(t, start, amp, freq=2.2, decay=3.5):
    """A damped oscillation that starts at `start`: 0 before it."""
    if t < start:
        return 0.0
    u = t - start
    return amp * math.exp(-decay * u) * math.sin(TAU * freq * u)


ease = anim.ease
smooth = anim.smooth
pulse = anim.pulse


# Contact sheets are drawn with PIL by the system Python (Blender ships without it); the script gets its
# arguments as JSON: [out path, font path, mode, ...].
_SHEET = r"""
import json, math, sys
from PIL import Image, ImageDraw, ImageFont
out, font, mode, data = json.loads(sys.argv[1])
try:
    f = ImageFont.truetype(font, 15)
except Exception:
    f = ImageFont.load_default()
def label(p):
    return p.replace("\\", "/").split("/")[-1][:-4]
if mode == "grid":
    files, cols, cell = data
    rows = math.ceil(len(files) / cols)
    sh = Image.new("RGB", (cols * cell, rows * (cell + 26)), (60, 60, 62))
    d = ImageDraw.Draw(sh)
    for i, p in enumerate(files):
        im = Image.open(p).convert("RGB").resize((cell, cell), Image.LANCZOS)
        x, y = (i % cols) * cell, (i // cols) * (cell + 26)
        sh.paste(im, (x, y))
        n = label(p)
        d.text((x + (cell - d.textlength(n, font=f)) / 2, y + cell + 4), n, fill=(235, 235, 235), font=f)
else:
    ims = [[Image.open(p).convert("RGB") for p in r] for r in data]
    w, h = ims[0][0].size
    sh = Image.new("RGB", (max(len(r) for r in ims) * w, len(ims) * (h + 22)), (40, 40, 42))
    d = ImageDraw.Draw(sh)
    for j, (r, pr) in enumerate(zip(ims, data)):
        for i, (im, p) in enumerate(zip(r, pr)):
            sh.paste(im, (i * w, j * (h + 22)))
            n = label(p).split("--")
            d.text((i * w + 4, j * (h + 22) + h + 3), n[1] + "  " + n[2] + " s", fill=(230, 230, 230), font=f)
sh.save(out)
"""


def _sheet(path, mode, data):
    import json
    font = str(next((p for p in FONTS if p.exists()), FONTS[-1]))
    try:
        r = subprocess.run(["python", "-c", _SHEET, json.dumps([str(path), font, mode, data])], capture_output=True,
                           text=True)
        if r.returncode:
            print("sheet failed:", r.stderr[-400:])
    except OSError as e:
        print("sheet skipped:", e)
    return path


def strip_sheet(rows, path):
    """Rows of stills side by side, each labelled with its clip and time."""
    return _sheet(path, "strip", [[str(p) for p in row] for row in rows])


def contact_sheet(renders, path, cols=8, cell=300):
    """A labelled grid of the renders."""
    return _sheet(path, "grid", [[str(p) for p in renders], cols, cell])
