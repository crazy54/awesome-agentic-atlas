"""Zip and Brick as the Atlas Core projects them: holo-zip (the tiny Zip the hostile takeover waves straight
through its gate, and the pocket rave's DJ) and holo-brick (the pocket rave's bouncer). Built the way
props_holo.py builds the bootleg Archie and the agents, but each on its own pal's skeleton, bone for bone (the
same names and rest frames, read from zip.build() and brick.build()), so any clip made for that pal plays on
it: a bit with Zip in its cast plays `s.zip`'s clips on holo-zip. Each also carries a few of its pal's own
everyday clips, baked from clips/zip_base.py and clips/brick_base.py, for bits its pal isn't in:

    holo-zip    idle  walk  wave  cheer  dance
    holo-brick  idle  bouncer  guard  guard-hold  shake-head  nod  raise-brow

They are built at their pals' own sizes (Zip 1.75 m, Brick 2.75 m to the head's top); the page scales them
down to stand in a world, the same factor for every figure so they keep the pals' sizes against each other.
Materials `holo_body` and `holo_accent`, in each pal's own colours as light (Zip violet and mint, Brick orange
and cream), so they read apart from the cyan agents; the page's figure shader draws them see-through.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

from mathutils import Vector

import props_kit as K
from kit import anim, geo, mat
from props_kit import V, lerp, prop

sys.path.insert(0, str(Path(__file__).resolve().parent / "clips"))

ZIP_CLIPS = ("idle", "walk", "wave", "cheer", "dance")
BRICK_CLIPS = ("idle", "bouncer", "guard", "guard-hold", "shake-head", "nod", "raise-brow")


def _materials(body_hex, accent_hex):
    body = mat.principled("holo_body", body_hex, rough=0.3, emit=body_hex, strength=2.0)
    accent = mat.principled("holo_accent", accent_hex, rough=0.3, emit=accent_hex, strength=2.5)
    return body, accent


def _pal(p, pal, wanted):
    """Build `pal` (its module and its base clips), declare its skeleton on `p` exactly as it declares it,
    and hand `p` the clips named in `wanted`, solved against the pal's own body. Returns the bone specs and
    the pal's module."""
    import common
    mod = importlib.import_module(pal)
    R, _, _ = mod.build()
    specs = {n: dict(R.specs[n]) for n in R.order}
    order = list(R.order)
    lib = importlib.import_module(f"{pal}_base")
    body = common.Body(anim.Skeleton(R.ob), **getattr(lib, "BODY", {}))
    body.lib = lib
    made = lib.clips(body)
    geo.reset()
    for n in order:
        s = specs[n]
        p.bone(n, s["head"], s["tail"], parent=s["parent"], z=s["z"])
    for name in wanted:
        c = made[name]
        c.post.append(_still)
        p.pose_clip(c)
    return specs, mod


QUIET = ("eye", "lid_", "brow_", "horn_", "ear_", "grip_", "thumb_", "index_", "middle_", "ring_")


def _still(t, pose, skel):
    """A figure a few centimetres tall shows none of a face's or a hand's play: leave those bones at rest, so
    their channels are never baked (the clip files are mostly them otherwise)."""
    for d in (pose.rot, pose.quat, pose.loc):
        for b in [b for b in d if b.startswith(QUIET)]:
            del d[b]
    pose.face.clear()
    return pose


def _seg(name, specs, bone, m, r, r2=None, ext=0.0, segs=8):
    s = specs[bone]
    a, b = Vector(s["head"]), Vector(s["tail"])
    d = (b - a).normalized()
    return K.capsule(name, a + d * ext, b - d * ext, r, m, segs=segs, rings=1, r2=r2)


def _hands(p, specs, body, accent, hand_r, finger_r, palm_scale=(1, 0.7, 1)):
    for sd in ("_L", "_R"):
        h = specs["hand" + sd]
        a, b = Vector(h["head"]), Vector(h["tail"])
        p.add(K.ball("palm" + sd, hand_r, body, a.lerp(b, 0.45), res=2, scale=palm_scale), "hand" + sd)
        for f in ("thumb", "index", "middle", "ring"):
            fa, fb = Vector(specs[f"{f}_1{sd}"]["head"]), Vector(specs[f"{f}_3{sd}"]["tail"])
            p.add(K.capsule(f"{f}{sd}", fa, fb, finger_r * (1.15 if f == "thumb" else 1.0), body, segs=5, rings=1),
                  f"{f}_1{sd}")


@prop("holo-zip", "The hostile takeover (the tiny Zip the agents wave straight through); The pocket rave (the DJ)",
      "floor between the feet, facing -Y, at Zip's own size (1.75 m) with his skeleton (scale it down with the "
      "other figures); materials holo_body (violet), holo_accent (mint)",
      rig="Zip's whole skeleton (plays any Zip clip): idle, walk, wave, cheer, dance")
