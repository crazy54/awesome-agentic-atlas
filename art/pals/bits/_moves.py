"""Pieces several of the props builder's bits share, written once and named per bit (bits/__init__.py skips
this module: it has no NAME). Each takes a pal's `Body` (its `.lib` the pal's base clip module) and the full
clip name, and returns a `kit.anim.Clip` that starts and ends on the pal's REST unless it says otherwise.

    hop_up(body, name)        up from behind an edge and a landing: the page lifts the pal from below the
                              edge's line (hidden there) over the first HOP_RISE seconds
    whistle(body, name)       two fingers to his mouth, a whistle for help, a look off to one side
    rest_wrists(body)         {side: the wrist's place at REST, feet planted}
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

HOP_RISE = 0.45


def loop_clip(name, T):
    """A loop's clip: T seconds of whole, even frames, baked with its closing frame (kit.anim.bake drops the
    closing frame of a `loop` clip and build_bits keeps every other frame, which would shorten the loop and
    make it jump); the page loops it."""
    n = int(round(T * 30))
    assert n % 2 == 0 and abs(n / 30 - T) < 1e-6, f"{name}: a loop needs an even number of frames"
    return Clip(name, T, loop=False, frames=n)


def V(*a):
    return Vector(a)


def rest_wrists(body):
    L = body.lib
    out = {}
    for sg in (1, -1):
        q = L.REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        out[sg] = L.wrist_of(body, q, sg)
    return out


def hop_up(body, name, T=1.2):
    L = body.lib
    up = L.REST.copy()
    up.both("upper_arm", x=-20, z=60)
    up.both("forearm", x=30)
    L.open_hand(up, 1, 12)
    L.open_hand(up, -1, 12)
    up.face = {"wide": 0.6, "grin": 0.4}
    c = Clip(name, T)
    c.key(0.0, up)
    c.key(HOP_RISE, up, "linear")
    c.key(T, L.REST, "out")

    def solve(t, p, skel):
        land = pulse(t, HOP_RISE, 0.08, 0.05, 0.45)
        L.hips(body, p, dz=-0.18 * land, pitch=10 * land)
        p.add("chest", 6 * land, 0, 0)
        p.add("head", -8 * land, 0, 0)
        tuck = 1 - smooth(HOP_RISE - 0.1, HOP_RISE, t)
        body.plant(p, 1, lift=0.12 * tuck)
        body.plant(p, -1, lift=0.08 * tuck)
        return p

    c.solve(solve)
    if hasattr(L, "crest_follow"):
        c.layer(lambda t: L.crest_follow(t * 8, 2.0 * pulse(t, HOP_RISE, 0.05, 0.1, 0.5)))
    return c


def whistle(body, name, T=1.8, side=-1):
    """Two fingers of the `side` hand (-1 right) to his mouth, a sharp whistle, then a look off to his left
    as if calling someone over."""
    L = body.lib
    RW = rest_wrists(body)
    c = Clip(name, T)
    c.key(0.0, L.REST)
    w = L.REST.copy()
    w.set("head", -10, 0, 0)
    w.set("chest", -6, 0, 0)
    w.face = {"oh": 1.0}
    c.key(0.35, w)
    c.key(T - 0.45, w, "linear")
    c.key(T, L.REST)
    mouth = V(0.0, -0.36, 1.9)

    def solve(t, p, skel):
        k = pulse(t, 0.0, 0.35, T - 0.8, 0.45)
        body.hand_to(p, side, RW[side].lerp(mouth + V(side * 0.02, -0.08, -0.1), k), elbow=(0.5, 0.3, -0.5),
                     hand_rot=L.hand_world((0, 0.3, 1), (0, 1, 0)) if k > 0.5 else None)
        L.point(p, side)
        p.side("middle_1", side, 0, 0, 0)
        p.side("middle_2", side, 0, 0, 0)
        p.side("middle_3", side, 0, 0, 0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    blow = lambda t: pulse(t, 0.45, 0.05, 0.5, 0.1)
    c.layer(lambda t: brows(Pose(), 1.2 * blow(t), 1.6 * blow(t), 1.0 * blow(t)) + look((6, 14 * smooth(0.9, 1.2, t))))
    return c


def pull_rope(body, name, T=1.4):
    """Loops: a tug-of-war heave, facing along the rope (his -Y): both hands on it at his waist, leaning
    back on a braced front leg, a big heave each loop."""
    L = body.lib
    RW = rest_wrists(body)
    c = loop_clip(name, T)
    st = L.REST.copy()
    st.face = {"grit": 1.0}
    c.key(0.0, st)

    def solve(t, p, skel):
        heave = 0.5 + 0.5 * math.sin(math.tau * t / T)
        L.hips(body, p, dy=0.12 + 0.08 * heave, dz=-0.12 - 0.04 * heave, pitch=-10 - 8 * heave)
        p.add("spine", -4 - 4 * heave, 0, 0)
        p.add("chest", 6, 0, 0)
        p.add("head", 10 + 4 * heave, 0, 0)
        for sg, dy in ((1, -0.06), (-1, 0.1)):
            tgt = Vector((sg * 0.06, -0.52 + dy + 0.08 * heave, 1.02 - 0.04 * heave))
            body.hand_to(p, sg, tgt, elbow=(0.3, 0.6, -0.4), hand_rot=L.hand_world((-sg * 0.9, -0.3, 0), (0, 0, 1)))
            L.fist(p, sg, 0.95)
        body.plant(p, 1, pos=(0.0, -0.32, 0), roll=-14)          # front foot braced, toe up
        body.plant(p, -1, pos=(0.0, 0.2, 0), roll=10)
        return p

    c.solve(solve)
    c.layer(lambda t: brows(Pose(), -1.2, -0.6, 0.6) + Pose(face={"grit": 0.3 * math.sin(math.tau * t / T)}))
    return c


def knocked_down(body, name, T=1.6, lurch=(0.0, -0.3, 0.0)):
    """Thrown off balance (a lurch of the hips by `lurch` metres first), down on his bottom: ends seated on
    the floor, arms flung, dazed (not on REST: follow with get_up)."""
    L = body.lib
    RW = rest_wrists(body)
    c = Clip(name, T)
    c.key(0.0, L.REST)
    dazed = L.REST.copy()
    dazed.face = {"oh": 1.0}
    c.key(0.3, dazed)
    c.key(T, dazed, "linear")
    lx, ly, lz = lurch

    def solve(t, p, skel):
        u = smooth(0.0, 0.25, t)
        k = smooth(0.15, 0.6, t)
        bump = pulse(t, 0.6, 0.06, 0.02, 0.2)
        L.seated(p, body, min(1.0, k + 0.06 * bump))
        L.hips(body, p, dx=lx * u * (1 - k), dy=ly * u * (1 - k), dz=lz * u * (1 - k))
        f = L.sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])
        fl = pulse(t, 0.1, 0.25, 0.3, 0.6)
        for sg in (1, -1):
            hk = smooth(0.5, 1.0, t)
            tgt = Vector((sg * 0.62, -0.1, 1.5)).lerp(Vector((sg * 0.42, 0.42, 0.14)), hk)
            body.hand_to(p, sg, RW[sg].lerp(tgt, max(fl, hk)), elbow=(0.5, 0.4, -0.2))
            L.open_hand(p, sg, 14 * fl)
        return p

    c.solve(solve)
    c.layer(lambda t: brows(Pose(), 1.6, 1.8, 1.0) + look((8 * math.sin(t * 9) * smooth(0.6, 0.9, t), 0)))
    return c


def get_up(body, name, T=1.8):
    """From sitting on the floor (as knocked_down leaves him) back up to REST, a dust-off on the way."""
    L = body.lib
    RW = rest_wrists(body)
    c = Clip(name, T)
    dazed = L.REST.copy()
    dazed.face = {"flat": 0.8}
    c.key(0.0, dazed)
    c.key(T - 0.3, dazed, "linear")
    c.key(T, L.REST)

    def solve(t, p, skel):
        k = 1 - smooth(0.2, 1.2, t)
        L.seated(p, body, k, lean=10 * pulse(t, 0.1, 0.3, 0.3, 0.5))
        f = L.sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])
        for sg in (1, -1):
            if k > 0.05:
                knee = body.where(p, f"shin{'_L' if sg > 0 else '_R'}")
                body.hand_to(p, sg, knee + Vector((0, -0.05, 0.08)), elbow=(0.6, 0.2, -0.4))
        dust = math.sin(t * 24) * pulse(t, 1.25, 0.1, 0.3, 0.1)
        if dust:
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg] + Vector((0.03 * dust * sg, -0.12, 0.05)), elbow=(0.5, 0.4, -0.6))
        return p

    c.solve(solve)
    return c
