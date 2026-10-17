"""The Atlas Core, Archie's favourite possession: a ceramic football of a ball that docks in his belly and
unfolds like a flower into a stage for a miniature holographic world. Built, rigged, animated and exported
from nothing but this script.

    blender -b --factory-startup --python art/pals/core.py -- [--views closed,closed-b,open,open-top,strip]
            [--out DIR] [--samples N] [--res WxH] [--state closed|open|<clip> [--t SECONDS]] [--save PATH]
            [--glb [PATH]] [--keep-raw] [--no-render] [--strip CLIP --every N]

`--glb` bakes every clip and writes the compressed GLB the site loads, docs/assets/pals/core.glb (or PATH);
the exporter's raw file goes to the system's temp folder, outside the repository, and is deleted unless
`--keep-raw`. `--state` poses the
stills: closed (the rest pose), open, or any clip at time `--t`; `strip` renders a contact strip of a clip
(default unfold), a frame every `--every` frames. `--look`, `--tuck` and `--lift` override the open pose's
numbers, for trying alternatives (see OPEN_LOOK).

The reference is `Archie's unfolding Atlas Core.png` (outside the repository, with the model sheets): the
closed ball (REMOVED), the open flower (UNFOLDED and the big centre image) and the worlds it projects.

THE BALL. A truncated icosahedron, a football's 12 pentagons and 20 hexagons, of radius 0.10 m (it fills
Archie's 0.118 m dock frame and sits in his palm), five-fold axis upright. Each panel is a graphite tray with a
glazed ceramic insert proud of it, the inserts printed with olive-lime continents from one atlas texture drawn
on the sphere, so the coastlines run on across the seams. The trays' rims are the graphite frame, cyan lights
set in some of it; the hinges are knuckles lying in the seams; a lime-ringed lens sits low on the front-right
pentagon.

THE PETALS. The bottom pentagon, its five hexagons and the five pentagons above them are the base cup. The
other 21 panels hang on its rim as ten petals of two panels each (a hinge at the rim, another between the
two panels), and the top pentagon is a lid hinged to the back petal's tip. Petals alternate round the rim:
the odd ones (`HH`, a hexagon on a hexagon) hinge on the top edges of the cup's pentagons, the even ones
(`HU`, a pentagon on a hexagon) lower down, between them. Opening, every petal swings out in its own
vertical plane and its tip flops right over onto the petal's back, so the open Core is one ring of panels
round the disc, as on the sheet; the back petal instead stands both its panels up, a long petal behind the
world with the lid tucked behind it. The panels are ceramic on both faces, so whichever face a petal shows a
camera, it shows a map. Every hinge's line stands clear of the panel it turns, so nothing swings through its
neighbour (the clips were checked, frame by frame, for interpenetration).

THE STAGE. Inside, on a stem, sits the projector: a graphite rim round a glowing disc with cyan rings. It
lifts a little as the Core opens, its rings ripple out, its glow rises, and the worlds stand on it.

THE RIG. Every state is a pose of the closed rest pose (rotations, plus the stage's lift and the glow's,
the rings' and the glint's scale), so the page can blend any of them:

    core_root                 the ball's centre: docks on Archie's `core` bone, or sits at `grip_*` + 0.085 Z
      base                    the cup; its head is the ball's lowest point, so it rocks on a palm
        petal_1..10           rim hinges, +X opens (1 is the back petal, counting anticlockwise from above)
          petal_N_tip         the hinge between a petal's two panels, +X unfolds
            cap               (on petal_1_tip) the top pentagon, +X lifts it back
        lens > glint          the button, and the star of light that glints on it (scaled up from nothing)
        stage                 the disc's centre; local Y is up and Z is front, so a world parented to it at
                              identity stands upright facing the camera
          rings               the disc's light rings (spin on Y, scale out from the centre)
          dial                the size dial on the rim (spin on Y)
          holo                the projector's glow (lifts and scales)

Budget: under 12k triangles, one skinned mesh. Materials are glTF-safe principled ones; everything that
glows is named `holo_*`, for the page to swap for additive shaders.
"""
from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Quaternion, Vector

HERE = Path(__file__).resolve().parent
SITE_GLB = HERE.parent.parent / "docs" / "assets" / "pals" / "core.glb"
sys.path.insert(0, str(HERE))
from kit import anim, export, geo, mat, rig, studio  # noqa: E402
from kit.anim import Clip, Pose  # noqa: E402
from kit.geo import V, lerp, part  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    if flag in ARGS:
        return ARGS[ARGS.index(flag) + 1]
    return default


# ----------------------------------------------------------------------------------------- dimensions
RADIUS = 0.100              # the ball, to the crown of an insert
R_TOP = 0.0984              # an insert's top at its rim (it domes to RADIUS)
R_TRAY = 0.0948             # a tray's top: the graphite frame, and the line every hinge turns on
R_BACK = 0.0860             # a tray's back
R_HINGE = R_TRAY + 0.0003   # the rim hinges' line, mid-edge
R_HINGE_TIP = R_TOP + 0.0012  # the tip hinges'
D_INS, RHO_INS, BEV_INS = 0.0068, 0.0095, 0.0032     # an insert's inset from the seam, corner radius, bevel
D_TRAY, RHO_TRAY, BEV_TRAY = 0.0005, 0.0062, 0.0016  # a tray's
RIDGE = 0.0011              # the frame's rail: a tray's rim rises this much round the insert
D_IN, RHO_IN, H_IN = 0.0062, 0.0055, 0.0016          # the ceramic on a petal's back
SPIN = 54.0                 # turns the football so that a petal of each kind lies on the Y axis
STAGE_Z = -0.012            # the disc's centre, closed; it rises by STAGE_LIFT to open
STAGE_LIFT = float(opt("--lift", "0.006"))
DISC_R, RIM_R = 0.071, 0.0795
RIM_TOP = (RIM_R - 0.0022 + DISC_R + 0.0016) / 2   # the middle of the rim's flat top: its lights, the dial
DIAL_AZ = 234.0             # the size dial's place on the rim (front left)
LENS_FACE = "L3"            # the front-right pentagon (azimuth -54)
LAND = 0.572                # the continents' threshold on the map's noise (a quarter of the globe is land)
PX = 1.0 / RADIUS           # metres -> units of a panel's tangent plane (one unit = one radius)
GLINT_SCALE = 0.03          # the glint star is built this small, hidden in the lens's knob


# ------------------------------------------------------------------------------------------- palette
def palette(atlas_img):
    P = dict(
        ceramic=mat.textured(mat.principled("ceramic", "#ebe5da", rough=0.24, coat=0.85, coat_rough=0.07),
                             atlas_img),
        graphite=mat.principled("graphite", "#1f1e1d", rough=0.32, coat=0.6, coat_rough=0.12, spec=0.45),
        lime=mat.principled("lime", "#a4c812", rough=0.26, coat=0.85, coat_rough=0.05),
        brass=mat.principled("brass", "#6f5534", metal=1.0, rough=0.42),
        chrome=mat.principled("chrome", "#55524f", metal=1.0, rough=0.22),
        lens=mat.principled("lens", "#121416", rough=0.06, coat=1.0, coat_rough=0.02, spec=0.8),
        holo_line=mat.principled("holo_line", "#2fe3f1", rough=0.3, emit="#2fe3f1", strength=3.0),
        holo_disc=mat.principled("holo_disc", "#031c21", rough=0.45, spec=0.2, emit="#0c8f9b", strength=1.8),
        holo_ring=mat.principled("holo_ring", "#2fe3f1", rough=0.3, emit="#2fe3f1", strength=4.0),
        holo_glow=mat.principled("holo_glow", "#000000", rough=1.0, spec=0.0, emit="#2fe3f1", strength=1.6,
                                 alpha=0.07),
        holo_veil=mat.principled("holo_veil", "#000000", rough=1.0, spec=0.0, emit="#2fe3f1", strength=1.6,
                                 alpha=0.025),
        holo_core=mat.principled("holo_core", "#d8fdff", rough=0.3, emit="#bff8ff", strength=6.0),
        holo_spark=mat.principled("holo_spark", "#ffffff", rough=0.3, emit="#f4ffe0", strength=8.0),
    )
    for k in ("holo_glow", "holo_veil"):
        P[k].use_backface_culling = False
    for m in P.values():
        m["pal"] = "core"
    return P


