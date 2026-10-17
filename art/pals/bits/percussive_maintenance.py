"""Percussive maintenance: the Atlas Core won't open. Archie taps it: nothing. He whacks it: nothing (it judders
and clamps shut every time). Brick ambles over and gives it one delicate fingertip tap -- and it springs open
perfectly. Archie looks at Brick, then at the reader, personally offended.

FORMATION (metres from Archie's root, x to his left -- the page's right -- y back): Archie at (0, 0) and Brick
at BRICK (to his left, a little behind), both facing the reader. Archie holds the Core on his left palm
(HOLD, bits/_corekit.py), its centre at _corekit.CORE_AT in his frame; Brick's right index tip touches it at
TAP_AT.

    archie  percussive-maintenance/take      REST -> HOLD (the Core to his palm at _corekit.GRAB)
            percussive-maintenance/hold      HOLD, looping
            percussive-maintenance/tap       two careful taps with his right forefinger, at TAPS
            percussive-maintenance/whack     a wind-up and a slap down on top of it (WHACK_AT), a shake
            percussive-maintenance/offended  a slow look at Brick, then at the reader: personally offended
            percussive-maintenance/back      HOLD -> REST (the Core back at _corekit.DOCK)
    brick   percussive-maintenance/tap-core  REST -> REST: one enormous finger, slowly out to the Core, a tap
                                             (TAP_AT), and back; a small, satisfied nod
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "percussive-maintenance"
CAST = ("archie", "brick")
BRICK = (2.0, 0.25)             # Brick's root, from Archie's (a long reach: he is wide)
TAPS = (0.55, 0.85)             # tap: his fingertip on the Core
WHACK_AT = 0.62                 # whack: his palm comes down on it
TAP_AT = 1.25                   # tap-core: Brick's fingertip on it


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie(bodies["archie"])
    if "brick" in bodies:
        out["brick"] = brick(bodies["brick"])
    return out


# ------------------------------------------------------------------------------------------ archie
def archie(body):
    L = body.lib
    hips, point, open_hand, hand_world = L.hips, L.point, L.open_hand, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    core = K.CORE_AT
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    # ---- tap -------------------------------------------------------------------------------------------
    T = 1.5
    c = Clip(f"{NAME}/tap", T)
    c.key(0.0, HOLD)
    hope = HOLD.copy()
    hope.set("head", 16, 8, -4)
    hope.face = {"smile": 0.8}
    c.key(0.3, hope, "inout")
    c.key(T - 0.3, hope, "linear")
    c.key(T, HOLD, "inout")
    side_of = core + V(-0.11, -0.02, 0.02)                      # the ball's side nearest his right hand

    def tap_solve(t, p, skel):
        K.held(body, p)
        w = pulse(t, 0.0, 0.4, T - 0.75, 0.35)
        if w > 0.01:
            tap = max(pulse(t, a - 0.06, 0.06, 0.02, 0.08) for a in TAPS)
            tip = side_of + V(-0.03 * (1 - tap), 0, 0)
            body.hand_to(p, -1, rw.lerp(tip + V(-0.22, 0.02, -0.04), w), elbow=(0.45, 0.3, -0.6),
                         hand_rot=hand_world((1, -0.15, 0.15), (0, 0, -1)) if w > 0.5 else None)
            point(p, -1)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(tap_solve)
    c.layer(lambda t: K.eyes_on_core(1.0))
    out.append(c)

    # ---- whack -----------------------------------------------------------------------------------------
    T = 1.7
    c = Clip(f"{NAME}/whack", T)
    c.key(0.0, HOLD)
    cross = HOLD.copy()
    cross.set("head", 14, 6, -4)
    cross.face = {"grit": 1.0}
    c.key(0.35, cross, "inout")
    c.key(T - 0.4, cross, "linear")
    c.key(T, HOLD, "inout")
    top = core + V(-0.02, 0.0, 0.1)                             # the top of the ball

    def whack_solve(t, p, skel):
        hit = pulse(t, WHACK_AT, 0.02, 0.05, 0.25)
        hips(body, p, dz=-0.03 * hit)
        p.add("chest", 6 * hit, 0, 0)
        # the Core bucks down under the blow, then he shakes it, cross
        shake = math.sin(math.tau * 7 * t) * pulse(t, 0.95, 0.08, 0.3, 0.15)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0.03 * shake, 0, -0.05 * hit))
        up = pulse(t, 0.05, 0.4, 0.05, 0.1)                     # the wind-up: high over it
        down = pulse(t, WHACK_AT - 0.1, 0.1, 0.25, 0.45)
        w = max(up, down)
        if w > 0.01:
            over = top + V(-0.05, 0.02, 0.45)
            tgt = over.lerp(top + V(0, 0.03, 0.12), smooth(WHACK_AT - 0.1, WHACK_AT, t))
            body.hand_to(p, -1, rw.lerp(tgt, w), elbow=(0.5, 0.2, -0.3),
                         hand_rot=hand_world((0.15, -1, 0), (0, 0, -1)) if w > 0.5 else None)
            open_hand(p, -1, 6 * w)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(whack_solve)

    def whack_face(t):
        p = Pose()
        k = pulse(t, 0.25, 0.15, 1.0, 0.3)
        abrows(p, -1.2 * k, -0.6 * k, 0.6 * k)
        p.both("lid_up", x=-14 * pulse(t, WHACK_AT, 0.02, 0.1, 0.2))
        return p + K.eyes_on_core(1.0)

    c.layer(whack_face)
    out.append(c)

    # ---- offended --------------------------------------------------------------------------------------
    T = 3.6
    c = Clip(f"{NAME}/offended", T)
    c.key(0.0, HOLD)
    at_brick = HOLD.copy()
    at_brick.set("head", -6, 26, 0)                            # up at Brick, on his left
    at_brick.set("chest", 0, 8, 0)
    at_brick.face = {"flat": 1.0}
    at_us = HOLD.copy()
    at_us.set("head", -8, -4, 0)
    at_us.set("chest", -3, -2, 0)
    at_us.face = {"flat": 0.7, "frown": 0.5}
    c.key(0.7, at_brick, "inout")
    c.key(1.6, at_brick, "linear")
    c.key(2.0, at_us, "inout")
    c.key(T - 0.4, at_us, "linear")
    c.key(T, HOLD, "inout")

    def offended_solve(t, p, skel):
        K.held(body, p)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(offended_solve)

    def offended_face(t):
        p = Pose()
        b = pulse(t, 0.5, 0.3, 1.0, 0.2)
        u = pulse(t, 1.8, 0.2, T - 2.4, 0.4)
        abrows(p, -1.4 * u, -0.8 * u, 0.4 * u)                 # lowered and drawn in: hmph
        abrows(p, 0.0, -0.6 * b, -0.6 * b)
        p.both("lid_up", x=-12 * max(b, u))                     # a long, level, heavy-lidded look
        p = p + look((10 * b, 24 * b)) + look((-2 * u, 0)) + K.eyes_on_core(1 - min(1.0, b + u))
        return p

    c.layer(offended_face)
    c.layer(blink_layer([1.85]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST, hand_world, point = L.REST, L.hand_world, L.point
    rw = L.rest_wrists(body)
    # the Core's centre in his own frame; his fingertip comes to its right side (screen right), pointing in
    core = K.CORE_AT - V(BRICK[0], BRICK[1], 0)
    touch = core + V(0.1, 0.0, 0.0)
    d = V(-0.75, -0.45, -0.48).normalized()                     # along his finger: in, forward and down
    hr = hand_world(d, (0.0, 0.25, -1.0))
    T = 2.8
    c = Clip(f"{NAME}/tap-core", T, frames=int(round(T * 30)))
    c.key(0.0, REST)
    lean = REST.copy()
    lean.set("chest", 10, -10, 4)
    lean.set("head", 22, -14, 0)
    lean.face = {"smile": 1.0}
    c.key(0.8, lean, "inout")
    c.key(1.9, lean, "linear")
    nod = REST.copy()
    nod.set("head", 12, -4, 0)
    c.key(2.3, nod, "inout")
    c.key(T, REST, "inout")

    def solve(t, p, skel):
        k = pulse(t, 0.1, 0.9, 0.55, 0.75)
        tap = pulse(t, TAP_AT - 0.08, 0.08, 0.03, 0.12)
        tip = touch + d * (-0.05 * (1 - tap) - 0.012 * (1 - k))
        wrist = tip - d * 0.58
        body.hand_to(p, -1, rw[-1].lerp(wrist, k), elbow=(0.6, 0.6, -0.6), hand_rot=hr if k > 0.45 else None)
        if k > 0.2:
            point(p, -1)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(solve)
    c.layer(lambda t: look((-24 * pulse(t, 0.4, 0.4, 1.0, 0.4), -18 * pulse(t, 0.4, 0.4, 1.0, 0.4))))
    c.layer(L.blinks([2.25]))
    return [c]
