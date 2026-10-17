"""Wrong way up: Archie leads the way; Brick follows, carrying a big app card (a picture of one) in front of
him. They stop and face the reader, and the card is upside down. Archie presents it, grandly. Brick, without
a word, turns it the right way up. Archie carries on presenting as if nothing had happened.

FORMATION (metres, x across the page, from Brick, both facing the reader): Archie stands ARCHIE_X from Brick
(to his right, the page's left). Brick holds the card (props/app-card.glb at CARD_SCALE, its face to the
reader) by its side edges, its middle at CARD; the page keeps the card's middle between his `grip_L` and
`grip_R` every frame, facing as he faces. In `turn` he turns it a half turn in its own plane, his hands
travelling round its rim: the page turns the card through pi, eased in-out, from TURN[0] to TURN[1] seconds
(anticlockwise as the reader sees it, the way his hands go).

    archie  wrong-way-up/present   the grand presentation: a sweep of the hand at the card, a spiel to the
                                   reader that does not look at the card while it turns, another sweep
    brick   wrong-way-up/carry     the walk, the card held out in front of him (edge on to the reader while he
                                   walks across the page)
            wrong-way-up/hold      holding it up, still (loops)
            wrong-way-up/turn      a half turn of the card, deadpan; his hands go round with it, then
                                   come back behind it to its sides; starts and ends on `hold`
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, brows as abrows, look, stride_foot
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "wrong-way-up"
CAST = ("archie", "brick")
ARCHIE_X = -1.95                # Archie, from Brick
CARD_SCALE = 1.8                # the app card prop is 1.2 x 0.8 m: this makes it 2.16 x 1.44
HALF = (0.6 * CARD_SCALE, 0.4 * CARD_SCALE)
CARD = (0.0, -0.62, 1.5)        # its middle, Brick's frame, as he holds it
TURN = (0.35, 2.05)             # seconds into wrong-way-up/turn: the half turn


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
    REST, hips, open_hand, hand_world, point = L.REST, L.hips, L.open_hand, L.hand_world, L.point
    out = []

    def rest_wrist(sg):
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        return L.wrist_of(body, q, sg)

    RW = {1: rest_wrist(1), -1: rest_wrist(-1)}
    edge = V(-ARCHIE_X - HALF[0], CARD[1], CARD[2])            # the card's near edge, from Archie

    T = 8.2
    c = Clip(f"{NAME}/present", T)
    c.key(0.0, REST)
    grand = REST.copy()
    grand.set("chest", -8, 10, 0)
    grand.set("head", -8, -6, -4)
    grand.face = {"grin": 1.0}
    spiel = REST.copy()
    spiel.set("chest", -6, -4, 0)
    spiel.set("head", -4, -8, 4)
    spiel.face = {"grin": 0.6, "ee": 0.4}
    c.key(0.6, grand, "back")
    c.key(2.4, grand, "linear")
    c.key(3.0, spiel, "inout")
    c.key(5.6, spiel, "linear")
    c.key(6.2, grand, "back")
    c.key(7.5, grand, "linear")
    c.key(T, REST, "inout")

    def present_solve(t, p, skel):
        # the sweep at the card (left hand, palm up), held; the spiel (right hand counting points); the sweep
        sw = max(pulse(t, 0.1, 0.5, 2.0, 0.5), pulse(t, 5.8, 0.4, 1.4, 0.6))
        tgt = edge + V(-0.35, -0.05, -0.2)
        body.hand_to(p, 1, RW[1].lerp(tgt, sw), elbow=(0.5, 0.3, -0.5),
                     hand_rot=hand_world((0.8, -0.5, 0.1), (0, 0, 1)) if sw > 0.5 else None)
        open_hand(p, 1, 12 * sw)
        sp = pulse(t, 2.7, 0.4, 2.6, 0.5)
        if sp > 0.01:
            beat = math.sin(math.tau * (t - 2.7) / 0.9)
            tgt = V(-0.28, -0.42, 1.42 + 0.05 * beat)
            body.hand_to(p, -1, RW[-1].lerp(tgt, sp), elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((0.1, -0.4, 1), (0.2, -1, 0)) if sp > 0.5 else None)
            point(p, -1)
        hips(body, p, roll=-3 * sw, yaw=6 * sw)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(present_solve)

    def present_face(t):
        p = Pose()
        b = pulse(t, 0.4, 0.3, 1.8, 0.4) + pulse(t, 6.0, 0.3, 1.2, 0.4)
        abrows(p, 1.2 * b, 1.5 * b, 1.1 * b)
        talk = pulse(t, 2.8, 0.2, 2.6, 0.3) * max(0.0, math.sin(t * 13))
        p.face["oh"] = 0.4 * talk
        # at the card on the sweeps; at the reader through the spiel (not once at the card)
        at = pulse(t, 0.3, 0.3, 1.9, 0.3) + pulse(t, 5.9, 0.3, 1.3, 0.3)
        return p + look((-6 * at, 22 * at))

    c.layer(present_face)
    c.layer(blink_layer([2.9, 5.1]))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    rw = L.rest_wrists(body)
    mid = V(*CARD)

    def at_grip(pt, hr):
        return pt - hr.col[1] * 0.23 - hr.col[2] * 0.16

    def hands_on(p, phi, k=1.0, bob=0.0, back=0.0):
        """Both hands on the middles of the card's side edges as it stands turned by phi (0: upright, the left hand
        on its left edge), the right opposite;
        each hand's fingers wrapped over the rim, palm in towards the card's middle; `back` metres behind it."""
        for sg, a in ((1, phi), (-1, phi + math.pi)):
            rim = mid + V(HALF[0] * math.cos(a), back, HALF[0] * math.sin(a) + bob)    # its side edges turn on a circle
            inward = (mid - rim).normalized()
            hr = L.hand_world((-inward.x * 0.2, -1.0, -inward.z * 0.2), inward)
            body.hand_to(p, sg, rw[sg].lerp(at_grip(rim + V(0, 0.04, 0), hr), k), elbow=(0.9, 0.5, -0.4),
                         hand_rot=hr if k > 0.5 else None)
            p.fingers(sg, 40 * k, spread=2, thumb=30 * k)

    # ---- carry: the walk, holding the card out in front --------------------------------------------
    T = L.WALK_PERIOD
    c = Clip(f"{NAME}/carry", T, loop=True, frames=int(round(T * 30)))
    base = REST.copy()
    base.set("chest", -3, 0, 0)
    c.key(0.0, base)

    def carry_layer(t):
        u = t / T
        p = Pose()
        dip = math.cos(math.tau * 2 * (u - 0.1))
        L.hips(body, p, dz=-0.045 + 0.028 * dip, dx=0.05 * math.sin(math.tau * (u - 0.07)),
               roll=-2.5 * math.sin(math.tau * (u - 0.07)))
        p.add("head", 1.2 * dip, -2 * math.sin(math.tau * u), 0)
        return p

    c.layer(carry_layer)

    def carry_solve(t, p, skel):
        hands_on(p, 0.0, bob=0.015 * math.cos(math.tau * 2 * (t / T - 0.1)))
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, L.WALK_STRIDE, L.WALK_STANCE, ph, height=0.12, toe_off=20.0,
                                        heel_strike=-10.0)
            body.plant(p, sg, pos=(0, y, 0), roll=roll, lift=lift, yaw=4)
        return p

    c.solve(carry_solve)
    out.append(c)

    # ---- hold ----------------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/hold", T, loop=True)
    c.key(0.0, REST)

    def hold_solve(t, p, skel):
        hands_on(p, 0.0, bob=0.006 * math.sin(math.tau * t / T))
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(hold_solve)
    c.layer(breathe(T, 1.0))
    c.layer(L.blinks([1.7]))
    out.append(c)

    # ---- turn: a half turn of the card in its own plane, his hands round its rim ------------------------
    T = 2.6
    c = Clip(f"{NAME}/turn", T)
    c.key(0.0, REST)

    def turn_solve(t, p, skel):
        # the hands go round with the card (its half turn), then let go and come back to their own sides
        # behind it (where the card hides them), so the piece ends on `hold`
        phi = math.pi * ease("inout", smooth(TURN[0], TURN[1], t))
        regrip = ease("inout", smooth(TURN[1] + 0.05, T - 0.1, t))
        hands_on(p, phi * (1 - regrip), back=0.3 * math.sin(math.pi * regrip))
        lean = math.sin(phi)
        L.hips(body, p, roll=-3 * lean)
        p.add("chest", 0, 0, -4 * lean)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(turn_solve)

    def turn_face(t):
        p = Pose()
        k = pulse(t, 0.1, 0.3, 2.0, 0.2)
        p.face.update({"smile": -0.6 * k, "flat": 0.6 * k})
        L.lids(p, 0.3 * k)
        return p + look((-14 * k, 0))

    c.layer(turn_face)
    out.append(c)
    return out
