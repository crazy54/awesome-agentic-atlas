"""Shapes: the handful of solids every pal is built from, and the plumbing that puts them in the scene.

Conventions, for the whole cast: metres, Z up, the character faces -Y (towards a front camera), and its own
left is +X. A part is built in the rest pose, in world space, and tagged with the bone it rides on
(`part(ob, bone)`); `rig.finalize()` later joins every part into one rigidly skinned mesh per character.

The solids:

  * `superquad`  a superellipsoid on a cube-sphere grid (no poles, so it subdivides and shades evenly), with
                 an optional `shape(p, q)` that moves each vertex: `p` the point, `q` the same point on the
                 unit shape, so a head can taper to its chin or a shell can flatten on one side.
  * `segment`    a superquad stretched from `a` to `b`: a limb shell with a taper, a bulge and a flat side.
  * `sweep`      a superelliptic section swept along a path, its half-width and half-height varying along it:
                 a crest, a horn, a cable, a strip of piping (`tube` is the round case).
  * `lathe`      a profile `[(radius, height), ...]` spun round an axis: joint discs, ear cups, lenses, rings.
  * `Surface`    ray casts against a finished part, for laying trim and decals onto it.
"""
from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

TAU = math.tau


def V(*a) -> Vector:
    return Vector(a)


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x


def smooth(e0, e1, x):
    """Smoothstep from 0 at e0 to 1 at e1 (either order)."""
    if e0 == e1:
        return 0.0 if x < e0 else 1.0
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------------------------------------- scene
_into = [None]


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _into[0] = None


def collection(name, parent=None):
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def into(col):
    """Every solid made from here on goes into `col`."""
    _into[0] = col
    return col


def link(ob):
    (_into[0] or bpy.context.scene.collection).objects.link(ob)
    return ob


def basis(z_dir, y_hint=(0, 1, 0)) -> Matrix:
    """A rotation whose Z is `z_dir` and whose Y leans towards `y_hint`."""
    z = Vector(z_dir).normalized()
    y = Vector(y_hint)
    y = (y - z * y.dot(z))
    if y.length < 1e-6:
        y = Vector((1, 0, 0)) - z * z.x
    y.normalize()
    x = y.cross(z)
    return Matrix((x, y, z)).transposed()


def mesh_object(name, bm, mat=None, smooth_=True):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    link(ob)
    if mat is not None:
        me.materials.append(mat)
    if smooth_:
        me.shade_smooth()
    return ob


def part(ob, bone):
    """Tag a solid with the bone it rides on."""
    for o in (ob if isinstance(ob, (list, tuple)) else [ob]):
        o["bone"] = bone
    return ob


def transform(ob, M):
    """Bake a world transform into a part's mesh (parts keep identity object transforms)."""
    ob.data.transform(M)
    ob.data.update()
    return ob


def mirror(ob, name=None, swap=True):
    """A mirror image of a part across X=0, its bone's side swapped (`_L` <-> `_R`)."""
    me = ob.data.copy()
    me.transform(Matrix.Scale(-1, 4, (1, 0, 0)))
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
    bm.to_mesh(me)
    bm.free()
    new = bpy.data.objects.new(name or flip_name(ob.name), me)
    link(new)
    for m in ob.modifiers:
        nm = new.modifiers.new(m.name, m.type)
        for attr in ("levels", "render_levels", "width", "segments", "limit_method", "angle_limit",
                     "harden_normals", "profile"):
            if hasattr(m, attr):
                try:
                    setattr(nm, attr, getattr(m, attr))
                except AttributeError:
                    pass
    if "bone" in ob and swap:
        new["bone"] = flip_name(ob["bone"])
    for k in ob.keys():
        if k not in ("bone",) and k not in new:
            new[k] = ob[k]
    return new


def flip_name(n):
    for a, b in (("_L", "_R"), ("_R", "_L"), (".L", ".R"), (".R", ".L"), ("-L", "-R"), ("-R", "-L")):
        if n.endswith(a):
            return n[: -len(a)] + b
        if a + "_" in n:
            return n.replace(a + "_", b + "_")
        if a + "-" in n:
            return n.replace(a + "-", b + "-")
    return n


def subsurf(ob, levels=1):
    m = ob.modifiers.new("subsurf", "SUBSURF")
    m.levels = m.render_levels = levels
    return ob


def bevel(ob, width, segments=3, angle=35.0):
    m = ob.modifiers.new("bevel", "BEVEL")
    m.width, m.segments = width, segments
    m.limit_method, m.angle_limit = "ANGLE", math.radians(angle)
    m.harden_normals = False
    return ob


