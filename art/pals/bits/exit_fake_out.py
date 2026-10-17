"""The exit fake-out: Archie moonwalks off the edge of the window. One eye slowly peeks back round the edge.
Then his hand reaches towards the light switch -- and freezes, because the reader is looking. He takes it
back, slowly, and ducks out of sight. A moment later the lights flicker anyway.

The page moonwalks him off (his everyday `moonwalk`), then stands him facing the reader just past the
window's right edge -- EDGE metres to his right of his root, so that at rest none of him shows -- at a scale
and height that put his index fingertip, at the full stretch (POINT, in his own frame), on the switch.
He plays:

    exit-fake-out/peek    his right hand comes up and curls round the edge; then he leans slowly out round
                          it, crest first, until his right eye is past it. Ends held.
    exit-fake-out/reach   (from the peek) the hand lets go and creeps out along the wall to the switch,
                          index out; at FREEZE his eye snaps to the reader; the hand inches back to the
                          edge; ends on the peek.
    exit-fake-out/duck    back out of sight, quick, from the peek to REST.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "exit-fake-out"
CAST = ("archie",)
EDGE = 0.56                       # the window's edge, to his right of his root, metres
POINT = (-1.22, -0.09, 1.22)      # his right index fingertip at the full stretch (exit_fake_out.js)
FREEZE = 1.7
GRIP = (-EDGE + 0.05, -0.02, 1.30)  # the right wrist, its fingers curled round the edge
BEHIND = (-EDGE + 0.2, -0.02, 1.30)  # and on its way there, out of sight
REACH = (-0.84, -0.08, 1.30)      # the right wrist at the full stretch


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    REST, hips, point, hand_world = L.REST, L.hips, L.point, L.hand_world
    RW = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    out = []

    def lean(p, k):
        """Leaning out round the edge to his right: the hips back behind it, the trunk tilting out from them,
        the head further."""
        hips(body, p, dx=0.04 * k, dz=-0.07 * k, roll=18 * k)
        p.add("spine", 0, 0, 20 * k)
        p.add("chest", 0, 0, 18 * k)
        p.add("neck", 0, 0, -6 * k)
        p.add("head", 0, -6 * k, -20 * k)
        # his left arm, hidden behind the edge, keeps out of the way
        p.add("upper_arm_L", 0, 0, -6 * k)
        body.plant(p, 1)
        body.plant(p, -1)

    def grip(p, k):
        """The right hand on the edge: up behind it, fingers up (none of it showing), then the fingers round
        it, curled -- the wrist just behind it."""
        if k <= 0.01:
            return
        up, out_ = smooth(0.0, 0.65, k), smooth(0.65, 1.0, k)
        tgt = RW[-1].lerp(V(*BEHIND), ease("inout", up)).lerp(V(*GRIP), ease("inout", out_))
        along = V(0, 0, 1).lerp(V(-1, 0, 0.15), out_)
        palm = V(-1, 0, 0).lerp(V(0, 1, 0), out_)
        body.hand_to(p, -1, tgt, elbow=(0.3, 0.4, -0.5),
                     hand_rot=hand_world(along, palm) if up > 0.25 else None)
        p.fingers(-1, 55 * out_, spread=0, thumb=20 * out_)

    # ---- peek ---------------------------------------------------------------------------------------
    TP = 3.4
    c = Clip(f"{NAME}/peek", TP)
    c.key(0.0, REST)
    sly = REST.copy()
    sly.face = {"smirk_L": 0.8, "grin": 0.2}
    c.key(1.8, sly)
    c.key(TP, sly, "linear")
    HAND, OUT = (0.15, 0.9), (1.0, 2.9)

    def peek(t, p, skel):
        # the lean comes in two slow goes: most of the way, a stop, the last little bit (the eye)
        k = ease("inout", smooth(*OUT, t))
        lean(p, k)
        grip(p, ease("inout", smooth(*HAND, t)))
        return p

    c.solve(peek)

    def peek_face(t):
        p = Pose()
        # the eye: along the page (to his right), a glance round, then a sly look at the reader
        a = smooth(1.9, 2.3, t) * (1 - smooth(2.7, 2.9, t))
        p = p + look((-4, -22 * smooth(1.2, 1.8, t) * (1 - a) + 4 * a))
        p.both("lid_up", x=6 * smooth(1.0, 1.6, t))
        brows(p, 0.2, 1.0 * smooth(1.6, 2.2, t), 0.8 * smooth(1.6, 2.2, t), side=-1)
        return p

    c.layer(peek_face)
    out.append(c)

    # ---- reach --------------------------------------------------------------------------------------
    TR = 4.0
    c = Clip(f"{NAME}/reach", TR)
    held = REST.copy()
    held.face = {"smirk_L": 0.8, "grin": 0.2}
    caught = REST.copy()
    caught.face = {"flat": 1.0, "oh": 0.35}
    c.key(0.0, held)
    c.key(FREEZE, held, "linear")
    c.key(FREEZE + 0.08, caught, "snap")
    c.key(TR - 0.5, caught, "linear")
    c.key(TR, held)
    BACK = (FREEZE + 0.7, TR - 0.25)

    def reach(t, p, skel):
        lean(p, 1.0)
        # off the edge and out along the wall: slow, then slower as it gets near; held at the freeze; and back
        # an inch at a time
        go = smooth(0.25, FREEZE - 0.1, t) ** 0.8
        k = go * (1 - ease("inout", smooth(*BACK, t)))
        home = V(*GRIP)
        tgt = home.lerp(V(*REACH), k)
        tgt.z += 0.03 * math.sin(math.pi * k)                 # a little arc off the wall and back
        body.hand_to(p, -1, tgt, elbow=(0.2, 0.5, -0.6),
                     hand_rot=hand_world((-1, -0.05 * k, 0.15 * (1 - k)), (0, 1, 0)))
        curl = 55 * (1 - smooth(0.0, 0.4, t)) + 55 * smooth(BACK[1] - 0.3, BACK[1], t)
        if t < 0.4 or t > BACK[1] - 0.3:
            p.fingers(-1, curl, spread=0, thumb=20)
        else:
            point(p, -1)
            # creeping: the index feels ahead, before the freeze
            p.add("index_1_R", 16 * max(0.0, math.sin(t * 8)) * (0.6 < t < FREEZE - 0.15), 0, 0)
        return p

    c.solve(reach)

    def reach_face(t):
        # from the peek's wide eye to a sneaky narrow one along his arm at the switch; then (FREEZE) wide,
        # straight at the reader, both brows up, and it stays there
        p = Pose()
        caught_ = smooth(FREEZE, FREEZE + 0.06, t)
        sneaky = smooth(0.2, 0.8, t)
        p = p + look(((-4 - 2 * sneaky) * (1 - caught_), (-22 - 2 * sneaky) * (1 - caught_)))
        p.both("lid_up", x=(6 - 20 * sneaky) * (1 - caught_) + 4 * caught_)
        one = (1 - sneaky) * (1 - caught_)
        brows(p, 0.2 * one + 2.0 * caught_, 1.0 * one + 2.2 * caught_, 0.8 * one + 1.8 * caught_, side=-1)
        brows(p, 2.0 * caught_, 2.2 * caught_, 1.8 * caught_, side=1)
        return p

    c.layer(reach_face)
    out.append(c)

    # ---- duck ---------------------------------------------------------------------------------------
    TD = 0.7
    c = Clip(f"{NAME}/duck", TD)
    c.key(0.0, held)
    c.key(TD, REST, "out")

    def duck(t, p, skel):
        k = 1 - ease("out", smooth(0.0, 0.45, t))
        lean(p, k)
        grip(p, 1 - smooth(0.1, TD, t))
        return p

    c.solve(duck)

    def duck_face(t):
        p = Pose()
        k = 1 - smooth(0.0, 0.35, t)
        p.both("lid_up", x=4 * k)
        brows(p, 2.0 * k, 2.2 * k, 1.8 * k)
        return p

    c.layer(duck_face)
    out.append(c)
    return {"archie": out}
