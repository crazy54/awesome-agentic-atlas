"""The dramatic entrance: a smoke machine, a spotlight, a drum roll's worth of smoke -- and when it clears,
Archie in his grandest pose, arms flung up, chin high... with his back to the reader. Zip walks in and turns
him round. He does it again, the right way.

The page stands Archie on the hero's top edge, turned away from the reader (facing into the page), and
shows him once the smoke is thick; it turns him to face the reader when Zip's push lands (ZIP_PUSH).

FORMATION (metres from Archie's root, x to his left; he faces away, so his left is screen left):
    archie  (0, 0, 0)
    zip     (ZIP_X, 0, 0) beside him, facing him

Pieces (Archie):
    dramatic-entrance/pose        into the grand pose: arms up in a V, chest out, chin up, one foot forward;
                                  ends held in it
    dramatic-entrance/hold        loops: the pose, a breath, a little vibrato in the fingers
    dramatic-entrance/oops        (still facing away) the arms sag, a look back over his shoulder: where is
                                  everyone? ends on REST
    dramatic-entrance/front       facing the reader at last: the pose again, bigger, a wink; ends on REST
Pieces (Zip, clips/zip_base.py), facing Archie (screen right) at ZIP_X beside him:
    dramatic-entrance/turn    both hands up on Archie's arm and a shove round (the page turns Archie at
                              ZIP_PUSH), then a dust of the hands
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import loop_clip, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "dramatic-entrance"
CAST = ("archie", "zip")
ZIP_X = 0.9
ZIP_PUSH = 1.0


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


def archie_clips(body):
    L = body.lib
    RW = rest_wrists(body)
    out = []

    def grand(p, k=1.0, big=1.0):
        """The pose, k of the way from REST: arms up in a V, the hands open, chest out, chin up."""
        L.hips(body, p, dz=-0.03 * k, pitch=-4 * k * big)
        p.add("spine", -4 * k * big, 0, 0)
        p.add("chest", -10 * k * big, 0, 0)
        p.add("head", -14 * k * big, 0, 0)
        for sg in (1, -1):
            tgt = Vector((sg * (0.78 + 0.08 * big), -0.18, 2.32 + 0.06 * big))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.8, 0.1, 0.1),
                         hand_rot=L.hand_world((sg * 0.6, -0.1, 1), (0, -1, 0)) if k > 0.6 else None)
            L.open_hand(p, sg, 14 * k)
        body.plant(p, 1, pos=(0.04 * k, -0.16 * k, 0), yaw=12 * k)
        body.plant(p, -1, pos=(-0.02 * k, 0.06 * k, 0), yaw=18 * k, roll=10 * k)
        return p

    proud = L.REST.copy()
    proud.face = {"grin": 1.0, "wide": 0.4}

    # ---- pose ----------------------------------------------------------------------------------------
    TP = 1.6
    c = Clip(f"{NAME}/pose", TP)
    c.key(0.0, L.REST)
    c.key(0.5, proud)
    c.key(TP, proud, "linear")
    c.solve(lambda t, p, skel: grand(p, ease_back(t / 0.55)))
    c.layer(lambda t: brows(Pose(), 1.2, 1.6, 1.2) + look((10, 0)))
    c.layer(lambda t: L.crest_follow(t * 10, 1.6 * pulse(t, 0.4, 0.1, 0.2, 0.6)))
    out.append(c)

    # ---- hold ----------------------------------------------------------------------------------------
    TH = 2.0
    c = loop_clip(f"{NAME}/hold", TH)
    c.key(0.0, proud)

    def hold_solve(t, p, skel):
        grand(p, 1.0)
        b = math.sin(math.tau * t / TH)
        p.add("chest", -1.5 * b, 0, 0)
        for sg in (1, -1):
            for f in ("index", "middle", "ring"):
                p.add(f"{f}_1{'_L' if sg > 0 else '_R'}", 6 * math.sin(t * 25 + sg), 0, 0)
        return p

    c.solve(hold_solve)
    c.layer(lambda t: brows(Pose(), 1.2, 1.6, 1.2) + look((10, 0)))
    c.layer(blink_layer([1.4]))
    out.append(c)

    # ---- oops: still facing away, a look back over his shoulder ---------------------------------------
    TO = 1.8
    c = Clip(f"{NAME}/oops", TO)
    back = L.REST.copy()
    back.set("head", 2, -62, 4)                                # over his right shoulder, towards the reader
    back.set("neck", 0, -14, 0)
    back.set("chest", 0, -14, 0)
    back.face = {"oh": 0.8}
    c.key(0.0, proud)
    c.key(0.9, back, "inout")
    c.key(TO, back, "linear")

    def oops_solve(t, p, skel):
        k = 1 - smooth(0.0, 0.7, t)
        grand(p, k)
        if k < 0.99:
            body.plant(p, 1)
            body.plant(p, -1)
        return p

    c.solve(oops_solve)
    c.layer(lambda t: brows(Pose(), 1.6 * smooth(0.6, 1.0, t), 1.4 * smooth(0.6, 1.0, t), 0.2)
            + look((0, -24 * smooth(0.6, 1.0, t))))
    out.append(c)

    # ---- front: the right way round, bigger, a wink ----------------------------------------------------
    TF = 3.2
    c = Clip(f"{NAME}/front", TF)
    c.key(0.0, L.REST)
    c.key(0.4, proud)
    c.key(TF - 0.6, proud, "linear")
    c.key(TF, L.REST)
    c.solve(lambda t, p, skel: grand(p, ease_back(t / 0.4) * (1 - smooth(TF - 0.7, TF, t)), big=1.4))

    def wink(t):
        p = brows(Pose(), 1.4, 1.8, 1.4)
        w = pulse(t, 1.4, 0.08, 0.35, 0.12)
        p.side("lid_up", 1, x=-46 * w)
        p.side("lid_lo", 1, x=40 * w)
        p.face["smirk_L"] = 0.8 * w
        return p + look((6, 0))

    c.layer(wink)
    c.layer(lambda t: L.crest_follow(t * 10, 1.6 * pulse(t, 0.3, 0.1, 0.2, 0.6)))
    out.append(c)
    return out


def ease_back(u):
    u = max(0.0, min(1.0, u))
    c = 1.7
    v = u - 1
    return 1 + (c + 1) * v * v * v + c * v * v


def zip_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    T = 2.2
    c = Clip(f"{NAME}/turn", T)
    c.key(0.0, L.REST)
    go = L.REST.copy()
    go.face = {"grin": 1.0, "smirk_L": 0.5}
    c.key(0.4, go)
    c.key(T - 0.3, go, "linear")
    c.key(T, L.REST)

    def turn_solve(t, p, skel):
        k = pulse(t, 0.0, 0.4, 0.9, 0.4)
        shove = smooth(ZIP_PUSH - 0.15, ZIP_PUSH + 0.1, t)
        L.hips(body, p, dy=-0.06 * shove, pitch=8 * shove)
        for sg in (1, -1):
            tgt = Vector((sg * 0.12 + 0.18 * shove, -0.42 - 0.12 * shove, 1.3))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.5, 0.4, -0.4),
                         hand_rot=L.hand_world((0, -0.2, 1), (0, -1, 0)) if k > 0.5 else None)
            L.open_hand(p, sg, 8)
        body.plant(p, 1)
        body.plant(p, -1, pos=(0, 0.08 * shove, 0), roll=10 * shove)
        return p

    c.solve(turn_solve)
    c.layer(lambda t: look((10, 0)) + L.horn_sway(t, T, 3.0))
    return [c]
