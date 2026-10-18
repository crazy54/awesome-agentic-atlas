"""Heavy README: the README, a long slab of it, lies on the floor. Archie squats, takes one end and heaves:
nothing. He calls for Brick. Brick ambles over, looks at it, slides one finger under its middle and lifts it
over his head like a plate on a stick. Archie stretches, rolls his shoulders and dusts his hands as if he
had done the work. Brick looks at him.

FORMATION (metres, x across the page, y back, from the slab's middle on the floor, all facing the reader): the
slab (props/readme-slab.glb, 1.9 m long, its origin on the floor under its middle) lies SLAB_Y in front of
the pals; Archie stands ARCHIE_X from it, Brick BRICK_X. The page parents the slab to Brick's right index
tip (bone index_3_R, plus TIP_OFF along it, kept upright) at GRAB_AT seconds into `lift`, at which moment
his fingertip is under the slab's middle; from then on it rides the finger, and `lift` ends with it on his
fingertip at the everyday `finger-hold`'s ONE_FINGER.

    archie  heavy-readme/strain     squats, takes the slab's end and heaves; it doesn't move; staggers back
            heavy-readme/call       turns to the side Brick comes from and bellows for him, hands cupped
            heavy-readme/stretch    a big stretch, a roll of the shoulders, hands dusted, hands on hips
    brick   heavy-readme/lift       looks down at it, one finger under its middle, up over his head
            heavy-readme/look       holding it up, a look across at Archie, the right brow up (from
                                    finger-hold, and back to it)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "heavy-readme"
CAST = ("archie", "brick")
SLAB_Y = -0.4                   # the slab, in front of them
SLAB_LEN = 1.9
ARCHIE_X = -1.35                # Archie, left of the slab's middle (its left end is 0.95 left of the middle)
BRICK_X = 1.05                  # Brick, right of it
GRAB_AT = 1.55                  # seconds into heavy-readme/lift: his fingertip is under the slab's middle
TIP_OFF = 0.12                  # metres along index_3_R to his fingertip


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
    end = V(-SLAB_LEN / 2 - ARCHIE_X, SLAB_Y, 0.0)          # the slab's left end, from Archie

    # ---- strain ----------------------------------------------------------------------------------
    T = 4.4
    c = Clip(f"{NAME}/strain", T)
    c.key(0.0, REST)

    def strain_solve(t, p, skel):
        down = pulse(t, 0.2, 0.6, 2.4, 0.6)
        heave = pulse(t, 1.0, 0.3, 1.5, 0.3)
        shake = math.sin(t * 55) * 0.012 * heave
        hips(body, p, dz=-0.42 * down + 0.08 * heave + shake, dx=0.1 * down, dy=0.08 * down,
             pitch=22 * down - 10 * heave, roll=4 * heave * math.sin(t * 31))
        p.add("spine", 14 * down - 6 * heave, 0, 0)
        p.add("chest", 10 * down - 10 * heave, 0, 0)
        p.add("head", -6 * down - 16 * heave, 0, 0)
        for sg, dz in ((1, 0.08), (-1, 0.32)):
            grip = end + V(0.02 * sg, 0.0, dz) + V(0, 0, shake)
            body.hand_to(p, sg, RW[sg].lerp(grip, down), elbow=(0.5, 0.2, -0.3),
                         hand_rot=hand_world((0.6, -0.4, -0.4), (0, 0.2, 1) if sg > 0 else (0, 0, -1)) if down > 0.5 else None)
            fist(p, sg, down)
        stag = pulse(t, 3.0, 0.15, 0.3, 0.5)
        hips(body, p, dx=-0.08 * stag, roll=-6 * stag)
        body.plant(p, 1, pos=(0.12 * down, 0, 0), knee_out=0.1 * down)
        body.plant(p, -1, pos=(-0.1 * down - 0.12 * stag, 0.05 * stag, 0), knee_out=0.1 * down)
        return p

    c.solve(strain_solve)

    def strain_face(t):
        p = Pose()
        heave = pulse(t, 1.0, 0.25, 1.6, 0.3)
        p.face.update({"grin": -1.0 * heave, "grit": heave})
        p.both("lid_up", x=-34 * heave)
        p.both("lid_lo", x=24 * heave)
        abrows(p, -1.4 * heave, -0.8 * heave, 0.5 * heave)
        puff = pulse(t, 3.0, 0.1, 0.5, 0.4)
        p.face.update({"oh": 0.7 * puff})
        abrows(p, 1.0 * puff, 1.2 * puff, 0.6 * puff)
        return p + look((-20 * pulse(t, 0.1, 0.3, 0.8, 0.3), 10 * pulse(t, 0.1, 0.3, 0.8, 0.3)))

    c.layer(strain_face)
    out.append(c)

    # ---- call ------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/call", T)
    c.key(0.0, REST)
    shout = REST.copy()
    shout.set("head", -10, 30, 4)
    shout.set("chest", -6, 14, 0)
    shout.face = {"wide": 1.0}
    c.key(0.35, shout, "back")
    c.key(1.6, shout, "linear")
    c.key(T, REST, "inout")

    def call_solve(t, p, skel):
        k = pulse(t, 0.1, 0.3, 1.3, 0.4)
        for sg in (1, -1):
            mouth = V(0.06 * sg + 0.08, -0.42, 1.98)
            body.hand_to(p, sg, RW[sg].lerp(mouth, k), elbow=(0.6, 0.3, -0.4),
                         hand_rot=hand_world((-sg * 0.3, -0.5, 0.8), (-sg, 0, 0)) if k > 0.5 else None)
            open_hand(p, sg, 0)
        body.plant(p, 1, roll=-12 * pulse(t, 0.3, 0.1, 1.2, 0.2))
        body.plant(p, -1)
        return p

    c.solve(call_solve)
    c.layer(lambda t: look((6, 26 * pulse(t, 0.1, 0.3, 1.3, 0.4))))
    out.append(c)

    # ---- stretch: like he did the work --------------------------------------------------------------
    T = 4.6
    c = Clip(f"{NAME}/stretch", T)
    c.key(0.0, REST)
    up = REST.copy()
    up.both("upper_arm", x=10, y=0, z=118)
    up.both("forearm", x=10, y=0, z=0)
    up.set("chest", -12, 0, 0)
    up.set("head", -16, 0, 0)
    up.face = {"oh": 0.9}
    lean = up.copy()
    lean.set("spine", 0, 0, 12)
    lean.set("chest", -8, 0, 8)
    lean.face = {"oh": 0.4, "grin": 0.4}
    c.key(0.6, up, "inout")
    c.key(1.3, up, "linear")
    c.key(1.9, lean, "inout")
    c.key(2.3, REST, "inout")
    proud = REST.copy()
    proud.set("chest", -8, 0, 0)
    proud.set("head", -8, -8, 6)
    proud.face = {"grin": 1.0}
    c.key(3.6, proud, "inout")
    c.key(4.2, proud, "linear")
    c.key(T, REST, "inout")

    def stretch_solve(t, p, skel):
        # the dusting (2.3-3.0): hands brushed together in front; then hands on hips (3.2-4.3)
        d = pulse(t, 2.3, 0.15, 0.45, 0.15)
        if d > 0.01:
            rub = 0.05 * math.sin(t * 28)
            for sg in (1, -1):
                tgt = V(sg * (0.05 + rub * sg), -0.42, 1.25)
                body.hand_to(p, sg, RW[sg].lerp(tgt, d), elbow=(0.6, 0.3, -0.4),
                             hand_rot=hand_world((0, -0.6, 0.8), (-sg, 0, 0)) if d > 0.5 else None)
                open_hand(p, sg, 2)
        hk = pulse(t, 3.1, 0.35, 0.8, 0.35)
        if hk > 0.01:
            for sg in (1, -1):
                tgt = V(sg * 0.32, -0.02, 1.08)
                body.hand_to(p, sg, RW[sg].lerp(tgt, hk), elbow=(0.6, 0.3, 0.0),
                             hand_rot=hand_world((-sg * 0.6, -0.2, -1), (-sg, 0, 0)) if hk > 0.5 else None)
                fist(p, sg, 0.7 * hk)
        body.plant(p, 1, roll=20 * pulse(t, 0.4, 0.3, 0.6, 0.3))
        body.plant(p, -1, roll=20 * pulse(t, 0.4, 0.3, 0.6, 0.3))
        return p

    c.solve(stretch_solve)

    def stretch_face(t):
        p = Pose()
        y = pulse(t, 0.6, 0.3, 0.6, 0.4)
        p.both("lid_up", x=-40 * y)
        abrows(p, 0.8 * y, 1.2 * y, 0.8 * y)
        pr = pulse(t, 3.3, 0.3, 0.8, 0.3)
        abrows(p, 0.0, 1.2 * pr, 1.0 * pr, side=1)
        return p

    c.layer(stretch_face)
    c.layer(blink_layer([2.6]))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    rw = L.rest_wrists(body)
    under = V(-BRICK_X, SLAB_Y, 0.04)                        # the slab's bottom middle, from Brick
    top = V(*L.ONE_FINGER)
    down = L.hand_world((-0.05, -0.15, -1), (0.9, 0.3, 0.1))     # the finger pointing down at the floor
    up = L.hand_world((-0.15, -0.2, 1), (-0.9, 0.2, 0.2))         # = brick_base one_finger_at, right hand

    # ---- lift: one finger under the middle, up over his head ------------------------------------------
    T = 3.6
    c = Clip(f"{NAME}/lift", T)
    c.key(0.0, REST)

    def lift_solve(t, p, skel):
        bend = pulse(t, 0.35, GRAB_AT - 0.35, 0.25, 1.2)
        reach = smooth(0.35, GRAB_AT, t)
        rise = ease("inout", smooth(GRAB_AT + 0.2, T - 0.35, t))
        L.hips(body, p, dz=-0.5 * bend, dy=0.12 * bend, pitch=26 * bend, yaw=-10 * bend)
        p.add("spine", 14 * bend, 0, 0)
        p.add("chest", 10 * bend - 3 * rise, -8 * bend, 2 * rise)
        p.add("head", 12 * bend - 6 * rise, 0, 0)
        if rise <= 0:
            k = reach
            hr = down
            target = under
            wrist = target - hr.col[1] * 0.58
            body.hand_to(p, -1, rw[-1].lerp(wrist, k), elbow=(0.6, 0.6, -0.4), hand_rot=hr if k > 0.4 else None)
        else:
            # the hand turns finger-up as it rises; the tip carries the slab from the floor to overhead
            tgt = under.lerp(top, rise) + V(0, 0, 0.25 * math.sin(math.pi * rise))
            d = (down.col[1].lerp(up.col[1], ease("inout", min(1.0, rise * 1.6)))).normalized()
            palm = (down.col[2].lerp(up.col[2], ease("inout", min(1.0, rise * 1.6)))).normalized()
            hr = L.hand_world(d, palm)
            body.hand_to(p, -1, tgt - d * 0.58, elbow=(0.6, 0.6, -0.4), hand_rot=hr)
        if t > 0.5:
            L.point(p, -1)
        body.plant(p, 1, yaw=L.STANCE, knee_out=0.14 * bend)
        body.plant(p, -1, pos=(-0.1 * bend, -0.15 * bend, 0), yaw=L.STANCE, knee_out=0.14 * bend)
        return p

    c.solve(lift_solve)

    def lift_face(t):
        p = Pose()
        at = pulse(t, 0.1, 0.3, 1.6, 0.4)
        up_ = smooth(GRAB_AT + 0.3, T - 0.4, t)
        return p + look((-22 * at + 14 * up_, 18 * at - 6 * up_))

    c.layer(lift_face)
    c.layer(L.blinks([0.3]))
    out.append(c)

    # ---- look: holding it up, a look across at Archie, the right brow up --------------------------------
    T = 3.4
    c = Clip(f"{NAME}/look", T)
    c.key(0.0, REST)

    def look_solve(t, p, skel):
        d = pulse(t, 0.2, 0.5, 2.0, 0.5)
        p.add("chest", -3, -6 * d, 2)
        p.add("head", -6 + 6 * d, -18 * d, 0)
        L.one_finger_at(body, p, 1.0, rw, top)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(look_solve)

    def look_face(t):
        p = Pose()
        d = pulse(t, 0.2, 0.5, 2.0, 0.5)
        b = pulse(t, 0.9, 0.45, 1.2, 0.5)
        L.brows(p, 0.6 * b, 2.0 * b, 1.6 * b, side=-1)
        L.brows(p, -0.3 * b, -0.4 * b, -0.2 * b, side=1)
        p.face.update({"smile": -0.5 * b, "flat": 0.5 * b})
        L.lids(p, 0.25 * b)
        return p + look((10 * (1 - d) - 8 * d, -6 * (1 - d) - 22 * d))

    c.layer(look_face)
    out.append(c)
    return out
