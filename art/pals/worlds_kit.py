"""The Atlas Core's worlds: the vocabulary they are built from (islands, trees, rocks, bots, arcs, rings,
cards, screens, glows, text), the node tree each world is joined into, the baker that writes its `appear`
and `idle` clips, and the preview renders. `worlds.py` composes the worlds out of these.

UNIT SPACE. A world stands on the Core's projection disc: radius 1.0 at Z = 0, +Y at the back, the reader
in front (-Y) and above. Everything stays inside that radius and below Z = 1.3, moving parts included
(`World.check()` measures every baked frame).

NODES. A world is a tree of nodes under one root empty, `world_<slug>`. A node is one joined mesh (a glTF
primitive per material) with its origin at a pivot. Parts are built in world space inside `with W.on(node):`
(each node collects its solids in a collection of its own, the way `geo.into` works) and `finalize()` joins
them. A node's motion is a delta about its pivot in its parent's frame: `idle(t)` for the 4 s loop, and
`appear(t)` for the 0.8 s entrance, which ends exactly on idle's first frame. Islands pop up with an
overshoot, hologram nodes flicker on, everything else rides on its parent.

MATERIALS. One shared palette, `M(name)`: matte island colours and a few paints for props, and the
holograms, every one named `holo_*` (emissive, double-sided), which the page swaps for additive shaders.
Solids are single-sided closed shells, as on the pals.
"""
from __future__ import annotations

import json
import math
import random
import struct
from contextlib import contextmanager
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

from kit import geo, mat, studio
from kit.anim import _fcurves_for, _push, _write, ease, smooth
from kit.geo import TAU, V

FPS = 30
IDLE_S, APPEAR_S = 4.0, 0.8
RADIUS, HEIGHT = 1.0, 1.3

# ------------------------------------------------------------------------------------------ palette
CYAN = "#2fe3f1"
LIME = "#b9e23c"                      # Archie's lime, lifted to glow: the sheet's arcs and paths
FAMILY = {"run": "#5BD5AA", "build": "#78B7F4", "extend": "#A99AF7", "data": "#E7B64D", "trust": "#EF7D86",
          "connect": "#9BA5B3"}

SOLID = {
    # name: (hex, roughness, metallic)
    "grass": ("#97c93d", 0.85, 0.0), "grass_dark": ("#6fa935", 0.85, 0.0),
    "soil": ("#b78a5c", 0.9, 0.0), "rock": ("#a08870", 0.9, 0.0), "rock_dark": ("#6a5c50", 0.9, 0.0),
    "leaf": ("#5aa83f", 0.8, 0.0), "pine": ("#2f7d4a", 0.8, 0.0), "trunk": ("#7a5434", 0.85, 0.0),
    "stone": ("#bfb8ad", 0.75, 0.0), "cream": ("#efe8dc", 0.35, 0.0), "graphite": ("#2c2e33", 0.45, 0.0),
    "metal": ("#a4a9af", 0.35, 0.8), "wood": ("#b37b47", 0.75, 0.0), "brass": ("#c99a45", 0.35, 0.9),
    "sand": ("#ead08e", 0.9, 0.0), "paper": ("#f6f0e2", 0.6, 0.0),
    "red": ("#e0564e", 0.5, 0.0), "yellow": ("#f3c24c", 0.5, 0.0), "blue": ("#4d8fe0", 0.5, 0.0),
    "orange": ("#f08a3a", 0.5, 0.0), "violet": ("#8c6fe0", 0.5, 0.0), "mint": ("#4fc79c", 0.5, 0.0),
    "pink": ("#f08fb8", 0.5, 0.0), "black": ("#141518", 0.4, 0.0), "velvet": ("#a3122d", 0.7, 0.0),
    "mirror": ("#dfe4ea", 0.12, 1.0), "white": ("#fbfaf6", 0.5, 0.0), "cardboard": ("#c9a06b", 0.85, 0.0),
    "lime": ("#a4c812", 0.45, 0.0),
}
FLAT = {"mirror"}                             # solids that keep their facets
HOLO = {
    # name: (hex, strength)
    "holo_cyan": (CYAN, 3.0), "holo_lime": (LIME, 3.0), "holo_panel": ("#0e5a66", 2.0),
    "holo_white": ("#e6fbff", 2.5), "holo_magenta": ("#ff4fd8", 3.0),
    **{f"holo_{k}": (v, 3.0) for k, v in FAMILY.items()},
}
_mats: dict = {}


def M(name):
    """The palette's material `name`, made the first time a world asks for it. Parts are built with the
    palette's names; `finalize()` then turns every solid colour into vertex colour on one of two shared
    materials, `solid` and `solid_metal`, so a node is one primitive plus one per hologram colour."""
    m = _mats.get(name)
    if m is not None and m.name in bpy.data.materials:
        return m
    if name in SOLID:
        hx, rough, metal = SOLID[name]
        m = mat.principled(name, hx, metal=metal, rough=rough, spec=0.4)
    elif name in ("solid", "solid_metal"):
        metal = name == "solid_metal"
        m = mat.principled(name, "#ffffff", metal=0.85 if metal else 0.0, rough=0.38 if metal else 0.62,
                           spec=0.4)
        nt = m.node_tree
        vc = nt.nodes.new("ShaderNodeVertexColor")
        vc.layer_name = "Col"
        nt.links.new(vc.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    elif name in HOLO:
        hx, strength = HOLO[name]
        m = mat.principled(name, hx, rough=0.4, emit=hx, strength=strength)
        m.use_backface_culling = False        # glTF doubleSided: holograms are seen through
    else:
        raise KeyError(name)
    m.name = name
    _mats[name] = m
    return m


def _mottle(co, amount):
    n = math.sin(co.x * 23.1 + co.y * 7.3) * 0.5 + math.sin(co.x * 5.7 - co.y * 19.1 + 1.3) * 0.5
    return 1 + amount * n


def _depth(co):
    """Darker towards an island's tip (islands pivot on their grass, so z is depth below it)."""
    u = min(1.0, max(0.0, -co.z / 0.4))
    return 1.0 - 0.38 * u * u * (3 - 2 * u)


# Solid colours shaded per vertex: grass and leaves mottled, an island's underside darkening downwards.
VARIED = {"grass": lambda co: _mottle(co, 0.09), "grass_dark": lambda co: _mottle(co, 0.06),
          "leaf": lambda co: _mottle(co, 0.12),
          "pine": lambda co: _mottle(co, 0.12), "soil": lambda co: _depth(co) * 1.04, "rock": _depth}

SHARP = math.radians(62)                      # boxes and caps keep their edges; hexagons and balls go smooth


def _colour_and_shade(ob):
    """Solid palette colours -> a corner colour attribute on `solid`/`solid_metal`; every face smooth, with
    sharp edges only between solid faces meeting at more than SHARP (a hologram's normals do not matter)."""
    me = ob.data
    names = [s.material.name if s.material else "stone" for s in ob.material_slots]
    out = []

    def slot(n):
        if n not in out:
            out.append(n)
        return out.index(n)

    remap, colour = [], []
    for n in names:
        if n in SOLID:
            remap.append(slot("solid_metal" if SOLID[n][2] > 0.5 else "solid"))
            colour.append(mat.srgb(SOLID[n][0]))
        else:
            remap.append(slot(n))
            colour.append((1.0, 1.0, 1.0, 1.0))
    bm = bmesh.new()
    bm.from_mesh(me)
    for f in bm.faces:
        f.smooth = names[f.material_index] not in FLAT
    for e in bm.edges:
        lf = e.link_faces
        if len(lf) == 2 and all(names[f.material_index] in SOLID for f in lf):
            e.smooth = e.calc_face_angle(0.0) <= SHARP
    bm.to_mesh(me)
    bm.free()
    idx = [0] * len(me.polygons)
    me.polygons.foreach_get("material_index", idx)
    corner = []
    for poly, mi in zip(me.polygons, idx):
        n = names[mi]
        if n not in VARIED:
            corner.extend(colour[mi] * poly.loop_total)
            continue
        for li in poly.loop_indices:
            k = VARIED[n](me.vertices[me.loops[li].vertex_index].co)
            c = colour[mi]
            corner.extend((c[0] * k, c[1] * k, c[2] * k, 1.0))
    if any(n in SOLID for n in names):
        attr = me.color_attributes.new("Col", "BYTE_COLOR", "CORNER")
        attr.data.foreach_set("color", corner)
    me.materials.clear()                      # (which zeroes every face's material index)
    for n in out:
        me.materials.append(M(n))
    me.polygons.foreach_set("material_index", [remap[i] for i in idx])
    me.update()


def accent(family):
    return f"holo_{family}" if family in FAMILY else "holo_cyan"


# ------------------------------------------------------------------------------------------- meshes
class Mesh:
    """Polygons, each with a material name and a shading flag, turned into one object. Rings run
    counter-clockwise seen from +Z; `bridge(lower, upper)` and `fan(ring, apex)` then face outwards."""

    def __init__(self):
        self.v, self.f = [], []

    def add(self, p):
        self.v.append(tuple(p))
        return len(self.v) - 1

    def ring(self, pts):
        return [self.add(p) for p in pts]

    def face(self, idx, m, smooth_=False):
        self.f.append((tuple(idx), m, smooth_))

    def bridge(self, a, b, m, smooth_=False, closed=True):
        n = len(a)
        for i in range(n if closed else n - 1):
            j = (i + 1) % n
            self.face((a[i], a[j], b[j], b[i]), m, smooth_)

    def fan(self, ring, apex, m, smooth_=False, down=False):
        n = len(ring)
        for i in range(n):
            j = (i + 1) % n
            self.face((ring[j], ring[i], apex) if down else (ring[i], ring[j], apex), m, smooth_)

    def cap(self, ring, m, down=False, smooth_=False):
        self.face(ring[::-1] if down else ring, m, smooth_)

    def build(self, name="part", M_=None, recalc=False):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], [f[0] for f in self.f])
        names = []
        for _, m, _ in self.f:
            if m not in names:
                names.append(m)
        for m in names:
            me.materials.append(M(m))
        me.polygons.foreach_set("material_index", [names.index(m) for _, m, _ in self.f])
        me.polygons.foreach_set("use_smooth", [s for _, _, s in self.f])
        if M_ is not None:
            me.transform(M_)
        if recalc:
            bm = bmesh.new()
            bm.from_mesh(me)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bm.to_mesh(me)
            bm.free()
        me.update()
        ob = bpy.data.objects.new(name, me)
        return geo.link(ob)


