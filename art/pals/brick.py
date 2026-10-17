"""Brick, as drawn on his model sheet: built, rigged and skinned from nothing but this script.

    blender -b --factory-startup --python art/pals/brick.py -- [--views front,side,back,three,face,hand]
            [--out DIR] [--samples N] [--res WxH] [--sheet-pose] [--save PATH] [--no-render]

The reference is `Brick, the friendly orange robot.png` (the sheets live outside the repository; their
landmarks are transcribed in art/pals/reference.md). The big, gentle one: a hunched barrel of a chest in glossy,
worn orange plates with panel lines and rivets, cream-rimmed shoulder sockets on its flanks, a graphite belly
plate and round ports at its lower corners; a small head set low and forward in a graphite collar (cream face,
orange crown, orange ear cups, amber eyes half lidded, thick dark brows, a small closed smile); domed
pauldrons; cream upper arms, graphite elbows, massive orange gauntlets and four-digit hands with orange-plated
graphite fingers; thick orange thighs, graphite knees, greaves with cream plates, and blocky boots on graphite
soles.

Scale: his head's top stands 2.75 m up (1.22 times Archie's head, about twice as broad). On the sheet that top
is 500 px above the front view's floor line (y 600), so one sheet pixel is 2.75 / 500 m; landmarks are sheet
pixels put through `X` (front view x, centre line 285), `Z` (front or side view y, down) and `SY` (side view
x, centre line 770), or plain metres.

Budget: just under 80k triangles, one skinned body mesh and one small face mesh (mouth and brows, which carry
the shape keys). Shells are smooth-shaded superquads; colour regions are cut into them along exact curves
(`paint`), so a plate's edge is a clean line with a seam laid along it rather than a separate skin.

RIG. The shared skeleton, nothing added (62 bones, all deforming). Joints, left side (the right mirrors x):
shoulder pivot (0.84, 0.30, 2.05), elbow (1.00, 0.42, 1.60), wrist (1.17, 0.34, 1.10); hip (0.40, -0.07, 1.22),
knee (0.50, -0.02, 0.75), ankle (0.61, 0.20, 0.20), the ball of the foot at y -0.24 (the toe bone carries the
toe cap, the front sole and its tread, so the boot bends there); heel and toe tips at y +0.56 / -0.54. His
arms hang behind his middle (y +0.3 to +0.4): that is the hunch. The palm faces the thigh, turned about 24
degrees back, so the thumb is on the front edge; the fingers hang to z 0.51, about 1.6 m from the shoulder.
The pauldrons ride on `upper_arm_*` (hollow domes over the shoulder ball, so a raised arm carries its armour
with it); for raises past about 60 degrees shrug `shoulder_*` (+z) too, or the dome tips into the head's
reach. `grip_*` sits about 7 cm off the palm, two thirds of the way to the knuckles (left: (1.106, 0.367,
0.828), its Y along the fingers and Z out of the palm), which is where a held prop goes. Lids: the upper shuts
at x -27 (it is built half down), the lower at +36; brows ride `brow_in/mid/out_*` (y up, metres).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kit import face, geo, mat, rig, studio  # noqa: E402
from kit.geo import V, clamp, lerp, part, smooth  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    if flag in ARGS:
        return ARGS[ARGS.index(flag) + 1]
    return default


PX = 2.75 / 500                       # metres per sheet pixel
FLOOR_PX, FRONT_CX_PX, SIDE_CX_PX = 600, 285, 770


def X(x):
    """Front-view sheet x pixel -> X in metres (screen right is the character's left, +X)."""
    return (x - FRONT_CX_PX) * PX


def SY(x):
    """Side-view sheet x pixel -> Y in metres (the side view faces screen right, which is -Y)."""
    return -(x - SIDE_CX_PX) * PX


def Z(y):
    return (FLOOR_PX - y) * PX


# ------------------------------------------------------------------------------------------ palette
def palette():
    orange_img = mat.specks("brick-orange", "#e5671d", speck_hex="#f4d3a8", count=130, seed=21, mottle=0.045,
                            size=(1.0, 2.6))
    cream_img = mat.specks("brick-cream", "#e8d0b8", speck_hex="#a8774a", count=150, seed=22, mottle=0.03,
                           size=(0.9, 2.4))
    P = dict(
        orange=mat.textured(mat.principled("orange", "#e5671d", rough=0.24, coat=0.8, coat_rough=0.07), orange_img),
        cream=mat.textured(mat.principled("cream", "#e8d0b8", rough=0.3, coat=0.6, coat_rough=0.1), cream_img),
        graphite=mat.principled("graphite", "#2f2b28", rough=0.4, coat=0.35, coat_rough=0.22, spec=0.45),
        rubber=mat.principled("rubber", "#241b16", rough=0.7, spec=0.28),     # treads, seams, the collar's floor
        steel=mat.principled("steel", "#a9a6a2", metal=1.0, rough=0.3, aniso=0.4),
        brass=mat.principled("brass", "#c08a48", metal=1.0, rough=0.34),
        lens=mat.principled("lens", "#121214", rough=0.08, coat=1.0, coat_rough=0.02, spec=0.8),
        mouth=mat.principled("mouth", "#341a14", rough=0.6, spec=0.3),
        teeth=mat.principled("teeth", "#f6f2ea", rough=0.18, coat=0.8),
        glint=mat.principled("glint", "#ffffff", rough=0.3, emit="#ffffff", strength=2.5),
        eye=mat.eye_material("brick-eye", inner_hex="#eda22a", outer_hex="#a9580a", limbal_hex="#2a1304",
                             iris_r=0.25, pupil_r=0.105),
    )
    for m in P.values():
        m["pal"] = "brick"
    return P


# ---------------------------------------------------------------------------------------- helpers
def _root(fn, a, b, fa, fb, steps=6):
    """Where fn crosses zero on the segment a-b (as a fraction from a), by regula falsi."""
    lo, hi, flo, fhi = 0.0, 1.0, fa, fb
    t = fa / (fa - fb)
    for _ in range(steps):
        ft = fn(a.lerp(b, t))
        if ft == 0.0:
            return t
        if (ft < 0) == (flo < 0):
            lo, flo = t, ft
        else:
            hi, fhi = t, ft
        t = lo + (hi - lo) * flo / (flo - fhi) if flo != fhi else (lo + hi) / 2
    return t


def paint(ob, fn, m, recolour=True):
    """Give the part of `ob` where fn(co) < 0 the material `m`, first cutting its faces along fn = 0 so the
    colour change is a clean curve, not the grid's staircase. Returns the cut as polylines
    [(points, normals, closed)], for laying a seam along. `recolour=False` only cuts (a seam between two plates
    of one colour)."""
    me = ob.data
    names = [x.name for x in me.materials]
    if recolour and m.name not in names:
        me.materials.append(m)
        names.append(m.name)
    idx = names.index(m.name) if recolour else 0
    bm = bmesh.new()
    bm.from_mesh(me)
    val = {v: fn(v.co) for v in bm.verts}
    # Vertices lying almost on the curve move onto it, so the cut leaves no slivers.
    snap = {}
    for e in bm.edges:
        a, b = e.verts
        fa, fb = val[a], val[b]
        if (fa < 0) == (fb < 0):
            continue
        t = _root(fn, a.co, b.co, fa, fb)
        if t < 0.1:
            snap.setdefault(a, a.co.lerp(b.co, t))
        elif t > 0.9:
            snap.setdefault(b, a.co.lerp(b.co, t))
    for v, co in snap.items():
        v.co = co
        val[v] = 0.0
    for e in list(bm.edges):
        a, b = e.verts
        fa, fb = val[a], val[b]
        if fa == 0.0 or fb == 0.0 or (fa < 0) == (fb < 0):
            continue
        t = _root(fn, a.co.copy(), b.co.copy(), fa, fb)
        _, nv = bmesh.utils.edge_split(e, a, t)
        val[nv] = 0.0
    # Split every face the curve crosses between its two on-curve vertices.
    todo = list(bm.faces)
    while todo:
        f = todo.pop()
        vs = list(f.verts)
        n = len(vs)
        sg = [0 if val[v] == 0.0 else (1 if val[v] > 0 else -1) for v in vs]
        if not (1 in sg and -1 in sg):
            continue
        for i in range(n):
            if sg[i]:
                continue
            j = (i + 1) % n
            run = 0
            while sg[j] and j != i:
                run += 1
                j = (j + 1) % n
            if run and j != i:
                new, _ = bmesh.utils.face_split(f, vs[i], vs[j])
                todo.extend((f, new))
                break
    inside = set()
    for f in bm.faces:
        s = [val[v] for v in f.verts if val[v] != 0.0]
        if s and (max(s) < 0) != (min(s) < 0):
            ins = fn(f.calc_center_median()) < 0
        else:
            ins = (min(s) < 0) if s else fn(f.calc_center_median()) < 0
        if ins:
            inside.add(f)
            if recolour:
                f.material_index = idx
    bm.normal_update()
    edges = [e for e in bm.edges if len(e.link_faces) == 2 and
             (e.link_faces[0] in inside) != (e.link_faces[1] in inside)]
    adj = {}
    for e in edges:
        for v in e.verts:
            adj.setdefault(v, []).append(e)
    used, loops = set(), []
    for v0 in [v for v in adj if len(adj[v]) == 1] + list(adj):
        for e0 in adj[v0]:
            if e0 in used:
                continue
            path, e, v = [v0], e0, v0
            while e is not None:
                used.add(e)
                v = e.other_vert(v)
                path.append(v)
                nxt = [x for x in adj[v] if x not in used]
                e = nxt[0] if nxt else None
            closed = path[0] is path[-1]
            if closed:
                path = path[:-1]
            loops.append(([p.co.copy() for p in path], [p.normal.copy() for p in path], closed))
    bm.to_mesh(me)
    bm.free()
    me.update()
    return loops


def paint_faces(ob, pred, m):
    """Give the faces for which pred(centre, normal) holds the material `m` (no cut: for a boundary that
    already follows the mesh's rows, like a dome's lip)."""
    me = ob.data
    names = [x.name for x in me.materials]
    if m.name not in names:
        me.materials.append(m)
        names.append(m.name)
    idx = names.index(m.name)
    for poly in me.polygons:
        if pred(poly.center, poly.normal):
            poly.material_index = idx
    return ob


def disc(name, radius, depth, m, center, axis, bevel_r=None, r_inner=0.0, segs=24, bulge=0.0):
    """geo.disc with two steps to each rounded rim instead of four: the same silhouette for half the rings."""
    prof = geo.rounded_profile(radius, depth, bevel_r if bevel_r is not None else depth * 0.3, r_inner, steps=2,
                               front_bulge=bulge)
    return geo.lathe(name, prof, m, center, axis, segs=segs, caps=False)


def resample(pts, step):
    """Keep points at least `step` apart along a polyline (its ends kept)."""
    if len(pts) < 3:
        return list(range(len(pts)))
    keep, last = [0], pts[0]
    for i in range(1, len(pts) - 1):
        if (pts[i] - last).length >= step:
            keep.append(i)
            last = pts[i]
    keep.append(len(pts) - 1)
    return keep


def place(ob, M):
    """Bake M into a part's mesh, its faces kept outward should M mirror."""
    geo.transform(ob, M)
    if M.to_3x3().determinant() < 0:
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.reverse_faces(bm, faces=bm.faces[:])
        bm.to_mesh(ob.data)
        bm.free()
    return ob


def frame_on(surf, p, up=(0, 0, 1)):
    """The nearest surface point to `p` and a rotation whose Y is the surface normal there, Z leaning `up`."""
    loc, nor, _, _ = surf.tree.find_nearest(Vector(p))
    u = Vector(up)
    u = u - nor * u.dot(nor)
    if u.length < 1e-6:
        u = nor.orthogonal()
    zz = u.normalized()
    xx = nor.cross(zz)
    return loc, nor, Matrix((xx, nor, zz)).transposed()


class Kit:
    """The trim every plate gets: seams along its cuts and rivets in its corners, each riding on one bone."""

    def __init__(self, M):
        self.M = M
        self.n = 0

    def _name(self, what):
        self.n += 1
        return f"{what}{self.n}"

    def seams(self, loops, bone, r=0.0045, step=0.07, side=""):
        out = []
        for pts, nors, closed in loops:
            keep = resample(pts, step)
            if closed and len(keep) > 2 and keep[-1] == len(pts) - 1:
                keep = keep[:-1]
            if len(keep) < 2:
                continue
            ps = [pts[i] - nors[i] * r * 0.3 for i in keep]
            ob = geo.tube(self._name("seam") + side, ps, r, self.M["rubber"], segs=4, caps=not closed,
                          closed=closed)
            out.append(part(ob, bone))
        return out

    def seam(self, surf, guide, bone, r=0.0045, side="", toward=None, front=False, back=False):
        """A seam along guide points laid onto `surf`: front/back projections take (x, z) pairs, `toward`
        casts each 3D point towards toward(p), else each is pulled to the nearest surface point."""
        pts = []
        for g in guide:
            if front:
                p = surf.front(g[0], g[1], offset=-r * 0.3)
            elif back:
                p = surf.back(g[0], g[1], offset=-r * 0.3)
            elif toward is not None:
                p = surf.toward(g, toward(Vector(g)), offset=-r * 0.3, far=1.0)
            else:
                p = surf.nearest(g, offset=-r * 0.3)
            if p is not None:
                pts.append(p)
        if len(pts) < 2:
            return None
        return part(geo.tube(self._name("seam") + side, pts, r, self.M["rubber"], segs=4), bone)

    def rivet(self, surf, p, bone, r=0.013, m=None, side=""):
        loc, nor, _ = frame_on(surf, p)
        d = r * 0.45
        prof = [(0.0, -d), (r, -d), (r * 0.82, d * 0.7), (0.0, d)]
        return part(geo.lathe(self._name("rivet") + side, prof, m or self.M["brass"], loc, nor, segs=6), bone)


# ------------------------------------------------------------------------------------------- build
REST_FACE = {"smile": 1.0}           # his everyday face: the sheet's small closed smile

HIP = V(0.40, -0.07, 1.22)
KNEE = V(0.50, -0.02, 0.75)
ANKLE = V(0.61, 0.20, 0.20)
FOOT_X = 0.645
SHOULDER = V(0.84, 0.30, 2.05)
ELBOW = V(1.00, 0.42, 1.60)
WRIST = V(1.17, 0.34, 1.10)
HEAD_C = V(0.0, 0.03, Z(139))
HEAD_R = (0.335, 0.29, 0.215)                     # half width, half depth, half height
CH_C = V(0.0, 0.06, 1.89)
CH_R = (0.75, 0.54, 0.49)
SOCK = (0.14, 1.98)                               # (Y, Z) of the shoulder sockets' centre on the flanks
COLLAR_C = V(0.0, -0.04, 2.13)


def build():
    M = palette()
    R = rig.Rig("brick")
    parts = []
    T = Kit(M)

    def add(obs, bone=None):
        obs = obs if isinstance(obs, (list, tuple)) else [obs]
        obs = [o for o in obs if o is not None]
        if bone:
            part(obs, bone)
        parts.extend(obs)
        return obs[0] if len(obs) == 1 else obs

    def both(ob, bone=None):
        """`ob` is built on the character's left (+X); add it and its mirror image for the right."""
        if ob is None:
            return None
        for o in (ob if isinstance(ob, (list, tuple)) else [ob]):
            if bone:
                part(o, bone)
            parts.append(o)
            parts.append(geo.mirror(o))
        return ob

    # ---- skeleton ----------------------------------------------------------------------------------
    R.bone("root", (0, 0, 0), (0, 0.35, 0), z=(0, 0, 1))
    R.bone("hips", (0, -0.06, 1.15), (0, -0.04, 1.40), "root")
    R.bone("spine", (0, -0.04, 1.40), (0, 0.0, 1.65), "hips")
    R.bone("chest", (0, 0.0, 1.65), (0, 0.03, 2.22), "spine")
    R.bone("neck", (0, -0.03, 2.22), (0, 0.0, 2.36), "chest")
    R.bone("head", (0, 0.0, 2.36), (0, 0.03, 2.72), "neck")
    for s, sx in rig.SIDES:
        R.bone(f"ear{s}", (sx * 0.335, 0.19, 2.49), (sx * 0.445, 0.19, 2.49), "head", z=(0, -1, 0))
        R.bone(f"shoulder{s}", (sx * 0.30, 0.20, 2.12), (sx * SHOULDER.x, SHOULDER.y, SHOULDER.z), "chest")
        R.bone(f"upper_arm{s}", (sx * SHOULDER.x, SHOULDER.y, SHOULDER.z), (sx * ELBOW.x, ELBOW.y, ELBOW.z),
               f"shoulder{s}")
        R.bone(f"forearm{s}", (sx * ELBOW.x, ELBOW.y, ELBOW.z), (sx * WRIST.x, WRIST.y, WRIST.z), f"upper_arm{s}")
        R.bone(f"thigh{s}", (sx * HIP.x, HIP.y, HIP.z), (sx * KNEE.x, KNEE.y, KNEE.z), "hips")
        R.bone(f"shin{s}", (sx * KNEE.x, KNEE.y, KNEE.z), (sx * ANKLE.x, ANKLE.y, ANKLE.z), f"thigh{s}")
        R.bone(f"foot{s}", (sx * ANKLE.x, ANKLE.y, ANKLE.z), (sx * FOOT_X, -0.24, 0.1), f"shin{s}", z=(0, 0, 1))
        R.bone(f"toe{s}", (sx * FOOT_X, -0.24, 0.1), (sx * FOOT_X, -0.5, 0.1), f"foot{s}", z=(0, 0, 1))

    head(M, R, T, add)
    torso(M, T, add)
    leg(M, T, both)
    arm(M, R, T, both)

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

    # Box UVs for everything wearing a textured (specked) material.
    for ob in parts:
        if ob.type == "MESH" and not ob.data.uv_layers and any(m and m.get("textured") for m in ob.data.materials):
            geo.box_uv(ob, 1.0)
    R.build()
    return R, parts, M


# -------------------------------------------------------------------------------------------- head
def head(M, R, T, add):
    def head_shape(p, q):
        # A rounded box: the face flat and upright, the crown a touch narrower, the jaw square.
        above = max(0.0, q.z)
        p = Vector((p.x * (1 - 0.07 * above ** 2), p.y, p.z))
        if q.y < 0:
            p.y *= 0.94
        return p

    skull = add(geo.superquad("head-shell", HEAD_R, M["cream"], HEAD_C, n=(3.0, 2.6, 2.8), shape=head_shape,
                              res=13), "head")
    surf = geo.Surface(skull)

    # The crown: an orange cap from the brow line back over the top and down the back of the skull, in
    # three plates.
    def crown(p):
        zb = lerp(2.70, 2.56, clamp((p.y + 0.24) / 0.55))
        return max(zb - p.z, abs(p.x) - 0.25)

    add(T.seams(paint(skull, crown, M["orange"]), "head"))
    for sx in (1, -1):
        add(T.seam(surf, [V(sx * 0.165, lerp(-0.4, 0.45, i / 12), 3.2) for i in range(13)], "head", r=0.0035,
                   toward=lambda p: V(p.x, p.y, HEAD_C.z)))

    # Ear cups: an orange housing, a graphite ring, an orange ring and a graphite hub, layered on X.
    for s, sx in rig.SIDES:
        c = V(sx * 0.335, 0.19, 2.49)
        ax = (sx, 0, 0)
        add([disc(f"ear-housing{s}", 0.158, 0.12, M["orange"], c, ax, bevel_r=0.04, segs=28),
             disc(f"ear-ring{s}", 0.128, 0.03, M["graphite"], c + V(sx * 0.065, 0, 0), ax, bevel_r=0.012, segs=24),
             geo.ring(f"ear-orange{s}", 0.086, 0.017, M["orange"], c + V(sx * 0.08, 0, 0), ax, segs=28, sides=6,
                      squash=0.8),
             disc(f"ear-hub{s}", 0.067, 0.03, M["graphite"], c + V(sx * 0.08, 0, 0), ax, bevel_r=0.01, segs=24,
                  bulge=0.006),
             geo.ring(f"ear-orange2{s}", 0.042, 0.008, M["orange"], c + V(sx * 0.096, 0, 0), ax, segs=20, sides=6),
             disc(f"ear-lens{s}", 0.032, 0.012, M["lens"], c + V(sx * 0.096, 0, 0), ax, segs=16, bulge=0.004)],
            f"ear{s}")

    # Eyes, set into the face, gazing straight out, the lids half down.
    eye_r = 0.112
    for s, sx in rig.SIDES:
        ex, ez = sx * 0.17, Z(142)
        front = surf.front(ex, ez)
        c = V(ex, front.y + eye_r * 0.5, ez)
        look = V(sx * 0.03, -1, 0.0).normalized()
        R.bone(f"eye{s}", c, c + look * 0.1, "head", z=(0, 0, 1))
        R.bone(f"lid_up{s}", c, c + look * 0.09, "head", z=(0, 0, 1))
        R.bone(f"lid_lo{s}", c, c + look * 0.08, "head", z=(0, 0, 1))
        eparts, _ = face.eye(f"eye{s}", sx, c, eye_r, look,
                             dict(eye=f"eye{s}", lid_up=f"lid_up{s}", lid_lo=f"lid_lo{s}", head="head"),
                             M["eye"], M["cream"], M["graphite"], M["glint"], lash=0.17, lash_flick=0.3,
                             up_open=27, lo_open=36, lid_roll=-3, res=7)
        add(eparts)

    # Brows: thick dark bars, blunt at the inner end, arching over the eye to a tapered outer end.
    for s, sx in rig.SIDES:
        pts2d = [(sx * 0.06, Z(121.5)), (sx * 0.1, Z(119)), (sx * 0.15, Z(117.5)), (sx * 0.2, Z(118)),
                 (sx * 0.24, Z(120)), (sx * 0.272, Z(123.5))]
        names = [f"brow_in{s}", f"brow_mid{s}", f"brow_out{s}"]
        for nm, (bx, bz) in zip(names, [pts2d[0], pts2d[2], pts2d[-1]]):
            p = surf.front(bx, bz)
            R.bone(nm, p, p + V(0, 0, 0.05), "head", z=(0, -1, 0))
        add(face.brow(f"brow{s}", sx, surf, pts2d, 0.029, 0.017, M["graphite"], names, taper=(0.95, 1.0, 0.5)))

    # Mouth: `rest` a neutral closed line; `smile`, his everyday face, the sheet's small closed smile.
    shapes = dict(
        rest=dict(w=0.105, smile=0.01, thick=0.009),
        smile=dict(w=0.122, smile=0.022, thick=0.0095, lift_L=0.007),
        grin=dict(w=0.135, smile=0.03, top=0.004, bot=0.036, teeth=0.45, thick=0.009),
        wide=dict(w=0.145, smile=0.026, top=0.012, bot=0.06, teeth=0.32, low_teeth=0.12, round=0.3),
        open=dict(w=0.085, smile=0.0, top=0.02, bot=0.048, round=0.6, teeth=0.18),
        oh=dict(w=0.042, smile=0.0, top=0.028, bot=0.032, round=1.0, thick=0.007),
        frown=dict(w=0.1, smile=-0.026, thick=0.009),
        flat=dict(w=0.095, smile=0.0, thick=0.008),
        smirk_L=dict(w=0.11, smile=0.006, lift_L=0.034, lift_R=-0.004, thick=0.009),
        smirk_R=dict(w=0.11, smile=0.006, lift_R=0.034, lift_L=-0.004, thick=0.009),
        grit=dict(w=0.12, smile=-0.004, top=0.016, bot=0.018, teeth=0.5, low_teeth=0.5, thick=0.007),
        ee=dict(w=0.135, smile=0.026, top=0.008, bot=0.022, teeth=0.55, low_teeth=0.3),
    )
    mth = face.mouth("mouth", surf, (0.006, Z(164)), shapes, (M["mouth"], M["teeth"]))
    for k, v in REST_FACE.items():
        mth.data.shape_keys.key_blocks[k].value = v
    add(mth)

    # Neck: a short graphite column rising out of the collar.
    add(geo.segment("neck-core", COLLAR_C + V(0, 0, -0.05), (0, 0.02, 2.42), 0.13, M["graphite"], res=6), "neck")


# ------------------------------------------------------------------------------------------- torso
def torso(M, T, add):
    def chest_shape(p, q):
        # The front's top falls back to the collar (the hunch), the barrel's belly low and forward; a scoop
        # in the top for the collar the head sits in.
        if q.y < 0:
            p = Vector((p.x, p.y * (1 - 0.36 * smooth(0.05, 1.0, q.z)) * (1 - 0.2 * abs(q.x) ** 2.5), p.z))
        w = max(0.0, 1 - (abs(p.x) / 0.56) ** 4)
        g = smooth(0.32, 0.08, p.y)
        p.z -= 0.19 * w * g * smooth(0.15, 0.85, q.z)
        e = (p.x / 0.4) ** 2 + ((p.y + CH_C.y - COLLAR_C.y) / 0.32) ** 2      # the pit under the collar
        p.z -= 0.26 * smooth(1.0, 0.7, e) * smooth(0.3, 0.8, q.z)
        if q.z < 0:
            p.x *= 1 + 0.06 * smooth(-0.2, -0.9, q.z)
        return p

    chest = add(geo.superquad("chest-shell", CH_R, M["orange"], CH_C, n=(3.4, 2.6, 3.6), shape=chest_shape,
                              res=19), "chest")
    csurf = geo.Surface(chest)

    def sock_d(p):
        return math.hypot(p.y - SOCK[0], p.z - SOCK[1])

    # The flanks: cream rims round the shoulder sockets, graphite inside them.
    add(T.seams(paint(chest, lambda p: max(abs(sock_d(p) - 0.37) - 0.075, 0.45 - abs(p.x)), M["cream"]), "chest"))
    paint(chest, lambda p: max(sock_d(p) - 0.295, 0.45 - abs(p.x)), M["graphite"])   # its edge is the rim's seam

    # The belly: graphite under an arch, front, bottom and back.
    def arch(p):
        ax = abs(p.x)
        top = 1.73 - 0.07 * (ax / 0.37) ** 2
        side = 0.27 + 0.1 * clamp((p.z - 1.375) / 0.29)
        return max(p.z - top, ax - side)

    add(T.seams(paint(chest, arch, M["graphite"]), "chest"))
    # The spine's channel down the back.
    add(T.seams(paint(chest, lambda p: max(abs(p.x) - 0.13, 0.25 - p.y, 1.62 - p.z), M["graphite"]), "chest"))

    # Front plates: the breastplate between the yokes, the yokes, the lower bands over the belly.
    for sx in (1, -1):
        add(T.seam(csurf, [(sx * x, z) for x, z in ((0.44, 2.134), (0.31, 2.0), (0.275, 1.80))], "chest",
                   front=True))
        add(T.seam(csurf, [(sx * x, z) for x, z in ((0.70, 1.66), (0.55, 1.735), (0.40, 1.775), (0.275, 1.80))],
                   "chest", front=True))
        add(T.seam(csurf, [(sx * 0.2, 1.8), (sx * 0.205, 1.70)], "chest", front=True))
    add(T.seam(csurf, [(x, 1.80 + 0.006 * (1 - (x / 0.275) ** 2)) for x in (lerp(-0.275, 0.275, i / 12) for i in range(13))],
               "chest", front=True))
    for x, z in ((0.36, 2.08), (0.25, 1.86), (0.12, 1.86), (0.58, 1.95), (0.5, 1.72), (0.33, 1.76), (0.42, 2.2)):
        for sx in (1, -1):
            p = csurf.front(sx * x, z)
            if p is not None:
                add(T.rivet(csurf, p, "chest"))
    # Back plates.
    for sx in (1, -1):
        add(T.seam(csurf, [(sx * x, z) for x, z in ((0.13, 1.85), (0.3, 1.82), (0.5, 1.9))], "chest", back=True))
        add(T.seam(csurf, [(sx * x, z) for x, z in ((0.3, 2.3), (0.33, 2.1), (0.3, 1.82))], "chest", back=True))
        for x, z in ((0.22, 2.2), (0.4, 2.0), (0.22, 1.7), (0.45, 1.75)):
            p = csurf.back(sx * x, z)
            if p is not None:
                add(T.rivet(csurf, p, "chest"))
    # Vertebrae down the channel.
    for i in range(9):
        z = lerp(2.3, 1.62, i / 8)
        p = csurf.back(0.0, z)
        if p is None:
            continue
        add(geo.superquad(f"vertebra{i}", (0.125 - 0.02 * i / 8, 0.04, 0.032), M["graphite"], p + V(0, 0.012, 0),
                          n=(3.4, 2.6, 3.0), res=1), "chest")

    # Belly plates, raised on the graphite.
    for i, (x, z, hw, hh) in enumerate(((0.0, 1.6, 0.16, 0.065), (0.0, 1.48, 0.13, 0.045), (0.25, 1.61, 0.06, 0.075),
                                        (-0.25, 1.61, 0.06, 0.075))):
        loc, nor, rot = frame_on(csurf, csurf.front(x, z) or V(x, -0.4, z))
        add(geo.superquad(f"belly-plate{i}", (hw, 0.022, hh), M["graphite"], loc + nor * 0.006, n=(3.2, 2.4, 3.2),
                          res=2, rot=rot), "chest")
    for i, (x, z, hw, hh) in enumerate(((0.0, 1.6, 0.16, 0.065), (0.0, 1.48, 0.13, 0.045))):
        loc, nor, rot = frame_on(csurf, csurf.back(x, z) or V(x, 0.5, z))
        add(geo.superquad(f"back-plate{i}", (hw, 0.022, hh), M["graphite"], loc + nor * 0.006, n=(3.2, 2.4, 3.2),
                          res=2, rot=rot), "chest")

    # Ports at the chest's lower corners: a cream rim, a graphite well, a brass ring and a dark lens.
    for s, sx in rig.SIDES:
        loc = csurf.front(sx * 0.57, 1.56)
        if loc is None:
            continue
        nor = (csurf.normal_at(loc) + V(sx * 0.6, -0.1, 0)).normalized()
        add([disc(f"port-rim{s}", 0.125, 0.06, M["cream"], loc, nor, bevel_r=0.022, segs=24),
             disc(f"port-well{s}", 0.09, 0.05, M["graphite"], loc + nor * 0.02, nor, bevel_r=0.01, segs=24),
             geo.ring(f"port-ring{s}", 0.058, 0.011, M["brass"], loc + nor * 0.042, nor, segs=24, sides=6),
             disc(f"port-lens{s}", 0.045, 0.02, M["lens"], loc + nor * 0.04, nor, segs=20, bulge=0.006)],
            "chest")

    # Collar: a graphite ring set in a pit in the top of the barrel, tipped forward, a ribbed skirt rising
    # inside it to the neck.
    tilt = V(0, -0.4, 1).normalized()
    sq = Matrix.Diagonal((1.0, 0.8, 1.0, 1.0))
    TM = Matrix.Translation(COLLAR_C) @ geo.basis(tilt, (0, 1, 0)).to_4x4() @ sq
    skirt = [(0.0, -0.04), (0.35, -0.04), (0.35, 0.0), (0.27, 0.06), (0.17, 0.12), (0.12, 0.13), (0.0, 0.13)]
    for ob in (disc("collar", 0.44, 0.16, M["graphite"], (0, 0, 0), (0, 0, 1), bevel_r=0.03, r_inner=0.34, segs=36),
               geo.lathe("collar-skirt", skirt, M["rubber"], (0, 0, 0), (0, 0, 1), segs=28)):
        add(place(ob, TM), "chest")
    for i in range(12):
        a = math.tau * (i + 0.5) / 12
        rib = geo.sweep(f"collar-rib{i}", [V(0.33 * math.cos(a), 0.33 * math.sin(a), 0.012),
                                           V(0.16 * math.cos(a), 0.16 * math.sin(a), 0.122)],
                        0.016, 0.012, M["graphite"], n=3.0, segs=6, up=(0, 0, 1))
        add(place(rib, TM), "chest")

    # Abdomen: a graphite core between the barrel and the pelvis.
    add(geo.superquad("abdomen", (0.36, 0.3, 0.13), M["graphite"], (0, -0.02, 1.43), n=(2.6, 2.6, 2.4), res=6), "spine")

    # Pelvis: the cream girdle, wide at the waist and narrowing to the brief, plates and rivets.
    PV_C = V(0.0, -0.06, 1.18)

    def pelvis_shape(p, q):
        t = (q.z + 1) / 2
        sx = lerp(0.42, 1.0, smooth(0.1, 0.85, t))
        return Vector((p.x * sx, p.y * lerp(0.82, 1.0, t), p.z))

    pelvis = add(geo.superquad("pelvis-shell", (0.44, 0.3, 0.23), M["cream"], PV_C, n=(2.6, 2.8, 3.0),
                               shape=pelvis_shape, res=10), "hips")
    psurf = geo.Surface(pelvis)
    add(T.seam(psurf, [(x, 1.255 + 0.02 * abs(x) / 0.3 + 0.1 * smooth(0.28, 0.42, abs(x)))
                       for x in (lerp(-0.42, 0.42, i / 20) for i in range(21))], "hips", front=True))
    for sx in (1, -1):
        add(T.seam(psurf, [(sx * 0.13, 1.245), (sx * 0.125, 1.1), (sx * 0.115, 1.0)], "hips", front=True))
        for x, z in ((0.07, 1.2), (0.07, 1.04), (0.3, 1.3)):
            p = psurf.front(sx * x, z)
            if p is not None:
                add(T.rivet(psurf, p, "hips"))
    for s, sx in rig.SIDES:
        add(disc(f"hip-joint{s}", 0.15, 0.24, M["graphite"], V(sx * 0.32, -0.06, 1.21), (1, 0, 0), bevel_r=0.04,
                 segs=24), f"thigh{s}")
        d = V(sx * 0.45, 1.0, 0.0).normalized()
        hc = V(sx * 0.42, 0.2, 1.2)
        add([disc(f"hip-cap{s}", 0.145, 0.08, M["graphite"], hc, d, bevel_r=0.02, segs=28),
             disc(f"hip-hub{s}", 0.09, 0.04, M["graphite"], hc + d * 0.04, d, bevel_r=0.01, segs=24),
             geo.ring(f"hip-ring{s}", 0.07, 0.012, M["brass"], hc + d * 0.055, d, segs=24, sides=6)], "hips")


# -------------------------------------------------------------------------------------------- legs
def leg(M, T, both):
    s, sx = "_L", 1
    knee = KNEE

    # Thigh: a big orange shell, boxy along its length, plates seamed down its front.
    def thigh_shape(p, q):
        # The inner top cut back off the hip joint (local x is the leg's inner side, -z its top).
        if q.x > 0 and q.z < 0:
            p.z += 0.15 * smooth(0.0, 1.0, q.x) * smooth(0.0, -1.0, q.z)
        return p

    th = geo.segment(f"thigh{s}", V(0.44, -0.08, 1.31), V(0.50, -0.05, 0.80), 0.27, M["orange"], flat=0.93,
                     bulge=0.04, n=(2.8, 2.6, 3.2), res=10, shape=thigh_shape)
    tsurf = geo.Surface(th)
    tc = lambda p: V(0.47, -0.065, p.z)
    both(T.seam(tsurf, [V(0.43 + 0.03 * t, -0.4, lerp(1.27, 0.86, t)) for t in (i / 8 for i in range(9))], f"thigh{s}",
                toward=tc))
    both(T.seam(tsurf, [V(lerp(0.85, 0.43, t), lerp(-0.1, -0.4, t), lerp(1.12, 1.02, t)) for t in (i / 8 for i in range(9))],
                f"thigh{s}", toward=tc))
    both(T.seams(paint(th, lambda p: p.z - 0.9 + 0.04 * (p.y + 0.06), M["orange"], recolour=False), f"thigh{s}"))
    both(th, f"thigh{s}")
    for p in (V(0.36, -0.4, 1.16), V(0.6, -0.4, 0.95), V(0.62, -0.38, 1.2), V(0.8, 0.0, 1.05)):
        both(T.rivet(tsurf, p, f"thigh{s}"))

    # Knee: a graphite hinge with discs at both ends.
    both(disc(f"knee-joint{s}", 0.12, 0.3, M["graphite"], knee, (1, 0, 0), bevel_r=0.035, segs=24), f"shin{s}")
    for k, off in enumerate((-1, 1)):
        both(disc(f"knee-disc{k}{s}", 0.1, 0.04, M["graphite"], knee + V(off * 0.16, 0, 0), (off, 0, 0),
                  bevel_r=0.012, segs=22), f"shin{s}")
        both(geo.ring(f"knee-ring{k}{s}", 0.06, 0.01, M["brass"], knee + V(off * 0.18, 0, 0), (off, 0, 0), segs=18,
                      sides=6), f"shin{s}")

    # Greave: one shell over shin and calf, the shin guard standing up to the knee in front and the calf
    # lower behind; a cream band down each flank and a cream plate over the knee.
    GC = V(0.56, 0.07, 0.6)

    def greave_shape(p, q):
        if q.z > 0:
            p = Vector((p.x, p.y, p.z * lerp(1.0, 0.42, smooth(-0.55, 0.85, q.y))))
        below = max(0.0, -q.z)
        above = max(0.0, q.z)
        return Vector((p.x * (1 - 0.14 * below ** 2) * (1 - 0.12 * above ** 2), p.y * (1 - 0.1 * below ** 2), p.z))

    gr = geo.superquad(f"greave{s}", (0.29, 0.37, 0.26), M["orange"], GC, n=(3.3, 3.0, 3.2), shape=greave_shape,
                       res=10)
    gsurf = geo.Surface(gr)

    def band(p):
        yb = lerp(-0.14, 0.04, clamp((0.66 - p.z) / 0.36))
        return max(abs(p.y - yb) - 0.065, 0.17 - abs(p.x - GC.x))

    both(T.seams(paint(gr, band, M["cream"]), f"shin{s}"))
    both(T.seams(paint(gr, lambda p: max(((p.x - 0.665) / 0.075) ** 4 + ((p.z - 0.73) / 0.065) ** 4 - 1, p.y + 0.12),
                       M["cream"]), f"shin{s}"))
    both(T.seam(gsurf, [V(lerp(0.3, 0.86, i / 10), -0.6, 0.5) for i in range(11)], f"shin{s}",
                toward=lambda p: V(p.x, GC.y, p.z)))
    both(gr, f"shin{s}")
    for p in (V(0.45, -0.32, 0.48), V(0.75, -0.3, 0.5), V(0.85, 0.25, 0.55), V(0.27, 0.25, 0.55)):
        both(T.rivet(gsurf, p, f"shin{s}"))

    # Ankle: a graphite block between greave and boot, a big disc on each side.
    both(geo.superquad(f"ankle{s}", (0.22, 0.25, 0.13), M["graphite"], V(FOOT_X, 0.15, 0.28), n=2.6, res=5), f"foot{s}")
    for k, off in enumerate((-1, 1)):
        c = V(FOOT_X + off * 0.27, ANKLE.y + 0.03, 0.17)
        both([disc(f"ankle-disc{k}{s}", 0.135, 0.07, M["graphite"], c, (off, 0, 0), bevel_r=0.02, segs=28),
              geo.ring(f"ankle-ring{k}{s}", 0.082, 0.013, M["brass"], c + V(off * 0.035, 0, 0), (off, 0, 0), segs=20,
                       sides=6),
              disc(f"ankle-hub{k}{s}", 0.05, 0.03, M["steel"], c + V(off * 0.04, 0, 0), (off, 0, 0), segs=14)],
             f"foot{s}")
    for ob in boot(s, sx, M, T):
        both(ob)


def boot(s, sx, M, T):
    """A blocky boot: graphite soles on rubber treads, an orange vamp and heel on the foot and a toe cap on the
    toe (the boot bends at the ball, Y -0.24), seams and rivets."""
    out = []
    fx = FOOT_X
    out.append(part(geo.superquad(f"sole{s}", (0.335, 0.4, 0.04), M["graphite"], (fx, 0.165, 0.075),
                                  n=(4.0, 4.0, 3.0), res=6), f"foot{s}"))
    out.append(part(geo.superquad(f"sole-toe{s}", (0.335, 0.16, 0.04), M["graphite"], (fx, -0.385, 0.075),
                                  n=(4.0, 3.2, 3.0), res=5), f"toe{s}"))
    for k, (y0, y1) in enumerate(((0.58, 0.36), (0.31, 0.03), (-0.02, -0.235), (-0.27, -0.55))):
        out.append(part(geo.superquad(f"tread{k}{s}", (0.325, (y0 - y1) / 2, 0.025), M["rubber"], (fx, (y0 + y1) / 2, 0.026),
                                      n=(3.4, 3.4, 3.0), res=1), f"toe{s}" if y0 < -0.2 else f"foot{s}"))

    def vamp_shape(p, q):
        t = (q.y + 1) / 2                   # 0 front .. 1 back
        return Vector((p.x, p.y, p.z * (lerp(0.7, 1.0, t) if q.z > 0 else 1.0)))

    vamp = geo.superquad(f"vamp{s}", (0.325, 0.2, 0.12), M["orange"], (fx, -0.07, 0.19), n=(3.4, 2.8, 2.6),
                         shape=vamp_shape, res=7)
    out.append(part(vamp, f"foot{s}"))

    def cap_shape(p, q):
        t = (q.y + 1) / 2
        z = p.z * (lerp(0.78, 1.0, smooth(0.0, 0.8, t)) if q.z > 0 else 1.0)
        return Vector((p.x * lerp(0.93, 1.0, smooth(0.0, 0.5, t)), p.y, z))

    cap = geo.superquad(f"toe-cap{s}", (0.325, 0.18, 0.11), M["orange"], (fx, -0.37, 0.165), n=(3.4, 2.6, 2.6),
                        shape=cap_shape, res=7)
    csurf = geo.Surface(cap)
    for x in (-0.12, 0.12):
        out.append(T.seam(csurf, [V(fx + x, y, 1.0) for y in (lerp(-0.56, -0.24, i / 6) for i in range(7))], f"toe{s}",
                          toward=lambda p: V(p.x, p.y, 0.0)))
    out.extend(T.seams(paint(cap, lambda p: p.z - 0.15, M["orange"], recolour=False), f"toe{s}"))
    out.append(part(cap, f"toe{s}"))
    heel = geo.superquad(f"heel{s}", (0.315, 0.15, 0.1), M["orange"], (fx, 0.42, 0.17), n=(3.4, 2.6, 2.6), res=7)
    out.append(part(heel, f"foot{s}"))
    hs, vs = geo.Surface(heel), geo.Surface(vamp)
    for p in (V(fx + 0.2, 0.55, 0.2), V(fx - 0.2, 0.55, 0.2)):
        out.append(T.rivet(hs, p, f"foot{s}"))
    for p in (V(fx + 0.2, -0.2, 0.28), V(fx - 0.2, -0.2, 0.28)):
        out.append(T.rivet(vs, p, f"foot{s}"))
    for p in (V(fx + 0.22, -0.52, 0.14), V(fx - 0.22, -0.52, 0.14)):
        out.append(T.rivet(csurf, p, f"toe{s}"))
    return [o for o in out if o is not None]


# -------------------------------------------------------------------------------------------- arms
def arm(M, R, T, both):
    s, sx = "_L", 1
    sh_, el, wr = SHOULDER.copy(), ELBOW.copy(), WRIST.copy()
    fw = (wr - el).normalized()

    # The shoulder mechanism: a graphite drum out of the socket, a ball at its end.
    both(geo.segment(f"shoulder-drum{s}", V(0.6, 0.26, 2.04), V(0.8, SHOULDER.y, SHOULDER.z + 0.02), 0.16,
                     M["graphite"], n=2.8, res=5), f"shoulder{s}")
    both(geo.ring(f"shoulder-drum-ring{s}", 0.16, 0.02, M["graphite"], V(0.72, 0.28, 2.05), (1, 0, 0),
                  segs=20, sides=5), f"shoulder{s}")
    both(geo.sphere(f"shoulder-ball{s}", 0.13, M["graphite"], sh_, res=5), f"upper_arm{s}")

    # The pauldron: a big orange dome tipped outward, hollow and graphite inside, a rim plate round its foot.
    PC = V(0.97, 0.355, 1.955)
    rot = Matrix.Rotation(math.radians(-13), 3, "Y")
    axis = rot @ V(0, 0, 1)

    def dome(p, q):
        if q.z >= 0:
            return p
        lip = min(1.0, abs(q.x) ** 2.25 + abs(q.y) ** 2.3)       # 1 at the lip, 0 under the crown
        k = lerp(0.86, 1.0, lip ** 4)
        return Vector((p.x * k, p.y * k, -0.06 * lip ** 3 + 0.24 * (1 - lip) ** 1.2))

    pd = geo.superquad(f"pauldron{s}", (0.3, 0.385, 0.49), M["orange"], PC, n=(2.25, 2.3, 2.2), shape=dome,
                       res=10, rot=rot)
    paint_faces(pd, lambda c, n: n.dot(axis) < -0.5 and (c - PC).dot(axis) > -0.02, M["graphite"])
    both(T.seams(paint(pd, lambda p: (p - PC).dot(axis) - 0.11 - 0.04 * (p.y - PC.y) / 0.38, M["orange"],
                       recolour=False), f"upper_arm{s}"))
    psurf = geo.Surface(pd)
    both(pd, f"upper_arm{s}")
    for p in (PC + V(0.2, -0.3, 0.15), PC + V(0.3, 0.1, 0.1), PC + V(0.0, -0.4, 0.12), PC + V(0.25, 0.4, 0.12)):
        both(T.rivet(psurf, p, f"upper_arm{s}"))

    # Upper arm: a cream segment under the pauldron.
    ua = geo.segment(f"upper-arm{s}", V(0.9, 0.37, 1.95), V(0.95, 0.42, 1.63), 0.2, M["cream"], flat=1.25,
                     bulge=0.06, n=(2.4, 2.4, 2.8), res=8)
    usurf = geo.Surface(ua)
    both(T.seam(usurf, [V(1.3, lerp(0.05, 0.75, i / 8), 1.8) for i in range(9)], f"upper_arm{s}",
                toward=lambda p: V(0.96, p.y, p.z)))
    both(ua, f"upper_arm{s}")

    # Elbow: a graphite hinge.
    both(disc(f"elbow-joint{s}", 0.15, 0.34, M["graphite"], el, (1, 0, 0), bevel_r=0.04, segs=24), f"forearm{s}")
    for k, off in enumerate((-1, 1)):
        both(geo.ring(f"elbow-band{k}{s}", 0.14, 0.012, M["graphite"], el + V(off * 0.12, 0, 0), (1, 0, 0), segs=24,
                      sides=5), f"forearm{s}")

    # Gauntlet: the massive orange forearm, a cap plate over its top, plates down its faces, graphite under.
    ga, gb = V(1.17, 0.40, 1.635), V(1.19, 0.38, 1.075)
    gd = (gb - ga).normalized()
    gc = (ga + gb) / 2
    g = geo.segment(f"gauntlet{s}", ga, gb, 0.29, M["orange"], flat=1.14, bulge=0.04, n=(2.5, 3.2, 3.2), res=10)
    both(T.seams(paint(g, lambda p: 0.255 - (p - gc).dot(gd), M["graphite"]), f"forearm{s}"))
    gsurf = geo.Surface(g)
    both(T.seams(paint(g, lambda p: (p - gc).dot(-gd) - 0.17 + 0.06 * abs(p.y - gc.y) / 0.33, M["orange"],
                       recolour=False), f"forearm{s}"))
    for x in (1.07, 1.3):
        both(T.seam(gsurf, [V(x, -0.5, lerp(1.48, 1.14, i / 6)) for i in range(7)], f"forearm{s}",
                    toward=lambda p: V(gc.x, gc.y, p.z)))
    both(T.seam(gsurf, [V(2.0, lerp(0.15, 0.75, i / 8), lerp(1.47, 1.4, i / 8)) for i in range(9)], f"forearm{s}",
                toward=lambda p: V(gc.x, p.y, p.z)))
    both(g, f"forearm{s}")
    for p in (V(1.0, -0.2, 1.3), V(1.38, -0.2, 1.3), V(1.18, -0.2, 1.55), V(1.5, 0.2, 1.25), V(1.5, 0.6, 1.3)):
        both(T.rivet(gsurf, p, f"forearm{s}"))
    dc = V(1.43, 0.47, 1.6)
    ax = (1, 0, 0)
    both([disc(f"elbow-disc{s}", 0.13, 0.06, M["orange"], dc, ax, bevel_r=0.02, segs=28),
          disc(f"elbow-hub{s}", 0.09, 0.03, M["graphite"], dc + V(0.03, 0, 0), ax, bevel_r=0.01, segs=24),
          geo.ring(f"elbow-ring{s}", 0.058, 0.01, M["brass"], dc + V(0.045, 0, 0), ax, segs=24, sides=6),
          disc(f"elbow-nut{s}", 0.035, 0.03, M["steel"], dc + V(0.05, 0, 0), ax, segs=6)], f"forearm{s}")
    both(geo.sphere(f"wrist-ball{s}", 0.12, M["graphite"], wr, res=4), f"hand{s}")
    for ob in hand(R, s, sx, wr, fw, M, T):
        both(ob)


def hand(R, s, sx, wrist, fw, M, T):
    """A big four-digit hand on the end of the gauntlet: an orange back, a cream palm in an orange rim, and
    graphite digits of three segments, orange plates on their middle segments. The palm faces the thigh (a
    little back), so the thumb is on the front edge. Declares the hand's bones on `R` as it goes."""
    out = []
    along = fw.normalized()
    palm_n = V(-sx, 0.45, 0.0)
    palm_n = (palm_n - along * palm_n.dot(along)).normalized()
    xa = palm_n.cross(along).normalized()                 # (xa, palm_n, along) is right handed
    across = xa if xa.y < 0 else -xa                      # towards the thumb's edge: the front
    base = wrist + along * 0.06
    L, W, Tk = 0.27, 0.21, 0.09                            # palm length, half width, half thickness
    R.bone(f"hand{s}", wrist, base + along * L, f"forearm{s}", z=palm_n)
    g0 = base + along * 0.17 + palm_n * 0.16
    R.bone(f"grip{s}", g0, g0 + along * 0.1, f"hand{s}", z=palm_n)
    Mh = Matrix.Translation(base + along * (L / 2)) @ Matrix((xa, palm_n, along)).transposed().to_4x4()
    blk = geo.superquad(f"hand-block{s}", (W, Tk, L / 2), M["orange"], (0, 0, 0), n=(3.2, 2.6, 3.0), res=8,
                        shape=lambda p, q: Vector((p.x * (1 - 0.08 * (1 - q.z) / 2), p.y, p.z)))
    place(blk, Mh)
    inv = Mh.inverted()

    def palm(p):
        l = inv @ p
        return max(-(l.y - Tk * 0.35), abs(l.x) - W * 0.84, abs(l.z) - L * 0.43)

    out.extend(T.seams(paint(blk, palm, M["cream"]), f"hand{s}", r=0.004))
    out.extend(T.seams(paint(blk, lambda p: (inv @ p).z - L * 0.22, M["orange"], recolour=False), f"hand{s}", r=0.004))
    bsurf = geo.Surface(blk)
    for u in (-1, 1):
        out.append(T.seam(bsurf, [Mh @ V(u * W * 0.32, -Tk * 2, lerp(-L * 0.42, L * 0.22, i / 6)) for i in range(7)],
                          f"hand{s}", r=0.0035, toward=lambda p: p + palm_n))
    # The palm's own plates: a seam down its middle and one across, a rivet in each corner.
    out.append(T.seam(bsurf, [Mh @ V(W * 0.05 * math.sin(i), Tk * 2, lerp(-L * 0.36, L * 0.2, i / 6)) for i in range(7)],
                      f"hand{s}", r=0.0035, toward=lambda p: p - palm_n))
    out.append(T.seam(bsurf, [Mh @ V(lerp(-W * 0.8, W * 0.8, i / 8), Tk * 2, -L * 0.05 + 0.02 * (i / 8 - 0.5)) for i in range(9)],
                      f"hand{s}", r=0.0035, toward=lambda p: p - palm_n))
    for u, w in ((-0.62, -0.3), (0.62, -0.3), (-0.6, 0.12), (0.6, 0.12)):
        out.append(T.rivet(bsurf, Mh @ V(u * W, Tk * 1.5, w * L), f"hand{s}", r=0.011))
    for u in (-0.6, 0.6):
        out.append(T.rivet(bsurf, Mh @ V(u * W, -Tk * 1.5, -L * 0.25), f"hand{s}", r=0.012))
    out.append(part(blk, f"hand{s}"))

    def digit(name, root, direction, lengths, radius, plate_k=1):
        d = direction.normalized()
        p = root.copy()
        parent = f"hand{s}"
        for k, ln in enumerate(lengths):
            bn = f"{name}_{k + 1}{s}"
            R.bone(bn, p, p + d * ln, parent, z=palm_n)
            r = radius * (1 - 0.04 * k)
            c = r * 0.22
            if k == len(lengths) - 1:
                prof = [(0.0, -c * 0.5), (r * 0.82, -c * 0.5), (r, c * 0.5)] + [
                    (r * math.cos(a), ln - r + r * math.sin(a)) for a in (math.pi / 2 * i / 6 for i in range(7))]
            else:
                prof = [(0.0, -c * 0.5), (r * 0.82, -c * 0.5), (r, c * 0.5), (r, ln - c), (r * 0.84, ln), (0.0, ln)]
            out.append(part(geo.lathe(f"{name}{k}{s}", prof, M["graphite"], p, d, segs=12, y_hint=palm_n), bn))
            if k == plate_k:
                pc = p + d * (ln * 0.52) - palm_n * (r * 0.78)
                out.append(part(geo.superquad(f"{name}-plate{k}{s}", (r * 0.95, r * 0.32, ln * 0.36), M["orange"],
                                              pc, n=(3.0, 2.4, 3.0), res=2, rot=geo.basis(d, palm_n)), bn))
            p = p + d * ln
            parent = bn

    tip_c = base + along * L
    for k, nm in ((1.0, "index"), (0.0, "middle"), (-1.0, "ring")):
        root = tip_c - along * 0.035 + across * (0.135 * k) + palm_n * 0.008
        d = (along + across * (k * 0.07)).normalized()
        ln = 0.35 if k == 0 else 0.33
        digit(nm, root, d, (ln * 0.28, ln * 0.36, ln * 0.36), 0.06)
    troot = base + along * 0.08 + across * (W * 0.92) + palm_n * 0.035
    tdir = (along * 0.62 + across * 0.5 + palm_n * 0.45).normalized()
    digit("thumb", troot, tdir, (0.105, 0.1, 0.105), 0.062, plate_k=0)
    return out


# ------------------------------------------------------------------------------------------- views
def sheet_pose(R):
    """The model sheet's stance: toes turned out, fingers loosely curled, a sideways glance with the right
    brow up and the left one down and slanted."""
    R.rest()
    pb = R.ob.pose.bones
    for s, sx in rig.SIDES:
        R.turn_world(f"foot{s}", (0, 0, 1), sx * 14.0)
        for f in ("index", "middle", "ring"):
            for k, c in ((1, 22), (2, 26), (3, 18)):
                pb[f"{f}_{k}{s}"].rotation_quaternion = Matrix.Rotation(math.radians(c), 3, "X").to_quaternion()
        for k, c in ((1, 10), (2, 18), (3, 14)):
            pb[f"thumb_{k}{s}"].rotation_quaternion = Matrix.Rotation(math.radians(c), 3, "X").to_quaternion()
        R.turn_world(f"eye{s}", (0, 0, 1), -11.0)
    for nm, dz in (("brow_in_R", 0.012), ("brow_mid_R", 0.022), ("brow_out_R", 0.016),
                   ("brow_in_L", -0.004), ("brow_mid_L", -0.012), ("brow_out_L", -0.022)):
        pb[nm].location = (0.0, dz, 0.0)
    pb["lid_up_L"].rotation_quaternion = Matrix.Rotation(math.radians(-7), 3, "X").to_quaternion()
    bpy.context.view_layer.update()


def render_views(out, views, samples, res):
    focus = V(0, 0, 1.45)
    studio.sheet_lights(focus, 1.2)
    studio.floor(0.0)
    studio.settings(res=res, samples=samples, engine="CYCLES", view=opt("--view", "Standard"),
                    exposure=float(opt("--exposure", "-0.9")))
    for v in views:
        if v == "face":
            cam = studio.camera("cam-face", V(0, 0, 2.45), 0, 4.3, lens=110)
        elif v == "hand":
            cam = studio.camera("cam-hand", V(1.2, 0.3, 0.84), -112, 2.6, lens=110)
        elif v == "three":
            cam = studio.camera("cam-three", focus, 32, 8.5, lens=60)
        else:
            # "side" is the sheet's side view, which faces screen right: seen from the character's right.
            ang = {"front": 0, "side": -90, "back": 180, "left": 90, "right": -90}[v]
            cam = studio.camera(f"cam-{v}", focus, ang, 12.0, ortho=3.2)
        bpy.context.scene.camera = cam
        studio.render(Path(out) / f"brick-{v}.png")


def main():
    geo.reset()
    R, parts, M = build()
    meshes = R.finalize(parts)
    tris = sum(len(p.vertices) - 2 for m in meshes.values() for p in m.data.polygons)
    print(f"BRICK bones={len(R.order)} verts={ {k: len(v.data.vertices) for k, v in meshes.items()} } tris={tris}")
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
