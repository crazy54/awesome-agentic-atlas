"""The glass door: Archie walks into the edge of the README viewer. Bonk. He feels for the invisible wall,
then draws a door on the glass -- the screen's own glass, between him and the reader -- opens it, and goes
through.

The page walks him along the bottom of the window to the reader's left edge (facing screen right, so the
wall is in front of him: WALL metres ahead of his root) and plays:

    glass-door/bonk     he walks face first into it, recoils, holds his nose, shakes it off
    glass-door/feel     palms flat on the glass, feeling round it, a knock with a knuckle: there IS a wall
    glass-door/draw     (turned to face the reader) a marker from behind his back; he draws a door in the air
                        in front of him, his own height and a little more, and dots a knob. The page traces
                        the marker's tip (bone `grip_R`, plus MARKER_TIP along it) into a line as he goes,
                        so the door is exactly where his hand went: DOOR, in his own frame.
    glass-door/through  he takes the knob, pulls the door open towards the reader, and steps through it;
                        the page clips him at the door's plane as he goes, and swings it shut behind him.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "glass-door"
CAST = ("archie",)
WALL = 0.36                     # metres from his root to the wall, facing it, at the moment of the bonk
# The door he draws, facing the reader, on the reader's surface beside him to his left (screen right), in
# his own frame (x to his left, z up): from the corner nearest him, up, across and down. Its hinge is the far
# edge; the knob is near the edge by him.
DOOR_Y = -0.25
DOOR = [(0.42, 0.04), (0.42, 2.25), (1.22, 2.25), (1.22, 0.04)]
KNOB = (0.55, 1.1)
MARKER_TIP = 0.16               # the marker's tip, metres along grip_L's Y


def V(*a):
    return Vector(a)


def clips(bodies):
    body = bodies["archie"]
    L = body.lib
    REST, hips, fist, point, open_hand, hand_world = L.REST, L.hips, L.fist, L.point, L.open_hand, L.hand_world
    out = []

    def rest_wrist(sg):
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        return L.wrist_of(body, q, sg)

    RW = {1: rest_wrist(1), -1: rest_wrist(-1)}

    # ---- bonk --------------------------------------------------------------------------------------
    c = Clip(f"{NAME}/bonk", 1.8)
    c.key(0.0, REST)

    def bonk_solve(t, p, skel):
        hit = pulse(t, 0.0, 0.04, 0.05, 0.35)                 # the recoil
        stag = smooth(0.05, 0.45, t) * (1 - smooth(1.2, 1.7, t))
        hips(body, p, dy=0.1 * stag + 0.05 * hit, dz=-0.04 * stag, pitch=-8 * hit + 4 * stag)
        p.add("chest", -14 * hit + 6 * stag, 0, 0)
        p.add("neck", -10 * hit, 0, 0)
        p.add("head", -22 * hit + 8 * stag, 0, 6 * stag)
        p.add("crest_1", 10 * hit, 0, 0); p.add("crest_2", 14 * hit, 0, 0); p.add("crest_3", 18 * hit, 0, 0)
        shake = math.sin((t - 1.0) * 30) * pulse(t, 0.95, 0.08, 0.3, 0.15)
        p.add("head", 0, 16 * shake, 0)
        # the back foot steps back as he staggers
        body.plant(p, 1, pos=(0, 0.16 * stag, 0), roll=-8 * pulse(t, 0.08, 0.1, 0.2, 0.2))
        body.plant(p, -1, pos=(0, 0.04 * stag, 0))
        # left hand flung up on the hit, right hand to his nose
        if hit > 0.01:
            p.side("upper_arm", 1, x=40 * hit, z=-44 + 60 * hit, add=False)
        n = pulse(t, 0.25, 0.25, 0.55, 0.3)
        if n > 0:
            nose = V(-0.02, -0.36, 1.86)
            body.hand_to(p, -1, RW[-1].lerp(nose + V(0, -0.06, -0.05), n), elbow=(0.4, 0.2, -0.6),
                         hand_rot=hand_world((0.3, 0.2, 1), (0, 1, 0)) if n > 0.5 else None)
        return p

    c.solve(bonk_solve)

    def bonk_face(t):
        p = Pose()
        hit = pulse(t, 0.0, 0.03, 0.2, 0.4)
        p.both("lid_up", x=-40 * hit)
        p.both("lid_lo", x=30 * hit)
        p.face.update({"grin": -1.0 * pulse(t, 0.0, 0.03, 1.2, 0.4), "grit": hit, "oh": pulse(t, 0.4, 0.1, 0.5, 0.2)})
        brows(p, 1.5 * pulse(t, 0.3, 0.1, 0.8, 0.3), 1.0 * pulse(t, 0.3, 0.1, 0.8, 0.3), -0.5 * hit)
        p = p + look((0, 0)) if t < 0.9 else p + look((8 * math.sin(t * 20), 14 * math.cos(t * 17)))
        return p

    c.layer(bonk_face)
    out.append(c)

    # ---- feel --------------------------------------------------------------------------------------
    c = Clip(f"{NAME}/feel", 3.2)
    c.key(0.0, REST)
    feel = REST.copy()
    feel.set("head", 4, 0, 10)
    feel.set("chest", 4, 0, 0)
    open_hand(feel, 1, 8)
    open_hand(feel, -1, 8)
    feel.face = {"flat": 0.6, "oh": 0.4}
    c.key(0.4, feel)
    c.key(2.7, feel, "linear")
    c.key(3.2, REST)
    wall_y = -WALL + 0.02

    def feel_solve(t, p, skel):
        w = pulse(t, 0.0, 0.4, 2.3, 0.5)
        hips(body, p, dy=-0.03 * w, pitch=4 * w)
        # palms flat on the glass, sliding round it; the right knocks twice near the end
        for sg, ph in ((1, 0.0), (-1, 1.7)):
            a = TAU_T(t, 1.7, ph)
            tgt = V(sg * (0.2 + 0.08 * math.cos(a)), wall_y + 0.14, 1.55 + 0.22 * math.sin(a))
            if sg < 0:
                knock = max(0.0, math.sin((t - 2.0) * 28)) * pulse(t, 2.0, 0.05, 0.4, 0.1)
                tgt = tgt + V(0, 0.06 * knock, 0)
            hr = hand_world((0, 0, 1), (0, -1, 0))             # fingers up, palm to the glass
            body.hand_to(p, sg, RW[sg].lerp(tgt, w), elbow=(0.6, 0.3, -0.4), hand_rot=hr if w > 0.5 else None)
        if 2.0 < t < 2.5:
            fist(p, -1)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(feel_solve)

    def feel_face(t):
        p = Pose()
        g = pulse(t, 0.6, 0.2, 1.8, 0.3)
        p = p + look((10 * math.sin(t * 2.3) * g, 12 * math.sin(t * 1.4) * g))
        brows(p, 0.4 * g, 1.6 * g, 1.0 * g, side=1)
        k = pulse(t, 2.0, 0.05, 0.5, 0.2)
        brows(p, 1.6 * k, 1.6 * k, 1.4 * k)
        return p

    c.layer(feel_face)
    c.layer(blink_layer([1.2, 2.6]))
    out.append(c)

    # ---- draw --------------------------------------------------------------------------------------
    TD = 3.8
    c = Clip(f"{NAME}/draw", TD)
    c.key(0.0, REST)
    pose = REST.copy()
    pose.face = {"smirk_L": 0.7, "grin": 0.3}
    pose.set("head", 4, 18, -4)                              # watching his own hand, out to his left
    c.key(0.6, pose)
    c.key(TD - 0.4, pose, "linear")
    c.key(TD, REST)
    path = [V(x, DOOR_Y, z) for x, z in DOOR]
    seg_len = [(b - a).length for a, b in zip(path, path[1:])]
    total = sum(seg_len)
    t0, t1 = 0.8, 2.9

    def along(u):
        d = u * total
        for a, b, l in zip(path, path[1:], seg_len):
            if d <= l:
                return a.lerp(b, d / l)
            d -= l
        return path[-1]

    def draw_solve(t, p, skel):
        # the marker from behind his back (0.05-0.6), the outline (t0-t1), a dot for the knob after
        reach = pulse(t, 0.05, 0.4, TD - 0.75, 0.3)
        if t < t0:
            tip = V(0.3, 0.2, 1.0).lerp(path[0], smooth(0.35, t0, t))
        elif t < t1:
            tip = along(ease("inout", (t - t0) / (t1 - t0)))
        else:
            k = smooth(t1, t1 + 0.25, t)
            tip = path[-1].lerp(V(KNOB[0], DOOR_Y, KNOB[1]), k)
            tip = tip + V(0, -0.05 * pulse(t, t1 + 0.28, 0.05, 0.06, 0.1), 0)
        # The body first: he leans and steps towards the far side, squats for the bottom corners and goes
        # up on his toes for the top. Then the arm, then the feet.
        far = smooth(0.55, 1.22, tip.x) * reach
        low = max(0.0, 0.95 - tip.z) * reach
        top = max(0.0, tip.z - 1.95) * reach
        hips(body, p, dx=0.26 * far, dz=-0.6 * low + 0.22 * top, roll=-10 * far, pitch=14 * low)
        p.add("spine", 10 * low, 0, -8 * far)
        p.add("chest", 0, 10 * far, -10 * far)
        p.add("head", -24 * top - 6 * low, 0, 0)
        wrist = tip + V(0, 0.2, 0)                            # the marker points at the glass, its tip ahead
        hr = hand_world((0.1, -1, 0.1), (1, 0, 0))
        body.hand_to(p, 1, RW[1].lerp(wrist, reach), elbow=(0.6, 0.4, -0.3), hand_rot=hr if reach > 0.4 else None)
        fist(p, 1, 0.85)
        body.plant(p, 1, pos=(0.22 * far, 0, 0), roll=36 * top, knee_out=0.12 * low)
        body.plant(p, -1, pos=(0.05 * far, 0, 0), roll=36 * top + 10 * far, knee_out=0.12 * low)
        return p

    c.solve(draw_solve)
    c.layer(lambda t: look((-4 + 14 * pulse(t, 1.1, 0.3, 0.7, 0.3), 16)))
    c.layer(blink_layer([0.5, 3.5]))
    out.append(c)

    # ---- through -----------------------------------------------------------------------------------
    # Facing the door now (screen right, so his right side is towards the reader): the right hand takes
    # the knob, a hand's length ahead of him, and pulls it round towards the reader; a little bow; then the
    # page walks him into the doorway.
    TT = 2.0
    c = Clip(f"{NAME}/through", TT)
    c.key(0.0, REST)
    go = REST.copy()
    go.face = {"grin": 1.0}
    c.key(0.5, go)
    c.key(TT - 0.3, go, "linear")
    c.key(TT, REST)

    def through_solve(t, p, skel):
        grab = pulse(t, 0.05, 0.3, 0.7, 0.35)
        knob = V(-0.05, -0.55, 1.1)
        pull = smooth(0.4, 1.0, t)
        k = knob.lerp(V(-0.55, -0.25, 1.1), pull)               # round towards his right: the reader's side
        bow = pulse(t, 1.05, 0.2, 0.2, 0.3)
        hips(body, p, pitch=8 * bow)
        p.add("chest", 16 * bow, 0, 0)
        p.add("head", 8 * bow, 0, 0)
        body.hand_to(p, -1, RW[-1].lerp(k + V(0, 0.16, 0), grab), elbow=(0.5, 0.4, -0.4),
                     hand_rot=hand_world((0, -1, 0), (1, 0, 0)) if grab > 0.5 else None)
        fist(p, -1, grab)
        p.side("upper_arm", 1, x=55 * bow, z=-25 * bow, add=True)
        open_hand(p, 1, 8 * bow)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(through_solve)
    c.layer(lambda t: look((0, -10 * pulse(t, 1.0, 0.2, 0.4, 0.3))))
    out.append(c)
    return {"archie": out}


def TAU_T(t, period, phase):
    return math.tau * t / period + phase