def rot3(r):
    """A 3x3 rotation from None, an Euler in degrees (x, y, z), a Matrix or a Quaternion."""
    if r is None:
        return Matrix.Identity(3)
    if isinstance(r, Quaternion):
        return r.to_matrix()
    if isinstance(r, Matrix):
        return r.to_3x3()
    return Euler([math.radians(a) for a in r], "XYZ").to_matrix()


def place(c=(0, 0, 0), r=None, s=1.0):
    S = Matrix.Diagonal((*s, 1.0)) if isinstance(s, (tuple, list)) else Matrix.Scale(s, 4)
    return Matrix.Translation(Vector(c)) @ rot3(r).to_4x4() @ S


def circle(n, r, z=0.0, a0=0.0, ry=None):
    ry = r if ry is None else ry
    return [V(r * math.cos(a0 + TAU * i / n), ry * math.sin(a0 + TAU * i / n), z) for i in range(n)]


def prism(m, c, r, h, n=6, r_top=None, rot=None, a0=None, bottom=True, top=True, smooth_=False, ry=None,
          mtop=None, scale=1.0):
    """A frustum standing on `c` (its base centre), `h` tall along its local Z; `r_top` 0 makes a cone."""
    r_top = r if r_top is None else r_top
    a0 = (math.pi / n if n == 4 else 0.0) if a0 is None else a0
    ry_ = r if ry is None else ry
    g = Mesh()
    lo = g.ring(circle(n, r, 0.0, a0, ry_))
    if r_top <= 1e-6:
        g.fan(lo, g.add((0, 0, h)), m, smooth_)
    else:
        hi = g.ring(circle(n, r_top, h, a0, ry_ * r_top / r))
        g.bridge(lo, hi, m, smooth_)
        if top:
            g.cap(hi, mtop or m)
    if bottom:
        g.cap(lo, m, down=True)
    return g.build("prism", place(c, rot, scale))


def box(m, c, size, rot=None, mtop=None):
    """A box of full size (sx, sy, sz) centred on `c`."""
    sx, sy, sz = (s / 2 for s in size)
    g = Mesh()
    lo = g.ring([(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz)])
    hi = g.ring([(-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)])
    g.bridge(lo, hi, m)
    g.cap(hi, mtop or m)
    g.cap(lo, m, down=True)
    return g.build("box", place(c, rot))


def slab(m, c, pts, h, rot=None, mside=None, bottom=True):
    """A flat outline `pts` (x, y, counter-clockwise) extruded `h` up from `c`, then turned by `rot`."""
    g = Mesh()
    lo = g.ring([(x, y, 0.0) for x, y in pts])
    hi = g.ring([(x, y, h) for x, y in pts])
    g.bridge(lo, hi, mside or m)
    g.cap(hi, m)
    if bottom:
        g.cap(lo, mside or m, down=True)
    ob = g.build("slab", place(c, rot))
    _triangulate(ob)
    return ob


def _triangulate(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 4], quad_method="BEAUTY",
                          ngon_method="EAR_CLIP")
    bm.to_mesh(ob.data)
    bm.free()


def ico(m, c, r, scale=(1, 1, 1), seed=0, jitter=0.12, subdiv=1, rot=None, smooth_=False):
    """A faceted ball (an icosahedron, 20 faces; `subdiv` 2 is 80), each vertex nudged by `jitter`."""
    rng = random.Random(seed)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    for v in bm.verts:
        v.co *= 1 + rng.uniform(-jitter, jitter)
    me = bpy.data.meshes.new("ico")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(M(m))
    if smooth_:
        me.shade_smooth()
    me.transform(place(c, rot, tuple(r * s for s in scale)))
    return geo.link(bpy.data.objects.new("ico", me))


def ball(m, c, r, segs=8, rings=4, scale=(1, 1, 1), rot=None):
    """A smooth low-poly sphere (a lathe with `rings` bands)."""
    prof = [(math.sin(math.pi * i / rings), -math.cos(math.pi * i / rings)) for i in range(rings + 1)]
    ob = geo.lathe("ball", prof, M(m), segs=segs, caps=False)
    return geo.transform(ob, place(c, rot, tuple(r * s for s in scale)))


def lathe(m, c, prof, segs=10, rot=None, smooth_=True):
    ob = geo.lathe("lathe", prof, M(m), segs=segs, smooth_=smooth_)
    return geo.transform(ob, place(c, rot))


def tube(m, pts, r, sides=5, caps=True):
    return geo.tube("tube", [Vector(p) for p in pts], r, M(m), segs=sides, caps=caps)


def torus(m, c, major, minor, rot=None, segs=16, sides=5, arc=None):
    prof = [(major + minor * math.cos(TAU * i / sides), minor * math.sin(TAU * i / sides))
            for i in range(sides + 1)]
    ob = geo.lathe("torus", prof, M(m), segs=segs, caps=False, arc=arc)
    return geo.transform(ob, place(c, rot))


def flat_ring(m, c, r, w, segs=32, rot=None, dashes=None, duty=0.6, arc=None):
    """A flat annulus of radius `r`, `w` wide, lying in its local XY plane; with `dashes` it is broken
    into that many dashes, each `duty` of its share long."""
    g = Mesh()
    if dashes:
        for k in range(dashes):
            a0 = TAU * k / dashes
            a1 = a0 + TAU * duty / dashes
            pts = []
            for a in (a0, a1):
                pts.append(((r - w / 2) * math.cos(a), (r - w / 2) * math.sin(a), 0))
                pts.append(((r + w / 2) * math.cos(a), (r + w / 2) * math.sin(a), 0))
            i = g.ring(pts)
            g.face((i[0], i[1], i[3], i[2]), m)
    else:
        span = TAU if arc is None else arc
        n = segs if arc is None else segs + 1
        inner = g.ring([((r - w / 2) * math.cos(span * i / segs), (r - w / 2) * math.sin(span * i / segs), 0)
                        for i in range(n)])
        outer = g.ring([((r + w / 2) * math.cos(span * i / segs), (r + w / 2) * math.sin(span * i / segs), 0)
                        for i in range(n)])
        g.bridge(outer, inner, m, closed=arc is None)
    return g.build("ring", place(c, rot))


def quad(m, c, w, h, rot=None):
    """A flat rectangle `w` x `h` facing -Y (in its local XZ plane) at `c`."""
    g = Mesh()
    i = g.ring([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)])
    g.face(i, m)
    return g.build("quad", place(c, rot))


