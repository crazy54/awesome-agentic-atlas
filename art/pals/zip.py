"""Zip, as drawn on his model sheet: built, rigged and skinned from nothing but this script.

    blender -b --factory-startup --python art/pals/zip.py -- [--views front,side,back,three,face,hand]
            [--out DIR] [--samples N] [--res WxH] [--sheet-pose] [--save PATH] [--no-render]

The reference is `Zip robot model reference sheet.png` (the sheets live outside the repository; their landmarks
are transcribed in art/pals/reference.md). Glossy violet, mint and graphite, on chibi proportions: a wide
helmet of a head, long front to back, with a cream faceplate; huge magenta eyes standing out of round
sockets under heavy lid lines, mint brow visors with dark brows under them and a wide grin; two horns, graphite
with faceted mint tips, rising up, out and back; big ear cups; a thin graphite neck, a small violet chest with
a mint gem, a graphite waist and a violet pelvis; long thin limbs on graphite ball joints, mint shoulder caps
and knee pads; four-digit hands and chunky sneakers.

Scale: the dome's top stands 1.75 m up (the horns' tips about 1.95). On the sheet the dome is 490 px above
the floor line (y 624), so one sheet pixel is 1.75 / 490 m; landmarks are sheet pixels put through `Z` (front
or side view, y down) and `SY` (side view x, from the body's centre line at 748), or plain metres across (the
front view's centre line is at x 282.5; the head is drawn turned a little, centred near 290).

Budget: about 69k triangles, one skinned body mesh and one small face mesh (the mouth, which carries the
shape keys). The head is two solids carved with booleans: a cream face under a violet helmet with the
faceplate and the eye sockets cut out of it.

THE RIG (the shared skeleton of kit/rig.py; every bone deforms; his clips are clips/zip_base.py):

  * Trunk: root on the floor; hips at the hip joints (z 0.81) up to the belt; spine, the graphite waist;
    chest to the neck's foot (z 1.19); neck; head from the neck's top (z 1.28) up through the skull.
  * Arms are built in the sheet's A-pose, 48 degrees below level: shoulder (from the chest, z 1.12) to the
    ball joint at (0.175, 0, 1.11), upper_arm to the elbow (0.32, 0, 0.95), forearm to the wrist (0.52, -0.02,
    0.76): a reach of 0.5 m, so his hands do not get above his ears (z 1.48) and never over his head. Hands
    hang a little steeper than the forearm, palms back (+Y), thumbs on the body side.
  * grip_L/R: 8 cm down the hand from its base and 5.5 cm off the palm (on the palm's side), pointing along
    the hand: where a held prop goes.
  * Legs: the rest stance is the sheet's (thighs splayed 20 degrees: knees at +-0.21, ankles at +-0.26), feet
    pointing straight ahead; thigh, shin, foot (ankle to the ball at y -0.15, z 0.06), toe (to the shoe's
    tip). The shoes' fronts are skinned across foot and toe, so the soles bend at the ball. Heels at y
    +0.23, toes at -0.32 (zip_base.BODY).
  * Face: eye_L/R and lid_up/lid_lo_L/R at the eyeballs' centres, gazing out and turned in 4.6 degrees (he
    looks at you). The lids are built open: the upper closes at x -80, the lower at x +66. brow_in/mid/out
    point up the face (+Y is up it); each mint visor is skinned with its brow, so a brow raise lifts its visor.
    ear_L/R run out along the cups' axes from their feet, just inside the helmet.
  * Horns: horn_1_L/R from the horn's root inside the crown to 56% of its length (the graphite stock and its
    violet sleeve), horn_2 on to the tip (the mint point): a two-bone chain for wobble. Their Z leans
    forward, so +X tips a horn forward.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
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


PX = 1.75 / 490                       # metres per sheet pixel
FLOOR_PX, SIDE_CX_PX = 624, 748


def SY(x):
    """Side-view sheet x pixel -> Y in metres (the side view faces screen right, which is -Y)."""
    return -(x - SIDE_CX_PX) * PX


def Z(y):
    return (FLOOR_PX - y) * PX


# ------------------------------------------------------------------------------------------ palette
def palette():
    cream_img = mat.specks("zip-cream", "#e9d2be", speck_hex="#a07d62", count=90, seed=5, mottle=0.03)
    P = dict(
        violet=mat.principled("violet", "#7440b8", rough=0.2, coat=0.9, coat_rough=0.05),
        mint=mat.principled("mint", "#72d3a4", rough=0.22, coat=0.85, coat_rough=0.05),
        graphite=mat.principled("graphite", "#2e2d2c", rough=0.42, coat=0.3, coat_rough=0.34, spec=0.45),
        rubber=mat.principled("rubber", "#222121", rough=0.75, spec=0.3),
        cream=mat.textured(mat.principled("cream", "#e9d2be", rough=0.38, coat=0.35, coat_rough=0.12), cream_img),
        steel=mat.principled("steel", "#a9a6a2", metal=1.0, rough=0.28, aniso=0.4),
        brass=mat.principled("brass", "#b8893f", metal=1.0, rough=0.32),
        lens=mat.principled("lens", "#121416", rough=0.08, coat=1.0, coat_rough=0.02, spec=0.8),
        mouth=mat.principled("mouth", "#3a1220", rough=0.6, spec=0.3),
        teeth=mat.principled("teeth", "#f6f4ef", rough=0.18, coat=0.8),
        glint=mat.principled("glint", "#ffffff", rough=0.3, emit="#ffffff", strength=2.5),
        eye=mat.textured(mat.principled("zip-eye", "#ffffff", rough=0.3, coat=0.35, coat_rough=0.05, spec=0.35),
                         eye_texture("zip-eye-tex", inner_hex="#cc2ee0", outer_hex="#4c0c84", limbal_hex="#20062c",
                                     iris_r=0.32, pupil_r=0.19)),
    )
    for m in P.values():
        m["pal"] = "zip"
    return P


# ------------------------------------------------------------------------------------- helpers
def eye_texture(name, inner_hex, outer_hex, limbal_hex, iris_r, pupil_r, n=256, streaks=40, seed=3):
    """`mat.iris` for an eye seen only on its front cap: no shading in the sclera (only the cap shows, and
    the socket's rim covers its edge), the iris graded from `outer_hex` at the rim through `inner_hex`,
    radial streaks, a lighter band round the big pupil."""
    yy, xx = (np.mgrid[0:n, 0:n] + 0.5) / n - 0.5
    r = np.sqrt(xx * xx + yy * yy)
    ang = np.arctan2(yy, xx)
    img = np.ones((n, n, 3), np.float32) * mat._hex01("#f6f3ef")
    t = np.clip((r - pupil_r) / (iris_r - pupil_r), 0, 1)          # 0 at the pupil .. 1 at the rim
    inner, outer = mat._hex01(inner_hex), mat._hex01(outer_hex)
    w = t[..., None] ** 1.6
    col = inner[None, None, :] * (1 - w) + outer[None, None, :] * w
    rng = np.random.default_rng(seed)
    phase = rng.random(streaks) * math.tau
    st = np.zeros_like(r)
    for k in range(streaks):
        st += np.cos(ang * (k % 7 + 3) + phase[k]) * 0.5 / streaks * 6
    col = col * (1 + 0.18 * np.clip(st, -1, 1)[..., None])
    col = col * (1 + 0.3 * np.exp(-((t - 0.22) / 0.14) ** 2)[..., None])
    inside = r < iris_r
    img[inside] = np.clip(col[inside], 0, 1)
    lim = np.exp(-((r - iris_r) / 0.01) ** 2)
    img = img * (1 - lim[..., None]) + mat._hex01(limbal_hex)[None, None, :] * lim[..., None]
    pup = np.clip((pupil_r - r) / 0.005 + 0.5, 0, 1)
    img = img * (1 - pup[..., None]) + np.array([0.01, 0.008, 0.014], np.float32)[None, None, :] * pup[..., None]
    return mat.image(name, np.clip(img, 0, 1))


def superquad2(name, rpos, rneg, m, center=(0, 0, 0), npos=2.0, nneg=None, shape=None, res=10):
    """`geo.superquad` with a half-size and an exponent per direction: `rpos`/`rneg` are the (x, y, z)
    half-sizes towards + and - each axis, `npos`/`nneg` the exponents likewise, so one solid can be flat in
    front and a bullet behind. `shape(p, q)` as for `geo.superquad`."""
    npos = tuple(npos) if isinstance(npos, (tuple, list)) else (npos,) * 3
    nneg = npos if nneg is None else (tuple(nneg) if isinstance(nneg, (tuple, list)) else (nneg,) * 3)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=res, use_grid_fill=True)
    for v in bm.verts:
        u = geo._spherify(v.co)
        e = [npos[i] if u[i] >= 0 else nneg[i] for i in range(3)]
        lo, hi = 0.0, 2.0
        for _ in range(40):
            k = (lo + hi) / 2
            f = abs(u.x * k) ** e[0] + abs(u.y * k) ** e[1] + abs(u.z * k) ** e[2]
            lo, hi = (k, hi) if f < 1 else (lo, k)
        q = u * ((lo + hi) / 2)
        p = Vector([q[i] * (rpos[i] if q[i] >= 0 else rneg[i]) for i in range(3)])
        v.co = shape(p, q) if shape else p
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-7)
    ob = geo.mesh_object(name, bm, m)
    return geo.transform(ob, Matrix.Translation(Vector(center)))


def disc(name, radius, depth, m, center, axis, bevel_r=None, r_inner=0.0, segs=32, bulge=0.0, steps=2):
    """`geo.disc` with fewer steps round its rims: a joint or a lens for a third of the triangles."""
    prof = geo.rounded_profile(radius, depth, bevel_r if bevel_r is not None else depth * 0.3, r_inner,
                               steps=steps, front_bulge=bulge)
    return geo.lathe(name, prof, m, center, axis, segs=segs, caps=False)


def carve(ob, cutters, op="DIFFERENCE"):
    """Boolean `cutters` into `ob` (exact solver) and apply; the cutters stay for the caller to drop."""
    for c in cutters:
        md = ob.modifiers.new("carve", "BOOLEAN")
        md.operation, md.object, md.solver = op, c, "EXACT"
    geo.apply_modifiers(ob)
    return ob


def drop(*obs):
    for o in obs:
        me = o.data
        bpy.data.objects.remove(o, do_unlink=True)
        if me is not None and me.users == 0:
            bpy.data.meshes.remove(me)


def sharpen(ob, angle=32.0):
    """Mark the edges folded more than `angle` degrees sharp, so a carved rim shades crisp."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    lim = math.radians(angle)
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > lim:
            e.smooth = False
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    return ob


def prism(name, outline, y0, y1):
    """The closed 2D outline [(x, z), ...] extruded along Y from y0 to y1, flat-shaded: a cutter."""
    bm = bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in outline]
    b = [bm.verts.new((x, y1, z)) for x, z in outline]
    n = len(outline)
    bm.faces.new(a)
    bm.faces.new(b[::-1])
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return geo.mesh_object(name, bm, None, smooth_=False)