# ------------------------------------------------------------------------------------------ football
class Face:
    """One panel of the football: its centre `c`, its corners `verts` (unit vectors, anticlockwise seen from
    outside), and a tangent frame (t1, t2, c) whose plane, at distance 1, the panel is drawn in."""

    def __init__(self, name, verts):
        self.name = name
        c = sum(verts, Vector()).normalized()
        up = V(0, 0, 1) - c * c.z
        if up.length < 1e-6:                     # the poles: up is towards the back petal
            up = V(0, 1, 0)
        t2 = up.normalized()
        t1 = t2.cross(c)
        pts = [self._plane(v, c, t1, t2) for v in verts]
        if sum(a.x * b.y - b.x * a.y for a, b in zip(pts, pts[1:] + pts[:1])) < 0:
            verts, pts = verts[::-1], pts[::-1]
        self.c, self.t1, self.t2, self.verts, self.poly = c, t1, t2, verts, pts
        self.n = len(verts)
        self.keys = [_key(v) for v in verts]
        self.r_in = sum(((a + b) / 2).length for a, b in zip(pts, pts[1:] + pts[:1])) / self.n
        self.angles = [math.atan2(p.y, p.x) for p in pts]

    @staticmethod
    def _plane(v, c, t1, t2):
        p = v / v.dot(c) - c
        return Vector((p.dot(t1), p.dot(t2)))

    def at(self, q, radius):
        """The point over plane point `q` at `radius` from the ball's centre."""
        return (self.c + self.t1 * q.x + self.t2 * q.y).normalized() * radius

    def ring(self, inset, rho, rad, m, scale=1.0):
        """The panel's outline inset by `inset` metres, its corners rounded with radius `rho`, offset to
        corner radius `rad` (the same corner centres, so rings of one profile correspond point for
        point), `m` points to a corner, shrunk towards the centre by `scale`. Plane coordinates."""
        k = math.pi / self.n
        cr = (self.r_in - (inset + rho) * PX) / math.cos(k)
        out = []
        for g in self.angles:
            C = Vector((math.cos(g), math.sin(g))) * cr
            for j in range(m):
                a = g + k * (2 * j / (m - 1) - 1)
                out.append((C + Vector((math.cos(a), math.sin(a))) * rad * PX) * scale)
        return out

    def edge_line(self, i, inset, frac=(0.0, 1.0), n=3):
        """Points along edge i (corner i to corner i+1) inset by `inset` metres, from frac[0] to frac[1]."""
        a, b = self.poly[i], self.poly[(i + 1) % self.n]
        s = (self.r_in - inset * PX) / self.r_in
        return [(a.lerp(b, lerp(frac[0], frac[1], t / (n - 1)))) * s for t in range(n)]

    def edge_index(self, other):
        """The index of the edge this face shares with `other`."""
        for i in range(self.n):
            if self.keys[i] in other.keys and self.keys[(i + 1) % self.n] in other.keys:
                return i
        raise ValueError(f"{self.name} and {other.name} share no edge")


def _key(v):
    return tuple(round(x, 5) for x in v)


def football():
    """The truncated icosahedron on the unit sphere: {name: Face}. The pentagons are an icosahedron's
    vertices (T the top, U0..4 the upper ring, L0..4 the lower ring, B the bottom) and the hexagons its faces
    (H1 round the top, H2 and H3 the bands above and below the equator, H4 round the bottom)."""
    lat = math.atan(0.5)

    def d(az, el):
        a = math.radians(az)
        return V(math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el))

    ico = {"T": V(0, 0, 1), "B": V(0, 0, -1)}
    for k in range(5):
        ico[f"U{k}"] = d(SPIN + 72 * k, lat)
        ico[f"L{k}"] = d(SPIN + 36 + 72 * k, -lat)
    tris = {}
    for k in range(5):
        k1 = (k + 1) % 5
        tris[f"H1{k}"] = ("T", f"U{k}", f"U{k1}")
        tris[f"H2{k}"] = (f"U{k}", f"U{k1}", f"L{k}")
        tris[f"H3{k}"] = (f"L{k}", f"L{k1}", f"U{k1}")
        tris[f"H4{k}"] = ("B", f"L{k1}", f"L{k}")
    nbrs = {n: set() for n in ico}
    for a, b, c in tris.values():
        for x, y in ((a, b), (b, c), (c, a)):
            nbrs[x].add(y)
            nbrs[y].add(x)
    faces = {}
    for n, X in ico.items():
        faces[n] = Face(n, _around(X, [((2 * X + ico[y]) / 3).normalized() for y in nbrs[n]]))
    for n, (a, b, c) in tris.items():
        A, B, C = ico[a], ico[b], ico[c]
        pts = [(2 * A + B) / 3, (A + 2 * B) / 3, (2 * B + C) / 3, (B + 2 * C) / 3, (2 * C + A) / 3, (C + 2 * A) / 3]
        faces[n] = Face(n, [p.normalized() for p in pts])
    return faces


def _around(c, pts):
    """`pts` sorted by angle round `c`."""
    t2 = (V(0, 0, 1) - c * c.z)
    t2 = (t2 if t2.length > 1e-6 else V(0, 1, 0)).normalized()
    t1 = t2.cross(c)
    return sorted(pts, key=lambda p: math.atan2(p.dot(t2), p.dot(t1)))


def petals(F):
    """The ten petals round the rim, anticlockwise from the back (+Y) seen from above:
    [(name, kind, lower face, tip face, the cup face the lower one hinges on)]."""
    out = []
    for i in range(10):
        if i % 2 == 0:
            k = i // 2
            out.append((f"petal_{i + 1}", "HH", F[f"H2{k}"], F[f"H1{k}"], F[f"L{k}"]))
        else:
            k = (i - 1) // 2
            out.append((f"petal_{i + 1}", "HU", F[f"H3{k}"], F[f"U{(k + 1) % 5}"], F[f"H4{k}"]))
    return out


BASE_FACES = ["B"] + [f"H4{k}" for k in range(5)] + [f"L{k}" for k in range(5)]


# --------------------------------------------------------------------------------------------- shells
def shell(name, rings, mat_, uv=None):
    """A mesh through `rings` of 3D points, every ring the same length; a lone Vector is a pole, fanned.
    The rings run round the panel anticlockwise seen from outside and the profile from the crown outwards,
    down the side and in along the back, which makes every face point out. `uv` gives each ring's
    texture coordinates (or None)."""
    bm = bmesh.new()
    uvl = bm.loops.layers.uv.new("UVMap") if uv else None
    vr = [bm.verts.new(r) if isinstance(r, Vector) else [bm.verts.new(p) for p in r] for r in rings]
    uvr = uv or [None] * len(rings)
    for (A, ua), (B, ub) in zip(zip(vr, uvr), list(zip(vr, uvr))[1:]):
        n = len(B) if isinstance(A, bmesh.types.BMVert) else len(A)
        for j in range(n):
            k = (j + 1) % n
            if isinstance(A, bmesh.types.BMVert):
                vs, us = (A, B[j], B[k]), (ua, ub[j], ub[k]) if uv else None
            elif isinstance(B, bmesh.types.BMVert):
                vs, us = (A[j], B, A[k]), (ua[j], ub, ua[k]) if uv else None
            else:
                vs, us = (A[j], B[j], B[k], A[k]), (ua[j], ub[j], ub[k], ua[k]) if uv else None
            f = bm.faces.new(vs)
            if uv:
                for loop, u in zip(f.loops, us):
                    loop[uvl].uv = u
    return geo.mesh_object(name, bm, mat_)


