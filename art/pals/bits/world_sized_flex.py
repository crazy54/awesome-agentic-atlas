"""The world-sized flex: Archie presents the Atlas Core's world with enormous theatrical effort -- heave, heave,
HEAVE -- and the projection swells to tower over the page. Zip strolls over, reaches up and turns the Core's
size dial down. The world shrinks to a speck. Archie deflates.

FORMATION (metres from Archie's root, x to his left -- the page's right -- y back): Archie at (0, 0), Zip at
ZIP, both facing the reader. Archie holds the Core on his left palm (HOLD, bits/_corekit.py); through the
heaving his hand comes back to the same place, so the Core's size dial is at DIAL (his frame: the dial on the
open Core's rim, front left) whenever Zip reaches for it.

    archie  world-sized-flex/take     REST -> HOLD (the Core to his palm at _corekit.GRAB)
            world-sized-flex/hold     HOLD, looping
            world-sized-flex/heave    HOLD -> STRAIN: three heaves (HEAVES), knees bent, his right hand under the
                                      Core too, trembling; the page swells the world on each
            world-sized-flex/strain   STRAIN, looping: holding it up, quivering
            world-sized-flex/deflate  STRAIN -> HOLD: the right hand drops, a slump, a look at the speck, a look
                                      at Zip
            world-sized-flex/back     HOLD -> REST (the Core back at _corekit.DOCK)
    zip     world-sized-flex/dial     REST -> REST: a look up at the size of it, up on his toes, a turn of the
                                      dial (TURN: the page spins the Core's `dial` bone and shrinks the world),
                                      and a brisk dust-off of his hands
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "world-sized-flex"
CAST = ("archie", "zip")
ZIP = (0.85, -0.15)             # Zip's root, from Archie's (clear of the Core: he leans in to reach it)
DIAL = K.CORE_AT + Vector((-0.044, -0.061, 0.0))   # the dial on the open Core (core.py DIAL_AZ, RIM_TOP)
HEAVES = (0.7, 1.7, 2.7)        # heave: the top of each push (the page swells the world)
TURN = (1.05, 1.85)             # dial: Zip's turn of the dial


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_(bodies["zip"])
    return out


# ------------------------------------------------------------------------------------------ archie
def archie(body):
    L = body.lib
    hips, open_hand, hand_world = L.hips, L.open_hand, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    under = K.CORE_AT + V(-0.07, 0.02, -0.15)                     # his right hand helping, under the ball
    palm_up = hand_world((0.6, -0.8, 0.05), (0, 0, 1))
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    STRAIN = HOLD.copy()
    STRAIN.set("head", -6, 4, 0)
    STRAIN.set("chest", -4, 2, 0)
    STRAIN.face = {"grit": 1.0}

    def strained(t, p, w, push=0.0, shake=1.0):
        """Knees bent, both hands under the Core (it stays put, lifted by `push`), quivering."""
        q = math.sin(math.tau * 9 * t) * 0.006 * shake * w
        hips(body, p, dz=-0.12 * w + 0.07 * push, pitch=4 * w, roll=120 * q)
        p.add("chest", 4 * push, 0, 0)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(q, 0, 0.08 * push))
        if w > 0.01:
            body.hand_to(p, -1, rw.lerp(under + V(q, 0, 0.08 * push), w), elbow=(0.4, 0.3, -0.7),
                         hand_rot=palm_up if w > 0.5 else None)
            open_hand(p, -1, 4 * w)
        body.plant(p, 1, knee_out=0.08 * w)
        body.plant(p, -1, knee_out=0.08 * w)

    def strain_face(t, w, push=0.0):
        p = Pose()
        abrows(p, 1.2 * w, -0.4 * w, -0.8 * w)
        p.both("lid_up", x=-30 * w * (0.6 + 0.4 * push))            # eyes squeezed on each push
        p.both("lid_lo", x=20 * w * (0.6 + 0.4 * push))
        return p

    # ---- heave -----------------------------------------------------------------------------------------
    T = 3.4
    c = Clip(f"{NAME}/heave", T)
    c.key(0.0, HOLD)
    c.key(0.4, STRAIN, "inout")

    def heave_solve(t, p, skel):
        w = smooth(0.0, 0.4, t)
        push = max(pulse(t, h - 0.25, 0.25, 0.05, 0.3) for h in HEAVES)
        strained(t, p, w, push)
        return p

    c.solve(heave_solve)
    c.layer(lambda t: strain_face(t, smooth(0, 0.4, t), max(pulse(t, h - 0.25, 0.25, 0.05, 0.3) for h in HEAVES)) +
            K.eyes_on_core(1 - smooth(0, 0.4, t)))
    c.layer(lambda t: L.crest_follow(t * 5, 2.0))
    out.append(c)

    # ---- strain ----------------------------------------------------------------------------------------
    c = K.loop_clip(f"{NAME}/strain", 2.0)
    c.key(0.0, STRAIN)

    def strain_solve(t, p, skel):
        strained(t, p, 1.0)
        return p

    c.solve(strain_solve)
    c.layer(lambda t: strain_face(t, 1.0))
    out.append(c)

    # ---- deflate ---------------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/deflate", T)
    c.key(0.0, STRAIN)
    slump = HOLD.copy()
    slump.set("head", 20, 4, -6)
    slump.set("chest", 10, 0, 0)
    slump.both("shoulder", z=-6)
    slump.face = {"frown": 0.6, "flat": 0.4}
    glum = HOLD.copy()
    glum.set("head", 4, 24, 0)                                    # at Zip, on his left
    glum.both("shoulder", z=-4)
    glum.face = {"flat": 1.0}
    c.key(0.6, slump, "inout")
    c.key(1.5, slump, "linear")
    c.key(2.0, glum, "inout")
    c.key(T - 0.4, glum, "linear")
    c.key(T, HOLD, "inout")

    def deflate_solve(t, p, skel):
        w = 1 - smooth(0.0, 0.6, t)
        strained(t, p, w, 0.0, 0.0)
        return p

    c.solve(deflate_solve)

    def deflate_face(t):
        p = Pose()
        s = pulse(t, 0.4, 0.3, 1.0, 0.3)
        abrows(p, 1.0 * s, 0.2 * s, -0.6 * s)                     # sad
        g = pulse(t, 1.7, 0.3, 0.8, 0.3)
        p.both("lid_up", x=-14 * g)
        return p + K.eyes_on_core(1 - g) + look((0, 24 * g))

    c.layer(deflate_face)
    c.layer(blink_layer([1.4]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return out


# --------------------------------------------------------------------------------------------- zip
def zip_(body):
    L = body.lib
    REST, hips, point, open_hand, hand_world = L.REST, L.hips, L.point, L.open_hand, L.hand_world
    rw = L.rest_wrists(body)
    dial = DIAL - V(ZIP[0], ZIP[1], 0)                            # the dial in his own frame
    T = 3.2
    c = Clip(f"{NAME}/dial", T, frames=int(round(T * 30)))
    c.key(0.0, REST)
    up = REST.copy()
    up.set("head", -22, -8, 0)                                    # up at the enormous thing
    up.face = {"flat": 0.6, "grin": 0.4}
    busy = REST.copy()
    busy.set("head", 10, -16, 0)
    busy.face = {"smirk_L": 0.8}
    done = REST.copy()
    done.face = {"grin": 1.0}
    c.key(0.35, up, "inout")
    c.key(0.75, busy, "inout")
    c.key(2.1, busy, "linear")
    c.key(2.5, done, "inout")
    c.key(T, REST, "inout")

    def solve(t, p, skel):
        reach = pulse(t, 0.55, 0.45, TURN[1] - 1.0 + 0.1, 0.35)
        toes = pulse(t, 0.55, 0.4, TURN[1] - 0.95, 0.35)
        hips(body, p, dz=0.05 * toes, dx=-0.16 * reach, roll=9 * reach)
        p.add("chest", 0, 0, 8 * reach)                             # leaning in to it
        turn = smooth(TURN[0], TURN[1], t)
        if reach > 0.01:
            fingers = V(-0.35, -0.55, 0.75).normalized()           # up and across to it
            tw = math.radians(-70 * turn)                          # the twist of the wrist
            palm = V(math.cos(tw) * 0.3, 0.2 + math.sin(tw) * 0.3, -0.9)
            wrist = dial - fingers * 0.13
            body.hand_to(p, -1, rw[-1].lerp(wrist, reach), elbow=(0.5, 0.2, -0.5),
                         hand_rot=hand_world(fingers, palm) if reach > 0.5 else None)
            p.fingers(-1, 40 * reach, spread=0, thumb=40 * reach)  # a pinch on the knob
        # the dust-off: hands brushed together, twice
        dust = pulse(t, 2.45, 0.15, 0.4, 0.2)
        if dust > 0.01:
            rub = 0.05 * math.sin(math.tau * 5 * t)
            for sg in (1, -1):
                body.hand_to(p, sg, rw[sg].lerp(V(sg * 0.05 + rub * sg, -0.32, 0.95), dust), elbow=(0.4, 0.3, -0.6),
                             hand_rot=hand_world((-sg * 0.6, -0.8, 0), (-sg, 0, 0)) if dust > 0.5 else None)
                open_hand(p, sg, 4 * dust)
        body.plant(p, 1, roll=24 * toes)
        body.plant(p, -1, roll=24 * toes)
        return p

    c.solve(solve)
    c.layer(lambda t: look((20 * pulse(t, 0.2, 0.2, 0.3, 0.2), 0)) +
            look((-10 * pulse(t, 0.7, 0.2, 1.3, 0.3), -16 * pulse(t, 0.7, 0.2, 1.3, 0.3))))
    c.layer(L.blinks([2.4]))
    return [c]