def apply_modifiers(ob):
    if not ob.modifiers:
        return ob
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=True, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return ob


def box_uv(ob, tile=0.5):
    """UVs by box projection in metres, `tile` metres to one repeat: the same texel size on every part."""
    me = ob.data
    if not me.uv_layers:
        me.uv_layers.new(name="UVMap")
    uv = me.uv_layers.active.data
    for poly in me.polygons:
        n = poly.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            u, v = [(co.y, co.z), (co.x, co.z), (co.x, co.y)][ax]
            uv[li].uv = (u / tile, v / tile)
    return ob


# --------------------------------------------------------------------------------------------- solids
def _spherify(c: Vector) -> Vector:
    """Cube surface point -> unit sphere, evenly spaced (the 'spherified cube' map)."""
    x, y, z = c.x, c.y, c.z
    x2, y2, z2 = x * x, y * y, z * z
    return Vector((x * math.sqrt(max(0.0, 1 - y2 / 2 - z2 / 2 + y2 * z2 / 3)),
                   y * math.sqrt(max(0.0, 1 - z2 / 2 - x2 / 2 + z2 * x2 / 3)),
                   z * math.sqrt(max(0.0, 1 - x2 / 2 - y2 / 2 + x2 * y2 / 3))))


def superquad(name, radii, mat, center=(0, 0, 0), n=2.0, shape=None, res=10, rot=None, smooth_=True):
    """A superellipsoid of half-sizes `radii` (n=2 an ellipsoid, 3..5 a softening box). `n` may be a
    3-tuple: the exponent along each of x, y, z. `shape(p, q)` reshapes each point, `p` the scaled point and
    `q` its place on the unit shape. Built about the origin, then turned by `rot` and moved to `center`."""
    nx, ny, nz = (n, n, n) if not isinstance(n, (tuple, list)) else n
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=res, use_grid_fill=True)
    for v in bm.verts:
        u = _spherify(v.co)
        # Scale the sphere direction onto the superellipsoid |x|^nx + |y|^ny + |z|^nz = 1 (bisection, since
        # the exponents may differ per axis).
        lo, hi = 0.0, 2.0
        for _ in range(40):
            k = (lo + hi) / 2
            f = abs(u.x * k) ** nx + abs(u.y * k) ** ny + abs(u.z * k) ** nz
            lo, hi = (k, hi) if f < 1 else (lo, k)
        q = u * ((lo + hi) / 2)
        p = Vector((q.x * radii[0], q.y * radii[1], q.z * radii[2]))
        v.co = shape(p, q) if shape else p
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    ob = mesh_object(name, bm, mat, smooth_)
    M = Matrix.Translation(Vector(center))
    if rot is not None:
        M = M @ (rot.to_4x4() if rot.__len__() == 3 else rot)
    return transform(ob, M)


def segment(name, a, b, ra, mat, rb=None, n=2.2, flat=1.0, bulge=0.0, front=0.0, ext=0.0, y_hint=(0, 1, 0),
            res=10, shape=None, smooth_=True):
    """A limb shell from `a` to `b`: radius `ra` at a easing to `rb` at b, squashed front-to-back by `flat`,
    swollen in the middle by `bulge` and on its front (-Y side of `y_hint`) by `front`; `ext` lengthens it
    past both ends."""
    a, b = Vector(a), Vector(b)
    rb = ra if rb is None else rb
    half = (b - a).length / 2 + ext

    def f(p, q):
        t = (q.z + 1) / 2
        s = lerp(ra, rb, smooth(0, 1, t)) / ra * (1 + bulge * (1 - q.z * q.z))
        p = Vector((p.x * s, p.y * s, p.z))
        if front and q.y < 0:
            p.y *= 1 + front * (1 - q.z * q.z)
        return shape(p, q) if shape else p

    return superquad(name, (ra, ra * flat, half), mat, (a + b) / 2, n=n, shape=f, res=res,
                     rot=basis(b - a, y_hint), smooth_=smooth_)


def _frames(pts, up_hint):
    """Parallel-transported frames (tangent, normal, binormal) along a polyline, normal leaning to up_hint."""
    T = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        t = (b - a)
        T.append(t.normalized() if t.length > 1e-9 else Vector((0, 0, 1)))
    up = Vector(up_hint)
    N = []
    n = (up - T[0] * up.dot(T[0]))
    if n.length < 1e-6:
        n = T[0].orthogonal()
    n.normalize()
    for i, t in enumerate(T):
        if i:
            # rotate the previous normal by the turn between tangents
            q = T[i - 1].rotation_difference(t)
            n = q @ n
            n = (n - t * n.dot(t)).normalized()
        N.append(n.copy())
    return T, N, [t.cross(n) for t, n in zip(T, N)]


