"""The souvenir theft: Zip tiptoes along the top of the home page's spotlight, stops over its star rating,
checks nobody is looking, and plucks a star out of it -- a decorative copy; the rating is never touched --
and hides it behind his back. He whistles. A star drops out from behind him. Then another. He stuffs them
back; they pour out faster than he can; he gives up, shows two empty hands, and legs it, still shedding
stars.

The page stands him on the card's top edge (the floor, z = 0), facing the reader, with the rating's star
glyph below and to his right (screen left): his root STAND metres to its right. Pieces:

    souvenir-theft/pinch     REST -> HIDE: a look down at the rating, a shifty look each way, a crouch and a
                             reach down over the edge with his right hand; at GRAB seconds the page lifts the
                             star out of the rating into his hand (grip_R); up, and the hand behind his back
    souvenir-theft/innocent  HIDE, looping: rocking heel to toe, whistling, eyes on the ceiling
    souvenir-theft/oops      HIDE -> HIDE: freezes, looks down behind himself at what just fell, then at the
                             reader, and grins
    souvenir-theft/stuff     HIDE, looping: frantic, both hands behind his back stuffing stars back in,
                             glancing over each shoulder
    souvenir-theft/busted    HIDE -> REST: brings both hands round, empty, palms up, the guilty grin

HIDE is REST with both hands behind his back, his wrists at HIDE_WRISTS (the right one holding the star).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "souvenir-theft"
CAST = ("zip",)
STAND = 0.2                     # his root this far to the right of the rating's star (screen right of it)
GRAB = 1.85                     # pinch: the star leaves the rating for his hand
HIDE_WRISTS = {1: (0.1, 0.26, 0.86), -1: (-0.1, 0.26, 0.88)}


def V(*a):
    return Vector(a)


def clips(bodies):
    if "zip" not in bodies:
        return {}
    body = bodies["zip"]
    L = body.lib
    RW = L.rest_wrists(body)
    behind = L.hand_world((0, 0.3, -1), (0, 1, 0))           # fingers down, palm back: hands behind him
    out = []

    def hidden(p, k=1.0, wob=0.0):
        """Both hands behind his back, `k` of the way from rest."""
        for sg in (1, -1):
            tgt = V(*HIDE_WRISTS[sg]) + V(0, 0, 0.02 * wob * sg)
            body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.5, 0.6, -0.4), hand_rot=behind if k > 0.6 else None)
        L.fist(p, -1, 0.7 * k)
        p.fingers(1, 40 * k + 22 * (1 - k), thumb=20)
        return p

    hide = L.REST.copy()
    hide.set("chest", -2, 0, 0)
    hide.face = {"grin": 0.6, "smile": 0.4}

    # ---- pinch ---------------------------------------------------------------------------------------
    T = 3.2
    c = Clip(f"{NAME}/pinch", T)
    c.key(0.0, L.REST)
    c.key(T, hide)
    star = V(-STAND, -0.42, 0.06)

    def pinch_solve(t, p, skel, T=T, star=star):
        down = pulse(t, 0.95, 0.4, 0.55, 0.45)
        L.hips(body, p, dz=-0.3 * down, dy=0.05 * down, pitch=22 * down, yaw=-10 * down)
        p.add("spine", 12 * down, 0, 0)
        p.add("chest", 8 * down, -8 * down, 0)
        reach = pulse(t, 1.05, 0.5, 0.35, 0.4)
        grab = smooth(GRAB - 0.08, GRAB, t)
        if reach > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(star + V(0.02, 0.12, 0.14), reach), elbow=(0.4, 0.2, -0.6),
                         hand_rot=L.hand_world((0, -0.6, -1), (0, 1, 0)) if reach > 0.5 else None)
            L.open_hand(p, -1, 10 * (1 - grab))
            if grab > 0:
                L.fist(p, -1, 0.7 * grab)
        tuck = smooth(2.35, 3.0, t)
        if tuck > 0:
            hidden(p, tuck)
        body.plant(p, 1, knee_out=0.06 * down)
        body.plant(p, -1, knee_out=0.06 * down)
        return p

    c.solve(pinch_solve)

    def pinch_face(t):
        p = Pose()
        at = pulse(t, 0.0, 0.25, 0.5, 0.15)                   # down at the rating
        shifty = math.sin(math.tau * (t - 0.6) / 0.7) * pulse(t, 0.55, 0.05, 0.6, 0.05)
        glee = pulse(t, GRAB, 0.1, 0.5, 0.3)
        p = p + look((-24 * at - 14 * pulse(t, 1.1, 0.2, 0.6, 0.2), -20 * at + 30 * shifty),
                     head=(14 * at, 0, -10 * at + 22 * shifty))
        brows(p, 0.4 * at, 1.0 * at, 0.6 * at)
        brows(p, -1.0 * abs(shifty), -0.4 * abs(shifty), 0.4 * abs(shifty))
        p.face.update({"grin": 1 - 0.6 * abs(shifty), "smirk_L": 0.8 * abs(shifty), "wide": 0.0})
        p.face["grin"] += 0.0
        L.squint(p, 0.4 * abs(shifty) + 0.5 * glee)
        L.horns(p, x=-4 * L.ring(t, 0.6) + 6 * L.ring(t, GRAB, 18, 6))
        return p

    c.layer(pinch_face)
    c.layer(L.blinks([0.45, 2.7]))
    out.append(c)

    # ---- innocent (loop) -----------------------------------------------------------------------------
    T = 2.4
    c = L.looped(f"{NAME}/innocent", T)
    c.key(0.0, hide)

    def innocent_solve(t, p, skel, T=T):
        u = t / T
        rock = math.sin(math.tau * u)
        L.hips(body, p, dy=0.015 * rock, dz=0.01 * abs(rock), pitch=-2 * rock)
        hidden(p, 1.0, rock)
        body.plant(p, 1, roll=-16 * max(0.0, -rock) + 12 * max(0.0, rock))
        body.plant(p, -1, roll=-16 * max(0.0, -rock) + 12 * max(0.0, rock))
        return p

    c.solve(innocent_solve)

    def innocent_face(t, T=T):
        u = t / T
        p = Pose()
        p = p + look((26, 14 * math.sin(math.tau * u)), head=(-8, 6 * math.sin(math.tau * u), 4 * math.sin(math.tau * u)))
        brows(p, 1.4, 1.6, 1.0)
        w = 0.5 + 0.5 * math.sin(math.tau * 4 * u)              # whistling: an "oo", pulsing
        p.face.update({"grin": 0.0, "oh": 0.5 + 0.3 * w, "smile": 0.2})
        L.horns(p, x=2 * math.sin(math.tau * u), z=1.5 * math.sin(math.tau * 2 * u))
        return p

    c.layer(innocent_face)
    out.append(c)

    # ---- oops ----------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/oops", T)
    c.key(0.0, hide)
    c.key(T, hide)

    def oops_solve(t, p, skel, T=T):
        froze = pulse(t, 0.0, 0.08, 1.4, 0.3)
        back = pulse(t, 0.25, 0.2, 0.5, 0.25)
        L.hips(body, p, dz=-0.015 * froze, yaw=12 * back)
        p.add("chest", 0, 14 * back, 0)
        hidden(p, 1.0)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(oops_solve)

    def oops_face(t, T=T):
        p = Pose()
        back = pulse(t, 0.25, 0.2, 0.5, 0.25)
        at_you = pulse(t, 1.05, 0.12, 0.4, 0.25)
        grin = smooth(1.15, 1.4, t)
        p = p + look((-22 * back, 28 * back), head=(10 * back, 0, 30 * back))
        p.face.update({"grin": grin * 0.6, "wide": 0.8 * pulse(t, 0.0, 0.06, 0.95, 0.2), "smirk_R": 0.6 * grin})
        brows(p, 1.8 * pulse(t, 0.0, 0.06, 1.0, 0.3), 2.0 * pulse(t, 0.0, 0.06, 1.0, 0.3), 1.0)
        L.horns(p, x=8 * L.ring(t, 0.02, 20, 5))
        p.face["grin"] += 0.0 * at_you
        return p

    c.layer(oops_face)
    c.layer(L.blinks([1.0]))
    out.append(c)

    # ---- stuff (loop) --------------------------------------------------------------------------------
    T = 1.2
    c = L.looped(f"{NAME}/stuff", T)
    c.key(0.0, hide)

    def stuff_solve(t, p, skel, T=T):
        u = t / T
        jab = math.sin(math.tau * 3 * u)
        L.hips(body, p, dz=-0.03 - 0.01 * abs(jab), yaw=10 * math.sin(math.tau * u), pitch=6)
        p.add("chest", 6, 10 * math.sin(math.tau * u), 0)
        for sg in (1, -1):
            k = math.sin(math.tau * 3 * u + (0 if sg > 0 else math.pi))
            tgt = V(*HIDE_WRISTS[sg]) + V(sg * 0.04 * k, 0.03 * k, -0.06 + 0.06 * k)
            body.hand_to(p, sg, tgt, elbow=(0.5, 0.6, -0.4), hand_rot=behind)
            L.open_hand(p, sg, 10)
        body.plant(p, 1, roll=8 * max(0.0, jab))
        body.plant(p, -1, roll=8 * max(0.0, -jab))
        return p

    c.solve(stuff_solve)

    def stuff_face(t, T=T):
        u = t / T
        p = Pose()
        over = math.sin(math.tau * u)
        p = p + look((-10, 30 * over), head=(6, 0, 28 * over))
        p.face.update({"grin": 0.0, "grit": 0.7, "wide": 0.3})
        brows(p, 1.6, 1.2, 0.4)
        L.horns(p, x=4 * math.sin(math.tau * 3 * u), z=3 * math.sin(math.tau * 3 * u + 1))
        return p

    c.layer(stuff_face)
    out.append(c)

    # ---- busted --------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/busted", T)
    c.key(0.0, hide)
    up = L.REST.copy()
    up.both("shoulder", z=14)
    up.set("head", -4, 0, 12)
    up.face = {"grin": 0.6, "smirk_L": 0.7}
    c.key(0.5, up)
    c.key(1.7, up, "linear")
    c.key(T, L.REST)

    def busted_solve(t, p, skel, T=T):
        hk = 1 - smooth(0.0, 0.55, t)                          # leaving HIDE
        show = pulse(t, 0.3, 0.3, 1.0, 0.5)
        if hk > 0.001:
            hidden(p, hk)
        for sg in (1, -1):
            if show > 0.01:
                tgt = V(sg * 0.42, -0.32, 0.94)
                cur = L.wrist_of(body, p, sg)
                body.hand_to(p, sg, cur.lerp(tgt, show), elbow=(0.2, 0.25, -1.0),
                             hand_rot=L.hand_world((sg * 0.55, -0.82, 0.08), (0, 0, 1)) if show > 0.5 else None)
                L.open_hand(p, sg, 12 * show)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(busted_solve)

    def busted_face(t, T=T):
        p = Pose()
        g = pulse(t, 0.3, 0.3, 1.1, 0.4)
        brows(p, 1.6 * g, 1.8 * g, 0.8 * g)
        L.squint(p, 0.4 * g)
        p = p + look((4 * g, -6 * g))
        return p

    c.layer(busted_face)
    c.layer(L.blinks([1.5]))
    out.append(c)
    return {"zip": out}
