"""The sneeze: Archie unfolds the Atlas Core's world, his nose twitches, ah... ah... CHOO -- and the world's
islands blow apart. The main one sails over his head into Brick's hands; a little one floats off like a
runaway balloon with Zip running after it. Brick lobs the main one back, the world gathers itself, and Zip
comes back towing the stray on a string.

FORMATION (metres from Archie's root, x to his left -- the page's right -- y back): Archie at (0, 0), Brick at
BRICK (on his right), Zip at ZIP (on his left), all facing the reader. Archie holds the Core on his left palm
(HOLD, bits/_corekit.py).

    archie  the-sneeze/take       REST -> HOLD (the Core to his palm at _corekit.GRAB)
            the-sneeze/hold       HOLD, looping
            the-sneeze/ah         HOLD -> (head back): two winding-up breaths, the head going back, eyes drooping
            the-sneeze/choo       (head back) -> HOLD: the sneeze (CHOO_AT), doubling him forward, and up again
            the-sneeze/sheepish   HOLD -> HOLD: a wipe of his nose on the back of his hand, a look round at
                                  the mess, a sheepish grin
            the-sneeze/back       HOLD -> REST (the Core back at _corekit.DOCK)
    brick   the-sneeze/catch      REST -> HOLDING: a quick dip, the right hand under it as it comes down
                                  (CATCH_AT), up to his chest with the left hand round it too
            the-sneeze/holding    HOLDING, looping: holding it, looking at it
            the-sneeze/toss       HOLDING -> REST: a gentle underhand lob back up to his left (released at
                                  TOSS_AT)
    zip     (everyday clips: run, jump, walk, cheer)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, ease, pulse, smooth
from . import _corekit as K

NAME = "the-sneeze"
CAST = ("archie", "brick", "zip")
BRICK = (-2.4, 0.2)             # Brick's root, from Archie's
ZIP = (2.3, 0.0)                # Zip's
CHOO_AT = 0.16                  # choo: the sneeze itself
CATCH_AT = 0.42                 # catch: the island lands in his right hand
TOSS_AT = 0.72                  # toss: he lets it go
HOLDING = (0.0, -0.95, 1.5)     # Brick: the middle of what he holds in both hands (brick_base.HOLD)


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
    hips, open_hand, hand_world = L.hips, L.open_hand, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    # ---- ah ----------------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/ah", T)
    c.key(0.0, HOLD)
    back1 = HOLD.copy()
    back1.set("head", -14, 4, 4)
    back1.set("chest", -6, 2, 0)
    back1.face = {"open": 0.6, "oh": 0.3}
    back2 = HOLD.copy()
    back2.set("head", -26, 6, 6)
    back2.set("chest", -12, 2, 0)
    back2.face = {"open": 1.0, "wide": 0.3}
    c.key(0.7, back1, "inout")
    c.key(0.95, HOLD, "inout")
    c.key(1.85, back2, "inout")
    c.key(T, back2, "linear")

    def ah_solve(t, p, skel):
        hips(body, p, dy=0.03 * smooth(1.0, 1.9, t), pitch=-4 * smooth(1.0, 1.9, t))
        K.held(body, p)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(ah_solve)
    c.layer(K.sniff_layer(0.2, 0.75))
    c.layer(K.sniff_layer(1.05, 1.15))
    c.layer(lambda t: K.eyes_on_core(1 - smooth(0.1, 0.5, t)) + look((14 * smooth(0.4, 1.9, t), 0)))
    out.append(c)

    # ---- choo --------------------------------------------------------------------------------------------
    T = 1.2
    c = Clip(f"{NAME}/choo", T)
    c.key(0.0, back2)
    fwd = HOLD.copy()
    fwd.set("head", 30, 0, -4)
    fwd.set("chest", 16, 0, 0)
    fwd.face = {"grit": 1.0}
    c.key(CHOO_AT, fwd, "snap")
    c.key(0.5, fwd, "linear")
    c.key(T, HOLD, "inout")

    def choo_solve(t, p, skel):
        jolt = pulse(t, CHOO_AT - 0.04, 0.04, 0.2, 0.5)
        hips(body, p, dy=0.03 * (1 - smooth(0, CHOO_AT, t)) - 0.04 * jolt, dz=-0.04 * jolt, pitch=12 * jolt)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0, -0.04 * jolt, -0.06 * jolt))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(choo_solve)

    def choo_face(t):
        p = Pose()
        k = pulse(t, CHOO_AT - 0.03, 0.03, 0.3, 0.3)
        p.both("lid_up", x=-46 * k)                             # eyes screwed shut
        p.both("lid_lo", x=40 * k)
        abrows(p, -1.4 * k, -0.8 * k, 0.6 * k)
        return p + look((14 * (1 - smooth(0, CHOO_AT, t)), 0)) + K.eyes_on_core(smooth(0.6, T, t))

    c.layer(choo_face)
    c.layer(lambda t: L.crest_follow(t * 6, 3.0 * pulse(t, CHOO_AT, 0.05, 0.2, 0.6)))
    out.append(c)

    # ---- sheepish ----------------------------------------------------------------------------------------
    T = 2.8
    c = Clip(f"{NAME}/sheepish", T)
    c.key(0.0, HOLD)
    wipe = HOLD.copy()
    wipe.set("head", 6, -10, 4)
    wipe.face = {"flat": 0.8}
    round_ = HOLD.copy()
    round_.set("head", -6, 18, 0)
    round_.face = {"smirk_L": 0.3, "flat": 0.4}
    grin = HOLD.copy()
    grin.set("head", -4, 0, 8)
    grin.face = {"grin": 0.8, "smirk_L": 0.6}
    c.key(0.35, wipe, "inout")
    c.key(0.9, wipe, "linear")
    c.key(1.4, round_, "inout")
    c.key(2.0, grin, "inout")
    c.key(T - 0.3, grin, "linear")
    c.key(T, HOLD, "inout")
    nose = V(-0.06, -0.38, 1.82)

    def sheep_solve(t, p, skel):
        K.held(body, p)
        w = pulse(t, 0.1, 0.3, 0.5, 0.35)
        if w > 0.01:
            swipe = math.sin(math.pi * smooth(0.4, 0.85, t))
            tgt = nose + V(0.04 - 0.1 * swipe, 0.02, -0.08)
            body.hand_to(p, -1, rw.lerp(tgt, w), elbow=(0.45, 0.3, -0.6),
                         hand_rot=hand_world((1, 0.1, 0.2), (0, 1, 0)) if w > 0.5 else None)
            L.fist(p, -1, 0.5 * w)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(sheep_solve)
    c.layer(lambda t: look((6, 20 * pulse(t, 1.1, 0.3, 0.3, 0.3))) + look((0, -20 * pulse(t, 0.4, 0.2, 0.4, 0.3))) +
            K.eyes_on_core(smooth(T - 0.5, T, t)))
    c.layer(blink_layer([1.0, 2.2]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST, hips, hand_world = L.REST, L.hips, L.hand_world
    rw = L.rest_wrists(body)
    hold = V(*HOLDING)
    low = V(0.1, -0.95, 0.75)                                   # where it comes down: in front, waist-low
    palm_up = hand_world((0.2, -1, 0.15), (0, 0, 1))
    side = {1: hand_world((-0.3, -1, 0.1), (-1, 0, 0)), -1: hand_world((0.3, -1, 0.1), (1, 0, 0))}

    def both_hands(p, at, k, rk=None):
        """Both palms round something at `at` (the right one under it until `rk` brings it round)."""
        for sg in (1, -1):
            wk = k if sg < 0 else k * (rk if rk is not None else 1.0)
            if wk < 0.01:
                continue
            tgt = at + V(sg * 0.32, 0.05, -0.05)
            body.hand_to(p, sg, rw[sg].lerp(tgt, wk), elbow=(0.7, 0.4, -0.5), hand_rot=side[sg] if wk > 0.5 else None)
            p.fingers(sg, 30 * wk, spread=4, thumb=20 * wk)

    # ---- catch -------------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/catch", T, frames=60)
    c.key(0.0, REST)
    hold_p = REST.copy()
    hold_p.set("head", 16, 0, 0)
    hold_p.face = {"smile": 1.0}
    c.key(T, hold_p, "inout")

    def catch_solve(t, p, skel):
        dive = smooth(0.0, CATCH_AT, t)
        up = smooth(CATCH_AT + 0.1, 1.3, t)
        sink = dive * (1 - up)
        hips(body, p, dz=-0.25 * sink, pitch=14 * sink)
        p.add("spine", 10 * sink, 0, 0)
        p.add("chest", 6 * sink, 0, 0)
        at = low.lerp(hold, ease("inout", up))
        # the right palm under it first, the left joining as it comes up
        body.hand_to(p, -1, rw[-1].lerp(at + V(-0.05, 0.02, -0.2), dive), elbow=(0.6, 0.5, -0.4),
                     hand_rot=palm_up if dive > 0.4 else None)
        p.fingers(-1, 30 * dive, spread=4, thumb=20 * dive)
        both_hands(p, at, smooth(0.6, 1.4, t), rk=0.0)
        body.plant(p, 1, yaw=L.STANCE, knee_out=0.1 * sink)
        body.plant(p, -1, yaw=L.STANCE, knee_out=0.1 * sink)
        return p

    c.solve(catch_solve)

    def catch_face(t):
        p = Pose()
        a = pulse(t, 0.0, 0.1, 0.4, 0.3)
        L.brows(p, 1.0 * a, 1.2 * a, 0.8 * a)
        return p + look((-26 * smooth(0, 0.3, t), 10 * (1 - smooth(0.2, 0.6, t))))

    c.layer(catch_face)
    c.layer(L.blinks([1.5]))
    out = [c]

    # ---- holding -----------------------------------------------------------------------------------------
    c = K.loop_clip(f"{NAME}/holding", 2.0)
    c.key(0.0, hold_p)

    def holding_solve(t, p, skel):
        bob = 0.01 * math.sin(math.tau * t / 2.0)
        at = hold + V(0, 0, bob)
        body.hand_to(p, -1, at + V(-0.05, 0.02, -0.2), elbow=(0.6, 0.5, -0.4), hand_rot=palm_up)
        p.fingers(-1, 30, spread=4, thumb=20)
        both_hands(p, at, 1.0, rk=0.0)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(holding_solve)
    c.layer(lambda t: look((-26, 0)))
    out.append(c)

    # ---- toss --------------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/toss", T, frames=54)
    c.key(0.0, hold_p)
    lob = REST.copy()
    lob.set("head", -14, 16, 0)                                 # watching it go, up to his left
    lob.face = {"smile": 1.0}
    c.key(TOSS_AT, lob, "inout")
    c.key(T - 0.4, lob, "linear")
    c.key(T, REST, "inout")

    def toss_solve(t, p, skel):
        dip = pulse(t, 0.0, 0.3, 0.0, 0.25)
        swing = smooth(0.25, TOSS_AT, t)                        # down a little, then up and out to his left
        home = smooth(TOSS_AT + 0.25, T, t)
        hips(body, p, dz=-0.08 * dip, pitch=6 * dip)
        at = hold + V(0.25 * swing, -0.1 * swing, -0.15 * dip + 0.55 * swing)
        k = 1 - home
        body.hand_to(p, -1, rw[-1].lerp(at + V(-0.05, 0.02, -0.2), k), elbow=(0.6, 0.5, -0.4),
                     hand_rot=palm_up if k > 0.4 else None)
        p.fingers(-1, 30 * k, spread=4, thumb=20 * k)
        both_hands(p, at, k * (1 - smooth(TOSS_AT, TOSS_AT + 0.2, t)), rk=0.0)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(toss_solve)
    c.layer(lambda t: look((-26 * (1 - smooth(0.4, 0.9, t)) + 16 * smooth(0.6, 1.0, t), 14 * smooth(0.6, 1.0, t))))
    out.append(c)
    return out
