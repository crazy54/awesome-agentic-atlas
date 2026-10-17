"""Zip moved in: Archie takes out the Atlas Core to show the reader this page's world, and it opens on Zip,
tiny, lounging in a deck chair in front of the world with a drink. He raises it: cheers. Archie protests
(MY core). Zip sips. Archie produces the lease and reads it, squinting, a finger running down it; he turns
it to the reader -- TENANT: ZIP -- and gives the reader a flat look. Zip waves him off, and Archie folds
the Core shut on him.

Archie holds the Core up on his left palm (HOLD, bits/_corekit.py) from `take` to `back`, his eyes up on
the projection (up, and to his left: screen right). His pieces (clips/archie_base.py, and the reactions
bits/_core_gags.py shares):

    zip-moved-in/take         REST -> HOLD (the Core to his palm at _corekit.GRAB)
    zip-moved-in/hold         HOLD, looping
    zip-moved-in/present      HOLD -> HOLD: behold
    zip-moved-in/double-take  HOLD -> HOLD
    zip-moved-in/protest      HOLD -> HOLD: MY core
    zip-moved-in/lease        HOLD -> HOLD: the right hand behind his back and out with the lease (in grip_R
                              from LEASE s), up before his eyes, read, squinting, a finger down it; at SHOW s
                              held out at the reader; lowered, and away behind his back again (gone at STOW s)
    zip-moved-in/deadpan      HOLD -> HOLD: a flat look at the reader
    zip-moved-in/back         HOLD -> REST (the Core back in the dock at _corekit.DOCK)
    zip-moved-in/belly        REST -> REST: a slurp from the Core in his belly: he looks down at it, pats it,
                              and gives the reader a flat look

Zip's, tiny, in the Core (clips/zip_base.py): he lies in the lounge-chair prop, which the page puts where
his root is, its foot end the way he faces; the page turns the two of them towards Archie, ahead of Zip and below.
The drink (prop) is in his left hand (grip_L) throughout, upright along the grip's -X.

    zip-moved-in/lounge       looping: lying back, the right hand behind his head, the drink on his chest,
                              a foot jiggling, eyes half shut
    zip-moved-in/cheers       lounge -> lounge: the drink raised high to Archie, clink clink, a wink
    zip-moved-in/sip          lounge -> lounge: a long sip through the straw
    zip-moved-in/bye          lounge -> lounge: the hand from behind his head and a slow wave over it (shoo),
                              eyes shut
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _core_gags as G
from . import _corekit as K

NAME = "zip-moved-in"
CAST = ("archie", "zip")
LEASE, SHOW, STOW = 0.75, 2.6, 4.6
CHAIR_SEAT = 0.38               # the lounge chair's seat, metres up (Zip-sized; its back from 0.28 m behind him)


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


def archie_clips(body):
    L = body.lib
    n = lambda piece: f"{NAME}/{piece}"           # noqa: E731
    out = [K.take(body, n("take")), K.hold(body, n("hold")), G.present(body, n("present")),
           G.double_take(body, n("double-take")), G.protest(body, n("protest")), G.deadpan(body, n("deadpan")),
           K.back(body, n("back"))]
    rw_r = K.rest_wrist(body, -1)

    # ---- lease ---------------------------------------------------------------------------------------
    T = 5.2
    c = Clip(n("lease"), T)
    c.key(0.0, K.HOLD)
    read = K.HOLD.copy()
    read.set("head", 10, -16, 0)
    read.face = {"flat": 0.6, "grin": 0.0}
    c.key(1.0, read)
    c.key(T - 0.6, read, "linear")
    c.key(T, K.HOLD)
    behind = V(-0.16, 0.26, 1.02)
    up = V(-0.36, -0.5, 1.2)                    # the lease up to read, in his right hand, its back to the reader
    out_ = V(-0.62, -0.5, 1.22)                 # held out to the reader, its face to them
    read_rot = L.hand_world((0, -0.3, 1), (0.3, 1, 0.2))      # (the page holds it along the fingers, its
    show_rot = L.hand_world((0.05, -0.1, 1), (0, -1, 0))      # face where the palm faces)

    def lease_solve(t, p, skel, T=T):
        K.held(body, p, 1.0)
        if t < LEASE:
            k = smooth(0.1, LEASE - 0.1, t)
            tgt = rw_r.lerp(behind, k)
            hr = None
        elif t < SHOW:
            k = smooth(LEASE, LEASE + 0.5, t)
            run = 0.03 * math.sin(math.tau * 1.3 * (t - 1.4)) * pulse(t, 1.4, 0.2, 0.7, 0.2)
            tgt = behind.lerp(up, k) + V(0, 0, run)             # scanning it, line by line
            hr = read_rot if k > 0.5 else None
        elif t < SHOW + 1.2:
            k = smooth(SHOW, SHOW + 0.35, t)
            tgt = up.lerp(out_, k)
            hr = show_rot
        else:
            k = smooth(SHOW + 1.2, STOW, t)
            tgt = out_.lerp(behind, k) if t < STOW else behind.lerp(rw_r, smooth(STOW, T, t))
            hr = show_rot if k < 0.5 else None
        body.hand_to(p, -1, tgt, elbow=(0.5, 0.3, -0.5), hand_rot=hr)
        L.fist(p, -1, 0.6 * smooth(LEASE - 0.15, LEASE, t) * (1 - smooth(STOW, STOW + 0.15, t)))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(lease_solve)

    def lease_face(t, T=T):
        p = Pose()
        rd = pulse(t, LEASE + 0.2, 0.3, SHOW - LEASE - 0.5, 0.3)
        sq = pulse(t, 1.6, 0.25, 0.6, 0.2)
        at_you = pulse(t, SHOW + 0.1, 0.2, 1.2, 0.3)
        p = p + look((-8 * rd, -20 * rd + 6 * math.sin(math.tau * 1.3 * t) * rd))     # down it, on his right
        p.both("lid_up", x=-20 * sq - 16 * at_you)
        brows(p, -0.8 * sq + 1.0 * at_you, -0.4 * sq + 1.2 * at_you, 0.3 * sq + 0.8 * at_you)
        p.face.update({"grit": 0.4 * sq, "flat": 0.6 * at_you})
        return p

    c.layer(lease_face)
    c.layer(blink_layer([0.4, 2.3, SHOW + 0.9]))
    out.append(c)

    # ---- belly ---------------------------------------------------------------------------------------
    T = 2.8
    c = Clip(n("belly"), T)
    c.key(0.0, L.REST)
    down = L.REST.copy()
    down.set("head", 24, 0, 0)
    down.set("chest", 6, 0, 0)
    down.face = {"oh": 0.3, "grin": 0.0}
    flat = L.REST.copy()
    flat.set("head", 0, 0, -3)
    flat.face = {"flat": 1.0, "grin": 0.0}
    c.key(0.35, down, "inout")
    c.key(1.3, down, "linear")
    c.key(1.7, flat, "inout")
    c.key(T - 0.35, flat, "linear")
    c.key(T, L.REST, "inout")

    def belly_solve(t, p, skel, T=T):
        k = pulse(t, 0.3, 0.3, 0.9, 0.35)
        tap = 0.03 * max(0.0, math.sin(math.tau * 3 * (t - 0.6))) * pulse(t, 0.6, 0.05, 0.55, 0.05)
        if k > 0.01:
            body.hand_to(p, -1, rw_r.lerp(V(-0.12, -0.38 - tap, 1.15), k), elbow=(0.5, 0.3, -0.6),
                         hand_rot=L.hand_world((1, 0, -0.2), (0, 1, 0)) if k > 0.5 else None)
            L.open_hand(p, -1, 4)
        p.both("shoulder", z=-5 * smooth(1.5, 1.9, t) * (1 - smooth(T - 0.4, T, t)))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(belly_solve)

    def belly_face(t, T=T):
        p = Pose()
        d = pulse(t, 0.2, 0.25, 1.0, 0.3)
        b = pulse(t, 2.0, 0.2, 0.2, 0.3)                 # the slow blink
        p.both("lid_up", x=-46 * b - 12 * smooth(1.5, 1.9, t) * (1 - b))
        p.both("lid_lo", x=20 * b)
        brows(p, 1.2 * d, 1.4 * d, 0.8 * d)
        return p + look((-30 * d, 0))

    c.layer(belly_face)
    out.append(c)
    return out


def zip_clips(body):
    L = body.lib
    out = []

    def lying(p):
        """In the chair: hips on its seat, lying back, legs out along it, the right hand behind his head. The
        body first, then the arms, then the feet; returns his left shoulder, where the drink hand works from."""
        L.hips(body, p, dy=0.16, dz=CHAIR_SEAT + 0.12 - body.hip_z, pitch=-42)
        p.add("spine", 4, 0, 0)
        p.add("chest", 6, 0, 0)
        p.add("head", 30, 0, -8)
        return body.where(p, "upper_arm_L")

    def pillow(p, k=1.0):
        """The right hand behind his head (k of the way there from his chest)."""
        sh_r = body.where(p, "upper_arm_R")
        body.hand_to(p, -1, (sh_r + V(0.1, -0.2, -0.1)).lerp(sh_r + V(0.0, 0.12, 0.32), k), elbow=(0.7, 0.2, 0.2),
                     hand_rot=L.hand_world((1, 0.2, 0.1), (0, -0.3, -1)) if k > 0.5 else None)
        L.open_hand(p, -1, 4)

    def feet(p, jiggle=0.0):
        # the legs out along the seat, the big shoes flopped out over its end, one of them waggling
        body.plant(p, 1, pos=(0.02, -0.66, 0), lift=CHAIR_SEAT, roll=-10, yaw=22)
        body.plant(p, -1, pos=(-0.02, -0.64, 0), lift=CHAIR_SEAT, roll=-14, yaw=10 + 26 * jiggle)

    def drink(p, sh_l, up=0.0, sip=0.0, clink=0.0):
        """The drink in his left hand (the page holds it upright along the grip's -X): on his chest, raised high
        to Archie (`up`, with a `clink` at the top), or to his mouth (`sip`)."""
        chest = sh_l + V(-0.14, -0.26, -0.12)
        raised = sh_l + V(0.12, -0.26, 0.66) + V(-0.04, -0.08, 0.04) * clink
        mouth = sh_l + V(-0.2, -0.32, 0.2)
        tgt = chest.lerp(raised, up).lerp(mouth, sip)
        body.hand_to(p, 1, tgt, elbow=(0.5, 0.3, -0.5), hand_rot=L.hand_world((-0.3, -1, 0), (-1, 0.3, 0)))
        L.fist(p, 1, 0.7)

    lounge = L.REST.copy()
    lounge.face = {"grin": 0.6, "smile": 0.4}

    # ---- lounge (loop) -------------------------------------------------------------------------------
    T = 3.0
    c = L.looped(f"{NAME}/lounge", T)
    c.key(0.0, lounge)

    def lounge_solve(t, p, skel, T=T):
        u = t / T
        sh_l = lying(p)
        pillow(p)
        drink(p, sh_l)
        feet(p, 0.5 + 0.5 * math.sin(math.tau * 3 * u))
        return p

    c.solve(lounge_solve)

    def lounge_face(t, T=T):
        u = t / T
        p = look((-6, 0))
        L.squint(p, 0.75)
        L.horns(p, x=2 * math.sin(math.tau * u))
        p.face["smile"] = 0.4 + 0.2 * math.sin(math.tau * u)
        return p

    c.layer(lounge_face)
    out.append(c)

    # ---- cheers --------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/cheers", T)
    c.key(0.0, lounge)
    c.key(T, lounge)

    def cheers_solve(t, p, skel, T=T):
        up = pulse(t, 0.15, 0.35, 1.0, 0.5)
        clink = pulse(t, 0.55, 0.08, 0.1, 0.2) + pulse(t, 0.85, 0.08, 0.1, 0.2)
        sh_l = lying(p)
        p.add("chest", -4 * up, 10 * up, 0)
        pillow(p)
        drink(p, sh_l, up=up, clink=clink)
        feet(p, 0.5)
        return p

    c.solve(cheers_solve)

    def cheers_face(t, T=T):
        up = pulse(t, 0.15, 0.35, 1.0, 0.5)
        p = look((-10 * up, 8 * up), head=(0, 0, 6 * up))          # at Archie: ahead of him, below
        brows(p, 0.0, 1.6 * up, 1.2 * up, side=1)
        p.face.update({"grin": 0.6 + 0.4 * up, "smirk_L": 0.8 * up, "smile": 0.4 * (1 - up)})
        L.squint(p, 0.75 - 0.4 * up)
        L.wink(p, 1, pulse(t, 0.9, 0.08, 0.2, 0.15))
        L.horns(p, x=8 * L.ring(t, 0.55, 18, 6))
        return p

    c.layer(cheers_face)
    out.append(c)

    # ---- sip -----------------------------------------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/sip", T)
    c.key(0.0, lounge)
    c.key(T, lounge)

    def sip_solve(t, p, skel, T=T):
        s = pulse(t, 0.15, 0.4, 0.9, 0.4)
        sh_l = lying(p)
        p.add("head", -8 * s, 0, -4 * s)
        pillow(p)
        drink(p, sh_l, sip=s)
        feet(p, 0.5)
        return p

    c.solve(sip_solve)

    def sip_face(t, T=T):
        s = pulse(t, 0.15, 0.4, 0.9, 0.4)
        p = look((0, 0))
        p.face.update({"grin": 0.6 * (1 - s), "oh": 0.7 * s, "smile": 0.4 * (1 - s)})
        L.squint(p, 0.75 + 0.25 * s)
        return p

    c.layer(sip_face)
    out.append(c)

    # ---- bye -----------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/bye", T)
    c.key(0.0, lounge)
    c.key(T, lounge)

    def bye_solve(t, p, skel, T=T):
        w = pulse(t, 0.1, 0.3, 1.3, 0.4)
        sh_l = lying(p)
        drink(p, sh_l)
        sh_r = body.where(p, "upper_arm_R")
        if w > 0.01:
            # the hand from behind his head, up over it, and waved off, slowly: shoo
            sw = math.sin(math.tau * 1.6 * (t - 0.4)) * smooth(0.35, 0.6, t)
            up = sh_r + V(-0.12 + 0.12 * sw, -0.2, 0.5)
            body.hand_to(p, -1, (sh_r + V(0.0, 0.12, 0.32)).lerp(up, w), elbow=(0.6, 0.1, -0.3),
                         hand_rot=L.hand_world((-0.5 * sw, -0.3, 1), (0.3 * sw, -1, 0)) if w > 0.5 else None)
            L.open_hand(p, -1, 8)
        else:
            pillow(p)
        feet(p, 0.5)
        return p

    c.solve(bye_solve)

    def bye_face(t, T=T):
        p = look((0, 0))
        L.squint(p, 1.0)
        p.face.update({"grin": 0.9, "smirk_L": 0.5})
        return p

    c.layer(bye_face)
    out.append(c)
    return out
