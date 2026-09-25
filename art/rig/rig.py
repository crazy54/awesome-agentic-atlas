"""Archie's stage rig: the fixtures his light show hangs, built from nothing but this script.

Run it headless and it writes two files:

    blender --background --factory-startup --python art/rig/rig.py

  * `art/rig/rig.blend`       -- the scene, for anyone who wants to open it and push vertices around.
  * `docs/assets/rig/rig.glb` -- every fixture, one root node each, for `archie-fx.js` to clone and place.

WHAT IS IN IT. One of each kind of thing the rig is made of; the page clones them, so a stage with sixteen
moving heads costs the bytes of one. Every root is a separate node with its origin at its HANG POINT (where
a clamp would meet the truss, or where it stands on the floor), in metres, glTF Y-up:

  head          a moving-head beam. `head` is the base (the clamp is at its top face), `head_yoke` its child,
                pivoting on the pan axis (local Y), `head_tilt` the yoke's child, pivoting on the tilt axis
                (local X), and `head_lens` the tilt's child: the lens, facing -Y (down) at rest. 0.25 m tall.
  blinder       a 2-lite molefay blinder: two lamp cups in one housing on a hanging bracket, both lenses in
                one mesh `blinder_lens`, facing +Z (at the audience).
  par           an LED wash par on a hanging bracket, lens `par_lens` facing -Y.
  laser         a floor laser projector standing on its feet, aperture `laser_lens` facing +Z.
  truss         one metre of 0.3 m box truss along X, origin at its centre, for the page to scale in X (the
                lacing is spaced so that a stretched segment still reads as truss).
  truss_corner  a 0.3 m corner block, to join two runs of truss at right angles.
  pod           a drop-down pod: a 0.4 m triangle of truss, origin at its top, with `pod_cable` running 1 m
                up (+Y) from it; the page lowers the pod and stretches the cable in Y to meet the rig.

Every `*_lens` mesh has its origin at the lens's centre, so its world position is where the beam starts.

MATERIALS are four, shared by every fixture, and named for the page to find: `body` (Archie's charcoal),
`trim` (his gold), `metal` (the truss and the brackets) and `lens`, white and emissive, which the page
overrides per fixture with the colour of the look. No textures: flat colour is the style, and it keeps the
file to a few tens of kilobytes. No Draco and no meshopt either, because `three-archie.js` is built with
GLTFLoader and nothing to decode them.

NO NORMALS, on purpose. With them the file was 101 KB, because every hard edge splits its vertices; without
them it is 42 KB (12 KB gzipped) and GLTFLoader, finding no normal attribute, gives each mesh a flat-shaded
copy of its material (`flatShading = true`, same name). Faceted is the low-poly look these are meant to have.
A page that swaps in its own lens material must set `flatShading: true` on it too, or the mesh lights black.

Procedural rather than modelled by hand, for the same reason as `art/archie/archie.py`: a change to a
fixture is a reviewable change to a number here, not a binary nobody can read.
"""
from __future__ import annotations

import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BLEND = HERE / "rig.blend"
GLB = ROOT / "docs" / "assets" / "rig" / "rig.glb"

# Blender is Z-up and the file is Y-up: the exporter turns Blender's +Z into glTF's +Y and Blender's -Y into
# glTF's +Z. So "down" (-Y in glTF) is -Z here, and "at the audience" (+Z in glTF) is -Y here.
DOWN, FRONT = Vector((0, 0, -1)), Vector((0, -1, 0))

BODY, TRIM, METAL, LENS = range(4)
PALETTE = {
    "body": dict(color=(0.043, 0.043, 0.055), metallic=0.25, roughness=0.55),   # #3a3a41-ish charcoal
    "trim": dict(color=(0.66, 0.42, 0.07), metallic=0.85, roughness=0.35),      # Archie's gold
    "metal": dict(color=(0.42, 0.44, 0.48), metallic=0.9, roughness=0.4),
    "lens": dict(color=(1.0, 1.0, 1.0), metallic=0.0, roughness=0.2, emit=1.0),
}


def materials() -> list:
    out = []
    for name, p in PALETTE.items():
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*p["color"], 1)
        b.inputs["Metallic"].default_value = p["metallic"]
        b.inputs["Roughness"].default_value = p["roughness"]
        if p.get("emit"):
            b.inputs["Emission Color"].default_value = (1, 1, 1, 1)
            b.inputs["Emission Strength"].default_value = p["emit"]
        out.append(m)
    return out


