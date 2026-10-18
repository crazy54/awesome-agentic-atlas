"""The victory dance theft: Archie starts his big dance. Brick, standing by, unimpressed, casually does his
own move -- much better, smooth as anything, finishing in a lean no one should be able to do. Archie stops,
stares, and quietly slides out of frame.

FORMATION (metres, x across the page, both facing the reader): Brick stands BRICK_X from Archie, to Archie's
right (the page's left). Archie dances one of his everyday dances (archie-dances.glb), then `stare`s while
Brick does `much-better` (brick_base.py; its lean is 5.0-6.7 s in), then `slink`s off to his left, the page
moving him at SLINK_SPEED.

    archie  victory-dance-theft/stare   the dance stops dead; he watches, mouth open, a double take at the lean
            victory-dance-theft/slink   a sideways shuffle to his left, shoulders up, head down (loops; in place,
                                        the page moves him at SLINK_SPEED)
    brick   victory-dance-theft/watch   standing by, unimpressed, watching Archie on his left (loops)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, brows as abrows, look, stride_foot
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "victory-dance-theft"
CAST = ("archie", "brick")
BRICK_X = -3.0                  # Brick, from Archie
SLINK_PERIOD, SLINK_STANCE, SLINK_STEP = 0.9, 0.6, 0.5
SLINK_SPEED = SLINK_STEP / (SLINK_STANCE * SLINK_PERIOD)       # 0.93 m/s, to his left


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
    REST, hips, open_hand = L.REST, L.hips, L.open_hand
    out = []

    # ---- stare: the dance stops; he watches Brick (on his right), mouth open --------------------------
    T = 8.0
    c = Clip(f"{NAME}/stare", T)
    c.key(0.0, REST)
    frozen = REST.copy()
    frozen.both("upper_arm", x=20, y=0, z=-30)
    frozen.both("forearm", x=50, y=0, z=0)
    frozen.set("head", 0, -24, 0)
    frozen.set("chest", 0, -8, 0)
    frozen.face = {"oh": 0.6, "wide": 0.3}
    slump = REST.copy()
    slump.both("upper_arm", x=2, y=0, z=-50)
    slump.set("head", 2, -28, 2)
    slump.set("chest", 4, -10, 0)
    slump.face = {"wide": 0.8, "oh": 0.5}
    c.key(0.25, frozen, "snap")
    c.key(1.4, frozen, "linear")
    c.key(2.4, slump, "inout")
    c.key(T, slump, "linear")

    def stare_layer(t):
        p = Pose()
        # the double take at the lean (Brick's 5.0-6.7 s, which is about 4.0-5.7 s into this)
        dt = pulse(t, 4.1, 0.12, 1.3, 0.5)
        p.add("head", -8 * dt, -6 * dt, 0)
        p.add("chest", -6 * dt, 0, 0)
        p.face.update({"wide": 0.4 * dt})
        abrows(p, 1.6 + 0.8 * dt, 1.8 + 0.8 * dt, 1.2 + 0.6 * dt)
        return p + look((4 * dt, -26))

    c.layer(stare_layer)
    c.layer(blink_layer([3.2]))

    def stare_feet(t, p, skel):
        dt = pulse(t, 4.1, 0.12, 1.3, 0.5)
        hips(body, p, dy=0.06 * dt, pitch=-4 * dt)
        body.plant(p, 1, pos=(0, 0.1 * dt, 0))
        body.plant(p, -1, pos=(0, 0.04 * dt, 0))
        return p

    c.solve(stare_feet)
    out.append(c)

    # ---- slink: a sideways shuffle to his left, embarrassed ---------------------------------------------
    T = SLINK_PERIOD
    c = Clip(f"{NAME}/slink", T, loop=True, frames=int(round(T * 30)))
    sheep = REST.copy()
    sheep.both("shoulder", z=10)
    sheep.both("upper_arm", x=6, y=0, z=-48)
    sheep.set("chest", 8, 0, 0)
    sheep.set("head", 14, 10, 0)
    sheep.face = {"smirk_R": 0.5, "flat": 0.5}
    c.key(0.0, sheep)

    def slink_layer(t):
        u = t / T
        p = Pose()
        bob = math.cos(math.tau * 2 * u)
        hips(body, p, dz=-0.04 + 0.012 * bob, roll=2 * math.sin(math.tau * u))
        p.add("head", 0, 4 * math.sin(math.tau * u), 0)
        abrows(p, 1.0, 0.4, -0.2)
        return p + look((-6, -14))

    c.layer(slink_layer)

    def slink_solve(t, p, skel):
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, SLINK_STEP, SLINK_STANCE, ph, height=0.07, toe_off=6.0,
                                        heel_strike=0.0)
            body.plant(p, sg, pos=(-y, 0, 0), lift=lift, roll=roll * 0.4)
        return p

    c.solve(slink_solve)
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    T = 4.0
    c = Clip(f"{NAME}/watch", T, loop=True)
    c.key(0.0, REST)

    def watch_layer(t):
        p = breathe(T, 1.3)(t)
        p.add("head", 2, 14, 0)
        p.add("chest", 0, 4, 0)
        p.face.update({"smile": -0.4, "flat": 0.4})
        L.lids(p, 0.3)
        g = pulse(t, 1.8, 0.4, 1.0, 0.4)
        L.brows(p, 0.2 * g, 0.9 * g, 0.6 * g, side=-1)
        return p + look((-2, 16))

    c.layer(watch_layer)
    c.layer(L.blinks([1.1, 3.3]))
    c.solve(L.stand(body))
    return [c]
