"""The unnecessary crew: Archie tries to move one tiny button and can't, and whistles for help. Brick arrives
with Zip, a row of traffic cones and a lifting harness built for a car. They rig the button into it, and up it
goes.

The page stands Archie on the hero's top edge with the button (prop `tiny-button`, BUTTON_SCALE) at his left
foot, puts the cones down round it as the crew sets them out, lowers the `lifting-harness` from above the
window until its cradle is on the edge, puts the button in the cradle, and hauls it all up.

FORMATION (metres from Archie's root, x to his left = screen right):
    archie  (0, 0, 0), facing the reader
    button  (BUTTON_X, 0, 0) on the edge
    cones   at CONES (x) on the edge, round the button
    brick   (BRICK_X, 0, 0), zip (ZIP_X, 0, 0)

Pieces (Archie):
    unnecessary-crew/push      down on one knee by the button, a fingertip push, a harder one, a strain: it won't
    unnecessary-crew/whistle   two fingers in his mouth: help!
    unnecessary-crew/direct    loops: the crane's banksman, both arms waving it up
    unnecessary-crew/thumbs    a big thumbs up
Brick and Zip play their everyday clips: Brick `carry` (the cones), `set-down`, `lift` (the button, with both
hands, as if it weighed a ton), `lift-hold`, `set-down`; Zip `run`, `point`, `cheer`.
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import loop_clip, rest_wrists, whistle
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "unnecessary-crew"
CAST = ("archie", "zip", "brick")
BUTTON_SCALE = 1.6
BUTTON_X = 0.5
CONES = (-0.2, 1.2, 1.9)
BRICK_X, ZIP_X = 2.8, -1.4


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    return out


def archie_clips(body):
    L = body.lib
    RW = rest_wrists(body)
    out = []

    # ---- push --------------------------------------------------------------------------------------
    TP = 3.2
    c = Clip(f"{NAME}/push", TP)
    c.key(0.0, L.REST)
    dn = L.REST.copy()
    dn.set("head", 12, 20, -6)
    dn.face = {"flat": 0.5}
    st = dn.copy()
    st.face = {"grit": 1.0}
    c.key(0.6, dn)
    c.key(1.6, dn, "linear")
    c.key(1.9, st)
    c.key(TP - 0.5, st, "linear")
    c.key(TP, L.REST)
    btn = Vector((BUTTON_X, -0.14, 0.12))

    def push_solve(t, p, skel):
        k = pulse(t, 0.0, 0.6, TP - 1.1, 0.5)
        L.hips(body, p, dx=0.12 * k, dz=-0.55 * k, pitch=10 * k, roll=-8 * k)
        p.add("spine", 6 * k, 0, -6 * k)
        push = 0.03 * pulse(t, 1.0, 0.1, 0.1, 0.2) + 0.05 * pulse(t, 1.9, 0.2, 0.7, 0.3)
        shake = 0.006 * math.sin(t * 40) * pulse(t, 1.9, 0.2, 0.7, 0.3)
        tgt = btn + Vector((-0.2 + push + shake, 0, 0.08))
        body.hand_to(p, 1, RW[1].lerp(tgt, k), elbow=(0.6, 0.3, -0.2),
                     hand_rot=L.hand_world((1, -0.2, -0.3), (0, -1, 0)) if k > 0.5 else None)
        L.point(p, 1)
        body.hand_to(p, -1, RW[-1].lerp(Vector((-0.22, -0.42, 0.6)), k), elbow=(0.6, 0.3, -0.2))
        body.plant(p, 1, pos=(0.1 * k, -0.06 * k, 0), knee_out=0.14 * k)
        body.plant(p, -1, pos=(-0.04 * k, 0.12 * k, 0), roll=26 * k, knee_out=0.1 * k)
        return p

    c.solve(push_solve)
    c.layer(lambda t: brows(Pose(), -1.0 * pulse(t, 1.8, 0.2, 0.8, 0.3), -0.6, 0.6) + look((-16, 16)))
    c.layer(blink_layer([0.5, 2.9]))
    out.append(c)
    out.append(whistle(body, f"{NAME}/whistle", T=1.8))

    # ---- direct: the banksman ------------------------------------------------------------------------
    TD = 1.6
    c = loop_clip(f"{NAME}/direct", TD)
    dr = L.REST.copy()
    dr.set("head", -16, 0, 0)
    dr.face = {"open": 0.6, "grin": 0.4}
    c.key(0.0, dr)

    def direct_solve(t, p, skel):
        u = math.sin(math.tau * t / TD)
        for sg in (1, -1):
            tgt = Vector((sg * 0.5, -0.3, 1.75 + 0.35 * max(0.0, sg * u)))
            body.hand_to(p, sg, tgt, elbow=(0.8, 0.2, 0.0), hand_rot=L.hand_world((0, -0.2, 1), (0, -1, 0)))
            L.open_hand(p, sg, 10)
            p.add(f"hand{'_L' if sg > 0 else '_R'}", 30 * max(0.0, sg * u), 0, 0)
        L.hips(body, p, dz=-0.02 * abs(u))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(direct_solve)
    c.layer(lambda t: brows(Pose(), 1.0, 1.4, 1.0) + look((20, 0)))
    out.append(c)

    # ---- thumbs ----------------------------------------------------------------------------------------
    TT = 1.8
    c = Clip(f"{NAME}/thumbs", TT)
    c.key(0.0, L.REST)
    th = L.REST.copy()
    th.face = {"grin": 1.0, "wide": 0.3}
    c.key(0.35, th)
    c.key(TT - 0.35, th, "linear")
    c.key(TT, L.REST)

    def thumbs_solve(t, p, skel):
        k = pulse(t, 0.05, 0.3, TT - 0.8, 0.4)
        body.hand_to(p, 1, RW[1].lerp(Vector((0.4, -0.5, 1.35)), k), elbow=(0.5, 0.2, -0.6),
                     hand_rot=L.hand_world((-0.3, -0.6, 0.7), (-1, 0, 0)) if k > 0.5 else None)
        L.fist(p, 1, k)
        p.side("thumb_1", 1, 0, 0, 0)
        p.side("thumb_2", 1, 0, 0, 0)
        p.side("thumb_3", 1, 0, 0, 0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(thumbs_solve)
    c.layer(lambda t: brows(Pose(), 1.0, 1.2, 1.0) + Pose().add("head", 6 * pulse(t, 0.4, 0.1, 0.05, 0.2), 0, 0))
    out.append(c)
    return out
