"""The holograms the Atlas Core projects: a bootleg Archie (a tiny, pompous, big-headed copy of him) and the
miniature agents. Both are built on Archie's own skeleton, bone for bone (the same names and the same rest
frames, read from archie.build()), so any clip made for Archie plays on them unchanged: the agents copying
his moves (and his embarrassing dance), Tiny Archie folding his arms when he does. They are built at
Archie's size; the page scales them down to stand on the Core's disc (about 0.035 puts one 8 cm tall).

Materials are `holo_body` (cyan) and `holo_accent` (lime), named like the Core's and the worlds' holograms
so the page's additive hologram shader picks them up. Clips of their own, in the pals' clip language
(kit.anim Poses, bone frames as clips/archie_base.py describes): `wave`, `fold_arms`, and for Tiny Archie
`pompous` (a lecture, finger raised) and for the agents `cheer`.
"""
from __future__ import annotations

import math

from mathutils import Vector

import props_kit as K
from props_kit import V, lerp, prop
from kit import anim, geo, mat
from kit.anim import Clip, Pose

TAU = math.tau


def _materials():
    body = mat.principled("holo_body", "#2fe3f1", rough=0.3, emit="#2fe3f1", strength=2.0)
    accent = mat.principled("holo_accent", "#b9e23c", rough=0.3, emit="#b9e23c", strength=2.5)
    return body, accent


def _archie_skeleton(p):
    """Declare Archie's skeleton on `p`, exactly as archie.py declares it (it is built, read and thrown
    away); returns the specs and a few landmarks."""
    import archie
    R, _, _ = archie.build()
    specs = {n: dict(R.specs[n]) for n in R.order}
    order = list(R.order)
    geo.reset()
    for n in order:
        s = specs[n]
        p.bone(n, s["head"], s["tail"], parent=s["parent"], z=s["z"])
    return specs, archie


def _seg(name, specs, bone, m, r, r2=None, ext=0.0, segs=8):
    s = specs[bone]
    a, b = Vector(s["head"]), Vector(s["tail"])
    d = (b - a).normalized()
    return K.capsule(name, a + d * ext, b - d * ext, r, m, segs=segs, rings=1, r2=r2)


def _limbs(p, specs, body, accent, arm_r=0.055, leg_r=0.08, fingers=True, hand_r=0.075):
    for sd in ("_L", "_R"):
        p.add(_seg("ua" + sd, specs, "upper_arm" + sd, body, arm_r, ext=0.02), "upper_arm" + sd)
        p.add(_seg("fa" + sd, specs, "forearm" + sd, body, arm_r * 0.9, ext=0.02), "forearm" + sd)
        sh = Vector(specs["upper_arm" + sd]["head"])
        p.add(K.ball("pad" + sd, arm_r * 1.9, body, sh + V(0, 0, 0.03), res=2), "upper_arm" + sd)
        h = specs["hand" + sd]
        a, b = Vector(h["head"]), Vector(h["tail"])
        p.add(K.ball("palm" + sd, hand_r, body, a.lerp(b, 0.45), res=2, scale=(1, 0.7, 1)), "hand" + sd)
        p.add(geo.ring("cuff" + sd, arm_r * 0.95, 0.012, accent, a, b - a, segs=8, sides=3), "hand" + sd)
        if fingers:                                           # one rigid digit per finger, on its first bone
            for f in ("thumb", "index", "middle", "ring"):
                a, b = Vector(specs[f"{f}_1{sd}"]["head"]), Vector(specs[f"{f}_3{sd}"]["tail"])
                p.add(K.capsule(f"{f}{sd}", a, b, 0.024 if f == "thumb" else 0.021, body, segs=5, rings=1),
                      f"{f}_1{sd}")
        p.add(_seg("th" + sd, specs, "thigh" + sd, body, leg_r, ext=0.03), "thigh" + sd)
        p.add(_seg("sh" + sd, specs, "shin" + sd, body, leg_r * 0.82, ext=0.03), "shin" + sd)
        p.add(K.ball("knee" + sd, leg_r * 1.1, accent, specs["shin" + sd]["head"], res=2), "shin" + sd)


@prop("holo-archie", "Bootleg Archie (the pompous projected copy); The sleepy atlas (the little hologram Zip "
      "draws the mustache on); Hostile takeover",
      "floor between the feet, facing -Y, at Archie's own size with his skeleton (scale ~0.035 to stand on "
      "the Core's disc); materials holo_body, holo_accent",
      rig="Archie's whole skeleton (plays any Archie clip): wave, fold_arms, pompous")
