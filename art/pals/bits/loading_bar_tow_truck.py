"""The loading-bar tow truck: while the README viewer is loading a file, Archie hooks a rope to a loading bar
(a picture of one, with wheels) and pulls. It won't budge. Zip pushes. Brick wanders over, looks at it, and
lets off the hand brake -- and the bar shoots forward, bowling Archie over, and fills up as it rolls.

The page stands the bar (prop `loading-bar`) on the viewer's top edge, Archie at its tow ring end (screen
right) facing back along it, draws the rope from his hands to the ring, and plays the bar's `brake_release`,
`roll` and `fill` clips when Brick's hand meets the lever (BRAKE_AT on Brick's clock).

FORMATION (metres from the bar's origin, on the edge; x screen right):
    bar     (0, 0, 0), towed towards +x
    archie  (ARCHIE_X, 0, 0), facing back along the rope towards the bar (screen left)
    zip     (ZIP_X, 0, 0), behind the bar, facing it
    brick   beside the brake lever at the bar's back end

Pieces (Archie):
    loading-bar-tow-truck/hook   down on his haunches at the tow ring: the hook on
    loading-bar-tow-truck/pull   loops: the heave (`_moves.pull_rope`)
    loading-bar-tow-truck/fall   the bar comes at him: down on his bottom
    loading-bar-tow-truck/up     back up
Zip pushes with his own `push` loop. Brick (clips/brick_base.py), beyond the bar facing back along it (screen
left), the lever on its back end ahead of him:
    loading-bar-tow-truck/release  a look at the bar, a stoop, his left forefinger flicks the hand brake off
                                   (BRAKE_AT)
"""
from __future__ import annotations

from mathutils import Vector

from bits._moves import get_up, knocked_down, pull_rope, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "loading-bar-tow-truck"
CAST = ("archie", "zip", "brick")
ARCHIE_X, ZIP_X = 2.1, -1.3
BRAKE_AT = 0.7


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    return out


def archie_clips(body):
    L = body.lib
    RW = rest_wrists(body)
    out = []
    TH = 2.0
    c = Clip(f"{NAME}/hook", TH)
    c.key(0.0, L.REST)
    hk = L.REST.copy()
    hk.set("head", 16, 0, 0)
    hk.face = {"grit": 0.5, "smirk_L": 0.5}
    c.key(0.5, hk)
    c.key(TH - 0.4, hk, "linear")
    c.key(TH, L.REST)
    ring = Vector((0.0, -0.6, 0.3))

    def hook_solve(t, p, skel):
        k = pulse(t, 0.0, 0.5, TH - 0.9, 0.4)
        L.hips(body, p, dz=-0.55 * k, pitch=14 * k)
        p.add("spine", 8 * k, 0, 0)
        twist = 0.03 * pulse(t, 0.9, 0.1, 0.3, 0.2)
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(ring + Vector((sg * (0.06 + twist), 0.12, 0.08)), k), elbow=(0.6, 0.3, -0.2))
            L.fist(p, sg, 0.8 * k)
        body.plant(p, 1, knee_out=0.14 * k)
        body.plant(p, -1, knee_out=0.14 * k)
        return p

    c.solve(hook_solve)
    c.layer(lambda t: look((-20, 0)))
    out.append(c)
    out.append(pull_rope(body, f"{NAME}/pull"))
    out.append(knocked_down(body, f"{NAME}/fall", lurch=(0.0, 0.4, 0.05)))
    out.append(get_up(body, f"{NAME}/up"))
    return out


def brick_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    T = 2.4
    c = Clip(f"{NAME}/release", T)
    c.key(0.0, L.REST)
    st = L.REST.copy()
    st.set("head", 18, 0, 0)
    st.face = {"flat": 1.0}
    c.key(0.4, st)
    c.key(T - 0.4, st, "linear")
    c.key(T, L.REST)
    lever = Vector((0.25, -0.75, 0.9))

    def release_solve(t, p, skel):
        bend = pulse(t, 0.0, 0.5, 0.6, 0.6)
        L.hips(body, p, dz=-0.2 * bend, pitch=22 * bend, dy=0.06 * bend)
        p.add("spine", 10 * bend, 0, 0)
        flick = smooth(BRAKE_AT - 0.08, BRAKE_AT + 0.05, t)
        tgt = lever + Vector((0, -0.16 * flick, 0.05 * flick))
        body.hand_to(p, 1, RW[1].lerp(tgt, bend), elbow=(0.5, 0.4, -0.5))
        L.point(p, 1)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(release_solve)
    c.layer(lambda t: L.brows(Pose(), 0.8 * pulse(t, 1.2, 0.2, 0.6, 0.3), 0.4, 0.0, side=1))
    return [c]
