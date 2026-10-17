"""The unauthorized renovation: the three of them turn up in hard hats and build a tiny balcony on the README
viewer's frame. Archie settles into a deck chair on it. Brick presents him with an eviction notice.

The page stands them on the viewer's top edge near its right end, hard hats on their heads (props
`hard-hat-lime`, `-violet`, `-orange` on each `head` bone), Archie with a `hammer` in his right hand; the
`balcony` prop is built out from the viewer's right edge (turned side on, its platform BALCONY_DEPTH deep)
while they hammer, the `deck-chair` stands on it, and Brick hands over the `eviction-notice`.

FORMATION (metres; Archie's root on the balcony is the deck chair's origin):
    archie  on the edge, hammering at HAMMER (in his frame); then on the balcony in the chair
    zip     (ZIP_X, 0, 0) beside him on the edge; brick on the edge at the viewer's corner, reaching down

Pieces (Archie):
    unauthorized-renovation/hammer   loops: down on one knee, hammering at the edge in front of him
    unauthorized-renovation/sit      down into the deck chair: leans back, hands behind his head; ends seated
    unauthorized-renovation/lounge   loops: seated, a contented sigh, a toe tap
    unauthorized-renovation/read     seated: takes the notice (right hand, READ_TAKE), reads it, his face falls
Zip (clips/zip_base.py): unauthorized-renovation/hammer, loops: his own hammering, beside Archie.
Brick (clips/brick_base.py), on the edge at the viewer's corner facing the balcony (screen right):
    unauthorized-renovation/present  the notice held out at arm's length to Archie in his chair; ends holding
                                     it out until Archie takes it (PRESENT_HOLD on)
"""
from __future__ import annotations

import math

from mathutils import Vector

from bits._moves import loop_clip, rest_wrists
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "unauthorized-renovation"
CAST = ("archie", "zip", "brick")
BALCONY_DEPTH = 2.4                  # the balcony's 0.6 m platform, drawn side on and stretched out
ZIP_X = -1.4
READ_TAKE = 0.7
PRESENT_HOLD = 1.3
HAMMER = Vector((0.0, -0.45, 0.1))


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    return out


def archie_clips(body):
    L = body.lib
    RW = rest_wrists(body)
    out = []

    # ---- hammer --------------------------------------------------------------------------------------
    TH = 0.8
    c = loop_clip(f"{NAME}/hammer", TH)
    kn = L.REST.copy()
    kn.set("head", 16, 0, 0)
    kn.face = {"grit": 0.6, "smirk_L": 0.4}
    c.key(0.0, kn)

    def hammer_solve(t, p, skel):
        L.hips(body, p, dz=-0.55, pitch=12, dy=0.05)
        p.add("spine", 8, 0, 0)
        p.add("chest", 6, 0, 0)
        u = (t / TH) % 1.0
        lift = math.sin(math.pi * u) ** 2 if u < 0.7 else 0.0
        hit = HAMMER + Vector((-0.14, 0.0, 0.42))
        tgt = hit + Vector((0.0, 0.1 * lift, 0.32 * lift))
        body.hand_to(p, -1, tgt, elbow=(0.6, 0.4, -0.2), hand_rot=L.hand_world((0.2, -1, 0.4 - 0.9 * lift), (1, 0, 0)))
        L.fist(p, -1, 1.0)
        body.hand_to(p, 1, HAMMER + Vector((0.16, 0.0, 0.32)), elbow=(0.6, 0.3, -0.2))
        L.fist(p, 1, 0.7)
        body.plant(p, 1, pos=(0.04, -0.2, 0), knee_out=0.1)
        body.plant(p, -1, pos=(-0.02, 0.24, 0), roll=34, knee_out=0.06)
        return p

    c.solve(hammer_solve)
    c.layer(lambda t: look((-24, 0)))
    out.append(c)

    def seated_pose(p, k, lean=-12.0):
        L.seated(p, body, k, lean=lean * k)
        f = L.sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])

    # ---- sit: into the deck chair, hands behind his head ---------------------------------------------
    TS = 2.6
    c = Clip(f"{NAME}/sit", TS)
    c.key(0.0, L.REST)
    ah = L.REST.copy()
    ah.face = {"smile": 1.0}
    c.key(1.2, ah)
    c.key(TS, ah, "linear")

    def sit_solve(t, p, skel):
        k = smooth(0.1, 1.2, t)
        seated_pose(p, k)
        hk = smooth(1.0, 1.8, t)
        for sg in (1, -1):
            behind = Vector((sg * 0.26, 0.12, 1.4))
            body.hand_to(p, sg, RW[sg].lerp(behind, hk), elbow=(0.9, 0.2, 0.4))
            L.open_hand(p, sg, 4)
        return p

    c.solve(sit_solve)

    def sit_face(t):
        p = Pose()
        r = smooth(1.6, 2.2, t)
        p.both("lid_up", x=-30 * r)
        return p + look((6, 0))

    c.layer(sit_face)
    out.append(c)

    # ---- lounge -----------------------------------------------------------------------------------------
    TL = 3.0
    c = loop_clip(f"{NAME}/lounge", TL)
    c.key(0.0, ah)

    def lounge_solve(t, p, skel):
        b = math.sin(math.tau * t / TL)
        seated_pose(p, 1.0)
        p.add("chest", -2 * b, 0, 0)
        for sg in (1, -1):
            body.hand_to(p, sg, Vector((sg * 0.26, 0.12, 1.4 + 0.01 * b)), elbow=(0.9, 0.2, 0.4))
            L.open_hand(p, sg, 4)
        p.add("toe_L", 20 * max(0.0, math.sin(math.tau * 2 * t / TL)), 0, 0)
        return p

    c.solve(lounge_solve)
    c.layer(lambda t: Pose().both("lid_up", x=-30))
    out.append(c)

    # ---- read: the notice ----------------------------------------------------------------------------
    TR = 3.6
    c = Clip(f"{NAME}/read", TR)
    c.key(0.0, ah)
    rd = L.REST.copy()
    rd.set("head", 14, 0, 0)
    rd.face = {"flat": 0.8}
    sad = L.REST.copy()
    sad.set("head", 6, 0, 6)
    sad.face = {"frown": 1.0}
    c.key(0.8, rd)
    c.key(2.2, rd, "linear")
    c.key(2.7, sad, "inout")
    c.key(TR, sad, "linear")

    def read_solve(t, p, skel):
        seated_pose(p, 1.0)
        take = smooth(0.2, READ_TAKE, t)
        held = Vector((-0.12, -0.55, 1.15))
        for sg in (1, -1):
            behind = Vector((sg * 0.26, 0.12, 1.4))
            if sg < 0:
                tgt = behind.lerp(Vector((-0.3, -0.8, 1.2)), take).lerp(held, smooth(READ_TAKE, READ_TAKE + 0.5, t))
            else:
                tgt = behind.lerp(held + Vector((0.24, 0.02, 0.02)), smooth(READ_TAKE + 0.2, READ_TAKE + 0.7, t))
            body.hand_to(p, sg, tgt, elbow=(0.6, 0.3, -0.4))
            L.fist(p, sg, 0.6)
        return p

    c.solve(read_solve)
    c.layer(lambda t: brows(Pose(), 1.2 * smooth(2.2, 2.6, t), 0.0, -0.8 * smooth(2.2, 2.6, t))
            + look((-20 * smooth(0.6, 1.0, t) * (1 - smooth(2.4, 2.7, t)), 0)))
    out.append(c)
    return out


