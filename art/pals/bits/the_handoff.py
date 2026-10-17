"""The handoff: Brick, the responsible one, the one who guards the switches and confiscates the remotes --
caught quietly handing Zip the remote.

Brick stands with his arms folded, as he always does. Zip sneaks up beside him and holds out a hand. Brick
doesn't look at him. His eyes go left, right... and his right hand comes out from under his folded arms with
the remote in it, down at his side, and Zip takes it. Then Brick's eyes come round to the reader. He holds
them there. One enormous finger goes to his lips. Zip sneaks off with it; Brick folds his arms again as if
nothing happened -- and as Zip leaves, the lights flicker.

THE LAYOUT (metres on the floor, both facing the reader): Brick at the origin; Zip ZIP_AT to his right (the
page's left). The remote passes at Brick's right grip: HAND is where his right wrist goes for it, and
REACH where Zip's left wrist goes to take it, in Zip's own frame (so his grip meets Brick's there).

    brick: the-handoff/slip    (from guard-hold) eyes left, right; the right hand out from the fold, down to
                               HAND with the remote (the page shows it in his grip at SHOW), held; Zip takes
                               it (TAKE); the hand back into the fold
           the-handoff/caught  his eyes to the reader, held; brows up; a finger to his lips; back to the fold
    zip:   the-handoff/ask     (standing) looks up at Brick, holds out his left hand, palm up, waiting (loop)
           the-handoff/take    the hand to REACH, closes on the remote at TAKE, back to his chest, then the
                               remote behind his back; a grin at nobody; ends standing, hand behind his back
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "the-handoff"
CAST = ("brick", "zip")
ZIP_AT = 1.44                     # Zip's root, to Brick's right (the page's left), metres
HAND = (-1.12, -0.12, 1.12)       # Brick's right wrist, holding the remote out at his side
REACH = (0.44, -0.19, 0.79)       # Zip's left wrist, taking it (Zip's frame)
SHOW, TAKE = 0.55, 1.75           # slip: the remote appears in Brick's hand; Zip's hand closes on it
TAKE_ZIP = 1.0                    # take: the same moment, in Zip's piece
TAU = math.tau


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


def brick_clips(body):
    L = body.lib
    REST, hand_world, point = L.REST, L.hand_world, L.point
    rw = L.rest_wrists(body)
    out = []

    def stand(p):
        body.plant(p, 1, pos=(0.06, 0, 0), yaw=L.STANCE + 4)
        body.plant(p, -1, pos=(-0.06, 0, 0), yaw=L.STANCE + 4)

    def guarded(t):
        """The guard-hold face, as it is at t = 0 of that loop: this piece starts from there."""
        p = Pose()
        p.face.update({"smile": -0.5, "flat": 0.5})
        L.lids(p, 0.2)
        return p

    # ---- slip ---------------------------------------------------------------------------------------
    T = 3.4
    c = Clip(f"{NAME}/slip", T)
    c.key(0.0, REST)

    def slip(t, p, skel):
        L.folded(body, p, 1.0, rw)                       # both folded; then the right hand comes out
        out_ = ease("inout", smooth(0.35, 1.25, t)) * (1 - ease("inout", smooth(2.35, 3.2, t)))
        if out_ > 0.001:
            fold = L.FOLD[-1]
            tgt = fold.lerp(V(*HAND), out_)
            tgt.z += 0.06 * math.sin(math.pi * out_) * (1 - out_)          # round the elbow, not through it
            body.hand_to(p, -1, tgt, elbow=(1.0, 0.2, -0.6),
                         hand_rot=hand_world((-0.2, -0.5, -1), (0.9, 0, -0.2)) if out_ > 0.5 else None)
            p.fingers(-1, 50, spread=0, thumb=30)
        stand(p)
        return p

    c.solve(slip)

    def slip_face(t):
        p = guarded(t)
        # eyes only: to his left, to his right (towards Zip, without turning the head), then front, away
        a = pulse(t, 0.2, 0.2, 0.3, 0.2)
        b = pulse(t, 0.9, 0.2, 1.3, 0.3)
        p = p + look((-3 * b, 22 * a - 26 * b))
        return p

    c.layer(slip_face)
    out.append(c)

    # ---- caught -------------------------------------------------------------------------------------
    T = 3.6
    c = Clip(f"{NAME}/caught", T)
    c.key(0.0, REST)

    def caught(t, p, skel):
        L.folded(body, p, 1.0, rw)
        # the finger to his lips: his left hand out of the fold
        k = pulse(t, 1.3, 0.45, 1.0, 0.5)
        if k > 0.001:
            lips = body.where(REST, "head") + V(0.0, -0.33, 0.12)
            body.hand_to(p, 1, L.FOLD[1].lerp(lips + V(0.02, -0.12, -0.42), k), elbow=(0.9, 0.0, -0.8),
                         hand_rot=hand_world((-0.1, 0.1, 1), (0, 1, 0)) if k > 0.5 else None)
            if k > 0.3:
                point(p, 1)
        stand(p)
        return p

    c.solve(caught)

    def caught_face(t):
        p = guarded(t)
        on = smooth(0.0, 0.08, t)                        # the eyes snap to the reader, and stay
        p = p + look((0, 0))
        L.brows(p, 1.0 * on * (1 - smooth(2.6, 3.2, t)), 1.6 * on * (1 - smooth(2.6, 3.2, t)), 0.8 * on, side=1)
        L.lids(p, 0.2 * (1 - on) - 0.1 * on)
        return p

    c.layer(caught_face)
    out.append(c)
    return out


def zip_clips(body):
    L = body.lib
    REST, hand_world, open_hand, fist = L.REST, L.hand_world, L.open_hand, L.fist
    rw = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    out = []

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    UP = (14, 30)                                        # eyes up and to his left: Brick's face

    # ---- ask ----------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/ask", T, loop=True)
    hopeful = REST.copy()
    hopeful.face = {"grin": 0.8, "wide": 0.2}
    c.key(0.0, hopeful)
    c.key(T, hopeful, "linear")
    ASK = V(0.34, -0.3, 0.86)

    def ask(t, p, skel):
        bob = math.sin(TAU * t / T)
        p.add("head", -10, 14, 0)
        body.hand_to(p, 1, ASK + V(0, 0, 0.01 * bob), elbow=(0.4, 0.3, -0.6),
                     hand_rot=hand_world((0.2, -1, 0.1), (0, 0, 1)))
        open_hand(p, 1, 8)
        L.hips(body, p, dz=0.008 * bob)
        stand(p)
        return p

    c.solve(ask)
    c.layer(lambda t: look(UP))
    out.append(c)

    # ---- take ---------------------------------------------------------------------------------------
    T = 3.2
    c = Clip(f"{NAME}/take", T)
    c.key(0.0, hopeful)
    glee = REST.copy()
    glee.face = {"grin": 1.0, "wide": 0.5}
    c.key(TAKE_ZIP + 0.2, glee)
    c.key(T, glee, "linear")
    CHEST, BEHIND = V(0.16, -0.32, 1.0), V(0.18, 0.28, 0.82)

    def take(t, p, skel):
        p.add("head", -10 * (1 - smooth(1.4, 2.0, t)), 14 * (1 - smooth(1.4, 2.0, t)), 0)
        go = ease("inout", smooth(0.1, TAKE_ZIP, t))
        back = ease("inout", smooth(TAKE_ZIP + 0.15, 1.8, t))
        hide = ease("inout", smooth(1.9, 2.7, t))
        tgt = ASK.lerp(V(*REACH), go).lerp(CHEST, back).lerp(BEHIND, hide)
        body.hand_to(p, 1, tgt, elbow=(0.4, 0.3 - 0.6 * hide, -0.6),
                     hand_rot=hand_world((0.1, -0.6 + 1.2 * hide, 0.8), (0, 0, 1)) if hide < 0.5 else None)
        if t < TAKE_ZIP:
            open_hand(p, 1, 8)
        else:
            fist(p, 1, 0.75)
        # a little shoulder hunch of glee
        g = pulse(t, TAKE_ZIP + 0.1, 0.15, 0.4, 0.3)
        p.both("shoulder", z=8 * g, add=True)
        stand(p)
        return p

    c.solve(take)

    def take_face(t):
        p = Pose()
        u = 1 - smooth(1.4, 1.9, t)
        p = p + look((UP[0] * u, UP[1] * u))
        L.squint(p, 0.4 * smooth(1.9, 2.3, t))
        return p

    c.layer(take_face)
    out.append(c)
    return out
