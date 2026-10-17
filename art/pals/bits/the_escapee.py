"""The escapee: one of the Atlas Core's tiny projected bots climbs out of its world, jumps down onto the page,
waves at Archie and runs off. Archie side-steps after it with an app card held like a tray, lays the card on
the floor in front of it, and when the curious little thing walks on, lifts it up and tips it back into the
world, where it folds its arms and sulks.

Archie holds the Core on his left palm throughout (HOLD, bits/_corekit.py); the card rides his right hand's
`grip_R` (the page attaches it, CARD_ON, and hides it again, CARD_OFF). He faces the reader all along: the bot
lands, and runs, on his left -- screen right.

    the-escapee/take    REST -> HOLD (the Core to his palm at _corekit.GRAB)
    the-escapee/hold    HOLD, looping
    the-escapee/spot    HOLD -> HOLD: a double take down at the bot on the floor by his left foot: hey!
    the-escapee/card    HOLD -> CARD: his right hand behind his back and out again with the card, held low in
                        front of him like a tray (the page shows the card at CARD_ON)
    the-escapee/creep   CARD, looping: side-steps to his left, the card and the Core held steady; the page
                        moves him at CREEP_SPEED, so the feet hold the floor
    the-escapee/offer   CARD -> OFFER: he crouches and lays the card on the floor by his left foot, and waits
    the-escapee/lift    OFFER -> HOLD: up, the card raised to the projection, tipped (TIP), and put away behind
                        his back (the page hides it at CARD_OFF)
    the-escapee/back    HOLD -> REST (the Core back at _corekit.DOCK)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "the-escapee"
CAST = ("archie",)
CARD_ON = 0.62                  # card: the card appears in his hand, coming out from behind his back
CARD_OFF = 2.05                 # lift: ... and goes away behind it again
TIP = 1.2                       # lift: the card tips towards the projection, and the bot slides off
CREEP_PERIOD, CREEP_STANCE, CREEP_STEP = 1.0, 0.6, 0.24
CREEP_SPEED = CREEP_STEP / (CREEP_STANCE * CREEP_PERIOD)        # metres a second, to his left
CARD_WRIST = (-0.22, -0.5, 0.98)    # his right wrist holding the card out like a tray
FLOOR_WRIST = (0.14, -0.62, 0.3)    # ... laying it on the floor by his left foot, crouched


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    hips, open_hand, hand_world = L.hips, L.open_hand, L.hand_world
    HOLD = K.HOLD
    rw = K.rest_wrist(body, -1)
    tray = hand_world((0.25, -0.95, 0.0), (0, 0, 1))           # palm up, fingers forward
    behind = V(-0.3, 0.32, 1.0)                                  # his right hand behind his back
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]

    def card_hand(p, w, at=CARD_WRIST, rot=tray):
        if w > 0.01:
            body.hand_to(p, -1, rw.lerp(V(*at), w), elbow=(0.45, 0.3, -0.7), hand_rot=rot if w > 0.4 else None)
            p.fingers(-1, 26 * w + 18 * (1 - w), spread=4, thumb=30 * w + 12 * (1 - w))

    # ---- spot ------------------------------------------------------------------------------------------
    T = 1.7
    c = Clip(f"{NAME}/spot", T)
    c.key(0.0, HOLD)
    down = HOLD.copy()
    down.set("head", 22, 18, 6)
    down.face = {"wide": 0.7, "oh": 0.4}
    c.key(0.22, HOLD, "linear")
    c.key(0.4, down, "snap")
    c.key(T - 0.4, down, "linear")
    c.key(T, HOLD, "inout")

    def spot_solve(t, p, skel):
        K.held(body, p)
        jump = pulse(t, 0.35, 0.06, 0.2, 0.3)
        hips(body, p, dz=0.02 * jump)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(spot_solve)

    def spot_face(t):
        p = Pose()
        d = pulse(t, 0.38, 0.05, 0.8, 0.3)
        brows(p, 1.8 * d, 2.0 * d, 1.2 * d)
        g = pulse(t, 0.1, 0.1, 0.05, 0.1) + d
        return p + look((-20 * min(1, g), 26 * min(1, g))) + K.eyes_on_core(1 - min(1, g))

    c.layer(spot_face)
    out.append(c)

    # ---- card ------------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/card", T)
    c.key(0.0, HOLD)
    set_ = HOLD.copy()
    set_.set("head", 18, 14, 4)
    set_.face = {"grit": 0.4, "smirk_L": 0.6}
    c.key(0.5, HOLD, "linear")
    c.key(T, set_, "inout")

    def card_solve(t, p, skel):
        K.held(body, p)
        a = smooth(0.0, 0.55, t)
        b = smooth(0.62, T, t)
        tgt = rw.lerp(behind, a).lerp(V(*CARD_WRIST), b)
        rot = tray if b > 0.4 else hand_world((0, 0, -1), (1, 0, 0))
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3 + 0.3 * a * (1 - b), -0.7), hand_rot=rot if a > 0.3 else None)
        p.fingers(-1, 18 + 8 * a, spread=4, thumb=12 + 18 * a)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(card_solve)
    c.layer(lambda t: look((-16 * smooth(0.6, T, t), 20 * smooth(0.6, T, t))) +
            K.eyes_on_core(1 - smooth(0.6, T, t)))
    out.append(c)
    CARD = set_                                  # the key pose under CARD (with the arms as card_hand puts them)

    # ---- creep -----------------------------------------------------------------------------------------
    T = CREEP_PERIOD
    c = K.loop_clip(f"{NAME}/creep", T)
    c.key(0.0, CARD)

    def creep_foot(t, phase):
        u = (t / T + phase) % 1.0
        if u < CREEP_STANCE:
            s = u / CREEP_STANCE
            return CREEP_STEP / 2 - CREEP_STEP * s, 0.0              # sliding to his right as he moves left
        s = (u - CREEP_STANCE) / (1 - CREEP_STANCE)
        return -CREEP_STEP / 2 + CREEP_STEP * (0.5 - 0.5 * math.cos(math.pi * s)), 0.06 * math.sin(math.pi * s)

    def creep_solve(t, p, skel):
        bob = math.cos(math.tau * 2 * t / T)
        hips(body, p, dz=-0.07 - 0.012 * bob, pitch=6)
        p.add("chest", 6, 0, 0)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0, 0, -0.04))
        card_hand(p, 1.0)
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            x, lift = creep_foot(t, ph)
            body.plant(p, sg, pos=(x, 0, 0), lift=lift, roll=12 * (lift > 0.005))
        return p

    c.solve(creep_solve)
    c.layer(lambda t: look((-14, 22)) + Pose(face={"grit": 0.3, "smirk_L": 0.6}))
    out.append(c)

    # ---- offer -----------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/offer", T)
    c.key(0.0, CARD)
    low = CARD.copy()
    low.set("head", 24, 16, 4)
    low.face = {"smirk_L": 0.8}
    c.key(T, low, "inout")

    def offer_solve(t, p, skel):
        k = smooth(0.0, T - 0.2, t)
        hips(body, p, dz=-0.07 * (1 - k) - 0.5 * k, dx=0.08 * k, pitch=6 + 24 * k)
        p.add("chest", 6 + 10 * k, 0, 0)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0.04 * k, -0.05 * k, -0.04 - 0.38 * k))
        card_hand(p, 1.0, V(*CARD_WRIST).lerp(V(*FLOOR_WRIST), k), tray)
        body.plant(p, 1, pos=(0.12 * k, 0, 0), knee_out=0.12 * k)
        body.plant(p, -1, pos=(-0.04 * k, 0.05 * k, 0), roll=30 * k, knee_out=0.1 * k)
        return p

    c.solve(offer_solve)
    c.layer(lambda t: look((-24, 20)) + Pose(face={"grit": 0.3 * (1 - smooth(0, T, t))}))
    c.layer(blink_layer([0.9]))
    out.append(c)

    # ---- lift ------------------------------------------------------------------------------------------
    T = 2.8
    c = Clip(f"{NAME}/lift", T)
    c.key(0.0, low)
    proud = HOLD.copy()
    proud.set("head", -6, 14, 6)
    proud.face = {"grin": 1.0}
    c.key(0.6, proud, "inout")
    c.key(T - 0.4, proud, "linear")
    c.key(T, HOLD, "inout")
    up_w = V(0.12, -0.42, 1.95)                    # the card raised up to his left, to the projection
    tipped = hand_world((0.6, -0.5, 0.6), (0.6, 0.0, 0.8))

    def lift_solve(t, p, skel):
        k = 1 - smooth(0.0, 0.6, t)                  # standing up out of the crouch
        hips(body, p, dz=-0.5 * k, dx=0.08 * k, pitch=30 * k)
        p.add("chest", 16 * k, 0, 0)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0.04 * k, -0.05 * k, -0.42 * k))
        r = smooth(0.25, 0.85, t)                    # the card up to the projection ...
        tip = smooth(TIP - 0.15, TIP + 0.1, t) * (1 - smooth(1.6, 1.8, t))
        away = smooth(1.7, CARD_OFF, t)              # ... and away behind his back
        home = smooth(CARD_OFF, T - 0.1, t)
        if home > 0:
            tgt = behind.lerp(rw, home)
        elif away > 0:
            tgt = up_w.lerp(behind, away)
        else:
            tgt = V(*FLOOR_WRIST).lerp(up_w, r)
        if home > 0.5:
            rot = None
        elif away > 0.5:
            rot = hand_world((0, 0, -1), (1, 0, 0))                 # palm in, going behind his back
        else:
            rot = tipped if tip > 0.5 else tray
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3, -0.7), hand_rot=rot)
        p.fingers(-1, 26 * (1 - home) + 18 * home, spread=4, thumb=30 * (1 - home) + 12 * home)
        body.plant(p, 1, pos=(0.12 * k, 0, 0), knee_out=0.12 * k)
        body.plant(p, -1, pos=(-0.04 * k, 0.05 * k, 0), roll=30 * k, knee_out=0.1 * k)
        return p

    c.solve(lift_solve)
    c.layer(lambda t: look((18 * pulse(t, 0.4, 0.4, 1.0, 0.4), 26 * pulse(t, 0.4, 0.4, 1.0, 0.4))) +
            look((-24 * (1 - smooth(0, 0.5, t)), 20 * (1 - smooth(0, 0.5, t)))) + K.eyes_on_core(smooth(T - 0.6, T, t)))
    c.layer(blink_layer([2.3]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return {"archie": out}