def holo_archie(p):
    specs, A = _archie_skeleton(p)
    body, accent = _materials()
    neck_top = Vector(specs["head"]["head"])
    k = 1.5                                                   # the bootleg's big head
    hc = neck_top + (Vector(A.HEAD_C) - neck_top) * k
    hr = [r * k for r in A.HEAD_R]

    def head_shape(q, u):
        below = max(0.0, -u.z)
        return V(q.x * (1 - 0.25 * below ** 1.8), q.y * (1 - 0.18 * below ** 1.8) - 0.03 * below ** 2, q.z)

    skull = geo.superquad("bootleg-head", hr, body, hc, n=2.15, shape=head_shape, res=5)
    p.add(skull, "head")
    surf = geo.Surface(skull)
    for s in (1, -1):
        e = surf.front(s * 0.16, hc.z + 0.02, offset=0.004)
        # smug, half-lidded eyes, and brows raised (the left one higher still)
        p.add(K.capsule(f"bootleg-eye{s}", e + V(-0.045, 0, 0), e + V(0.045, 0, 0), 0.03, accent, segs=6, rings=1),
              "head")
        b = surf.front(s * 0.17, hc.z + 0.13 + (0.035 if s > 0 else 0), offset=0.006)
        p.add(K.capsule(f"bootleg-brow{s}", b + V(-0.07, 0, -0.012 * s), b + V(0.07, 0, 0.012 * s), 0.02, accent,
                        segs=6, rings=1), "head")
        ear = hc + V(s * (hr[0] + 0.01), 0.02, -0.02)
        p.add(K.cyl(f"bootleg-ear{s}", 0.13, ear - V(s * 0.04, 0, 0), ear + V(s * 0.04, 0, 0), body, segs=12,
                    steps=1), "head")
        p.add(K.cyl(f"bootleg-ear-lens{s}", 0.075, ear, ear + V(s * 0.05, 0, 0), accent, segs=10, steps=1), "head")
    mouth = [surf.front(x, hc.z - 0.13 + 0.25 * x * x + 0.06 * max(0.0, x), offset=0.004) for x in
             (lerp(-0.1, 0.12, j / 8) for j in range(9))]
    p.add(geo.tube("bootleg-smirk", [m for m in mouth if m], 0.012, accent, segs=5), "head")
    # the crest, bigger still, swept forward off the crown
    top = hc + V(0, 0.05, hr[2] - 0.05)
    crest = [top, top + V(0.03, -0.08, 0.17), top + V(0.1, -0.2, 0.27), top + V(0.2, -0.33, 0.3),
             top + V(0.3, -0.4, 0.28)]
    p.add(geo.sweep("bootleg-crest", K.polyline(crest, 12), [lerp(0.06, 0.006, j / 12) for j in range(13)],
                    [lerp(0.22, 0.01, (j / 12) ** 1.3) for j in range(13)], accent, n=2.4, segs=8,
                    up=(0, -1, 0.2)), "head")
    p.add(_seg("bootleg-neck", specs, "neck", body, 0.07), "neck")
    # a puffed-out chest, the core's dock in the belly
    p.add(geo.superquad("bootleg-chest", (0.34, 0.3, 0.23), body, (0, -0.07, specs["chest"]["head"].z + 0.12),
                        n=2.4, res=3), "chest")
    p.add(geo.ring("bootleg-chevron", 0.27, 0.014, accent, (0, -0.1, specs["chest"]["head"].z + 0.05), (0, -0.4, 1),
                   segs=16, sides=3, squash=1.0), "chest")
    sp = specs["spine"]
    p.add(K.capsule("bootleg-belly", sp["head"], sp["tail"], 0.13, body, segs=10, rings=1), "spine")
    dock = Vector(specs["core"]["head"])
    p.add(geo.ring("bootleg-dock", 0.08, 0.016, accent, dock + V(0, -0.03, 0), (0, -1, 0), segs=8, sides=4),
          "spine")
    hp = specs["hips"]
    p.add(geo.superquad("bootleg-pelvis", (0.2, 0.15, 0.11), body, Vector(hp["head"]) + V(0, 0, -0.02), n=2.4,
                        res=3), "hips")
    _limbs(p, specs, body, accent, arm_r=0.05, leg_r=0.075)
    for sd, sx in (("_L", 1), ("_R", -1)):                   # big shoes
        p.add(geo.superquad("bootleg-shoe" + sd, (0.17, 0.27, 0.11), body, (sx * 0.222, -0.1, 0.11), n=2.4, res=2),
              "foot" + sd)
        p.add(geo.superquad("bootleg-toe" + sd, (0.16, 0.13, 0.085), body, (sx * 0.222, -0.4, 0.085), n=2.4, res=2),
              "toe" + sd)
    p.skin = True
    _clips(p, pompous=True)
    p.display = ("pompous", 0.6)
    p.view = dict(az=25, el=10)


@prop("holo-agent", "The miniature rebellion (they copy Archie's moves); The escapee (climbs out, waves, runs "
      "off); Hostile takeover; Bootleg Archie",
      "floor between the feet, facing -Y, at Archie's own size with his skeleton (scale ~0.03 on the disc); "
      "materials holo_body, holo_accent",
      rig="Archie's whole skeleton (plays any Archie clip, walk for running off): wave, fold_arms, cheer")
