"""The stolen spotlight: Archie, up on the home page's spotlight (`article.hero`), introduces its project in a
spotlight's beam. Zip swings the light round onto himself and dances in it. Archie hauls it back. Then
Brick switches on a third spotlight, twice the size, and dances them both off the stage.

The page stands them on the hero's top edge and aims the lights (props `spotlight-stand`; Brick's at
BIG_SCALE) at whoever has them by turning their `pan` and `tilt` bones every frame.

FORMATION (metres from Archie's root at the start, x to his left = screen right; all on the edge):
    archie  (0, 0, 0), facing the reader
    lamp    (LAMP_X, 0, 0): his spotlight, at the right end
    zip     (ZIP_X, 0, 0): between Archie and the lamp, once he has it
    brick   (BRICK_X, 0, 0): far left, his own lamp behind him at BRICK_LAMP_X

Pieces (Archie):
    stolen-spotlight/present  a sweep of his arm down at the project below him: may I present
    stolen-spotlight/huh      the light's gone: a look up and round for it
    stolen-spotlight/grab     at the lamp: both hands on its head, a wrestle, a heave round (the page swings
                              it back to his spot from GRAB_TURN)
    stolen-spotlight/jaw      slack-jawed, staring at Brick
Zip (clips/zip_base.py), at the lamp (screen left of it), facing it:
    stolen-spotlight/swing    both hands up on the lamp's head, a heave round towards himself (the page swings
                              the beam onto him from SWING_TURN); then he dances (his own `dance`)
    stolen-spotlight/stare    jaw on the floor, at Brick
Brick plays his everyday `finger-point` (the big lamp's switch, beside his head) and `much-better`.
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "stolen-spotlight"
CAST = ("archie", "zip", "brick")
LAMP_X, ZIP_X, BRICK_X, BRICK_LAMP_X = 3.6, 1.9, -3.0, -4.6
BIG_SCALE = 2.0
GRAB_TURN = 0.9
SWING_TURN = 0.8


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


def archie_clips(body):
    L = body.lib
    RW = rest_wrists(body)
    out = []

    # ---- present ------------------------------------------------------------------------------------
    TP = 3.0
    c = Clip(f"{NAME}/present", TP)
    c.key(0.0, L.REST)
    pr = L.REST.copy()
    pr.set("chest", -8, 6, 0)
    pr.set("head", 4, 10, -4)
    pr.face = {"wide": 0.7, "grin": 0.6}
    c.key(0.5, pr)
    c.key(TP - 0.4, pr, "linear")
    c.key(TP, L.REST)

    def present_solve(t, p, skel):
        k = pulse(t, 0.1, 0.5, TP - 1.0, 0.4)
        sweep = smooth(0.3, 1.2, t)
        tgt = Vector((0.9, -0.5, 1.6)).lerp(Vector((0.95, -0.35, 0.75)), sweep)
        body.hand_to(p, 1, RW[1].lerp(tgt, k), elbow=(0.7, 0.3, -0.2),
                     hand_rot=L.hand_world((0.8, -0.4, -0.4 * sweep), (0, 0, 1)) if k > 0.5 else None)
        L.open_hand(p, 1, 12)
        body.hand_to(p, -1, RW[-1].lerp(Vector((-0.12, -0.38, 1.3)), k), elbow=(0.5, 0.3, -0.6))
        body.plant(p, 1, pos=(0.04 * k, -0.06 * k, 0), yaw=10 * k)
        body.plant(p, -1)
        return p

    c.solve(present_solve)
    c.layer(lambda t: brows(Pose(), 1.0, 1.4, 1.0) + look((-14 * smooth(0.3, 1.2, t), 12)))
    c.layer(blink_layer([2.2]))
    out.append(c)

    # ---- huh: where's my light ----------------------------------------------------------------------
    TH = 1.6
    c = Clip(f"{NAME}/huh", TH)
    c.key(0.0, L.REST)
    up = L.REST.copy()
    up.set("head", -22, 0, 6)
    up.face = {"oh": 1.0}
    c.key(0.35, up, "snap")
    c.key(TH - 0.3, up, "linear")
    c.key(TH, L.REST)
    c.layer(lambda t: brows(Pose(), 1.6, 1.8, 1.2) + look((20, 30 * math.sin(t * 5) * pulse(t, 0.4, 0.2, 0.7, 0.2)))
            + Pose().add("head", 0, 20 * math.sin(t * 4) * pulse(t, 0.4, 0.2, 0.7, 0.2), 0))
    c.solve(lambda t, p, skel: (body.plant(p, 1), body.plant(p, -1), p)[-1])
    out.append(c)

    # ---- grab: wrestle the lamp back (the lamp head at his left, up at shoulder height) ---------------
    TG = 2.2
    c = Clip(f"{NAME}/grab", TG)
    c.key(0.0, L.REST)
    gr = L.REST.copy()
    gr.set("head", 0, 20, 0)
    gr.face = {"grit": 1.0}
    c.key(0.4, gr)
    c.key(TG - 0.3, gr, "linear")
    c.key(TG, L.REST)
    lamp = Vector((0.62, -0.25, 1.72))

    def grab_solve(t, p, skel):
        k = pulse(t, 0.0, 0.4, TG - 0.8, 0.4)
        heave = smooth(GRAB_TURN - 0.2, GRAB_TURN + 0.3, t)
        wr = 0.05 * math.sin(t * 18) * pulse(t, 0.4, 0.1, 0.4, 0.1)
        L.hips(body, p, dx=-0.06 * heave, dy=0.06 * heave, roll=6 * heave, yaw=-10 * heave)
        for sg, dx in ((1, 0.08), (-1, -0.1)):
            tgt = lamp + Vector((dx + wr, -0.12 * heave, 0.04 * sg))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.6, 0.3, -0.3))
            L.fist(p, sg, 0.9 * k)
        body.plant(p, 1, pos=(0.08, 0, 0))
        body.plant(p, -1, pos=(-0.06, 0.08 * heave, 0), roll=8 * heave)
        return p

    c.solve(grab_solve)
    c.layer(lambda t: brows(Pose(), -1.2, -0.6, 0.6) + look((10, 20)))
    out.append(c)

    # ---- jaw: Brick's dance ---------------------------------------------------------------------------
    TJ = 3.4
    c = Clip(f"{NAME}/jaw", TJ)
    c.key(0.0, L.REST)
    jw = L.REST.copy()
    jw.set("head", 4, -28, 0)
    jw.set("chest", 4, -10, 0)
    jw.both("upper_arm", x=4, z=-50)
    jw.face = {"wide": 1.0}
    c.key(0.5, jw)
    c.key(TJ - 0.4, jw, "linear")
    c.key(TJ, L.REST)
    c.layer(lambda t: brows(Pose(), 1.8, 1.8, 1.4) + look((0, -20)))
    c.layer(blink_layer([2.4]))
    c.solve(lambda t, p, skel: (L.hips(body, p, dz=-0.03 * smooth(0.2, 0.6, t)), body.plant(p, 1), body.plant(p, -1), p)[-1])
    out.append(c)
    return out


def zip_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    TS = 1.8
    c = Clip(f"{NAME}/swing", TS)
    c.key(0.0, L.REST)
    sly = L.REST.copy()
    sly.face = {"grin": 1.0, "smirk_L": 0.8}
    c.key(0.4, sly)
    c.key(TS - 0.3, sly, "linear")
    c.key(TS, L.REST)
    lamp = Vector((0.0, -0.42, 1.5))

    def swing_solve(t, p, skel):
        k = pulse(t, 0.0, 0.4, 1.0, 0.4)
        heave = smooth(SWING_TURN - 0.2, SWING_TURN + 0.3, t)
        for sg in (1, -1):
            tgt = lamp + Vector((sg * 0.1 - 0.2 * heave, 0.12 * heave, 0.0))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.5, 0.4, -0.4))
            L.fist(p, sg, 0.9 * k)
        body.plant(p, 1, roll=20 * k)
        body.plant(p, -1, roll=20 * k)
        L.hips(body, p, dz=0.04 * k, dy=0.05 * heave)
        return p

    c.solve(swing_solve)
    c.layer(lambda t: look((20, 0)) + L.horn_sway(t, TS, 3.0))
    out.append(c)
    TT = 3.0
    c = Clip(f"{NAME}/stare", TT)
    c.key(0.0, L.REST)
    jw = L.REST.copy()
    jw.set("head", 2, 30, 0)
    jw.face = {"wide": 1.0}
    c.key(0.4, jw)
    c.key(TT - 0.3, jw, "linear")
    c.key(TT, L.REST)
    c.solve(L.stand(body))
    c.layer(lambda t: brows(Pose(), 1.6, 1.8, 1.2) + look((0, 24)) + L.horn_sway(t, TT, 6.0))
    out.append(c)
    return out
