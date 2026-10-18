"""The missing screw: Archie finds a screw on the floor, shrugs, and pockets it. The card behind him
swings down on its one remaining screw. He slowly looks at the reader. Then, hurriedly, a jump and a slap
at the card, which swings back level, and he leaves whistling as though nothing happened.

The page stands him facing the reader at the foot of a card (the card is the "panel"), with the screw at
his feet, SCREW ahead of his root; he plays:

    missing-screw/spot      notices it, squats, picks it up with his right hand (the page puts the screw in
                            grip_R at GRAB)
    missing-screw/inspect   holds it up, turns it, squints; a small shrug
    missing-screw/pocket    a shrug, and into the pocket on his right hip (the screw goes at POCKET)
    missing-screw/take      (the card has just swung) he freezes; his eyes go to it; slowly back to the
                            reader; deadpan; one slow blink. Ends held.
    missing-screw/fix       the screw back out, a look up over his shoulder, a crouch, a jump with his arm
                            up, a slap at the top of the jump (SLAP: the page swings the card back), lands,
                            dusts his hands
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "missing-screw"
CAST = ("archie",)
SCREW = (-0.12, -0.36)          # the screw on the floor: x (his left +), y (towards the back +), metres
GRAB, POCKET, SLAP = 1.2, 0.8, 1.3


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    REST, hips, fist, open_hand, hand_world = L.REST, L.hips, L.fist, L.open_hand, L.hand_world
    RW = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    out = []

    # ---- spot ---------------------------------------------------------------------------------------
    TS = 2.1
    c = Clip(f"{NAME}/spot", TS)
    c.key(0.0, REST)
    floor = V(SCREW[0], SCREW[1], 0.06)

    def spot(t, p, skel):
        down = pulse(t, 0.35, 0.55, 0.5, 0.6)              # the squat
        hips(body, p, dz=-0.5 * down, dy=0.08 * down, pitch=20 * down)
        p.add("spine", 16 * down, 0, 0)
        p.add("chest", 8 * down, 0, 0)
        reach = pulse(t, 0.45, 0.6, 0.25, 0.6)
        if reach > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(floor + V(0, 0.1, 0.08), reach), elbow=(0.4, 0.5, -0.4),
                         hand_rot=hand_world((0, -0.3, -1), (0, 0, -1)) if reach > 0.5 else None)
        fist(p, -1, smooth(GRAB - 0.1, GRAB + 0.05, t))
        body.plant(p, 1, knee_out=0.1 * down)
        body.plant(p, -1, knee_out=0.1 * down)
        return p

    c.solve(spot)

    def spot_face(t):
        p = Pose()
        n = pulse(t, 0.05, 0.15, 1.6, 0.3)
        p = p + look((-26 * n, -8 * n), head=(14 * n, 0, -6 * n))
        brows(p, 1.2 * pulse(t, 0.1, 0.1, 0.4, 0.3), 1.6 * pulse(t, 0.1, 0.1, 0.4, 0.3), 1.0)
        p.face.update({"oh": 0.6 * pulse(t, 0.1, 0.1, 0.4, 0.3)})
        return p

    c.layer(spot_face)
    out.append(c)

    # ---- inspect ------------------------------------------------------------------------------------
    TI = 1.9
    c = Clip(f"{NAME}/inspect", TI)
    c.key(0.0, REST)

    def inspect(t, p, skel):
        up = pulse(t, 0.0, 0.35, 1.1, 0.4)
        tw = 40 * math.sin(t * 7) * pulse(t, 0.4, 0.15, 0.7, 0.2)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.08, -0.42, 1.78), up), elbow=(0.4, 0.3, -0.6),
                     hand_rot=hand_world((0.2, -0.2, 1), (0.9, -0.3, 0)) if up > 0.5 else None)
        p.add("hand_R", 0, tw, 0)
        fist(p, -1)
        sh = pulse(t, 1.35, 0.15, 0.1, 0.25)
        p.both("shoulder", z=10 * sh, add=True)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(inspect)

    def inspect_face(t):
        p = Pose()
        up = pulse(t, 0.0, 0.35, 1.1, 0.4)
        p = p + look((10 * up, -10 * up), head=(-4 * up, 0, 6 * up))
        p.both("lid_up", x=-20 * up)
        brows(p, -0.6 * up, -0.2 * up, 0.4 * up, side=-1)
        brows(p, 0.8 * up, 1.2 * up, 0.8 * up, side=1)
        p.face.update({"grin": -0.6 * up, "smirk_L": 0.6 * up})
        return p

    c.layer(inspect_face)
    out.append(c)

    # ---- pocket -------------------------------------------------------------------------------------
    TP = 1.5
    c = Clip(f"{NAME}/pocket", TP)
    c.key(0.0, REST)

    def pocket(t, p, skel):
        sh = pulse(t, 0.0, 0.2, 0.2, 0.3)
        p.both("shoulder", z=12 * sh, add=True)
        p.add("head", 0, 0, 10 * sh)
        k = pulse(t, 0.3, 0.45, 0.2, 0.5)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.33, -0.02, 1.02), k), elbow=(0.6, 0.4, -0.2),
                     hand_rot=hand_world((0, 0.2, -1), (1, 0, 0)) if k > 0.5 else None)
        fist(p, -1, 1 - smooth(POCKET, POCKET + 0.15, t))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(pocket)
    c.layer(lambda t: Pose(face={"oh": 0.5 * pulse(t, 0.6, 0.2, 0.5, 0.2), "grin": -0.4 * pulse(t, 0.6, 0.2, 0.5, 0.2)}))
    out.append(c)

    # ---- take ---------------------------------------------------------------------------------------
    TK = 2.8
    c = Clip(f"{NAME}/take", TK)
    held = REST.copy()
    held.face = {"flat": 1.0}
    c.key(0.0, REST)
    c.key(0.12, held, "snap")
    c.key(TK, held, "linear")

    def take(t, p, skel):
        # the freeze: a tiny jolt, then dead still; the eyes do the work
        j = pulse(t, 0.0, 0.05, 0.05, 0.15)
        hips(body, p, dz=0.015 * j)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(take)

    def take_face(t):
        p = Pose()
        # eyes off to his left and up, at the card; then slowly back to the reader
        side = pulse(t, 0.15, 0.25, 0.7, 1.0)
        p = p + look((10 * side, 28 * side), head=(0, 0, 0))
        p.add("head", 0, 8 * side, 0)
        b = pulse(t, 0.1, 0.1, 0.9, 0.6)
        brows(p, 1.4 * b, 1.6 * b, 1.2 * b)
        # the slow blink, looking straight at the reader
        bl = pulse(t, 2.15, 0.25, 0.1, 0.3)
        p.both("lid_up", x=-46 * bl)
        p.both("lid_lo", x=40 * bl)
        return p

    c.layer(take_face)
    out.append(c)

    # ---- fix ----------------------------------------------------------------------------------------
    TF = 2.6
    c = Clip(f"{NAME}/fix", TF)
    c.key(0.0, REST)

    def fix(t, p, skel):
        # out of the pocket (0-0.35), a look up over the shoulder, a crouch (0.5-0.8), the jump (0.8-1.7)
        crouch = pulse(t, 0.45, 0.3, 0.05, 0.15)
        air = max(0.0, math.sin(math.pi * smooth(0.8, 1.75, t))) if 0.8 < t < 1.75 else 0.0
        land = pulse(t, 1.75, 0.06, 0.05, 0.3)
        hips(body, p, dz=-0.18 * crouch + 0.45 * air - 0.12 * land, pitch=10 * crouch)
        reach = pulse(t, 0.7, 0.35, 0.45, 0.35)
        top = V(0.32, -0.08, 2.75)
        if reach > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(top, reach), elbow=(0.5, 0.3, -0.6),
                         hand_rot=hand_world((0.2, 0, 1), (0, 1, 0)) if reach > 0.5 else None)
            open_hand(p, -1, 8)
        elif t < 0.4:
            k = pulse(t, 0.0, 0.15, 0.1, 0.15)
            body.hand_to(p, -1, RW[-1].lerp(V(-0.33, -0.02, 1.02), k), elbow=(0.6, 0.4, -0.2))
        # dusting his hands after: they meet in front and rub
        dust = pulse(t, 2.0, 0.15, 0.3, 0.2)
        if dust > 0.01:
            rub = 0.04 * math.sin(t * 40)
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.07 + rub * sg, -0.42, 1.25), dust), elbow=(0.5, 0.3, -0.5),
                             hand_rot=hand_world((-sg * 0.3, -0.6, 0.2), (-sg, 0, 0)) if dust > 0.5 else None)
                open_hand(p, sg, 0)
        lift = 0.5 * air
        body.plant(p, 1, lift=lift, roll=-15 * air)
        body.plant(p, -1, lift=lift, roll=-15 * air)
        return p

    c.solve(fix)

    def fix_face(t):
        p = Pose()
        up = pulse(t, 0.35, 0.2, 1.0, 0.3)
        p = p + look((24 * up, 10 * up), head=(-22 * up, 0, 0))
        g = pulse(t, 0.8, 0.1, 0.8, 0.3)
        p.face.update({"grit": g, "grin": -g})
        d = pulse(t, 1.9, 0.2, 0.6, 0.2)
        p.face["smile"] = d
        return p

    c.layer(fix_face)
    c.layer(blink_layer([2.35]))
    out.append(c)
    return {"archie": out}