def sweep(name, pts, half_w, half_h, mat, n=2.0, segs=16, up=(0, 0, 1), caps=True, twist=None, smooth_=True,
          closed=False):
    """A section swept along `pts`: at each point a superellipse of half-sizes (half_w[i] across the
    binormal, half_h[i] along the normal, normal leaning towards `up`). Either size list may be a number.
    Ends whose size is near zero close to a point; otherwise `caps` fans them shut."""
    pts = [Vector(p) for p in pts]
    m = len(pts)
    hw = half_w if isinstance(half_w, (list, tuple)) else [half_w] * m
    hh = half_h if isinstance(half_h, (list, tuple)) else [half_h] * m
    T, N, B = _frames(pts, up)
    bm = bmesh.new()
    rings = []
    for i, p in enumerate(pts):
        ring = []
        tw = twist[i] if twist else 0.0
        for j in range(segs):
            a = TAU * j / segs + tw
            c, s = math.cos(a), math.sin(a)
            cx = math.copysign(abs(c) ** (2 / n), c)
            sy = math.copysign(abs(s) ** (2 / n), s)
            ring.append(bm.verts.new(p + B[i] * (cx * hw[i]) + N[i] * (sy * hh[i])))
        rings.append(ring)
    for i in range(m - 1 + (1 if closed else 0)):
        r0, r1 = rings[i], rings[(i + 1) % m]
        for j in range(segs):
            bm.faces.new((r0[j], r0[(j + 1) % segs], r1[(j + 1) % segs], r1[j]))
    if caps and not closed:
        for ring, rev in ((rings[0], True), (rings[-1], False)):
            c = sum((v.co for v in ring), Vector()) / segs
            cv = bm.verts.new(c)
            for j in range(segs):
                f = (ring[j], ring[(j + 1) % segs], cv)
                bm.faces.new(f[::-1] if rev else f)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return mesh_object(name, bm, mat, smooth_)


def tube(name, pts, radius, mat, radii=None, segs=10, caps=True, up=(0, 0, 1), closed=False):
    r = radii if radii is not None else radius
    return sweep(name, pts, r, r, mat, n=2.0, segs=segs, up=up, caps=caps, closed=closed)