class Atlas:
    """Hands out texture cells: an 8x8 grid, one cell per ceramic face (the panels' outer and inner faces).
    A cell spans plane coordinates -EXTENT..EXTENT both ways."""
    GRID, EXTENT = 8, 0.5

    def __init__(self):
        self.cells = []

    def cell(self, face, inner=False):
        self.cells.append((face, inner))
        i = len(self.cells) - 1
        gx, gy = i % self.GRID, i // self.GRID
        s = 1.0 / self.GRID

        def uv(q):
            return ((gx + (q.x / self.EXTENT + 1) / 2) * s, (gy + (q.y / self.EXTENT + 1) / 2) * s)
        return uv


def insert(face, M, atlas, name):
    """The ceramic insert: a domed plate with rounded corners and a rounded rim, sunk into its tray."""
    uv = atlas.cell(face)
    c45 = math.cos(math.pi / 4)
    prof = [  # (corner radius, radius from the ball's centre)
        (RHO_INS - BEV_INS, R_TOP),
        (RHO_INS - BEV_INS * (1 - c45), R_TOP - BEV_INS * (1 - c45)),
        (RHO_INS, R_TOP - BEV_INS),
        (RHO_INS, R_TRAY - 0.0015),
    ]
    rings, uvs = [face.c * RADIUS], [uv(Vector((0, 0)))]
    for rho, rad in prof:
        q = face.ring(D_INS, RHO_INS, rho, 3)
        rings.append([face.at(p, rad) for p in q])
        uvs.append([uv(p) for p in q])
    return shell(name, rings, M["ceramic"], uvs)


def tray(face, M, name, back=True):
    """The graphite tray an insert sits in: its top is the frame round the insert, its back the inside of
    the ball. `back=False` leaves a hole in the back for an inner insert to plug."""
    m = 2
    prof = [(face.ring(D_INS, RHO_INS, RHO_INS - 0.0016, m), R_TRAY),
            (face.ring(D_TRAY, RHO_TRAY, RHO_TRAY - BEV_TRAY - 0.0018, m), R_TRAY + RIDGE),
            (face.ring(D_TRAY, RHO_TRAY, RHO_TRAY - BEV_TRAY, m), R_TRAY),
            (face.ring(D_TRAY, RHO_TRAY, RHO_TRAY, m), R_TRAY - BEV_TRAY),
            (face.ring(D_TRAY, RHO_TRAY, RHO_TRAY, m), R_BACK)]
    if not back:
        prof.append((face.ring(D_IN, RHO_IN, RHO_IN - 0.0014, m), R_BACK))
    rings = [[face.at(p, rad) for p in q] for q, rad in prof]
    if back:
        rings.append(face.c * R_BACK)
    return shell(name, rings, M["graphite"])


def inner_insert(face, M, atlas, name):
    """Ceramic on a petal's back, so an open petal shows a map whichever face it turns to the camera."""
    uv = atlas.cell(face, inner=True)
    rings, uvs = [], []
    for rho, rad in ((RHO_IN, R_BACK + 0.0012), (RHO_IN - 0.0012, R_BACK - H_IN)):
        q = face.ring(D_IN, RHO_IN, rho, 2)
        rings.append([face.at(p, rad) for p in q])
        uvs.append([uv(p) for p in q])
    rings.append(face.c * (R_BACK - H_IN * 1.8))
    uvs.append(uv(Vector((0, 0))))
    return shell(name, rings, M["ceramic"], uvs)


def light_strip(face, i, M, name, frac=(0.2, 0.8)):
    """A cyan light set in the frame's rail along edge i of `face`."""
    rail = D_TRAY + RHO_TRAY - (RHO_TRAY - BEV_TRAY - 0.0018)
    pts = [face.at(q, R_TRAY + RIDGE + 0.0002) for q in face.edge_line(i, rail, frac, 3)]
    return geo.sweep(name, pts, 0.00085, 0.0007, M["holo_line"], n=4, segs=4, up=face.c)


def barrel(name, centre, axis, length, radius, mat_, segs=6):
    h = length / 2
    return geo.lathe(name, [(0.0, -h), (radius, -h), (radius, h), (0.0, h)], mat_, centre, axis, segs=segs)


def hinge_line(face, other, radius=R_HINGE):
    """The hinge between two neighbouring panels: (midpoint, unit direction, length), the chord of their
    shared edge, its middle `radius` from the centre. No part of a panel stands proud of its hinge's line,
    or it would swing into its neighbour: a rim hinge lies on the trays' top, a tip's stands on the seam at
    the inserts' height, so that the tip can fold right over onto the back of its petal."""
    i = face.edge_index(other)
    a, b = face.verts[i], face.verts[(i + 1) % face.n]
    k = radius / ((a + b) / 2).length
    a, b = a * k, b * k
    return (a + b) / 2, (b - a).normalized(), (b - a).length


# ------------------------------------------------------------------------------------------- texture
def _hash3(ix, iy, iz, seed):
    h = (ix * 73856093) ^ (iy * 19349663) ^ (iz * 83492791) ^ (seed * 2654435761)
    h &= 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 1274126177) & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFF) / float(0xFFFFFF)


def _vnoise(p, seed):
    """Smooth 3D value noise in 0..1 at points p (..., 3)."""
    i = np.floor(p).astype(np.int64)
    f = p - i
    f = f * f * (3 - 2 * f)
    out = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((f[..., 0] if dx else 1 - f[..., 0]) * (f[..., 1] if dy else 1 - f[..., 1]) *
                     (f[..., 2] if dz else 1 - f[..., 2]))
                out = out + w * _hash3(i[..., 0] + dx, i[..., 1] + dy, i[..., 2] + dz, seed)
    return out


def _fbm(p, seed, octaves=5, gain=0.5):
    tot, amp, norm = 0.0, 1.0, 0.0
    for o in range(octaves):
        tot = tot + amp * _vnoise(p * (2.03 ** o), seed + o * 17)
        norm += amp
        amp *= gain
    return tot / norm