# ---- mesh building ---------------------------------------------------------------------------------------
# A part is a primitive dropped into the object's bmesh with one material. `M` places it: a translation, then
# an optional rotation taking the primitive's own Z axis onto `axis`, then a scale.
def _place(loc, axis=None, scale=(1, 1, 1)) -> Matrix:
    R = Matrix.Identity(4)
    if axis is not None:
        R = Vector((0, 0, 1)).rotation_difference(Vector(axis).normalized()).to_matrix().to_4x4()
    return Matrix.Translation(Vector(loc)) @ R @ Matrix.Diagonal((*scale, 1))


class Part:
    def __init__(self):
        self.bm = bmesh.new()

    def _tag(self, before, mat):
        for f in set(self.bm.faces) - before:
            f.material_index = mat

    def box(self, loc, size, mat=BODY, axis=None):
        before = set(self.bm.faces)
        bmesh.ops.create_cube(self.bm, size=1, matrix=_place(loc, axis, size))
        self._tag(before, mat)

    def cyl(self, loc, axis, r, depth, mat=BODY, seg=12, r2=None, caps=True):
        before = set(self.bm.faces)
        bmesh.ops.create_cone(self.bm, cap_ends=caps, cap_tris=False, segments=seg, radius1=r,
                              radius2=r if r2 is None else r2, depth=depth, matrix=_place(loc, axis))
        self._tag(before, mat)

    def disc(self, loc, axis, r, mat=LENS, seg=16):
        """A flat lens: a one-sided circle facing `axis`."""
        before = set(self.bm.faces)
        res = bmesh.ops.create_circle(self.bm, cap_ends=True, segments=seg, radius=r, matrix=_place(loc, axis))
        self._tag(before, mat)
        return res

    def rod(self, a, b, r, mat=METAL, seg=6):
        """A tube from a to b, open-ended: its ends are buried in whatever it joins, and caps on the truss's
        sixty-odd rods were a third of the file."""
        a, b = Vector(a), Vector(b)
        self.cyl((a + b) / 2, b - a, r, (b - a).length, mat, seg, caps=False)

    def to_object(self, name, mats, parent=None, origin=(0, 0, 0), smooth=True):
        me = bpy.data.meshes.new(name)
        bmesh.ops.remove_doubles(self.bm, verts=self.bm.verts, dist=1e-5)
        self.bm.to_mesh(me)
        self.bm.free()
        for m in mats:
            me.materials.append(m)
        if smooth:
            for p in me.polygons:
                p.use_smooth = True
            try:                                    # Blender 4.1+: flat faces stay flat, rounds go round
                me.set_sharp_from_angle(angle=math.radians(35))
            except AttributeError:
                pass
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        if parent is not None:
            ob.parent = parent
        ob.location = origin
        return ob


def empty_part():
    return Part()


# Geometry is written in each object's own space: a child's parts are relative to its origin (its pivot).
def moving_head(M, x):
    base = Part()
    base.box((0, 0, -0.012), (0.12, 0.05, 0.024), METAL)           # the clamp plate
    base.box((0, 0, -0.06), (0.19, 0.17, 0.07), BODY)              # the base
    base.box((0, -0.086, -0.06), (0.12, 0.004, 0.03), TRIM)        # a gold display strip on the front
    root = base.to_object("head", M)
    root.location = (x, 0, 0)

    yoke = Part()                                                  # pivot: pan axis, 0.095 m below the clamp
    yoke.cyl((0, 0, -0.005), (0, 0, 1), 0.05, 0.02, METAL, 16)     # the turntable
    yoke.box((0, 0, -0.025), (0.21, 0.07, 0.03), BODY)
    for s in (-1, 1):
        yoke.box((s * 0.093, 0, -0.08), (0.028, 0.07, 0.1), BODY)
        yoke.cyl((s * 0.108, 0, -0.1), (1, 0, 0), 0.022, 0.006, TRIM, 16)   # gold tilt hubs
    y = yoke.to_object("head_yoke", M, root, (0, 0, -0.095))

    head = Part()                                                  # pivot: tilt axis, 0.1 m below the pan
    head.cyl((0, 0, 0.0), (0, 0, 1), 0.072, 0.1, BODY, 20)         # the drum
    head.cyl((0, 0, -0.06), (0, 0, 1), 0.066, 0.02, TRIM, 20, 0.07)  # gold bezel, flaring to the lens
    for k in range(4):                                             # cooling fins round the back
        a = k * math.pi / 2 + math.pi / 4
        head.box((math.cos(a) * 0.06, math.sin(a) * 0.06, 0.05), (0.03, 0.03, 0.012), METAL)
    t = head.to_object("head_tilt", M, y, (0, 0, -0.1))

    lens = Part()
    lens.disc((0, 0, 0), DOWN, 0.055, LENS, 20)
    lens.disc((0, 0, 0.0005), DOWN, 0.064, BODY, 20)               # a dark ring behind the glass
    lens.to_object("head_lens", M, t, (0, 0, -0.0705))
    return root


