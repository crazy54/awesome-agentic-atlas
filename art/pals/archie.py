"""Archie, as drawn on his model sheet: built, rigged and skinned from nothing but this script.

    blender -b --factory-startup --python art/pals/archie.py -- [--views front,side,back,three,face]
            [--out DIR] [--samples N] [--res WxH] [--sheet-pose] [--save PATH] [--no-render]

The reference is `Archie robot model reference sheet.png` (the sheets live outside the repository; their
landmarks are transcribed in art/pals/reference.md). Glazed ceramic white, graphite and lime: a broad, round
helmet of a head -- as wide as it is tall and deeper than either, an upright face plate on the front and a
ball of panels behind -- with big lime-iris eyes set into it, heavy brows (his right one arched high), the
sheet's lopsided smirk, and a graphite-and-lime pompadour swept up and over to his left; headphone cups for
ears, ceramic with a lime band; a graphite neck and spine; the Atlas Core's octagonal dock in his belly;
four-digit hands with brass knuckle rings; chunky sneakers.

Scale: the crest's tip stands 2.40 m up, the height of the Archie the homepage banner was framed for, so the
new one stands in the same pixels. One sheet pixel is 2.40 / 567 m; landmarks are sheet pixels put through
`Z` (front or side view, y down), `SY` (side view x) and plain metres across.

Budget: about 50k triangles, one skinned body mesh and one small face mesh (mouth and brows, which carry the
shape keys). Shells are smooth-shaded superquads at a resolution chosen per part rather than subdivided.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kit import face, geo, mat, rig, studio  # noqa: E402
from kit.geo import V, lerp, part, smooth  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    if flag in ARGS:
        return ARGS[ARGS.index(flag) + 1]
    return default


PX = 2.40 / 567                       # metres per sheet pixel
FLOOR_PX, SIDE_CX_PX = 632, 730


def SY(x):
    """Side-view sheet x pixel -> Y in metres (the side view faces screen right, which is -Y)."""
    return -(x - SIDE_CX_PX) * PX


def Z(y):
    return (FLOOR_PX - y) * PX


# ------------------------------------------------------------------------------------------ palette
def palette():
    ceramic_img = mat.specks("archie-ceramic", "#ebe5da", speck_hex="#8a735c", count=200, seed=11)
    P = dict(
        ceramic=mat.textured(mat.principled("ceramic", "#ebe5da", rough=0.24, coat=0.85, coat_rough=0.07),
                             ceramic_img),
        graphite=mat.principled("graphite", "#2b2a29", rough=0.42, coat=0.35, coat_rough=0.25, spec=0.45),
        rubber=mat.principled("rubber", "#1c1b1b", rough=0.78, spec=0.3),
        lime=mat.principled("lime", "#a4c812", rough=0.26, coat=0.85, coat_rough=0.05),
        steel=mat.principled("steel", "#a9a6a2", metal=1.0, rough=0.28, aniso=0.4),
        brass=mat.principled("brass", "#b8893f", metal=1.0, rough=0.32),
        lens=mat.principled("lens", "#121416", rough=0.08, coat=1.0, coat_rough=0.02, spec=0.8),
        mouth=mat.principled("mouth", "#26090c", rough=0.6, spec=0.3),
        teeth=mat.principled("teeth", "#f6f4ef", rough=0.18, coat=0.8),
        glint=mat.principled("glint", "#ffffff", rough=0.3, emit="#ffffff", strength=2.5),
        eye=mat.eye_material("archie-eye", inner_hex="#dcf55e", outer_hex="#77a40a", limbal_hex="#1a2604",
                             iris_r=0.285, pupil_r=0.185),
    )
    for m in P.values():
        m["pal"] = "archie"
    return P


# ------------------------------------------------------------------------------------------- build
REST_FACE = {"grin": 1.0}            # his everyday face: the sheet's open smirk

HIP_Z, KNEE_Z, ANKLE_Z = Z(400), Z(493), Z(580)
HIP_X, KNEE_X, ANKLE_X = 0.165, 0.19, 0.205
SHOULDER = V(0.335, 0.0, Z(280))
ELBOW = V(0.61, 0.0, Z(331))
WRIST = V(0.865, 0.0, Z(388))
HEAD_C = V(0.0, SY(734), Z(171))
HEAD_R = (0.25, 0.279, 0.24)                     # the skull's half width, half depth, half height
EYE_X, EYE_Z = 0.112, Z(180)                     # the eyes' centres across and up
EYE_R = 0.105                                    # eyeball radius (only a cap of it shows)
EYE_SINK = 0.0                                   # how far the eye's front sits under the face round it
SOCKET = (0.045, 0.07, 0.14)                     # socket depth, and the radii its wall starts and ends at
EAR_Y, EAR_Z = SY(708), Z(175)
MOUTH_Z = Z(204)                                 # the bottom of the smile's curve


def _skull_F(x, y, z):
    """The skull about HEAD_C, < 1 inside. Seen from above it is round, face and all; seen from the side the
    face is upright -- the forehead straight up to a tight turn on to a flat crown, the chin turning under
    more softly -- and the back of the head a ball. The jaw narrows to the chin, more at the front."""
    rx0, ry0, rz0 = HEAD_R
    zt = z / rz0
    below = max(0.0, -zt)
    fr = max(0.0, -y / ry0)
    rx = rx0 * (1 - 0.1 * below ** 2.2 - 0.22 * below ** 2.4 * fr ** 1.5)
    a = 2.1
    h = ((abs(x) / rx) ** a + (abs(y) / ry0) ** a) ** (1 / a)
    # How squarely each point faces forward (or back), seen from above: the upright face is the middle of
    # the front only, so that seen from the front the head keeps a round outline and full cheeks.
    c_f = max(0.0, -y / ry0) / max(h, 1e-6)
    c_b = max(0.0, y / ry0) / max(h, 1e-6)
    b = (2.5 + (lerp(3.0, 4.3, smooth(-0.2, 0.3, zt)) - 2.5) * smooth(0.35, 0.97, c_f)
         - 0.3 * smooth(0.2, 0.9, c_b))
    return h ** b + abs(zt) ** b


def _skull_r(d):
    """Distance from HEAD_C to the skull along the unit direction `d` (before the sockets)."""
    lo, hi = 0.0, 0.6
    for _ in range(32):
        k = (lo + hi) / 2
        lo, hi = (k, hi) if _skull_F(d.x * k, d.y * k, d.z * k) < 1 else (lo, k)
    return (lo + hi) / 2


def _face_y(x, z):
    """Y (relative to HEAD_C) of the skull's front at `x` across and `z` up from HEAD_C."""
    lo, hi = -0.6, 0.0
    for _ in range(40):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if _skull_F(x, m, z) < 1 else (m, hi)
    return (lo + hi) / 2


def eye_axis(sx):
    """Where the eye's socket meets the face (relative to HEAD_C), and the way it faces: out of the face,
    which is turning away towards the side there."""
    ez = EYE_Z - HEAD_C.z
    return V(sx * EYE_X, _face_y(EYE_X, ez), ez), V(sx * 0.32, -1, 0.02).normalized()


def _socket_r(q):
    """How far `q` (relative to HEAD_C) is from the nearer eye's axis."""
    best = 9.0
    for sx in (1, -1):
        e, n = eye_axis(sx)
        d = q - e
        best = min(best, (d - n * d.dot(n)).length)
    return best


def eye_centre(sx):
    e, n = eye_axis(sx)
    return HEAD_C + e - n * (EYE_R + EYE_SINK), n