def zip_clips(body):
    from bits._moves import loop_clip
    L = body.lib
    TH = 0.8
    c = loop_clip(f"{NAME}/hammer", TH)
    kn = L.REST.copy()
    kn.set("head", 14, 0, 0)
    kn.face = {"grin": 1.0}
    c.key(0.0, kn)

    def hammer_solve(t, p, skel):
        L.hips(body, p, dz=-0.32, pitch=10, dy=0.04)
        u = (t / TH + 0.5) % 1.0
        lift = math.sin(math.pi * u) ** 2 if u < 0.7 else 0.0
        hit = Vector((-0.1, -0.35, 0.36))
        body.hand_to(p, -1, hit + Vector((0.0, 0.08 * lift, 0.25 * lift)), elbow=(0.5, 0.4, -0.2),
                     hand_rot=L.hand_world((0.2, -1, 0.4 - 0.9 * lift), (1, 0, 0)))
        L.fist(p, -1, 1.0)
        body.hand_to(p, 1, Vector((0.12, -0.32, 0.3)), elbow=(0.5, 0.3, -0.2))
        L.fist(p, 1, 0.7)
        body.plant(p, 1, pos=(0.03, -0.14, 0), knee_out=0.08)
        body.plant(p, -1, pos=(-0.02, 0.18, 0), roll=30, knee_out=0.05)
        return p

    c.solve(hammer_solve)
    c.layer(lambda t: look((-24, 0)) + L.horn_sway(t, TH, 3.0, cycles=(1, 2)))
    return [c]


def brick_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    T = 3.2
    c = Clip(f"{NAME}/present", T)
    c.key(0.0, L.REST)
    st = L.REST.copy()
    st.set("head", 12, 0, 0)
    st.face = {"flat": 1.0}
    c.key(0.6, st)
    c.key(T, st, "linear")
    out_at = Vector((-0.35, -1.25, 1.35))

    def present_solve(t, p, skel):
        k = smooth(0.1, PRESENT_HOLD, t)
        L.hips(body, p, pitch=10 * k)
        body.hand_to(p, -1, RW[-1].lerp(out_at, k), elbow=(0.5, 0.3, -0.6),
                     hand_rot=L.hand_world((0, -0.4, 1), (0, -1, 0)) if k > 0.5 else None)
        L.fist(p, -1, 0.7)
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)
        return p

    c.solve(present_solve)
    c.layer(lambda t: L.brows(Pose(), 0.4, 0.2, -0.3) + look((-20, 0)))
    return [c]