def _smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def atlas_image(atlas, n=1024, seed=4):
    """The map printed on the ceramic, cell by cell: warm white glaze with a faint mottle, olive-lime
    continents with a darker coast, thin map lines (rivers, roads, a few great circles), dots for cities,
    and the glaze's brown specks. Drawn on the sphere, so neighbouring panels agree; outside its panel a
    cell is plain glaze, which keeps the texture small."""
    g, E = Atlas.GRID, Atlas.EXTENT
    cs = n // g
    img = np.zeros((n, n, 3), np.float32)
    hexc = lambda h: np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)], np.float32)
    base, land, land2, coast = hexc("#efe6d4"), hexc("#979a3c"), hexc("#a9ab50"), hexc("#7b8027")
    line_c, dot_c, speck_c = hexc("#a0a23f"), hexc("#8f962c"), hexc("#8a735c")
    rng = np.random.default_rng(seed)
    circles = [Vector(rng.normal(size=3)).normalized() for _ in range(7)]
    cities = rng.normal(size=(260, 3))
    cities /= np.linalg.norm(cities, axis=1, keepdims=True)
    u = (np.arange(cs) + 0.5) / cs * 2 - 1
    X, Y = np.meshgrid(u * E, u * E)
    px = 2 * E / cs                                     # plane units (radians, near the centre) per pixel
    cover = []
    for idx, (face, inner) in enumerate(atlas.cells):
        d = (np.array(face.c)[None, None, :] + X[..., None] * np.array(face.t1) + Y[..., None] * np.array(face.t2))
        d /= np.linalg.norm(d, axis=2, keepdims=True)
        p = d if not inner else d[..., [1, 2, 0]] * np.array([1, -1, 1]) + 3.1
        # continents: a warped fbm, thresholded softly
        warp = np.stack([_fbm(p * 1.7 + 11.3, seed + 40, 3), _fbm(p * 1.7 + 5.1, seed + 50, 3),
                         _fbm(p * 1.7 + 7.7, seed + 60, 3)], axis=-1) - 0.5
        h = _fbm(p * 3.0 + warp * 1.1, seed, 6)
        m = _smooth(LAND - 0.006, LAND + 0.006, h)
        shore = np.exp(-((h - LAND) / 0.005) ** 2)
        cover.append(float(m.mean()))
        inside = _fbm(p * 7.0, seed + 90, 3)
        col = base[None, None, :] * (1 + (_fbm(p * 5.0, seed + 7, 3) - 0.5)[..., None] * 0.07)
        lc = land[None, None, :] * (1 - inside[..., None]) + land2[None, None, :] * inside[..., None]
        col = col * (1 - 0.88 * m[..., None]) + lc * (0.88 * m[..., None])
        col = col * (1 - 0.45 * shore[..., None]) + coast[None, None, :] * (0.45 * shore[..., None])
        # thin map lines: contours of two noises (rivers and roads), and great circles
        ln = 0.0
        for k, (f, w) in enumerate(((3.1, 0.010), (5.3, 0.008))):
            q = _fbm(p * f + 20 + k, seed + 100 + k, 4)
            ln = np.maximum(ln, np.exp(-((q - 0.5) / w) ** 2) * (0.75 - 0.25 * k))
        for cv in circles:
            dd = np.abs(d @ np.array(cv))
            ln = np.maximum(ln, np.exp(-(dd / (px * 0.55)) ** 2) * 0.5)
        col = col * (1 - ln[..., None] * 0.6) + line_c[None, None, :] * (ln[..., None] * 0.6)
        # cities: dots near the lines and the land
        near = cities[(cities @ np.array(face.c)) > 0.8]
        for cpt in near:
            ang = np.arccos(np.clip(d @ cpt, -1, 1))
            w = np.clip(1.6 - ang / (px * 1.4), 0, 1)
            col = col * (1 - w[..., None] * 0.85) + dot_c[None, None, :] * (w[..., None] * 0.85)
        # specks in the glaze
        for _ in range(6):
            sx, sy = rng.uniform(-E * 0.8, E * 0.8, 2)
            r = rng.uniform(0.6, 1.3) * px
            w = np.clip(1.5 - np.sqrt((X - sx) ** 2 + (Y - sy) ** 2) / r, 0, 1) * rng.uniform(0.3, 0.6)
            col = col * (1 - w[..., None]) + speck_c[None, None, :] * w[..., None]
        # outside the panel nothing is drawn: flat glaze compresses to nothing
        on_panel = np.ones_like(X, bool)
        for pa, pb in zip(face.poly, face.poly[1:] + face.poly[:1]):
            on_panel &= (pb.x - pa.x) * (Y - pa.y) - (pb.y - pa.y) * (X - pa.x) > -0.02 * (pb - pa).length
        col = np.where(on_panel[..., None], col, base[None, None, :])
        gx, gy = idx % g, idx // g
        r0 = n - (gy + 1) * cs
        img[r0:r0 + cs, gx * cs:(gx + 1) * cs] = np.clip(col[::-1], 0, 1)
    print(f"CORE atlas land cover {sum(cover) / len(cover):.2f}")
    return mat.image("core-atlas", img)


