"""The invisible tug-of-war: Archie hauls on a cable that runs off the side of the page. Zip joins him. Brick
gives it one gentle tug -- and Archie is yanked off his feet, by his own back: the cable is his tether, and
it was plugged into him all along.

The page stands Archie on the hero's top edge facing screen right, the cable (drawn by the page) running
from his hands off the window's right edge, and his own tether from the port low on his back (bone `tether`)
down to the edge, along it under their feet and off the same side. At Brick's tug (TUG_AT on Brick's clock)
the slack runs out and the tether snaps him forwards.

FORMATION (metres from Archie's root; he faces screen right, his -Y):
    archie  (0, 0, 0)
    zip     (0, ZIP_AHEAD, 0): ahead of him on the cable, also facing right
    brick   further ahead, BRICK_AHEAD

Pieces (Archie):
    invisible-tug-of-war/pull     loops: the heave (`_moves.pull_rope`)
    invisible-tug-of-war/yank     snapped forwards off his feet by the back, down on his bottom
    invisible-tug-of-war/up       back up
    invisible-tug-of-war/look     a look back over his shoulder at the port in his back, then at the reader
Zip hauls with his own `pull` loop. Brick (clips/brick_base.py), facing screen right, the cable in both hands:
    invisible-tug-of-war/tug      one gentle tug (TUG_AT), and a look back down the line
"""
from __future__ import annotations

from mathutils import Vector

from bits._moves import get_up, knocked_down, pull_rope, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "invisible-tug-of-war"
CAST = ("archie", "zip", "brick")
ZIP_AHEAD, BRICK_AHEAD = 1.3, 2.8
TUG_AT = 0.6


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    return out


def archie_clips(body):
    L = body.lib
    out = [pull_rope(body, f"{NAME}/pull"),
           knocked_down(body, f"{NAME}/yank", lurch=(0.0, -0.5, 0.06)),
           get_up(body, f"{NAME}/up")]
    TL = 3.2
    c = Clip(f"{NAME}/look", TL)
    c.key(0.0, L.REST)
    back = L.REST.copy()
    back.set("head", 6, -70, 6)                                  # over his right shoulder, down at his back
    back.set("neck", 0, -16, 0)
    back.set("chest", 4, -18, 0)
    back.face = {"oh": 0.8}
    you = L.REST.copy()
    you.set("head", -2, -40, 6)
    you.face = {"flat": 1.0}
    c.key(0.6, back)
    c.key(1.6, back, "linear")
    c.key(2.0, you, "inout")
    c.key(TL - 0.3, you, "linear")
    c.key(TL, L.REST)
    c.layer(lambda t: brows(Pose(), 1.6 * pulse(t, 0.4, 0.2, 1.0, 0.3), 1.6 * pulse(t, 0.4, 0.2, 1.0, 0.3), 0.6)
            + look((-20 * pulse(t, 0.4, 0.2, 1.0, 0.3), -24)))
    c.layer(blink_layer([2.4]))
    c.solve(lambda t, p, skel: (body.plant(p, 1), body.plant(p, -1), p)[-1])
    out.append(c)
    return out


def brick_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    T = 2.8
    c = Clip(f"{NAME}/tug", T)
    c.key(0.0, L.REST)
    st = L.REST.copy()
    st.face = {"flat": 1.0}
    c.key(0.4, st)
    c.key(T - 0.3, st, "linear")
    c.key(T, L.REST)

    def tug_solve(t, p, skel):
        k = pulse(t, 0.0, 0.35, T - 0.8, 0.4)
        tug = pulse(t, TUG_AT - 0.1, 0.1, 0.1, 0.4)
        L.hips(body, p, dy=0.06 * tug, pitch=-4 * tug)
        for sg in (1, -1):
            tgt = Vector((sg * 0.14, -0.75 + 0.22 * tug + (0.1 if sg < 0 else 0.0), 1.25))
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.4, 0.5, -0.5),
                         hand_rot=L.hand_world((-sg, -0.2, 0), (0, 0, 1)) if k > 0.5 else None)
            L.fist(p, sg, 0.9 * k)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(tug_solve)
    c.layer(lambda t: look((-10, 0)) + Pose().add("head", 0, -40 * smooth(1.4, 1.8, t), 0))
    return [c]
