"""Pieces the Core gags of the worlds builder share: Archie reacting to what the Atlas Core shows (the hostile
takeover, the pocket rave), and the moves of the little hologram agents in it. Not a bit itself (bits/__init__.py
skips modules whose names start with an underscore). Each takes Archie's `Body` (its `.lib` is archie_base)
and the piece's full name, and returns a `kit.anim.Clip`.

Archie, holding the Core up on his left palm (HOLD, bits/_corekit.py); each starts and ends on HOLD, his eyes
going up to the projection (PROJ: up, and to his left, screen right, where archie-stage.js `project()` puts it):

    present(body, name)      the presenter's sweep of his free right hand, proud: behold
    double_take(body, name)  up at the projection, a glance away, and snapping back to it, eyes wide
    lean_in(body, name)      he leans in up to it and squints, and straightens again
    protest(body, name)      two jabs at his own chest (MY core), then a finger up at the projection
    deadpan(body, name)      he turns to the reader: a flat look, a slow blink, the shoulders dropping

Archie with his hands free (REST to REST):

    serious(body, name)      a fist to his mouth (ahem), chin up, a grave little nod: what follows is serious

The agents (holo-agent figures, on Archie's own skeleton, so these play on them; from REST):

    agent_heave(body, name)    loop: both arms up overhead, pushing, knees pumping: heaving something up
    agent_point(body, name)    REST -> held: the right arm out to the side, pointing (at the sign); ends there
    agent_stop(body, name)     REST -> held: the right palm out at the reader: stop right there; ends there
    agent_marshal(body, name)  loop: the right arm sweeping across in front, again and again: come on through
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

PROJ = (14, 30)                 # his eyes on the projection: up, to his left (degrees)


def V(*a):
    return Vector(a)


def loop_clip(name, T):
    return K.loop_clip(name, T)


def _eyes_up(k):
    return look((PROJ[0] * k, PROJ[1] * k)) + K.eyes_on_core(1 - k)


# --------------------------------------------------------------------------------------------- Archie
def present(body, name, T=2.4):
    """HOLD -> HOLD: the presenter's sweep, proud; his eyes go to the projection and back to the reader."""
    L = body.lib
    rw = K.rest_wrist(body, -1)
    c = Clip(name, T)
    c.key(0.0, K.HOLD)
    proud = K.HOLD.copy()
    proud.set("head", -4, 10, 4)
    proud.set("chest", -6, 6, 0)
    proud.face = {"grin": 1.0}
    c.key(0.5, proud, "back")
    c.key(T - 0.5, proud, "linear")
    c.key(T, K.HOLD, "inout")

    def solve(t, p, skel):
        K.held(body, p)
        a = pulse(t, 0.1, 0.4, T - 1.1, 0.5)
        if a > 0.01:
            body.hand_to(p, -1, rw.lerp(V(-0.36, -0.5, 1.4), a), elbow=(0.5, 0.3, -0.5),
                         hand_rot=L.hand_world((0.7, -0.6, 0.2), (0, 0, 1)) if a > 0.5 else None)
            L.open_hand(p, -1, 10 * a)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(lambda t: _eyes_up(pulse(t, 0.9, 0.3, T - 1.7, 0.4)))
    c.layer(blink_layer([0.7]))
    return c