def frame(m, c, w, h, t, rot=None):
    """A flat rectangular outline facing -Y: four bars `t` wide round a `w` x `h` panel."""
    g = Mesh()
    o = g.ring([(-w / 2, 0, -h / 2), (w / 2, 0, -h / 2), (w / 2, 0, h / 2), (-w / 2, 0, h / 2)])
    i = g.ring([(-w / 2 + t, 0, -h / 2 + t), (w / 2 - t, 0, -h / 2 + t), (w / 2 - t, 0, h / 2 - t),
                (-w / 2 + t, 0, h / 2 - t)])
    for k in range(4):
        j = (k + 1) % 4
        g.face((o[k], o[j], i[j], i[k]), m)
    return g.build("frame", place(c, rot))


_font = [None]


def reset():
    """A fresh empty scene for the next world (and nothing cached from the last one)."""
    geo.reset()
    _mats.clear()
    _font[0] = None


def text(s, m, c, size, rot=(90, 0, 0), extrude=0.0, align="CENTER", res=2, spacing=1.0):
    """Arial Bold text converted to a mesh, centred on `c`. By default it stands up facing -Y."""
    if _font[0] is None or _font[0].name not in bpy.data.fonts:
        _font[0] = bpy.data.fonts.load("C:/Windows/Fonts/arialbd.ttf", check_existing=True)
    cu = bpy.data.curves.new("text", type="FONT")
    cu.body = s
    cu.font = _font[0]
    cu.size = size
    cu.extrude = extrude
    cu.resolution_u = res
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.space_character = spacing
    tmp = bpy.data.objects.new("text-tmp", cu)
    bpy.context.scene.collection.objects.link(tmp)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    bpy.data.objects.remove(tmp)
    bpy.data.curves.remove(cu)
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=size * 1e-4)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method="BEAUTY", ngon_method="EAR_CLIP")
    bm.to_mesh(me)
    bm.free()
    me.materials.clear()
    me.materials.append(M(m))
    me.transform(place(c, rot))
    return geo.link(bpy.data.objects.new("text", me))


# ------------------------------------------------------------------------------------------ islands
class Isle:
    """Where an island is: its centre, radii, the grass height and the tip's height."""

    def __init__(self, x, y, r, ry, top, bottom, dome):
        self.x, self.y, self.r, self.ry, self.top, self.bottom, self.dome = x, y, r, ry, top, bottom, dome

    def at(self, dx=0.0, dy=0.0, dz=0.0):
        """A point on the grass, `dx`/`dy` from the centre."""
        f = min(1.0, math.hypot(dx / self.r, dy / self.ry))
        return V(self.x + dx, self.y + dy, self.top + self.dome * (1 - f) - 0.002 + dz)

    @property
    def c(self):
        return self.at()

    @property
    def tip(self):
        return V(self.x, self.y, self.bottom)


def island(x, y, r, top, depth=None, seed=1, sides=12, ry=None, grass="grass", soil="soil", rock="rock"):
    """A floating island: a grass cap with a lip, a band of soil, and a jagged rocky underside that tapers
    to a point, its outline lobed and jittered by `seed`. Returns the `Isle`."""
    rng = random.Random(seed)
    ry = r if ry is None else ry
    depth = min(r * 1.45 if depth is None else depth, top - 0.07)     # clear of the disc, even popping
    dome = 0.01 * r / 0.2
    angs = [TAU * (i + rng.uniform(-0.2, 0.2)) / sides for i in range(sides)]
    lobes, ph = rng.choice((2, 3)), rng.uniform(0, TAU)
    jr = [1 + 0.07 * math.cos(lobes * a + ph) + rng.uniform(-0.05, 0.05) for a in angs]

    def ring(s, z, jz=0.0, jj=0.0, off=(0.0, 0.0)):
        return [V(x + off[0] + math.cos(a) * r * s * k * (1 + rng.uniform(-jj, jj)),
                  y + off[1] + math.sin(a) * ry * s * k * (1 + rng.uniform(-jj, jj)), z + rng.uniform(-jz, jz))
                for a, k in zip(angs, jr)]

    g = Mesh()
    centre = g.add((x, y, top + dome))
    rim = g.ring(ring(1.0, top, jz=0.002))
    # A cliff the reader can see (a face turned down by less than the camera's 30 degrees up is in view),
    # then the taper underneath.
    lip = g.ring(ring(1.025, top - 0.01 - 0.02 * r))
    soil1 = g.ring(ring(0.98, top - 0.03 - 0.12 * r, jz=0.004))
    rock1 = g.ring(ring(0.88, top - min(0.05 + 0.22 * r, depth * 0.48), jz=0.006, jj=0.06))
    rock2 = g.ring(ring(0.6, top - depth * 0.66, jz=depth * 0.06, jj=0.16))
    off = (rng.uniform(-0.15, 0.15) * r, rng.uniform(-0.15, 0.15) * ry)
    rock3 = g.ring(ring(0.28, top - depth * 0.86, jz=depth * 0.05, jj=0.3, off=off))
    tip = g.add((x + off[0] * 1.4, y + off[1] * 1.4, top - depth))
    g.fan(rim, centre, grass, True)
    g.bridge(lip, rim, "grass_dark")
    g.bridge(soil1, lip, soil)
    g.bridge(rock1, soil1, rock)
    g.bridge(rock2, rock1, rock)
    g.bridge(rock3, rock2, rock)
    g.fan(rock3, tip, rock, down=True)
    g.build("island")
    return Isle(x, y, r, ry, top, top - depth, dome)


def tree(p, h=0.09, kind="pine", seed=0, lean=0.0):
    """A low-poly tree standing on `p`: a pine of two cones or a round crown of faceted balls."""
    rng = random.Random(seed)
    p = Vector(p)
    a = rng.uniform(0, TAU)
    R = (rng.uniform(-6, 6) + lean, rng.uniform(-6, 6), math.degrees(a))
    prism("trunk", p - V(0, 0, 0.004), h * 0.07, h * 0.4, n=4, r_top=h * 0.05, bottom=False, top=False)
    if kind == "pine":
        prism("pine", p + V(0, 0, h * 0.18), h * 0.34, h * 0.55, n=6, r_top=0, rot=R, a0=a, bottom=False)
        prism("pine", p + V(0, 0, h * 0.45), h * 0.25, h * 0.55, n=6, r_top=0, rot=R, a0=a + 0.5,
              bottom=False)
    else:
        ico("leaf", p + V(0, 0, h * 0.62), h * 0.33, (1, 1, 0.9), seed=seed)
        ico("leaf", p + V(h * 0.14, -h * 0.08, h * 0.48), h * 0.2, (1, 1, 0.9), seed=seed + 1)


def bush(p, r=0.025, seed=0, m="leaf"):
    ico(m, Vector(p) + V(0, 0, r * 0.35), r, (1.2, 1.0, 0.75), seed=seed)


def rock(p, r=0.025, seed=0, m="stone"):
    ico(m, Vector(p) + V(0, 0, r * 0.2), r, (1.2, 0.9, 0.7), seed=seed, jitter=0.25,
        rot=(0, 0, random.Random(seed).uniform(0, 360)))


def scatter(isle, n, seed=0, kinds=("pine", "round"), h=(0.08, 0.12), ring_=(0.55, 0.88), avoid=None,
            arc=None, companions=0.4):
    """`n` trees round the edge of an island, between fractions `ring_` of its radius; `avoid(x, y)`
    rejects a spot, `arc` (a0, a1 degrees) limits the angles."""
    rng = random.Random(seed)
    out, tries = [], 0
    while len(out) < n and tries < 400:
        tries += 1
        a = math.radians(rng.uniform(*arc)) if arc else rng.uniform(0, TAU)
        f = rng.uniform(*ring_)
        dx, dy = math.cos(a) * isle.r * f, math.sin(a) * isle.ry * f
        if avoid and avoid(isle.x + dx, isle.y + dy):
            continue
        if any((dx - ox) ** 2 + (dy - oy) ** 2 < (0.045) ** 2 for ox, oy in out):
            continue
        out.append((dx, dy))
        tree(isle.at(dx, dy), rng.uniform(*h), rng.choice(kinds), seed=seed * 31 + len(out))
        if rng.random() < companions:
            a2 = a + rng.choice((-1, 1)) * 0.5
            bush(isle.at(dx + math.cos(a2) * 0.035, dy + math.sin(a2) * 0.035), 0.016 + 0.006 * rng.random(),
                 seed=seed + len(out))
    return out


# --------------------------------------------------------------------------------------- holograms
def beam(isle, r=None, to=0.004, m="holo_cyan", splash=True):
    """A waterfall of light from under an island down to the disc, splashing in a ring."""
    r = isle.r * 0.18 if r is None else r
    tip = isle.tip
    prism(m, V(tip.x, tip.y, to), r * 0.7, tip.z + 0.03 - to, n=6, r_top=r, bottom=False, top=False,
          smooth_=True)
    if splash:
        flat_ring(m, V(tip.x, tip.y, to + 0.002), r * 2.2, r * 0.5, segs=16)


