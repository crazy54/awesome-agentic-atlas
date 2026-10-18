"""The light-switch stakeout: Archie has been flicking the theme, slapping the switch on the hop. Brick, who
has been standing a little way off with his arms folded, watching, walks over and lays one enormous finger
on it. Archie tries to get at it round the finger -- under it, beside it, on the hop -- and can't. Brick looks
down at him and raises an eyebrow.

FORMATION (metres, x across the page, z up, from the switch's centre, both facing the reader): the switch is
SWITCH_Z above their floor (the page sizes the cast to make it so). Archie stands to its right, SLAP from
him as he slaps it with his right hand, and hops back STEP when the finger arrives; Brick stands to its
left, COVER from him, his left index tip on it, his arm raised over his head.

    archie  light-switch-stakeout/slap        a crouch, a hop, a slap at the switch high on his right; lands.
                                              His hand is on it SLAP_AT seconds in (the page flips the theme)
            light-switch-stakeout/startle     a jump back from the huge finger (the page slides him STEP right)
            light-switch-stakeout/reach-round under the finger, beside it, on the hop: he can't get at it
            light-switch-stakeout/give-up     arms drop, a slump, a sheepish look at the reader
    brick   light-switch-stakeout/cover       one finger, raised and laid on the switch; ends holding it
            light-switch-stakeout/cover-hold  holding it, calm (loops)
            light-switch-stakeout/brow        holding it, he looks down at Archie and the right brow goes up
            light-switch-stakeout/brow-reader the same, at the reader
            light-switch-stakeout/uncover     the finger off, back to rest
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "light-switch-stakeout"
CAST = ("archie", "brick")
SWITCH_Z = 2.9                  # the switch above the floor, metres
SLAP = (-0.55, -0.15)           # Archie: the switch from his root (x to his left) as he slaps it
SLAP_AT = 0.5                   # seconds into `slap`: his hand on it (the page flips the theme)
STEP = 0.35                     # how far Archie hops back to his left (the page's right) at the startle
COVER = (1.3, -0.45)            # Brick: the switch from his root, to his left; his left index tip on it


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
    REST, hips, point, open_hand, hand_world = L.REST, L.hips, L.point, L.open_hand, L.hand_world
    out = []

    def rest_wrist(sg):
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        return L.wrist_of(body, q, sg)

    RW = {1: rest_wrist(1), -1: rest_wrist(-1)}
    SW = V(SLAP[0], SLAP[1], SWITCH_Z)

    # ---- slap: crouch, a big hop, slap it high on his right, land ----------------------------------
    T = 1.3
    c = Clip(f"{NAME}/slap", T)
    c.key(0.0, REST)

    def slap_solve(t, p, skel):
        crouch = pulse(t, 0.0, 0.2, 0.04, 0.14)
        land = pulse(t, 0.66, 0.06, 0.05, 0.3)
        air = pulse(t, 0.26, 0.2, 0.08, 0.2)
        hips(body, p, dz=-0.13 * crouch - 0.08 * land + 0.42 * air, pitch=8 * crouch + 5 * land - 4 * air)
        p.add("chest", -6 * air, 0, 4 * air)
        p.add("head", -18 * air, -8 * air, 0)
        reach = pulse(t, 0.22, 0.26, 0.12, 0.45)
        wrist = SW + V(0.05, 0.12, -0.22)
        body.hand_to(p, -1, RW[-1].lerp(wrist, reach), elbow=(0.5, 0.3, -0.4),
                     hand_rot=hand_world((-0.15, -0.1, 1), (0, -1, 0)) if reach > 0.5 else None)
        open_hand(p, -1, 10 * reach)
        p.side("upper_arm", 1, x=-10 * air, z=25 * air, add=True)
        open_hand(p, 1, 8 * air)
        push = pulse(t, 0.18, 0.08, 0.04, 0.08)
        for sg in (1, -1):
            body.plant(p, sg, lift=0.42 * air, roll=26 * push + 6 * air)
        return p

    c.solve(slap_solve)

    def slap_face(t):
        p = Pose()
        g = pulse(t, 0.35, 0.1, 0.4, 0.3)
        p.face.update({"grin": 0.4 * g, "ee": 0.6 * g})
        abrows(p, 1.0 * g, 1.4 * g, 1.0 * g)
        return p + look((26 * pulse(t, 0.12, 0.2, 0.45, 0.3), -12 * pulse(t, 0.12, 0.2, 0.45, 0.3)))

    c.layer(slap_face)
    out.append(c)

    # ---- startle: the huge finger arrives on the switch; he jumps back (the page slides him) -------------
    T = 1.2
    c = Clip(f"{NAME}/startle", T)
    c.key(0.0, REST)

    def startle_solve(t, p, skel):
        j = pulse(t, 0.0, 0.12, 0.3, 0.5)
        air = pulse(t, 0.05, 0.12, 0.08, 0.2)
        hips(body, p, dz=0.08 * air - 0.04 * j, dx=0.04 * j, roll=-6 * j, pitch=-8 * j)
        p.add("chest", -12 * j, 10 * j, 0)
        p.add("head", -14 * j, 14 * j, 0)
        for sg in (1, -1):
            p.side("upper_arm", sg, x=35 * j, z=25 * j, add=True)
            p.side("forearm", sg, x=40 * j, add=True)
            open_hand(p, sg, 14 * j)
        body.plant(p, 1, lift=0.1 * air)
        body.plant(p, -1, lift=0.1 * air)
        return p

    c.solve(startle_solve)

    def startle_face(t):
        p = Pose()
        j = pulse(t, 0.0, 0.08, 0.4, 0.5)
        p.face.update({"grin": -1.0 * j, "wide": 0.6 * j, "oh": 0.4 * j})
        abrows(p, 2.0 * j, 2.2 * j, 1.6 * j)
        return p + look((20 * j, -16 * j))

    c.layer(startle_face)
    out.append(c)

    # ---- reach-round: round the finger -- under it, beside it, a hop over it ----------------------------
    T = 4.4
    c = Clip(f"{NAME}/reach-round", T)
    c.key(0.0, REST)
    sw = V(SLAP[0] - STEP, SLAP[1], SWITCH_Z)
    tries = [(0.5, sw + V(0.08, -0.15, -0.42)),           # under the finger
             (1.6, sw + V(0.02, -0.3, -0.12)),            # in front of it
             (2.7, sw + V(0.0, -0.1, 0.12))]              # over the top, on the hop

    def reach_solve(t, p, skel):
        k = pulse(t, 0.15, 0.35, 3.4, 0.5)
        tgt = tries[0][1]
        for (a, pa), (b, pb) in zip(tries, tries[1:]):
            if t > a:
                tgt = pa.lerp(pb, ease("inout", min(1.0, max(0.0, (t - a) / (b - a - 0.3)))))
        lean = k * (0.7 + 0.3 * smooth(2.4, 2.9, t))
        air = pulse(t, 2.75, 0.18, 0.12, 0.25)
        toes = pulse(t, 1.4, 0.3, 1.2, 0.3)
        hips(body, p, dx=-0.1 * lean, dz=0.05 * toes + 0.36 * air - 0.04 * (1 - toes) * k, roll=10 * lean)
        p.add("spine", 0, 0, 8 * lean)
        p.add("chest", -4 * toes, -6 * lean, 10 * lean)
        p.add("head", -16 * k, -8 * lean, 0)
        wig = 0.03 * math.sin(t * 16) * k
        body.hand_to(p, -1, RW[-1].lerp(tgt + V(0.05, 0.1, -0.2 + wig), k), elbow=(0.6, 0.3, -0.3),
                     hand_rot=hand_world((-0.3, -0.2, 1), (0, -1, 0)) if k > 0.5 else None)
        point(p, -1)
        p.side("upper_arm", 1, x=10 * lean, z=25 * lean, add=True)
        open_hand(p, 1, 8 * lean)
        body.plant(p, 1, roll=30 * toes, lift=0.36 * air)
        body.plant(p, -1, pos=(-0.08 * lean, 0, 0), roll=30 * toes, lift=0.36 * air)
        return p

    c.solve(reach_solve)

    def reach_face(t):
        p = Pose()
        k = pulse(t, 0.25, 0.3, 3.3, 0.5)
        p.face.update({"grin": -0.7 * k, "grit": 0.6 * k})
        abrows(p, -0.8 * k, -0.2 * k, 0.6 * k)
        return p + look((26 * k, -14 * k))

    c.layer(reach_face)
    c.layer(blink_layer([1.3, 3.9]))
    out.append(c)

    # ---- give up -----------------------------------------------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/give-up", T)
    c.key(0.0, REST)
    slump = REST.copy()
    slump.both("shoulder", z=-6)
    slump.both("upper_arm", x=4, y=0, z=-50)
    slump.set("chest", 8, 0, 0)
    slump.set("head", 14, 10, -6)
    slump.face = {"flat": 1.0}
    look_up = slump.copy()
    look_up.set("head", -2, 14, -4)
    look_up.face = {"smirk_L": 0.8, "flat": 0.3}
    c.key(0.5, slump, "inout")
    c.key(1.3, slump, "linear")
    c.key(1.7, look_up, "inout")
    c.key(2.1, look_up, "linear")
    c.key(T, REST, "inout")

    def give_face(t):
        p = Pose()
        s = pulse(t, 1.6, 0.2, 0.4, 0.3)
        abrows(p, 1.2 * s, 0.6 * s, -0.2 * s)
        return p + look((0, 12 * s))

    c.layer(give_face)
    c.solve(L.stand(body))
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    rw = L.rest_wrists(body)
    tip = V(COVER[0], COVER[1], SWITCH_Z)
    up = L.hand_world((0.25, -0.3, 1), (0.95, 0.3, 0.0))       # finger up and a little out, palm to the switch

    def holding(p, k, look_down=0.0):
        p.add("chest", -2 * k, 4 * k + 6 * look_down, -4 * k)
        p.add("head", 8 * look_down - 4 * k, 6 * k + 16 * look_down, 2 * look_down)
        p.side("shoulder", 1, z=10 * k, add=True)          # a shrug of the raised side lifts the dome clear
        wrist = tip - up.col[1] * 0.6
        body.hand_to(p, 1, rw[1].lerp(wrist, k), elbow=(0.9, 0.4, -0.3), hand_rot=up if k > 0.45 else None)
        if k > 0.2:
            L.point(p, 1)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)

    # ---- cover: the finger raised and laid on the switch, slowly, without fuss -------------------------
    T = 1.9
    c = Clip(f"{NAME}/cover", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: holding(p, ease("inout", smooth(0.15, 1.6, t))) or p)
    c.layer(lambda t: look((18 * smooth(0.2, 1.0, t), 14 * smooth(0.2, 1.0, t))))
    out.append(c)

    # ---- cover-hold ----------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/cover-hold", T, loop=True)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: holding(p, 1.0) or p)

    def hold_face(t, T=T):
        p = Pose()
        g = math.sin(math.tau * t / T)
        p = p + look((4, 4 + 4 * g))
        p.add("chest", -0.8 * g, 0, 0)
        return p

    c.layer(hold_face)
    c.layer(L.blinks([1.6]))
    out.append(c)

    # ---- brow: holding it, a look down at Archie on his left (or out at the reader), the right brow up -----
    for nm, at_archie in (("brow", True), ("brow-reader", False)):
        T = 3.2 if at_archie else 2.8
        c = Clip(f"{NAME}/{nm}", T)
        c.key(0.0, REST)
        d_of = (lambda t: pulse(t, 0.1, 0.5, 2.1, 0.5)) if at_archie else (lambda t: 0.0)
        c.solve(lambda t, p, skel, d_of=d_of: holding(p, 1.0, look_down=d_of(t)) or p)

        def brow_face(t, d_of=d_of, at_archie=at_archie):
            p = Pose()
            d = d_of(t)
            b = pulse(t, 0.8, 0.45, 1.3, 0.5) if at_archie else pulse(t, 0.3, 0.5, 1.6, 0.4)
            L.brows(p, 0.6 * b, 2.0 * b, 1.6 * b, side=-1)
            L.brows(p, -0.3 * b, -0.4 * b, -0.2 * b, side=1)
            p.face.update({"smile": -0.5 * b, "flat": 0.5 * b})
            L.lids(p, 0.25 * b)
            if not at_archie:
                p.add("head", 0, -8 * b, 0)                  # from the switch round to the reader
                return p + look((-2 * b, -4 * b))
            return p + look((-16 * d, 18 * d))

        c.layer(brow_face)
        out.append(c)

    # ---- uncover -------------------------------------------------------------------------------------
    T = 1.5
    c = Clip(f"{NAME}/uncover", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: holding(p, 1 - ease("inout", smooth(0.0, 1.3, t))) or p)
    out.append(c)
    return out