# --------------------------------------------------------------------------------------------- build
def build():
    F = football()
    P = petals(F)
    atlas = Atlas()
    parts, later = [], []

    def add(ob, bone):
        part(ob, bone)
        parts.append(ob)
        return ob

    # The material list needs the atlas image, which needs every cell handed out first: build the
    # textured inserts against a placeholder material and swap it in at the end.
    M = palette(bpy.data.images.new("core-atlas-tmp", 4, 4))
    R = rig.Rig("core")

    # ---- skeleton --------------------------------------------------------------------------------
    R.bone("core_root", (0, 0, 0), (0, -0.1, 0), z=(0, 0, 1))
    R.bone("base", (0, 0, -RADIUS), (0, 0, 0), "core_root", z=(0, -1, 0))
    hinge = {}
    for name, kind, low, tip, cup in P:
        mid, ax, ln = hinge_line(low, cup)
        up = (low.c * R_TRAY - mid).normalized()
        R.bone(name, mid, mid + up * 0.03, "base", z=low.c)
        hinge[name] = (mid, ax, ln)
        mid2, ax2, ln2 = hinge_line(tip, low, R_HINGE_TIP)
        up2 = (tip.c * R_TRAY - mid2).normalized()
        R.bone(name + "_tip", mid2, mid2 + up2 * 0.03, name, z=tip.c)
        hinge[name + "_tip"] = (mid2, ax2, ln2)
    cap_low = P[0][3]
    mid3, ax3, ln3 = hinge_line(F["T"], cap_low, R_HINGE_TIP)
    R.bone("cap", mid3, mid3 + (F["T"].c * R_TRAY - mid3).normalized() * 0.03, "petal_1_tip", z=(0, 0, 1))
    hinge["cap"] = (mid3, ax3, ln3)
    lf = F[LENS_FACE]
    R.bone("lens", lf.c * RADIUS, lf.c * (RADIUS + 0.03), "base", z=(0, 0, 1))
    R.bone("glint", lf.c * (R_TOP + 0.0096), lf.c * (RADIUS + 0.03), "lens", z=(0, 0, 1))
    sz = STAGE_Z
    R.bone("stage", (0, 0, sz), (0, 0, sz + 0.06), "base", z=(0, -1, 0))
    R.bone("rings", (0, 0, sz), (0, 0, sz + 0.04), "stage", z=(0, -1, 0))
    dial_az = math.radians(DIAL_AZ)
    dial_p = V(math.cos(dial_az), math.sin(dial_az), 0) * RIM_TOP + V(0, 0, sz + 0.0056)
    R.bone("dial", dial_p, dial_p + V(0, 0, 0.02), "stage", z=(0, -1, 0))
    R.bone("holo", (0, 0, sz), (0, 0, sz + 0.05), "stage", z=(0, -1, 0))

    # ---- panels ----------------------------------------------------------------------------------
    owner = {f: "base" for f in BASE_FACES}
    for name, kind, low, tip, cup in P:
        owner[low.name], owner[tip.name] = name, name + "_tip"
    owner["T"] = "cap"
    for fname in BASE_FACES + [n for n in F if n not in BASE_FACES]:
        face = F[fname]
        bone = owner[fname]
        add(insert(face, M, atlas, f"insert-{fname}"), bone)
        is_petal = bone != "base"
        add(tray(face, M, f"tray-{fname}", back=not is_petal), bone)
        if is_petal:
            later.append((face, bone))
    for face, bone in later:
        add(inner_insert(face, M, atlas, f"inner-{face.name}"), bone)

    # ---- hinges: brass knuckles at the rim, dark chrome ones between a petal's panels ---------------
    for name, kind, low, tip, cup in P:
        mid, ax, ln = hinge[name]
        for s in (-1, 1):
            add(barrel(f"knuckle-{name}{s}", mid + ax * s * ln * 0.3, ax, ln * 0.2, 0.0031, M["brass"]), "base")
        add(barrel(f"knuckle-{name}", mid, ax, ln * 0.34, 0.0031, M["brass"]), name)
        mid2, ax2, ln2 = hinge[name + "_tip"]
        add(barrel(f"knuckle-{name}_tip", mid2, ax2, ln2 * 0.4, 0.0029, M["chrome"]), name + "_tip")
    mid3, ax3, ln3 = hinge["cap"]
    add(barrel("knuckle-cap", mid3, ax3, ln3 * 0.4, 0.0029, M["chrome"]), "cap")

    # ---- light: cyan strips along the far edges of the petal tips, the cap and a few cup seams ------
    for name, kind, low, tip, cup in P:
        i0 = tip.edge_index(low)
        far = [(i0 + tip.n // 2) % tip.n] if kind == "HH" else [(i0 + 2) % 5, (i0 + 3) % 5]
        for i in far:
            add(light_strip(tip, i, M, f"light-{name}-{i}", (0.18, 0.82)), name + "_tip")
    T = F["T"]
    i0 = T.edge_index(cap_low)
    for i in ((i0 + 2) % 5, (i0 + 3) % 5):
        add(light_strip(T, i, M, f"light-cap-{i}"), "cap")
    for k in range(5):
        h4 = F[f"H4{k}"]
        i = h4.edge_index(F[f"L{k}"])
        add(light_strip(h4, i, M, f"light-H4{k}", (0.25, 0.75)), "base")

    # ---- the lens: a lime ring, a graphite cup, a thin lime ring and dark glass, a knob in the middle -
    c, ax = lf.c, lf.c
    o = c * (R_TOP - 0.001)
    for ob in (
        geo.lathe("lens-cup", [(0.0, 0.0), (0.0192, 0.0), (0.0197, 0.0056), (0.0172, 0.0074), (0.0, 0.0074)],
                  M["graphite"], o, ax, segs=18),
        geo.ring("lens-lime", 0.0206, 0.0035, M["lime"], c * (R_TOP + 0.0016), ax, segs=18, sides=4, squash=0.9),
        geo.ring("lens-lime2", 0.0128, 0.0013, M["lime"], o + ax * 0.0075, ax, segs=18, sides=3),
        geo.lathe("lens-glass", [(0.0119, 0.0066), (0.0106, 0.0086), (0.006, 0.0098), (0.0, 0.0102)], M["lens"],
                  o, ax, segs=18, caps=False),
        geo.lathe("lens-knob", [(0.0042, 0.0092), (0.0042, 0.0106), (0.003, 0.0114), (0.0, 0.0114)],
                  M["chrome"], o, ax, segs=10, caps=False)):
        add(ob, "lens")
    # the glint: a star of light, built tiny and hidden in the knob (the clips push it out and scale it up)
    star = glint_star(M, o + ax * 0.0106, ax)
    add(star, "glint")

    # ---- the stage --------------------------------------------------------------------------------
    stage_parts(M, add)

    R.build()
    img = atlas_image(atlas, int(opt("--atlas", "1024")))
    tmp = M["ceramic"].node_tree.nodes["Image Texture"].image
    M["ceramic"].node_tree.nodes["Image Texture"].image = img
    bpy.data.images.remove(tmp)
    return R, parts, M


def glint_star(M, centre, axis):
    """Four long spikes and four short ones round a point, facing out along `axis`."""
    B = geo.basis(axis, (0, 0, 1))
    bm = bmesh.new()
    cv = bm.verts.new(centre)
    pts = []
    for j in range(8):
        a = math.tau * j / 8
        r = (0.02 if j % 2 == 0 else 0.007) * GLINT_SCALE
        pts.append(bm.verts.new(centre + B @ V(math.cos(a) * r, math.sin(a) * r, 0)))
    ring_ = []
    for j in range(8):
        a = math.tau * (j + 0.5) / 8
        r = 0.0016 * GLINT_SCALE
        ring_.append(bm.verts.new(centre + B @ V(math.cos(a) * r, math.sin(a) * r, 0)))
    for j in range(8):
        bm.faces.new((cv, ring_[j - 1], pts[j]))
        bm.faces.new((cv, pts[j], ring_[j]))
    return geo.mesh_object("glint", bm, M["holo_spark"])


def band(name, r0, r1, z, mat_, segs=36, a0=0.0, a1=None):
    """A flat strip facing up: an annulus from r0 to r1 at height z, or an arc of one from a0 to a1."""
    full = a1 is None
    n = segs if full else segs + 1
    ang = [a0 + (math.tau if full else a1 - a0) * j / segs for j in range(n)]
    ring_ = lambda r: [V(math.cos(a) * r, math.sin(a) * r, z) for a in ang]
    if full:
        return shell(name, [ring_(r0), ring_(r1)], mat_)
    bm = bmesh.new()
    vi, vo = [bm.verts.new(p) for p in ring_(r0)], [bm.verts.new(p) for p in ring_(r1)]
    for j in range(segs):
        bm.faces.new((vi[j], vo[j], vo[j + 1], vi[j + 1]))
    return geo.mesh_object(name, bm, mat_)


def stage_parts(M, add):
    """The projector: a graphite rim round a glowing disc, light rings on it, a stem below, the size dial on
    the rim and the glow above."""
    sz = STAGE_Z
    up = (0, 0, 1)
    O = V(0, 0, sz)
    rim = [(0.0, -0.011), (0.06, -0.008), (RIM_R, -0.0035), (RIM_R, 0.0025), (RIM_R - 0.0022, 0.0058),
           (DISC_R + 0.0016, 0.0058), (DISC_R, 0.0012)]
    add(geo.lathe("stage-rim", rim, M["graphite"], O, up, segs=28, caps=False), "stage")
    add(shell("stage-disc", [O + V(0, 0, 0.0012), [V(math.cos(a) * DISC_R, math.sin(a) * DISC_R, sz + 0.0012)
                                                   for a in (math.tau * j / 32 for j in range(32))]],
              M["holo_disc"]), "stage")
    add(geo.lathe("stage-stem", [(0.0, -0.072), (0.011, -0.072), (0.011, -0.009)], M["graphite"], O, up, segs=8,
                  caps=False), "stage")
    for k in range(6):                                  # cyan lights set into the rim's top
        a0 = math.tau * (k + 0.5) / 6
        pts = [V(math.cos(a0 + da) * RIM_TOP, math.sin(a0 + da) * RIM_TOP, sz + 0.006) for da in (-0.12, 0.12)]
        add(geo.sweep(f"rim-light{k}", pts, 0.0009, 0.0005, M["holo_line"], n=4, segs=4, up=up), "stage")
    # the dial: a graphite knob with a lime cap and a cyan tick
    dial_az = math.radians(DIAL_AZ)
    dd = V(math.cos(dial_az), math.sin(dial_az), 0)
    dc = dd * RIM_TOP + V(0, 0, sz + 0.0056)
    add(geo.lathe("dial-knob", [(0.0, 0.0), (0.0052, 0.0), (0.0052, 0.0046), (0.0038, 0.006), (0.0, 0.006)],
                  M["graphite"], dc, up, segs=10), "dial")
    add(geo.ring("dial-lime", 0.0045, 0.0009, M["lime"], dc + V(0, 0, 0.005), up, segs=10, sides=3), "dial")
    add(geo.sweep("dial-tick", [dc + V(0, 0, 0.0062) - dd * 0.0036, dc + V(0, 0, 0.0062) - dd * 0.0008], 0.0006,
                  0.0004, M["holo_line"], n=4, segs=4, up=up), "dial")
    # the light rings: three bright circles and six dashes between the outer two
    for k, (r0, r1) in enumerate(((0.25, 0.28), (0.49, 0.515), (0.9, 0.925))):
        add(band(f"ring{k}", r0 * DISC_R, r1 * DISC_R, sz + 0.0019, M["holo_ring"]), "rings")
    for k in range(6):
        a0 = math.tau * k / 6
        add(band(f"ring-dash{k}", 0.68 * DISC_R, 0.71 * DISC_R, sz + 0.0019, M["holo_ring"], 4, a0, a0 + 0.55),
            "rings")
    # the projector's lens in the middle, and its glow (built squat: `holo` stretches it to open)
    add(geo.lathe("holo-emitter", [(0.0085, 0.0012), (0.006, 0.0035), (0.0, 0.0045)], M["holo_core"], O, up,
                  segs=12, caps=False), "stage")
    add(geo.ring("holo-emitter-rim", 0.0097, 0.0013, M["graphite"], O + V(0, 0, 0.0014), up, segs=12, sides=3),
        "stage")
    # the glow fades upwards in two steps, a brighter skirt and a faint veil, with an orbit of light between
    add(geo.lathe("holo-glow", [(0.82 * DISC_R, 0.0015), (0.86 * DISC_R, 0.013)], M["holo_glow"], O, up, segs=24,
                  caps=False), "holo")
    add(geo.lathe("holo-veil", [(0.86 * DISC_R, 0.013), (0.92 * DISC_R, 0.034)], M["holo_veil"], O, up, segs=24,
                  caps=False), "holo")
    r = 0.86 * DISC_R
    add(band("holo-orbit", r - 0.0005, r + 0.0005, sz + 0.013, M["holo_ring"], 32), "holo")


# --------------------------------------------------------------------------------------------- poses
def _petal_specs():
    out = {}
    for i in range(10):
        out[f"petal_{i + 1}"] = dict(kind="HH" if i % 2 == 0 else "HU", order=min(i, 10 - i))
    return out


PETALS = _petal_specs()
# The open flower: each kind of petal's lower panel stands at this elevation (degrees above the horizontal,
# leaning out), and its tip either folds right over onto the petal's back ("tuck") or stands at its own
# elevation. The back petal stands taller, both panels up, a backdrop to the world, its tip carrying the cap
# tucked behind.
OPEN_LOOK = dict(HH=(33.0, "tuck"), HU=(42.0, "tuck"), back=(38.0, 30.0), cap="tuck")
TUCK = float(opt("--tuck", "32"))                 # how far a tucked panel stands off the back it folds onto


def _look_arg():
    a = opt("--look")
    if a:
        for kv in a.split(","):
            k, v = kv.split("=")
            if k == "cap":
                OPEN_LOOK[k] = v
            else:
                e, t = v.split(":")
                OPEN_LOOK[k] = (float(e), t if t == "tuck" else float(t))


def _elevation(R, name):
    """The rest elevation of a bone's Y (degrees above the horizontal, leaning out from the axis)."""
    s = R.specs[name]
    y = (s["tail"] - s["head"]).normalized()
    e = V(s["head"].x, s["head"].y, 0).normalized()
    return math.degrees(math.atan2(y.z, y.dot(e)))


def open_angles(R):
    """{bone: +X degrees} for the open flower. Every petal hinge turns in the petal's vertical plane, so a
    panel's elevation is its rest elevation less the turns of its hinge and the hinges below it."""
    fold = lambda child, parent: (_elevation(R, child) - _elevation(R, parent) + 180.0) % 360.0 - 180.0
    out = {}
    for name, s in PETALS.items():
        e1, tip = OPEN_LOOK["back" if name == "petal_1" else s["kind"]]
        out[name] = _elevation(R, name) - e1
        if tip == "tuck":
            out[name + "_tip"] = fold(name + "_tip", name) + 180.0 - TUCK
        else:
            out[name + "_tip"] = fold(name + "_tip", name) + e1 - tip
    cap = OPEN_LOOK["cap"]
    if cap == "tuck":
        out["cap"] = fold("cap", "petal_1_tip") + 180.0 - TUCK
    elif cap.startswith("r"):
        out["cap"] = float(cap[1:])
    else:
        e2 = OPEN_LOOK["back"][1]
        out["cap"] = fold("cap", "petal_1_tip") + e2 - float(cap[1:])
    return out


HOLO_OPEN = (1.1, 2.3, 1.1)   # the glow's scale open (local Y is up); it also lifts by HOLO_LIFT
HOLO_LIFT = 0.004
RINGS_SMALL = 0.5               # the light rings ripple out from this scale as the disc lights
GLINT_PEAK = 22.0               # how far the glint star scales up from its hidden size when it flashes


def open_pose(R, w=1.0):
    """The open Core, or `w` of the way there (rotations and the stage's lift; see `open_scales`)."""
    p = Pose()
    for name, x in open_angles(R).items():
        p.set(name, x * w)
    p.move("stage", y=STAGE_LIFT * w)
    p.move("holo", y=HOLO_LIFT * w)
    return p


def open_scales(w=1.0):
    return {"holo": tuple(1 + (s - 1) * w for s in HOLO_OPEN)}


# ---------------------------------------------------------------------------------------------- clips
class SClip(Clip):
    """A clip whose poses also scale bones (a kit Pose turns and moves them only): `scaling(fn)` adds a
    callable t -> {bone: (x, y, z)}, the factors multiplied together. Scale is what lets the glow grow out
    of nothing and the light rings ripple out; everything else in every clip is rotation and the stage's
    lift."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.scalers = []

    def scaling(self, fn):
        self.scalers.append(fn)
        return self

    def scales(self, t):
        out = {}
        for fn in self.scalers:
            for b, v in fn(t).items():
                a = out.get(b, (1.0, 1.0, 1.0))
                out[b] = (a[0] * v[0], a[1] * v[1], a[2] * v[2])
        return out


def bake(clip, skel):
    """`anim.bake`, plus the clip's scale channels in the same action."""
    acts = anim.bake(clip, skel)
    act = acts[0]
    bag = anim._fcurves_for(act, act.slots[0])
    n = clip.frames + (0 if clip.loop else 1)
    frames = [1 + i for i in range(n)]
    sc = [clip.scales(i / clip.fps) for i in range(n)]
    for bn in sorted({b for s in sc for b in s}):
        vals = [s.get(bn, (1.0, 1.0, 1.0)) for s in sc]
        if all(abs(c - 1) < 1e-6 for v in vals for c in v):
            continue
        for i in range(3):
            anim._write(bag, f'pose.bones["{bn}"].scale', i, frames, [v[i] for v in vals], bn)
    return acts


def apply(clip, skel, t):
    """Pose the Core at time t of `clip`, for stills."""
    anim.apply(clip, skel, t)
    sc = clip.scales(t)
    for pb in skel.ob.pose.bones:
        pb.scale = sc.get(pb.name, (1.0, 1.0, 1.0))
    bpy.context.view_layer.update()


def land(t):
    """0 -> 1 like a panel flopping over onto its stop: gathering speed into it, then two small bounces off
    it (a tucked panel can't go past its stop, so it bounces back, never through)."""
    if t <= 0:
        return 0.0
    if t >= 1:
        return 1.0
    if t < 0.62:
        u = t / 0.62
        return u * u * (2 - u)
    b = (t - 0.62) / 0.38
    return 1 - 0.05 * abs(math.sin(math.tau * b)) * (1 - b) ** 1.5


def _e(kind, t0, dur, t):
    return land((t - t0) / dur) if kind == "land" else anim.ease(kind, (t - t0) / dur)


def _petals(A, p, lower, tip, cap):
    """Set every petal hinge to the given fraction of open: lower(name), tip(name), and the cap."""
    for name in PETALS:
        p.set(name, A[name] * lower(name))
        p.set(name + "_tip", A[name + "_tip"] * tip(name))
    p.set("cap", A["cap"] * cap)
    return p


def _glint(p, sc, t, at, size=1.0, dur=0.16):
    """A flash of the star on the lens: out of the knob, up to size, a quarter turn, and back."""
    w = anim.pulse(t, at, dur * 0.35, dur * 0.1, dur * 0.55)
    out = anim.pulse(t, at - 0.02, 0.02, dur, 0.02)
    p.move("glint", y=0.0032 * out)
    p.set("glint", 0, 90 * anim.smooth(at, at + dur, t) * (out > 0), 0)
    g = 1 + (GLINT_PEAK * size - 1) * w
    sc["glint"] = (g, g, g)


def clips(R):
    """The Core's clips. Each starts and ends on the closed rest pose or the open pose, so the page can chain
    them: closed > unfold > open-idle > fold > closed, closed > pop-open / wont-open, open > sneeze."""
    A = open_angles(R)
    order = {n: s["order"] for n, s in PETALS.items()}
    phase = {n: 1.7 * i for i, n in enumerate(PETALS)}
    out = []

    def make(name, seconds, fn, loop=False):
        c = SClip(name, seconds, loop=loop)
        memo = {}

        def both(t):
            if t not in memo:
                memo.clear()
                memo[t] = fn(t)
            return memo[t]
        c.layer(lambda t: both(t)[0]).scaling(lambda t: both(t)[1])
        out.append(c)
        return c

    def disc(p, sc, stage, rings, ring_spin, holo):
        """The stage lifted `stage` of the way, the rings rippled out `rings` of the way and turned, the glow
        grown `holo` of the way (each may overshoot)."""
        p.move("stage", y=STAGE_LIFT * stage)
        p.set("rings", 0, ring_spin, 0)
        r = RINGS_SMALL + (1 - RINGS_SMALL) * rings
        sc["rings"] = (r, 1.0, r)
        p.move("holo", y=HOLO_LIFT * holo)
        sc["holo"] = tuple(max(0.02, 1 + (s - 1) * holo) for s in HOLO_OPEN)

    # closed: a short hold, the lens's aperture turning a little as if it were thinking
    def closed(t):
        p = Pose().set("lens", 0, 24 * anim.pulse(t, 0.05, 0.2, 0.0, 0.2), 0)
        return p, {}
    make("closed", 0.5, closed)

    # unfold: a click, the lens glints, the cap pops, the petals peel open from the back round to the front,
    # each lower panel overshooting a little and its tip flopping over behind it; the disc lifts, its rings
    # ripple out and spin up, the glow rises
    def unfold(t):
        p, sc = Pose(), {}
        press = anim.pulse(t, 0.0, 0.04, 0.03, 0.08)
        p.move("lens", y=-0.0022 * press)
        p.set("base", 1.4 * press, 0, 0)
        _glint(p, sc, t, 0.06)
        _petals(A, p, lambda n: _e("back", 0.16 + 0.05 * order[n], 0.42, t),
                lambda n: _e("land", 0.22 + 0.05 * order[n], 0.52, t), _e("land", 0.36, 0.5, t))
        rings = 1.0 if t < 0.04 else 0.0 if t < 0.5 else _e("out", 0.55, 0.45, t)
        spin_up = -110 * (1 - _e("out", 0.5, 0.7, t)) * anim.smooth(0, 0.08, t)
        disc(p, sc, _e("out", 0.42, 0.42, t), rings, spin_up, _e("back", 0.62, 0.45, t))
        return p, sc
    make("unfold", 1.2, unfold)

    # open-idle: the world bobs on its stage, the petals breathe in a slow wave round the ring, the rings
    # turn a sixth (their pattern repeats every sixth), the glow shimmers; every wobble is nought at the
    # loop's seam, so the clip begins and ends on the open pose
    def idle(t):
        p, sc = Pose(), {}
        w = t / 4.0 * math.tau
        env = (1 - math.cos(w)) / 2
        _petals(A, p, lambda n: 1 + 1.8 / A[n] * env * math.sin(2 * w - phase[n]),
                lambda n: 1 - 2.4 / A[n + "_tip"] * env * (0.5 + 0.5 * math.sin(2 * w - phase[n] - 0.7)),
                1 - 2.0 / A["cap"] * env * (0.5 + 0.5 * math.sin(2 * w - 0.7)))
        disc(p, sc, 1 + 0.0028 / STAGE_LIFT * math.sin(w), 1.0, 60 * t / 4.0, 1.0)
        h = sc["holo"]
        f = 1 + 0.05 * math.sin(2 * w) + 0.03 * math.sin(5 * w)
        g = 1 + 0.02 * math.sin(3 * w)
        sc["holo"] = (h[0] * g, h[1] * f, h[2] * g)
        return p, sc
    make("open-idle", 4.0, idle, loop=True)

    # fold: the glow drops, the disc sinks, the tips flip back over (front first) and the petals swing shut,
    # speeding up into it; the cap comes down last, snap, and the ball rocks once on its bottom
    def fold(t):
        p, sc = Pose(), {}
        rev = lambda n: 5 - order[n]
        _petals(A, p, lambda n: 1 - _e("in", 0.2 + 0.03 * rev(n), 0.3, t),
                lambda n: 1 - _e("inout", 0.1 + 0.03 * rev(n), 0.3, t), 1 - _e("in", 0.5, 0.24, t))
        hit = 0.74
        k = max(0.0, t - hit)
        for name in PETALS:                       # a little rebound as they hit the stop
            p.add(name, 2.2 * math.exp(-k * 30) * abs(math.sin(k * 40)) * (t > hit))
        p.set("base", 3.0 * math.exp(-k * 9) * math.sin(k * 34) * (t > hit) * (1 - anim.smooth(0.88, 1.0, t)), 0, 0)
        rings = 1 - _e("inout", 0.04, 0.22, t) + _e("inout", 0.8, 0.15, t)
        disc(p, sc, 1 - _e("inout", 0.12, 0.3, t), rings, 0, 1 - _e("in", 0.0, 0.24, t))
        _glint(p, sc, t, 0.8, 0.6, 0.14)
        return p, sc
    make("fold", 1.0, fold)

    # spin: the closed ball spinning in place, wobbling round its spin like a top on a palm (the wobble
    # swells and dies each turn, so a turn begins and ends upright)
    def spin(t):
        p = Pose()
        tilt = math.radians(7) * math.sin(math.pi * t) ** 2
        q = Quaternion((math.cos(math.tau * t), 0, math.sin(math.tau * t)), tilt) @ \
            Quaternion((0, 1, 0), math.tau * t)
        p.quat["base"] = q
        return p, {}
    make("spin", 1.0, spin, loop=True)

    # sneeze: "ah..." the petals draw in and the Core tips back; "CHOO": it bucks forward, every panel flaps
    # (a tucked tip can only flap away from its petal), the disc jumps, the glow scatters; then it settles
    def sneeze(t):
        p, sc = Pose(), {}
        ah = anim.pulse(t, 0.0, 0.14, 0.0, 0.05)
        t0 = 0.14
        k = max(0.0, t - t0)
        jolt = math.exp(-k * 6.5) * anim.smooth(t0, t0 + 0.025, t) * (1 - anim.smooth(0.6, 0.8, t))
        fl = lambda n, f, ph=0.0: math.sin(math.tau * f * k + phase[n] + ph)
        _petals(A, p, lambda n: 1 + (-10 * ah + 22 * jolt * fl(n, 8.5)) / A[n],
                lambda n: 1 - (15 * ah + 32 * jolt * (0.5 + 0.5 * fl(n, 8.5, 0.8))) / A[n + "_tip"],
                1 - (15 * ah + 36 * jolt * (0.5 + 0.5 * math.sin(math.tau * 8.5 * k + 2.0))) / A["cap"])
        p.set("base", -5 * ah + 15 * jolt * math.cos(math.tau * 5.5 * k), 0,
              6 * jolt * math.sin(math.tau * 4.5 * k + 0.4))
        disc(p, sc, 1 - 0.3 * ah + 0.9 * jolt * abs(math.cos(math.tau * 5 * k)), 1.0,
             55 * jolt * math.sin(math.tau * 3 * k), 1.0)
        p.set("dial", 0, 50 * jolt * math.sin(math.tau * 6 * k), 0)
        h = sc["holo"]
        f = 1 - 0.25 * ah + 0.6 * jolt * math.sin(math.tau * 11 * k)
        g = 1 + 0.07 * jolt * math.sin(math.tau * 9 * k + 1)    # wide enough to scatter, not to hit the dial
        sc["holo"] = (h[0] * g, h[1] * max(0.2, f), h[2] * g)
        return p, sc
    make("sneeze", 0.8, sneeze)

    # wont-open: click, a fizzle of a glint, the petals strain and judder and stick; a harder try, the cap
    # rattling; it clamps shut and rattles, and one petal pops up a crack and slams again
    def wont(t):
        p, sc = Pose(), {}
        press = anim.pulse(t, 0.0, 0.04, 0.03, 0.08)
        p.move("lens", y=-0.0022 * press - 0.0018 * anim.pulse(t, 0.6, 0.03, 0.02, 0.06))
        _glint(p, sc, t, 0.06, 0.3, 0.1)
        s1 = anim.smooth(0.12, 0.42, t) * (1 - anim.smooth(0.48, 0.58, t))
        s2 = anim.smooth(0.6, 0.82, t) * (1 - anim.smooth(0.86, 0.9, t))
        lift = {"HH": 1.0, "HU": 0.75}
        for name, sp in PETALS.items():
            j = math.sin(math.tau * 19 * t + phase[name])
            a = (6 + 2.2 * j) * s1 + (12 + 3.5 * j) * s2
            if name == "petal_4":                 # the one that pops up again after it's clamped
                a += 7 * anim.pulse(t, 1.1, 0.05, 0.05, 0.03)
            p.set(name, max(0.0, a * lift[sp["kind"]]))
        p.set("cap", max(0.0, (9 + 4 * math.sin(math.tau * 23 * t)) * s2))
        k = max(0.0, t - 0.9)
        rattle = 3.2 * math.exp(-k * 7) * (t > 0.9) * (1 - anim.smooth(1.3, 1.5, t))
        p.set("base", (1.2 * s1 + 2.0 * s2) * math.sin(math.tau * 13 * t) + rattle * math.sin(math.tau * 9 * k),
              0, (1.5 * s1 + 2.5 * s2) * math.sin(math.tau * 14 * t + 1) + rattle * math.cos(math.tau * 7 * k))
        return p, sc
    make("wont-open", 1.5, wont)

    # pop-open: a delicate tap, a ding, and everything springs open at once
    def pop(t):
        p, sc = Pose(), {}
        tap = anim.pulse(t, 0.0, 0.03, 0.0, 0.06)
        p.set("base", 2.5 * tap, 0, 0)
        p.move("lens", y=-0.0018 * tap)
        _glint(p, sc, t, 0.03, 0.8, 0.14)
        _petals(A, p, lambda n: _e("back", 0.06 + 0.006 * order[n], 0.22, t),
                lambda n: _e("land", 0.09 + 0.006 * order[n], 0.3, t), _e("land", 0.12, 0.3, t))
        rings = 1.0 if t < 0.02 else 0.0 if t < 0.14 else _e("out", 0.14, 0.26, t)
        spin_up = -60 * (1 - _e("out", 0.1, 0.4, t)) * anim.smooth(0, 0.05, t)
        disc(p, sc, _e("back", 0.12, 0.2, t), rings, spin_up, _e("back", 0.16, 0.26, t))
        return p, sc
    make("pop-open", 0.5, pop)
    return out


# ---------------------------------------------------------------------------------------------- views
def main():
    _look_arg()
    geo.reset()
    R, parts, M = build()
    meshes = R.finalize(parts)
    body = meshes["body"]
    tris = sum(len(p.vertices) - 2 for p in body.data.polygons)
    print(f"CORE bones={len(R.order)} verts={len(body.data.vertices)} tris={tris}")
    skel = anim.Skeleton(R.ob)
    cl = {c.name: c for c in clips(R)}
    glb = None
    if "--glb" in ARGS:
        given = opt("--glb")
        glb = Path(given) if given and not given.startswith("--") else SITE_GLB
    if glb or "--bake" in ARGS:
        for c in cl.values():
            bake(c, skel)
            print(f"CORE clip {c.name} {c.seconds:.2f}s")
    if glb:
        raw = export.glb(Path(tempfile.gettempdir()) / "core.raw.glb", [R.ob, body], image_quality=80)
        export.compress(raw, glb)
        print(f"CORE glb {glb}: raw={raw.stat().st_size} compressed={glb.stat().st_size}")
        if "--keep-raw" not in ARGS:
            raw.unlink()
    if R.ob.animation_data:
        R.ob.animation_data.use_nla = False       # stills pose the rig directly
    state = opt("--state", "closed")
    if state == "open":
        apply(SClip("open", 0.1).key(0, open_pose(R)).scaling(lambda t: open_scales()), skel, 0.0)
    elif state in cl:
        apply(cl[state], skel, float(opt("--t", "0")))
    save = opt("--save")
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(save).resolve()), compress=True)
    if "--no-render" in ARGS:
        return
    out = Path(opt("--out", str(HERE / "renders"))).resolve()
    out.mkdir(parents=True, exist_ok=True)
    res = tuple(int(x) for x in opt("--res", "900x900").split("x"))
    views = opt("--views", "closed").split(",")
    tag = state if "--t" not in ARGS else f"{state}-{float(opt('--t')):.2f}"
    render_views(out, [v for v in views if v != "strip"], int(opt("--samples", "48")), res, tag)
    if "strip" in views:
        strip(out, cl[opt("--strip", "unfold")], skel, int(opt("--every", "6")), int(opt("--samples", "48")))