def drip(isle, n=2, seed=0, m="holo_cyan", length=None):
    """Light dripping from an island's underside: a few thin icicles of hologram."""
    rng = random.Random(seed)
    L = min(isle.r * 0.5 if length is None else length, isle.bottom - 0.035)
    for k in range(n):
        a = rng.uniform(0, TAU)
        f = 0.0 if k == 0 else rng.uniform(0.2, 0.4)
        x, y = isle.x + math.cos(a) * isle.r * f, isle.y + math.sin(a) * isle.ry * f
        z = isle.bottom + (isle.top - isle.bottom) * (0.05 if k == 0 else 0.4)
        prism(m, V(x, y, z + 0.01), isle.r * 0.07, -L * (1.0 if k == 0 else 0.6), n=5, r_top=0,
              bottom=False)


def arc_pts(a, b, h, n=14):
    a, b = Vector(a), Vector(b)
    return [a.lerp(b, i / (n - 1)) + V(0, 0, h * 4 * (i / (n - 1)) * (1 - i / (n - 1))) for i in range(n)]


def arc(a, b, h=0.2, m="holo_lime", r=0.0055, n=12, sides=3):
    """A glowing arch from `a` to `b`, rising `h` above the straight line between them."""
    return tube(m, arc_pts(a, b, h, n), r, sides=sides)


def spire(m, p, r, h, n=6, tip=0.25, rot=None):
    """A crystal: a prism with a pointed top."""
    p = Vector(p)
    g = Mesh()
    lo = g.ring(circle(n, r, 0.0))
    hi = g.ring(circle(n, r * 0.92, h * (1 - tip)))
    g.bridge(lo, hi, m, True)
    g.fan(hi, g.add((0, 0, h)), m, True)
    return g.build("spire", place(p, rot))


def card(c, w, h, rot=None, lines=3, m="holo_panel", ml="holo_cyan", head=None, seed=0):
    """A floating holographic card facing -Y: a dim panel, a bright edge, a header bar and text lines."""
    rng = random.Random(seed)
    R = rot3(rot)
    c = Vector(c)
    obs = [quad(m, c, w, h, R), frame(ml, c - R @ V(0, 0.001, 0), w, h, min(w, h) * 0.06, R)]
    top = h / 2 - h * 0.2
    if head:
        obs.append(quad(head, c + R @ V(0, -0.002, top), w * 0.8, h * 0.14, R))
        top -= h * 0.2
    for k in range(lines):
        z = top - k * (h * 0.6 / max(1, lines))
        lw = w * rng.uniform(0.45, 0.75)
        obs.append(quad(ml, c + R @ V(-w * 0.38 + lw / 2, -0.002, z), lw, h * 0.05, R))
    return obs


def glow_cone(m, apex, base_c, r, n=8):
    """An open cone of light from `apex` to a circle of radius `r` round `base_c` (a spotlight's beam)."""
    apex, base_c = Vector(apex), Vector(base_c)
    d = base_c - apex
    g = Mesh()
    ring_ = g.ring(circle(n, r, 0.0))
    g.fan(ring_, g.add((0, 0, -d.length)), m, True, down=True)
    return g.build("cone", Matrix.Translation(base_c) @ geo.basis(d).to_4x4())


# --------------------------------------------------------------------------------------------- bots
def bot(W, name, p, face=0.0, s=1.0, body="cream", eye=None, tip=None, parent=None, idle=None,
        arms=None, kind="solid"):
    """A tiny agent, about 0.16 tall at `s` 1: a round head with a dark visor and glowing eyes, a little
    body, an antenna. `face` turns it from facing the reader (-Y) towards +X (degrees). With `arms` a
    pair of callables (left, right), each arm is a child node (`<name>_arm_L/R`, pivoting at its shoulder)
    driven by it; otherwise the arms hang still. Returns the node name."""
    p = Vector(p)
    eye = eye or tip or "holo_cyan"           # eyes and antenna in one hologram colour: one primitive fewer
    Mt = place(p, (0, 0, face), s)
    W.node(name, p, parent=parent, idle=idle, kind=kind)
    with W.on(name):
        for ob in (
            lathe(body, (0, 0, 0), [(0.0, 0.0), (0.026, 0.0), (0.034, 0.024), (0.03, 0.054), (0.0, 0.07)], segs=8),
            ball(body, (0, 0, 0.112), 0.046, segs=10, rings=4, scale=(1.08, 1.0, 0.94)),
            prism("graphite", (0, -0.03, 0.108), 0.031, 0.02, n=8, rot=(90, 0, 0), ry=0.022, smooth_=True),
            ball(eye, (-0.0135, -0.0505, 0.112), 0.0078, segs=5, rings=2, scale=(1, 0.5, 1.3)),
            ball(eye, (0.0135, -0.0505, 0.112), 0.0078, segs=5, rings=2, scale=(1, 0.5, 1.3)),
            prism("graphite", (0, 0, 0.152), 0.003, 0.03, n=3, bottom=False, top=False),
            ball(tip or eye, (0, 0, 0.186), 0.01, segs=5, rings=2, scale=(1, 1, 1.2)),
        ):
            geo.transform(ob, Mt)
        if not arms:
            for sx in (-1, 1):
                geo.transform(tube(body, [(sx * 0.03, 0, 0.056), (sx * 0.041, -0.004, 0.034),
                                          (sx * 0.042, -0.008, 0.016)], 0.0085, sides=4), Mt)
    if arms:
        for sx, fn, side in ((1, arms[0], "L"), (-1, arms[1], "R")):
            sh = Mt @ V(sx * 0.03, 0, 0.056)
            an = W.node(f"{name}_arm_{side}", sh, parent=name, idle=fn)
            with W.on(an):
                geo.transform(tube(body, [(sx * 0.03, 0, 0.056), (sx * 0.041, -0.004, 0.034),
                                          (sx * 0.042, -0.008, 0.016)], 0.0085, sides=4), Mt)
    return name


# ------------------------------------------------------------------------------------- composition
@contextmanager
def scaled(k, about, rot=None):
    """Everything built inside, scaled by `k` (and turned by `rot`) about the point `about`: a prop group
    written at one size and fitted to its island afterwards."""
    col = geo._into[0] or bpy.context.scene.collection
    before = set(col.objects)
    yield
    about = Vector(about)
    M = Matrix.Translation(about) @ rot3(rot).to_4x4() @ Matrix.Scale(k, 4) @ Matrix.Translation(-about)
    for ob in col.objects:
        if ob not in before and ob.type == "MESH":
            ob.data.transform(M)


WORLDS: dict = {}


def world(slug, family=None, **kw):
    """Register a world's builder under its slug (the page asks for `<slug>.glb`); `kw` goes to World."""
    def deco(fn):
        WORLDS[slug] = (fn, family, kw)
        return fn
    return deco


def polar(a_deg, r, z=0.0):
    a = math.radians(a_deg)
    return V(math.cos(a) * r, math.sin(a) * r, z)


def isle_node(W, name, x, y, r, top, idle=None, **kw):
    """An island as a node of its own, pivoting at the middle of its grass."""
    W.node(name, (x, y, top), idle=idle, kind="island", size=r)
    with W.on(name):
        return island(x, y, r, top, **kw)


def sat(W, name, a_deg, d, r, top, seed, trees=2, idle=None, depth=None, sides=9, drip_m=None, clear=0.0,
        kinds=("pine", "round"), bushes=2):
    """A satellite island `d` out at angle `a_deg`, with a few trees round its edge (keeping `clear` of
    its middle) and light dripping from under it."""
    p = polar(a_deg, d)
    S = isle_node(W, name, p.x, p.y, r, top, idle=idle, depth=depth, sides=sides, seed=seed)
    with W.on(name):
        if trees:
            scatter(S, trees, seed=seed + 7, ring_=(0.55, 0.85), h=(0.07, 0.1), kinds=kinds,
                    avoid=lambda x, y: math.hypot(x - S.x, y - S.y) < clear)
        if drip_m:
            drip(S, 2, seed=seed, m=drip_m, length=r * 0.4)
        rng = random.Random(seed)
        for k in range(bushes):
            a = rng.uniform(0, TAU)
            bush(S.at(math.cos(a) * r * 0.7, math.sin(a) * S.ry * 0.7), 0.018 + 0.006 * rng.random(), seed=seed + k)
    return S