def holo_zip(p):
    specs, Z = _pal(p, "zip", ZIP_CLIPS)
    body, accent = _materials("#b98cff", "#6ff0c8")
    hc = Vector(Z.HEAD_C)
    # the wide helmet, long front to back, flattening under the chin, the faceplate cut back
    def head_shape(q, u):
        below = max(0.0, -u.z)
        return V(q.x * (1 - 0.18 * below ** 2), q.y * (1 - 0.1 * below ** 2), q.z)

    head = geo.superquad("zip-head", (0.33, 0.34, 0.25), body, hc + V(0, 0.02, 0.0), n=2.3, shape=head_shape, res=5)
    p.add(head, "head")
    surf = geo.Surface(head)
    for s in (1, -1):
        e = surf.front(s * 0.11, hc.z - 0.03, offset=-0.01)
        p.add(K.ball(f"zip-eye{s}", 0.085, accent, e, res=3, scale=(0.95, 0.55, 1.1)), "head")
        p.add(K.ball(f"zip-pupil{s}", 0.04, body, e + V(-s * 0.008, -0.045, 0.0), res=2, scale=(1, 0.5, 1.2)),
              "head")
        b = surf.front(s * 0.13, hc.z + 0.085, offset=0.004)
        p.add(K.capsule(f"zip-brow{s}", b + V(s * 0.07, 0, -0.012), b + V(-s * 0.06, 0, 0.012), 0.022, accent,
                        segs=6, rings=1), "head")
        eb = "ear" + ("_L" if s > 0 else "_R")
        a_, b_ = Vector(specs[eb]["head"]), Vector(specs[eb]["tail"])
        p.add(K.cyl(f"zip-ear{s}", 0.12, a_, a_ + (b_ - a_) * 0.6, body, segs=14, steps=1), eb)
        p.add(geo.ring(f"zip-ear-rim{s}", 0.1, 0.018, accent, a_ + (b_ - a_) * 0.62, b_ - a_, segs=14, sides=4), eb)
        for k, hb in enumerate(("horn_1", "horn_2")):
            bn = hb + ("_L" if s > 0 else "_R")
            m = body if k == 0 else accent
            p.add(_seg(f"zip-{bn}", specs, bn, m, 0.045 if k == 0 else 0.038, r2=0.035 if k == 0 else 0.008,
                       ext=-0.005, segs=7), bn)
    grin = [surf.front(x, hc.z - 0.15 + 0.6 * x * x, offset=0.004) for x in (lerp(-0.13, 0.13, j / 10)
                                                                            for j in range(11))]
    p.add(geo.tube("zip-grin", [g for g in grin if g], 0.012, accent, segs=5), "head")
    p.add(_seg("zip-neck", specs, "neck", body, 0.035), "neck")
    ch = specs["chest"]
    cz = (Vector(ch["head"]).z + Vector(ch["tail"]).z) / 2
    p.add(geo.superquad("zip-chest", (0.15, 0.11, 0.1), body, (0, -0.01, cz + 0.02), n=2.6, res=3), "chest")
    p.add(K.ball("zip-gem", 0.035, accent, (0, -0.11, cz + 0.03), res=2, scale=(1, 0.5, 1.2)), "chest")
    p.add(_seg("zip-waist", specs, "spine", body, 0.07), "spine")
    hp = specs["hips"]
    p.add(geo.superquad("zip-pelvis", (0.14, 0.1, 0.08), body, Vector(hp["head"]) + V(0, 0, 0.02), n=2.6, res=2),
          "hips")
    for sd, sx in (("_L", 1), ("_R", -1)):
        p.add(K.ball("zip-cap" + sd, 0.06, accent, specs["upper_arm" + sd]["head"], res=2), "upper_arm" + sd)
        p.add(_seg("zip-ua" + sd, specs, "upper_arm" + sd, body, 0.03, ext=0.01), "upper_arm" + sd)
        p.add(K.ball("zip-elbow" + sd, 0.038, body, specs["forearm" + sd]["head"], res=2), "forearm" + sd)
        p.add(_seg("zip-fa" + sd, specs, "forearm" + sd, body, 0.032, r2=0.038, ext=0.01), "forearm" + sd)
        p.add(_seg("zip-th" + sd, specs, "thigh" + sd, body, 0.045, ext=0.02), "thigh" + sd)
        p.add(K.ball("zip-knee" + sd, 0.055, accent, specs["shin" + sd]["head"], res=2), "shin" + sd)
        p.add(_seg("zip-sh" + sd, specs, "shin" + sd, body, 0.04, ext=0.02), "shin" + sd)
        ank = Vector(specs["foot" + sd]["head"])
        p.add(geo.superquad("zip-shoe" + sd, (0.12, 0.17, 0.08), body, (ank.x, -0.03, 0.08), n=2.6, res=2),
              "foot" + sd)
        p.add(geo.superquad("zip-sole" + sd, (0.13, 0.15, 0.03), accent, (ank.x, -0.12, 0.03), n=3.0, res=2),
              "toe" + sd)
    _hands(p, specs, body, accent, hand_r=0.05, finger_r=0.018)
    p.skin = True
    p.display = ("dance", 2.1)
    p.view = dict(az=25, el=10)