def holo_agent(p):
    specs, A = _archie_skeleton(p)
    body, accent = _materials()
    neck_top = Vector(specs["head"]["head"])
    hc = neck_top + V(0, -0.02, 0.26)
    head = K.ball("agent-head", 0.26, body, hc, res=4, scale=(1.05, 0.95, 0.92))
    p.add(head, "head")
    p.add(geo.superquad("agent-visor", (0.2, 0.08, 0.075), accent, hc + V(0, -0.2, 0.02), n=2.6, res=2), "head")
    p.add(K.capsule("agent-antenna", hc + V(0, 0, 0.2), hc + V(0.04, 0.02, 0.38), 0.014, body, segs=6, rings=1),
          "head")
    p.add(K.ball("agent-antenna-tip", 0.035, accent, hc + V(0.04, 0.02, 0.4), res=2), "head")
    p.add(_seg("agent-neck", specs, "neck", body, 0.06), "neck")
    ch = specs["chest"]
    p.add(geo.superquad("agent-chest", (0.27, 0.2, 0.21), body, (0, -0.02, ch["head"].z + 0.1), n=3.0, res=3),
          "chest")
    p.add(geo.disc("agent-emblem", 0.07, 0.02, accent, (0, -0.22, ch["head"].z + 0.12), (0, -1, 0), segs=6), "chest")
    sp = specs["spine"]
    p.add(K.capsule("agent-belly", sp["head"], sp["tail"], 0.12, body, segs=8, rings=1), "spine")
    hp = specs["hips"]
    p.add(geo.superquad("agent-pelvis", (0.19, 0.14, 0.1), body, Vector(hp["head"]) + V(0, 0, -0.02), n=3.0, res=2),
          "hips")
    _limbs(p, specs, body, accent, arm_r=0.045, leg_r=0.065, fingers=False, hand_r=0.07)
    for sd, sx in (("_L", 1), ("_R", -1)):
        p.add(geo.superquad("agent-foot" + sd, (0.12, 0.2, 0.075), body, (sx * 0.215, -0.15, 0.075), n=3.0, res=2),
              "foot" + sd)
    p.skin = True
    _clips(p, cheer=True)
    p.display = ("wave", 0.9)
    p.view = dict(az=25, el=10)


def _clips(p, pompous=False, cheer=False):
    """Wave, fold the arms, and a pompous lecture or a cheer, on Archie's skeleton (built at finish)."""
    wave = Clip("wave", 2.0)
    up = Pose().side("upper_arm", 1, x=-10, z=95).side("forearm", 1, x=70)
    wave.key(0.0, Pose()).key(0.45, up, "back").key(1.6, up, "linear").key(2.0, Pose(), "inout")
    wave.layer(lambda t: Pose().side("forearm", 1, z=25 * math.sin(t * 9) * anim.pulse(t, 0.45, 0.15, 1.0, 0.3)))
    p.pose_clip(wave)

    fold = Clip("fold_arms", 1.2)
    fold.key(0.0, Pose()).key(0.7, Pose().both("index_1", 40).both("middle_1", 40).both("ring_1", 40)
                             .set("head", -6, 0, 0).set("chest", -4, 0, 0), "inout")
    fold.key(1.2, fold.base.keys[-1][1], "linear")
    targets = {1: (V(-0.12, -0.37, 1.41), V(0.75, -0.45, 1.3)), -1: (V(0.13, -0.39, 1.35), V(-0.75, -0.45, 1.25))}

    def solve(t, pose, skel):
        w = K.ease("inout", min(1.0, t / 0.7))
        for s, (tgt, pole) in targets.items():
            sd = "_L" if s > 0 else "_R"
            rest = skel.tail(Pose(), "forearm" + sd)
            skel.two_bone(pose, "upper_arm" + sd, "forearm" + sd, rest.lerp(tgt, w), pole)
        return pose

    fold.solve(solve)
    p.pose_clip(fold)

    if pompous:
        lec = Clip("pompous", 3.0, loop=True)
        base = (Pose().set("chest", -8, 0, 0).set("head", -12, 0, 0)
                .side("upper_arm", -1, x=35, z=55).side("forearm", -1, x=95)
                .side("upper_arm", 1, x=-15, z=-25).side("forearm", 1, x=70).side("hand", 1, z=-30)
                .side("middle_1", -1, 85).side("ring_1", -1, 85).side("thumb_1", -1, 40)
                .both("index_1", 15).side("middle_1", 1, 20).side("ring_1", 1, 20))
        base.side("index_1", -1, 0, 0, 0)
        lec.key(0.0, base)
        lec.layer(lambda t: Pose().side("forearm", -1, z=14 * math.sin(TAU * t / 0.75))
                  .set("head", 0, 8 * math.sin(TAU * t / 1.5), 4 * math.sin(TAU * t / 3.0))
                  .set("spine", 0, 5 * math.sin(TAU * t / 3.0), 0))
        p.pose_clip(lec)
    if cheer:
        ch = Clip("cheer", 1.2, loop=True)
        arms = Pose().both("upper_arm", -15, 0, 120).both("forearm", 20)
        ch.key(0.0, arms)
        ch.layer(lambda t: Pose().both("upper_arm", 0, 0, 12 * math.sin(TAU * t / 0.6))
                 .set("spine", 6 * math.sin(TAU * t / 0.6), 0, 0)
                 .move("hips", 0, 0.05 * abs(math.sin(TAU * t / 1.2)), 0))
        p.pose_clip(ch)