def glint(W, name, pts, period=IDLE_S, phase=0.0, m="holo_white", r=0.014, closed=False, fade=0.0,
          shape="ball", parent=None, spin_=0):
    """A packet of light running along `pts` (an open path jumps back to its start, best hidden in
    something that glows; `fade` shrinks it away at the ends instead, at the cost of a channel)."""
    pts = [Vector(p) for p in pts]
    mv = along(pts, pts[0], period, phase, closed=closed, fade=fade)
    idle = chain(mv, spin(spin_)) if spin_ else mv
    W.node(name, pts[0], idle=idle, kind="holo", parent=parent)
    with W.on(name):
        if shape == "cube":
            box(m, pts[0], (r * 1.6, r * 1.6, r * 1.6), rot=(0, 0, 45))
        else:
            ball(m, pts[0], r, segs=6, rings=3)


def disc_ring(m, r=0.93, w=0.008, dashes=36, z=0.012):
    """The sheet's dashed ring round the edge of the disc."""
    return flat_ring(m, (0, 0, z), r, w, dashes=dashes, duty=0.55)


def pedestal(p, r=0.05, h=0.014, m="graphite", glow=None):
    """A dark round pedestal (the sheet's bots and cubes stand on them), ringed with light."""
    p = Vector(p)
    prism(m, p - V(0, 0, 0.004), r, h + 0.004, n=8, r_top=r * 0.94)
    if glow:
        flat_ring(glow, p + V(0, 0, h + 0.001), r * 0.8, r * 0.12, segs=12)
    return p + V(0, 0, h)


# ------------------------------------------------------------------------------------------- motion
def xf(loc=(0, 0, 0), rot=None, scale=1.0):
    """A delta transform: move, turn (Euler degrees, Quaternion or Matrix), scale (number or triple)."""
    return place(loc, rot, scale)


def bob(amp=0.012, period=IDLE_S, phase=0.0, axis=(0, 0, 1)):
    ax = Vector(axis)
    return lambda t: Matrix.Translation(ax * amp * math.sin(TAU * (t / period + phase)))


def spin(turns=1, axis="Z", phase=0.0):
    """Whole turns per loop, so it closes."""
    return lambda t: Matrix.Rotation(TAU * (turns * t / IDLE_S + phase), 4, axis)


def swing(deg, period=IDLE_S, phase=0.0, axis="Z", bias=0.0):
    return lambda t: Matrix.Rotation(math.radians(bias + deg * math.sin(TAU * (t / period + phase))), 4, axis)


def throb(amp=0.08, period=1.0, phase=0.0, axes=(1, 1, 1), base=1.0):
    def f(t):
        k = amp * math.sin(TAU * (t / period + phase))
        return Matrix.Diagonal((base + k * axes[0], base + k * axes[1], base + k * axes[2], 1.0))
    return f


def chain(*fns):
    """Compose deltas, the first outermost."""
    def f(t):
        out = Matrix.Identity(4)
        for fn in fns:
            out = out @ fn(t)
        return out
    return f


def along(pts, pivot, period=IDLE_S, phase=0.0, closed=True, face=False, fade=0.0):
    """Travel a polyline at an even speed, once per `period`, relative to the node's `pivot`. `face`
    turns the node along its path (its -Y forward); `fade` shrinks it to nothing over that fraction at each
    end of an open path, so it can wrap round unseen."""
    pts = [Vector(p) for p in pts]
    if closed:
        pts = pts + [pts[0]]
    seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
    total = sum(seg)
    pivot = Vector(pivot)

    def at(u):
        d = (u % 1.0) * total
        for i, L in enumerate(seg):
            if d <= L or i == len(seg) - 1:
                return pts[i].lerp(pts[i + 1], d / L if L else 0), (pts[i + 1] - pts[i])
            d -= L

    def f(t):
        u = (t / period + phase) % 1.0
        p, d = at(u)
        R = Matrix.Identity(4)
        if face and d.length > 1e-9:
            R = Matrix.Rotation(math.atan2(d.y, d.x) + math.pi / 2, 4, "Z")
        s = 1.0
        if fade:
            s = max(0.001, min(1.0, smooth(0, fade, u), smooth(1, 1 - fade, u)))
        return Matrix.Translation(p - pivot) @ R @ Matrix.Scale(s, 4)
    return f


def shuttle(pts, pivot, out=(0.3, 1.5), back=(2.8, 3.8), how="inout"):
    """Out along `pts` between the times `out`, held at the far end, home again between `back`."""
    pts = [Vector(p) for p in pts]
    seg = [(pts[i + 1] - pts[i]).length for i in range(len(pts) - 1)]
    total = sum(seg)
    pivot = Vector(pivot)

    def at(u):
        d = u * total
        for i, L in enumerate(seg):
            if d <= L or i == len(seg) - 1:
                return pts[i].lerp(pts[i + 1], min(1.0, d / L) if L else 0)
            d -= L

    def f(t):
        if t <= out[0] or t >= back[1]:
            u = 0.0
        elif t < out[1]:
            u = ease(how, (t - out[0]) / (out[1] - out[0]))
        elif t <= back[0]:
            u = 1.0
        else:
            u = 1 - ease(how, (t - back[0]) / (back[1] - back[0]))
        return Matrix.Translation(at(u) - pivot)
    return f


HOP = (0.0, 0.75, 1.0, 0.75, 0.0)               # a parabola through five points: it keys in five


def hop(height, at, period=IDLE_S, dur=0.35):
    """A little jump, `dur` long, starting at `at` in each `period`."""
    def f(t):
        x = ((t - at) % period) / dur
        if x >= 1:
            return Matrix.Identity(4)
        k = min(3, int(x * 4))
        w = x * 4 - k
        return Matrix.Translation((0, 0, height * (HOP[k] + (HOP[k + 1] - HOP[k]) * w)))
    return f


def pop(delay, dur=0.38, rise=0.18):
    """Appear: up from below and out of nothing, with an overshoot, starting at `delay`."""
    def f(t):
        u = (t - delay) / dur
        if u >= 1:
            return Matrix.Identity(4)
        u = max(0.0, u)
        s = max(0.001, ease("back", u))
        return Matrix.Translation((0, 0, -rise * (1 - ease("out", u)))) @ Matrix.Scale(s, 4)
    return f


def flicker(delay):
    """Appear: a hologram stutters on: on, off, on, off, on."""
    marks = [(0.0, 1), (0.05, 0), (0.09, 1), (0.12, 0), (0.17, 1)]

    def f(t):
        if t < delay:
            return Matrix.Scale(0.001, 4)
        on = 1
        for at, v in marks:
            if t - delay >= at:
                on = v
        return Matrix.Identity(4) if on else Matrix.Scale(0.001, 4)
    return f


def blink(period=1.0, phase=0.0, duty=0.5):
    """Idle: on for `duty` of each period, off (shrunk away) for the rest."""
    def f(t):
        u = (t / period + phase) % 1.0
        return Matrix.Identity(4) if u < duty else Matrix.Scale(0.001, 4)
    return f


# -------------------------------------------------------------------------------------------- world
class Node:
    __slots__ = ("name", "pivot", "parent", "idle", "motion", "kind", "col", "ob", "rest", "cyclic", "size")

    def __init__(self, name, pivot, parent, idle, kind, col, cyclic=True, size=None):
        self.name, self.pivot, self.parent = name, Vector(pivot), parent
        self.idle, self.kind, self.col, self.cyclic, self.size = idle, kind, col, cyclic, size
        self.motion = {}                      # clip -> t -> delta Matrix, applied over idle's first frame
        self.ob, self.rest = None, None


# The clips a world carries, in baking order: (name, seconds, loops). Idle goes last, the NLA's top track,
# so frame 1 is its first frame and that is the rest pose the exporter writes.
WORLD_CLIPS = [("appear", APPEAR_S, False), ("scatter", 1.0, False), ("gather", 1.2, False),
               ("tilt", 0.8, False), ("level", 0.6, False), ("idle", IDLE_S, True)]
HOME_AT_END = ("appear", "gather", "level")   # these end on idle's first frame
FOLLOWS = (("scatter", "gather"), ("tilt", "level"))   # the second starts where the first ends


def azimuth(p):
    """Degrees round from the reader's side (-Y), counter-clockwise seen from above (towards +X first)."""
    return math.degrees(math.atan2(p.x, -p.y)) % 360


