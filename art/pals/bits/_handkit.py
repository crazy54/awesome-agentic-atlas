"""Hands that go from one hold to the next without a pop: the apology video's and the fake settings panel's
(not a bit itself: `bits.all_bits()` skips modules whose names start with an underscore).

A `Hand` has named states -- (wrist (a function of the pose, so it follows the body), the hand's world
rotation, the elbow's pole, the fingers (curl, spread, thumb)) -- and is driven along a path: the state it
starts in, then (t0, t1, state, easing) moves. Wrist, rotation, pole and fingers all blend, so a piece that
starts in the state the last one ended in starts exactly where it did.

GRIPS. Every pal's `grip_L`/`grip_R` is turned as his hand is: Y along the fingers, Z out of the palm, at
GRIP[pal] (along Y, out along Z) from the wrist. A prop held on a grip lies along the fingers, its front out
of the palm (a remote's buttons, IR end towards the fingertips).
"""
from __future__ import annotations

from mathutils import Vector

from kit.anim import ease

GRIP = {"archie": (0.14, 0.07), "zip": (0.102, 0.055), "brick": (0.23, 0.16)}


def V(*a):
    return Vector(a)


def slerp(a, b, w):
    if w <= 0:
        return a
    if w >= 1:
        return b
    return a.to_quaternion().slerp(b.to_quaternion(), w).to_matrix()


def mixt(a, b, w):
    return tuple(x + (y - x) * w for x, y in zip(a, b))


def rest_hands(body):
    """{side: (wrist, hand world rotation)} at REST, feet planted."""
    q = body.lib.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    out = {}
    for sg, s in ((1, "_L"), (-1, "_R")):
        M = body.skel.fk(q, "hand" + s)["hand" + s]
        out[sg] = (M.translation.copy(), M.to_3x3())
    return out


def wrist_for(grip_at, rot, grip):
    """Where the wrist goes to put the grip at `grip_at`, the hand turned `rot`."""
    return V(*grip_at) - rot @ V(0, grip[0], grip[1])


class Hand:
    def __init__(self, body, side, states):
        self.body, self.side, self.states = body, side, states

    def __call__(self, p, t, path):
        prev = cur = path[0]
        w = 1.0
        for a, b, st, how in path[1:]:
            if t < a:
                break
            prev, cur = cur, st
            w = ease(how, (t - a) / (b - a)) if t < b else 1.0
        s0, s1 = self.states[prev], self.states[cur]
        wr = s0[0](p).lerp(s1[0](p), w)
        self.body.hand_to(p, self.side, wr, elbow=mixt(s0[2], s1[2], w), hand_rot=slerp(s0[1], s1[1], w))
        f0, f1 = s0[3], s1[3]
        c0, c1 = (x if isinstance(x, tuple) else (x, x, x) for x in (f0[0], f1[0]))
        p.fingers(self.side, mixt(c0, c1, w), spread=f0[1] + (f1[1] - f0[1]) * w,
                  thumb=f0[2] + (f1[2] - f0[2]) * w)
        return p