def skull(M):
    """The head shell: a spherified cube put onto `_skull_F`, cut finer where the sockets' walls are, with
    the two sockets pressed in along the eyes' axes."""
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=17, use_grid_fill=True)
    axes = [eye_axis(sx) for sx in (1, -1)]

    def place(co):
        d = geo._spherify(co).normalized()
        return d * _skull_r(d)

    fine = set()
    for f in bm.faces:
        q = place(f.calc_center_median())
        if q.y < -0.1 and 0.035 < _socket_r(q) < 0.14:
            fine.update(f.edges)
    bmesh.ops.subdivide_edges(bm, edges=list(fine), cuts=2, use_grid_fill=True)
    sd, s0, s1 = SOCKET
    for v in bm.verts:
        q = place(v.co)
        if q.y < 0:
            for e, n in axes:
                d = q - e
                r = (d - n * d.dot(n)).length
                q -= n * (sd * (1 - smooth(s0, s1, r)) * smooth(0.0, 0.1, -q.y))
        v.co = HEAD_C + q
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    return geo.mesh_object("head-shell", bm, M["ceramic"])


def build():
    M = palette()
    R = rig.Rig("archie")
    parts = []

    def add(obs, bone):
        obs = obs if isinstance(obs, (list, tuple)) else [obs]
        part(obs, bone)
        parts.extend(obs)
        return obs[0] if len(obs) == 1 else obs

    def both(ob, bone=None):
        """`ob` is built on the character's left (+X); add it and its mirror image for the right."""
        if bone:
            part(ob, bone)
        parts.append(ob)
        parts.append(geo.mirror(ob))
        return ob

    # ---- skeleton ----------------------------------------------------------------------------------
    R.bone("root", (0, 0, 0), (0, 0.35, 0), z=(0, 0, 1))
    R.bone("hips", (0, 0, HIP_Z + 0.02), (0, 0, Z(365)), "root")
    R.bone("spine", (0, 0, Z(365)), (0, 0, Z(318)), "hips")
    R.bone("chest", (0, 0, Z(318)), (0, 0, Z(250)), "spine")
    R.bone("neck", (0, 0.0, Z(250)), (0, 0.0, Z(224)), "chest")
    R.bone("head", (0, 0.0, Z(224)), (0, 0.0, Z(150)), "neck")
    crest_path = [(-0.045, 736, 134), (-0.025, 750, 118), (0.01, 770, 96), (0.07, 792, 74), (0.125, 801, 57)]
    cp = [V(x, SY(px), Z(pz)) for x, px, pz in crest_path]
    R.bone("crest_1", cp[0], cp[1], "head", z=(0, -1, 0.3))
    R.bone("crest_2", cp[1], cp[3], "crest_1", z=(0, -1, 0.3))
    R.bone("crest_3", cp[3], cp[4], "crest_2", z=(0, -1, 0.3))
    for s, sx in rig.SIDES:
        R.bone(f"ear{s}", (sx * 0.27, EAR_Y, EAR_Z), (sx * 0.34, EAR_Y, EAR_Z), "head", z=(0, -1, 0))
    R.bone("core", (0, -0.11, Z(342)), (0, -0.23, Z(342)), "spine", z=(0, 0, 1))
    # The tether port low on his back (the end of his own tether, in "the invisible tug-of-war"). (The
    # back door's `hatch` bone is made with the door, below: it hangs on the plate's own edge.)
    R.bone("tether", (0, 0.17, Z(380)), (0, 0.27, Z(380)), "hips", z=(0, 0, 1))
    for s, sx in rig.SIDES:
        R.bone(f"shoulder{s}", (sx * 0.08, 0, Z(262)), (sx * SHOULDER.x, 0, SHOULDER.z), "chest")
        R.bone(f"upper_arm{s}", (sx * SHOULDER.x, 0, SHOULDER.z), (sx * ELBOW.x, 0, ELBOW.z), f"shoulder{s}")
        R.bone(f"forearm{s}", (sx * ELBOW.x, 0, ELBOW.z), (sx * WRIST.x, 0, WRIST.z), f"upper_arm{s}")
        R.bone(f"thigh{s}", (sx * HIP_X, 0, HIP_Z), (sx * KNEE_X, -0.005, KNEE_Z), "hips")
        R.bone(f"shin{s}", (sx * KNEE_X, -0.005, KNEE_Z), (sx * ANKLE_X, 0.03, ANKLE_Z), f"thigh{s}")
        R.bone(f"foot{s}", (sx * ANKLE_X, 0.03, ANKLE_Z), (sx * 0.222, -0.25, 0.075), f"shin{s}", z=(0, 0, 1))
        R.bone(f"toe{s}", (sx * 0.222, -0.25, 0.075), (sx * 0.222, -0.46, 0.075), f"foot{s}", z=(0, 0, 1))

    # ---- head --------------------------------------------------------------------------------------
    # The sheet's head is a broad ceramic helmet, as wide as it is tall and deeper than either, the face a
    # flat plate on the front of it and the back a ball of panels. The eyes are set into sockets in that
    # plate, so the shell is finer round them than elsewhere (see `skull`).
    skull_ob = add(skull(M), "head")
    geo.box_uv(skull_ob, 0.5)
    surf = geo.Surface(skull_ob)

    def on_skull(name, dirs, r=0.0042):
        """A seam: graphite laid just proud of the shell along the directions `dirs` (from HEAD_C)."""
        pts = [surf.toward(HEAD_C + d.normalized() * 0.6, HEAD_C, offset=0.0016) for d in dirs]
        pts = [p for p in pts if p is not None]
        if len(pts) > 2:
            add(geo.tube(name, pts, r, M["graphite"], segs=5), "head")

    def az_el(a, e):
        """A direction by azimuth round from the back of the head (+Y) towards his left, and elevation."""
        return V(math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))

    def chain(*pts, n=10):
        out = []
        for (a0, e0), (a1, e1) in zip(pts, pts[1:]):
            out += [az_el(lerp(a0, a1, i / n), lerp(e0, e1, i / n)) for i in range(n)]
        return out + [az_el(*pts[-1])]

    # The face plate's edge: up the temples just in front of the ear cups, over the top under the crest and
    # round under the jaw.
    fy = SY(749) - HEAD_C.y
    on_skull("face-seam", [V(math.cos(a) * 0.5, fy, math.sin(a) * 0.5) for a in
                           (math.tau * i / 72 for i in range(73))])
    # The back of the head, as on the sheet's back view: a hexagonal panel in the middle and the seams that
    # run from its corners to the crest, the ear cups and the neck.
    hexv = [(-0.3, 0.42), (0.3, 0.42), (0.47, 0.02), (0.3, -0.4), (-0.3, -0.4), (-0.47, 0.02), (-0.3, 0.42)]
    on_skull("head-seam-hex", chain(*hexv, n=8))
    for k, (a, b) in enumerate([((-0.3, 0.42), (-0.5, 0.85)), ((0.3, 0.42), (0.5, 0.85)),
                                ((0.47, 0.02), (1.05, 0.08)), ((-0.47, 0.02), (-1.05, 0.08)),
                                ((0.3, -0.4), (0.62, -0.85)), ((-0.3, -0.4), (-0.62, -0.85)),
                                ((0.75, 0.05), (0.95, 0.55)), ((-0.75, 0.05), (-0.95, 0.55))]):
        on_skull(f"head-seam{k}", chain(a, b, n=10))

    # Ear cups, layered on the X axis as on the head-profile panel: a ceramic housing with a lime band round
    # its front, a graphite face, a thin lime ring, the dark lens and a brass pin.
    for s, sx in rig.SIDES:
        c = V(sx * 0.258, EAR_Y, EAR_Z)
        ax = (sx, 0, 0)
        band = [c + V(sx * 0.037, -math.sin(a) * 0.101, math.cos(a) * 0.101)
                for a in (lerp(0.15, 2.95, i / 24) for i in range(25))]
        add([geo.disc(f"ear-housing{s}", 0.12, 0.072, M["ceramic"], c, ax, bevel_r=0.026, segs=40),
             geo.sweep(f"ear-lime{s}", band, 0.013, 0.006, M["lime"], segs=6, up=ax),
             geo.disc(f"ear-face{s}", 0.088, 0.03, M["graphite"], c + V(sx * 0.044, 0, 0), ax, bevel_r=0.012,
                      segs=36),
             geo.ring(f"ear-lime2{s}", 0.064, 0.0085, M["lime"], c + V(sx * 0.06, 0, 0), ax, segs=36, sides=6),
             geo.disc(f"ear-lens{s}", 0.055, 0.02, M["lens"], c + V(sx * 0.06, 0, 0), ax, bevel_r=0.008,
                      segs=32, bulge=0.008),
             geo.disc(f"ear-pin{s}", 0.018, 0.014, M["brass"], c + V(sx * 0.074, 0, 0), ax, segs=14)],
            f"ear{s}")

    # The crest: a pompadour, lofted from the sheet's side view. Each slice is an ellipse spanning the
    # crest's back edge to its front edge (sheet pixels, side view). Across the head, each slice's centre
    # and half-width are read off the front view (with the sheet's head tilt taken out): seen from the front
    # the crest is a swoosh, a long hollow slope from his right temple up to a tip over his left eye, and
    # a near-upright left side.
    across = [  # t, centre, half-width (metres, + his left)
        (0.0, -0.03, 0.2), (0.15, 0.01, 0.175), (0.3, 0.05, 0.135), (0.45, 0.085, 0.095), (0.6, 0.105, 0.067),
        (0.75, 0.12, 0.042), (0.88, 0.12, 0.02), (1.0, 0.11, 0.004)]
    edges = [  # t, back (x, y), front (x, y)
        (0.00, (681, 141), (792, 129)), (0.15, (698, 118), (802, 118)), (0.30, (716, 105), (809, 106)),
        (0.45, (735, 95), (813, 94)), (0.60, (755, 85), (813, 83)), (0.75, (774, 74), (810, 72)),
        (0.88, (790, 65), (806, 63)), (1.0, (801, 57), (802, 57))]
    def through(rows, t):
        """The rows' values at `t`, on a smooth curve through them (Catmull-Rom in each column)."""
        ts = [r[0] for r in rows]
        i = max(0, min(len(rows) - 2, next((k for k in range(len(ts) - 1) if t <= ts[k + 1]), len(ts) - 2)))
        f = (t - ts[i]) / (ts[i + 1] - ts[i])
        P = [rows[max(0, min(len(rows) - 1, k))][1:] for k in (i - 1, i, i + 1, i + 2)]
        return [0.5 * (2 * b + (-a + c) * f + (2 * a - 5 * b + 4 * c - d) * f * f + (-a + 3 * b - 3 * c + d) * f ** 3)
                for a, b, c, d in zip(*P)]

    flat = [(t, bx, by, fx, fy_) for t, (bx, by), (fx, fy_) in edges]
    rings, ring_n = [], 32
    for t in (1 - (1 - i / 20) ** 1.25 for i in range(21)):        # closer together towards the tip
        bx, by, fx, fy_ = through(flat, t)
        B, Fp = V(0, SY(bx), Z(by)), V(0, SY(fx), Z(fy_))
        u = (Fp - B)
        d = max(u.length / 2, 0.002)
        u = u.normalized() if u.length > 1e-6 else V(0, -1, 0)
        x0, w = through(across, t)
        w = max(w, 0.003)
        cb, cf = x0 + 0.015 * (1 - t), x0 - 0.025 * (1 - t)
        rings.append(((B + Fp) / 2, u, d, w, cb, cf, t))
    import bmesh as _bm
    bm = _bm.new()
    vrows = []
    for Cn, u, d, w, cb, cf, t in rings:
        row = []
        for j in range(ring_n):
            a = math.tau * j / ring_n
            ca, sa = math.cos(a), math.sin(a)
            # a superellipse, squarer across than along
            px = math.copysign(abs(ca) ** 0.8, ca) * d
            py = math.copysign(abs(sa) ** 0.7, sa) * w
            shear = lerp(cb, cf, (px / d + 1) / 2)
            co = Cn + u * px + V(1, 0, 0) * (py + shear)
            if t == 0.0:
                # the foot: dropped on to the skull and a little into it, so the crest sits down into the
                # head all round, however the crown falls away under its edges
                hit, _ = surf.cast((co.x, co.y, co.z + 1.0), (0, 0, -1))
                if hit is not None:
                    co = hit - V(0, 0, 0.022)
            row.append(bm.verts.new(co))
        vrows.append(row)

    def crest_lime(a, t):
        # The tip's front face, and a streak along each flank, kept to the loft's own lines so it runs
        # smoothly: low at the back of the foot, climbing to the tip (seen from the side, the sheet's
        # stripe rising along the crest; from behind, one up either side).
        a = math.atan2(math.sin(a), math.cos(a))           # -pi .. pi: his right flank is negative
        return (t > 0.36 and math.cos(a) > 0.74) or (t < 0.9 and 1.76 < abs(a) < 2.32)

    for (r0, r1), (_, _, _, _, _, _, t) in zip(zip(vrows, vrows[1:]), rings):
        for j in range(ring_n):
            f = bm.faces.new((r0[j], r0[(j + 1) % ring_n], r1[(j + 1) % ring_n], r1[j]))
            f.material_index = 1 if crest_lime(math.tau * (j + 0.5) / ring_n, t + 0.025) else 0
    tipv = bm.verts.new(sum((v.co for v in vrows[-1]), V(0, 0, 0)) / ring_n + V(0, -0.002, 0.004))
    for j in range(ring_n):
        f = bm.faces.new((vrows[-1][j], vrows[-1][(j + 1) % ring_n], tipv))
        f.material_index = 1
    basev = bm.verts.new(sum((v.co for v in vrows[0]), V(0, 0, 0)) / ring_n - V(0, 0, 0.05))
    for j in range(ring_n):
        bm.faces.new((vrows[0][(j + 1) % ring_n], vrows[0][j], basev))
    _bm.ops.recalc_face_normals(bm, faces=bm.faces[:])
    crest = geo.mesh_object("crest", bm, M["graphite"])
    crest.data.materials.append(M["lime"])
    zr0, zr1 = Z(141), Z(57)
    vgs = [crest.vertex_groups.new(name=f"crest_{i}") for i in (1, 2, 3)]
    for v in crest.data.vertices:
        t = (v.co.z - zr0) / (zr1 - zr0)
        w = [max(0.0, 1 - abs(t - c) / 0.4) + 1e-6 for c in (0.0, 0.5, 1.0)]
        tot = sum(w)
        for vg, x in zip(vgs, w):
            if x / tot > 1e-3:
                vg.add([v.index], x / tot, "REPLACE")
    parts.append(crest)

    # Eyes, set into the sockets, gazing straight out. The eyeball is bigger than the socket's mouth, so only
    # a shallow cap of it shows: wide open, a big lime iris and a big pupil, the heavy upper lid just over
    # the top of the iris.
    for s, sx in rig.SIDES:
        c, look = eye_centre(sx)
        R.bone(f"eye{s}", c, c + look * 0.08, "head", z=(0, 0, 1))
        R.bone(f"lid_up{s}", c, c + look * 0.07, "head", z=(0, 0, 1))
        R.bone(f"lid_lo{s}", c, c + look * 0.06, "head", z=(0, 0, 1))
        eparts, _ = face.eye(f"eye{s}", sx, c, EYE_R, look,
                             dict(eye=f"eye{s}", lid_up=f"lid_up{s}", lid_lo=f"lid_lo{s}", head="head"),
                             M["eye"], M["ceramic"], M["graphite"], M["glint"], lash=0.115, lash_flick=0.0,
                             up_open=43, lo_open=47, lid_roll=-4, res=10, lid_r=1.03, lash_span=0.95,
                             glint=(0.26, 0.42), glint_size=0.13, iris_up=0.076)
        parts.extend(eparts)
        # the lash line's wing, past the outer corner and up, on the face itself
        wing = [surf.front(sx * (EYE_X + dx), EYE_Z + dz, offset=0.003) for dx, dz in
                ((0.066, 0.04), (0.08, 0.044), (0.093, 0.052), (0.104, 0.064))]
        add(geo.sweep(f"eye-wing{s}", [p for p in wing if p], [0.011, 0.0095, 0.0065, 0.002],
                      [0.005, 0.0045, 0.0035, 0.0012], M["graphite"], segs=6, up=(0, -1, 0)), "head")

    # Brows: heavy graphite bars, rounded at the ends. His right one is the sheet's high, arched one; his
    # left sits lower and flatter, its inner end thick and turned up -- the smirk's eyebrow.
    brow_pts = {
        1: [(0.032, Z(146)), (0.07, Z(148)), (0.11, Z(149)), (0.15, Z(152)), (0.185, Z(158))],
        -1: [(-0.035, Z(141)), (-0.075, Z(134)), (-0.115, Z(131)), (-0.155, Z(134)), (-0.19, Z(141)),
             (-0.207, Z(149))],
    }

    def spline(pts, n=14):
        """A smooth curve through `pts` (Catmull-Rom), so a brow bends rather than kinks."""
        P = [pts[0]] + pts + [pts[-1]]
        out = []
        for i in range(1, len(P) - 2):
            for k in range(n // (len(pts) - 1) + (1 if i == len(P) - 3 else 0)):
                t = k / (n // (len(pts) - 1))
                a, b, c, d = P[i - 1], P[i], P[i + 1], P[i + 2]
                out.append(tuple(0.5 * (2 * b[j] + (-a[j] + c[j]) * t + (2 * a[j] - 5 * b[j] + 4 * c[j] - d[j]) * t * t
                                        + (-a[j] + 3 * b[j] - 3 * c[j] + d[j]) * t ** 3) for j in (0, 1)))
        return out

    for s, sx in rig.SIDES:
        pts2d = spline(brow_pts[sx])
        names = [f"brow_in{s}", f"brow_mid{s}", f"brow_out{s}"]
        for nm, (bx, bz) in zip(names, [pts2d[0], pts2d[2], pts2d[-1]]):
            p = surf.front(bx, bz)
            R.bone(nm, p, p + V(0, 0, 0.05), "head", z=(0, -1, 0))
        parts.append(face.brow(f"brow{s}", sx, surf, pts2d, 0.028, 0.018, M["graphite"], names,
                               taper=(1.2, 1.0, 0.45) if sx > 0 else (0.9, 1.0, 0.4), segs=12))

    # Mouth: rest is a closed, pleased smile; `grin` is the sheet's smirk and is on by default -- wide and
    # thin, his right corner higher and dimpled, only the left half open, over a strip of top teeth.
    shapes = dict(
        rest=dict(w=0.118, smile=0.02, thick=0.011, lift_R=0.012, hook_R=0.008),
        grin=dict(w=0.136, smile=0.012, lift_R=0.028, lift_L=0.005, hook_R=0.014, bot=0.036, open_a=-0.55,
                  open_b=0.93, teeth=0.42, thick=0.013, lip=0.0055),
        smile=dict(w=0.128, smile=0.036, bot=0.014, thick=0.011),
        wide=dict(w=0.148, smile=0.03, top=0.012, bot=0.064, teeth=0.3, low_teeth=0.12, round=0.3, lip=0.006),
        open=dict(w=0.09, smile=0.0, top=0.022, bot=0.05, round=0.6, teeth=0.18, lip=0.006),
        oh=dict(w=0.045, smile=0.0, top=0.03, bot=0.034, round=1.0, thick=0.007),
        frown=dict(w=0.105, smile=-0.03, thick=0.01),
        flat=dict(w=0.098, smile=0.0, thick=0.009),
        smirk_L=dict(w=0.118, smile=0.008, lift_L=0.042, lift_R=-0.006, hook_L=0.006, thick=0.01),
        smirk_R=dict(w=0.118, smile=0.008, lift_R=0.042, lift_L=-0.006, hook_R=0.006, thick=0.01),
        grit=dict(w=0.13, smile=-0.004, top=0.016, bot=0.018, teeth=0.5, low_teeth=0.5, thick=0.007, lip=0.004),
        ee=dict(w=0.142, smile=0.03, top=0.008, bot=0.024, teeth=0.55, low_teeth=0.3, lip=0.005),
    )
    mth = face.mouth("mouth", surf, (0.0, MOUTH_Z), shapes, (M["mouth"], M["teeth"]))
    mth.data.shape_keys.key_blocks["grin"].value = 1.0
    parts.append(mth)

    # Neck: a graphite spine, as on the sheet's head panels -- four ribbed segments up a core, each split
    # down the front into a left and a right half, narrowing a little towards the head.
    nz0, nz1 = Z(252), Z(214)
    add(geo.segment("neck-core", (0, 0, nz0 - 0.03), (0, 0, nz1 + 0.05), 0.058, M["graphite"], res=7), "neck")
    for i in range(4):
        z = lerp(nz0, nz1, (i + 0.5) / 4)
        k = 1 - 0.05 * i
        for sx in (1, -1):
            add(geo.superquad(f"neck-rib{i}{'_L' if sx > 0 else '_R'}", (0.037 * k, 0.066 * k, 0.017),
                              M["graphite"], (sx * 0.039 * k, 0.004, z), n=(2.6, 2.4, 2.2), res=4,
                              shape=lambda p, q: Vector((p.x, p.y - 0.008 * max(0.0, -q.y) * (1 - abs(q.z)), p.z))),
                "neck" if i else "chest")

    # ---- torso -------------------------------------------------------------------------------------
    CH_C = V(0, -0.025, Z(279))
    BAY_FLOOR = Z(318)                    # the ledge in the bay behind his back door (the fake crash)
    DOOR = 1                              # which back plate is the door: his left (+1), clear of a raised right arm

    def chest_shape(p, q):
        # Wide at the shoulders, tapering to the waist; pecs forward, the back flatter.
        t = (q.z + 1) / 2                       # 0 bottom .. 1 top
        sx = lerp(0.7, 1.0, smooth(0.0, 0.7, t))
        p = Vector((p.x * sx, p.y, p.z))
        if q.y < 0:
            p.y *= 1.0 + 0.12 * math.sin(math.pi * t) * (1 - 0.5 * abs(q.x))
        else:
            p.y *= 0.86
        return p

    # The torso is white plates over a graphite body, as on the sheet: the black shows at the V of the
    # collar, under the arms, down the spine and at the waist.
    TC = CH_C + V(0, 0.015, -0.02)

    def torso_shape(p, q):
        x = p.x * lerp(0.78, 1.0, smooth(-1, 0.6, q.z))
        # the bay behind his back door: the core's back pressed in there, out of sight while the door is shut
        z = TC.z + p.z
        bay = (smooth(0.07, 0.11, DOOR * x) * smooth(BAY_FLOOR - 0.03, BAY_FLOOR + 0.01, z) *
               (1 - smooth(Z(256) - 0.05, Z(256) - 0.01, z)) * smooth(0.15, 0.55, q.y))
        return Vector((x, p.y - 0.065 * bay, p.z))

    torso_core = add(geo.superquad("torso-core", (0.235, 0.175, 0.19), M["graphite"], TC, n=(2.5, 2.4, 2.6), res=14,
                                   shape=torso_shape), "chest")
    chest_base = geo.superquad("chest-base", (0.282, 0.226, 0.188), M["ceramic"], CH_C, n=(2.6, 2.4, 3.3),
                               shape=chest_shape, res=13)

    def chest_front(co):
        neck_v = Z(250) - 0.045 + 0.4 * abs(co.x)            # the V of the collar
        return min(CH_C.y + 0.075 - co.y,                     # the front three fifths
                   neck_v - co.z,
                   0.266 - abs(co.x) - 0.06 * max(0.0, co.z - CH_C.z) / 0.18)   # clear of the armpits

    chest, rims = geo.plate("chest-plate", chest_base, chest_front, M["ceramic"], thickness=0.03, rim=M["lime"],
                            rim_r=0.009)
    geo.box_uv(chest, 0.5)
    add(chest, "chest")
    add(rims, "chest")

    # The two back plates either side of the spine. One of them (DOOR's side) is a door, as nothing on the
    # sheet shows: it hangs on a hinge down its outer edge (the `hatch` bone runs up the hinge; turning it by
    # -DOOR about its Y swings the door open), and behind it is a little bay -- where, in "the fake crash",
    # Brick finds Zip at the controls.
    def chest_back(sx):
        return lambda co: min(co.y - (CH_C.y + 0.1), sx * co.x - 0.065, Z(256) - co.z, 0.258 - abs(co.x))

    for s, sx in rig.SIDES:
        back, brims = geo.plate(f"back-plate{s}", chest_base, chest_back(sx), M["ceramic"], thickness=0.03,
                                rim=M["lime"], rim_r=0.007)
        geo.box_uv(back, 0.5)
        door = sx == DOOR
        if door:
            edge = [back.matrix_world @ v.co for v in back.data.vertices if DOOR * v.co.x > 0.245]
            hinge = V(DOOR * (max(DOOR * v.x for v in edge) - 0.004), sum(v.y for v in edge) / len(edge) - 0.012, 0)
            R.bone("hatch", (hinge.x, hinge.y, min(v.z for v in edge)), (hinge.x, hinge.y, max(v.z for v in edge)),
                   "chest", z=(0, 1, 0))
        add(back, "hatch" if door else "chest")
        add(brims, "hatch" if door else "chest")
    csurf = geo.Surface(chest_base)
    bpy.data.objects.remove(chest_base)

    def on_chest(name, xz, r, bone="chest", offset=0.006):
        pts = [p for p in (csurf.front(x, z, offset=offset) for x, z in xz) if p is not None]
        return add(geo.tube(name, pts, r, M["lime"], segs=7), bone)

    # Lime piping across the pecs: a shallow chevron, and from its ends down and in to the waist.
    on_chest("chest-chevron", [(u * 0.23, Z(290) - 0.022 * (1 - abs(u)) ** 1.4 + 0.02 * abs(u) ** 3)
                               for u in (-1 + 2 * i / 26 for i in range(27))], 0.009)
    for sx in (1, -1):
        on_chest(f"chest-flank{'_L' if sx > 0 else '_R'}",
                 [(sx * lerp(0.232, 0.17, t), lerp(Z(291), Z(316), t)) for t in (i / 8 for i in range(9))], 0.008)

    # Graphite under-armour: the spine down the back, segmented.
    add(geo.segment("spine-back", (0, 0.14, Z(252)), (0, 0.14, Z(328)), 0.075, M["graphite"], flat=0.62, n=2.8,
                    res=7), "chest")
    for i in range(5):
        z = lerp(Z(258), Z(326), i / 4)
        add(geo.superquad(f"spine-plate{i}", (0.062, 0.024, 0.015), M["graphite"], (0, 0.166, z), n=2.6, res=3),
            "chest")

    # The bay behind the door: a matt back wall on the graphite core, a ledge along its foot (BAY_FLOOR: what
    # stands in it stands there), a column of status lights and two cable runs.
    tsurf = geo.Surface(torso_core)
    wall = tsurf.back(DOOR * 0.165, BAY_FLOOR + 0.12)
    add(geo.superquad("bay-wall", (0.075, 0.006, 0.105), M["rubber"], (DOOR * 0.165, wall.y, BAY_FLOOR + 0.12),
                      n=(3.4, 2.0, 3.4), res=5), "chest")
    add(geo.superquad("bay-ledge", (0.08, 0.024, 0.007), M["graphite"], (DOOR * 0.165, wall.y + 0.024, BAY_FLOOR + 0.004),
                      n=(3.0, 3.0, 2.4), res=4), "chest")
    # `bay`: the middle of the ledge's top, for the page to stand things on (a bone of its own, so it is wherever
    # the chest is; a joint, as every bone is, or the exporter would drop it)
    R.bone("bay", (DOOR * 0.165, wall.y + 0.024, BAY_FLOOR + 0.011), (DOOR * 0.165, wall.y + 0.024, BAY_FLOOR + 0.06), "chest",
           z=(0, 1, 0))
    # status lights up the spine side (the hinge side is behind the open door), two lime bars under them
    for i in range(3):
        add(geo.sphere(f"bay-light{i}", 0.006, M["lime"], (DOOR * 0.1, wall.y + 0.007, BAY_FLOOR + 0.15 + 0.022 * i),
                       res=3), "chest")
    for i in range(2):
        add(geo.superquad(f"bay-bar{i}", (0.022, 0.004, 0.0035), M["lime"],
                          (DOOR * 0.135, wall.y + 0.006, BAY_FLOOR + 0.1 + 0.016 * i), n=(3.0, 2.0, 2.4), res=3), "chest")
    for k, x in enumerate((DOOR * 0.12, DOOR * 0.205)):
        add(geo.tube(f"bay-cable{k}", [V(x, wall.y + 0.006, BAY_FLOOR + 0.22), V(x + DOOR * 0.01, wall.y + 0.01, BAY_FLOOR + 0.12),
                                         V(x - DOOR * 0.004, wall.y + 0.007, BAY_FLOOR + 0.02)], 0.005, M["graphite"], segs=5),
            "chest")
    # The tether port: a graphite socket with a lime ring, low on the back.
    tp = V(0, 0.16, Z(382))
    add([geo.disc("tether-port", 0.04, 0.04, M["graphite"], tp, (0, 1, 0), bevel_r=0.01, segs=20),
         geo.ring("tether-ring", 0.032, 0.006, M["lime"], tp + V(0, 0.02, 0), (0, 1, 0), segs=20, sides=6)], "hips")

    # Abdomen: graphite plates stacked like abs, narrowing downwards, and the Atlas Core's octagonal dock.
    AB_Z0, AB_Z1 = Z(370), Z(312)
    add(geo.segment("abdomen-core", (0, 0.0, AB_Z0 - 0.02), (0, 0.0, AB_Z1 + 0.03), 0.14, M["graphite"],
                    flat=0.85, n=2.4, res=8), "spine")
    for i in range(4):
        z = lerp(AB_Z0 + 0.02, AB_Z1 - 0.02, i / 3)
        rr = 0.15 - 0.016 * (3 - i)
        add(geo.superquad(f"abdomen-rib{i}", (rr, rr * 0.86, 0.024), M["graphite"], (0, 0.008, z), n=(2.4, 2.4, 3),
                          res=5, shape=lambda p, q: Vector((p.x, p.y, p.z - 0.012 * max(0.0, -q.y) * (1 - abs(q.x))))),
            "spine")
    dock_c = V(0, -0.128, Z(342))
    turn = Matrix.Translation(dock_c) @ Matrix.Rotation(math.pi / 8, 4, (0, 1, 0)) @ Matrix.Translation(-dock_c)
    frame = geo.lathe("dock-frame", geo.rounded_profile(0.118, 0.042, 0.012, r_inner=0.085), M["graphite"],
                      dock_c, (0, -1, 0), segs=8, y_hint=(0, 0, 1))
    add(geo.transform(frame, turn), "spine")
    well = geo.disc("dock-well", 0.088, 0.03, M["rubber"], dock_c + V(0, 0.018, 0), (0, -1, 0), segs=8)
    add(geo.transform(well, turn), "spine")
    add(geo.superquad("dock-clasp", (0.032, 0.018, 0.013), M["lime"], dock_c + V(0, -0.012, 0.11), n=2.6, res=4),
        "spine")

    # Pelvis: a ceramic brief with a lime waistband and a lime-edged panel in front; the big graphite hip
    # joints face forward and out, as on the sheet's front view.
    PV_C = V(0, 0.0, Z(392))

    def pelvis_shape(p, q):
        t = (q.z + 1) / 2
        sx = lerp(0.58, 1.0, smooth(0.0, 0.9, t))
        return Vector((p.x * sx, p.y * lerp(0.8, 1.0, t), p.z))

    pv_base = geo.superquad("pelvis-base", (0.222, 0.175, 0.122), M["ceramic"], PV_C, n=(2.5, 2.3, 2.4),
                            shape=pelvis_shape, res=12)
    pelvis, prims = geo.plate("pelvis-shell", pv_base, lambda co: (PV_C.z + 0.085) - co.z, M["ceramic"],
                              thickness=0.04, rim=M["lime"], rim_r=0.009)
    geo.box_uv(pelvis, 0.5)
    add(pelvis, "hips")
    add(prims, "hips")
    add(geo.superquad("pelvis-core", (0.17, 0.13, 0.05), M["graphite"], PV_C + V(0, 0, 0.08), n=2.6, res=6), "hips")
    psurf = geo.Surface(pv_base)
    bpy.data.objects.remove(pv_base)
    panel = [psurf.front(0.062 * math.sin(a), PV_C.z + 0.075 - 0.105 * math.cos(a * 0.9), offset=0.004)
             for a in (lerp(-1.5, 1.5, i / 20) for i in range(21))]
    add(geo.tube("pelvis-panel", [p for p in panel if p], 0.0075, M["lime"], segs=7), "hips")
    for s, sx in rig.SIDES:
        c = V(sx * 0.2, -0.045, HIP_Z - 0.005)
        ax = V(sx * 0.55, -0.83, 0).normalized()
        add([geo.disc(f"hip-joint{s}", 0.098, 0.07, M["graphite"], c, ax, bevel_r=0.022, segs=32),
             geo.ring(f"hip-ring{s}", 0.08, 0.009, M["graphite"], c + ax * 0.036, ax, segs=32, sides=6),
             geo.disc(f"hip-hub{s}", 0.05, 0.03, M["lens"], c + ax * 0.036, ax, bevel_r=0.008, segs=24, bulge=0.006),
             geo.ring(f"hip-lime{s}", 0.062, 0.0055, M["lime"], c + ax * 0.04, ax, segs=32, sides=6)], f"thigh{s}")

    # ---- legs and arms (built on the left, mirrored) -----------------------------------------------
    leg(M, both)
    arm(M, R, both)

    # The right side's hand bones, mirrored from the left ones `hand()` declared.
    for name in list(R.order):
        if not name.endswith("_L"):
            continue
        rn = name[:-2] + "_R"
        if rn in R.specs:
            continue
        sp = R.specs[name]
        par = sp["parent"]
        R.bone(rn, V(-sp["head"].x, sp["head"].y, sp["head"].z), V(-sp["tail"].x, sp["tail"].y, sp["tail"].z),
               geo.flip_name(par) if par else None, z=V(-sp["z"].x, sp["z"].y, sp["z"].z), deform=sp["deform"])

    R.build()
    return R, parts, M


def sleeve(name, a, b, ra, rb, M, cut=(0.1, 0.1), rims=(True, True), tilt=(None, None), bulge=0.06, front=0.0,
           flat=0.95, n=2.25, res=7, shape=None, core=0.62, y_hint=(0, 1, 0)):
    """A limb as the sheet draws one: a graphite core from `a` to `b` and over it a ceramic sleeve, its ends
    cut back (`cut` = fractions of the length at each end, `tilt` = an optional plane normal for a slanted
    cut) with lime piping round each open end that `rims` asks for. Returns the parts, untagged."""
    a, b = Vector(a), Vector(b)
    axis = (b - a).normalized()
    L = (b - a).length
    out = [geo.segment(f"{name}-core", a, b, ra * core, M["graphite"], rb=rb * core, n=2.2, res=4, y_hint=y_hint)]
    base = geo.segment(f"{name}-base", a, b, ra, M["ceramic"], rb=rb, bulge=bulge, front=front, flat=flat, n=n,
                       res=res, shape=shape, y_hint=y_hint)

    def field(co):
        s0 = (co - a).dot(Vector(tilt[0]).normalized() * -1 if tilt[0] else axis) - cut[0] * L
        s1 = (b - co).dot(Vector(tilt[1]).normalized() if tilt[1] else axis) - cut[1] * L
        return min(s0, s1)

    shell, tubes = geo.plate(name, base, field, M["ceramic"], thickness=0.022, rim=M["lime"], rim_r=0.0085)
    bpy.data.objects.remove(base)
    geo.box_uv(shell, 0.5)
    out.append(shell)
    for tb in tubes:
        c = sum((v.co for v in tb.data.vertices), Vector()) / max(1, len(tb.data.vertices))
        end = 0 if (c - a).dot(axis) < L / 2 else 1
        if rims[end]:
            out.append(tb)
        else:
            bpy.data.objects.remove(tb)
    return out


def leg(M, both):
    s, sx = "_L", 1
    hip = V(sx * HIP_X, 0, HIP_Z)
    knee = V(sx * KNEE_X, -0.005, KNEE_Z)
    ankle = V(sx * ANKLE_X, 0.03, ANKLE_Z)
    # The thigh's sleeve: cut on a slant at the top (higher outside, round the hip joint), square above
    # the knee; lime at both ends.
    for ob in sleeve(f"thigh{s}", hip + V(sx * 0.016, 0, 0.02), knee + V(0, 0, 0.06), 0.14, 0.086, M,
                     cut=(0.08, 0.06), tilt=(V(-sx * 0.35, 0.0, 1.0), None), bulge=0.09, front=0.07, flat=0.93):
        both(ob, f"thigh{s}")
    # knee: a graphite hinge, lime rings either side, and a ceramic shield of a kneecap edged in lime
    both(geo.disc(f"knee-joint{s}", 0.078, 0.19, M["graphite"], knee, (1, 0, 0), bevel_r=0.03, segs=28), f"shin{s}")
    for k, off in enumerate((-1, 1)):
        both(geo.ring(f"knee-ring{k}{s}", 0.066, 0.0085, M["lime"], knee + V(off * 0.094, 0, 0), (1, 0, 0), segs=28,
                      sides=6), f"shin{s}")
    cap_base = geo.superquad(f"kneecap-base{s}", (0.094, 0.07, 0.118), M["ceramic"], knee + V(0, -0.075, 0.005),
                             n=(2.6, 2.0, 2.8), res=9)
    cap, crims = geo.plate(f"kneecap{s}", cap_base, lambda co: (knee.y - 0.065) - co.y, M["ceramic"], thickness=0.03,
                           rim=M["lime"], rim_r=0.008)
    bpy.data.objects.remove(cap_base)
    geo.box_uv(cap, 0.5)
    both(cap, f"shin{s}")
    for tb in crims:
        both(tb, f"shin{s}")
    # the shin's sleeve: a calf behind, lime at the top under the knee and at the ankle
    for ob in sleeve(f"shin{s}", knee + V(0, 0, -0.05), ankle + V(0, 0, 0.035), 0.102, 0.066, M, cut=(0.06, 0.05),
                     bulge=0.07, flat=0.95,
                     shape=lambda p, q: Vector((p.x, p.y + (0.045 * (1 - q.z * q.z) if q.y > 0 else 0), p.z))):
        both(ob, f"shin{s}")
    both(geo.disc(f"ankle-joint{s}", 0.066, 0.16, M["graphite"], ankle, (1, 0, 0), bevel_r=0.026, segs=24), f"foot{s}")
    both(geo.disc(f"ankle-disc{s}", 0.056, 0.03, M["graphite"], ankle + V(sx * 0.082, 0, 0), (sx, 0, 0),
                  bevel_r=0.01, segs=24), f"foot{s}")
    both(geo.ring(f"ankle-ring{s}", 0.044, 0.0065, M["lime"], ankle + V(sx * 0.098, 0, 0), (sx, 0, 0), segs=24,
                  sides=6), f"foot{s}")
    for ob in sneaker(s, sx, M):
        both(ob)


def arm(M, R, both):
    s, sx = "_L", 1
    sh_ = V(sx * SHOULDER.x, 0, SHOULDER.z)
    el = V(sx * ELBOW.x, 0, ELBOW.z)
    wr = V(sx * WRIST.x, 0, WRIST.z)
    up = (el - sh_).normalized()
    fw = (wr - el).normalized()
    # The shoulder: a big graphite joint of stepped rings, and over it a ceramic pauldron cut away
    # underneath, lime round its edge (the sheet's shoulder detail).
    jc = sh_ + V(sx * 0.03, 0, 0.0)
    both(geo.disc(f"shoulder-joint{s}", 0.09, 0.07, M["graphite"], jc, (sx, 0, 0), bevel_r=0.02, segs=32), f"upper_arm{s}")
    both(geo.ring(f"shoulder-ring{s}", 0.072, 0.008, M["graphite"], jc + V(sx * 0.037, 0, 0), (sx, 0, 0), segs=32,
                  sides=6), f"upper_arm{s}")
    both(geo.disc(f"shoulder-hub{s}", 0.045, 0.03, M["lens"], jc + V(sx * 0.036, 0, 0), (sx, 0, 0), bevel_r=0.008,
                  segs=24, bulge=0.006), f"upper_arm{s}")
    pad_c = sh_ + V(sx * 0.012, -0.005, 0.06)

    def pad_field(co):
        # keep the top and the outside; the cut line drops from high in front to low at the outer side
        out_ = sx * (co.x - pad_c.x)
        return (co.z - (pad_c.z - 0.035)) + 0.55 * max(0.0, out_) - 0.25 * max(0.0, -out_)

    pad_base = geo.superquad(f"pauldron-base{s}", (0.138, 0.14, 0.125), M["ceramic"], pad_c, n=2.25, res=9)
    pad, pr = geo.plate(f"pauldron{s}", pad_base, pad_field, M["ceramic"], thickness=0.028, rim=M["lime"],
                        rim_r=0.0105)
    bpy.data.objects.remove(pad_base)
    geo.box_uv(pad, 0.5)
    both(pad, f"upper_arm{s}")
    for tb in pr:
        both(tb, f"upper_arm{s}")
    for ob in sleeve(f"upper-arm{s}", sh_ + up * 0.05, el - up * 0.02, 0.082, 0.068, M, cut=(0.08, 0.1),
                     rims=(False, True), bulge=0.08, y_hint=(0, 0, 1)):
        both(ob, f"upper_arm{s}")
    both(geo.disc(f"elbow-joint{s}", 0.068, 0.14, M["graphite"], el, (0, 1, 0), bevel_r=0.024, segs=24), f"forearm{s}")
    for k, off in enumerate((-1, 1)):
        both(geo.ring(f"elbow-ring{k}{s}", 0.058, 0.0075, M["lime"], el + V(0, off * 0.07, 0), (0, 1, 0), segs=24,
                      sides=6), f"forearm{s}")
    for ob in sleeve(f"forearm{s}", el + fw * 0.035, wr - fw * 0.02, 0.095, 0.074, M, cut=(0.1, 0.1), bulge=0.07,
                     flat=0.93, y_hint=(0, 0, 1),
                     shape=lambda p, q: Vector((p.x * (1 + 0.08 * max(0.0, -q.z)), p.y, p.z))):
        both(ob, f"forearm{s}")
    both(geo.disc(f"wrist-joint{s}", 0.05, 0.06, M["graphite"], wr, fw, bevel_r=0.013, segs=20), f"hand{s}")
    for ob in hand(R, s, sx, wr, fw, M):
        both(ob)


def sneaker(s, sx, M):
    """A chunky sneaker: graphite tread, lime midsole, a ceramic upper with lime side panels, graphite laces."""
    out = []
    fx = sx * 0.228
    L0, L1 = 0.19, -0.49                       # heel and toe, Y
    cy = (L0 + L1) / 2
    hl = (L0 - L1) / 2

    def sole_shape(p, q):
        t = (q.y + 1) / 2                       # 0 toe .. 1 heel
        w = lerp(0.86, 1.0, smooth(0.0, 0.6, t))
        z = p.z + (0.03 * smooth(0.25, 0.0, t) if q.z > -0.5 else 0.024 * smooth(0.2, 0.0, t))
        return Vector((p.x * w, p.y, z))

    tread = geo.superquad(f"shoe-tread{s}", (0.166, hl, 0.024), M["rubber"], (fx, cy, 0.024), n=(3.0, 3.2, 3.0),
                          shape=sole_shape, res=7)
    out.append(part(tread, f"foot{s}"))
    mid = geo.superquad(f"shoe-mid{s}", (0.172, hl - 0.006, 0.036), M["lime"], (fx, cy, 0.074), n=(3.0, 3.0, 2.6),
                        shape=sole_shape, res=7)
    out.append(part(mid, f"foot{s}"))

    def upper_shape(p, q):
        t = (q.y + 1) / 2                       # 0 toe .. 1 heel
        top = lerp(0.45, 1.0, smooth(0.15, 0.7, t))
        z = p.z * (top if q.z > 0 else 1.0)
        w = lerp(0.82, 1.0, smooth(0.0, 0.55, t)) * (1 - 0.1 * max(0.0, q.z))
        return Vector((p.x * w, p.y, z))

    upper = geo.superquad(f"shoe-upper{s}", (0.155, hl - 0.03, 0.115), M["ceramic"], V(fx, cy + 0.035, 0.168),
                          n=(2.4, 2.6, 2.2), shape=upper_shape, res=8)
    geo.box_uv(upper, 0.5)
    out.append(part(upper, f"foot{s}"))
    us = geo.Surface(upper)
    for side in (1, -1):
        sw = []
        for i in range(16):
            t = i / 15
            y = lerp(L0 - 0.06, L1 + 0.17, t)
            z = lerp(0.215, 0.115, t) + 0.028 * math.sin(math.pi * t)
            p = us.side(y, z, s=side * (1 if sx > 0 else -1), offset=0.003)
            if p is not None:
                sw.append(p)
        if len(sw) > 3:
            r = [0.014 + 0.024 * math.sin(math.pi * k / (len(sw) - 1)) for k in range(len(sw))]
            out.append(part(geo.sweep(f"shoe-panel{side}{s}", sw, [0.006] * len(sw), r, M["lime"], segs=8, up=(0, 0, 1)),
                            f"foot{s}"))
    for k, y in enumerate(lerp(-0.06, -0.28, i / 4) for i in range(5)):
        p = us.cast(V(fx, y, 1.0), V(0, 0, -1))[0]
        if p is not None:
            out.append(part(geo.superquad(f"shoe-lace{k}{s}", (0.075 - 0.006 * k, 0.013, 0.011), M["graphite"],
                                          p + V(0, 0, 0.006), n=2.6, res=3), f"foot{s}"))
    out.append(part(geo.superquad(f"shoe-tongue{s}", (0.065, 0.055, 0.045), M["graphite"], V(fx, -0.02, 0.255),
                                  n=2.4, res=5), f"foot{s}"))
    out.append(part(geo.ring(f"shoe-collar{s}", 0.092, 0.02, M["graphite"], V(fx, 0.065, 0.272), (0, 0.25, 1),
                             segs=28, sides=8, squash=0.8), f"foot{s}"))
    return out


def hand(R, s, sx, wrist, fw, M):
    """A hand at the end of the forearm: a ceramic back with a lime band at the wrist, a graphite palm, and
    four graphite digits (thumb and three fingers) of three segments, brass rings at the knuckles. Declares
    the hand's bones on `R` as it goes. As on the sheet the palm faces back (+Y), so the thumb is on the edge
    nearer the body."""
    out = []
    along = fw.normalized()
    palm_n = V(0, 1, 0)
    palm_n = (palm_n - along * palm_n.dot(along)).normalized()
    across = along.cross(palm_n).normalized()          # over the back of the hand towards the thumb's edge
    if across.x * sx > 0:
        across = -across
    base = wrist + along * 0.03
    L = 0.17
    R.bone(f"hand{s}", base - along * 0.03, base + along * L, f"forearm{s}", z=palm_n)
    R.bone(f"grip{s}", base + along * 0.11 + palm_n * 0.07, base + along * 0.11 + palm_n * 0.07 + along * 0.06,
           f"hand{s}", z=palm_n)
    Mh = Matrix.Translation(base + along * (L / 2)) @ Matrix((across, palm_n, along)).transposed().to_4x4()
    back = geo.superquad(f"hand-back{s}", (0.092, 0.046, L / 2), M["ceramic"], (0, 0, 0), n=(2.6, 2.2, 2.8), res=7,
                         shape=lambda p, q: Vector((p.x * (1 - 0.12 * (1 - q.z) / 2), p.y, p.z)))
    geo.transform(back, Mh)
    geo.box_uv(back, 0.5)
    out.append(part(back, f"hand{s}"))
    palm = geo.superquad(f"hand-palm{s}", (0.086, 0.028, L / 2 - 0.006), M["graphite"], (0, 0, 0), n=2.6, res=5)
    out.append(part(geo.transform(palm, Mh @ Matrix.Translation((0, 0.026, 0))), f"hand{s}"))
    band = geo.superquad(f"hand-band{s}", (0.096, 0.05, 0.014), M["lime"], (0, 0, 0), n=2.8, res=4)
    out.append(part(geo.transform(band, Mh @ Matrix.Translation((0, -0.003, -L / 2 + 0.022))), f"hand{s}"))

    def digit(name, root, direction, lengths, radius):
        """Three rounded cylinders end to end, a thin brass collar at each knuckle and a domed tip."""
        d = direction.normalized()
        p = root.copy()
        parent = f"hand{s}"
        for k, ln in enumerate(lengths):
            bn = f"{name}_{k + 1}{s}"
            R.bone(bn, p, p + d * ln, parent, z=palm_n)
            r = radius * (1 - 0.06 * k)
            c = r * 0.22                                  # chamfer at the knuckle ends
            if k == len(lengths) - 1:
                prof = [(0.0, -c * 0.5), (r * 0.82, -c * 0.5), (r, c * 0.5)] + [
                    (r * math.cos(a), ln - r + r * math.sin(a)) for a in (math.pi / 2 * i / 6 for i in range(7))]
            else:
                prof = [(0.0, -c * 0.5), (r * 0.82, -c * 0.5), (r, c * 0.5), (r, ln - c), (r * 0.84, ln), (0.0, ln)]
            out.append(part(geo.lathe(f"{name}{k}{s}", prof, M["graphite"], p, d, segs=14, y_hint=palm_n), bn))
            if k:
                out.append(part(geo.ring(f"{name}-ring{k}{s}", r * 0.93, r * 0.12, M["brass"], p, d, segs=14, sides=4,
                                         squash=1.5), bn))
            p = p + d * ln
            parent = bn

    tip_c = base + along * L
    for k, nm, ln in ((-1.0, "index", 0.2), (0.0, "middle", 0.215), (1.0, "ring", 0.19)):
        root = tip_c - along * 0.02 + across * (0.058 * -k) + palm_n * 0.006
        d = (along + across * (-k * 0.12)).normalized()
        digit(nm, root, d, (ln * 0.38, ln * 0.33, ln * 0.29), 0.03)
    troot = base + along * 0.05 + across * 0.085 + palm_n * 0.024
    tdir = (along * 0.55 + across * 0.8 + palm_n * 0.25).normalized()
    digit("thumb", troot, tdir, (0.064, 0.056, 0.05), 0.033)
    return out


# ------------------------------------------------------------------------------------------- views
def sheet_pose(R):
    """The model sheet's stance: feet set wide, toes out."""
    R.rest()
    for s, sx in rig.SIDES:
        R.turn_world(f"thigh{s}", (0, 1, 0), -sx * 7.0)
        R.turn_world(f"foot{s}", (0, 1, 0), sx * 7.0)
        R.turn_world(f"foot{s}", (0, 0, 1), sx * 6.0)


def render_views(out, views, samples, res):
    focus = V(0, 0, 1.2)
    studio.sheet_lights(focus, 1.0)
    studio.floor(0.0)
    studio.settings(res=res, samples=samples, engine="CYCLES", view=opt("--view", "Standard"),
                    exposure=float(opt("--exposure", "-0.9")))
    for v in views:
        if v == "face":
            cam = studio.camera("cam-face", V(0, 0, 1.98), 0, 3.2, lens=110)
        elif v == "hand":
            cam = studio.camera("cam-hand", V(0.98, -0.02, 0.92), 20, 1.6, lens=110)
        elif v == "three":
            cam = studio.camera("cam-three", focus, 32, 9.0, lens=60)
        else:
            # "side" is the sheet's side view, which faces screen right: seen from the character's right.
            ang = {"front": 0, "side": -90, "back": 180, "left": 90, "right": -90}[v]
            cam = studio.camera(f"cam-{v}", focus, ang, 12.0, ortho=2.85)
        bpy.context.scene.camera = cam
        studio.render(Path(out) / f"archie-{v}.png")


def main():
    geo.reset()
    R, parts, M = build()
    meshes = R.finalize(parts)
    tris = sum(len(p.vertices) - 2 for m in meshes.values() for p in m.data.polygons)
    print(f"ARCHIE bones={len(R.order)} verts={ {k: len(v.data.vertices) for k, v in meshes.items()} } tris={tris}")
    if "--sheet-pose" in ARGS:
        sheet_pose(R)
    save = opt("--save")
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(save).resolve()), compress=True)
    if "--no-render" in ARGS:
        return
    out = Path(opt("--out", str(HERE / "renders"))).resolve()
    out.mkdir(parents=True, exist_ok=True)
    res = tuple(int(x) for x in opt("--res", "900x1200").split("x"))
    render_views(out, opt("--views", "front,side,back,three").split(","), int(opt("--samples", "64")), res)


if __name__ == "__main__":
    main()