def blinder(M, x):
    body = Part()
    body.box((0, 0, -0.012), (0.1, 0.05, 0.024), METAL)            # clamp
    for s in (-1, 1):                                              # the hanging bracket: a U round the housing
        body.box((s * 0.2, 0, -0.1), (0.02, 0.04, 0.17), METAL)
    body.box((0, 0, -0.022), (0.42, 0.04, 0.02), METAL)
    body.box((0, 0.01, -0.13), (0.37, 0.1, 0.19), BODY)            # the housing
    body.box((0, -0.041, -0.13), (0.38, 0.004, 0.2), TRIM)         # gold face plate
    for s in (-1, 1):                                              # the two cups, deep, round, reflector-bright
        body.cyl((s * 0.09, -0.06, -0.13), FRONT, 0.078, 0.04, BODY, 20)
        body.cyl((s * 0.09, -0.06, -0.13), FRONT, 0.07, 0.042, METAL, 20)
    root = body.to_object("blinder", M)
    root.location = (x, 0, 0)
    lens = Part()                                                  # both lamps, one mesh, origin between them
    for s in (-1, 1):
        lens.disc((s * 0.09, 0, 0), FRONT, 0.062, LENS, 20)
    lens.to_object("blinder_lens", M, root, (0, -0.0815, -0.13))
    return root


def par(M, x):
    body = Part()
    body.box((0, 0, -0.012), (0.1, 0.05, 0.024), METAL)
    body.box((0, 0, -0.03), (0.24, 0.04, 0.016), METAL)            # bracket across the top
    for s in (-1, 1):
        body.box((s * 0.112, 0, -0.1), (0.016, 0.04, 0.14), METAL)
        body.cyl((s * 0.104, 0, -0.13), (1, 0, 0), 0.02, 0.006, TRIM, 12)
    body.cyl((0, 0, -0.13), (0, 0, 1), 0.095, 0.16, BODY, 20)       # the can, standing lens-down
    body.cyl((0, 0, -0.215), (0, 0, 1), 0.098, 0.012, TRIM, 20)     # gold rim
    root = body.to_object("par", M)
    root.location = (x, 0, 0)
    lens = Part()
    lens.disc((0, 0, 0), DOWN, 0.084, LENS, 20)
    # The LED cells as a raised dot pattern would be sixty draw calls' worth of detail nobody sees at this
    # size; one disc tinted by the page reads as the glow a wash is.
    lens.to_object("par_lens", M, root, (0, 0, -0.2215))
    return root


def laser(M, x):
    body = Part()
    for sx in (-1, 1):
        for sy in (-1, 1):
            body.cyl((sx * 0.085, sy * 0.075, 0.006), (0, 0, 1), 0.012, 0.012, METAL, 8)   # feet
    body.box((0, 0, 0.062), (0.22, 0.19, 0.1), BODY)
    for k in range(5):                                             # heat-sink fins on top
        body.box((-0.08 + k * 0.04, 0.01, 0.118), (0.012, 0.15, 0.012), METAL)
    body.box((0, -0.0965, 0.062), (0.2, 0.004, 0.08), TRIM)        # gold front plate
    body.box((0, -0.1, 0.062), (0.06, 0.006, 0.05), BODY)          # the aperture's dark surround
    root = body.to_object("laser", M)
    root.location = (x, 0, 0)
    lens = Part()
    before = set(lens.bm.faces)
    bmesh.ops.create_grid(lens.bm, x_segments=1, y_segments=1, size=0.018, matrix=_place((0, 0, 0), FRONT))
    lens._tag(before, LENS)
    lens.to_object("laser_lens", M, root, (0, -0.1035, 0.062), smooth=False)
    return root


