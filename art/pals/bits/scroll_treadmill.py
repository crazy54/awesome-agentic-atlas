"""The scroll treadmill: as the reader scrolls a row of cards, Archie, standing on top of it, jogs to keep up.
Eventually he grabs a passing card and rides it.

The page stands him on the top edge of a row of cards (the homepage's `.rowscroll` shelves: the reader
scrolls them sideways, with the arrows or a swipe) and does the treadmill itself: while the cards move
under him it plays `jog` facing against them, faster the faster they go (a jog's own ground speed is JOG,
so `timeScale` = belt / JOG), and lets him drift with them when they outrun him.

    scroll-treadmill/land    he drops onto the edge from above (the page moves him down over the first
                             LAND seconds), lands, steadies
    scroll-treadmill/egg     points up at the row's arrows, then at the reader: go on
    scroll-treadmill/jog     (loop) a jog in place, leaning into it, arms pumping
    scroll-treadmill/pant    (loop) hands on his knees, puffing
    scroll-treadmill/hop-on  from standing, a hop up and onto the edge of the card under him, sitting, his
                             legs over the front of it
    scroll-treadmill/ride    (loop) sitting on the card's edge, swinging his legs, holding on
    scroll-treadmill/bye     (from the ride) a wave goodbye, still sitting
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look, stride_foot
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "scroll-treadmill"
CAST = ("archie",)
JOG_PERIOD, JOG_STRIDE, JOG_STANCE = 0.48, 0.55, 0.42
JOG = JOG_STRIDE / (JOG_STANCE * JOG_PERIOD)        # 2.73 m/s
LAND = 0.35
TAU = math.tau


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    REST, hips, hand_world, open_hand, fist, point = L.REST, L.hips, L.hand_world, L.open_hand, L.fist, L.point
    RW = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    out = []

    def stand(p, **kw):
        body.plant(p, 1, **kw)
        body.plant(p, -1, **kw)

    # ---- land ---------------------------------------------------------------------------------------
    T = 1.1
    c = Clip(f"{NAME}/land", T)
    c.key(0.0, REST)

    def land(t, p, skel):
        air = 1 - smooth(LAND - 0.05, LAND, t)
        squash = pulse(t, LAND, 0.06, 0.08, 0.4)
        hips(body, p, dz=-0.22 * squash, pitch=14 * squash)
        p.add("spine", 8 * squash, 0, 0)
        p.both("upper_arm", x=-10 * air + 20 * squash, z=40 * air + 12 * squash, add=True)
        p.both("forearm", x=30 * air, add=True)
        tuck = 0.18 * air
        stand(p, lift=tuck, roll=-20 * air, knee_out=0.05 * squash)
        return p

    c.solve(land)
    c.layer(lambda t: Pose(face={"oh": 0.7 * (1 - smooth(LAND, LAND + 0.3, t))}))
    c.layer(lambda t: look((-14 * pulse(t, 0.0, 0.1, LAND, 0.3), 0)))
    out.append(c)

    # ---- egg on: the arrows, then the reader --------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/egg", T)
    c.key(0.0, REST)
    sly = REST.copy()
    sly.face = {"smirk_L": 0.9, "grin": 0.3}
    c.key(0.8, sly)
    c.key(T, REST)

    def egg(t, p, skel):
        k = pulse(t, 0.1, 0.35, 1.0, 0.4)
        # up and to his left (screen right): where the row's arrows are
        body.hand_to(p, 1, RW[1].lerp(V(0.55, -0.35, 1.95), k), elbow=(0.5, 0.2, -0.6),
                     hand_rot=hand_world((0.5, -0.4, 0.8), (0, -1, 0)) if k > 0.5 else None)
        if k > 0.2:
            point(p, 1)
        # then the come-on: a beckon with the other hand
        b = pulse(t, 1.2, 0.2, 0.6, 0.3)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.32, -0.42, 1.3), b), elbow=(0.5, 0.2, -0.6),
                     hand_rot=hand_world((0.1, -0.3, 1), (0, -1, 0)) if b > 0.5 else None)
        if b > 0.2:
            p.fingers(-1, 50 + 40 * max(0.0, math.sin(TAU * 3 * t)), spread=0, thumb=20)
        stand(p)
        return p

    c.solve(egg)

    def egg_face(t):
        p = Pose()
        a = smooth(0.2, 0.5, t) * (1 - smooth(1.0, 1.2, t))
        p = p + look((22 * a, 26 * a), head=(-10 * a, 14 * a, 0))
        brows(p, 0.6 * smooth(1.1, 1.4, t), 1.2 * smooth(1.1, 1.4, t), 0.8, side=1)
        return p

    c.layer(egg_face)
    out.append(c)

    # ---- jog ----------------------------------------------------------------------------------------
    T = JOG_PERIOD
    c = Clip(f"{NAME}/jog", T, loop=True)
    jog_face = REST.copy()
    jog_face.face = {"grit": 0.5, "grin": 0.4}
    c.key(0.0, jog_face)
    c.key(T, jog_face, "linear")

    def jog(t, p, skel):
        u = t / T
        bob = math.cos(TAU * 2 * (u - 0.05))
        hips(body, p, dz=-0.05 + 0.04 * bob, pitch=8, yaw=-8 * math.sin(TAU * u))
        p.add("spine", 4, 0, 0)
        p.add("chest", 0, 10 * math.sin(TAU * u), 0)
        p.add("head", -4 + 2 * bob, -4 * math.sin(TAU * u), 0)
        sw = math.sin(TAU * u)
        for sg in (1, -1):
            p.side("upper_arm", sg, x=-40 * sw * sg + 10, z=-38, add=True)
            p.side("forearm", sg, x=70 + 15 * sw * sg, add=True)
            fist(p, sg, 0.7)
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, JOG_STRIDE, JOG_STANCE, ph, height=0.2)
            body.plant(p, sg, pos=(0, y, 0), lift=lift, roll=roll)
        return p

    c.solve(jog)
    c.layer(lambda t: Pose(face={"oh": 0.25 * (0.5 + 0.5 * math.sin(TAU * 2 * t / T))}))
    out.append(c)

    # ---- pant ---------------------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/pant", T, loop=True)
    puff = REST.copy()
    puff.face = {"open": 0.5, "oh": 0.3}
    c.key(0.0, puff)
    c.key(T, puff, "linear")

    def pant(t, p, skel):
        h = math.sin(TAU * 2 * t / T)                   # two puffs a loop
        hips(body, p, dy=0.06, dz=-0.12, pitch=30)
        p.add("spine", 14 + 2 * h, 0, 0)
        p.add("chest", 6 + 3 * h, 0, 0)
        p.add("head", -26 - 2 * h, 0, 0)
        for sg in (1, -1):
            knee = V(sg * 0.2, -0.24, 0.6)
            body.hand_to(p, sg, knee + V(sg * 0.02, 0, 0.02 * h), elbow=(0.6, 0.4, 0.0),
                         hand_rot=hand_world((-sg * 0.3, -0.3, -1), (0, 0, -1)))
            open_hand(p, sg, 6)
        stand(p, knee_out=0.06)
        return p

    c.solve(pant)
    c.layer(lambda t: Pose(face={"open": 0.25 * (0.5 + 0.5 * math.sin(TAU * 2 * t / T))}))
    out.append(c)

    # ---- the ledge sit: hips on the card's edge, legs over the front --------------------------------
    def ledge(p, k, swing=0.0):
        hz = body.hip_z
        hips(body, p, dy=0.06 * k, dz=(0.17 - hz) * k, pitch=-8 * k)
        p.add("spine", 10 * k, 0, 0)
        p.add("chest", 4 * k, 0, 0)
        for sg in (1, -1):
            w = RW[sg].lerp(V(sg * 0.36, 0.08, 0.06), k)
            body.hand_to(p, sg, w, elbow=(0.3, 0.6, 0.2), hand_rot=hand_world((0, 0.2, -1), (0, 0, -1)) if k > 0.6 else None)
            fist(p, sg, 0.6 * k)
            sw = swing * sg
            body.plant(p, sg, pos=(0, (-0.3 + 0.12 * sw) * k, 0), lift=(-0.62 + 0.05 * sw) * k, roll=(-6 - 22 * sw) * k)

    T = 0.8
    c = Clip(f"{NAME}/hop-on", T)
    c.key(0.0, REST)
    seat = REST.copy()
    seat.face = {"grin": 1.0, "wide": 0.3}
    c.key(T, seat)

    def hop_on(t, p, skel):
        up = pulse(t, 0.05, 0.18, 0.05, 0.3)
        k = ease("inout", smooth(0.25, T, t))
        hips(body, p, dz=0.12 * up * (1 - k))
        ledge(p, k)
        return p

    c.solve(hop_on)
    out.append(c)

    T = 1.6
    c = Clip(f"{NAME}/ride", T, loop=True)
    c.key(0.0, seat)
    c.key(T, seat, "linear")

    def ride(t, p, skel):
        ledge(p, 1.0, swing=math.sin(TAU * t / T))
        p.add("head", 0, 6 * math.sin(TAU * t / T), 0)
        return p

    c.solve(ride)
    out.append(c)

    T = 2.0
    c = Clip(f"{NAME}/bye", T)
    c.key(0.0, seat)
    c.key(T, seat, "linear")

    def bye(t, p, skel):
        ledge(p, 1.0, swing=math.sin(TAU * t / 1.6))
        k = pulse(t, 0.0, 0.3, 1.3, 0.35)
        w = math.sin(TAU * 2.4 * t)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.45 + 0.06 * w, -0.2, 0.95), k), elbow=(0.5, 0.2, -0.5),
                     hand_rot=hand_world((-0.3 + 0.4 * w, -0.1, 1), (0, -1, 0)) if k > 0.5 else None)
        if k > 0.3:
            open_hand(p, -1, 12)
        return p

    c.solve(bye)
    c.layer(lambda t: look((0, 0), head=(0, 0, 0)))
    out.append(c)
    return {"archie": out}
