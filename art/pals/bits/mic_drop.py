"""The mic drop: Archie, standing on the spotlight, presents its project into a tiny microphone (it has a
FRAGILE sticker on it), holds the mic out at arm's length and drops it, and turns away. Brick, beside him,
lunges with surprising speed and catches it a hand's breadth off the floor, looks it over, and hands it back.
Then he taps the sticker with one enormous finger, twice. Archie looks at it.

FORMATION (metres, x across the page, from Archie, both facing the reader): Brick stands BRICK_X from
Archie (to Archie's right, the page's left). The page keeps the mic upright on Archie's `grip_R` until DROP_AT
seconds into `drop`, lets it fall into Brick's `grip_L` (Brick's `save` starts at that moment; his palm is under
it CATCH_AT seconds in), moves it to Archie's `grip_R` at HAND_AT seconds into Brick's `save` (Archie's
`take` is started TAKE_LEAD seconds before, so his hand meets it there), and Brick's taps on it fall at TAPS.

    archie  mic-drop/present   the mic at his mouth, the other arm sweeping out over the spotlight
            mic-drop/drop      the mic held out at arm's length, a beat, let go; chin up, turned away
            mic-drop/take      a double take; his right hand takes it from Brick, holds it up in front of him
                               for the taps, and lowers it
            mic-drop/sheepish  he looks at the sticker, then at the reader; a sheepish grin
    brick   mic-drop/save      the lunge and the catch, a look at it, back to Archie, then a finger on the
                               sticker, twice
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "mic-drop"
CAST = ("archie", "brick")
BRICK_X = -2.6                  # Brick, from Archie (to his right)
DROP = (-0.74, -0.25, 1.62)     # Archie's right wrist as he holds it out, his frame
DROP_AT = 0.95                  # seconds into mic-drop/drop: he lets go
CATCH = (-0.78, -0.25, 0.3)     # where Brick's palm meets it, Archie's frame
CATCH_AT = 0.6                  # seconds into mic-drop/save: Brick's palm under it (the fall's length)
HAND = (-0.95, -0.45, 1.38)     # where it changes hands, Archie's frame
HAND_AT = 3.6                   # seconds into mic-drop/save: it is Archie's again
TAKE_LEAD = 1.2                 # Archie's take starts this long before HAND_AT
HELD = (-0.32, -0.48, 1.38)     # Archie holding it up in front of him for the taps, his frame
TAPS = (4.65, 5.2)              # seconds into mic-drop/save: Brick's fingertip on the sticker


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
    REST, hips, fist, open_hand, hand_world = L.REST, L.hips, L.fist, L.open_hand, L.hand_world
    out = []

    def rest_wrist(sg):
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        return L.wrist_of(body, q, sg)

    RW = {1: rest_wrist(1), -1: rest_wrist(-1)}
    grip = hand_world((0.5, -0.3, 0.2), (0.2, 0.9, -0.2))          # a fist round the mic, knuckles to the reader

    def at_grip(pt, hr):
        """The wrist that puts his grip bone on `pt` with the hand turned `hr` (archie.py: 0.14 m along, 0.07 off
        the palm)."""
        return pt - hr.col[1] * 0.14 - hr.col[2] * 0.07

    # ---- present -----------------------------------------------------------------------------------
    T = 3.4
    c = Clip(f"{NAME}/present", T)
    c.key(0.0, REST)

    def present_solve(t, p, skel):
        m = pulse(t, 0.1, 0.45, 2.4, 0.45)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.1, -0.36, 1.8), m), elbow=(0.5, 0.4, -0.6),
                     hand_rot=grip if m > 0.5 else None)
        fist(p, -1, 0.85)
        sw = pulse(t, 0.6, 0.5, 1.4, 0.5)
        tgt = V(0.55 + 0.25 * smooth(0.6, 1.6, t), -0.5, 1.3 - 0.15 * smooth(0.6, 1.6, t))
        body.hand_to(p, 1, RW[1].lerp(tgt, sw), elbow=(0.5, 0.3, -0.5),
                     hand_rot=hand_world((0.7, -0.6, -0.1), (0, 0, 1)) if sw > 0.5 else None)
        open_hand(p, 1, 12 * sw)
        hips(body, p, roll=-3 * sw)
        p.add("chest", -6 * m, 6 * sw, 0)
        p.add("head", -4 * m, 10 * sw, 0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(present_solve)

    def present_face(t):
        p = Pose()
        k = pulse(t, 0.3, 0.2, 2.4, 0.4)
        p.face.update({"grin": -0.5 * k, "wide": 0.5 * k, "ee": 0.3 * k})
        abrows(p, 1.0 * k, 1.3 * k, 0.9 * k)
        return p + look((-10 * pulse(t, 0.7, 0.3, 1.2, 0.3), 14 * pulse(t, 0.7, 0.3, 1.2, 0.3)))

    c.layer(present_face)
    c.layer(blink_layer([2.6]))
    out.append(c)

    # ---- drop: long enough that the cool pose is still held when Brick's `save` cues his double take ------
    T = 3.4
    c = Clip(f"{NAME}/drop", T)
    c.key(0.0, REST)
    out_at = V(*DROP)

    def drop_solve(t, p, skel):
        k = pulse(t, 0.05, 0.5, DROP_AT - 0.5, 0.9)
        body.hand_to(p, -1, RW[-1].lerp(out_at, k), elbow=(0.3, 0.6, -0.2),
                     hand_rot=hand_world((-1, -0.1, 0.0), (0, 0.2, -1)) if k > 0.5 else None)
        if t < DROP_AT:
            fist(p, -1, 0.85 * smooth(0.0, 0.3, t))
        else:
            open_hand(p, -1, 14 * smooth(DROP_AT, DROP_AT + 0.08, t))
        away = smooth(DROP_AT + 0.05, DROP_AT + 0.5, t) * (1 - smooth(T - 0.3, T, t))
        p.add("chest", -6 * away, 8 * away, 0)
        p.add("head", -14 * away, 30 * away, 0)
        p.side("upper_arm", 1, x=10 * away, z=-6 * away, add=True)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(drop_solve)

    def drop_face(t):
        p = Pose()
        s = pulse(t, 0.2, 0.3, 2.6, 0.3)
        p.face.update({"grin": -0.4 * s, "smirk_L": 0.9 * s})
        p.both("lid_up", x=-22 * smooth(DROP_AT, DROP_AT + 0.3, t) * (1 - smooth(T - 0.4, T, t)))
        abrows(p, 0.0, 1.2 * s, 1.0 * s, side=1)
        return p + look((0, -20 * pulse(t, 0.2, 0.3, 0.4, 0.2) + 10 * smooth(DROP_AT, DROP_AT + 0.4, t)))

    c.layer(drop_face)
    out.append(c)

    # ---- take: the double take, and his hand meets Brick's at HAND -------------------------------------
    T = 4.6
    c = Clip(f"{NAME}/take", T)
    c.key(0.0, REST)
    hand, held = V(*HAND), V(*HELD)

    def take_solve(t, p, skel):
        snap = pulse(t, 0.0, 0.15, 3.8, 0.5)
        p.add("head", 0, -26 * snap, 0)
        p.add("chest", 0, -8 * snap, 0)
        reach = smooth(0.35, TAKE_LEAD, t)
        back = smooth(TAKE_LEAD + 0.1, TAKE_LEAD + 0.7, t)
        down = smooth(3.9, 4.5, t)
        tgt = RW[-1].lerp(at_grip(hand, grip), ease("inout", reach)).lerp(at_grip(held, grip), ease("inout", back))
        tgt = tgt.lerp(RW[-1], down)
        body.hand_to(p, -1, tgt, elbow=(0.4, 0.4, -0.5),
                     hand_rot=grip if 0.4 < reach and down < 0.6 else None)
        if t > TAKE_LEAD - 0.1:
            fist(p, -1, 0.85 * (1 - down))
        else:
            open_hand(p, -1, 8 * reach)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(take_solve)

    def take_face(t):
        p = Pose()
        j = pulse(t, 0.0, 0.1, 0.6, 0.4)
        p.face.update({"grin": -1.0 * pulse(t, 0.0, 0.1, 3.9, 0.5), "oh": 0.7 * j, "flat": 0.5 * smooth(0.8, 1.2, t)})
        abrows(p, 2.0 * j, 2.2 * j, 1.6 * j)
        at_mic = pulse(t, 1.5, 0.3, 2.2, 0.4)
        return p + look((-24 * at_mic, -22 * (1 - at_mic) * pulse(t, 0.0, 0.15, 3.8, 0.5)))

    c.layer(take_face)
    c.layer(blink_layer([2.4]))
    out.append(c)

    # ---- sheepish --------------------------------------------------------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/sheepish", T)
    c.key(0.0, REST)
    sh = REST.copy()
    sh.set("head", -2, 0, -8)
    sh.both("shoulder", z=8)
    sh.face = {"smirk_R": 0.6, "grin": 0.2}
    c.key(0.5, sh, "inout")
    c.key(2.0, sh, "linear")
    c.key(T, REST, "inout")

    def sheep_face(t):
        p = Pose()
        k = pulse(t, 0.3, 0.3, 1.6, 0.4)
        abrows(p, 1.4 * k, 0.8 * k, -0.2 * k)
        return p + look((-4 * k, -6 * k))

    c.layer(sheep_face)
    c.solve(L.stand(body))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    rw = L.rest_wrists(body)
    off = V(-BRICK_X, 0, 0)                                       # Archie's frame to Brick's
    catch, hand, held = V(*CATCH) + off, V(*HAND) + off, V(*HELD) + off
    inspect = V(0.6, -0.95, 1.55)
    palm_up = L.hand_world((0.25, -1, 0.1), (0, 0, 1))
    offer = L.hand_world((0.6, -0.8, 0.0), (0.0, 0.0, 1))

    def at_grip(pt, hr):
        """The wrist that puts his grip bone on `pt` (brick.py: 0.23 m along the hand, 0.16 off the palm)."""
        return pt - hr.col[1] * 0.23 - hr.col[2] * 0.16

    T = 7.6
    c = Clip(f"{NAME}/save", T)
    c.key(0.0, REST)

    def save_solve(t, p, skel):
        # ---- the body: a lunge to his left and a dip for the catch; up again
        lunge = pulse(t, 0.0, CATCH_AT, 0.3, 1.0)
        L.hips(body, p, dx=0.45 * lunge, dz=-0.52 * lunge, dy=0.06 * lunge, pitch=20 * lunge, roll=14 * lunge)
        p.add("spine", 10 * lunge, 0, -8 * lunge)
        p.add("chest", 8 * lunge, 10 * lunge, -10 * lunge)
        p.add("head", 10 * lunge, 0, 0)
        # ---- the left hand: catch, inspect, offer, point
        if t < CATCH_AT:
            k = ease("out", t / CATCH_AT)
            tgt, hr = rw[1].lerp(at_grip(catch, palm_up), k), palm_up if k > 0.3 else None
        elif t < 1.8:
            k = ease("inout", smooth(0.8, 1.8, t))
            tgt, hr = at_grip(catch, palm_up).lerp(at_grip(inspect, palm_up), k), palm_up
        elif t < HAND_AT:
            k = ease("inout", smooth(2.4, HAND_AT, t))
            tgt, hr = at_grip(inspect, palm_up).lerp(at_grip(hand, offer), k), palm_up if k < 0.5 else offer
        else:
            # after the hand-off: withdraw, then the finger on the sticker, twice, then away
            w = smooth(HAND_AT, HAND_AT + 0.45, t)
            pt = pulse(t, HAND_AT + 0.45, 0.4, TAPS[1] - HAND_AT - 0.45, 0.8)
            tap = max(pulse(t, TAPS[0] - 0.12, 0.12, 0.02, 0.15), pulse(t, TAPS[1] - 0.12, 0.12, 0.02, 0.15))
            aim = held + V(-0.12, -0.08, 0.02)                            # the sticker, on Archie's mic
            d = (aim - V(0.84, 0.3, 1.9)).normalized()
            fing = L.hand_world(d, (0, 0, 1))
            tip = aim - d * (0.16 - 0.14 * tap)
            park = at_grip(hand, offer).lerp(V(0.9, -0.5, 1.3), w)
            tgt = park.lerp(tip - d * 0.6, pt)
            hr = fing if pt > 0.3 else offer
            back = smooth(6.6, 7.4, t)
            tgt = tgt.lerp(rw[1], back)
            if back > 0.6:
                hr = None
        body.hand_to(p, 1, tgt, elbow=(0.8, 0.4, -0.5), hand_rot=hr)
        if t < CATCH_AT + 0.05:
            L.open_hand(p, 1, 6)
        elif t < HAND_AT + 0.1:
            p.fingers(1, 30, spread=4, thumb=20)
        elif t < 6.6:
            L.point(p, 1)
        body.plant(p, 1, pos=(0.55 * lunge, -0.1 * lunge, 0), yaw=L.STANCE, knee_out=0.15 * lunge)
        body.plant(p, -1, yaw=L.STANCE, knee_out=0.1 * lunge)
        return p

    c.solve(save_solve)

    def save_face(t):
        p = Pose()
        a = pulse(t, 0.0, 0.1, 0.5, 0.4)
        L.brows(p, 1.4 * a, 1.6 * a, 1.0 * a)
        insp = pulse(t, 1.0, 0.4, 1.2, 0.4)
        to_a = pulse(t, 2.3, 0.3, 4.2, 0.6)
        L.brows(p, 0.5 * insp, 0.8 * insp, 0.3 * insp)
        p.face.update({"smile": -0.6 * (insp + to_a), "flat": 0.6 * (insp + to_a)})
        b = pulse(t, 4.4, 0.3, 1.4, 0.5)
        L.brows(p, 0.6 * b, 1.8 * b, 1.4 * b, side=-1)
        L.lids(p, 0.25 * to_a)
        p.add("head", 8 * insp, 14 * to_a, 0)
        return p + look((-24 * pulse(t, 0.0, 0.1, 0.6, 0.3) - 18 * insp - 10 * to_a, 22 * pulse(t, 0.0, 0.1, 0.6, 0.3) + 6 * insp + 16 * to_a))

    c.layer(save_face)
    c.layer(L.blinks([2.2, 6.9]))
    out.append(c)
    return out