def strip(out, clip, skel, every, samples):
    """A contact strip of `clip`, a frame every `every` frames, seen from a three-quarter camera."""
    frames = list(range(0, clip.frames + 1, every))
    if frames[-1] != clip.frames:
        frames.append(clip.frames)
    tiles = []
    for f in frames:
        apply(clip, skel, f / clip.fps)
        path = render_views(out / "strip", ["strip"], samples, (420, 420), f"{clip.name}-f{f:02d}")[0]
        img = bpy.data.images.load(str(path))
        w, h = img.size
        tiles.append(np.array(img.pixels[:], np.float32).reshape(h, w, 4))
        bpy.data.images.remove(img)
    row = np.concatenate(tiles, axis=1)
    img = bpy.data.images.new(f"strip-{clip.name}", row.shape[1], row.shape[0], alpha=True)
    img.pixels.foreach_set(row.ravel())
    img.filepath_raw = str(out / f"core-strip-{clip.name}.png")
    img.file_format = "PNG"
    img.save()
    print(f"CORE strip {img.filepath_raw}")


def lights():
    """The sheet's studio: a dark charcoal room, a warm key high on the left, a cool fill, a warm rim behind,
    and a dark floor to catch the shadow."""
    f = V(0, 0, 0)
    studio.area("key", 27, (-0.5, -0.6, 0.7), f, 0.5, (1.0, 0.92, 0.82))
    studio.area("fill", 7, (0.75, -0.45, 0.25), f, 0.7, (0.82, 0.9, 1.0))
    studio.area("rim", 30, (0.4, 0.7, 0.45), f, 0.35, (1.0, 0.86, 0.68))
    studio.area("top", 6, (0.0, 0.1, 0.9), f, 0.6, (1.0, 1.0, 1.0))
    studio.world((0.018, 0.019, 0.023), 1.0)
    me = bpy.data.meshes.new("floor")
    h = 30.0
    me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new("floor", me)
    geo.link(ob)
    ob.location.z = -RADIUS - 0.0005
    me.materials.append(mat.principled("floor", "#16171a", rough=0.5, spec=0.25))