def keyed(knots):
    """A motion through `knots` [(frame, Matrix)], straight (slerped) between them and held after the last.
    Keys only at the knots: every channel on the same knots shares one time accessor in the GLB."""
    ts = [f / FPS for f, _ in knots]
    dec = [m.decompose() for _, m in knots]

    def f(t):
        if t >= ts[-1]:
            return knots[-1][1].copy()
        i = max(0, max(k for k in range(len(ts)) if ts[k] <= t)) if t > ts[0] else 0
        w = 0.0 if t <= ts[0] else (t - ts[i]) / (ts[i + 1] - ts[i])
        (l0, q0, s0), (l1, q1, s1) = dec[i], dec[i + 1]
        return Matrix.LocRotScale(l0.lerp(l1, w), q0.slerp(q1, w), s0.lerp(s1, w))
    return f


# Scatter: blown out hard and slowing (an ease-out, frame: fraction of the way). Gather: drifting back,
# then snapping home with a little overshoot.
SCATTER_KNOTS = [(0, 0.0), (4, 0.35), (10, 0.704), (18, 0.936), (30, 1.0)]
GATHER_KNOTS = [(0, 1.0), (10, 0.82), (20, 0.42), (27, 0.05), (32, -0.03), (36, 0.0)]
HOLO_OUT = [(0, 1.0), (1, 0.001), (2, 1.0), (3, 0.001), (30, 0.001)]            # stutters off
HOLO_IN = [(0, 0.001), (30, 0.001), (31, 1.0), (32, 0.001), (33, 1.0), (34, 0.001), (35, 1.0), (36, 1.0)]
# Tilt hinges the stage on the disc's rim, low on the right and a little in front (TILT_LOW), so the world
# comes up off the disc on the other side rather than sinking through it.
TILT_LOW = Vector((1.0, -0.35, 0.0)).normalized()
TILT_HINGE = TILT_LOW * 0.94
TILT_AXIS, TILT_DEG = Vector((-TILT_LOW.y, TILT_LOW.x, 0.0)), 5.0


def blown(pivot, seed, main=False):
    """An island's (scatter, gather): blown out from the middle, tumbling, and back."""
    rng = random.Random(seed * 7 + 3)
    p = Vector(pivot)
    if main or p.xy.length < 0.15:
        a = rng.uniform(0, TAU)
        d, D, tumble = V(math.cos(a), math.sin(a), 0), 0.1, rng.uniform(18, 26)
    else:
        d, D, tumble = V(p.x, p.y, 0).normalized(), rng.uniform(0.15, 0.2), rng.uniform(45, 70)
    rise, arc = rng.uniform(0.03 if main else 0.0, 0.07), 0.09
    turn = rng.uniform(30, 75) * rng.choice((-1, 1))
    axis = V(0, 0, 1).cross(d).normalized()          # tips its top outwards, its root inwards

    def P(u):
        loc = d * (D * u) + V(0, 0, rise * u + arc * 4 * u * (1 - u))
        return Matrix.Translation(loc) @ Matrix.Rotation(math.radians(tumble * u), 4, axis) @ \
            Matrix.Rotation(math.radians(turn * u), 4, "Z")

    return keyed([(f, P(u)) for f, u in SCATTER_KNOTS]), keyed([(f, P(u)) for f, u in GATHER_KNOTS])


def _tilted(u):
    return Matrix.Rotation(math.radians(TILT_DEG * u), 4, TILT_AXIS)


def tilt(t):
    """The whole stage lurches off level and stays there."""
    return _tilted(ease("settle", t / 0.7))


def level(t):
    """Back down onto the disc, and a little bump as it lands (never past level: that would sink it)."""
    x = t / 0.6
    if x < 0.6:
        u = 1 - smooth(0.0, 1.0, x / 0.6)
    elif x < 1.0:
        u = 0.12 * math.sin(math.pi * (x - 0.6) / 0.4)
    else:
        u = 0.0
    return _tilted(u)


