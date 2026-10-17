"""Archie and the Atlas Core: the poses and pieces every Atlas Core bit shares. Not a bit itself
(`bits.all_bits()` skips modules whose names start with an underscore); the Core bits import it.

THE CORE IN HIS HANDS. The Core (art/pals/core.py) is docked in his belly, on his `core` bone, and held on
his left palm: the page keeps it at `grip_L` plus PALM along the grip's Z, upright, as archie-core.js does
for the `core` act. These pieces are archie_base's `core-show` act cut into parts a bit strings together:

    take(body, name)     REST -> HOLD: his left hand to the dock, takes the Core (at GRAB seconds the page moves
                         it from his `core` bone to his palm), and up, palm up, in front of his chest
    hold(body, name)     HOLD, held, looping: breathing, a slow bob, his eyes on it
    back(body, name)     HOLD -> REST: down to the dock (at DOCK seconds the page moves it back), the hand away

HOLD is REST with his left wrist at archie_base.CORE_HOLD, palm up, the fingers cupped round the ball. A piece
that "starts (ends) on HOLD" starts (ends) exactly there. `held(body, p, k)` puts the arm there, k of the way
from where it hangs at rest, for bits writing their own pieces round the Core.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth
import archie_base as AB

GRAB = 0.62                     # take: the Core leaves the dock for his palm
DOCK = 0.86                     # back: ... and goes back
PALM = 0.085                    # the ball's centre above grip_L, along its Z (archie-core.js PALM)
HOLD_WRIST = Vector(AB.CORE_HOLD)
CORE_AT = Vector((0.092, -0.583, 1.582))         # the Core's centre, held (HOLD), in his frame (measured: grip_L
                                                 # posed at HOLD, plus PALM along its Z) -- for other pals to reach
DOCK_HAND = Vector((0.12, -0.22, 1.205))        # his left wrist taking it from the dock (core-show's)
PALM_UP = AB.hand_world((-0.35, -0.9, 0.05), (0, 0, 1))
PALM_IN = AB.hand_world((-0.3, -0.2, -1), (-1, 0, 0))
ELBOW = (0.55, 0.35, -0.5)


def V(*a):
    return Vector(a)


def rest_wrist(body, side):
    q = AB.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    return AB.wrist_of(body, q, side)


def held(body, p, k=1.0, wrist=None, cup=30.0):
    """The left arm holding the Core up, `k` of the way from rest (`wrist` overrides where the wrist goes)."""
    if k <= 0.001:
        return p
    rw = rest_wrist(body, 1)
    body.hand_to(p, 1, rw.lerp(wrist if wrist is not None else HOLD_WRIST, k), elbow=ELBOW,
                 hand_rot=PALM_UP if k > 0.3 else None)
    p.fingers(1, cup * k + 18 * (1 - k), spread=6, thumb=20 * k + 12 * (1 - k))
    return p


def hold_pose():
    """The key pose under HOLD: chin down a little towards the Core, the chest turned to it."""
    p = AB.REST.copy()
    p.set("head", 10, 6, -3)
    p.set("chest", 2, 4, 0)
    return p


HOLD = hold_pose()


def eyes_on_core(k):
    """His eyes on the Core in his left hand, `k` of the way."""
    return look((-18 * k, 14 * k))


def take(body, name, T=1.2):
    """REST -> HOLD: reach to the dock, take the Core (GRAB), bring it up, palm up (ease back)."""
    c = Clip(name, T)
    c.key(0.0, AB.REST)
    down = AB.REST.copy()
    down.set("head", 18, 6, -4)
    down.set("chest", 6, 4, 0)
    c.key(0.45, down, "inout")
    c.key(T, HOLD, "inout")
    rw = rest_wrist(body, 1)

    def solve(t, p, skel, rw=rw):
        if t < GRAB:
            k = smooth(0.12, GRAB, t)
            body.hand_to(p, 1, rw.lerp(DOCK_HAND, k), elbow=ELBOW, hand_rot=PALM_IN if k > 0.5 else None)
            p.fingers(1, 18 + 37 * smooth(0.4, GRAB, t), spread=4 + 2 * k, thumb=12 + 8 * k)
        else:
            k = ease("back", min(1.0, (t - GRAB) / (T - GRAB)))
            body.hand_to(p, 1, DOCK_HAND.lerp(HOLD_WRIST, k), elbow=ELBOW, hand_rot=PALM_UP if k > 0.3 else PALM_IN)
            p.fingers(1, 30, spread=6, thumb=20)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(lambda t: eyes_on_core(smooth(0.1, 0.4, t)))
    return c


def loop_clip(name, T):
    """A loop's clip: whole, even frames, baked with its closing frame (the first again). kit.anim.bake drops
    a `loop` clip's closing frame and build_bits keeps every other frame, which would shorten the loop and
    make it jump; the page loops it."""
    n = int(round(T * 30))
    assert n % 2 == 0 and abs(n / 30 - T) < 1e-6, f"{name}: a loop needs an even number of frames"
    return Clip(name, T, frames=n)


def hold(body, name, T=4.0):
    """HOLD, held, looping: breathing, a slow bob of the hand, a blink, eyes on the Core."""
    c = loop_clip(name, T)
    c.key(0.0, HOLD)

    def solve(t, p, skel):
        bob = 0.01 * math.sin(math.tau * t / T)
        held(body, p, 1.0, HOLD_WRIST + V(0, 0, bob))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(lambda t: eyes_on_core(1.0))
    c.layer(breathe(T / 2, 0.8))
    c.layer(blink_layer([0.4 * T]))
    return c


def back(body, name, T=1.6):
    """HOLD -> REST: the Core down to the dock (DOCK), the hand away, the head up."""
    c = Clip(name, T)
    c.key(0.0, HOLD)
    c.key(0.6, HOLD, "linear")
    c.key(T, AB.REST, "inout")
    rw = rest_wrist(body, 1)

    def solve(t, p, skel, rw=rw):
        if t < DOCK:
            k = smooth(0.0, DOCK, t)
            body.hand_to(p, 1, HOLD_WRIST.lerp(DOCK_HAND, k), elbow=ELBOW, hand_rot=PALM_IN if k > 0.6 else PALM_UP)
            p.fingers(1, 30, spread=6, thumb=20)
        else:
            k = smooth(DOCK, T - 0.1, t)
            body.hand_to(p, 1, DOCK_HAND.lerp(rw, k), elbow=ELBOW, hand_rot=PALM_IN if k < 0.5 else None)
            p.fingers(1, 30 * (1 - k) + 18 * k, spread=6 - 2 * k, thumb=20 * (1 - k) + 12 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(lambda t: eyes_on_core(1 - smooth(0.7, T, t)))
    return c


def sniff_layer(at, dur=0.9):
    """The nose before a sneeze: brows up and in, the lids drooping, the mouth falling open (a face layer)."""
    def f(t):
        k = pulse(t, at, dur * 0.6, dur * 0.4, 0.05)
        if k <= 0:
            return None
        p = Pose()
        brows(p, 1.6 * k, 0.6 * k, -0.4 * k)
        p.both("lid_up", x=-22 * k)
        p.face.update({"grin": -1.0 * k, "open": 0.7 * k})
        return p
    return f
