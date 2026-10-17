"""Archie, as drawn on his model sheet: built, rigged and skinned from nothing but this script.

    blender -b --factory-startup --python art/pals/archie.py -- [--views front,side,back,three,face]
            [--out DIR] [--samples N] [--res WxH] [--sheet-pose] [--save PATH] [--no-render]

The reference is `Archie robot model reference sheet.png` (the sheets live outside the repository; their
landmarks are transcribed in art/pals/reference.md). Glazed ceramic white, graphite and lime: an egg of a
head with lime-iris eyes, heavy brows, a smirk and a graphite-and-lime crest swept forward; headphone cups
for ears; a graphite neck and spine; the Atlas Core's octagonal dock in his belly; four-digit hands with brass
knuckle rings; chunky sneakers.

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
        mouth=mat.principled("mouth", "#3a1216", rough=0.6, spec=0.3),
        teeth=mat.principled("teeth", "#f6f4ef", rough=0.18, coat=0.8),
        glint=mat.principled("glint", "#ffffff", rough=0.3, emit="#ffffff", strength=2.5),
        eye=mat.eye_material("archie-eye", inner_hex="#dcf55e", outer_hex="#77a40a", limbal_hex="#1a2604",
                             iris_r=0.37, pupil_r=0.155),
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
HEAD_C = V(0.0, SY(742), Z(160))
HEAD_R = (0.242, 0.262, 0.27)                    # half width, half depth, half height


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
    crest_path = [(0.0, 728, 128), (0.03, 744, 100), (0.09, 765, 80), (0.165, 787, 66), (0.228, 803, 57)]
    cp = [V(x, SY(px), Z(pz)) for x, px, pz in crest_path]
    R.bone("crest_1", cp[0], cp[1], "head", z=(0, -1, 0.3))
    R.bone("crest_2", cp[1], cp[3], "crest_1", z=(0, -1, 0.3))
    R.bone("crest_3", cp[3], cp[4], "crest_2", z=(0, -1, 0.3))
    for s, sx in rig.SIDES:
        R.bone(f"ear{s}", (sx * 0.27, SY(722), Z(180)), (sx * 0.34, SY(722), Z(180)), "head", z=(0, -1, 0))
    R.bone("core", (0, -0.11, Z(342)), (0, -0.23, Z(342)), "spine", z=(0, 0, 1))
    for s, sx in rig.SIDES:
        R.bone(f"shoulder{s}", (sx * 0.08, 0, Z(262)), (sx * SHOULDER.x, 0, SHOULDER.z), "chest")
        R.bone(f"upper_arm{s}", (sx * SHOULDER.x, 0, SHOULDER.z), (sx * ELBOW.x, 0, ELBOW.z), f"shoulder{s}")
        R.bone(f"forearm{s}", (sx * ELBOW.x, 0, ELBOW.z), (sx * WRIST.x, 0, WRIST.z), f"upper_arm{s}")
        R.bone(f"thigh{s}", (sx * HIP_X, 0, HIP_Z), (sx * KNEE_X, -0.005, KNEE_Z), "hips")
        R.bone(f"shin{s}", (sx * KNEE_X, -0.005, KNEE_Z), (sx * ANKLE_X, 0.03, ANKLE_Z), f"thigh{s}")
        R.bone(f"foot{s}", (sx * ANKLE_X, 0.03, ANKLE_Z), (sx * 0.222, -0.25, 0.075), f"shin{s}", z=(0, 0, 1))
        R.bone(f"toe{s}", (sx * 0.222, -0.25, 0.075), (sx * 0.222, -0.46, 0.075), f"foot{s}", z=(0, 0, 1))

    # ---- head --------------------------------------------------------------------------------------
    def head_shape(p, q):
        # Broad cranium, full cheeks, a rounded chin; the face flatter than the back of the skull.
        below = max(0.0, -q.z)
        sx = 1.0 - 0.27 * below ** 1.9
        sy = 1.0 - 0.2 * below ** 1.8
        p = Vector((p.x * sx, p.y * sy, p.z))
        if q.y < 0:
            p.y *= 0.9 - 0.05 * max(0.0, q.z)
        else:
            p.y *= 1.05
        p.y -= 0.03 * below ** 2                # the chin a touch forward
        return p

    skull = add(geo.superquad("head-shell", HEAD_R, M["ceramic"], HEAD_C, n=2.15, shape=head_shape, res=15),
                "head")
    geo.box_uv(skull, 0.5)
    surf = geo.Surface(skull)

    # Ear cups: layered on the X axis, as on the head-profile panel.
    for s, sx in rig.SIDES:
        c = V(sx * 0.262, SY(722), Z(181))
        ax = (sx, 0, 0)
        add([geo.disc(f"ear-housing{s}", 0.11, 0.075, M["graphite"], c, ax, bevel_r=0.022, segs=36),
             geo.ring(f"ear-lime{s}", 0.096, 0.017, M["lime"], c + V(sx * 0.038, 0, 0), ax, segs=32, sides=6,
                      squash=0.8),
             geo.disc(f"ear-face{s}", 0.08, 0.03, M["graphite"], c + V(sx * 0.044, 0, 0), ax, bevel_r=0.01,
                      segs=32),
             geo.ring(f"ear-lime2{s}", 0.054, 0.0075, M["lime"], c + V(sx * 0.06, 0, 0), ax, segs=32, sides=6),
             geo.disc(f"ear-lens{s}", 0.044, 0.02, M["lens"], c + V(sx * 0.06, 0, 0), ax, bevel_r=0.008,
                      segs=28, bulge=0.006),
             geo.disc(f"ear-pin{s}", 0.012, 0.012, M["brass"], c + V(sx * 0.072, 0, 0), ax, segs=12)],
            f"ear{s}")

    # The crest: a fin of graphite rising from the crown and sweeping forward, lime along its leading edge
    # and its outer (character's left) flank.
    depth = [0.17, 0.135, 0.09, 0.045, 0.004]       # half-size in the plane of symmetry
    thick = [0.062, 0.058, 0.046, 0.028, 0.004]     # half-size across
    pts, dd, tt = [], [], []
    for i in range(len(cp) - 1):                    # densify the path
        for k in range(4):
            t = k / 4
            pts.append(cp[i].lerp(cp[i + 1], t))
            dd.append(lerp(depth[i], depth[i + 1], t))
            tt.append(lerp(thick[i], thick[i + 1], t))
    pts.append(cp[-1])
    dd.append(depth[-1])
    tt.append(thick[-1])
    pts.insert(0, cp[0] + V(0, 0.01, -0.06))       # root it inside the skull
    dd.insert(0, 0.16)
    tt.insert(0, 0.05)
    crest = geo.sweep("crest", pts, tt, dd, M["graphite"], n=2.4, segs=16, up=(0, -1, 0.15))
    # The lime: a band capping the fin's leading edge from the brow to the tip, a little proud of it.
    T_, N_, B_ = geo._frames(pts, (0, -1, 0.15))
    lead_pts, lead_w, lead_h = [], [], []
    for i in range(2, len(pts)):
        lead_pts.append(pts[i] + N_[i] * dd[i] * 0.78 + B_[i] * tt[i] * 0.42)
        lead_w.append(tt[i] * 0.72 + 0.002)
        lead_h.append(max(0.004, min(0.036, dd[i] * 0.3)))
    lime_band = geo.sweep("crest-lime", lead_pts, lead_w, lead_h, M["lime"], n=2.4, segs=14, up=(0, -1, 0.15))
    geo.subsurf(lime_band, 1)
    parts.append(lime_band)
    geo.subsurf(crest, 1)
    zr0, zr1 = Z(140), Z(57)
    for ob in (crest, lime_band):
        vgs = [ob.vertex_groups.new(name=f"crest_{i}") for i in (1, 2, 3)]
        for v in ob.data.vertices:
            t = (v.co.z - zr0) / (zr1 - zr0)
            w = [max(0.0, 1 - abs(t - c) / 0.4) + 1e-6 for c in (0.0, 0.5, 1.0)]
            tot = sum(w)
            for vg, x in zip(vgs, w):
                if x / tot > 1e-3:
                    vg.add([v.index], x / tot, "REPLACE")
    parts.append(crest)

    # Eyes, set into the face, gazing straight out.
    eye_r = 17.5 * PX
    for s, sx in rig.SIDES:
        ex, ez = sx * 0.106, Z(171)
        front = surf.front(ex, ez)
        c = V(ex, front.y + eye_r * 0.45, ez)
        look = V(sx * 0.05, -1, 0.0).normalized()
        R.bone(f"eye{s}", c, c + look * 0.08, "head", z=(0, 0, 1))
        R.bone(f"lid_up{s}", c, c + look * 0.07, "head", z=(0, 0, 1))
        R.bone(f"lid_lo{s}", c, c + look * 0.06, "head", z=(0, 0, 1))
        eparts, _ = face.eye(f"eye{s}", sx, c, eye_r, look,
                             dict(eye=f"eye{s}", lid_up=f"lid_up{s}", lid_lo=f"lid_lo{s}", head="head"),
                             M["eye"], M["ceramic"], M["graphite"], M["glint"], lash=0.2, lash_flick=0.4,
                             up_open=34, lo_open=62, lid_roll=-5, res=8)
        parts.extend(eparts)

    # Brows: heavy graphite bars, the inner end low and blunt, arching to a tapered outer end.
    for s, sx in rig.SIDES:
        pts2d = [(sx * 0.032, Z(151)), (sx * 0.065, Z(143)), (sx * 0.105, Z(138)), (sx * 0.145, Z(139)),
                 (sx * 0.178, Z(146)), (sx * 0.198, Z(156))]
        names = [f"brow_in{s}", f"brow_mid{s}", f"brow_out{s}"]
        for nm, (bx, bz) in zip(names, [pts2d[0], pts2d[2], pts2d[-1]]):
            p = surf.front(bx, bz)
            R.bone(nm, p, p + V(0, 0, 0.05), "head", z=(0, -1, 0))
        parts.append(face.brow(f"brow{s}", sx, surf, pts2d, 0.03, 0.017, M["graphite"], names,
                               taper=(0.8, 1.0, 0.4)))

    # Mouth: rest is a closed, pleased smile; `grin` is the sheet's open smirk and is on by default.
    shapes = dict(
        rest=dict(w=0.11, smile=0.026, thick=0.01, lift_L=0.008),
        grin=dict(w=0.14, smile=0.036, top=0.006, bot=0.044, teeth=0.42, thick=0.009, lift_L=0.03, lift_R=-0.004),
        smile=dict(w=0.125, smile=0.04, bot=0.014, thick=0.01),
        wide=dict(w=0.15, smile=0.032, top=0.014, bot=0.08, teeth=0.3, low_teeth=0.12, round=0.3),
        open=dict(w=0.09, smile=0.0, top=0.024, bot=0.056, round=0.6, teeth=0.18),
        oh=dict(w=0.045, smile=0.0, top=0.032, bot=0.036, round=1.0, thick=0.007),
        frown=dict(w=0.105, smile=-0.032, thick=0.01),
        flat=dict(w=0.095, smile=0.0, thick=0.009),
        smirk_L=dict(w=0.115, smile=0.008, lift_L=0.045, lift_R=-0.006, thick=0.01),
        smirk_R=dict(w=0.115, smile=0.008, lift_R=0.045, lift_L=-0.006, thick=0.01),
        grit=dict(w=0.13, smile=-0.004, top=0.018, bot=0.02, teeth=0.5, low_teeth=0.5, thick=0.007),
        ee=dict(w=0.145, smile=0.032, top=0.009, bot=0.026, teeth=0.55, low_teeth=0.3),
    )
    mth = face.mouth("mouth", surf, (0.008, Z(201)), shapes, (M["mouth"], M["teeth"]))
    mth.data.shape_keys.key_blocks["grin"].value = 1.0
    parts.append(mth)

    # Neck: a graphite column of rings on a core.
    nz0, nz1 = Z(252), Z(214)
    add(geo.segment("neck-core", (0, 0, nz0 - 0.03), (0, 0, nz1 + 0.05), 0.062, M["graphite"], res=7), "neck")
    for i in range(3):
        z = lerp(nz0, nz1, (i + 0.5) / 3)
        add(geo.disc(f"neck-ring{i}", 0.084 - 0.005 * i, 0.03, M["graphite"], (0, 0.005, z), (0, 0, 1),
                     bevel_r=0.012, segs=24), "neck" if i else "chest")

    # ---- torso -------------------------------------------------------------------------------------
    CH_C = V(0, -0.025, Z(279))

    def chest_shape(p, q):
        # Wide at the shoulders, tapering to the waist; pecs forward, the back flatter.
        t = (q.z + 1) / 2                       # 0 bottom .. 1 top
        sx = lerp(0.72, 1.0, smooth(0.0, 0.7, t))
        p = Vector((p.x * sx, p.y, p.z))
        if q.y < 0:
            p.y *= 1.0 + 0.1 * math.sin(math.pi * t) * (1 - 0.5 * abs(q.x))
        else:
            p.y *= 0.86
        return p

    chest = add(geo.superquad("chest-shell", (0.278, 0.222, 0.186), M["ceramic"], CH_C, n=(2.6, 2.4, 3.3),
                              shape=chest_shape, res=13), "chest")
    geo.box_uv(chest, 0.5)
    csurf = geo.Surface(chest)

    def on_chest(name, xz, r, bone="chest", offset=0.002):
        pts = [p for p in (csurf.front(x, z, offset=offset) for x, z in xz) if p is not None]
        return add(geo.tube(name, pts, r, M["lime"], segs=7), bone)

    # Lime piping: the chevron under the pecs, the collar, and the V seams out to the shoulders.
    on_chest("chest-chevron", [(u * 0.25, Z(291) - 0.03 * (1 - abs(u)) ** 1.5 + 0.03 * abs(u) ** 3)
                               for u in (-1 + 2 * i / 26 for i in range(27))], 0.0095)
    on_chest("chest-collar", [(u * 0.115, Z(252) - 0.045 * (1 - u * u)) for u in (-1 + 2 * i / 22 for i in range(23))],
             0.012)
    for sx in (1, -1):
        on_chest(f"chest-seam{'_L' if sx > 0 else '_R'}",
                 [(sx * lerp(0.115, 0.255, t), lerp(Z(253), Z(266), t)) for t in (i / 11 for i in range(12))], 0.0075)

    # Graphite under-armour: the spine down the back, flush.
    add(geo.segment("spine-back", (0, 0.14, Z(252)), (0, 0.14, Z(328)), 0.075, M["graphite"], flat=0.62, n=2.8,
                    res=7), "chest")
    for i in range(5):
        z = lerp(Z(258), Z(326), i / 4)
        add(geo.superquad(f"spine-plate{i}", (0.068, 0.02, 0.015), M["graphite"], (0, 0.158, z), n=2.6, res=3),
            "chest")

    # Abdomen: graphite ribs round a core, and the Atlas Core's octagonal dock in front.
    AB_Z0, AB_Z1 = Z(368), Z(312)
    add(geo.segment("abdomen-core", (0, 0.0, AB_Z0 - 0.02), (0, 0.0, AB_Z1 + 0.03), 0.14, M["graphite"],
                    flat=0.85, n=2.4, res=8), "spine")
    for i in range(4):
        z = lerp(AB_Z0 + 0.02, AB_Z1 - 0.02, i / 3)
        rr = 0.155 - 0.012 * abs(i - 1.5)
        add(geo.superquad(f"abdomen-rib{i}", (rr, rr * 0.84, 0.023), M["graphite"], (0, 0.012, z), n=(2.4, 2.4, 3),
                          res=5), "spine")
    dock_c = V(0, -0.125, Z(342))
    turn = Matrix.Translation(dock_c) @ Matrix.Rotation(math.pi / 8, 4, (0, 1, 0)) @ Matrix.Translation(-dock_c)
    frame = geo.lathe("dock-frame", geo.rounded_profile(0.118, 0.042, 0.012, r_inner=0.085), M["graphite"],
                      dock_c, (0, -1, 0), segs=8, y_hint=(0, 0, 1))
    add(geo.transform(frame, turn), "spine")
    well = geo.disc("dock-well", 0.088, 0.03, M["rubber"], dock_c + V(0, 0.018, 0), (0, -1, 0), segs=8)
    add(geo.transform(well, turn), "spine")
    add(geo.superquad("dock-clasp", (0.032, 0.018, 0.013), M["lime"], dock_c + V(0, -0.012, 0.11), n=2.6, res=4),
        "spine")

    # Pelvis: a ceramic brief, a lime-edged plate in front, graphite hip joints at its sides.
    PV_C = V(0, 0.0, Z(392))

    def pelvis_shape(p, q):
        t = (q.z + 1) / 2
        sx = lerp(0.6, 1.0, smooth(0.0, 0.9, t))
        return Vector((p.x * sx, p.y * lerp(0.8, 1.0, t), p.z))

    pelvis = add(geo.superquad("pelvis-shell", (0.22, 0.172, 0.118), M["ceramic"], PV_C, n=(2.5, 2.3, 2.4),
                               shape=pelvis_shape, res=10), "hips")
    geo.box_uv(pelvis, 0.5)
    psurf = geo.Surface(pelvis)
    # a U-shaped panel: down from the waistband and round under
    plate = [psurf.front(0.06 * math.sin(a), PV_C.z + 0.085 - 0.11 * math.cos(a * 0.9), offset=0.002)
             for a in (lerp(-1.5, 1.5, i / 20) for i in range(21))]
    add(geo.tube("pelvis-plate", [p for p in plate if p], 0.0075, M["lime"], segs=7), "hips")
    for s, sx in rig.SIDES:
        c = V(sx * 0.172, 0.0, HIP_Z)
        add(geo.disc(f"hip-joint{s}", 0.086, 0.075, M["graphite"], c + V(sx * 0.035, 0, 0), (sx, 0, 0),
                     bevel_r=0.022, segs=28), f"thigh{s}")
        add(geo.ring(f"hip-ring{s}", 0.066, 0.0085, M["lime"], c + V(sx * 0.074, 0, 0), (sx, 0, 0), segs=28, sides=6),
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

    R.build()
    return R, parts, M


def stripe(name, surf, pts3d, centre_fn, r, m, offset=0.002):
    """Lime trim laid onto a limb: each guide point is pushed onto the surface along the line from its own
    axis point (`centre_fn(p)`) outwards."""
    out = []
    for p in pts3d:
        q = surf.toward(p, centre_fn(p), offset=offset, far=0.4)
        if q is not None:
            out.append(q)
    return geo.tube(name, out, r, m, segs=6) if len(out) > 2 else None


def leg(M, both):
    s, sx = "_L", 1
    hip = V(sx * HIP_X, 0, HIP_Z)
    knee = V(sx * KNEE_X, -0.005, KNEE_Z)
    ankle = V(sx * ANKLE_X, 0.03, ANKLE_Z)
    th = geo.segment(f"thigh{s}", hip + V(sx * 0.014, 0, -0.035), knee + V(0, 0, 0.075), 0.124, M["ceramic"],
                     rb=0.098, flat=0.93, bulge=0.07, front=0.07, n=2.3, res=8)
    geo.box_uv(th, 0.5)
    both(th, f"thigh{s}")
    tsurf = geo.Surface(th)
    axis = lambda p: hip.lerp(knee, max(0.0, min(1.0, (HIP_Z - p.z) / (HIP_Z - KNEE_Z))))
    st = stripe(f"thigh-stripe{s}", tsurf,
                [V(sx * (0.3 - 0.02 * t), -0.04 - 0.03 * t, lerp(HIP_Z - 0.06, KNEE_Z + 0.12, t)) for t in
                 (i / 10 for i in range(11))], axis, 0.0075, M["lime"])
    if st:
        both(st, f"thigh{s}")
    band = geo.ring(f"thigh-band{s}", 0.1, 0.009, M["lime"], knee + V(0, -0.002, 0.13), (0.03, 0, 1), segs=28, sides=6,
                    squash=1.2)
    both(band, f"thigh{s}")
    # knee: a graphite hinge with lime rings, and a ceramic cap with lime edging in front
    both(geo.disc(f"knee-joint{s}", 0.074, 0.18, M["graphite"], knee, (1, 0, 0), bevel_r=0.03, segs=28), f"shin{s}")
    for k, off in enumerate((-1, 1)):
        both(geo.ring(f"knee-ring{k}{s}", 0.066, 0.0085, M["lime"], knee + V(off * 0.088, 0, 0), (1, 0, 0), segs=28,
                      sides=6), f"shin{s}")
    cap = geo.superquad(f"kneecap{s}", (0.092, 0.05, 0.112), M["ceramic"], knee + V(0, -0.09, 0.005),
                        n=(2.3, 2.0, 2.4), res=8,
                        shape=lambda p, q: Vector((p.x, p.y + 0.022 * (q.x * q.x + q.z * q.z), p.z)))
    geo.box_uv(cap, 0.5)
    both(cap, f"shin{s}")
    ksurf = geo.Surface(cap)
    edge = [ksurf.front(knee.x + 0.077 * math.sin(a), knee.z + 0.005 + 0.094 * math.cos(a), offset=0.001)
            for a in (math.tau * i / 30 for i in range(30))]
    edge = [p for p in edge if p]
    if len(edge) > 4:
        both(geo.tube(f"kneecap-edge{s}", edge, 0.008, M["lime"], segs=6, caps=False, closed=True), f"shin{s}")
    sh = geo.segment(f"shin{s}", knee + V(0, 0, -0.065), ankle + V(0, 0, 0.045), 0.1, M["ceramic"], rb=0.078,
                     flat=0.95, bulge=0.06, n=2.3, res=8,
                     shape=lambda p, q: Vector((p.x, p.y + (0.028 * (1 - q.z * q.z) if q.y > 0 else 0), p.z)))
    geo.box_uv(sh, 0.5)
    both(sh, f"shin{s}")
    both(geo.ring(f"shin-band{s}", 0.092, 0.0085, M["lime"], knee + V(0, 0.004, -0.09), (0.02, -0.08, 1), segs=28,
                  sides=6, squash=1.2), f"shin{s}")
    both(geo.disc(f"ankle-joint{s}", 0.066, 0.16, M["graphite"], ankle, (1, 0, 0), bevel_r=0.026, segs=24), f"foot{s}")
    both(geo.disc(f"ankle-disc{s}", 0.054, 0.03, M["graphite"], ankle + V(sx * 0.082, 0, 0), (sx, 0, 0),
                  bevel_r=0.01, segs=24), f"foot{s}")
    both(geo.ring(f"ankle-ring{s}", 0.043, 0.0065, M["lime"], ankle + V(sx * 0.098, 0, 0), (sx, 0, 0), segs=24,
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
    both(geo.disc(f"shoulder-joint{s}", 0.08, 0.065, M["graphite"], sh_ + V(-sx * 0.02, 0, 0.0), (sx, 0, 0),
                  bevel_r=0.02, segs=28), f"upper_arm{s}")
    # The pad: a ceramic cap over the joint, lime round its lower edge.
    pad_c = sh_ + V(sx * 0.02, 0, 0.055)

    def pad_shape(p, q):
        z = p.z * (1.0 if q.z > -0.15 else 0.5)
        return Vector((p.x * (1 - 0.1 * max(0.0, -q.x * sx)), p.y, z))

    pad = geo.superquad(f"shoulder-pad{s}", (0.13, 0.13, 0.115), M["ceramic"], pad_c, n=2.25, res=8, shape=pad_shape)
    geo.box_uv(pad, 0.5)
    both(pad, f"upper_arm{s}")
    rim = [pad_c + V(math.cos(a) * 0.124, math.sin(a) * 0.126, -0.058) for a in (math.tau * i / 36 for i in range(36))]
    both(geo.tube(f"shoulder-pad-rim{s}", rim, 0.012, M["lime"], segs=7, caps=False, closed=True), f"upper_arm{s}")
    ua = geo.segment(f"upper-arm{s}", sh_ + up * 0.06, el - up * 0.03, 0.086, M["ceramic"], rb=0.074, bulge=0.08,
                     flat=0.95, n=2.25, res=8, y_hint=(0, 0, 1))
    geo.box_uv(ua, 0.5)
    both(ua, f"upper_arm{s}")
    both(geo.ring(f"upper-arm-band{s}", 0.074, 0.0085, M["lime"], el - up * 0.075, up, segs=28, sides=6, squash=1.4),
         f"upper_arm{s}")
    both(geo.disc(f"elbow-joint{s}", 0.066, 0.135, M["graphite"], el, (0, 1, 0), bevel_r=0.024, segs=24), f"forearm{s}")
    for k, off in enumerate((-1, 1)):
        both(geo.ring(f"elbow-ring{k}{s}", 0.057, 0.0075, M["lime"], el + V(0, off * 0.067, 0), (0, 1, 0), segs=24,
                      sides=6), f"forearm{s}")
    fa = geo.segment(f"forearm{s}", el + fw * 0.045, wr - fw * 0.035, 0.084, M["ceramic"], rb=0.066, bulge=0.06,
                     flat=0.93, n=2.25, res=8, y_hint=(0, 0, 1),
                     shape=lambda p, q: Vector((p.x * (1 + 0.08 * max(0.0, -q.z)), p.y, p.z)))
    geo.box_uv(fa, 0.5)
    both(fa, f"forearm{s}")
    fsurf = geo.Surface(fa)
    out_dir = V(fw.z, 0, -fw.x).normalized() * (1 if sx > 0 else -1)      # the forearm's outer, upper edge
    if out_dir.z < 0:
        out_dir = -out_dir
    st = stripe(f"forearm-stripe{s}", fsurf,
                [el.lerp(wr, t) + out_dir * 0.2 + V(0, -0.03, 0) for t in (lerp(0.2, 0.8, i / 9) for i in range(10))],
                lambda p: el + fw * (p - el).dot(fw), 0.0075, M["lime"])
    if st:
        both(st, f"forearm{s}")
    both(geo.ring(f"wrist-cuff{s}", 0.066, 0.012, M["lime"], wr - fw * 0.1, fw, segs=28, sides=6, squash=1.6),
         f"forearm{s}")
    both(geo.disc(f"wrist-joint{s}", 0.05, 0.055, M["graphite"], wr, fw, bevel_r=0.013, segs=20), f"hand{s}")
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
