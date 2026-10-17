"""The README hostage situation: Archie climbs onto the README viewer and holds a sign up over it, BACK IN 5
MINUTES, so big it hides all of him but his shoes and the tip of his crest. Brick lifts it off. Underneath,
Archie is holding a smaller one: BACK IN 4 MINUTES.

The page stands Archie on the viewer's top edge, facing the reader, and draws the signs (props
`sign-back-in-5` at BIG_SCALE, `sign-back-in-4` at SMALL_SCALE) where his hands are: the big one's board
top edge at the midpoint of his hands from RAISE_SHOW on, the small one's at his chest hands from the reveal.

FORMATION (metres from Archie's root, x to his left = screen right):
    archie  (0, 0, 0), facing the reader
    brick   (BRICK_X, 0, 0), facing Archie (screen right), arm's length from the sign's hook

Pieces (Archie):
    readme-hostage/hop          up from behind the viewer onto its edge (the page lifts him, _moves.HOP_RISE)
    readme-hostage/raise        both hands round behind him and up over his head, the big sign's top edge in
                                them (the page shows the sign from RAISE_SHOW); ends holding it up
    readme-hostage/hold         loops: holding it up, a little sway
    readme-hostage/reveal       from the hold: the arms snap down to his chest (the small sign is in them by
                                REVEAL_SNAP), a deadpan stare at the reader, a blink; ends holding it
    readme-hostage/small        loops: holding the small sign, deadpan
Pieces (Brick, clips/brick_base.py), facing Archie (screen right), his right hand the near one:
    readme-hostage/lift         a big hand on the near edge of the board (LIFT_GRAB), up and back with it,
                                held up at his side; ends holding it
    readme-hostage/look         loops: holding it there, a long look at Archie's smaller sign
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import loop_clip, hop_up, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "readme-hostage"
CAST = ("archie", "brick")
BIG_SCALE, SMALL_SCALE = 5.0, 3.6
RAISE_SHOW = 0.85
REVEAL_SNAP = 0.18
BRICK_X = -2.5
LIFT_GRAB = 0.7
UP_L, UP_R = Vector((0.24, -0.34, 2.06)), Vector((-0.24, -0.34, 2.06))      # wrists, holding the big sign
CHEST_L, CHEST_R = Vector((0.2, -0.42, 1.28)), Vector((-0.2, -0.42, 1.28))  # wrists, holding the small one


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
    out = [hop_up(body, f"{NAME}/hop")]
    hold_hand = L.hand_world((0, 0.2, 1), (0, -1, 0.1))         # fingers up, palm to the reader
    chest_hand = L.hand_world((0, -0.2, 1), (0, -1, 0))

    def up_pose(p, k=1.0, sway=0.0):
        for sg, tgt in ((1, UP_L), (-1, UP_R)):
            body.hand_to(p, sg, RW[sg].lerp(tgt + Vector((sway, 0, 0)), k), elbow=(0.7, 0.2, -0.1),
                         hand_rot=hold_hand if k > 0.6 else None)
            L.fist(p, sg, 0.7 * k)

    # ---- raise: round behind him, then up -------------------------------------------------------------
    TR = 1.8
    c = Clip(f"{NAME}/raise", TR)
    c.key(0.0, L.REST)
    st = L.REST.copy()
    st.set("chest", -6, 0, 0)
    st.set("head", -6, 0, 0)
    st.face = {"grin": 1.0, "smirk_L": 0.5}
    c.key(0.9, st)
    c.key(TR, st, "linear")
    behind = {1: Vector((0.3, 0.26, 1.0)), -1: Vector((-0.3, 0.26, 1.0))}

    def raise_solve(t, p, skel):
        L.hips(body, p, dz=-0.04 * pulse(t, 0.6, 0.2, 0.1, 0.4))
        if t < 0.5:
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg].lerp(behind[sg], smooth(0.0, 0.45, t)), elbow=(0.5, 0.5, -0.6))
        else:
            k = smooth(0.5, RAISE_SHOW, t)
            for sg, tgt in ((1, UP_L), (-1, UP_R)):
                body.hand_to(p, sg, behind[sg].lerp(tgt, k), elbow=(0.7, 0.2 + 0.3 * (1 - k), -0.1),
                             hand_rot=hold_hand if k > 0.6 else None)
                L.fist(p, sg, 0.7 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(raise_solve)
    c.layer(blink_layer([1.3]))
    out.append(c)

    # ---- hold: up, a little sway --------------------------------------------------------------------
    TH = 2.4
    c = loop_clip(f"{NAME}/hold", TH)
    c.key(0.0, st)

    def hold_solve(t, p, skel):
        sway = 0.02 * math.sin(math.tau * t / TH)
        L.hips(body, p, dx=sway * 0.5, roll=-1.5 * math.sin(math.tau * t / TH))
        up_pose(p, 1.0, sway)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(hold_solve)
    c.layer(blink_layer([0.9]))
    out.append(c)

    # ---- reveal: the arms down to his chest, the stare ----------------------------------------------
    TV = 3.0
    c = Clip(f"{NAME}/reveal", TV)
    dead = L.REST.copy()
    dead.set("head", -2, 0, 0)
    dead.face = {"flat": 1.0}
    c.key(0.0, st)
    c.key(REVEAL_SNAP, dead, "snap")
    c.key(TV, dead, "linear")

    def chest_pose(p, k=1.0, frm=None):
        for sg, tgt in ((1, CHEST_L), (-1, CHEST_R)):
            src = frm[sg] if frm else RW[sg]
            body.hand_to(p, sg, src.lerp(tgt, k), elbow=(0.5, 0.3, -0.7), hand_rot=chest_hand if k > 0.5 else None)
            L.fist(p, sg, 0.6)

    def reveal_solve(t, p, skel):
        k = smooth(0.0, REVEAL_SNAP, t)
        chest_pose(p, k, {1: UP_L, -1: UP_R})
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(reveal_solve)

    def reveal_face(t):
        p = Pose()
        b = pulse(t, 1.4, 0.06, 0.12, 0.1)                       # one slow, deliberate blink
        p.both("lid_up", x=-46 * b)
        p.both("lid_lo", x=40 * b)
        p.both("lid_up", x=-10, add=True)
        brows(p, -0.4, -0.2, 0.2)
        return p + look((0, 0))

    c.layer(reveal_face)
    out.append(c)

    # ---- small: holding the small sign, deadpan -----------------------------------------------------
    TS = 3.0
    c = loop_clip(f"{NAME}/small", TS)
    c.key(0.0, dead)

    def small_solve(t, p, skel):
        chest_pose(p)
        p.add("head", 0, 0, 3 * math.sin(math.tau * t / TS))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(small_solve)
    c.layer(lambda t: Pose().both("lid_up", x=-10))
    c.layer(blink_layer([2.2]))
    out.append(c)
    return out


def brick_clips(body):
    """Brick's pieces: beside Archie (BRICK_X), facing him; the big sign's near edge is ahead of him, its
    middle at GRAB in his frame."""
    from bits._moves import loop_clip
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    GRAB, UP, ASIDE = Vector((-0.3, -0.78, 1.25)), Vector((-0.3, -0.62, 2.4)), Vector((-0.55, 0.05, 2.25))
    TL = 2.6
    c = Clip(f"{NAME}/lift", TL)
    c.key(0.0, L.REST)
    flat = L.REST.copy()
    flat.face = {"flat": 1.0}
    c.key(0.6, flat)
    c.key(TL, flat, "linear")

    def where(t):
        if t < LIFT_GRAB:
            return RW[-1].lerp(GRAB, smooth(0.0, LIFT_GRAB, t))
        if t < 1.5:
            return GRAB.lerp(UP, smooth(LIFT_GRAB, 1.5, t))
        return UP.lerp(ASIDE, smooth(1.5, TL - 0.2, t))

    def lift_solve(t, p, skel):
        L.hips(body, p, pitch=6 * pulse(t, 0.3, 0.4, 0.3, 0.4))
        body.hand_to(p, -1, where(t), elbow=(0.5, 0.4, -0.5))
        L.fist(p, -1, smooth(LIFT_GRAB - 0.15, LIFT_GRAB, t))
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(lift_solve)
    out.append(c)
    TK = 3.0
    c = loop_clip(f"{NAME}/look", TK)
    c.key(0.0, flat)

    def look_solve(t, p, skel):
        body.hand_to(p, -1, ASIDE, elbow=(0.5, 0.4, -0.5))
        L.fist(p, -1, 1.0)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(look_solve)
    c.layer(lambda t: L.brows(Pose(), 1.2, 0.6, -0.4, side=1) + look((-6, 0)))
    out.append(c)
    return out
