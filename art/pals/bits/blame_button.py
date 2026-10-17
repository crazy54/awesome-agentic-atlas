"""The blame button: something falls over -- a traffic cone, between them -- and all three point at each
other. A little replay pops up over their heads: the three of them, in the act, plotting it together. Archie
reaches up and closes the replay.

The page stands the cast on the hero's top edge, the cone (prop `traffic-cone-large`) between Archie and Zip,
topples it, pops up the `replay-screen` prop above them (its screen drawn by the page: the replay), and plays
the screen's `close` clip when Archie's finger lands (CLOSE_HIT).

FORMATION (metres from Archie's root, x to his left = screen right):
    archie  (0, 0, 0), facing the reader
    cone    (CONE_X, 0, 0)
    zip     (ZIP_X, 0, 0)
    brick   (BRICK_X, 0, 0)
    screen  centre (SCREEN_X, SCREEN_Z) over their heads; its close button at its top right

Pieces (Archie):
    blame-button/point     he points at Zip (his left) -- him! -- then at Brick, indignant
    blame-button/close     a reach up to the replay's close button, a firm poke (CLOSE_HIT), a sheepish grin
    blame-button/whistle   hands behind his back, an innocent whistle at the sky
Zip points with his own `point`; Brick (clips/brick_base.py), facing the reader at Archie's right:
    blame-button/point     one enormous arm out at Archie: him
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import rest_wrists, whistle
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "blame-button"
CAST = ("archie", "zip", "brick")
CONE_X, ZIP_X, BRICK_X = 1.1, 2.2, -1.9
SCREEN_X, SCREEN_Z = 0.4, 3.4
CLOSE_HIT = 0.8


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
    out = []

    # ---- point: him! no, him! ------------------------------------------------------------------------
    TP = 3.0
    c = Clip(f"{NAME}/point", TP)
    c.key(0.0, L.REST)
    a = L.REST.copy()
    a.set("head", -4, 24, -4)
    a.set("chest", -2, 10, 0)
    a.face = {"grit": 0.6, "frown": 0.5}
    b = L.REST.copy()
    b.set("head", -4, -26, 4)
    b.set("chest", -2, -10, 0)
    b.face = {"grit": 0.6, "frown": 0.5}
    c.key(0.3, a, "snap")
    c.key(1.4, a, "linear")
    c.key(1.6, b, "snap")
    c.key(TP - 0.3, b, "linear")
    c.key(TP, L.REST)

    def point_solve(t, p, skel):
        ka = pulse(t, 0.05, 0.2, 1.1, 0.2)
        kb = pulse(t, 1.4, 0.2, 1.0, 0.25)
        jab = 0.04 * math.sin(t * 16)
        if ka > 0:
            body.hand_to(p, 1, RW[1].lerp(Vector((0.85 + jab, -0.4, 1.55)), ka), elbow=(0.7, 0.2, -0.1),
                         hand_rot=L.hand_world((1, -0.3, 0.1), (0, 0, 1)) if ka > 0.5 else None)
            L.point(p, 1)
        if kb > 0:
            body.hand_to(p, -1, RW[-1].lerp(Vector((-0.85 - jab, -0.4, 1.55)), kb), elbow=(0.7, 0.2, -0.1),
                         hand_rot=L.hand_world((-1, -0.3, 0.1), (0, 0, 1)) if kb > 0.5 else None)
            L.point(p, -1)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(point_solve)
    c.layer(lambda t: brows(Pose(), -1.4, -0.8, 0.8) + look((0, 20 if t < 1.5 else -20)))
    out.append(c)

    # ---- close: up to the replay's close button --------------------------------------------------------
    TC = 2.2
    c = Clip(f"{NAME}/close", TC)
    c.key(0.0, L.REST)
    up = L.REST.copy()
    up.set("head", -18, 8, 0)
    up.face = {"grit": 0.4, "smile": 0.6}
    c.key(0.4, up)
    c.key(1.4, up, "linear")
    sheep = L.REST.copy()
    sheep.set("head", -2, 0, 8)
    sheep.face = {"grit": 0.8, "smile": 0.4}
    c.key(1.7, sheep)
    c.key(TC, sheep, "linear")
    button = Vector((0.55, -0.45, 2.48))

    def close_solve(t, p, skel):
        k = pulse(t, 0.05, 0.5, 0.65, 0.4)
        poke = pulse(t, CLOSE_HIT - 0.1, 0.1, 0.05, 0.15)
        body.hand_to(p, 1, RW[1].lerp(button + Vector((0, 0.05 * poke - 0.05, -0.12)), k), elbow=(0.6, 0.3, -0.2),
                     hand_rot=L.hand_world((0.2, -0.3, 1), (0, -1, 0)) if k > 0.5 else None)
        L.point(p, 1)
        body.plant(p, 1, roll=18 * k)                           # up on his toes
        body.plant(p, -1, roll=18 * k)
        L.hips(body, p, dz=0.05 * k)
        return p

    c.solve(close_solve)
    c.layer(lambda t: brows(Pose(), 0.6, 1.2, 1.0) + look((16 * (1 - smooth(1.3, 1.6, t)), 0)))
    out.append(c)
    out.append(whistle(body, f"{NAME}/whistle", T=2.2))
    return out


def brick_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    T = 2.8
    c = Clip(f"{NAME}/point", T)
    c.key(0.0, L.REST)
    st = L.REST.copy()
    st.set("head", -2, 20, 0)
    st.face = {"flat": 1.0}
    c.key(0.5, st)
    c.key(T - 0.4, st, "linear")
    c.key(T, L.REST)

    def point_solve(t, p, skel):
        k = pulse(t, 0.2, 0.4, T - 1.1, 0.4)
        body.hand_to(p, 1, RW[1].lerp(Vector((1.9, -0.6, 2.0)), k), elbow=(0.8, 0.2, -0.2),
                     hand_rot=L.hand_world((1, -0.25, 0), (0, 0, 1)) if k > 0.5 else None)
        L.point(p, 1)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(point_solve)
    c.layer(lambda t: L.brows(Pose(), -0.6, -0.4, 0.4) + look((0, 20)))
    return [c]


def zip_clips(body):
    return []
