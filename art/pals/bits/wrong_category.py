"""Wrong category: Archie takes out the Atlas Core to present the coding workshop. It unfolds onto a tiny media
stage instead -- disco ball, spotlights, two little hologram dancers -- and a dance number starts. He does a
double take, holds the Core up to his face and taps it, looks again: still dancing. So he joins in.

The page stands him facing the reader and plays (the Core pieces are bits/_corekit.py's; HOLD is the Core
held up on his left palm):

    wrong-category/take     REST -> HOLD: the Core out of his belly (the page moves it to his palm at
                            _corekit.GRAB) and up
    wrong-category/present  HOLD -> HOLD: the presenter's sweep, proud, as it unfolds; his eyes go to the
                            projection, up to his left (screen right)
    wrong-category/huh      HOLD -> HOLD: a double take; the Core up to his face, peered at, tapped twice with
                            his right forefinger (TAPS); a look back up at the stage
    wrong-category/disco    HOLD -> HOLD: he joins in for twelve beats (BEAT), the Core held steady, his right
                            hand doing the disco point up and across, hips bouncing, eyes on the stage
    wrong-category/back     HOLD -> REST: the Core back in its dock (at _corekit.DOCK)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "wrong-category"
CAST = ("archie",)
BEAT = 0.5                      # seconds a beat in the dance number (120 a minute)
TAPS = (2.05, 2.35)             # huh: his fingertip on the Core
PROJ = (14, 30)                 # his eyes on the projection: up, to his left (degrees)


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    REST, hips, point, open_hand, hand_world = L.REST, L.hips, L.point, L.open_hand, L.hand_world
    HOLD = K.HOLD
    out = [K.take(body, f"{NAME}/take"), K.hold(body, f"{NAME}/hold")]
    rw_r = K.rest_wrist(body, -1)

    # ---- present -------------------------------------------------------------------------------------
    TP = 2.4
    c = Clip(f"{NAME}/present", TP)
    c.key(0.0, HOLD)
    proud = HOLD.copy()
    proud.set("head", -4, 10, 4)
    proud.set("chest", -6, 6, 0)
    proud.face = {"grin": 1.0}
    c.key(0.5, proud, "back")
    c.key(TP - 0.5, proud, "linear")
    c.key(TP, HOLD, "inout")

    def present_solve(t, p, skel):
        K.held(body, p)
        ta = pulse(t, 0.1, 0.4, 1.3, 0.5)
        if ta > 0.01:
            body.hand_to(p, -1, rw_r.lerp(V(-0.36, -0.5, 1.4), ta), elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((0.7, -0.6, 0.2), (0, 0, 1)) if ta > 0.5 else None)
            open_hand(p, -1, 10 * ta)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(present_solve)
    c.layer(lambda t: K.eyes_on_core(1 - pulse(t, 0.3, 0.3, 1.2, 0.3)) +
            look((PROJ[0] * pulse(t, 1.2, 0.3, 0.4, 0.4), PROJ[1] * pulse(t, 1.2, 0.3, 0.4, 0.4))))
    c.layer(blink_layer([0.9]))
    out.append(c)

    # ---- huh -----------------------------------------------------------------------------------------
    TH = 4.2
    c = Clip(f"{NAME}/huh", TH)
    c.key(0.0, HOLD)
    up = HOLD.copy()
    up.set("head", -8, 16, 6)                  # up at the stage, to his left
    up.face = {"grin": 0.6}
    snap = up.copy()
    snap.set("head", -12, 22, 9)
    snap.face = {"wide": 0.8, "oh": 0.3}
    peer = HOLD.copy()
    peer.set("head", 14, 8, -8)
    peer.set("chest", 6, 6, 0)
    peer.face = {"flat": 0.8}
    again = up.copy()
    again.face = {"flat": 1.0}
    c.key(0.3, up, "inout")
    c.key(0.62, HOLD, "inout")                 # glances down ...
    c.key(0.8, snap, "snap")                   # ... and snaps back up: the double take
    c.key(1.25, snap, "linear")
    c.key(1.6, peer, "inout")
    c.key(2.7, peer, "linear")
    c.key(3.1, again, "inout")
    c.key(3.7, again, "linear")
    c.key(TH, HOLD, "inout")
    near = V(0.1, -0.42, 1.62)                 # the Core up by his face

    def huh_solve(t, p, skel):
        k = pulse(t, 1.25, 0.4, 1.1, 0.45)
        K.held(body, p, 1.0, K.HOLD_WRIST.lerp(near, k))
        # the right forefinger taps the Core twice
        tk = pulse(t, 1.75, 0.25, 0.65, 0.3)
        if tk > 0.01:
            tap = max(pulse(t, a - 0.06, 0.06, 0.02, 0.08) for a in TAPS)
            core = near + V(-0.02, -0.06, 0.13)
            tgt = core + V(-0.2 + 0.06 * tap, -0.05, 0.02)
            body.hand_to(p, -1, rw_r.lerp(tgt, tk), elbow=(0.45, 0.3, -0.6),
                         hand_rot=hand_world((1, -0.2, 0.1), (0, 0, -1)) if tk > 0.5 else None)
            point(p, -1)
        # a one-shoulder shrug at the end
        s = pulse(t, 3.4, 0.2, 0.2, 0.35)
        p.add("shoulder_R", 0, 0, -12 * s)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(huh_solve)

    def huh_face(t):
        p = Pose()
        d = pulse(t, 0.75, 0.05, 0.5, 0.3)
        brows(p, 1.8 * d, 2.0 * d, 1.2 * d)
        p.both("lid_up", x=10 * d)               # eyes wide
        f = pulse(t, 1.5, 0.2, 1.2, 0.3)
        brows(p, -1.0 * f, 0.2 * f, 1.4 * f, side=1)
        u = min(1.0, pulse(t, 0.12, 0.15, 0.3, 0.1) + pulse(t, 0.75, 0.05, 0.5, 0.2) + pulse(t, 3.0, 0.2, 0.6, 0.3))
        p = p + look((PROJ[0] * u, PROJ[1] * u)) + K.eyes_on_core(1 - u)
        return p

    c.layer(huh_face)
    c.layer(blink_layer([1.4, 3.15]))
    out.append(c)

    # ---- disco ---------------------------------------------------------------------------------------
    # Twelve beats: the right hand points up to his right on the odd beats and down across his body on the
    # even ones; a bounce on every beat, the hips swaying with the point; easing in from HOLD and back.
    TD = 12 * BEAT
    c = Clip(f"{NAME}/disco", TD)
    c.key(0.0, HOLD)
    groove = HOLD.copy()
    groove.face = {"grin": 1.0}
    c.key(0.5, groove, "inout")
    c.key(TD - 0.5, groove, "linear")
    c.key(TD, HOLD, "inout")
    hi, lo = V(-0.62, -0.32, 2.1), V(0.12, -0.42, 1.0)
    hr_hi = hand_world((-0.55, -0.25, 0.8), (0, -1, 0))
    hr_lo = hand_world((0.6, -0.2, -0.75), (0, -1, 0))
    env = lambda t: smooth(0.0, 0.6, t) * (1 - smooth(TD - 0.6, TD, t))

    def disco_solve(t, p, skel):
        w = env(t)
        b = t / BEAT
        k = 0.5 - 0.5 * math.cos(math.pi * (b % 2))         # 0 up .. 1 down, through each two beats
        bounce = abs(math.sin(math.pi * b)) * w
        sway = math.sin(math.pi * b) * w
        hips(body, p, dz=-0.035 * bounce, dx=0.05 * sway, roll=-3 * sway, yaw=4 * (1 - 2 * k) * w)
        p.add("chest", 0, -6 * (1 - 2 * k) * w, 3 * sway)
        p.add("head", 4 * bounce, -8 * (1 - 2 * k) * w, 0)
        K.held(body, p, 1.0, K.HOLD_WRIST + V(0.02 * sway, 0, -0.015 * bounce))
        if w > 0.01:
            body.hand_to(p, -1, rw_r.lerp(hi.lerp(lo, k), w), elbow=(0.5, 0.2, -0.4),
                         hand_rot=(hr_hi if k < 0.5 else hr_lo) if w > 0.5 else None)
            point(p, -1)
        step = max(0.0, math.sin(math.pi * b)) * w
        body.plant(p, 1, roll=8 * step * (k < 0.5))
        body.plant(p, -1, roll=8 * step * (k >= 0.5))
        return p

    c.solve(disco_solve)
    c.layer(lambda t: K.eyes_on_core(1 - env(t)) +
            look((PROJ[0] * env(t) + 6 * math.sin(math.pi * t / BEAT) * env(t), PROJ[1] * 0.6 * env(t))))
    c.layer(lambda t: L.crest_follow(t * 3, 1.5 * env(t)))
    c.layer(blink_layer([2.2, 5.6]))
    out.append(c)

    out.append(K.back(body, f"{NAME}/back"))
    return {"archie": out}