def double_take(body, name, T=2.0):
    """HOLD -> HOLD: a look up at the projection, a glance back at the reader, and snapping back to it with
    his eyes wide and his brows up; he leans back a touch, and settles."""
    c = Clip(name, T)
    c.key(0.0, K.HOLD)
    up = K.HOLD.copy()
    up.set("head", -8, 16, 6)
    up.face = {"grin": 0.6}
    away = K.HOLD.copy()
    away.set("head", -2, -4, 0)
    away.face = {"grin": 0.8}
    snap = up.copy()
    snap.set("head", -12, 22, 9)
    snap.face = {"wide": 0.9, "oh": 0.4}
    c.key(0.3, up, "inout")
    c.key(0.62, away, "inout")
    c.key(0.8, snap, "snap")
    c.key(T - 0.45, snap, "linear")
    c.key(T, K.HOLD, "inout")

    def solve(t, p, skel):
        K.held(body, p)
        back = pulse(t, 0.75, 0.08, T - 1.4, 0.5)
        body.lib.hips(body, p, dy=0.04 * back, pitch=-3 * back)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)

    def face(t):
        p = Pose()
        d = pulse(t, 0.76, 0.05, T - 1.3, 0.4)
        brows(p, 1.8 * d, 2.0 * d, 1.2 * d)
        p.both("lid_up", x=10 * d)
        u = min(1.0, pulse(t, 0.12, 0.15, 0.3, 0.1) + pulse(t, 0.76, 0.05, T - 1.3, 0.3))
        return p + _eyes_up(u)

    c.layer(face)
    return c


def lean_in(body, name, T=2.6):
    """HOLD -> HOLD: he leans in up towards the projection, squinting at it, and straightens again."""
    c = Clip(name, T)
    c.key(0.0, K.HOLD)
    lean = K.HOLD.copy()
    lean.set("head", -14, 18, 12)
    lean.set("chest", 4, 10, -6)
    lean.face = {"flat": 0.6, "smirk_L": 0.3}
    c.key(0.6, lean, "inout")
    c.key(T - 0.6, lean, "linear")
    c.key(T, K.HOLD, "inout")

    def solve(t, p, skel):
        k = pulse(t, 0.0, 0.6, T - 1.2, 0.6)
        body.lib.hips(body, p, dx=0.08 * k, dy=-0.04 * k, roll=-5 * k, yaw=6 * k)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0.03 * k, -0.04 * k, 0.03 * k))
        body.plant(p, 1)
        body.plant(p, -1, roll=10 * k)
        return p

    c.solve(solve)

    def face(t):
        p = Pose()
        k = pulse(t, 0.3, 0.4, T - 1.3, 0.5)
        p.both("lid_up", x=-18 * k)              # squinting
        p.both("lid_lo", x=-10 * k)
        brows(p, -0.8 * k, -0.4 * k, 0.4 * k)
        return p + _eyes_up(min(1.0, smooth(0.1, 0.4, t) * (1 - smooth(T - 0.4, T, t))))

    c.layer(face)
    return c


def protest(body, name, T=2.4):
    """HOLD -> HOLD: two jabs of his right forefinger at his own chest -- MY core -- and the finger up at the
    projection, indignant."""
    L = body.lib
    rw = K.rest_wrist(body, -1)
    c = Clip(name, T)
    c.key(0.0, K.HOLD)
    cross = K.HOLD.copy()
    cross.set("head", -6, 10, -4)
    cross.set("chest", -6, 4, 0)
    cross.face = {"grit": 0.8, "frown": 0.5}
    c.key(0.35, cross, "inout")
    c.key(T - 0.4, cross, "linear")
    c.key(T, K.HOLD, "inout")
    chest = V(-0.05, -0.36, 1.5)                 # his right wrist with the fingertip on his chest
    up = V(-0.05, -0.55, 1.95)                   # ... and pointing up at the projection, across him
    jab = (0.45, 0.75)

    def solve(t, p, skel):
        K.held(body, p)
        a = pulse(t, 0.05, 0.3, T - 0.8, 0.45)
        tap = max(pulse(t, j - 0.08, 0.08, 0.02, 0.1) for j in jab)
        go = smooth(1.0, 1.35, t)
        if a > 0.01:
            tgt = chest + V(0, -0.06 * (1 - tap), 0)
            tgt = tgt.lerp(up, go)
            body.hand_to(p, -1, rw.lerp(tgt, a), elbow=(0.5, 0.25, -0.5),
                         hand_rot=L.hand_world((0.2, 0.6, -0.4), (1, 0, 0)) if go < 0.5 else
                         L.hand_world((0.45, -0.5, 0.75), (1, 0, 0)))
            L.point(p, -1)
            p.add("hand_R", 0, 0, 8 * math.sin(math.tau * t * 4) * smooth(1.4, 1.6, t) * (1 - smooth(T - 0.6, T, t)))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)

    def face(t):
        p = Pose()
        k = pulse(t, 0.2, 0.2, T - 0.7, 0.3)
        brows(p, -1.4 * k, -0.6 * k, 0.8 * k)
        g = smooth(1.0, 1.35, t) * (1 - smooth(T - 0.4, T, t))
        return p + look((PROJ[0] * g, PROJ[1] * g * 0.6)) + look((-6 * (1 - g) * k, 0))

    c.layer(face)
    return c


