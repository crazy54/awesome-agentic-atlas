"""Pocket universe, wrong pocket: Archie can't find the Atlas Core. He pats himself down, then digs behind his
back and pulls out a rubber duck (over his shoulder with it), a cable (dropped, dangling) and a tiny traffic
cone (set down, carefully). Zip wanders over and points at his tummy: it's docked there, where it always is.
Archie, unruffled, takes it out and shows the world as if that had been the plan all along.

FORMATION (metres from Archie's root, x to his left -- the page's right): Archie at (0, 0) and Zip at ZIP, both
facing the reader. What he digs out rides his right hand's `grip_R` (the page attaches it at PULL_AT and lets
it go at TOSS_AT, DROP_AT or SET_AT); the Core is in its dock until `take`.

    archie  pocket-universe/search   REST -> REST: pats his chest, his sides, looks about him: where is it?
            pocket-universe/dig      REST -> SHOW: his right hand behind his back, rummaging, and out with
                                     something (PULL_AT), held up in front of his face, palm up
            pocket-universe/toss     SHOW -> REST: a flick over his right shoulder (TOSS_AT)
            pocket-universe/drop     SHOW -> REST: the hand opens (DROP_AT); a look down after it
            pocket-universe/set      SHOW -> REST: down on one knee-ish, set by his right foot (SET_AT)
            pocket-universe/realize  REST -> REST: looks down at the dock, a double take, a hand on the Core,
                                     a sheepish look at the reader
            pocket-universe/take, hold, present, back   the Core out, held, shown off, and back (HOLD:
                                     bits/_corekit.py; the page moves it at _corekit.GRAB and DOCK)
    zip     pocket-universe/point-belly REST -> REST: a hop closer, his right forefinger at Archie's tummy,
                                     held, a grin
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows as abrows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "pocket-universe"
CAST = ("archie", "zip")
ZIP = (0.95, -0.1)              # Zip's root, from Archie's
PULL_AT = 0.75                  # dig: it comes out from behind his back
TOSS_AT = 0.32                  # toss: let go, over his shoulder
DROP_AT = 0.45                  # drop: the hand opens
SET_AT = 0.95                   # set: it's on the floor
SHOW_WRIST = (-0.16, -0.5, 1.7)
DOCK = (0.0, -0.2, 1.225)       # the front of his dock (archie.py dock_c), for Zip to point at


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_(bodies["zip"])
    return out


# ------------------------------------------------------------------------------------------ archie
def archie(body):
    L = body.lib
    REST, hips, point, open_hand, hand_world, fist = L.REST, L.hips, L.point, L.open_hand, L.hand_world, L.fist
    rw = {sg: K.rest_wrist(body, sg) for sg in (1, -1)}
    behind = V(-0.28, 0.33, 1.02)
    palm_up = hand_world((0.35, -0.92, 0.1), (0, 0, 1))
    show = V(*SHOW_WRIST)
    out = []

    SHOW = REST.copy()
    SHOW.set("head", 8, -10, 6)                                 # peering at it
    SHOW.face = {"flat": 0.7, "oh": 0.2}
    eyes_on_it = look((-6, -12))

    def showing(p, k=1.0, at=None):
        tgt = rw[-1].lerp(at if at is not None else show, k)
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3, -0.6), hand_rot=palm_up if k > 0.5 else None)
        p.fingers(-1, 26 * k + 18 * (1 - k), spread=6, thumb=20 * k + 12 * (1 - k))

    # ---- search --------------------------------------------------------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/search", T)
    c.key(0.0, REST)
    down = REST.copy()
    down.set("head", 22, 0, 0)
    down.set("chest", 6, 0, 0)
    down.face = {"flat": 0.6, "frown": 0.3}
    about = REST.copy()
    about.set("head", 6, 24, 0)
    about.face = {"frown": 0.4}
    about2 = about.copy()
    about2.set("head", 6, -24, 0)
    c.key(0.35, down, "inout")
    c.key(1.2, down, "linear")
    c.key(1.6, about, "inout")
    c.key(2.1, about2, "inout")
    c.key(T, REST, "inout")

    def search_solve(t, p, skel):
        chest = pulse(t, 0.1, 0.25, 0.35, 0.25)
        sides = pulse(t, 0.75, 0.2, 0.3, 0.25)
        pat = abs(math.sin(math.tau * 4 * t)) * 0.03
        for sg in (1, -1):
            tgt = None
            if chest > 0.01:
                tgt = rw[sg].lerp(V(sg * 0.14, -0.3 - pat, 1.5), chest)
            if sides > 0.01:
                tgt = rw[sg].lerp(V(sg * 0.33, -0.12 - pat, 1.02), sides)
            if tgt is not None:
                body.hand_to(p, sg, tgt, elbow=(0.5, 0.3, -0.6),
                             hand_rot=hand_world((0, 0, -1), (0, 1, 0)) if max(chest, sides) > 0.5 else None)
                open_hand(p, sg, 4)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(search_solve)
    c.layer(lambda t: look((-24 * pulse(t, 0.3, 0.2, 0.9, 0.2), 0)))
    c.layer(blink_layer([1.4]))
    out.append(c)

    # ---- dig -----------------------------------------------------------------------------------------
    T = 1.5
    c = Clip(f"{NAME}/dig", T)
    c.key(0.0, REST)
    rum = REST.copy()
    rum.set("head", 4, -16, -6)
    rum.set("chest", 4, -10, 0)
    rum.face = {"grit": 0.4, "flat": 0.4}
    c.key(0.4, rum, "inout")
    c.key(PULL_AT, rum, "linear")
    c.key(T, SHOW, "inout")

    def dig_solve(t, p, skel):
        a = smooth(0.0, 0.4, t)
        b = smooth(PULL_AT, T - 0.1, t)
        rummage = 0.04 * math.sin(math.tau * 5 * t) * (1 - b) * a
        tgt = rw[-1].lerp(behind + V(rummage, 0, 0.5 * rummage), a).lerp(show, b)
        rot = palm_up if b > 0.4 else (hand_world((0, 0, -1), (1, 0, 0)) if a > 0.3 else None)
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3 + 0.4 * a * (1 - b), -0.6), hand_rot=rot)
        p.fingers(-1, 18 + 8 * a, spread=6, thumb=12 + 8 * a)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(dig_solve)
    c.layer(lambda t: eyes_on_it.scaled(smooth(PULL_AT, T, t)))
    out.append(c)

    # ---- toss / drop / set ---------------------------------------------------------------------------
    T = 1.2
    c = Clip(f"{NAME}/toss", T)
    c.key(0.0, SHOW)
    meh = REST.copy()
    meh.face = {"flat": 1.0}
    c.key(TOSS_AT, meh, "snap")
    c.key(T, REST, "inout")
    over = V(-0.45, -0.05, 2.05)                                # flicked up past his right shoulder

    def toss_solve(t, p, skel):
        flick = smooth(0.05, TOSS_AT, t)
        home = smooth(TOSS_AT + 0.1, T, t)
        tgt = show.lerp(over, flick).lerp(rw[-1], home)
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3, -0.6), hand_rot=None if home > 0.5 else palm_up)
        if t > TOSS_AT:
            open_hand(p, -1, 10 * (1 - home))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(toss_solve)
    out.append(c)

    T = 1.3
    c = Clip(f"{NAME}/drop", T)
    c.key(0.0, SHOW)
    c.key(DROP_AT + 0.2, meh, "inout")
    c.key(T, REST, "inout")

    def drop_solve(t, p, skel):
        home = smooth(DROP_AT + 0.25, T, t)
        showing(p, 1 - home)
        if t > DROP_AT:
            open_hand(p, -1, 10 * (1 - home))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(drop_solve)
    c.layer(lambda t: look((-26 * pulse(t, DROP_AT, 0.15, 0.3, 0.3), -10 * pulse(t, DROP_AT, 0.15, 0.3, 0.3))))
    out.append(c)

    T = 1.9
    c = Clip(f"{NAME}/set", T)
    c.key(0.0, SHOW)
    careful = REST.copy()
    careful.set("head", 26, -10, 0)
    careful.face = {"flat": 0.6, "smirk_R": 0.4}
    c.key(0.6, careful, "inout")
    c.key(SET_AT + 0.3, careful, "linear")
    c.key(T, REST, "inout")
    floor_w = V(-0.42, -0.42, 0.42)

    def set_solve(t, p, skel):
        k = pulse(t, 0.05, SET_AT - 0.05, 0.2, T - SET_AT - 0.25)
        hips(body, p, dz=-0.42 * k, pitch=22 * k, dx=-0.06 * k)
        p.add("spine", 10 * k, 0, 0)
        tgt = show.lerp(floor_w, smooth(0.05, SET_AT, t)).lerp(rw[-1], smooth(SET_AT + 0.2, T, t))
        body.hand_to(p, -1, tgt, elbow=(0.45, 0.3, -0.6), hand_rot=palm_up if t < SET_AT + 0.3 else None)
        body.plant(p, 1, knee_out=0.1 * k)
        body.plant(p, -1, pos=(0, 0.06 * k, 0), roll=24 * k, knee_out=0.1 * k)
        return p

    c.solve(set_solve)
    out.append(c)

    # ---- realize -------------------------------------------------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/realize", T)
    c.key(0.0, REST)
    belly = REST.copy()
    belly.set("head", 26, 0, 0)
    belly.set("chest", 8, 0, 0)
    belly.face = {"flat": 1.0}
    sheep = REST.copy()
    sheep.set("head", -2, -4, 10)
    sheep.face = {"grin": 0.7, "smirk_L": 0.7}
    c.key(0.3, belly, "inout")
    c.key(0.55, REST, "inout")
    c.key(0.75, belly, "snap")                                 # the double take
    c.key(1.7, belly, "linear")
    c.key(2.1, sheep, "inout")
    c.key(T - 0.3, sheep, "linear")
    c.key(T, REST, "inout")

    def realize_solve(t, p, skel):
        k = pulse(t, 0.9, 0.35, 0.8, 0.45)
        if k > 0.01:
            body.hand_to(p, 1, rw[1].lerp(V(*DOCK) + V(0.14, -0.04, 0.02), k), elbow=(0.55, 0.35, -0.5),
                         hand_rot=K.PALM_IN if k > 0.5 else None)
            open_hand(p, 1, 4 * k)
        s = pulse(t, 2.0, 0.2, 0.6, 0.2)
        if s > 0.01:
            body.hand_to(p, -1, rw[-1].lerp(V(-0.12, -0.05, 2.05), s), elbow=(0.5, 0.3, -0.3),
                         hand_rot=hand_world((0.2, 0.2, -1), (0, 1, 0)) if s > 0.5 else None)
            fist(p, -1, 0.4 * s)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(realize_solve)

    def realize_face(t):
        p = Pose()
        d = pulse(t, 0.72, 0.05, 0.6, 0.3)
        abrows(p, 1.8 * d, 2.0 * d, 1.2 * d)
        p.both("lid_up", x=10 * d)
        return p + look((-26 * pulse(t, 0.2, 0.15, 1.4, 0.3), 0))

    c.layer(realize_face)
    c.layer(blink_layer([2.3]))
    out.append(c)

    # ---- the Core after all ----------------------------------------------------------------------------
    out += [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]
    T = 2.2
    c = Clip(f"{NAME}/present", T)
    c.key(0.0, K.HOLD)
    proud = K.HOLD.copy()
    proud.set("head", -6, 10, 4)
    proud.face = {"grin": 1.0, "smirk_L": 0.5}
    c.key(0.4, proud, "back")
    c.key(T - 0.4, proud, "linear")
    c.key(T, K.HOLD, "inout")

    def present_solve(t, p, skel):
        K.held(body, p)
        ta = pulse(t, 0.1, 0.4, 1.1, 0.5)
        if ta > 0.01:
            body.hand_to(p, -1, rw[-1].lerp(V(-0.36, -0.5, 1.4), ta), elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((0.7, -0.6, 0.2), (0, 0, 1)) if ta > 0.5 else None)
            open_hand(p, -1, 10 * ta)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(present_solve)
    c.layer(lambda t: K.eyes_on_core(1 - pulse(t, 0.3, 0.3, 1.0, 0.3)))
    out.append(c)
    out.append(K.back(body, f"{NAME}/back"))
    return out


# --------------------------------------------------------------------------------------------- zip
def zip_(body):
    L = body.lib
    REST, hips, point, hand_world = L.REST, L.hips, L.point, L.hand_world
    rw = L.rest_wrists(body)
    belly = V(*DOCK) - V(ZIP[0], ZIP[1], 0)                     # Archie's dock, in Zip's frame
    T = 2.6
    c = Clip(f"{NAME}/point-belly", T, frames=78)
    c.key(0.0, REST)
    smug = REST.copy()
    smug.set("head", -4, -20, 6)
    smug.face = {"grin": 1.0, "smirk_R": 0.6}
    c.key(0.4, smug, "inout")
    c.key(T - 0.4, smug, "linear")
    c.key(T, REST, "inout")
    d = (belly - V(-0.25, -0.05, 1.15)).normalized()            # from about his right shoulder to it

    def solve(t, p, skel):
        k = pulse(t, 0.15, 0.4, 1.4, 0.45)
        hips(body, p, dx=-0.06 * k, roll=4 * k)
        tgt = V(-0.25, -0.05, 1.15) + d * 0.52
        hr = hand_world(d, (0, 0, -1))
        body.hand_to(p, -1, rw[-1].lerp(tgt, k), elbow=(0.5, 0.2, -0.4), hand_rot=hr if k > 0.5 else None)
        if k > 0.2:
            point(p, -1)
        jab = math.sin(math.tau * 3 * t) * pulse(t, 0.7, 0.1, 0.6, 0.2) * 0.03
        if jab:
            body.hand_to(p, -1, rw[-1].lerp(tgt + d * jab, k), elbow=(0.5, 0.2, -0.4),
                         hand_rot=hand_world(d, (0, 0, -1)) if k > 0.5 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    c.layer(lambda t: look((-10 * pulse(t, 0.3, 0.2, 1.3, 0.3), -20 * pulse(t, 0.3, 0.2, 1.3, 0.3))))
    c.layer(L.blinks([1.9]))
    return [c]
