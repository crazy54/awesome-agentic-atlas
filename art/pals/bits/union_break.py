"""The union break: an app card is stuck fast in the floor, at a tilt. Archie, behind it, heaves at it: nothing.
He wipes his brow and whistles for help. Zip strolls in with a picket sign, Brick lugs in two folding chairs.
Zip plants the sign -- YOUR POOR PLANNING IS NOT OUR EMERGENCY -- Brick unfolds the chairs, and they sit down
beside it, arms folded. Archie stares. He gives up and slumps over the card.

FORMATION (metres from Archie's root, x to his left = screen right, y back, z up; everyone faces the reader
unless walking): the card (the `app-card` prop at CARD_S times, its middle at (0, CARD_Y, CARD_Z), tipped TILT
degrees to screen right, the floor hiding its bottom) stands in front of Archie, his hands on its top edge at
EDGE[side]. The others come in from screen right: Zip plants the sign (the `picket-sign` at SIGN_S, gripped
STICK_GRIP up its stick) at his own SIGN_AT standing at ZIP_PLANT_X; Brick sets the chairs (`folding-chair`,
Zip's at 1, his at CHAIR_S[brick]) down at his sides, each held by the middle of its back at CHAIR_TOP (times
its scale, from the chair's origin), from BRICK_SET_X. Seated, each pal's root is SEAT_FROM[pal] in front of
his chair's origin (the page moves him there, in depth, as he walks over), his hips at SEAT[pal]; the page
turns chairs and sitters a little towards Archie, so the chairs show.

    union-break/heave        archie  REST -> REST: hands on the card's edge (HANDS_ON), two heaves (PULLS: the
                                     page shudders the card), and his hands slip off it (LET_GO)
    union-break/wipe         archie  REST -> REST: the back of his wrist across his brow, a puff
    union-break/whistle      archie  REST -> REST: two fingers in his mouth, a whistle, a look off to his left
    union-break/stare        archie  REST -> REST: across at the two of them, sitting there; a slow blink
    union-break/slump        archie  REST -> SLUMP: forearms on the card's edge, chin down: he gives up
    union-break/slump-hold   archie  SLUMP, looping: a sigh
    union-break/carry-sign   zip     the walk, looping, the sign's stick in his right hand at SIGN_HOLD
    union-break/plant-sign   zip     carry-sign -> REST: up, and down into the floor at PLANT_AT (the page leaves
                                     it standing there), a pat, his hand back
    union-break/sit-down     zip     REST -> SEATED: down onto the chair, arms folding
    union-break/seated       zip     SEATED, looping: arms folded, chin up, a foot tapping
    union-break/lug          brick   the walk, looping (two strides), a folded chair hanging from each hand at
                                     LUG[side]
    union-break/set-chairs   brick   lug -> REST: both chairs down onto their feet (SET_AT: the page leaves them
                                     there and unfolds them), his hands back
    union-break/sit-down     brick   REST -> SEATED: down onto his chair, arms folding
    union-break/seated       brick   SEATED, looping: arms folded, deadpan, a slow blink
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth
from bits import _moves as M

NAME = "union-break"
CAST = ("archie", "zip", "brick")
TAU = math.tau

CARD_S = 1.5                               # the app card: 1.2 x 0.8 m as built
CARD_Y, CARD_Z = -0.45, 0.35               # its middle: in front of him, low (the floor hides a quarter of it)
TILT = 9.0                                 # tipped, top to screen right
HANDS_ON, PULLS, LET_GO = 0.45, ((0.9, 1.7), (2.0, 2.9)), 2.9

SIGN_S = 1.3                               # the picket sign: 1.55 m tall as built
STICK_GRIP = 0.7 * SIGN_S                  # his grip, that far up the stick
SIGN_HOLD = Vector((-0.42, 0.12, 0.98))    # carrying it, at his side and a little behind him: his right grip
SIGN_AT = Vector((-0.45, 0.12, 0.0))       # planted: the stick's foot, in his frame (the board behind him)
PLANT_AT = 0.75
ZIP_PLANT_X, ZIP_CHAIR_X = 2.2, 2.75

CHAIR_S = {"zip": 1.0, "brick": 1.4}
CHAIR_TOP = Vector((0.0, 0.18, 0.89))      # the middle of a chair's back, from its origin, at scale 1
LUG = {1: Vector((0.9, 0.0, 1.45)), -1: Vector((-0.9, 0.0, 1.45))}   # Brick's grips, lugging: his left his own
SET_AT = 1.1
BRICK_SET_X = 3.65                         # Zip's chair lands at BRICK_SET_X - 0.9, his own at + 0.9
SEAT_FROM = {"zip": 0.27, "brick": 0.5}    # seated: his root, this far in front of the chair's origin
SEAT = {"zip": Vector((0, 0.25, 0.58)), "brick": Vector((0, 0.45, 0.83))}   # ... and his hips, from his root


def V(*a):
    return Vector(a)


def edge(side):
    """Archie's grip on the card's top edge: a third of a metre either side of its middle."""
    a = math.radians(TILT)
    top = V(0, CARD_Y, CARD_Z) + 0.4 * CARD_S * V(math.sin(a), 0, math.cos(a))
    return top + side * 0.32 * V(math.cos(a), 0, -math.sin(a)) + V(0, 0, 0.025)


def grip_to(body, p, side, target, elbow, hand_rot):
    """Put the hand's grip bone (not the wrist) on `target`: aim the wrist, see where the grip landed, and aim
    again by the miss."""
    s = "_L" if side > 0 else "_R"
    target = Vector(target)
    aim = target.copy()
    for _ in range(3):
        body.hand_to(p, side, aim, elbow=elbow, hand_rot=hand_rot)
        g = body.skel.fk(p, f"grip{s}")[f"grip{s}"].translation
        aim = aim + (target - g)
    return p


def rest_grip(body, side):
    q = body.lib.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    s = "_L" if side > 0 else "_R"
    return body.skel.fk(q, f"grip{s}")[f"grip{s}"].translation.copy()


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    return out


# --------------------------------------------------------------------------------------------- Archie
def archie_clips(body):
    L = body.lib
    REST, hips, hand_world, open_hand = L.REST, L.hips, L.hand_world, L.open_hand
    n = lambda piece: f"{NAME}/{piece}"
    rw = M.rest_wrists(body)
    g0 = {sg: rest_grip(body, sg) for sg in (1, -1)}
    over = {sg: hand_world((0, -0.75, -0.65), (-sg * 0.15, 0.2, -1)) for sg in (1, -1)}   # fingers over the edge
    out = []

    def stand(p, **kw):
        body.plant(p, 1, **kw)
        body.plant(p, -1, **kw)

    # ---- heave ------------------------------------------------------------------------------------------
    T = 3.6
    c = Clip(n("heave"), T)
    c.key(0.0, REST)
    grit = REST.copy()
    grit.set("head", 12, 0, 0)
    grit.face = {"grit": 1.0, "grin": -0.6}
    puff = REST.copy()
    puff.set("head", 4, 0, 0)
    puff.face = {"oh": 0.7}
    c.key(0.6, grit, "inout")
    c.key(PULLS[0][1], grit, "linear")
    c.key(PULLS[0][1] + 0.15, puff, "inout")
    c.key(PULLS[1][0], grit, "inout")
    c.key(LET_GO, grit, "linear")
    c.key(LET_GO + 0.12, puff, "snap")
    c.key(T, REST, "inout")

    def heave_solve(t, p, skel, T=T):
        a, b = PULLS
        pull = max(pulse(t, a[0], 0.25, a[1] - a[0] - 0.55, 0.3), 1.25 * pulse(t, b[0], 0.25, b[1] - b[0] - 0.3, 0.05))
        crouch = pulse(t, 0.3, 0.4, LET_GO - 0.7, 0.4)
        stagger = pulse(t, LET_GO, 0.12, 0.05, 0.5)
        shake = math.sin(TAU * 9 * t) * pull
        hips(body, p, dy=0.15 * pull + 0.08 * stagger, dz=-0.07 * crouch - 0.1 * pull, pitch=-13 * pull - 10 * stagger)
        p.add("spine", -9 * pull - 4 * stagger, 0, 0)
        p.add("chest", -5 * pull, 0, 2.5 * shake)
        k = smooth(0.05, HANDS_ON, t)
        fling = smooth(LET_GO, LET_GO + 0.12, t)        # his hands flung up as they slip off, and back down
        back = smooth(LET_GO + 0.25, T - 0.05, t)
        for sg in (1, -1):
            at = g0[sg].lerp(edge(sg), k).lerp(V(sg * 0.45, -0.4, 1.25), fling).lerp(g0[sg], back)
            if back < 0.999 and k > 0.01:
                grip_to(body, p, sg, at, (0.6, 0.4, -0.4), over[sg] if k > 0.4 and fling < 0.5 else None)
            hold = k * (1 - fling)
            p.fingers(sg, 22 + 48 * hold, spread=2 + 10 * fling * (1 - back), thumb=14 + 16 * hold)
        stand(p)
        return p

    c.solve(heave_solve)

    def heave_face(t, T=T):
        p = Pose()
        a, b = PULLS
        e = max(pulse(t, a[0], 0.25, a[1] - a[0] - 0.55, 0.3), pulse(t, b[0], 0.25, b[1] - b[0] - 0.3, 0.05))
        p.both("lid_up", x=-28 * e)
        p.both("lid_lo", x=20 * e)
        brows(p, -1.2 * e, -0.4 * e, 0.4 * e)
        w = pulse(t, LET_GO, 0.08, 0.3, 0.3)
        return p + look((-20 * (1 - w) * smooth(0.0, 0.5, t), 0)) + look((10 * w, 0))

    c.layer(heave_face)
    out.append(c)

    # ---- wipe --------------------------------------------------------------------------------------------
    T = 1.6
    c = Clip(n("wipe"), T)
    c.key(0.0, REST)
    phew = REST.copy()
    phew.set("head", -6, 0, 4)
    phew.face = {"oh": 0.5, "flat": 0.4}
    c.key(0.4, phew, "inout")
    c.key(T - 0.4, phew, "linear")
    c.key(T, REST, "inout")

    def wipe_solve(t, p, skel, T=T):
        k = pulse(t, 0.05, 0.35, 0.7, 0.45)
        u = smooth(0.4, 1.0, t)
        brow = V(-0.32, -0.4, 2.12).lerp(V(0.2, -0.4, 2.16), u)       # across his brow, right to left
        body.hand_to(p, -1, rw[-1].lerp(brow, k), elbow=(0.7, 0.1, -0.2),
                     hand_rot=hand_world((1, 0, 0.3), (0, -0.4, -1)) if k > 0.5 else None)
        open_hand(p, -1, 4)
        stand(p)
        return p

    c.solve(wipe_solve)
    c.layer(lambda t: Pose().both("lid_up", x=-24 * pulse(t, 0.4, 0.2, 0.6, 0.3)))
    out.append(c)

    out.append(M.whistle(body, n("whistle"), side=-1))

    # ---- stare: at the two of them, sitting there --------------------------------------------------------
    T = 2.4
    c = Clip(n("stare"), T)
    c.key(0.0, REST)
    at_them = REST.copy()
    at_them.set("head", 4, 30, 2)
    at_them.set("chest", 0, 8, 0)
    at_them.face = {"flat": 1.0, "grin": -0.5}
    c.key(0.45, at_them, "inout")
    c.key(T - 0.4, at_them, "linear")
    c.key(T, REST, "inout")
    c.solve(lambda t, p, skel: (stand(p), p)[-1])

    def stare_face(t, T=T):
        p = Pose()
        b = pulse(t, 1.1, 0.3, 0.25, 0.35)              # the slow blink
        p.both("lid_up", x=-46 * b - 12 * (1 - b) * pulse(t, 0.4, 0.3, T - 1.0, 0.3))
        return p + look((-2, 26 * pulse(t, 0.25, 0.3, T - 0.9, 0.3)))

    c.layer(stare_face)
    out.append(c)

    # ---- slump: he gives up, over the card ---------------------------------------------------------------
    def slumped(p, k):
        hips(body, p, dy=0.04 * k, dz=-0.06 * k, pitch=8 * k)
        p.add("spine", 10 * k, 0, 0)
        p.add("chest", 6 * k, 0, 0)
        for sg in (1, -1):
            w = edge(sg) + V(-sg * 0.1, 0.02, 0.07)    # the wrists on the edge, the forearms along it
            body.hand_to(p, sg, rw[sg].lerp(w, k), elbow=(0.9, 0.1, -0.1),
                         hand_rot=hand_world((-sg, -0.4, -0.1), (0, 0, -1)) if k > 0.5 else None)
            open_hand(p, sg, 4)
        stand(p)

    T = 1.6
    c = Clip(n("slump"), T)
    c.key(0.0, REST)
    glum = REST.copy()
    glum.set("head", 18, 0, -6)
    glum.face = {"flat": 1.0, "frown": 0.6}
    c.key(T, glum, "inout")
    c.solve(lambda t, p, skel, T=T: (slumped(p, ease("inout", smooth(0.1, T - 0.2, t))), p)[-1])
    c.layer(lambda t, T=T: Pose().both("lid_up", x=-20 * smooth(0.6, T, t)))
    out.append(c)

    T = 3.0
    c = M.loop_clip(n("slump-hold"), T)
    c.key(0.0, glum)

    def slump_hold(t, p, skel, T=T):
        sigh = 0.5 - 0.5 * math.cos(TAU * t / T)
        p.add("chest", -3 * sigh, 0, 0)
        p.add("head", -3 * sigh, 0, 0)
        slumped(p, 1.0)
        return p

    c.solve(slump_hold)
    c.layer(lambda t, T=T: Pose(face={"oh": 0.4 * pulse(t, 0.8, 0.4, 0.4, 0.6)}).both("lid_up", x=-20))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------------ Zip
def zip_clips(body):
    L = body.lib
    REST, hand_world, hips, fist = L.REST, L.hand_world, L.hips, L.fist
    n = lambda piece: f"{NAME}/{piece}"
    rw = L.rest_wrists(body)
    stick = hand_world((0.1, -0.9, -0.4), (1, 0, 0))      # round the stick, palm in
    walk = L.walk(body)
    out = []

    def bob_of(t):                                      # the walk's hips, up and down (zip_base.walk)
        return -0.025 + 0.028 * math.cos(TAU * 2 * (t / L.WALK_PERIOD - 0.1))

    # ---- carry-sign: the walk, the stick in his right hand ----------------------------------------------
    T = L.WALK_PERIOD
    c = M.loop_clip(n("carry-sign"), T)
    c.key(0.0, REST)

    def carry_solve(t, p, skel, T=T):
        p = walk.at(t % T, skel)
        grip_to(body, p, -1, SIGN_HOLD + V(0, 0, bob_of(t)), (0.5, 0.3, -0.6), stick)
        fist(p, -1, 0.8)
        return p

    c.solve(carry_solve)
    out.append(c)

    # ---- plant-sign --------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(n("plant-sign"), T)
    c.key(0.0, REST)
    proud = REST.copy()
    proud.set("head", -6, -10, 4)
    proud.face = {"grin": 1.0, "smirk_R": 0.5}
    c.key(0.5, proud, "inout")
    c.key(T, REST, "inout")
    up = SIGN_HOLD + V(-0.03, 0, 0.14)
    planted = SIGN_AT + V(0, 0, STICK_GRIP)

    def plant_solve(t, p, skel, T=T):
        thump = pulse(t, PLANT_AT, 0.05, 0.05, 0.3)
        hips(body, p, dz=0.04 * pulse(t, 0.1, 0.35, 0.0, 0.3) - 0.06 * thump)
        if t < 0.45:
            at = SIGN_HOLD.lerp(up, ease("inout", smooth(0.0, 0.45, t)))
        elif t < PLANT_AT:
            at = up.lerp(planted, ease("in", smooth(0.45, PLANT_AT, t)))
        else:
            at = planted
        let = smooth(1.0, 1.6, t)
        if let < 0.999:
            g = grip_to(body, p.copy(), -1, at, (0.5, 0.3, -0.6), stick)
            if let > 0.0:
                body.hand_to(p, -1, L.wrist_of(body, g, -1).lerp(rw[-1], let), elbow=(0.5, 0.3, -0.6))
            else:
                p = g
        fist(p, -1, 0.8 * (1 - let))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(plant_solve)
    out.append(c)

    # ---- sit-down, seated --------------------------------------------------------------------------------
    fold = {1: V(-0.13, -0.27, 1.07), -1: V(0.14, -0.24, 1.02)}     # zip_base.fold_arms
    fold_rot = {1: hand_world((-1, 0.1, 0.1), (0, -0.2, -1)), -1: hand_world((1, 0.1, -0.1), (0, -0.3, 1))}
    seat = SEAT["zip"]

    def sat(p, k, f, tap=0.0):
        d = V(0, seat.y, seat.z - body.hip_z) * k
        hips(body, p, d.x, d.y, d.z, pitch=-6 * k)
        p.add("spine", 8 * k, 0, 0)
        p.add("chest", -4 * k, 0, 0)
        for sg in (1, -1):
            body.hand_to(p, sg, rw[sg].lerp(fold[sg] + d, f), elbow=(0.55, 0.15, -0.35),
                         hand_rot=fold_rot[sg] if f > 0.5 else None)
            fist(p, sg, 0.6 * f)
        body.plant(p, 1, pos=(0, -0.12 * k, 0))
        body.plant(p, -1, pos=(0, -0.12 * k, 0), roll=-16 * tap)

    T = 1.2
    c = Clip(n("sit-down"), T)
    c.key(0.0, REST)
    smug = REST.copy()
    smug.set("head", -8, 0, 6)
    smug.face = {"flat": 0.5, "smirk_R": 0.7}
    c.key(T, smug, "inout")

    def sit_solve(t, p, skel, T=T):
        k = 1.04 * ease("in", smooth(0.1, 0.6, t)) if t < 0.6 else 1.0 + 0.04 * (1 - smooth(0.6, 0.85, t))
        sat(p, k, ease("inout", smooth(0.45, T, t)))
        return p

    c.solve(sit_solve)
    out.append(c)

    T = 2.0
    c = M.loop_clip(n("seated"), T)
    c.key(0.0, smug)

    def seated_solve(t, p, skel, T=T):
        sat(p, 1.0, 1.0, tap=max(0.0, math.sin(TAU * 2 * t / T)) ** 2)
        return p

    c.solve(seated_solve)
    c.layer(lambda t, T=T: Pose().both("lid_up", x=0.3 * L.LID_UP) + L.horn_sway(t, T, 2.0))
    out.append(c)
    return out


# ---------------------------------------------------------------------------------------------- Brick
def brick_clips(body):
    L = body.lib
    REST, hand_world, hips, fist = L.REST, L.hand_world, L.hips, L.fist
    n = lambda piece: f"{NAME}/{piece}"
    rw = L.rest_wrists(body)
    rail = {sg: hand_world((-sg * 0.15, -1, -0.2), (0, 0, -1)) for sg in (1, -1)}   # round a chair's back rail
    walk = L.walk(body)
    out = []

    def bob_of(t):                                      # the walk's hips (brick_base.walk)
        return -0.045 + 0.028 * math.cos(TAU * 2 * (t / L.WALK_PERIOD - 0.1))

    # ---- lug: the walk, a chair in each hand -------------------------------------------------------------
    T = 2 * L.WALK_PERIOD
    c = M.loop_clip(n("lug"), T)
    c.key(0.0, REST)

    def lug_solve(t, p, skel, T=T):
        p = walk.at(t % L.WALK_PERIOD, skel)
        for sg in (1, -1):
            grip_to(body, p, sg, LUG[sg] + V(0, 0, bob_of(t)), (0.9, 0.2, -0.4), rail[sg])
            fist(p, sg, 0.7)
        return p

    c.solve(lug_solve)
    out.append(c)

    # ---- set-chairs: both down onto their feet -----------------------------------------------------------
    T = 2.4
    c = Clip(n("set-chairs"), T)
    c.key(0.0, REST)
    eyes_down = REST.copy()
    eyes_down.set("head", 14, 0, 0)
    c.key(1.0, eyes_down, "inout")
    c.key(T, REST, "inout")
    down = {1: LUG[1] + V(0, 0, CHAIR_S["brick"] * CHAIR_TOP.z - LUG[1].z),
            -1: LUG[-1] + V(0, 0, CHAIR_S["zip"] * CHAIR_TOP.z - LUG[-1].z)}

    def set_solve(t, p, skel, T=T):
        sink = pulse(t, 0.1, 0.9, 0.2, 0.9)
        hips(body, p, dz=-0.12 * sink, dy=0.04 * sink, pitch=8 * sink)
        p.add("spine", 6 * sink, 0, 0)
        k = ease("inout", smooth(0.0, SET_AT, t))
        let = smooth(SET_AT + 0.1, T - 0.2, t)
        for sg in (1, -1):
            at = LUG[sg].lerp(down[sg], k)
            if let < 0.999:
                g = grip_to(body, p.copy(), sg, at, (0.9, 0.2, -0.4), rail[sg])
                if let > 0.0:
                    body.hand_to(p, sg, L.wrist_of(body, g, sg).lerp(rw[sg], ease("inout", let)), elbow=(0.9, 0.2, -0.4))
                else:
                    p = g
            fist(p, sg, 0.7 * (1 - let))
        body.plant(p, 1, yaw=L.STANCE, knee_out=0.08 * sink)
        body.plant(p, -1, yaw=L.STANCE, knee_out=0.08 * sink)
        return p

    c.solve(set_solve)
    out.append(c)

    # ---- sit-down, seated --------------------------------------------------------------------------------
    seat = SEAT["brick"]

    def sat(p, k, f):
        d = V(0, seat.y, seat.z - body.hip_z) * k
        hips(body, p, d.x, d.y, d.z, pitch=-4 * k)
        p.add("spine", 6 * k, 0, 0)
        p.add("chest", -4 * f, 0, 0)
        p.add("head", -4 * f, 0, 0)
        for sg in (1, -1):
            tgt = rw[sg].lerp(L.FOLD[sg] + d, f)
            body.hand_to(p, sg, tgt, elbow=(1.0, -0.2, -0.3),
                         hand_rot=hand_world((-sg * 1, -0.1, 0.1), (0, 0.3 * sg, -1)) if f > 0.5 else None)
            p.fingers(sg, 22 + 40 * f, spread=0, thumb=14 + 20 * f)
        body.plant(p, 1, pos=(0, -0.2 * k, 0), yaw=L.STANCE)
        body.plant(p, -1, pos=(0, -0.2 * k, 0), yaw=L.STANCE)

    T = 1.8
    c = Clip(n("sit-down"), T)
    c.key(0.0, REST)
    dead = REST.copy()
    dead.face = {"smile": -0.4, "flat": 0.7}
    c.key(T, dead, "inout")

    def sit_solve(t, p, skel, T=T):
        k = ease("inout", smooth(0.1, 1.1, t))
        k += 0.03 * pulse(t, 1.0, 0.1, 0.0, 0.4)        # the chair takes his weight
        sat(p, k, ease("inout", smooth(0.8, T, t)))
        return p

    c.solve(sit_solve)
    c.layer(lambda t, T=T: _lids(L, 0.25 * smooth(0.8, T, t)))
    out.append(c)

    T = 3.0
    c = M.loop_clip(n("seated"), T)
    c.key(0.0, dead)

    def seated_solve(t, p, skel, T=T):
        breath = 0.5 - 0.5 * math.cos(TAU * t / T)
        p.add("chest", -1.5 * breath, 0, 0)
        sat(p, 1.0, 1.0)
        return p

    c.solve(seated_solve)
    c.layer(lambda t: _lids(L, 0.25 + 0.75 * L.blink_at(t, [1.4])))
    out.append(c)
    return out


def _lids(L, k):
    p = Pose()
    L.lids(p, k)
    return p