def deadpan(body, name, T=2.2):
    """HOLD -> HOLD: he turns to the reader, a flat look, a slow blink, the shoulders dropping: really?"""
    c = Clip(name, T)
    c.key(0.0, K.HOLD)
    flat = K.HOLD.copy()
    flat.set("head", 0, -4, 0)
    flat.set("chest", 2, 0, 0)
    flat.face = {"flat": 1.0}
    c.key(0.45, flat, "inout")
    c.key(T - 0.4, flat, "linear")
    c.key(T, K.HOLD, "inout")

    def solve(t, p, skel):
        k = pulse(t, 0.3, 0.4, T - 1.1, 0.4)
        p.both("shoulder", z=-5 * k)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0, 0, -0.03 * k))
        body.lib.hips(body, p, dz=-0.012 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)

    def face(t):
        p = Pose()
        b = pulse(t, 0.9, 0.25, 0.25, 0.35)       # the slow blink
        p.both("lid_up", x=-46 * b)
        p.both("lid_lo", x=20 * b)
        k = pulse(t, 0.3, 0.3, T - 1.0, 0.4)
        p.both("lid_up", x=-12 * k * (1 - b))     # heavy lids
        return p + look((0, 0)) + K.eyes_on_core(0.0)

    c.layer(face)
    return c