def rounded(poly, iters=2, closed=True):
    """Chaikin corner cutting: a polygon's corners rounded off."""
    pts = [tuple(p) for p in poly]
    for _ in range(iters):
        out = []
        n = len(pts)
        rng = range(n) if closed else range(n - 1)
        if not closed:
            out.append(pts[0])
        for i in rng:
            a, b = pts[i], pts[(i + 1) % n]
            out.append(tuple(lerp(a[k], b[k], 0.25) for k in range(len(a))))
            out.append(tuple(lerp(a[k], b[k], 0.75) for k in range(len(a))))
        if not closed:
            out.append(pts[-1])
        pts = out
    return pts


def front_ray(a, b):
    return V(a, -5.0, b), V(0, 1, 0)


def back_ray(a, b):
    return V(a, 5.0, b), V(0, -1, 0)


def plate(name, surf, outline, m, ray=front_ray, lift=0.004, sink=0.01, rings=3):
    """A slab laid on `surf` over the closed 2D outline: `ray(a, b) -> (origin, direction)` casts each
    point of it onto the surface; the slab's face stands `lift` proud of the surface, its back `sink` under
    it, and its rim is crisp. For emblems, light strips and panels."""
    pts = list(outline)
    n = len(pts)
    ca = sum(p[0] for p in pts) / n
    cb = sum(p[1] for p in pts) / n

    def hit(a, b):
        o, d = ray(a, b)
        loc, nor = surf.cast(o, d)
        if loc is None:
            raise ValueError(f"plate {name}: ({a:.3f}, {b:.3f}) misses the surface")
        return loc, nor

    bm = bmesh.new()
    loc, nor = hit(ca, cb)
    ct, cb_ = bm.verts.new(loc + nor * lift), bm.verts.new(loc - nor * sink)
    tops, bots = [], []
    for k in range(1, rings + 1):
        t = k / rings
        rt, rb = [], []
        for a, b in pts:
            loc, nor = hit(ca + (a - ca) * t, cb + (b - cb) * t)
            rt.append(bm.verts.new(loc + nor * lift))
            rb.append(bm.verts.new(loc - nor * sink))
        tops.append(rt)
        bots.append(rb)
    for j in range(n):
        k = (j + 1) % n
        bm.faces.new((ct, tops[0][j], tops[0][k]))
        bm.faces.new((cb_, bots[0][k], bots[0][j]))
        for r in range(rings - 1):
            bm.faces.new((tops[r][j], tops[r + 1][j], tops[r + 1][k], tops[r][k]))
            bm.faces.new((bots[r][k], bots[r + 1][k], bots[r + 1][j], bots[r][j]))
        bm.faces.new((tops[-1][j], bots[-1][j], bots[-1][k], tops[-1][k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    ob = geo.mesh_object(name, bm, m)
    return sharpen(ob, 50)


def path_weights(ob, pts, bones):
    """Skin `ob` smoothly across three bones (inner, middle, outer) by where along the path `pts` each
    vertex lies, as `face.brow` does for a brow."""
    seglen = [0.0]
    for a, b in zip(pts, pts[1:]):
        seglen.append(seglen[-1] + (b - a).length)
    L = seglen[-1]
    vgs = [ob.vertex_groups.new(name=b) for b in bones]
    for v in ob.data.vertices:
        best, bi, bt = 1e9, 0, 0.0
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            ab = b - a
            t = max(0.0, min(1.0, (v.co - a).dot(ab) / max(ab.length_squared, 1e-12)))
            d = (a + ab * t - v.co).length
            if d < best:
                best, bi, bt = d, i, t
        s = (seglen[bi] + (seglen[bi + 1] - seglen[bi]) * bt) / L
        w_in = max(0.0, 1 - 2 * s)
        w_out = max(0.0, 2 * s - 1)
        for vg, w in zip(vgs, (w_in, 1 - w_in - w_out, w_out)):
            if w > 1e-4:
                vg.add([v.index], w, "REPLACE")
    return ob


# ------------------------------------------------------------------------------------------- build
REST_FACE = {"grin": 1.0}            # his everyday face: the sheet's wide grin

HEAD_C = V(0.0, -0.025, 1.51)
HIP = V(0.098, 0.0, Z(398))
KNEE = V(0.213, -0.014, Z(487))
ANKLE = V(0.262, 0.06, 0.175)
SHOULDER = V(0.175, 0.0, Z(312))
ELBOW = V(0.323, -0.005, Z(359))
WRIST = V(0.52, -0.02, Z(412))
EYE_R, EYE_OPEN = 0.12, 0.106           # the eyeball, and the round opening it shows through
EYE_X, EYE_Z = 0.15, Z(216)
FACE_Y = -0.36                         # the front of the face, and of the eyes, at eye height


def head_shape(p, q):
    """The helmet's profile: the crown highest over the brow and sloping back to a bullet nose behind, the
    underside rising behind the neck, the jaw narrower than the cranium."""
    if q.z > 0:
        p.z *= 1.0 - 0.08 * q.y
    else:
        p.z *= 1.0 - 0.25 * max(0.0, q.y) ** 1.6
        p.x *= 1.0 - 0.36 * (-q.z) ** 2.0
    if q.y > 0:
        p.x *= 1.0 - 0.2 * q.y ** 2
        p.z += 0.035 * q.y ** 2
    return p


def head_solid(name, m, grow=0.0, res=14):
    g = grow
    return superquad2(name, (0.326 + g, 0.335 + g, 0.2302 + g), (0.326 + g, 0.335 + g, 0.243 + g), m, HEAD_C,
                      npos=(2.5, 1.75, 2.3), nneg=(2.5, 2.9, 2.5), shape=head_shape, res=res)


def socket_profile(r_open, rs, front=0.25, back=112.0):
    """The eye socket's cutter as a lathe profile [(radius, height along the gaze)]: a drum of the opening's
    radius `r_open` out through the face, widening behind it into a bowl of radius `rs` round the eye's
    centre, back to `back` degrees from the gaze. From the front the opening is a true circle; where the
    face falls away (round the outer side) the bowl shows, and with it the eyeball's flank."""
    a0 = math.asin(r_open / rs)
    prof = [(r_open, front), (r_open, rs * math.cos(a0))]
    for i in range(1, 11):
        a = lerp(a0, math.radians(back), i / 10)
        prof.append((rs * math.sin(a), rs * math.cos(a)))
    return prof


def socket_rim(inside, c, look, prof, n=48):
    """Where the socket cutter's surface (`prof`, as `socket_profile` gives it) breaks the head (`inside(p)`
    tells which side of it p is): for each of `n` meridians, walking the profile from the front, the first
    point that goes in. Returns the rim's points and each one's outward direction off the gaze."""
    up = (V(0, 0, 1) - look * look.z).normalized()
    side = look.cross(up).normalized()
    pts, outs = [], []
    for i in range(n):
        a = math.tau * i / n
        u = up * math.sin(a) + side * math.cos(a)

        def at(r, h):
            return c + look * h + u * r

        hit = at(*prof[-1])
        for (r0, h0), (r1, h1) in zip(prof, prof[1:]):
            if inside(at(r1, h1)):
                lo, hi = 0.0, 1.0
                for _ in range(24):
                    mid = (lo + hi) / 2
                    if inside(at(lerp(r0, r1, mid), lerp(h0, h1, mid))):
                        hi = mid
                    else:
                        lo = mid
                hit = at(lerp(r0, r1, lo), lerp(h0, h1, lo))
                break
        pts.append(hit)
        outs.append(u)
    return pts, outs


def build():
    M = palette()
    R = rig.Rig("zip")
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
        m = geo.mirror(ob)
        for vg in m.vertex_groups:                     # the mirror keeps the groups' names: swap their side
            vg.name = geo.flip_name(vg.name)
        parts.append(m)
        return ob

    # ---- skeleton ----------------------------------------------------------------------------------
    R.bone("root", (0, 0, 0), (0, 0.3, 0), z=(0, 0, 1))
    R.bone("hips", (0, 0, HIP.z), (0, 0, Z(376)), "root")
    R.bone("spine", (0, 0, Z(376)), (0, 0, Z(346)), "hips")
    R.bone("chest", (0, 0, Z(346)), (0, 0, Z(290)), "spine")
    R.bone("neck", (0, -0.005, Z(290)), (0, -0.005, Z(266)), "chest")
    R.bone("head", (0, -0.005, Z(266)), (0, -0.005, Z(180)), "neck")
    for s, sx in rig.SIDES:
        R.bone(f"shoulder{s}", (sx * 0.05, 0, Z(306)), (sx * SHOULDER.x, SHOULDER.y, SHOULDER.z), "chest")
        R.bone(f"upper_arm{s}", (sx * SHOULDER.x, SHOULDER.y, SHOULDER.z), (sx * ELBOW.x, ELBOW.y, ELBOW.z),
               f"shoulder{s}")
        R.bone(f"forearm{s}", (sx * ELBOW.x, ELBOW.y, ELBOW.z), (sx * WRIST.x, WRIST.y, WRIST.z), f"upper_arm{s}")
        R.bone(f"thigh{s}", (sx * HIP.x, HIP.y, HIP.z), (sx * KNEE.x, KNEE.y, KNEE.z), "hips")
        R.bone(f"shin{s}", (sx * KNEE.x, KNEE.y, KNEE.z), (sx * ANKLE.x, ANKLE.y, ANKLE.z), f"thigh{s}")
        R.bone(f"foot{s}", (sx * ANKLE.x, ANKLE.y, ANKLE.z), (sx * ANKLE.x, -0.15, 0.06), f"shin{s}", z=(0, 0, 1))
        R.bone(f"toe{s}", (sx * ANKLE.x, -0.15, 0.06), (sx * ANKLE.x, -0.31, 0.06), f"foot{s}", z=(0, 0, 1))

    # ---- head --------------------------------------------------------------------------------------
    # A cream head under a violet helmet: the helmet is the same solid grown a few millimetres, with the
    # faceplate cut out of it (everything below the brows and inside the cheeks, but for the violet ridge
    # running down between the eyes), so its rim stands as a lip round the face.
    skull = head_solid("head-face", M["cream"])
    helmet = head_solid("head-shell", M["violet"], grow=0.007)
    left = [(0.0, 1.4), (0.011, 1.403), (0.018, 1.416), (0.02, 1.45), (0.023, 1.51), (0.034, 1.567),
            (0.05, 1.585), (0.1, 1.603), (0.16, 1.612), (0.22, 1.607), (0.262, 1.59), (0.284, 1.555),
            (0.293, 1.5), (0.3, 1.45), (0.6, 1.38)]   # the nose's tip, round the brow, down the side
    contour = [(-x, z) for x, z in left[::-1]] + left[1:]
    outline = [(0.6, 1.0), (-0.6, 1.0)] + rounded(contour, 2, closed=False)
    # The eyes are big balls standing out of the face, each showing through a round opening that widens
    # behind the face into a bowl a little larger than the ball (`socket_profile`), carved from the face and
    # the helmet; the opening's lip is outlined in graphite, heavy along the top like a lid line. The lip is
    # found against the smooth solids, before any carving.
    s_in, h_in = geo.Surface(skull), geo.Surface(helmet)

    def under(sf, p):
        loc, nor, _, _ = sf.tree.find_nearest(p)
        return loc is not None and (p - loc).dot(nor) < 0

    def in_mask(p):
        if p.y > -0.17:
            return False
        hit = False
        for (x0, z0), (x1, z1) in zip(outline, outline[1:] + outline[:1]):
            if (z0 > p.z) != (z1 > p.z) and p.x < x0 + (p.z - z0) * (x1 - x0) / (z1 - z0):
                hit = not hit
        return hit

    def inside(p):
        return under(s_in, p) or (under(h_in, p) and not in_mask(p))

    mask = prism("face-mask", outline, -1.0, -0.17)
    carve(helmet, [mask])
    drop(mask)

    sockets, looks, rims = [], {}, {}
    for s, sx in rig.SIDES:
        look = V(-sx * 0.08, -1, 0.0).normalized()
        c = V(sx * EYE_X, FACE_Y + EYE_R, EYE_Z)
        looks[s] = (c, look)
        prof = socket_profile(EYE_OPEN, EYE_R * 1.07)
        rims[s] = socket_rim(inside, c, look, prof)
        # (only the bowl's front: what lay behind the eye's equator would be a hidden cavity)
        sockets.append(geo.lathe(f"socket{s}", [(0.0, prof[0][1])] + prof + [(0.0, prof[-1][1])], None, c, look,
                                 segs=40, caps=False))
    carve(helmet, sockets)
    carve(skull, sockets)
    # the cream head shows only at the front: the rest of it, under the helmet, goes
    keep = geo.superquad("face-keep", (1.0, 0.47, 1.0), None, (0, -0.53, 1.5), n=4.0, res=2)
    carve(skull, [keep], "INTERSECT")
    drop(keep, *sockets)
    for ob in (skull, helmet):
        sharpen(ob, 40)
    geo.box_uv(skull, 0.5)
    add(skull, "head")
    add(helmet, "head")
    surf = geo.Surface(skull, helmet)
    hsurf = geo.Surface(helmet)

    # Eyes, the irises turned in a touch (he looks at you).
    for s, sx in rig.SIDES:
        c, look = looks[s]
        R.bone(f"eye{s}", c, c + look * 0.08, "head", z=(0, 0, 1))
        R.bone(f"lid_up{s}", c, c + look * 0.07, "head", z=(0, 0, 1))
        R.bone(f"lid_lo{s}", c, c + look * 0.06, "head", z=(0, 0, 1))
        eparts, _ = face.eye(f"eye{s}", sx, c, EYE_R, look,
                             dict(eye=f"eye{s}", lid_up=f"lid_up{s}", lid_lo=f"lid_lo{s}", head="head"),
                             M["eye"], M["cream"], M["graphite"], M["glint"], lid_r=1.045, lash=0.12,
                             lash_flick=0.0, up_open=80, lo_open=66, lid_roll=-4, res=8, glint=(0.24, 0.3),
                             glint_size=0.13)
        parts.extend(eparts)
        pts, outs = rims[s]
        n = len(pts)
        for _ in range(3):                                                    # smooth the lip's line
            pts = [(pts[i - 1] + pts[i] * 2 + pts[(i + 1) % n]) / 4 for i in range(n)]
        top = [max(0.0, math.sin(math.tau * i / n)) for i in range(n)]       # 1 at the top of the eye
        hw = [0.0042 + 0.012 * t ** 0.8 for t in top]
        # its outer edge on the lip; the heavy top grows inwards, over the eye, as a lid line does
        rim = [p + o * (0.005 - w) for p, o, w in zip(pts, outs, hw)]
        add(geo.sweep(f"eye-rim{s}", rim, hw, [0.007] * n, M["graphite"], segs=6, up=look, closed=True,
                      caps=False), "head")

    # Brows: a mint visor on the shell over each eye, a dark brow along its lower edge; both bend on the
    # brow bones, so the visor lifts with the brow.
    for s, sx in rig.SIDES:
        bpts = [(sx * 0.045, 1.606), (sx * 0.09, 1.621), (sx * 0.14, 1.63), (sx * 0.19, 1.631), (sx * 0.235, 1.622),
                (sx * 0.265, 1.604)]
        names = [f"brow_in{s}", f"brow_mid{s}", f"brow_out{s}"]
        for nm, (bx, bz) in zip(names, [bpts[0], bpts[2], bpts[-1]]):
            p = surf.front(bx, bz)
            R.bone(nm, p, p + V(0, 0, 0.05), "head", z=(0, -1, 0))
        parts.append(face.brow(f"brow{s}", sx, surf, bpts, 0.021, 0.012, M["graphite"], names,
                               taper=(1.1, 0.95, 0.5), offset=0.003))
        vis = [(sx * 0.04, 1.638), (sx * 0.09, 1.66), (sx * 0.14, 1.671), (sx * 0.19, 1.672), (sx * 0.235, 1.659),
               (sx * 0.274, 1.63)]
        vpts = [hsurf.front(x, z, offset=0.006) for x, z in vis]
        hw = [0.012, 0.024, 0.028, 0.027, 0.021, 0.011]
        visor = geo.sweep(f"visor{s}", vpts, [0.009] * len(vpts), hw, M["mint"], n=2.6, segs=12, up=(0, 0, 1))
        path_weights(visor, vpts, names)
        parts.append(visor)

    # Mouth: rest is a closed smile; `grin` is the sheet's wide open grin, on by default.
    shapes = dict(
        rest=dict(w=0.088, smile=0.02, thick=0.008),
        grin=dict(w=0.094, smile=0.024, top=0.003, bot=0.026, teeth=0.5, thick=0.008, lift_L=0.012, lift_R=-0.002),
        smile=dict(w=0.1, smile=0.03, bot=0.012, thick=0.009),
        wide=dict(w=0.115, smile=0.024, top=0.01, bot=0.042, teeth=0.32, low_teeth=0.12, round=0.3),
        open=dict(w=0.075, smile=0.0, top=0.018, bot=0.04, round=0.6, teeth=0.18),
        oh=dict(w=0.04, smile=0.0, top=0.024, bot=0.028, round=1.0, thick=0.007),
        frown=dict(w=0.085, smile=-0.024, thick=0.009),
        flat=dict(w=0.08, smile=0.0, thick=0.008),
        smirk_L=dict(w=0.095, smile=0.006, lift_L=0.034, lift_R=-0.005, thick=0.009),
        smirk_R=dict(w=0.095, smile=0.006, lift_R=0.034, lift_L=-0.005, thick=0.009),
        grit=dict(w=0.1, smile=-0.003, top=0.014, bot=0.016, teeth=0.5, low_teeth=0.5, thick=0.007),
        ee=dict(w=0.115, smile=0.025, top=0.007, bot=0.02, teeth=0.55, low_teeth=0.3),
    )
    mth = face.mouth("mouth", geo.Surface(skull), (0.0, 1.333), shapes, (M["mouth"], M["teeth"]))
    mth.data.shape_keys.key_blocks["grin"].value = 1.0
    parts.append(mth)

    # Ear cups: layered on the X axis, the housing violet, a broad mint ring, a dark lens, a brass pin.
    ear_y, ear_z = SY(725), Z(209)
    eb = hsurf.side(ear_y, ear_z, s=1).x - 0.012      # the cup's foot, just inside the helmet
    for s, sx in rig.SIDES:
        R.bone(f"ear{s}", (sx * eb, ear_y, ear_z), (sx * (eb + 0.1), ear_y, ear_z), "head", z=(0, -1, 0))

    def at(dx):
        return V(eb + dx, ear_y, ear_z)

    ax = (1, 0, 0)
    for ob in (disc("ear-housing_L", 0.138, 0.11, M["violet"], at(0.055), ax, bevel_r=0.032, segs=32),
               geo.ring("ear-mint_L", 0.1, 0.0175, M["mint"], at(0.11), ax, segs=32, sides=8, squash=0.9),
               disc("ear-face_L", 0.088, 0.03, M["graphite"], at(0.11), ax, bevel_r=0.01, segs=32),
               geo.ring("ear-mint2_L", 0.058, 0.0065, M["mint"], at(0.125), ax, segs=32, sides=6),
               disc("ear-lens_L", 0.05, 0.02, M["lens"], at(0.124), ax, bevel_r=0.008, segs=24, bulge=0.008),
               disc("ear-pin_L", 0.017, 0.014, M["brass"], at(0.138), ax, segs=16)):
        both(ob, "ear_L")

    # Horns: from the crown's shoulders, up, out and swept back; a graphite hexagonal stock in a violet
    # sleeve, and a faceted mint tip, on two bones so they can wobble.
    hdir = V(0.55, 0.75, 1.0).normalized()
    hx, hy = 0.235, 0.02
    top = hsurf.cast(V(hx, hy, 3.0), V(0, 0, -1))[0]
    hb = V(hx, hy, top.z - 0.045)
    HL = 0.42
    hm = hb + hdir * HL * 0.56
    ht = hb + hdir * HL
    for s, sx in rig.SIDES:
        R.bone(f"horn_1{s}", V(sx * hb.x, hb.y, hb.z), V(sx * hm.x, hm.y, hm.z), "head", z=(0, -1, 0))
        R.bone(f"horn_2{s}", V(sx * hm.x, hm.y, hm.z), V(sx * ht.x, ht.y, ht.z), f"horn_1{s}", z=(0, -1, 0))
    n_st = 7
    stock = [hb.lerp(hm, i / (n_st - 1)) for i in range(n_st)]
    sw = [lerp(0.05, 0.043, i / (n_st - 1)) for i in range(n_st)]
    sd = [lerp(0.066, 0.056, i / (n_st - 1)) for i in range(n_st)]
    both(geo.sweep("horn-stock_L", stock, sw, sd, M["graphite"], n=2.0, segs=6, up=(0, 1, -0.3), smooth_=False,
                   twist=[math.pi / 6] * n_st),
         "horn_1_L")
    sl = [hb.lerp(hb + hdir * HL * 0.14, i / 3) for i in range(4)]
    both(geo.sweep("horn-sleeve_L", sl, 0.055, 0.071, M["violet"], n=2.0, segs=6, up=(0, 1, -0.3), smooth_=False,
                   twist=[math.pi / 6] * 4),
         "horn_1_L")
    tp = [hm - hdir * 0.01] + [hm.lerp(ht, t) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
    tw = [0.04, 0.047, 0.045, 0.037, 0.022, 0.003]
    td = [0.052, 0.06, 0.058, 0.047, 0.028, 0.003]
    both(geo.sweep("horn-tip_L", tp, tw, td, M["mint"], n=2.0, segs=6, up=(0, 1, -0.3), smooth_=False,
                   twist=[math.pi / 6] * len(tp)), "horn_2_L")

    # Under the head, behind the neck: a graphite socket, and a mint light strip across the back.
    add(disc("head-socket", 0.085, 0.04, M["graphite"], (0, 0.0, Z(266) + 0.012), (0, 0, 1), bevel_r=0.012, segs=28),
        "head")
    strip = rounded([(-0.08, 1.41), (0.08, 1.41), (0.08, 1.393), (-0.08, 1.393)], 2)
    add(plate("head-light", hsurf, strip, M["mint"], ray=back_ray, lift=0.004, sink=0.01, rings=1), "head")
    under = rounded([(-0.1, 1.384), (0.1, 1.384), (0.135, 1.338), (-0.135, 1.338)], 2)
    add(plate("head-underplate", hsurf, under, M["graphite"], ray=back_ray, lift=0.003, sink=0.01, rings=2), "head")
    # Panel seams on the dome, as on the sheet: one over the crown between the horns, one round the back
    # from ear to ear, riveted.
    crown = [hsurf.cast(V(x, -0.07 + 0.25 * x * x, 3.0), V(0, 0, -1))[0] for x in (lerp(-0.2, 0.2, i / 20)
                                                                                for i in range(21))]
    add(geo.tube("seam-crown", [p for p in crown if p is not None], 0.0026, M["graphite"], segs=6), "head")
    back = []
    for i in range(25):
        a = math.radians(lerp(-62, 62, i / 24))
        d = V(math.sin(a), math.cos(a), 0.0)
        p = hsurf.toward(V(0, 0, 1.62) + d * 1.0, V(0, 0, 1.62))
        if p is not None:
            back.append(p)
    add(geo.tube("seam-back", back, 0.0026, M["graphite"], segs=6), "head")
    for k, p in enumerate(back[2:-2:4]):
        add(geo.sphere(f"rivet{k}", 0.0065, M["steel"], p + hsurf.normal_at(p) * 0.002, res=2), "head")

    # Neck: a thin graphite column of rings.
    nz0, nz1 = Z(292), Z(262)
    add(geo.segment("neck-core", (0, -0.005, nz0 - 0.02), (0, -0.005, nz1 + 0.03), 0.045, M["graphite"], res=6),
        "neck")
    for i in range(3):
        z = lerp(nz0, nz1, (i + 0.5) / 3)
        add(disc(f"neck-ring{i}", 0.058, 0.022, M["graphite"], (0, -0.005, z), (0, 0, 1), bevel_r=0.009,
                     segs=24), "neck" if i else "chest")

    # ---- torso -------------------------------------------------------------------------------------
    CH_C = V(0, -0.012, Z(318))

    def chest_shape(p, q):
        # A shield: broad across the shoulders, tapering to a narrow waist; the front a little proud.
        t = (q.z + 1) / 2
        sx = lerp(0.7, 1.0, smooth(0.05, 0.6, t)) * lerp(1.0, 0.9, smooth(0.8, 1.0, t))
        p = Vector((p.x * sx, p.y * lerp(0.82, 1.0, smooth(0.0, 0.6, t)), p.z))
        if q.y < 0:
            p.y *= 1.0 + 0.08 * math.sin(math.pi * t)
        return p

    chest = add(geo.superquad("chest-shell", (0.156, 0.15, 0.12), M["violet"], CH_C, n=(2.6, 2.4, 3.0),
                              shape=chest_shape, res=10), "chest")
    csurf = geo.Surface(chest)
    gem = rounded([(-0.056, 1.127), (-0.042, 1.137), (0.042, 1.137), (0.056, 1.127), (0.012, 1.054),
                   (-0.012, 1.054)], 2)
    add(plate("chest-gem", csurf, gem, M["mint"], lift=0.005, sink=0.01), "chest")
    for k, sx in enumerate((1, -1)):                 # the panel seams either side of the gem
        seam = [csurf.front(sx * (lerp(0.112, 0.05, t) + 0.018 * math.sin(math.pi * t)), lerp(1.185, 1.0, t))
                for t in (i / 14 for i in range(15))]
        add(geo.tube(f"chest-seam{k}", [q for q in seam if q is not None], 0.0024, M["graphite"], segs=6), "chest")
    add(plate("chest-light", csurf, rounded([(-0.04, 1.012), (0.04, 1.012), (0.04, 0.997), (-0.04, 0.997)], 2),
              M["mint"], lift=0.004, sink=0.01, rings=1), "chest")
    add(plate("collar-light", csurf, rounded([(-0.026, 1.19), (0.026, 1.19), (0.026, 1.18), (-0.026, 1.18)], 2),
              M["mint"], lift=0.003, sink=0.01, rings=1), "chest")
    bgem = rounded([(-0.05, 1.12), (-0.038, 1.13), (0.038, 1.13), (0.05, 1.12), (0.01, 1.058), (-0.01, 1.058)], 2)
    add(plate("back-gem", csurf, bgem, M["mint"], ray=back_ray, lift=0.005, sink=0.01), "chest")
    add(plate("back-light", csurf, rounded([(-0.032, 1.01), (0.032, 1.01), (0.032, 0.997), (-0.032, 0.997)], 2),
              M["mint"], ray=back_ray, lift=0.004, sink=0.01, rings=1), "chest")

    # Waist: a graphite plate under the chest, then a ribbed column down into the pelvis.
    add(geo.superquad("abdomen-plate", (0.088, 0.085, 0.026), M["graphite"], (0, -0.004, Z(350)),
                      n=(2.6, 2.4, 2.8), res=5,
                      shape=lambda p, q: Vector((p.x * (1 - 0.18 * (1 - q.z) / 2), p.y, p.z))), "chest")
    add(geo.segment("waist-core", (0, 0.0, Z(386)), (0, 0.0, Z(350)), 0.06, M["graphite"], flat=0.9, n=2.4,
                    res=6), "spine")
    for i in range(2):
        z = lerp(Z(374), Z(362), i)
        add(geo.superquad(f"waist-rib{i}", (0.068, 0.066, 0.011), M["graphite"], (0, 0.0, z),
                          n=(2.4, 2.4, 3), res=4), "spine")

    # Pelvis: a violet brief under a belt, graphite ball joints at its corners.
    PV_C = V(0, 0.0, Z(402))

    def pelvis_shape(p, q):
        t = (q.z + 1) / 2
        sx = lerp(0.6, 1.0, smooth(0.0, 0.8, t))
        return Vector((p.x * sx, p.y * lerp(0.75, 1.0, smooth(0.0, 0.7, t)), p.z))

    add(geo.superquad("pelvis-shell", (0.13, 0.122, 0.098), M["violet"], PV_C, n=(2.5, 2.3, 2.4),
                      shape=pelvis_shape, res=8), "hips")
    add(geo.superquad("pelvis-belt", (0.135, 0.127, 0.02), M["violet"], (0, 0.0, Z(380)), n=(2.6, 2.4, 3.0),
                      res=6), "hips")
    add(geo.superquad("pelvis-slot", (0.026, 0.01, 0.007), M["graphite"], (0, -0.127, Z(381)), n=2.6, res=3),
        "hips")
    for s, sx in rig.SIDES:
        add(geo.sphere(f"hip-ball{s}", 0.058, M["graphite"], (sx * HIP.x, HIP.y, HIP.z), res=4), f"thigh{s}")
        d = V(sx * 0.6, -0.8, 0.0).normalized()
        add(disc(f"hip-disc{s}", 0.05, 0.03, M["graphite"], V(sx * HIP.x, HIP.y, HIP.z) + d * 0.045, d,
                 bevel_r=0.01, segs=24), f"thigh{s}")
        add(disc(f"hip-cap{s}", 0.022, 0.012, M["brass"], V(sx * HIP.x, HIP.y, HIP.z) + d * 0.062, d, segs=16),
            f"thigh{s}")

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

    # Textured materials need UVs on every part that wears them (the lids are cream too).
    for ob in parts:
        if not ob.data.uv_layers and any(m is not None and m.get("textured") for m in ob.data.materials):
            geo.box_uv(ob, 0.5)

    R.build()
    return R, parts, M


def leg(M, both):
    s, sx = "_L", 1
    hip, knee, ankle = HIP.copy(), KNEE.copy(), ANKLE.copy()
    down = (knee - hip).normalized()
    # thigh: a drumstick, full under the pelvis and rounded off above the knee
    th = geo.segment(f"thigh{s}", hip + down * 0.025 + V(0.018, 0, 0), knee - down * 0.055, 0.1, M["violet"],
                     rb=0.074, flat=1.02, bulge=0.03, n=2.5, res=7, y_hint=(0, 1, 0))
    both(th, f"thigh{s}")
    both(geo.ring(f"hip-mint{s}", 0.042, 0.0065, M["mint"], hip + V(0.04, 0, 0), (1, 0, 0), segs=24, sides=6),
         f"thigh{s}")
    # knee: a graphite knuckle with a mint ring on its outer side, and a mint pad in front, riding on the shin
    both(geo.superquad(f"knee-joint{s}", (0.076, 0.06, 0.066), M["graphite"], knee, n=2.4, res=5), f"shin{s}")
    both(geo.ring(f"knee-ring{s}", 0.042, 0.006, M["mint"], knee + V(0.06, 0, 0), (1, 0, 0), segs=24, sides=6),
         f"shin{s}")
    pad = geo.superquad(f"knee-pad{s}", (0.054, 0.034, 0.074), M["mint"], knee + V(0.0, -0.058, 0.0),
                        n=(2.2, 2.0, 2.3), res=5,
                        shape=lambda p, q: Vector((p.x, p.y + 0.014 * (q.x * q.x + q.z * q.z), p.z)))
    both(pad, f"shin{s}")
    # shin: a teardrop, full under the knee with a calf behind, down to a slim ankle
    dn = (ankle - knee).normalized()

    def shin_shape(p, q):
        t = (q.z + 1) / 2                         # 0 knee .. 1 ankle
        if q.y > 0:
            p.y *= 1 + 0.45 * math.sin(math.pi * min(1.0, t * 1.5)) ** 1.5
        if q.x < 0:                               # local -x is the outer flank on the left
            p.x *= 1 + 0.15 * math.sin(math.pi * min(1.0, t * 1.4))
        return p

    sh = geo.segment(f"shin{s}", knee + dn * 0.025, ankle - dn * 0.06, 0.09, M["violet"], rb=0.05, flat=0.92,
                     bulge=0.06, n=2.4, res=7, y_hint=(0, 1, 0), shape=shin_shape)
    both(sh, f"shin{s}")
    both(geo.sphere(f"ankle-ball{s}", 0.052, M["graphite"], ankle, res=4), f"foot{s}")
    both(geo.segment(f"ankle-post{s}", ankle - dn * 0.08, ankle, 0.038, M["graphite"], res=5), f"shin{s}")
    ad = ankle + V(sx * 0.078, 0.035, -0.018)
    both(disc(f"ankle-disc{s}", 0.06, 0.034, M["graphite"], ad, (sx, 0, 0), bevel_r=0.01, segs=28), f"foot{s}")
    both(geo.ring(f"ankle-ring{s}", 0.044, 0.0065, M["mint"], ad + V(sx * 0.017, 0, 0), (sx, 0, 0), segs=24,
                  sides=6), f"foot{s}")
    both(disc(f"ankle-lens{s}", 0.032, 0.012, M["lens"], ad + V(sx * 0.019, 0, 0), (sx, 0, 0), segs=16,
                  bulge=0.004), f"foot{s}")
    for ob in sneaker(s, sx, M):
        both(ob)


def arm(M, R, both):
    s, sx = "_L", 1
    sh_ = SHOULDER.copy()
    el = ELBOW.copy()
    wr = WRIST.copy()
    up = (el - sh_).normalized()
    fw = (wr - el).normalized()
    both(geo.sphere(f"shoulder-ball{s}", 0.054, M["graphite"], sh_, res=5), f"shoulder{s}")
    both(disc(f"shoulder-cap{s}", 0.022, 0.012, M["brass"], sh_ + V(0.014, -0.047, 0), V(0.3, -1, 0), segs=16),
         f"shoulder{s}")
    # the pad: a violet cap over the top of the arm, mint over its outer crown
    pad_c = sh_ + V(0.05, 0.0, -0.014)
    pad = geo.superquad(f"shoulder-pad{s}", (0.066, 0.07, 0.076), M["violet"], pad_c, n=2.3, res=6,
                        rot=geo.basis(V(0.35, 0, 1), (0, 1, 0)))
    both(pad, f"upper_arm{s}")
    both(geo.superquad(f"shoulder-mint{s}", (0.056, 0.06, 0.03), M["mint"], pad_c + V(0.03, 0, 0.046), n=2.3,
                       res=5, rot=geo.basis(V(0.7, 0, 1), (0, 1, 0))), f"upper_arm{s}")
    ua = geo.segment(f"upper-arm{s}", sh_ + up * 0.03, el - up * 0.035, 0.048, M["violet"], rb=0.04, bulge=0.04,
                     n=2.4, res=6, y_hint=(0, 0, 1))
    both(ua, f"upper_arm{s}")
    both(geo.segment(f"upper-arm-cuff{s}", el - up * 0.06, el - up * 0.028, 0.037, M["graphite"], res=5,
                     y_hint=(0, 0, 1)), f"upper_arm{s}")
    both(geo.sphere(f"elbow-ball{s}", 0.058, M["graphite"], el, res=5), f"forearm{s}")
    # forearm: a gauntlet, full at the elbow end and tapering to the wrist, mint round its top
    fa = geo.segment(f"forearm{s}", el + fw * 0.03, wr - fw * 0.02, 0.074, M["violet"], rb=0.056, bulge=0.03,
                     flat=0.92, n=2.5, res=7, y_hint=(0, 0, 1))
    both(fa, f"forearm{s}")
    both(geo.segment(f"forearm-mint{s}", el + fw * 0.036, el + fw * 0.074, 0.079, M["mint"], flat=0.93, n=2.6,
                     res=5, y_hint=(0, 0, 1)), f"forearm{s}")
    both(geo.sphere(f"wrist-ball{s}", 0.04, M["graphite"], wr, res=4), f"hand{s}")
    for ob in hand(R, s, sx, wr, fw, M):
        both(ob)


def ball_bend(ob, s, y0=-0.11, y1=-0.19):
    """Skin a shoe part across the foot and the toe: what lies ahead of the ball follows the toe."""
    f, t = ob.vertex_groups.new(name=f"foot{s}"), ob.vertex_groups.new(name=f"toe{s}")
    for v in ob.data.vertices:
        w = smooth(y0, y1, v.co.y)
        if w < 1.0:
            f.add([v.index], 1.0 - w, "REPLACE")
        if w > 0.0:
            t.add([v.index], w, "REPLACE")
    return ob


def sneaker(s, sx, M):
    """A chunky sneaker: a graphite tread with a lip, a thick mint sole that rises at toe and heel, a bulbous
    violet toe box and instep that stop at the ankle, a violet heel tab behind with a mint cap, and between
    them, above the heel, the ankle's graphite works; a graphite tongue and laces, a mint loop over them."""
    out = []
    fx = sx * ANKLE.x
    L0, L1 = 0.232, -0.318                     # heel and toe, Y
    cy = (L0 + L1) / 2
    hl = (L0 - L1) / 2

    def sole_shape(p, q):
        t = (q.y + 1) / 2                       # 0 toe .. 1 heel
        w = lerp(0.86, 1.0, smooth(0.0, 0.5, t)) * lerp(1.0, 0.94, smooth(0.6, 1.0, t))
        z = p.z + (0.026 * smooth(0.2, 0.0, t) if q.z > -0.5 else 0.018 * smooth(0.16, 0.0, t))
        return Vector((p.x * w, p.y, z))

    tread = geo.superquad(f"shoe-tread{s}", (0.13, hl + 0.004, 0.022), M["rubber"], (fx, cy, 0.022),
                          n=(3.2, 3.4, 3.4), shape=sole_shape, res=6)
    out.append(part(ball_bend(tread, s), f"foot{s}"))

    def mid_shape(p, q):
        p = sole_shape(p, q)
        if q.z > 0:
            p.z += 0.026 * abs(q.y) ** 3
        return p

    mid = geo.superquad(f"shoe-mid{s}", (0.126, hl - 0.006, 0.042), M["mint"], (fx, cy, 0.072), n=(3.0, 3.0, 2.6),
                        shape=mid_shape, res=7)
    out.append(part(ball_bend(mid, s), f"foot{s}"))

    def upper_shape(p, q):
        t = (q.y + 1) / 2                       # 0 toe .. 1 the ankle's back
        top = lerp(0.84, 1.0, smooth(0.05, 0.45, t)) * lerp(1.0, 0.78, smooth(0.75, 1.0, t))
        z = p.z * (top if q.z > 0 else 1.0)
        w = lerp(0.86, 1.0, smooth(0.0, 0.45, t)) * (1 - 0.14 * max(0.0, q.z))
        return Vector((p.x * w, p.y, z))

    UY0, UY1 = 0.115, L1 + 0.008               # the upper runs from behind the ankle to the toe
    upper = geo.superquad(f"shoe-upper{s}", (0.118, (UY0 - UY1) / 2, 0.11), M["violet"],
                          V(fx, (UY0 + UY1) / 2, 0.12), n=(2.3, 2.1, 2.2), shape=upper_shape, res=7)
    us = geo.Surface(upper)
    out.append(part(ball_bend(upper, s), f"foot{s}"))
    for k, y in enumerate(lerp(-0.1, -0.2, i / 2) for i in range(3)):
        p = us.cast(V(fx, y, 1.0), V(0, 0, -1))[0]
        if p is not None:
            out.append(part(ball_bend(geo.superquad(f"shoe-lace{k}{s}", (0.06 - 0.007 * k, 0.012, 0.01),
                                                    M["graphite"], p + V(0, 0, 0.004), n=2.6, res=2), s), f"foot{s}"))
    out.append(part(geo.superquad(f"shoe-tongue{s}", (0.054, 0.06, 0.04), M["graphite"], V(fx, -0.03, 0.222),
                                  n=2.4, res=5), f"foot{s}"))
    out.append(part(geo.ring(f"shoe-collar{s}", 0.064, 0.017, M["graphite"], V(fx, 0.04, 0.215), (0, 0.3, 1),
                             segs=24, sides=6, squash=0.8), f"foot{s}"))
    out.append(part(geo.ring(f"shoe-loop{s}", 0.05, 0.013, M["mint"], V(fx, -0.062, 0.205), (0, -0.55, 1),
                             segs=20, sides=6), f"foot{s}"))
    out.append(part(geo.superquad(f"shoe-heel{s}", (0.095, 0.05, 0.062), M["violet"], V(fx, L0 - 0.045, 0.135),
                                  n=(2.4, 2.4, 2.6), res=5), f"foot{s}"))
    out.append(part(geo.superquad(f"shoe-heel-cap{s}", (0.088, 0.034, 0.028), M["mint"], V(fx, L0 - 0.03, 0.185),
                                  n=2.5, res=5), f"foot{s}"))
    # the ankle's works: a graphite housing round the joint above the heel
    out.append(part(geo.superquad(f"ankle-housing{s}", (0.064, 0.075, 0.052), M["graphite"],
                                  V(fx, ANKLE.y + 0.03, ANKLE.z - 0.02), n=2.4, res=5), f"foot{s}"))
    return out


def hand(R, s, sx, wrist, fw, M):
    """A hand at the end of the forearm, hanging a little steeper than it: a violet body with a graphite pad
    on the palm and a mint cuff at the wrist, and four graphite digits (thumb and three fingers) of three
    segments, brass rings at the knuckles, violet plates on the backs of the fingers' middle segments and a
    mint ring round the thumb's root. Declares the hand's bones on `R` as it goes. The palm faces back (+Y),
    so the thumb is on the edge nearer the body."""
    out = []
    along = (fw + V(0, 0, -0.3)).normalized()
    palm_n = V(0, 1, 0)
    palm_n = (palm_n - along * palm_n.dot(along)).normalized()
    across = along.cross(palm_n).normalized()          # over the back of the hand towards the thumb's edge
    if across.x * sx > 0:
        across = -across
    base = wrist + along * 0.025
    L = 0.115
    R.bone(f"hand{s}", base - along * 0.022, base + along * L, f"forearm{s}", z=palm_n)
    R.bone(f"grip{s}", base + along * 0.08 + palm_n * 0.055, base + along * 0.08 + palm_n * 0.055 + along * 0.06,
           f"hand{s}", z=palm_n)
    Mh = Matrix.Translation(base + along * (L / 2)) @ Matrix((across, palm_n, along)).transposed().to_4x4()
    back = geo.superquad(f"hand-back{s}", (0.078, 0.038, L / 2), M["violet"], (0, 0, 0), n=(2.4, 2.2, 2.6), res=5,
                         shape=lambda p, q: Vector((p.x * (1 - 0.14 * (1 - q.z) / 2), p.y, p.z)))
    out.append(part(geo.transform(back, Mh @ Matrix.Translation((0, -0.004, 0))), f"hand{s}"))
    palm = geo.superquad(f"hand-palm{s}", (0.074, 0.03, L / 2 - 0.004), M["violet"], (0, 0, 0), n=2.6, res=5)
    out.append(part(geo.transform(palm, Mh @ Matrix.Translation((0, 0.018, 0))), f"hand{s}"))
    pad = geo.superquad(f"hand-pad{s}", (0.05, 0.012, L / 2 - 0.02), M["graphite"], (0, 0, 0), n=2.4, res=4)
    out.append(part(geo.transform(pad, Mh @ Matrix.Translation((0, 0.042, 0.006))), f"hand{s}"))
    cuff = geo.superquad(f"hand-cuff{s}", (0.084, 0.045, 0.014), M["mint"], (0, 0, 0), n=(2.6, 2.4, 3.0), res=4)
    out.append(part(geo.transform(cuff, Mh @ Matrix.Translation((0, 0.002, -L / 2 + 0.014))), f"hand{s}"))

    def digit(name, root, direction, lengths, radius):
        """Three rounded cylinders end to end, a thin brass collar at each knuckle and a domed tip; a violet
        plate on the back of the middle one."""
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
            out.append(part(geo.lathe(f"{name}{k}{s}", prof, M["graphite"], p, d, segs=10, y_hint=palm_n), bn))
            if k:
                out.append(part(geo.ring(f"{name}-ring{k}{s}", r * 0.93, r * 0.13, M["brass"], p, d, segs=10,
                                         sides=4, squash=1.5), bn))
            if k == 1 and name != "thumb":
                pl = geo.superquad(f"{name}-plate{s}", (r * 0.9, r * 0.32, ln * 0.4), M["violet"], (0, 0, 0),
                                   n=(2.8, 2.2, 3.2), res=4)
                side = d.cross(palm_n).normalized()
                Mp = Matrix.Translation(p + d * (ln * 0.5) - palm_n * (r * 0.84)) @ \
                    Matrix((side, palm_n, d)).transposed().to_4x4()
                out.append(part(geo.transform(pl, Mp), bn))
            p = p + d * ln
            parent = bn

    tip_c = base + along * L
    for k, nm, ln in ((-1.0, "index", 0.17), (0.0, "middle", 0.19), (1.0, "ring", 0.165)):
        root = tip_c - along * 0.018 + across * (0.05 * -k) + palm_n * 0.006
        d = (along + across * (-k * 0.14)).normalized()
        digit(nm, root, d, (ln * 0.38, ln * 0.33, ln * 0.29), 0.026)
    troot = base + along * 0.035 + across * 0.072 + palm_n * 0.022
    tdir = (along * 0.55 + across * 0.8 + palm_n * 0.3).normalized()
    out.append(part(geo.ring(f"thumb-cuff{s}", 0.03, 0.01, M["mint"], troot + tdir * 0.004, tdir, segs=20,
                             sides=8, squash=1.5), f"hand{s}"))
    digit("thumb", troot, tdir, (0.058, 0.05, 0.044), 0.027)
    return out


# ------------------------------------------------------------------------------------------- views
def sheet_pose(R):
    """The model sheet's stance: toes turned out, and the brows pulled into his mischief (the left one up)."""
    R.rest()
    for s, sx in rig.SIDES:
        R.turn_world(f"foot{s}", (0, 0, 1), sx * 28.0)
    pb = R.ob.pose.bones
    for name, up in (("brow_in_L", 0.012), ("brow_mid_L", 0.016), ("brow_out_L", 0.004)):
        pb[name].location = (0.0, up, 0.0)               # along the bone: up the face
    bpy.context.view_layer.update()


def render_views(out, views, samples, res):
    focus = V(0, 0, 1.0)
    studio.sheet_lights(focus, 0.85)
    studio.floor(0.0)
    studio.settings(res=res, samples=samples, engine="CYCLES", view=opt("--view", "Standard"),
                    exposure=float(opt("--exposure", "-0.9")))
    for v in views:
        if v == "face":
            cam = studio.camera("cam-face", V(0, 0, 1.62), 0, 3.4, lens=110)
        elif v == "hand":
            cam = studio.camera("cam-hand", V(0.6, -0.03, 0.64), 25, 2.5, lens=110)
        elif v == "three":
            cam = studio.camera("cam-three", focus, 32, 4.7, lens=60)
        else:
            # "side" is the sheet's side view, which faces screen right: seen from the character's right.
            ang = {"front": 0, "side": -90, "back": 180, "left": 90, "right": -90}[v]
            cam = studio.camera(f"cam-{v}", focus, ang, 12.0, ortho=2.3)
        bpy.context.scene.camera = cam
        studio.render(Path(out) / f"zip-{v}.png")


def main():
    geo.reset()
    R, parts, M = build()
    meshes = R.finalize(parts)
    tris = sum(len(p.vertices) - 2 for m in meshes.values() for p in m.data.polygons)
    print(f"ZIP bones={len(R.order)} verts={ {k: len(v.data.vertices) for k, v in meshes.items()} } tris={tris}")
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