def truss(M, x):
    """One metre along X. Four chords at the corners of a 0.3 m square, lacing zig-zagging on each face."""
    p = Part()
    h = 0.135
    corners = [(-h, -h), (h, -h), (h, h), (-h, h)]
    for (cy, cz) in corners:
        p.rod((-0.5, cy, cz), (0.5, cy, cz), 0.019, METAL, 6)
    n = 4                                                          # four bays a metre
    for i in range(4):
        (ay, az), (by, bz) = corners[i], corners[(i + 1) % 4]
        for k in range(n):
            x0, x1 = -0.5 + k / n, -0.5 + (k + 1) / n
            a, b = ((ay, az), (by, bz)) if k % 2 == 0 else ((by, bz), (ay, az))
            p.rod((x0, *a), (x1, *b), 0.008, METAL, 4)
    for xe in (-0.5, 0.5):                                         # end plates, for the joints to butt against
        for i in range(4):
            (ay, az), (by, bz) = corners[i], corners[(i + 1) % 4]
            p.rod((xe, ay, az), (xe, by, bz), 0.01, METAL, 4)
    ob = p.to_object("truss", M)
    ob.location = (x, 0, 0)
    return ob


def truss_corner(M, x):
    p = Part()
    p.box((0, 0, 0), (0.3, 0.3, 0.3), METAL)
    p.box((0, 0, 0), (0.24, 0.31, 0.24), BODY)                     # dark panels inset on each face
    p.box((0, 0, 0), (0.31, 0.24, 0.24), BODY)
    p.box((0, 0, 0), (0.24, 0.24, 0.31), BODY)
    ob = p.to_object("truss_corner", M, smooth=False)
    ob.location = (x, 0, 0)
    return ob


def pod(M, x):
    """A triangle of truss, 0.4 m a side, hanging level from a cable at its centre."""
    p = Part()
    r = 0.4 / math.sqrt(3)                                         # circumradius of the triangle
    pts = [(math.cos(a) * r, math.sin(a) * r) for a in (math.pi / 2, math.pi / 2 + 2.0944, math.pi / 2 + 4.1888)]
    for dz in (-0.02, -0.14):                                      # two rings of chord, 0.12 apart
        for i in range(3):
            (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 3]
            p.rod((ax, ay, dz), (bx, by, dz), 0.012, METAL, 6)
    for i in range(3):                                             # uprights and diagonals between them
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % 3]
        p.rod((ax, ay, -0.02), (ax, ay, -0.14), 0.008, METAL, 5)
        p.rod((ax, ay, -0.02), (bx, by, -0.14), 0.006, METAL, 5)
    for (ax, ay) in pts:                                           # three bridle wires to the cable's shackle
        p.rod((ax, ay, -0.02), (0, 0, 0.1), 0.003, METAL, 4)
    p.cyl((0, 0, 0.1), (1, 0, 0), 0.016, 0.01, TRIM, 10)           # the shackle, in gold
    p.cyl((0, 0, -0.08), (0, 0, 1), 0.03, 0.12, BODY, 12)          # the motor at the centre
    root = p.to_object("pod", M)
    root.location = (x, 0, 0)
    c = Part()
    c.rod((0, 0, 0), (0, 0, 1), 0.005, METAL, 6)                   # 1 m up from the shackle: scale it in Y
    c.to_object("pod_cable", M, root, (0, 0, 0.1), smooth=False)
    return root


def main() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    M = materials()
    # All at the world origin, overlapping in the .blend: a root's translation in the file is where a clone
    # starts, and a page that forgets to reset it would hang every blinder 1.2 m to the right. Hide the others
    # in the outliner to work on one.
    for make in (moving_head, blinder, par, laser, truss, truss_corner, pod):
        make(M, 0.0)
    GLB.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.preferences.filepaths.save_version = 0            # no rig.blend1 beside it on a re-run
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND), compress=True)
    bpy.ops.export_scene.gltf(
        filepath=str(GLB), export_format="GLB", export_apply=True, export_yup=True,
        export_animations=False, export_cameras=False, export_lights=False, export_extras=False,
        export_texcoords=False, export_normals=False, export_materials="EXPORT")
    print(f"wrote {GLB}  {GLB.stat().st_size:,} bytes")


main()
