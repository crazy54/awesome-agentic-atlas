"""Contraband inspection: Archie takes out the Atlas Core. Brick, arms folded, holds out one enormous hand
for it. Archie hands it over, reluctantly. Brick turns it upside down and shakes it like a salt cellar: out
falls the stolen spotlight, three decorative stars and the missing light-switch remote. Brick looks at the
pile, then at Archie. Archie whistles, hands behind his back, looking anywhere else.

FORMATION (metres, x across the page, from Archie, both facing the reader): Brick stands BRICK_X from Archie
(to Archie's left, the page's right). The Core comes out of Archie's dock and onto his left palm with
_corekit's take (at _corekit.GRAB); Archie's `hand-over` puts it at OFFER (his frame) HAND_AT seconds in, where
Brick's palm is under it TAKE_AT seconds into his `inspect` (the page starts the two so those moments
coincide, and moves the Core from Archie's grip_L, PALM up its Z, to Brick's grip_R, BRICK_PALM along its Z).
In `inspect` Brick holds it up, upside down from FLIP[0] to FLIP[1] (the page turns the ball over), and
shakes; things fall out of it at SPAWN seconds.

    archie  contraband-inspection/take       the Core out of his dock and up on his palm (_corekit.take)
            contraband-inspection/hold       holding it up (_corekit.hold; loops)
            contraband-inspection/hand-over  from `hold`: a look at it, a look at Brick, and it goes out to him
            contraband-inspection/whistle    hands behind his back, rocking, looking up and away (loops)
    brick   contraband-inspection/inspect    a hand out; takes it; up, over, three shakes; a look at the pile and
                                             at Archie. Ends holding it in front of his chest (inspect-hold)
            contraband-inspection/inspect-hold  holding it, the look, the right brow up (loops)
"""
from __future__ import annotations

import math

from mathutils import Vector