@prop("holo-brick", "The pocket rave (the bouncer at the nightclub's velvet rope)",
      "floor between the feet, facing -Y, at Brick's own size (2.75 m) with his skeleton (scale it down with the "
      "other figures); materials holo_body (orange), holo_accent (cream)",
      rig="Brick's whole skeleton (plays any Brick clip): idle, bouncer, guard, guard-hold, shake-head, nod, "
          "raise-brow")
def holo_brick(p):
    specs, B = _pal(p, "brick", BRICK_CLIPS)
    body, accent = _materials("#ffa45c", "#fff1d6")
    hc = Vector(B.HEAD_C)
    hr = B.HEAD_R
    head = geo.superquad("brick-head", hr, accent, hc, n=2.4, res=4)
    p.add(head, "head")
    p.add(geo.superquad("brick-crown", (hr[0] * 1.02, hr[1] * 1.02, hr[2] * 0.55), body, hc + V(0, 0.01, hr[2] * 0.55),
                        n=2.4, res=3), "head")
    surf = geo.Surface(head)
    for s in (1, -1):
        e = surf.front(s * 0.12, hc.z - 0.01, offset=0.004)
        p.add(K.ball(f"brick-eye{s}", 0.05, body, e, res=2, scale=(1.1, 0.5, 0.75)), "head")
        b = surf.front(s * 0.13, hc.z + 0.07, offset=0.006)
        p.add(K.capsule(f"brick-brow{s}", b + V(s * 0.08, 0, 0), b + V(-s * 0.06, 0, -0.02), 0.025, body, segs=6,
                        rings=1), "head")
        ear = hc + V(s * (hr[0] + 0.02), 0.0, 0.0)
        p.add(K.cyl(f"brick-ear{s}", 0.12, ear - V(s * 0.04, 0, 0), ear + V(s * 0.05, 0, 0), body, segs=12, steps=1),
              "head")
    smile = [surf.front(x, hc.z - 0.1 + 0.5 * x * x, offset=0.004)
             for x in (lerp(-0.08, 0.08, j / 6) for j in range(7))]
    p.add(geo.tube("brick-smile", [m for m in smile if m], 0.01, body, segs=5), "head")
    p.add(geo.superquad("brick-collar", (0.36, 0.3, 0.1), body, B.COLLAR_C, n=2.4, res=2), "chest")
    p.add(geo.superquad("brick-chest", B.CH_R, body, B.CH_C, n=2.5, res=4), "chest")
    p.add(geo.superquad("brick-belly", (0.48, 0.4, 0.22), accent, (0, 0.04, 1.47), n=2.6, res=3), "spine")
    hp = specs["hips"]
    p.add(geo.superquad("brick-pelvis", (0.5, 0.36, 0.2), body, Vector(hp["head"]) + V(0, -0.02, -0.02), n=2.6, res=3),
          "hips")
    for sd, sx in (("_L", 1), ("_R", -1)):
        sh = Vector(B.SHOULDER) * V(sx, 1, 1)
        p.add(K.ball("brick-pauldron" + sd, 0.36, body, sh + V(sx * 0.04, 0, 0.1), res=3, scale=(1, 1, 0.85)),
              "upper_arm" + sd)
        p.add(_seg("brick-ua" + sd, specs, "upper_arm" + sd, accent, 0.14, ext=0.02), "upper_arm" + sd)
        p.add(K.ball("brick-elbow" + sd, 0.15, body, specs["forearm" + sd]["head"], res=2), "forearm" + sd)
        p.add(_seg("brick-gauntlet" + sd, specs, "forearm" + sd, body, 0.17, r2=0.22, ext=0.02), "forearm" + sd)
        p.add(_seg("brick-th" + sd, specs, "thigh" + sd, body, 0.21, ext=0.03), "thigh" + sd)
        p.add(K.ball("brick-knee" + sd, 0.17, accent, specs["shin" + sd]["head"], res=2), "shin" + sd)
        p.add(_seg("brick-greave" + sd, specs, "shin" + sd, body, 0.18, r2=0.2, ext=0.03), "shin" + sd)
        ank = Vector(specs["foot" + sd]["head"])
        p.add(geo.superquad("brick-boot" + sd, (0.24, 0.36, 0.16), body, (ank.x, -0.02, 0.16), n=3.0, res=2),
              "foot" + sd)
        p.add(geo.superquad("brick-toe" + sd, (0.23, 0.17, 0.12), body, (ank.x, -0.38, 0.12), n=3.0, res=2),
              "toe" + sd)
    _hands(p, specs, body, accent, hand_r=0.16, finger_r=0.055, palm_scale=(0.8, 1, 1))
    p.skin = True
    p.display = ("bouncer", 1.0)
    p.view = dict(az=25, el=10)
