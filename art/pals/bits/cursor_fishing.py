"""Cursor fishing: Zip, up on the top edge of the home page's spotlight, spots the reader's pointer below
him on the card. Fishing rod out, a cast, and a horseshoe magnet lowered on its line towards it. The
magnet snaps onto the pointer -- and the pointer, it turns out, is stronger than he is: he is dragged along
the edge, heels skidding, leaning back on the rod, until he heaves; the magnet springs free (the reader's
pointer never notices any of this: nothing of it is touched) and clangs onto his own horn, and he sits
down hard. He looks at it, at the reader, shrugs, and goes, the magnet still on his horn.

The page stands him on the edge facing the pointer's side (1 or -1: screen right or left), and plays:

    cursor-fishing/spot    a stop, a look down over the edge at it, a slow, delighted grin, hands rubbed
    cursor-fishing/cast    the rod from behind his back (grip_R from ROD s), back over his shoulder, and a
                           cast: ends on FISH, the rod held out ahead, the line's end at its tip
    cursor-fishing/fish    FISH, looping: jiggling the rod, eyes on the magnet, tongue-in-cheek patience
    cursor-fishing/bite    FISH -> TUG: the snap: yanked forward, eyes wide
    cursor-fishing/drag    TUG, looping: heels dug in and skidding (the page drags him at whatever speed it
                           likes; the feet hold still under him, so on the page they slide), leaning back
    cursor-fishing/yank    TUG -> SEATED: an almighty heave back (the magnet lets go at FREE s), arms
                           flung up as he goes over backwards onto his bottom (the page sticks the magnet
                           on his left horn at CLANG s)
    cursor-fishing/up      SEATED -> REST: a look up at his horn, a shrug, and up

The rod is the fishing-rod prop in grip_R, along the grip's Y (where his fingers point): ROD_LEN metres to
its tip, where the page hangs its own line and magnet.
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "cursor-fishing"
CAST = ("zip",)
ROD, FREE, CLANG = 0.75, 0.42, 0.95
ROD_LEN = 1.3


def V(*a):
    return Vector(a)


def clips(bodies):
    if "zip" not in bodies:
        return {}
    body = bodies["zip"]
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    FISH_W = V(-0.12, -0.36, 1.02)                         # right wrist holding the rod out
    fish_rot = L.hand_world((0.05, -0.75, 0.66), (1, 0, 0))  # fingers (and the rod) forward and up
    TUG_W = V(-0.06, -0.38, 0.86)
    tug_rot = L.hand_world((0.05, -0.95, 0.25), (1, 0, 0))   # the rod pulled down level towards the pull

    def rod_hand(p, w, rot, k=1.0, left=True):
        body.hand_to(p, -1, RW[-1].lerp(w, k), elbow=(0.4, 0.3, -0.6), hand_rot=rot if k > 0.5 else None)
        L.fist(p, -1, 0.9 * k)
        if left and k > 0.01:
            body.hand_to(p, 1, RW[1].lerp(w + V(0.1, 0.06, -0.08), k), elbow=(0.5, 0.3, -0.5),
                         hand_rot=rot if k > 0.5 else None)
            L.fist(p, 1, 0.8 * k)

    fish = L.REST.copy()
    fish.set("chest", 6, 0, 0)
    fish.set("head", 14, 0, 0)
    fish.face = {"grin": 0.6, "smirk_L": 0.6}
    tug = L.REST.copy()
    tug.face = {"grin": 0.0, "grit": 1.0}

    # ---- spot ----------------------------------------------------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/spot", T)
    c.key(0.0, L.REST)

    def spot_solve(t, p, skel, T=T):
        lean = pulse(t, 0.2, 0.3, 1.3, 0.4)
        L.hips(body, p, dy=-0.04 * lean, pitch=10 * lean)
        p.add("head", 16 * lean, 0, 0)
        rub = pulse(t, 1.2, 0.2, 0.7, 0.3)
        if rub > 0.01:
            r = 0.02 * math.sin(math.tau * 5 * t)
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg].lerp(V(sg * (0.06 + r * sg), -0.32, 0.98), rub), elbow=(0.5, 0.3, -0.5),
                             hand_rot=L.hand_world((-sg, -0.3, 0.3), (0, 0, 1) if sg > 0 else (0, 0, -1)) if rub > 0.5 else None)
                L.open_hand(p, sg, 4)
        body.plant(p, 1, roll=8 * lean)
        body.plant(p, -1, roll=8 * lean)
        return p

    c.solve(spot_solve)

    def spot_face(t, T=T):
        p = Pose()
        down = pulse(t, 0.15, 0.25, 1.5, 0.4)
        grin = smooth(0.7, 1.4, t)
        p = p + look((-30 * down, 0))
        p.face.update({"grin": 0.6 * grin + 0.4 * (1 - down), "oh": 0.5 * down * (1 - grin), "smirk_L": 0.7 * grin})
        brows(p, 1.2 * down, 1.4 * down, 0.8 * down)
        brows(p, -1.0 * grin, -0.4 * grin, 0.3 * grin, side=-1)
        L.squint(p, 0.5 * grin)
        return p

    c.layer(spot_face)
    c.layer(L.blinks([0.9]))
    out.append(c)

    # ---- cast ----------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/cast", T)
    c.key(0.0, L.REST)
    c.key(T, fish)

    def cast_solve(t, p, skel, T=T):
        back = pulse(t, 0.1, 0.35, 0.25, 0.25)
        up = pulse(t, 0.75, 0.35, 0.15, 0.1)
        flick = smooth(1.3, 1.55, t)
        L.hips(body, p, dy=0.04 * up - 0.03 * flick, pitch=-6 * up + 8 * flick)
        p.add("chest", -10 * up + 8 * flick, 0, 0)
        if t < 0.75:
            body.hand_to(p, -1, RW[-1].lerp(V(-0.12, 0.26, 0.86), back), elbow=(0.5, 0.6, -0.4))
            L.fist(p, -1, smooth(0.4, ROD, t))
        elif t < 1.3:
            k = smooth(0.75, 1.1, t)
            body.hand_to(p, -1, V(-0.12, 0.26, 0.86).lerp(V(-0.16, 0.05, 1.42), k), elbow=(0.5, 0.2, -0.3),
                         hand_rot=L.hand_world((0, 0.6, 0.8), (1, 0, 0)) if k > 0.4 else None)
            L.fist(p, -1, 1.0)
        else:
            rod_hand(p, V(-0.16, 0.05, 1.42).lerp(FISH_W, flick), fish_rot if flick > 0.3 else L.hand_world((0, 0.6, 0.8), (1, 0, 0)),
                     left=flick > 0.6)
        body.plant(p, 1, roll=10 * flick * (1 - smooth(1.7, T, t)))
        body.plant(p, -1)
        return p

    c.solve(cast_solve)

    def cast_face(t, T=T):
        p = Pose()
        g = pulse(t, 0.7, 0.2, 0.7, 0.3)
        p.face.update({"grin": 1 - g, "grit": 0.7 * g})
        p = p + look((10 * g - 20 * smooth(1.5, 2.0, t), 0))
        L.horns(p, x=-8 * g + 10 * L.ring(t, 1.5, 18, 5))
        return p

    c.layer(cast_face)
    out.append(c)

    # ---- fish (loop) ---------------------------------------------------------------------------------
    T = 2.4
    c = L.looped(f"{NAME}/fish", T)
    c.key(0.0, fish)

    def fish_solve(t, p, skel, T=T):
        u = t / T
        jig = 0.02 * math.sin(math.tau * 3 * u)
        L.hips(body, p, dz=-0.02 + 0.01 * math.sin(math.tau * u))
        rod_hand(p, FISH_W + V(0, 0, jig), fish_rot)
        body.plant(p, 1, roll=-10 * max(0.0, math.sin(math.tau * 2 * u)) ** 2)
        body.plant(p, -1)
        return p

    c.solve(fish_solve)

    def fish_face(t, T=T):
        u = t / T
        p = Pose()
        p = p + look((-30 + 4 * math.sin(math.tau * u), 0))
        brows(p, 0.6, 0.8 + 0.4 * math.sin(math.tau * 2 * u), 0.6)
        L.horns(p, x=2 * math.sin(math.tau * u))
        return p

    c.layer(fish_face)
    c.layer(L.blinks([1.4]))
    out.append(c)

    # ---- bite ----------------------------------------------------------------------------------------
    T = 0.8
    c = Clip(f"{NAME}/bite", T)
    c.key(0.0, fish)
    c.key(T, tug)

    def bite_solve(t, p, skel, T=T):
        yank = pulse(t, 0.0, 0.06, 0.15, 0.4)
        set_ = smooth(0.25, T, t)
        L.hips(body, p, dy=-0.1 * yank + 0.1 * set_, pitch=18 * yank - 14 * set_, dz=-0.06 * set_)
        p.add("chest", 10 * yank, 0, 0)
        rod_hand(p, FISH_W.lerp(TUG_W, max(yank, set_)) + V(0, -0.1 * yank, 0), fish_rot if set_ < 0.5 else tug_rot)
        body.plant(p, 1, roll=20 * yank)
        body.plant(p, -1, roll=20 * yank)
        return p

    c.solve(bite_solve)

    def bite_face(t, T=T):
        p = Pose()
        w = pulse(t, 0.0, 0.05, 0.3, 0.3)
        p.face.update({"wide": w, "grit": smooth(0.3, T, t)})
        brows(p, 2.2 * w, 2.2 * w, 1.6 * w)
        L.horns(p, x=14 * L.ring(t, 0.02, 20, 5))
        return p

    c.layer(bite_face)
    out.append(c)

    # ---- drag (loop) ---------------------------------------------------------------------------------
    T = 0.8
    c = L.looped(f"{NAME}/drag", T)
    c.key(0.0, tug)

    def drag_solve(t, p, skel, T=T):
        u = t / T
        jolt = math.sin(math.tau * 2 * u)
        L.hips(body, p, dy=0.12, dz=-0.08 + 0.01 * jolt, pitch=-16 + 3 * jolt, roll=3 * math.sin(math.tau * u))
        p.add("chest", -6, 0, 0)
        p.add("head", 12, 0, 0)
        rod_hand(p, TUG_W + V(0, -0.02 * jolt, 0.01 * jolt), tug_rot)
        # heels dug in, toes up, the feet chattering
        body.plant(p, 1, pos=(0, -0.08, 0), roll=-22 + 5 * jolt)
        body.plant(p, -1, pos=(0, 0.04, 0), roll=-16 - 5 * jolt)
        return p

    c.solve(drag_solve)

    def drag_face(t, T=T):
        u = t / T
        p = Pose()
        p.face.update({"grin": 0.0, "grit": 1.0, "wide": 0.3})
        L.squint(p, 0.6)
        brows(p, -1.4, -0.6, 0.8)
        p = p + look((-20, 0))
        L.horns(p, x=10 + 4 * math.sin(math.tau * 2 * u), z=3 * math.sin(math.tau * 3 * u))
        L.ears(p, tilt=-8)
        return p

    c.layer(drag_face)
    out.append(c)

    # ---- yank ----------------------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/yank", T)
    c.key(0.0, tug)
    seated = L.REST.copy()
    seated.face = {"grin": 0.0, "flat": 0.7}
    c.key(T, seated)

    def yank_solve(t, p, skel, T=T):
        heave = pulse(t, 0.0, 0.3, 0.1, 0.05)
        go = smooth(FREE, FREE + 0.45, t)
        L.seated(p, body, go)
        L.hips(body, p, dy=0.12 * (1 - go) + 0.08 * go, dz=(-0.08 - 0.04 * heave) * (1 - go), pitch=(-16 - 12 * heave) * (1 - go) - 14 * go)
        bump = pulse(t, FREE + 0.45, 0.04, 0.05, 0.3)
        L.hips(body, p, dz=-0.03 * bump)
        if go < 0.5:
            rod_hand(p, TUG_W + V(0, 0.08 * heave, 0.06 * heave), tug_rot)
        else:
            k = smooth(0.5, 1.0, go)
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.42, 0.12, 1.32), k * (1 - smooth(1.15, T, t))) + V(0, 0, 0),
                             elbow=(0.6, 0.2, -0.3))
                L.open_hand(p, sg, 12)
        f = L.sit_feet(go)
        body.plant(p, 1, pos=f[1]["pos"], yaw=f[1]["yaw"], lift=0.2 * pulse(t, FREE, 0.2, 0.1, 0.3))
        body.plant(p, -1, pos=f[-1]["pos"], yaw=f[-1]["yaw"], lift=0.14 * pulse(t, FREE, 0.2, 0.1, 0.3))
        return p

    c.solve(yank_solve)

    def yank_face(t, T=T):
        p = Pose()
        go = smooth(FREE, FREE + 0.3, t)
        clang = pulse(t, CLANG, 0.03, 0.1, 0.4)
        p.face.update({"grin": 0.0, "grit": 1 - go, "wide": go * (1 - clang) * 0.8, "oh": clang})
        brows(p, 2.0 * go, 2.0 * go, 1.4 * go)
        L.squint(p, 0.9 * clang)
        L.horns(p, x=-14 * go + 22 * L.ring(t, CLANG, 22, 5), z=8 * L.ring(t, CLANG, 18, 5))
        return p

    c.layer(yank_face)
    out.append(c)

    # ---- up ------------------------------------------------------------------------------------------
    T = 2.8
    c = Clip(f"{NAME}/up", T)
    c.key(0.0, seated)
    c.key(T, L.REST)

    def up_solve(t, p, skel, T=T):
        k = 1 - smooth(1.9, 2.6, t)
        L.seated(p, body, k)
        shr = pulse(t, 0.9, 0.25, 0.5, 0.3)
        p.both("shoulder", z=16 * shr, add=True)
        f = L.sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])
        if shr > 0.01:
            for sg in (1, -1):
                knee = body.where(p, f"shin{'_L' if sg > 0 else '_R'}")
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.42, -0.2, 0.62 + 0.4 * k * 0), shr), elbow=(0.2, 0.25, -1.0),
                             hand_rot=L.hand_world((sg * 0.55, -0.82, 0.08), (0, 0, 1)) if shr > 0.5 else None)
                L.open_hand(p, sg, 10 * shr)
        return p

    c.solve(up_solve)

    def up_face(t, T=T):
        p = Pose()
        horn = pulse(t, 0.1, 0.25, 0.4, 0.3)
        at_you = pulse(t, 0.9, 0.2, 0.6, 0.3)
        p = p + look((30 * horn, 22 * horn - 4 * at_you), head=(-6 * horn, 0, 10 * horn))
        p.face.update({"flat": 0.7 * (1 - at_you), "smirk_R": 0.8 * at_you, "grin": 0.4 * at_you + smooth(2.2, T, t)})
        brows(p, 1.4 * horn, 1.6 * horn, 1.0 * horn)
        brows(p, 0.0, 1.4 * at_you, 1.0 * at_you, side=-1)
        return p

    c.layer(up_face)
    c.layer(L.blinks([0.6, 1.7]))
    out.append(c)
    return {"zip": out}
