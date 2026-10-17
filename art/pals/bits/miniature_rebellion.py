"""The miniature rebellion: three tiny projected agents on the Atlas Core's world copy whatever Archie does. He
loves it -- a hand up, a wave, a flex -- until he tries a little dance, a chicken-ish wiggle he'd rather no
one saw. He stops; they don't.

The agents are the holo-agent prop, built on Archie's own skeleton, so the page plays these same clips on
them, a beat behind him. Archie holds the Core throughout (HOLD: bits/_corekit.py), so every piece but
`take` and `back` starts and ends on HOLD, and leaves his left arm alone -- the copies hold an invisible Core.

    miniature-rebellion/take          REST -> HOLD (the Core to his palm at _corekit.GRAB)
    miniature-rebellion/hold          HOLD, looping
    miniature-rebellion/raise         his right hand up: hey!
    miniature-rebellion/wave          a wave
    miniature-rebellion/flex          a biceps flex, chin up
    miniature-rebellion/awkward       HOLD -> mid-dance: the wiggle, the elbow flapping, the head pecking; it
                                      ends in the middle of a peck, for `caught` to take over
    miniature-rebellion/awkward-loop  the same wiggle, looping (the agents', once he has stopped)
    miniature-rebellion/caught        (from mid-dance) -> HOLD: he freezes, his eyes dart, a hand over his eyes
    miniature-rebellion/back          HOLD -> REST (the Core back at _corekit.DOCK)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "miniature-rebellion"
CAST = ("archie",)
PECK = 0.25                     # seconds a peck of the head in the wiggle (four a second)
PROJ = (14, 30)                 # his eyes on the projection: up, to his left


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    hips, fist, point, open_hand, hand_world = L.hips, L.fist, L.point, L.open_hand, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    def right_arm_piece(name, T, target, hand, curl, face, elbow=(0.45, 0.3, -0.6), extra=None, eyes=PROJ):
        """HOLD -> HOLD: the right arm out to `target(t)` (a wrist position) and back, the hand turned to
        `hand` and shaped by `curl(p)`; `face` the key pose's face; `extra(t, p, w)` adds to the body."""
        c = Clip(f"{NAME}/{name}", T)
        c.key(0.0, HOLD)
        k = HOLD.copy()
        k.face = face
        c.key(0.35, k, "back")
        c.key(T - 0.4, k, "linear")
        c.key(T, HOLD, "inout")
        env = lambda t: pulse(t, 0.0, 0.35, T - 0.75, 0.4)

        def solve(t, p, skel):
            w = env(t)
            if extra:
                extra(t, p, w)
            K.held(body, p)
            if w > 0.01:
                body.hand_to(p, -1, rw.lerp(target(t), w), elbow=elbow, hand_rot=hand if w > 0.5 else None)
                curl(p, w)
            body.plant(p, 1)
            body.plant(p, -1)
            return p

        c.solve(solve)
        c.layer(lambda t: K.eyes_on_core(1 - env(t)) + look((eyes[0] * env(t), eyes[1] * env(t))))
        return c

    # ---- raise / wave / flex ---------------------------------------------------------------------------
    up = hand_world((0.05, 0, 1), (0, -1, 0))                 # fingers up, palm to the front
    out.append(right_arm_piece("raise", 1.6, lambda t: V(-0.42, -0.18, 2.12), up,
                               lambda p, w: open_hand(p, -1, 12 * w), {"grin": 1.0},
                               extra=lambda t, p, w: p.add("chest", -4 * w, 0, -3 * w)))
    out.append(right_arm_piece("wave", 2.2,
                               lambda t: V(-0.46 + 0.07 * math.sin(math.tau * 2.5 * t), -0.2, 1.98), up,
                               lambda p, w: open_hand(p, -1, 14 * w), {"grin": 1.0, "wide": 0.3},
                               extra=lambda t, p, w: p.add("head", 0, 0, 5 * w * math.sin(math.tau * 2.5 * t))))

    def flex_body(t, p, w):
        hips(body, p, dz=0.01 * w)
        p.add("chest", -8 * w, 0, 0)
        p.add("head", -8 * w, -10 * w, 0)

    out.append(right_arm_piece("flex", 1.9, lambda t: V(-0.5, -0.06, 1.86), hand_world((0.1, 0, 1), (1, 0, 0)),
                               lambda p, w: fist(p, -1, w), {"smirk_R": 1.0, "grin": 0.4}, elbow=(0.75, 0.05, 0.0),
                               extra=flex_body, eyes=(4, -28)))

    # ---- the wiggle ------------------------------------------------------------------------------------
    def wiggle(t, p, w):
        """Knees in, hips wagging, the right elbow flapping, the head pecking forward on every PECK."""
        b = t / PECK
        peck = max(0.0, math.sin(math.pi * b)) * w
        wag = math.sin(math.pi * b / 2) * w
        hips(body, p, dz=-0.06 * w - 0.02 * peck, dx=0.03 * wag, roll=-7 * wag, yaw=5 * wag, pitch=6 * w)
        p.add("chest", 8 * peck, 0, 4 * wag)
        p.add("neck", 10 * peck, 0, 0)
        p.add("head", 8 * peck - 6 * w, 0, -6 * wag)
        flap = 0.5 + 0.5 * math.sin(math.pi * b)
        body.hand_to(p, -1, rw.lerp(V(-0.26, -0.08, 1.42), w), elbow=(0.55 + 0.25 * flap, 0.25, -0.3),
                     hand_rot=hand_world((0.2, -0.3, -1), (1, 0, 0)) if w > 0.5 else None)
        fist(p, -1, 0.6 * w)
        # knock-kneed, the toes turned in, one heel then the other up on the beat
        knees = 0.1 * w
        body.plant(p, 1, yaw=-14 * w, roll=10 * max(0.0, math.sin(math.pi * b)) * w, knee_out=-knees)
        body.plant(p, -1, yaw=-14 * w, roll=10 * max(0.0, -math.sin(math.pi * b)) * w, knee_out=-knees)

    def wiggle_face(t, w):
        p = Pose()
        p.face.update({"grin": -0.4 * w, "oh": 0.6 * w})
        brows(p, 0.8 * w, 1.4 * w, 0.4 * w)
        return p + look((-6 * w, 0))

    TA = 12 * PECK
    c = Clip(f"{NAME}/awkward", TA)
    c.key(0.0, HOLD)
    c.key(0.3, HOLD, "linear")

    def awkward_solve(t, p, skel):
        K.held(body, p)
        wiggle(t, p, smooth(0.0, 0.3, t))
        return p

    c.solve(awkward_solve)
    c.layer(lambda t: K.eyes_on_core(1 - smooth(0, 0.3, t)) + wiggle_face(t, smooth(0, 0.3, t)))
    c.layer(lambda t: L.crest_follow(t * 4, 2.0))
    out.append(c)

    c = K.loop_clip(f"{NAME}/awkward-loop", 4 * PECK)
    c.key(0.0, HOLD)

    def loop_solve(t, p, skel):
        K.held(body, p)
        wiggle(t, p, 1.0)
        return p

    c.solve(loop_solve)
    c.layer(lambda t: wiggle_face(t, 1.0))
    out.append(c)

    # ---- caught ----------------------------------------------------------------------------------------
    TC = 2.6
    c = Clip(f"{NAME}/caught", TC)
    frozen = HOLD.copy()
    frozen.set("head", 2, 0, 0)
    frozen.face = {"flat": 1.0, "grit": 0.4}
    sheep = HOLD.copy()
    sheep.set("head", 16, -6, 6)
    sheep.face = {"frown": 0.4, "flat": 0.6}
    c.key(0.0, frozen)
    c.key(0.9, frozen, "linear")
    c.key(1.3, sheep, "inout")
    c.key(TC - 0.45, sheep, "linear")
    c.key(TC, HOLD, "inout")
    face_w = V(-0.06, -0.33, 1.9)                    # his right hand over his eyes

    def caught_solve(t, p, skel):
        K.held(body, p)
        wiggle(0.0, p, 1 - smooth(0.0, 0.25, t))    # the dance stops dead (and plants the feet)
        cover = pulse(t, 1.0, 0.35, 0.75, 0.45)
        if cover > 0.01:
            body.hand_to(p, -1, rw.lerp(face_w, cover), elbow=(0.4, 0.4, -0.6),
                         hand_rot=hand_world((0.3, 0.1, 1), (0, 1, 0)) if cover > 0.5 else None)
            open_hand(p, -1, 6 * cover)
        return p

    c.solve(caught_solve)

    def caught_face(t):
        p = Pose()
        dart = pulse(t, 0.25, 0.08, 0.55, 0.1)
        side = 1 if t < 0.55 else -1
        p = p + look((0, 24 * side * dart))
        brows(p, 1.4 * pulse(t, 0.1, 0.1, 0.8, 0.2), 1.2 * pulse(t, 0.1, 0.1, 0.8, 0.2), 0.0)
        return p + K.eyes_on_core(smooth(TC - 0.5, TC, t))

    c.layer(caught_face)
    c.layer(blink_layer([1.15]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return {"archie": out}