CAMERAS = {           # name: (focus, angle round from the front, distance, height, lens)
    "closed": (V(0, 0, 0.0), -40, 0.78, 0.18, 85),
    "closed-b": (V(0, 0, 0.0), 150, 0.78, 0.42, 85),
    "front": (V(0, 0, 0.0), 0, 0.8, 0.05, 85),
    "open": (V(0, 0, 0.01), -22, 0.95, 0.5, 85),
    "open-top": (V(0, 0, 0.01), -8, 0.62, 0.95, 85),
    "open-front": (V(0, 0, 0.02), 0, 1.0, 0.22, 85),
    "open-back": (V(0, 0, 0.0), 160, 0.95, 0.12, 85),
    "strip": (V(0, 0, 0.01), -22, 1.12, 0.6, 85),
}


def render_views(out, views, samples, res, state):
    if not bpy.data.objects.get("key"):
        lights()
    studio.settings(res=res, samples=samples, engine="CYCLES", exposure=float(opt("--exposure", "-1.1")))
    bpy.context.scene.view_settings.view_transform = opt("--view", "Standard")
    tone = opt("--tone")
    if tone:
        bpy.context.scene.view_settings.look = tone
    paths = []
    for v in views:
        focus, ang, dist, height, lens = CAMERAS[v]
        cam = studio.camera(f"cam-{v}", focus, ang, dist, height=height, lens=lens)
        studio.aim(cam, focus)
        bpy.context.scene.camera = cam
        paths.append(studio.render(Path(out) / f"core-{v}-{state}.png"))
    return paths


if __name__ == "__main__":
    main()