class World:
    def __init__(self, slug, family=None, clips=None, root_name=None):
        self.slug, self.family = slug, family
        self.clips = list(clips or WORLD_CLIPS)
        self.gags = clips is None                 # a world (rather than a prop): stage, islands, gag clips
        self.root_name = root_name or "world_" + slug.replace("-", "_")
        self.col = geo.collection(self.root_name)
        self.nodes: dict[str, Node] = {}
        self.order: list[str] = []
        self.root = None
        self.islands: list[str] = []              # island_main, island_1 ... in that order
        self.renamed: dict[str, str] = {}         # an island's build name -> its name in the GLB
        self.preview_t = 0.0                      # the moment of idle the preview render shows
        self.camera = {}                          # stage() overrides for the preview
        self.strips = None                        # [(row label, [(clip, t), ...]), ...] for --strip

    @property
    def accent(self):
        return accent(self.family)

    @property
    def clip_names(self):
        return [c[0] for c in self.clips]

    # ---- declaring ----
    def node(self, name, pivot=(0, 0, 0), parent=None, idle=None, appear=None, kind="solid", cyclic=True,
             size=None, motion=None):
        """Declare node `name` pivoting at `pivot` (world space, at rest). `kind` picks its default
        entrance: "island" pops up, "holo" flickers on, "solid" rides on its parent (or pops, at the top
        level). `cyclic` False lets a loop end where it does not start, for a turn that a symmetric shape
        hides (a ring of 48 dashes turned by a 48th). `motion` maps other clips to deltas, like `appear`."""
        if name in self.nodes:
            raise ValueError(f"node {name} declared twice")
        if parent is not None and parent not in self.nodes:
            raise ValueError(f"node {name}: unknown parent {parent}")
        col = geo.collection(name, self.col)
        nd = Node(name, pivot, parent, idle, kind, col, cyclic, size)
        nd.motion.update(motion or {})
        if appear is not None:
            nd.motion["appear"] = appear
        self.nodes[name] = nd
        self.order.append(name)
        return name

    def anchor(self, name, p, parent=None):
        """An empty the page can find (a spot for a pal to stand, a stage's centre)."""
        return self.node(name, p, parent=parent, kind="anchor")

    @contextmanager
    def on(self, name):
        prev = geo._into[0]
        geo.into(self.nodes[name].col)
        try:
            yield name
        finally:
            geo._into[0] = prev

    # ---- the world's shape ----
    def _name_islands(self):
        """island_main (the biggest) and island_1 ... (round from the reader's side, counter-clockwise)."""
        isl = [n for n in self.order if self.nodes[n].kind == "island" and self.nodes[n].parent is None]
        if not isl:
            return
        main = max(isl, key=lambda n: (self.nodes[n].size or 0.0, -self.nodes[n].pivot.xy.length))
        others = sorted((n for n in isl if n != main), key=lambda n: azimuth(self.nodes[n].pivot))
        mapping = {main: "island_main", **{n: f"island_{k + 1}" for k, n in enumerate(others)}}
        clash = [v for v in mapping.values() if v in self.nodes and v not in mapping]
        if clash:
            raise ValueError(f"{self.slug}: node names {clash} are kept for islands")
        nodes = {}
        for name in self.order:
            nd = self.nodes[name]
            nd.name = mapping.get(name, name)
            nd.parent = mapping.get(nd.parent, nd.parent)
            nodes[nd.name] = nd
        self.nodes = nodes
        self.order = [mapping.get(n, n) for n in self.order]
        self.renamed = mapping
        self.islands = ["island_main"] + [f"island_{k + 1}" for k in range(len(others))]

    def _entrances(self):
        """Default `appear`s: top-level solids pop up in order of their distance from the centre, holograms
        flicker on once they are up."""
        tops = [n for n in self.order if self.nodes[n].parent is None]
        solid = sorted([n for n in tops if self.nodes[n].kind not in ("holo", "anchor")],
                       key=lambda n: self.nodes[n].pivot.xy.length)
        for k, n in enumerate(solid):
            self.nodes[n].motion.setdefault("appear", pop(0.36 * k / max(1, len(solid) - 1)))
        for name in self.order:
            nd = self.nodes[name]
            if nd.kind == "holo":
                nd.motion.setdefault("appear", flicker(0.48 + 0.08 * ((sum(map(ord, name)) % 7) / 6)))

    def _group(self):
        """root > `stage` (tilt and level turn it, about a hinge on the disc's rim) > the islands, and
        `holograms` (scatter and gather blink it out and in) > the top-level holograms: arcs, rings, glints,
        floating cards."""
        tops = [n for n in self.order if self.nodes[n].parent is None]
        self.node("stage", TILT_HINGE, kind="group", motion={"tilt": tilt, "level": level})
        self.node("holograms", (0, 0, 0), parent="stage", kind="group",
                  motion={"scatter": keyed([(f, Matrix.Scale(s, 4)) for f, s in HOLO_OUT]),
                          "gather": keyed([(f, Matrix.Scale(s, 4)) for f, s in HOLO_IN])})
        self.order = self.order[-2:] + self.order[:-2]
        for n in tops:
            nd = self.nodes[n]
            nd.parent = "holograms" if nd.kind == "holo" else "stage"
            if nd.kind not in ("island", "holo", "anchor"):
                print(f"  NOTE {self.slug}/{n}: a top-level {nd.kind} node, which scatter leaves where it is")
        for k, n in enumerate(self.islands):
            sc, ga = blown(self.nodes[n].pivot, k + 11 * len(self.slug), main=(k == 0))
            self.nodes[n].motion.update(scatter=sc, gather=ga)

    # ---- joining ----
    def finalize(self):
        view = bpy.context.view_layer
        if self.gags:
            self._name_islands()
        if "appear" in self.clip_names:
            self._entrances()
        if self.gags:
            self._group()
        self.root = bpy.data.objects.new(self.root_name, None)
        self.root.empty_display_size = 0.2
        self.col.objects.link(self.root)
        for name in self.order:
            nd = self.nodes[name]
            obs = [o for o in nd.col.objects if o.type == "MESH"]
            if obs:
                for o in list(bpy.context.selected_objects):
                    o.select_set(False)
                for o in obs:
                    o.select_set(True)
                view.objects.active = obs[0]
                if len(obs) > 1:
                    bpy.ops.object.join()
                ob = view.objects.active
                ob.name = ob.data.name = name
                ob.data.transform(Matrix.Translation(-nd.pivot))
                self._weld(ob)
                _colour_and_shade(ob)
            else:
                ob = bpy.data.objects.new(name, None)
                ob.empty_display_size = 0.05
                nd.col.objects.link(ob)
            if ob.name != name:
                raise ValueError(f"node name {name} taken by another datablock ({ob.name})")
            for c in list(ob.users_collection):
                c.objects.unlink(ob)
            self.col.objects.link(ob)
            ob.rotation_mode = "QUATERNION"
            par = self.nodes[nd.parent] if nd.parent else None
            ob.parent = par.ob if par else self.root
            ob.matrix_parent_inverse = Matrix.Identity(4)
            nd.rest = Matrix.Translation(nd.pivot - (par.pivot if par else Vector()))
            nd.ob = ob
            self.col.children.unlink(nd.col)
            bpy.data.collections.remove(nd.col)
        for name in self.order:
            nd = self.nodes[name]
            nd.ob.matrix_basis = self.local(nd, "idle", 0.0)
        view.update()
        return self

    @staticmethod
    def _weld(ob):
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-6)
        bm.to_mesh(ob.data)
        bm.free()

    # ---- motion ----
    def local(self, nd, clip, t):
        if clip == "idle":
            return nd.rest @ (nd.idle(t) if nd.idle else Matrix.Identity(4))
        idle0 = nd.idle(0.0) if nd.idle else Matrix.Identity(4)
        fn = nd.motion.get(clip)
        return nd.rest @ (fn(t) if fn else Matrix.Identity(4)) @ idle0

    def bake(self):
        """Write every clip as NLA tracks named for it, idle last (on top, so frame 1 is the rest pose)."""
        clips = [c for c in self.clips if c[0] != "idle"] + [c for c in self.clips if c[0] == "idle"]
        frames_of = {name: int(round(secs * FPS)) + 1 for name, secs, _ in clips}   # with the closing frame
        moved = set()
        for clip, secs, loops in clips:
            n = frames_of[clip]
            every = [1 + i for i in range(n)]
            for name in self.order:
                nd = self.nodes[name]
                frames = every
                mats = [self.local(nd, clip, i / FPS) for i in range(n)]
                if all(_close(m, mats[0]) for m in mats):
                    if clip == "idle" and name in moved:
                        # Held, but keyed: the NLA's top track then decides frame 1 for every node, so
                        # the rest pose the exporter writes is idle's first frame, not another clip's.
                        frames, mats = [1, n], [mats[0], mats[0]]
                    else:
                        continue
                moved.add(name)
                if loops and nd.cyclic and not _close(mats[0], mats[-1], 1e-4):
                    raise ValueError(f"{self.slug}: {name}'s {clip} does not loop")
                if clip in HOME_AT_END and not _close(mats[-1], self.local(nd, "idle", 0.0), 1e-5):
                    raise ValueError(f"{self.slug}: {name}'s {clip} does not end on idle's first frame")
                for a, b in FOLLOWS:
                    if clip == b and a in frames_of:
                        end = self.local(nd, a, (frames_of[a] - 1) / FPS)
                        if not _close(mats[0], end, 1e-5):
                            raise ValueError(f"{self.slug}: {name}'s {b} does not start where {a} ends")
                act = bpy.data.actions.new(f"{clip}@{name}")
                slot = act.slots.new(id_type="OBJECT", name=name)
                bag = _fcurves_for(act, slot)
                dec = [m.decompose() for m in mats]
                quats = [d[1] for d in dec]
                for i in range(1, len(quats)):
                    if quats[i].dot(quats[i - 1]) < 0:
                        quats[i] = -quats[i]
                for i in range(3):
                    _write(bag, "location", i, frames, [d[0][i] for d in dec])
                    _write(bag, "scale", i, frames, [d[2][i] for d in dec])
                for i in range(4):
                    _write(bag, "rotation_quaternion", i, frames, [q[i] for q in quats])
                _push(nd.ob, act, slot, clip, 1)
        bpy.context.scene.frame_set(1)

    def pose(self, clip, t):
        """Hold every node at time `t` of `clip`, for a still (the NLA tracks are muted: export first)."""
        for name in self.order:
            nd = self.nodes[name]
            if nd.ob.animation_data:
                for tr in nd.ob.animation_data.nla_tracks:
                    tr.mute = True
            nd.ob.matrix_basis = self.local(nd, clip, t)
        bpy.context.view_layer.update()

    def check(self):
        """The world's reach over every baked frame: (max radius, min z, max z) of all the clips but the
        scatter (whose islands are blown past the disc's edge on purpose; its reach is `scattered`), and its
        triangles."""
        import numpy as np
        meshes = [self.nodes[n].ob for n in self.order if self.nodes[n].ob.type == "MESH"]
        co = {}
        for ob in meshes:
            a = np.empty(len(ob.data.vertices) * 3, np.float32)
            ob.data.vertices.foreach_get("co", a)
            co[ob.name] = np.c_[a.reshape(-1, 3), np.ones(len(ob.data.vertices))]
        reach = {}
        worst = {}
        for clip, secs, _ in self.clips:
            n = int(round(secs * FPS)) + 1
            group = "scattered" if clip in ("scatter", "gather") else "kept"
            r0, z0_, z1_ = reach.get(group, (0.0, 9.0, -9.0))
            for i in range(0, n, 3 if clip == "idle" else 2):
                t = i / FPS
                W = {}
                for name in self.order:
                    nd = self.nodes[name]
                    P = W[nd.parent] if nd.parent else Matrix.Identity(4)
                    W[name] = P @ self.local(nd, clip, t)
                for ob in meshes:
                    p = co[ob.name] @ np.array(W[ob.name]).T
                    xy = np.sqrt(p[:, 0] ** 2 + p[:, 1] ** 2)
                    r_, z0, z1 = float(xy.max()), float(p[:, 2].min()), float(p[:, 2].max())
                    r0, z0_, z1_ = max(r0, r_), min(z0_, z0), max(z1_, z1)
                    if group == "kept" and (r_ > RADIUS or z0 < -0.001 or z1 > HEIGHT):
                        worst.setdefault(ob.name, f"{clip}@{t:.2f}s r={r_:.3f} z=[{z0:.3f}, {z1:.3f}]")
            reach[group] = (r0, z0_, z1_)
        tris = sum(len(p.vertices) - 2 for ob in meshes for p in ob.data.polygons)
        for k, v in worst.items():
            print(f"  OUT {self.slug}/{k}: {v}")
        r, z0, z1 = reach["kept"]
        out = dict(radius=round(r, 3), zmin=round(z0, 3), zmax=round(z1, 3), tris=tris, nodes=len(self.order),
                   mats=sorted({s.material.name for ob in meshes for s in ob.material_slots if s.material}))
        if "scattered" in reach:
            r, z0, z1 = reach["scattered"]
            out["scattered"] = (round(r, 3), round(z0, 3), round(z1, 3))
        return out

    def objects(self):
        return [self.root] + [self.nodes[n].ob for n in self.order]


def _close(a, b, eps=1e-7):
    return all(abs(a[i][j] - b[i][j]) <= eps for i in range(4) for j in range(4))