from . import _corekit as CK
from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "contraband-inspection"
CAST = ("archie", "brick")
BRICK_X = 1.95                  # Brick, from Archie (to his left)
OFFER = (0.62, -0.58, 1.5)      # the Core's middle as Archie holds it out to Brick, Archie's frame
HAND_AT = 1.7                   # seconds into hand-over: it is at OFFER
TAKE_AT = 1.3                   # seconds into inspect: Brick's palm under it
BRICK_PALM = 0.0               # the Core's middle along Brick's grip_R Z (his grip is 16 cm off the palm)
FLIP = (1.9, 4.9)               # seconds into inspect: the Core upside down
SHAKES = ((2.15, 2.75), (3.05, 3.65), (3.95, 4.55))
SPAWN = (2.4, 3.2, 3.32, 3.44, 4.25)        # spotlight, star, star, star, remote
HELD_B = (-0.55, -0.85, 1.55)  # where Brick holds it after (inspect-hold), his frame


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
    REST, hips, hand_world = L.REST, L.hips, L.hand_world
    out = [CK.take(body, f"{NAME}/take"), CK.hold(body, f"{NAME}/hold")]
    rw = CK.rest_wrist(body, 1)
    core_from_wrist = CK.CORE_AT - CK.HOLD_WRIST                  # where the ball sits from his wrist, held
    offer_wrist = V(*OFFER) - core_from_wrist

    # ---- hand-over -------------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/hand-over", T)
    c.key(0.0, CK.HOLD)
    loath = CK.HOLD.copy()
    loath.set("head", 6, 16, 6)
    loath.face = {"grin": 0.0, "flat": 0.8, "smirk_R": 0.3}
    c.key(0.7, loath, "inout")
    c.key(HAND_AT, loath, "linear")
    c.key(T, REST, "inout")

    def over_solve(t, p, skel):
        out_k = ease("inout", smooth(0.8, HAND_AT, t))
        away = smooth(HAND_AT + 0.15, T - 0.1, t)
        wrist = CK.HOLD_WRIST.lerp(offer_wrist, out_k).lerp(rw, away)
        body.hand_to(p, 1, wrist, elbow=CK.ELBOW, hand_rot=CK.PALM_UP if away < 0.6 else None)
        p.fingers(1, 30 * (1 - away) + 18 * away, spread=6, thumb=20 * (1 - away) + 12 * away)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(over_solve)

    def over_face(t):
        p = Pose()
        at_core = pulse(t, 0.0, 0.1, 0.6, 0.3)
        at_brick = pulse(t, 0.7, 0.3, 1.0, 0.4)
        abrows(p, 1.2 * at_brick, 0.8 * at_brick, -0.2 * at_brick)
        return p + look((-18 * at_core, 14 * at_core + 26 * at_brick))

    c.layer(over_face)
    out.append(c)

    # ---- whistle: hands behind his back, rocking heel and toe, looking up and away -------------------------
    T = 3.0
    c = CK.loop_clip(f"{NAME}/whistle", T)
    innocent = REST.copy()
    innocent.set("chest", -6, -8, 0)
    innocent.set("head", -14, -22, 6)
    innocent.face = {"oh": 0.75, "grin": 0.0}
    c.key(0.0, innocent)

    def whistle_solve(t, p, skel):
        u = t / T
        rock = math.sin(math.tau * u)
        hips(body, p, dy=0.03 * rock, dz=0.015 * abs(rock), pitch=-2 * rock)
        for sg in (1, -1):
            body.hand_to(p, sg, V(sg * 0.1, 0.24, 1.0), elbow=(0.7, 0.2, 0.2),
                         hand_rot=hand_world((-sg * 0.7, 0.3, -0.6), (0, 1, 0)))
            p.fingers(sg, 40, thumb=20)
        body.plant(p, 1, roll=18 * max(0.0, rock) - 12 * max(0.0, -rock))
        body.plant(p, -1, roll=18 * max(0.0, rock) - 12 * max(0.0, -rock))
        return p

    c.solve(whistle_solve)

    def whistle_face(t):
        p = Pose()
        abrows(p, 1.6, 1.8, 1.2)
        side = math.sin(math.tau * t / T * 0.5)
        return p + look((16, -18 + 10 * side))

    c.layer(whistle_face)
    c.layer(blink_layer([1.4]))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    rw = L.rest_wrists(body)
    palm_up = L.hand_world((1.0, -0.25, 0.0), (0, 0, 1))         # flat, fingers in across him: the ball shows
    offer = V(*OFFER) - V(BRICK_X, 0, 0)                          # the Core at the hand-over, his frame
    up = V(-0.7, -0.75, 2.25)                                     # held up to shake, his frame
    held = V(*HELD_B)

    def wrist_for(core, hr):
        """The wrist that puts the Core's middle (BRICK_PALM along grip_R's Z) at `core`."""
        grip = core - hr.col[2] * BRICK_PALM
        return grip - hr.col[1] * 0.23 - hr.col[2] * 0.16

    def shake_of(t):
        v = 0.0
        for a, b in SHAKES:
            if a <= t <= b:
                v = math.sin(math.tau * (t - a) * 4.5) * math.sin(math.pi * (t - a) / (b - a))
        return v

    T = 7.8
    c = Clip(f"{NAME}/inspect", T)
    c.key(0.0, REST)

    def inspect_solve(t, p, skel):
        if t < TAKE_AT:
            k = ease("inout", smooth(0.1, TAKE_AT, t))
            tgt, hr = rw[-1].lerp(wrist_for(offer, palm_up), k), palm_up if k > 0.4 else None
        elif t < FLIP[1] + 0.3:
            k = ease("inout", smooth(TAKE_AT + 0.1, FLIP[0], t))
            core = offer.lerp(up, k) + V(0, 0, 0.14 * shake_of(t))
            tgt, hr = wrist_for(core, palm_up), palm_up
        else:
            k = ease("inout", smooth(FLIP[1] + 0.3, FLIP[1] + 1.2, t))
            core = up.lerp(held, k)
            tgt, hr = wrist_for(core, palm_up), palm_up
        body.hand_to(p, -1, tgt, elbow=(0.8, 0.5, -0.4), hand_rot=hr)
        p.fingers(-1, 12, spread=4, thumb=8)
        sh = shake_of(t)
        p.add("chest", 0, -6 * smooth(TAKE_AT, FLIP[0], t), 2 * sh)
        p.add("head", 0, 0, -2 * sh)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(inspect_solve)

    def inspect_face(t):
        p = Pose()
        dead = smooth(0.3, 0.8, t)
        p.face.update({"smile": -0.6 * dead, "flat": 0.6 * dead})
        L.lids(p, 0.25 * dead)
        at_core = pulse(t, 1.5, 0.3, 3.2, 0.3)
        at_pile = pulse(t, 5.0, 0.3, 0.9, 0.3)
        at_archie = smooth(6.3, 6.9, t)
        p.add("head", 12 * at_pile + 4 * at_archie, -8 * at_core - 16 * at_archie, 0)
        b = smooth(6.7, 7.3, t)
        L.brows(p, 0.6 * b, 2.0 * b, 1.6 * b, side=-1)
        return p + look((14 * at_core - 30 * at_pile - 6 * at_archie, -16 * at_core - 6 * at_pile - 22 * at_archie))

    c.layer(inspect_face)
    c.layer(L.blinks([1.0, 5.9]))
    out.append(c)

    # ---- inspect-hold: holding it, the look at Archie, the brow up ----------------------------------------
    T = 3.0
    c = CK.loop_clip(f"{NAME}/inspect-hold", T)
    c.key(0.0, REST)

    def ih_solve(t, p, skel):
        bob = 0.008 * math.sin(math.tau * t / T)
        body.hand_to(p, -1, wrist_for(held + V(0, 0, bob), palm_up), elbow=(0.8, 0.5, -0.4), hand_rot=palm_up)
        p.fingers(-1, 12, spread=4, thumb=8)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(ih_solve)

    def ih_face(t):
        p = Pose()
        p.face.update({"smile": -0.6, "flat": 0.6})
        L.lids(p, 0.25)
        p.add("head", 4, -16, 0)
        L.brows(p, 0.6, 2.0, 1.6, side=-1)
        return p + look((-6, -22))

    c.layer(ih_face)
    c.layer(L.blinks([2.1]))
    out.append(c)
    return out
