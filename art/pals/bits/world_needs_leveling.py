"""The world needs leveling: the Atlas Core's world comes up tipped. Archie gets out a spirit level, sets it on
the main island and fiddles -- the stage comes level, and every other island tips. He fiddles again; they tip
further. Brick strolls over and gently takes the level away; once it has gone, everything settles level on its
own.

FORMATION (metres from Archie's root, x to his left -- the page's right -- y back): Archie at (0, 0) and Brick
at BRICK (on his right), both facing the reader. Archie holds the Core on his left palm (HOLD,
bits/_corekit.py) and the level in his right hand, palm down on its top; the page keeps the level on his
`grip_R` (LEVEL_GRIP along the grip's Z, upright) and puts the world beside him so that its main island sits
under the level, whose middle is at LEVEL_AT in his frame while he holds it there (LEVELING).

    archie  world-needs-leveling/take      REST -> HOLD (the Core to his palm at _corekit.GRAB)
            world-needs-leveling/hold      HOLD, looping
            world-needs-leveling/level-out HOLD -> LEVELING: his right hand behind his back and out with the
                                           level (the page shows it at LEVEL_ON), up and onto the island
            world-needs-leveling/fiddle    LEVELING -> LEVELING: nudges and taps, frowning at the bubble
            world-needs-leveling/huh       LEVELING -> LEVELING: a look round at the other islands
            world-needs-leveling/let-go    LEVELING -> HOLD: Brick has it (the page moves it at LET_GO); his
                                           hand comes down empty
            world-needs-leveling/protest   HOLD -> HOLD: a finger up -- but -- and a sag
            world-needs-leveling/back      HOLD -> REST (the Core back at _corekit.DOCK)
    brick   world-needs-leveling/take-level REST -> REST: his left hand out to the level, takes it (TAKE_AT),
                                           and down to his side with it
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows as abrows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "world-needs-leveling"
CAST = ("archie", "brick")
BRICK = (-2.3, 0.2)             # Brick's root, from Archie's
LEVEL_WRIST = (-0.7, -0.38, 1.86)   # Archie's right wrist with the level held out on the island
LEVEL_AT = (-0.84, -0.38, 1.69)     # ... the level's middle (its bottom edge) then (measured: grip_R at LEVELING,
                                    # plus LEVEL_GRIP along its Z, which points straight down)
LEVEL_GRIP = 0.1                # the level's bottom below his palm, along grip_R's Z
LEVEL_ON = 0.6                  # level-out: the level appears in his hand
LET_GO = 0.55                   # let-go: Brick has it
TAKE_AT = 1.1                   # take-level: Brick's hand closes on it


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
    hips, open_hand, point, hand_world = L.hips, L.open_hand, L.point, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    behind = V(-0.3, 0.32, 1.0)
    on_top = hand_world((-1, 0, 0), (0, 0, -1))                # fingers to his right, palm down on it
    wrist = V(*LEVEL_WRIST)
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    LEVELING = HOLD.copy()
    LEVELING.set("head", 2, -22, 4)                            # watching the bubble, up to his right
    LEVELING.set("chest", 0, -8, 0)
    LEVELING.face = {"flat": 0.6, "smirk_R": 0.4}
    bubble = look((10, -24))                                   # his eyes on the level

    def levelling(p, at=None, k=1.0):
        K.held(body, p)
        tgt = rw.lerp(at if at is not None else wrist, k)
        body.hand_to(p, -1, tgt, elbow=(0.5, 0.15, -0.5), hand_rot=on_top if k > 0.5 else None)
        p.fingers(-1, 30 * k + 18 * (1 - k), spread=6, thumb=14)
        body.plant(p, 1)
        body.plant(p, -1)

    # ---- level-out ---------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/level-out", T)
    c.key(0.0, HOLD)
    c.key(0.5, HOLD, "linear")
    c.key(T, LEVELING, "inout")

    def out_solve(t, p, skel):
        a = smooth(0.0, 0.5, t)
        b = smooth(LEVEL_ON, T - 0.1, t)
        K.held(body, p)
        tgt = rw.lerp(behind, a).lerp(wrist, b)
        rot = on_top if b > 0.4 else (hand_world((0, 0, -1), (1, 0, 0)) if a > 0.3 else None)
        body.hand_to(p, -1, tgt, elbow=(0.5, 0.15 + 0.4 * a * (1 - b), -0.5), hand_rot=rot)
        p.fingers(-1, 18 + 12 * a, spread=6, thumb=14)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(out_solve)
    c.layer(lambda t: K.eyes_on_core(1 - smooth(0.6, 1.4, t)) + bubble.scaled(smooth(0.9, T, t)))
    out.append(c)

    # ---- fiddle ------------------------------------------------------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/fiddle", T)
    c.key(0.0, LEVELING)
    frown = LEVELING.copy()
    frown.face = {"grit": 0.6, "flat": 0.4}
    c.key(0.3, frown, "inout")
    c.key(T - 0.3, frown, "linear")
    c.key(T, LEVELING, "inout")

    def fiddle_solve(t, p, skel):
        nudge = 0.012 * math.sin(math.tau * 2.5 * t) * pulse(t, 0.1, 0.2, 1.1, 0.2)
        tap = max(pulse(t, a - 0.05, 0.05, 0.02, 0.08) for a in (1.7, 1.95))
        levelling(p, wrist + V(nudge, 0, -0.012 * tap))
        if tap > 0.01:
            point(p, -1)
        return p

    c.solve(fiddle_solve)

    def fiddle_face(t):
        p = Pose()
        k = pulse(t, 0.2, 0.2, 1.8, 0.2)
        abrows(p, -1.0 * k, -0.4 * k, 0.4 * k)
        return p + bubble

    c.layer(fiddle_face)
    out.append(c)

    # ---- huh ---------------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/huh", T)
    c.key(0.0, LEVELING)
    round_ = LEVELING.copy()
    round_.set("head", -6, -6, 0)
    round_.face = {"oh": 0.5, "flat": 0.5}
    c.key(0.4, round_, "inout")
    c.key(T - 0.4, round_, "linear")
    c.key(T, LEVELING, "inout")

    def huh_solve(t, p, skel):
        levelling(p)
        return p

    c.solve(huh_solve)

    def huh_face(t):
        p = Pose()
        k = pulse(t, 0.2, 0.2, 1.0, 0.3)
        abrows(p, 1.6 * k, 1.4 * k, 0.6 * k)
        dart = math.sin(math.tau * 1.4 * (t - 0.3)) * k
        return p + bubble.scaled(1 - k) + look((14 * k, -30 * dart))

    c.layer(huh_face)
    out.append(c)

    # ---- let-go ------------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/let-go", T)
    c.key(0.0, LEVELING)
    miffed = HOLD.copy()
    miffed.set("head", 0, -24, 0)                               # at Brick, on his right
    miffed.face = {"flat": 1.0}
    c.key(0.5, LEVELING, "linear")
    c.key(T, miffed, "inout")

    def letgo_solve(t, p, skel):
        k = 1 - smooth(LET_GO, T, t)
        levelling(p, k=k)
        if t > LET_GO:
            open_hand(p, -1, 8 * k)
        return p

    c.solve(letgo_solve)
    c.layer(lambda t: bubble.scaled(1 - smooth(LET_GO, T, t)) + look((4, -26)).scaled(smooth(LET_GO, T, t)))
    out.append(c)

    # ---- protest -----------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/protest", T)
    c.key(0.0, miffed)
    but = miffed.copy()
    but.face = {"open": 0.6, "oh": 0.4}
    sag = HOLD.copy()
    sag.set("head", 12, -6, 6)
    sag.both("shoulder", z=-6)
    sag.face = {"flat": 1.0, "frown": 0.3}
    c.key(0.3, but, "inout")
    c.key(0.9, but, "linear")
    c.key(1.4, sag, "inout")
    c.key(T - 0.3, sag, "linear")
    c.key(T, HOLD, "inout")

    def protest_solve(t, p, skel):
        K.held(body, p)
        f = pulse(t, 0.1, 0.25, 0.6, 0.4)
        if f > 0.01:
            body.hand_to(p, -1, rw.lerp(V(-0.42, -0.38, 1.72), f), elbow=(0.45, 0.3, -0.6),
                         hand_rot=hand_world((0, 0, 1), (0, -1, 0)) if f > 0.5 else None)
            point(p, -1)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(protest_solve)
    c.layer(lambda t: look((4 * (1 - smooth(1.0, 1.4, t)), -26 * (1 - smooth(1.0, 1.4, t)))) +
            K.eyes_on_core(smooth(1.3, T, t)))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST, hand_world = L.REST, L.hand_world
    rw = L.rest_wrists(body)
    level = V(*LEVEL_AT) - V(BRICK[0], BRICK[1], 0)            # the level's middle, in his frame
    grab = level + V(-0.12, 0.05, 0.05)                         # his left wrist taking it by the near end
    hr = hand_world((0.85, -0.3, 0.2), (0.0, 0.3, -1.0))
    tuck = V(1.0, 0.25, 1.05)                                   # down at his side with it
    T = 2.6
    c = Clip(f"{NAME}/take-level", T, frames=78)
    c.key(0.0, REST)
    gentle = REST.copy()
    gentle.set("head", 8, 18, 0)
    gentle.face = {"smile": 1.0}
    c.key(0.6, gentle, "inout")
    c.key(1.6, gentle, "linear")
    c.key(T, REST, "inout")

    def solve(t, p, skel):
        k = smooth(0.15, TAKE_AT, t)
        down = smooth(TAKE_AT + 0.25, T - 0.2, t)
        tgt = rw[1].lerp(grab, k).lerp(tuck, down)
        body.hand_to(p, 1, tgt, elbow=(0.7, 0.5, -0.5), hand_rot=hr if k > 0.45 and down < 0.6 else None)
        shut = smooth(TAKE_AT - 0.1, TAKE_AT, t)                  # his hand closing on it
        p.fingers(1, 10 + 40 * shut, spread=2, thumb=10 + 30 * shut)
        p.add("chest", 4 * k * (1 - down), 10 * k * (1 - down), 0)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(solve)
    c.layer(lambda t: look((-10 * pulse(t, 0.3, 0.3, 1.0, 0.4), 16 * pulse(t, 0.3, 0.3, 1.0, 0.4))))
    c.layer(L.blinks([1.9]))
    return [c]