# ------------------------------------------------------------------------------------------- export
def export(W, path, raw_dir):
    """The world's GLB, slimmed (resampled, pruned, meshopt-compressed); Blender's own export is kept in
    `raw_dir` (outside the repository)."""
    from kit import export as ex
    path, raw = Path(path), Path(raw_dir) / (Path(path).stem + ".raw.glb")
    path.parent.mkdir(parents=True, exist_ok=True)
    ex.glb(raw, W.objects())
    _unlit_holos(raw)
    ex.compress(raw, path)
    _tidy(path)
    return path


def _read_glb(path):
    data = Path(path).read_bytes()
    n = struct.unpack_from("<I", data, 12)[0]
    return json.loads(data[20:20 + n]), data[20 + n:]


def _write_glb(path, js, rest):
    body = json.dumps(js, separators=(",", ":")).encode()
    body += b" " * (-len(body) % 4)
    Path(path).write_bytes(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(body) + len(rest)) +
                           struct.pack("<II", len(body), 0x4E4F534A) + body + rest)


def _tidy(path):
    """Shrink the JSON chunk without changing what it says: every float to 7 significant digits (the
    values are float32, from a world one unit across), the clear-coat extension Blender writes with a
    factor of 0 dropped, and fields that only restate glTF's defaults left out."""
    js, rest = _read_glb(path)

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
    for an in js.get("animations", []):
        for sm in an["samplers"]:
            if sm.get("interpolation") == "LINEAR":     # glTF's default
                del sm["interpolation"]
    _write_glb(path, walk(js), rest)


def _unlit_holos(path):
    """Drop the normals of hologram primitives: the page draws them unlit (additive), and a plain glTF
    viewer, finding none, shades them flat. The orphaned accessors go in compress()'s prune."""
    js, rest = _read_glb(path)
    mats = js.get("materials", [])
    for me in js.get("meshes", []):
        for pr in me["primitives"]:
            if mats[pr.get("material", 0)].get("name", "").startswith("holo"):
                pr["attributes"].pop("NORMAL", None)
    _write_glb(path, js, rest)


def inspect(path):
    """What a GLB carries: its nodes, materials, animations (name, seconds) and triangle count."""
    data = Path(path).read_bytes()
    n = struct.unpack_from("<I", data, 12)[0]
    js = json.loads(data[20:20 + n])
    acc = js.get("accessors", [])
    tris = 0
    for me in js.get("meshes", []):
        for pr in me["primitives"]:
            if "indices" in pr:
                tris += acc[pr["indices"]]["count"] // 3
    anims = []
    for a in js.get("animations", []):
        t = max(acc[s["input"]]["max"][0] for s in a["samplers"])
        anims.append((a["name"], round(t, 3), len(a["channels"])))
    return dict(bytes=len(data), nodes=[nd.get("name") for nd in js.get("nodes", [])],
                materials=[m.get("name") for m in js.get("materials", [])], animations=anims, tris=tris)


# ------------------------------------------------------------------------------------------- render
def _preview_holos():
    """For the preview only (after export): holograms as the page draws them, additive light."""
    for m in bpy.data.materials:
        if not m.name.startswith("holo"):
            continue
        b = m.node_tree.nodes["Principled BSDF"]
        col = b.inputs["Emission Color"].default_value[:]
        k = b.inputs["Emission Strength"].default_value
        nt = m.node_tree
        for nd in list(nt.nodes):
            if nd.type != "OUTPUT_MATERIAL":
                nt.nodes.remove(nd)
        out = next(nd for nd in nt.nodes if nd.type == "OUTPUT_MATERIAL")
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = col
        em.inputs["Strength"].default_value = k * 0.4
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        add = nt.nodes.new("ShaderNodeAddShader")
        nt.links.new(tr.outputs[0], add.inputs[0])
        nt.links.new(em.outputs[0], add.inputs[1])
        nt.links.new(add.outputs[0], out.inputs["Surface"])


def _stage():
    """The Core's disc as a stand-in for the preview (not exported): dark glass with a glowing rim."""
    geo.into(None)
    dark = mat.principled("preview-disc", "#0b1115", rough=0.55, coat=0.3, coat_rough=0.3, spec=0.3)
    rim = mat.principled("preview-rim", "#000000", emit=CYAN, strength=6.0)
    faint = mat.principled("preview-faint", "#000000", emit="#1d6f7a", strength=2.0)
    geo.disc("preview-disc", 1.06, 0.04, dark, (0, 0, -0.022), (0, 0, 1), segs=64)
    geo.ring("preview-rim", 1.065, 0.008, rim, (0, 0, 0.0), (0, 0, 1), segs=96, sides=6)
    for r in (0.45, 0.75):
        geo.ring("preview-faint", r, 0.0018, faint, (0, 0, 0.0), (0, 0, 1), segs=96, sides=4)


def _glow():
    sc = bpy.context.scene
    tree = bpy.data.node_groups.new("glow", "CompositorNodeTree")
    tree.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = tree.nodes.new("CompositorNodeRLayers")
    gl = tree.nodes.new("CompositorNodeGlare")
    gl.inputs["Type"].default_value = "Bloom"
    gl.inputs["Threshold"].default_value = 0.9
    gl.inputs["Strength"].default_value = 0.55
    gl.inputs["Size"].default_value = 0.6
    out = tree.nodes.new("NodeGroupOutput")
    tree.links.new(rl.outputs["Image"], gl.inputs["Image"])
    tree.links.new(gl.outputs["Image"], out.inputs[0])
    sc.compositing_node_group = tree
    sc.render.use_compositing = True


def stage(samples=40, res=800, az=20.0, el=30.0, dist=3.3, focus=(0, 0, 0.42)):
    """The preview studio: a three-quarter view from in front and above, on a stand-in disc, lit like the
    sheet, holograms drawn as the page draws them."""
    _preview_holos()
    _stage()
    geo.into(None)
    f = Vector(focus)
    studio.area("key", 380, f + V(-2.2, -2.6, 3.2), f, 4.0, (1.0, 0.92, 0.82))
    studio.area("fill", 90, f + V(2.8, -1.8, 1.2), f, 3.0, (0.78, 0.86, 1.0))
    studio.area("rim", 220, f + V(0.8, 3.2, 2.4), f, 2.0, (0.75, 0.95, 1.0))
    studio.world((0.028, 0.031, 0.037), 1.0)
    a, e = math.radians(az), math.radians(el)
    cam = bpy.data.cameras.new("preview")
    cam.lens = 50
    ob = bpy.data.objects.new("preview", cam)
    geo.link(ob)
    ob.location = f + V(math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)) * dist
    studio.aim(ob, f)
    bpy.context.scene.camera = ob
    studio.settings(res=(res, res), samples=samples, engine="CYCLES", view="AgX")
    bpy.context.scene.view_settings.look = "AgX - Punchy"
    _glow()


def render(path, W=None, clip="idle", t=0.0, res=None, samples=None):
    """A still of the world at `t` seconds into `clip`."""
    sc = bpy.context.scene
    if res:
        sc.render.resolution_x = sc.render.resolution_y = res
    if samples:
        sc.cycles.samples = samples
    if W is not None:
        W.pose(clip, t)
    return studio.render(path)


def contact_sheet(paths, out, cols=5, tile=320, labels=None):
    """All the renders on one sheet, labelled (PIL, from the system Python; Blender has none)."""
    import subprocess
    script = (
        "import sys,json\nfrom PIL import Image,ImageDraw,ImageFont\n"
        "a=json.loads(sys.argv[1]);ps=a['paths'];ls=a['labels'];c=a['cols'];t=a['tile']\n"
        "rows=(len(ps)+c-1)//c;S=Image.new('RGB',(c*t,rows*(t+26)),(20,22,26));d=ImageDraw.Draw(S)\n"
        "try:\n f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',15)\n"
        "except Exception:\n f=ImageFont.load_default()\n"
        "for i,(p,l) in enumerate(zip(ps,ls)):\n"
        " im=Image.open(p).convert('RGB').resize((t,t),Image.LANCZOS);x,y=(i%c)*t,(i//c)*(t+26)\n"
        " S.paste(im,(x,y));d.text((x+8,y+t+4),l,fill=(190,230,235),font=f)\n"
        "S.save(a['out'])\n")
    arg = json.dumps(dict(paths=[str(p) for p in paths], labels=labels or [Path(p).stem for p in paths],
                          cols=cols, tile=tile, out=str(out)))
    for py in ("python", "py"):
        try:
            r = subprocess.run([py, "-c", script, arg], capture_output=True, text=True)
        except FileNotFoundError:
            continue
        if r.returncode == 0:
            return out
        print("contact sheet:", r.stderr.strip()[-400:])
    return None
