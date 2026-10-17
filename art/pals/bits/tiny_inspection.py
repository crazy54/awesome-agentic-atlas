"""The tiny inspection: Zip finds an access panel on the page's glass, knocks, hears something hollow, kits
up (a violet hard hat clapped on, a flashlight from behind his back), heaves the panel up and duck-walks in
under it. It drops shut. A little inspection light moves about inside -- leaking round the panel's edges,
through its empty screw holes, out under it across the floor -- with thumps and a "hmm". Then the panel
lifts and he backs out, stands up, and on his head, over the hat, sits an enormous dust bunny, looking at
the reader. He looks up at it. He sneezes.

The page walks him along the bottom of the window to the panel's left edge, facing it (screen right), his
root PANEL_GAP metres short of it, and plays (all in place; the page moves him for the duck-walk):

    tiny-inspection/knock    two knocks on the panel at chest height, an ear to it, a sly look round at the
                             reader (his right, the reader's side, as he faces screen right)
    tiny-inspection/kit-up   (facing the reader) the right hand behind his back and out with the flashlight
                             (in grip_R from TORCH s), the left up behind his head: the hat goes on at HAT s
    tiny-inspection/lift     (facing the panel) hands under its bottom edge, heaved up over his head (the
                             page swings it up from LIFT s); down into the duck-walk's crouch: ends on DUCK
    tiny-inspection/duck     DUCK, looping: a waddling duck-walk in place at DUCK_SPEED, the light held out
    tiny-inspection/emerge   DUCK -> REST: up out of the crouch with a pop (the bunny on his head bounces),
                             eyes rolled up at it, a wary blink
    tiny-inspection/sneeze   a sneeze: ah... ah... CHOO, the horns flapping, a sniff
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import brows, look, stride_foot
from kit.anim import Clip, Pose, pulse, smooth

NAME = "tiny-inspection"
CAST = ("zip",)
PANEL_GAP = 0.42                # his root this far left of the panel's left edge for knock and lift
TORCH, HAT = 0.75, 1.45         # kit-up: flashlight into grip_R; hat on his head
LIFT = 0.45                     # lift: the panel starts to swing up
DUCK_PERIOD, DUCK_STANCE, DUCK_STRIDE = 0.6, 0.6, 0.24
DUCK_SPEED = DUCK_STRIDE / (DUCK_STANCE * DUCK_PERIOD)       # 0.67 m/s
SNEEZE = 1.05                   # sneeze: the CHOO


def V(*a):
    return Vector(a)


def clips(bodies):
    if "zip" not in bodies:
        return {}
    body = bodies["zip"]
    L = body.lib
    RW = L.rest_wrists(body)
    out = []

    def crouched(p, k, bob=0.0):
        L.hips(body, p, dz=-0.32 * k + bob, dy=0.06 * k, pitch=26 * k)
        p.add("spine", 10 * k, 0, 0)
        p.add("chest", 6 * k, 0, 0)
        p.add("head", -26 * k, 0, 0)
        return p

    # ---- knock ---------------------------------------------------------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/knock", T)
    c.key(0.0, L.REST)

    def knock_solve(t, p, skel, T=T):
        w = pulse(t, 0.1, 0.25, 1.15, 0.35)
        rap = max(pulse(t, 0.5, 0.05, 0.02, 0.1), pulse(t, 0.78, 0.05, 0.02, 0.1))
        ear = pulse(t, 1.05, 0.2, 0.5, 0.3)
        L.hips(body, p, dy=-0.03 * ear, pitch=6 * ear, roll=-3 * ear)
        if w > 0.01:
            tgt = V(0.04, -PANEL_GAP + 0.14 + 0.05 * rap, 0.86)
            body.hand_to(p, -1, RW[-1].lerp(tgt, w), elbow=(0.4, 0.3, -0.6),
                         hand_rot=L.hand_world((0.1, -0.3, 1), (0, -1, 0)) if w > 0.5 else None)
            L.fist(p, -1, w)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(knock_solve)

    def knock_face(t, T=T):
        p = Pose()
        ear = pulse(t, 1.05, 0.2, 0.5, 0.3)
        sly = pulse(t, 1.85, 0.12, 0.45, 0.2)
        p = p + look((6 * ear, 0), head=(4 * ear, -10 * ear, -40 * sly))
        L.ears(p, spin=60 * ear, side=1)
        brows(p, 1.4 * ear, 1.2 * ear, 0.6 * ear)
        brows(p, 0.0, 1.6 * sly, 1.2 * sly, side=1)
        p.face.update({"grin": 1 - 0.6 * ear + 0.2 * sly, "oh": 0.5 * ear, "smirk_L": 0.8 * sly})
        L.squint(p, 0.4 * sly)
        L.horns(p, x=4 * L.ring(t, 0.52) + 4 * L.ring(t, 0.8))
        return p

    c.layer(knock_face)
    c.layer(L.blinks([0.3, 2.3]))
    out.append(c)

    # ---- kit-up --------------------------------------------------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/kit-up", T)
    c.key(0.0, L.REST)
    proud = L.REST.copy()
    proud.set("chest", -6, 0, 0)
    proud.set("head", -6, 0, 6)
    proud.face = {"grin": 1.0, "smirk_L": 0.4}
    c.key(1.9, proud)
    c.key(T, L.REST)

    def kit_solve(t, p, skel, T=T):
        # right hand: behind his back (0.15-0.6), out with the torch (0.75), held up at the chest (1.2-2.0)
        back = pulse(t, 0.12, 0.35, 0.18, 0.25)
        show = pulse(t, 0.85, 0.3, 0.9, 0.35)
        if back > 0.01:
            body.hand_to(p, -1, RW[-1].lerp(V(-0.12, 0.26, 0.86), back), elbow=(0.5, 0.6, -0.4))
        if show > 0.01:
            cur = L.wrist_of(body, p, -1)
            body.hand_to(p, -1, cur.lerp(V(-0.26, -0.36, 1.0), show), elbow=(0.6, 0.2, -0.5),
                         hand_rot=L.hand_world((0.2, -1, 0.5), (1, 0, 0)) if show > 0.5 else None)
        L.fist(p, -1, smooth(0.5, TORCH, t))
        # left hand: up behind his head and down onto his crown with the hat (1.0-1.6)
        hat = pulse(t, 0.95, 0.35, 0.25, 0.4)
        if hat > 0.01:
            tgt = V(0.3, -0.02, 1.48 + 0.04 * pulse(t, 1.25, 0.1, 0.0, 0.2))
            body.hand_to(p, 1, RW[1].lerp(tgt, hat), elbow=(0.7, 0.1, -0.2),
                         hand_rot=L.hand_world((-0.3, 0, 1), (-1, 0, 0)) if hat > 0.5 else None)
            L.open_hand(p, 1, 8 * hat)
        bump = pulse(t, HAT, 0.04, 0.02, 0.2)
        L.hips(body, p, dz=-0.03 * bump)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(kit_solve)

    def kit_face(t, T=T):
        p = Pose()
        bump = pulse(t, HAT, 0.04, 0.05, 0.25)
        p = p + look((10 * bump, 0))
        L.squint(p, 0.7 * bump)
        brows(p, 1.4 * pulse(t, 1.75, 0.1, 0.3, 0.2), 1.4 * pulse(t, 1.75, 0.1, 0.3, 0.2), 1.0)
        L.horns(p, x=-8 * L.ring(t, HAT, 18, 6), z=4 * L.ring(t, HAT, 16, 6))
        return p

    c.layer(kit_face)
    out.append(c)

    # ---- lift ----------------------------------------------------------------------------------------
    duck = L.REST.copy()
    duck.face = {"grin": 0.6, "smirk_L": 0.6}
    T = 1.7
    c = Clip(f"{NAME}/lift", T)
    c.key(0.0, L.REST)
    c.key(T, duck)

    def lift_solve(t, p, skel, T=T):
        grab = pulse(t, 0.0, 0.3, 0.0, 0.01)
        heave = smooth(LIFT, LIFT + 0.6, t)
        low = smooth(1.15, T, t)
        squat = pulse(t, 0.05, 0.3, 0.25, 0.35)
        crouched(p, max(0.35 * squat, low))
        for sg in (1, -1):
            under = V(sg * 0.1, -PANEL_GAP + 0.06, 0.22)
            over = V(sg * 0.12, -0.18, 1.42)
            tgt = under.lerp(over, heave)
            k = smooth(0.0, 0.3, t) * (1 - smooth(1.2, 1.55, t))
            if k > 0.01:
                body.hand_to(p, sg, RW[sg].lerp(tgt, k), elbow=(0.5, 0.3, -0.5),
                             hand_rot=L.hand_world((0, -0.4, 1), (0, 0, 1)) if k > 0.5 else None)
            L.open_hand(p, sg, 8 * k)
        if low > 0.01:
            torch(p, low)
        body.plant(p, 1, knee_out=0.08 * max(squat, low))
        body.plant(p, -1, knee_out=0.08 * max(squat, low))
        return p

    def torch(p, k):
        """The flashlight held out in front, low, lighting the way."""
        body.hand_to(p, -1, RW[-1].lerp(V(-0.18, -0.42, 0.62), k), elbow=(0.5, 0.2, -0.5),
                     hand_rot=L.hand_world((0, -1, -0.1), (1, 0, 0)) if k > 0.5 else None)
        L.fist(p, -1, 1.0)

    c.solve(lift_solve)

    def lift_face(t, T=T):
        p = Pose()
        strain = pulse(t, LIFT, 0.15, 0.45, 0.2)
        p.face.update({"grin": 1 - strain, "grit": strain})
        brows(p, -1.0 * strain, -0.4 * strain, 0.4 * strain)
        p = p + look((10 * strain, 0))
        L.horns(p, x=-6 * strain)
        return p

    c.layer(lift_face)
    out.append(c)

    # ---- duck (loop) ---------------------------------------------------------------------------------
    T = DUCK_PERIOD
    c = L.looped(f"{NAME}/duck", T)
    c.key(0.0, duck)

    def duck_solve(t, p, skel, T=T):
        u = t / T
        crouched(p, 1.0, bob=0.02 * math.cos(math.tau * 2 * (u - 0.1)))
        L.hips(body, p, roll=7 * math.sin(math.tau * u), yaw=-6 * math.sin(math.tau * u))
        torch(p, 1.0)
        p.side("upper_arm", 1, x=-20 * math.sin(math.tau * u), add=True)
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, DUCK_STRIDE, DUCK_STANCE, ph, height=0.07, toe_off=16, heel_strike=-6)
            body.plant(p, sg, pos=(0, y, 0), lift=lift, roll=roll, knee_out=0.1)
        return p

    c.solve(duck_solve)
    c.layer(lambda t, T=T: L.horns(Pose(), x=4 * math.cos(math.tau * 2 * t / T), z=2 * math.sin(math.tau * t / T)))
    out.append(c)

    # ---- emerge --------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/emerge", T)
    c.key(0.0, duck)
    wary = L.REST.copy()
    wary.face = {"grin": 0.0, "flat": 0.6, "oh": 0.3}
    c.key(0.5, wary)
    c.key(1.7, wary, "linear")
    c.key(T, L.REST)

    def emerge_solve(t, p, skel, T=T):
        k = 1 - smooth(0.0, 0.4, t)
        pop = pulse(t, 0.38, 0.06, 0.04, 0.25)
        crouched(p, k)
        L.hips(body, p, dz=0.05 * pop)
        hold = 1 - smooth(1.6, T, t)
        torch(p, max(hold, 0.0) * 0.7 + 0.0)
        body.plant(p, 1, roll=10 * pop)
        body.plant(p, -1, roll=10 * pop)
        return p

    c.solve(emerge_solve)

    def emerge_face(t, T=T):
        p = Pose()
        up = pulse(t, 0.55, 0.25, 0.9, 0.35)
        p = p + look((34 * up, 0), head=(-6 * up, 0, 0))
        brows(p, 1.8 * up, 2.0 * up, 1.2 * up)
        L.horns(p, x=10 * L.ring(t, 0.4, 16, 5))
        return p

    c.layer(emerge_face)
    c.layer(L.blinks([1.0, 1.2]))
    out.append(c)

    # ---- sneeze --------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/sneeze", T)
    c.key(0.0, L.REST)

    def sneeze_solve(t, p, skel, T=T):
        wind = smooth(0.05, SNEEZE - 0.05, t) * (1 - smooth(SNEEZE - 0.05, SNEEZE, t))
        choo = pulse(t, SNEEZE, 0.05, 0.08, 0.45)
        L.hips(body, p, dy=0.04 * wind - 0.05 * choo, pitch=-8 * wind + 18 * choo, dz=-0.03 * choo)
        p.add("chest", -10 * wind + 16 * choo, 0, 0)
        p.add("head", -16 * wind + 18 * choo, 0, 0)
        if wind + choo > 0.01:
            p.both("upper_arm", x=-10 * wind + 10 * choo, z=10 * wind, add=True)
        body.plant(p, 1, roll=-10 * wind)
        body.plant(p, -1, roll=-10 * wind)
        return p

    c.solve(sneeze_solve)

    def sneeze_face(t, T=T):
        p = Pose()
        wind = smooth(0.05, SNEEZE - 0.05, t) * (1 - smooth(SNEEZE - 0.05, SNEEZE, t))
        choo = pulse(t, SNEEZE, 0.05, 0.1, 0.4)
        sniff = pulse(t, 1.5, 0.08, 0.1, 0.15)
        p.face.update({"grin": 0.0, "open": 0.8 * wind, "grit": choo, "flat": sniff})
        L.squint(p, 0.6 * wind + 1.0 * choo)
        brows(p, 1.4 * wind - 1.0 * choo, 1.2 * wind, 0.6 * wind)
        L.horns(p, x=-8 * wind + 20 * L.ring(t, SNEEZE, 18, 4), z=6 * L.ring(t, SNEEZE, 15, 4))
        L.ears(p, tilt=-10 * wind)
        return p

    c.layer(sneeze_face)
    out.append(c)
    return {"zip": out}