def lathe(name, profile, mat, center=(0, 0, 0), axis=(0, 0, 1), segs=32, y_hint=(0, 1, 0), smooth_=True,
          caps=True, arc=None):
    """Spin `profile`, a list of (radius, height) running from one end to the other, round `axis` through
    `center`. A radius of 0 closes that end to a point; otherwise `caps` fans the ends flat. `arc` spins
    only part of the way round (radians)."""
    bm = bmesh.new()
    full = arc is None
    n = segs if full else segs + 1
    sweep_ = TAU if full else arc
    rings = []
    for r, h in profile:
        ring = []
        for j in range(n):
            a = sweep_ * j / segs
            ring.append(bm.verts.new((r * math.cos(a), r * math.sin(a), h)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        r0, r1 = rings[i], rings[i + 1]
        for j in range(segs):
            k = (j + 1) % n if full else j + 1
            bm.faces.new((r0[j], r0[k], r1[k], r1[j]))
    if caps and full:
        for ring, (r, h), rev in ((rings[0], profile[0], True), (rings[-1], profile[-1], False)):
            if r > 1e-6:
                cv = bm.verts.new((0, 0, h))
                for j in range(segs):
                    f = (ring[j], ring[(j + 1) % n], cv)
                    bm.faces.new(f[::-1] if rev else f)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    ob = mesh_object(name, bm, mat, smooth_)
    return transform(ob, Matrix.Translation(Vector(center)) @ basis(axis, y_hint).to_4x4())


def rounded_profile(r_outer, depth, bevel_r, r_inner=0.0, steps=4, front_bulge=0.0):
    """A lathe profile for a disc or ring of radius r_outer and thickness `depth` (centred on 0), its rims
    rounded by `bevel_r`. With r_inner > 0 it is a ring with a hole; `front_bulge` domes the +Z face."""
    b = min(bevel_r, depth / 2, (r_outer - r_inner) / 2 - 1e-4)
    out = []
    h0, h1 = -depth / 2, depth / 2
    if r_inner <= 0:
        out.append((0.0, h0))
    else:
        for i in range(steps + 1):
            a = math.pi + (math.pi / 2) * i / steps          # inner bottom rim, going outward
            out.append((r_inner + b + b * math.cos(a), h0 + b + b * math.sin(a)))
    for i in range(steps + 1):
        a = -math.pi / 2 + (math.pi / 2) * i / steps
        out.append((r_outer - b + b * math.cos(a), h0 + b + b * math.sin(a)))
    for i in range(steps + 1):
        a = (math.pi / 2) * i / steps
        out.append((r_outer - b + b * math.cos(a), h1 - b + b * math.sin(a)))
    if r_inner <= 0:
        if front_bulge:
            for i in range(1, 6):
                t = i / 6
                rr = (r_outer - b) * (1 - t)
                out.append((rr, h1 + front_bulge * math.sin(t * math.pi / 2)))
        out.append((0.0, h1 + front_bulge))
    else:
        for i in range(steps + 1):
            a = math.pi / 2 + (math.pi / 2) * i / steps
            out.append((r_inner + b + b * math.cos(a), h1 - b + b * math.sin(a)))
        out.append(out[0])
    return out


def disc(name, radius, depth, mat, center, axis, bevel_r=None, r_inner=0.0, segs=32, bulge=0.0):
    prof = rounded_profile(radius, depth, bevel_r if bevel_r is not None else depth * 0.3, r_inner,
                           front_bulge=bulge)
    return lathe(name, prof, mat, center, axis, segs=segs, caps=False)


def ring(name, major, minor, mat, center, axis, segs=40, sides=10, y_hint=(0, 1, 0), squash=1.0):
    """A torus round `axis`; `squash` flattens its section along the axis."""
    prof = [(major + minor * math.cos(TAU * i / sides), minor * squash * math.sin(TAU * i / sides))
            for i in range(sides + 1)]
    return lathe(name, prof, mat, center, axis, segs=segs, y_hint=y_hint, caps=False)


def sphere(name, radius, mat, center=(0, 0, 0), res=8, scale=(1, 1, 1)):
    return superquad(name, (radius * scale[0], radius * scale[1], radius * scale[2]), mat, center, n=2.0,
                     res=res)


# -------------------------------------------------------------------------------------------- surface
class Surface:
    """Ray casts against one or more finished parts (modifiers applied), in world space."""

    def __init__(self, *obs):
        dg = bpy.context.evaluated_depsgraph_get()
        bm = bmesh.new()
        for ob in obs:
            ev = ob.evaluated_get(dg)
            me = ev.to_mesh()
            tmp = bmesh.new()
            tmp.from_mesh(me)
            tmp.transform(ob.matrix_world)
            m2 = bpy.data.meshes.new("_tmp")
            tmp.to_mesh(m2)
            tmp.free()
            bm.from_mesh(m2)
            bpy.data.meshes.remove(m2)
            ev.to_mesh_clear()
        self.tree = BVHTree.FromBMesh(bm)
        bm.free()

    def cast(self, origin, direction, dist=20.0):
        loc, nor, _, _ = self.tree.ray_cast(Vector(origin), Vector(direction).normalized(), dist)
        return (loc, nor) if loc is not None else (None, None)

    def front(self, x, z, y0=-5.0, offset=0.0):
        loc, nor = self.cast((x, y0, z), (0, 1, 0))
        return None if loc is None else loc + nor * offset

    def back(self, x, z, y0=5.0, offset=0.0):
        loc, nor = self.cast((x, y0, z), (0, -1, 0))
        return None if loc is None else loc + nor * offset

    def side(self, y, z, s=1, x0=5.0, offset=0.0):
        loc, nor = self.cast((s * x0, y, z), (-s, 0, 0))
        return None if loc is None else loc + nor * offset

    def toward(self, point, centre, offset=0.0, far=2.0):
        """The surface point on the line from far outside `point` in towards `centre`."""
        p, c = Vector(point), Vector(centre)
        d = (c - p).normalized()
        loc, nor = self.cast(p - d * far, d, far * 4)
        return None if loc is None else loc + nor * offset

    def nearest(self, point, offset=0.0):
        loc, nor, _, _ = self.tree.find_nearest(Vector(point))
        return None if loc is None else loc + nor * offset

    def normal_at(self, point):
        _, nor, _, _ = self.tree.find_nearest(Vector(point))
        return nor