def serious(body, name, T=2.0):
    """REST -> REST: a fist to his mouth (ahem), chin up, a grave nod: what follows is serious."""
    L = body.lib
    rw = K.rest_wrist(body, -1)
    c = Clip(name, T)
    c.key(0.0, L.REST)
    grave = L.REST.copy()
    grave.set("head", -8, 0, 0)
    grave.set("chest", -6, 0, 0)
    grave.face = {"flat": 0.7, "smile": 0.2}
    nod = grave.copy()
    nod.set("head", 10, 0, 0)
    c.key(0.5, grave, "inout")
    c.key(1.1, grave, "linear")
    c.key(1.35, nod, "inout")
    c.key(1.6, grave, "inout")
    c.key(T, L.REST, "inout")
    mouth = V(-0.06, -0.48, 1.84)

    def solve(t, p, skel):
        a = pulse(t, 0.0, 0.35, 0.55, 0.35)
        cough = pulse(t, 0.4, 0.06, 0.04, 0.1) + pulse(t, 0.62, 0.06, 0.04, 0.1)
        if a > 0.01:
            body.hand_to(p, -1, rw.lerp(mouth + V(0, -0.02 * cough, 0), a), elbow=(0.4, 0.2, -0.7),
                         hand_rot=L.hand_world((0.6, 0.1, 0.8), (0, 1, 0)) if a > 0.5 else None)
            L.fist(p, -1, a)
        p.add("chest", 6 * cough, 0, 0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(blink_layer([0.45, 1.75]))
    return c


# --------------------------------------------------------------------------------------------- agents
def _agent_feet(body, p, bob=0.0):
    body.lib.hips(body, p, dz=-bob)
    body.plant(p, 1)
    body.plant(p, -1)


def agent_heave(body, name, T=1.0):
    """Loop: both arms up overhead, palms up, pushing; the knees pumping with each shove."""
    L = body.lib
    c = loop_clip(name, T)
    base = L.REST.copy()
    base.set("head", -14, 0, 0)
    base.face = {"grit": 1.0}
    c.key(0.0, base)

    def solve(t, p, skel):
        k = 0.5 - 0.5 * math.cos(math.tau * t / T)          # 0 low .. 1 shoved up
        for sg in (1, -1):
            body.hand_to(p, sg, V(0.22 * sg, -0.18, 1.78 + 0.22 * k), elbow=(0.6, 0.1, -0.3),
                         hand_rot=L.hand_world((0, -0.3, 1), (0, 0.2, 1)))
            L.open_hand(p, sg, 8)
        _agent_feet(body, p, bob=0.12 * (1 - k))
        return p

    c.solve(solve)
    return c


def agent_point(body, name, T=1.0, side=1):
    """REST -> held: the arm on `side` (1 his left, screen right) out to that side, pointing; ends there."""
    L = body.lib
    c = Clip(name, T)
    c.key(0.0, L.REST)
    at = L.REST.copy()
    at.set("head", -4, 30 * side, 0)
    at.set("chest", 0, 10 * side, 0)
    at.face = {"grit": 0.6}
    c.key(0.35, at, "back")
    c.key(T, at, "linear")
    rw = K.rest_wrist(body, side)

    def solve(t, p, skel):
        k = min(1.0, smooth(0.0, 0.35, t) * 1.0)
        body.hand_to(p, side, rw.lerp(V(0.9 * side, -0.25, 1.62), k), elbow=(0.3, 0.6, -0.2),
                     hand_rot=L.hand_world((side, -0.1, 0.05), (0, 0, -1)) if k > 0.5 else None)
        L.point(p, side)
        jab = 0.04 * pulse(t, 0.55, 0.08, 0.0, 0.15)
        p.move("hips", 0, 0, 0)
        _agent_feet(body, p, bob=jab)
        return p

    c.solve(solve)
    return c


def agent_stop(body, name, T=0.8):
    """REST -> held: the right palm out at the reader, fingers up: stop right there; ends there."""
    L = body.lib
    c = Clip(name, T)
    c.key(0.0, L.REST)
    at = L.REST.copy()
    at.set("head", -8, 0, 0)
    at.set("chest", -6, 0, 0)
    at.face = {"flat": 1.0}
    c.key(0.25, at, "back")
    c.key(T, at, "linear")
    rw = K.rest_wrist(body, -1)

    def solve(t, p, skel):
        k = smooth(0.0, 0.25, t)
        body.hand_to(p, -1, rw.lerp(V(-0.18, -0.72, 1.55), k), elbow=(0.5, 0.4, -0.5),
                     hand_rot=L.hand_world((0, 0.1, 1), (0, -1, 0)) if k > 0.4 else None)
        L.open_hand(p, -1, 6)
        lw = K.rest_wrist(body, 1)
        body.hand_to(p, 1, lw.lerp(V(0.36, -0.08, 1.08), k), elbow=(0.6, 0.5, -0.2))    # the other on his hip
        _agent_feet(body, p)
        return p

    c.solve(solve)
    return c


def agent_marshal(body, name, T=1.2, side=1):
    """Loop: the right arm sweeping across in front of him towards `side` (1 his left) and back, the head
    nodding the way it goes: come on, through you go."""
    L = body.lib
    c = loop_clip(name, T)
    base = L.REST.copy()
    base.face = {"grin": 1.0}
    c.key(0.0, base)

    def solve(t, p, skel):
        u = 0.5 - 0.5 * math.cos(math.tau * t / T)          # 0 out to his right .. 1 across to `side`
        out = V(-0.75, -0.45, 1.25)
        across = V(0.55 * side, -0.55, 1.15)
        body.hand_to(p, -1, out.lerp(across, u), elbow=(0.5, 0.3, -0.5),
                     hand_rot=L.hand_world((side * (2 * u - 1), -0.6, 0.1), (0, 0, -1)))
        L.open_hand(p, -1, 8)
        p.add("head", 6 * math.sin(math.tau * t / T), 20 * side * (u - 0.5), 0)
        p.add("chest", 0, 12 * side * (u - 0.5), 0)
        _agent_feet(body, p, bob=0.02 * abs(math.sin(math.tau * t / T)))
        return p

    c.solve(solve)
    return c
