"""The inspection scam: Archie, up on a project's card, stamps it QUALITY CHECKED without so much as a glance
at it -- eyes on the reader the whole time -- and leaves the stamp standing on the card while he takes the
credit. Brick picks the stamp up and turns its face to the reader: I LICKED THIS. So does the ink on the card.

The page stands Archie on the card's top edge, facing the reader, the `rubber-stamp` prop (STAMP_SCALE: a
stamp half his height, held by its shaft, STAMP_HOLD above the prop's origin) upright in his left hand from
STAMP_SHOW. At STAMP_HIT it comes down on the card's face below the edge, and the page leaves it standing
there, stuck, when his hand lets go (STAMP_LET); the ink it leaves (`stamp-mark-licked`, INK_SCALE) is where
its pad was.
The stamp has been flipped (its `flip` clip) so the face it prints is I LICKED THIS; QUALITY CHECKED is what
he says.

FORMATION (metres from Archie's root, x to his left = screen right; the card's top edge is z = 0):
    archie  (0, 0, 0)
    stamp   pad at PAD, on the card's face below the edge
    brick   (BRICK_X, 0, 0), beside him on the row of cards, facing him

Pieces (Archie):
    inspection-scam/hop       up onto the card (the page lifts him from below its edge)
    inspection-scam/stamp     the stamp up, a confident look at the reader, down it comes on the card without
                              a look, a wiggle to make it take, and he lets go
    inspection-scam/present   both palms to the card: behold
    inspection-scam/stare     the truth: a slow look from the stamp to the reader, a weak grin, a shrug
    inspection-scam/check     (without Brick) he picks the stamp up himself and reads its face: the same
Pieces (Brick, clips/brick_base.py), facing Archie (screen left), his left hand the near one:
    inspection-scam/turn      a bend, the stamp off the card by its shaft (TURN_TAKE), up in front of his
                              chest (the page turns its face to the reader from TURN_FACE), a raised brow
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import hop_up, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "inspection-scam"
CAST = ("archie", "brick")
STAMP_SCALE, STAMP_HOLD, INK_SCALE = 8.0, 0.055, 3.5
STAMP_SHOW, STAMP_HIT, STAMP_LET = 0.25, 1.35, 2.1
BRICK_X = 2.4
TURN_TAKE, TURN_FACE = 0.8, 1.6


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
    upright = L.hand_world((0, 0, -1), (0, -1, 0))         # fingers down round the handle, palm forward

    # ---- stamp ---------------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/stamp", T)
    c.key(0.0, L.REST)
    smug = L.REST.copy()
    smug.set("head", -8, -10, 6)                              # turned away from the card, at the reader
    smug.set("chest", -4, -6, 0)
    smug.face = {"grin": 1.0, "smirk_L": 0.6}
    c.key(0.5, smug)
    c.key(T - 0.4, smug, "linear")
    c.key(T, L.REST)
    grip_up = Vector((0.5, -0.4, 1.78))                       # wrists: the stamp held high, out to his left,
    grip_down = Vector((0.52, -0.34, 0.74))                   # and down, its pad on the card below the edge

    def stamp_solve(t, p, skel):
        bend = smooth(STAMP_HIT - 0.35, STAMP_HIT, t) * (1 - smooth(STAMP_LET + 0.1, T - 0.2, t))
        L.hips(body, p, dx=0.08 * bend, dz=-0.2 * bend, pitch=8 * bend, roll=-8 * bend)
        p.add("spine", 4 * bend, 0, -6 * bend)
        p.add("chest", 2 * bend, 0, -6 * bend)
        if t < STAMP_HIT - 0.3:
            tgt = RW[1].lerp(grip_up, smooth(0.0, 0.6, t))
        elif t < STAMP_HIT:
            tgt = grip_up.lerp(grip_down, ease("in", (t - (STAMP_HIT - 0.3)) / 0.3))
        elif t < STAMP_LET:
            wig = 0.015 * math.sin((t - STAMP_HIT) * 30) * pulse(t, STAMP_HIT + 0.1, 0.05, 0.4, 0.1)
            tgt = grip_down + Vector((wig, 0, -0.02 * pulse(t, STAMP_HIT, 0.03, 0.05, 0.1)))
        else:
            tgt = grip_down.lerp(RW[1], smooth(STAMP_LET, T - 0.1, t))
        held = STAMP_SHOW < t < STAMP_LET
        body.hand_to(p, 1, tgt, elbow=(0.6, 0.4, -0.2), hand_rot=upright if held and t > 0.5 else None)
        L.fist(p, 1, 0.9 if held else 0.3)
        body.plant(p, 1, pos=(0.1 * bend, 0, 0), knee_out=0.1 * bend)
        body.plant(p, -1, knee_out=0.08 * bend)
        return p

    c.solve(stamp_solve)
    c.layer(lambda t: look((0, -16)) + brows(Pose(), 0.4, 1.4 * pulse(t, 1.0, 0.2, 1.2, 0.3), 0.8, side=1))
    c.layer(blink_layer([0.7, 2.5]))
    out.append(c)

    # ---- present: behold ---------------------------------------------------------------------------
    TP = 2.4
    c = Clip(f"{NAME}/present", TP)
    c.key(0.0, L.REST)
    pr = L.REST.copy()
    pr.set("chest", -8, 0, 0)
    pr.set("head", -10, 0, -4)
    pr.face = {"grin": 1.0, "wide": 0.3}
    c.key(0.4, pr)
    c.key(TP - 0.4, pr, "linear")
    c.key(TP, L.REST)

    def present_solve(t, p, skel):
        k = pulse(t, 0.05, 0.4, TP - 0.9, 0.45)
        for sg in (1, -1):
            tgt = Vector((sg * 0.62 + 0.12, -0.42, 0.92))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.4, 0.2, -0.7),
                         hand_rot=L.hand_world((sg * 0.5 + 0.2, -0.6, -0.4), (0, 0, 1)) if k > 0.5 else None)
            L.open_hand(p, sg, 12)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(present_solve)
    c.layer(lambda t: look((4, 0)) + brows(Pose(), 1.0, 1.4, 1.0))
    out.append(c)

    # ---- stare: the truth dawns ---------------------------------------------------------------------
    TS = 3.2
    c = Clip(f"{NAME}/stare", TS)
    c.key(0.0, L.REST)
    at_stamp = L.REST.copy()
    at_stamp.set("head", 10, 24, -8)
    at_stamp.face = {"oh": 0.8}
    at_you = L.REST.copy()
    at_you.set("head", -2, 0, 8)
    at_you.face = {"grit": 0.7, "smile": 0.3}
    c.key(0.5, at_stamp)
    c.key(1.4, at_stamp, "linear")
    c.key(1.8, at_you, "inout")
    c.key(TS - 0.2, at_you, "linear")
    c.key(TS, L.REST)
    shrug = pulse

    def stare_solve(t, p, skel):
        k = shrug(t, 2.1, 0.3, 0.4, 0.35)
        p.both("shoulder", z=12 * k, add=True)
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(Vector((sg * 0.48, -0.34, 1.12)), k), elbow=(0.15, 0.25, -1.0),
                         hand_rot=L.hand_world((sg * 0.55, -0.82, 0.08), (0, 0, 1)) if k > 0.4 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(stare_solve)
    c.layer(lambda t: brows(Pose(), 1.8 * pulse(t, 0.4, 0.2, 0.9, 0.3), 1.6 * pulse(t, 0.4, 0.2, 0.9, 0.3), 0.6)
            + look((-12 * pulse(t, 0.3, 0.2, 1.0, 0.3), 18 * pulse(t, 0.3, 0.2, 1.0, 0.3))))
    c.layer(blink_layer([1.6]))
    out.append(c)

    # ---- check: (without Brick) he lifts the stamp himself and reads its face -----------------------
    TC = 3.0
    c = Clip(f"{NAME}/check", TC)
    c.key(0.0, L.REST)
    rd = L.REST.copy()
    rd.set("head", 6, 8, 0)
    rd.face = {"flat": 0.6}
    c.key(0.7, rd)
    c.key(TC - 0.4, rd, "linear")
    c.key(TC, L.REST)
    held_at = Vector((0.24, -0.5, 1.5))

    def check_solve(t, p, skel):
        bend = pulse(t, 0.0, 0.3, 0.15, 0.35)
        L.hips(body, p, dx=0.08 * bend, dz=-0.2 * bend, pitch=8 * bend, roll=-8 * bend)
        if t < 0.45:
            tgt = RW[1].lerp(grip_down, smooth(0.0, 0.3, t))
        else:
            tgt = grip_down.lerp(held_at, smooth(0.45, 0.9, t))
        body.hand_to(p, 1, tgt, elbow=(0.6, 0.4, -0.3), hand_rot=upright if t < 0.6 else
                     L.hand_world((0, -0.4, 1), (0, -1, 0)))
        L.fist(p, 1, 0.9 if t > 0.3 else 0.3)
        body.plant(p, 1, pos=(0.1 * bend, 0, 0))
        body.plant(p, -1)
        return p

    c.solve(check_solve)
    c.layer(lambda t: brows(Pose(), 1.6 * smooth(1.2, 1.5, t), 1.8 * smooth(1.2, 1.5, t), 0.8)
            + look((-6, 10)) + Pose(face={"oh": smooth(1.2, 1.5, t)}))
    out.append(c)
    return out


def brick_clips(body):
    """Brick's pieces: on the card beside Archie's left (BRICK_X), facing him; the stamp's shaft is ahead of
    him and low, at SHAFT in his frame."""
    L = body.lib
    RW = L.rest_wrists(body)
    SHAFT, SHOW = Vector((0.32, -1.05, 0.72)), Vector((0.32, -0.9, 1.75))
    T = 3.6
    c = Clip(f"{NAME}/turn", T)
    c.key(0.0, L.REST)
    flat = L.REST.copy()
    flat.face = {"flat": 1.0}
    c.key(0.5, flat)
    c.key(T, flat, "linear")

    def turn_solve(t, p, skel):
        bend = pulse(t, 0.1, 0.6, 0.15, 0.6)
        L.hips(body, p, dz=-0.3 * bend, pitch=26 * bend, dy=0.1 * bend)
        p.add("spine", 12 * bend, 0, 0)
        if t < TURN_TAKE:
            tgt = RW[1].lerp(SHAFT, smooth(0.1, TURN_TAKE, t))
        else:
            tgt = SHAFT.lerp(SHOW, smooth(TURN_TAKE, TURN_FACE, t))
        body.hand_to(p, 1, tgt, elbow=(0.5, 0.4, -0.5))
        L.fist(p, 1, smooth(TURN_TAKE - 0.15, TURN_TAKE, t))
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(turn_solve)
    c.layer(lambda t: L.brows(Pose(), 1.4 * smooth(2.2, 2.5, t), 0.8 * smooth(2.2, 2.5, t), 0.0, side=1)
            + look((-20 * (1 - smooth(1.4, 1.8, t)), 18 * smooth(2.2, 2.6, t))))
    return [c]
