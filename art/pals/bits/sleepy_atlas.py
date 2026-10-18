"""The sleepy atlas: in an idle moment Archie takes out the Atlas Core, hugs it like a teddy bear, sits down
and nods off. Its lights pulse gently and a little hologram of him floats above it, holding forth in his sleep.
Zip tiptoes in with a marker and, very carefully, draws a mustache on it; tiptoes off, shaking with silent
laughter. Archie stirs, gets up, docks the Core and wanders off, none the wiser.

FORMATION (metres from Archie's root, x to his left -- the page's right): Archie at (0, 0), Zip at ZIP, both
facing the reader. The Core rides Archie's left palm (HOLD, bits/_corekit.py) until HUG_AT, then his `chest`
bone (the page fixes it where it is then: HUG, in front of his chest) until DOCK_AT in `wake`. The hologram
(holo-archie, HOLO_SCALE of his size) floats at HOLO_AT from the Core; seated, the Core is at SEATED_CORE, so
the hologram's top lip is at LIP (both in his frame) -- where Zip's marker goes.

    archie  sleepy-atlas/take      REST -> HOLD (the Core to his palm at _corekit.GRAB)
            sleepy-atlas/hug-sit   HOLD -> SLEEP: the Core to his chest in both arms (HUG_AT), a yawn, down
                                   onto the floor, the head drooping, the eyes closing
            sleepy-atlas/doze      SLEEP, looping: slow breaths, a nod, a contented smile
            sleepy-atlas/wake      SLEEP -> REST: a stir, a stretch, up, the Core back in its dock (DOCK_AT)
    zip     sleepy-atlas/draw      REST -> REST: up on tiptoe, the marker to the hologram's lip, two careful
                                   strokes (DRAW: the page plays the mustache's own `draw`), back down, a hand
                                   over his mouth, shoulders shaking
            (everyday: sneak)
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, look
from kit.anim import Clip, Pose, ease, pulse, smooth
from . import _corekit as K

NAME = "sleepy-atlas"
CAST = ("archie", "zip")
ZIP = (0.85, -0.3)              # Zip's root, from Archie's
HUG_AT = 0.7                    # hug-sit: the Core leaves his palm for his chest
DOCK_AT = 2.0                   # wake: ... and goes back in its dock
HUG = (0.0, -0.42, 1.44)        # the Core, hugged, standing (his frame)
SEATED_CORE = (-0.029, -0.219, 0.741)  # ... and seated (measured: HUG carried by `chest` into SLEEP)
HOLO_SCALE = 0.3                # the hologram: his size, scaled
HOLO_AT = (0.42, 0.15)          # its feet from the Core's centre: out to his left, beside his head, and up
LIP = (0.391, -0.351, 1.509)    # its top lip, seated: SEATED_CORE + HOLO_AT + the big-headed bootleg's upper lip
                                # (2.06 up, 0.44 forward: props_holo.holo_archie), scaled
DRAW = (1.15, 2.05)             # draw: the marker on the lip


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
    REST, hips, hand_world, open_hand = L.REST, L.hips, L.hand_world, L.open_hand
    skel = body.skel
    rw = {sg: K.rest_wrist(body, sg) for sg in (1, -1)}
    out = [K.take(body, f"{NAME}/take")]

    # the Core in the chest's own frame, as it is when he hugs it: what the hands hold on to, seated or not
    hug_pose = K.HOLD.copy()
    chest0 = skel.fk(hug_pose, "chest")["chest"]
    in_chest = chest0.inverted() @ V(*HUG)
    palm_up = hand_world((-0.35, -0.9, 0.05), (0, 0, 1))
    over = hand_world((0.95, -0.2, -0.2), (0, 0.6, -0.8))       # the right forearm across the top of it

    def hug(p, k, sit):
        """Both arms round the Core (k of the way from where they are), the body `sit` of the way down."""
        L.seated(p, body, sit)
        core = skel.fk(p, "chest")["chest"] @ in_chest
        # the left palm stays under it (it carried it there); the right arm comes round it, k of the way
        body.hand_to(p, 1, core + V(0.06, 0.1, -0.14), elbow=(0.55, 0.35, -0.5), hand_rot=palm_up)
        p.fingers(1, 30, spread=6, thumb=20)
        if k > 0.01:
            body.hand_to(p, -1, rw[-1].lerp(core + V(-0.12, 0.08, 0.06), k), elbow=(0.5, 0.35, -0.6),
                         hand_rot=over if k > 0.5 else None)
            p.fingers(-1, 26 * k + 18 * (1 - k), spread=6, thumb=16)
        f = L.sit_feet(sit)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])

    def sleepy(p, a, t=0.0):
        """The head drooping (a of the way) and lolling with the breath."""
        b = 0.5 + 0.5 * math.sin(math.tau * t / 4.0)
        p.add("head", 22 * a + 3 * a * b, 0, 10 * a)
        p.add("neck", 6 * a, 0, 3 * a)

    def asleep_face(a, smile=1.0):
        p = Pose()
        p.both("lid_up", x=-48 * a)
        p.both("lid_lo", x=36 * a)
        p.face.update({"grin": -a, "smile": smile * a})
        return p

    # ---- hug-sit -------------------------------------------------------------------------------------
    T = 3.2
    c = Clip(f"{NAME}/hug-sit", T)
    c.key(0.0, K.HOLD)
    snug = REST.copy()
    snug.set("head", 14, 6, 4)
    snug.face = {"smile": 0.8}
    yawn = snug.copy()
    yawn.face = {"open": 1.0, "wide": 0.5}
    c.key(0.6, snug, "inout")
    c.key(1.0, yawn, "inout")
    c.key(1.5, snug, "inout")
    c.key(T, snug, "linear")

    def hugsit_solve(t, p, skel_):
        lift = smooth(0.1, HUG_AT, t)                             # the Core up to his chest
        if t < HUG_AT:
            K.held(body, p, 1.0, K.HOLD_WRIST.lerp(V(*HUG) + V(0.05, 0.15, -0.16), lift))
            body.plant(p, 1)
            body.plant(p, -1)
        else:
            hug(p, smooth(HUG_AT, HUG_AT + 0.35, t), ease("inout", smooth(1.5, 2.8, t)))
        sleepy(p, smooth(2.2, T, t), t)
        return p

    c.solve(hugsit_solve)
    c.layer(lambda t: asleep_face(smooth(2.3, T, t)) + K.eyes_on_core(1 - smooth(0.4, 0.9, t)))
    c.layer(blink_layer([1.9]))
    out.append(c)

    # ---- doze ----------------------------------------------------------------------------------------
    c = K.loop_clip(f"{NAME}/doze", 4.0)
    c.key(0.0, snug)

    def doze_solve(t, p, skel_):
        hug(p, 1.0, 1.0)
        sleepy(p, 1.0, t)
        return p

    c.solve(doze_solve)
    c.layer(lambda t: asleep_face(1.0))
    c.layer(breathe(4.0, 1.8))
    out.append(c)

    # ---- wake ----------------------------------------------------------------------------------------
    T = 3.4
    c = Clip(f"{NAME}/wake", T)
    c.key(0.0, snug)
    stretch = REST.copy()
    stretch.set("head", -16, 0, 0)
    stretch.set("chest", -10, 0, 0)
    stretch.face = {"open": 0.8}
    c.key(0.6, snug, "linear")
    c.key(1.1, stretch, "inout")
    c.key(1.5, snug, "inout")
    c.key(T, REST, "inout")
    dock_w = K.DOCK_HAND

    def wake_solve(t, p, skel_):
        up = 1 - ease("inout", smooth(1.2, 2.4, t))
        if t < 0.3:
            hug(p, 1.0, up)
        else:                                                     # the right arm off it, a stretch, and up
            L.seated(p, body, up)
            core = skel.fk(p, "chest")["chest"] @ in_chest
            k = smooth(1.5, DOCK_AT, t)
            if t < DOCK_AT:                                       # the Core to its dock ...
                tgt = (core + V(0.06, 0.1, -0.14)).lerp(dock_w, k)
            else:                                                 # ... and the hand away
                tgt = dock_w.lerp(rw[1], smooth(DOCK_AT, T - 0.1, t))
            hr = (K.PALM_IN if k > 0.6 else palm_up) if t < DOCK_AT + 0.6 else None
            body.hand_to(p, 1, tgt, elbow=(0.55, 0.35, -0.5), hand_rot=hr)
            p.fingers(1, 30 * (1 - smooth(DOCK_AT, T, t)) + 18 * smooth(DOCK_AT, T, t), spread=5, thumb=16)
            s = pulse(t, 0.4, 0.4, 0.3, 0.5)                      # the right arm up in a stretch
            if s > 0.01:
                body.hand_to(p, -1, rw[-1].lerp(V(-0.4, 0.0, 2.35), s), elbow=(0.3, 0.2, 0.2))
                open_hand(p, -1, 10 * s)
            f = L.sit_feet(up)
            body.plant(p, 1, **f[1])
            body.plant(p, -1, **f[-1])
        sleepy(p, 1 - smooth(0.2, 0.9, t), t)
        return p

    c.solve(wake_solve)
    c.layer(lambda t: asleep_face(1 - smooth(0.3, 1.0, t), 1.0) + K.eyes_on_core(pulse(t, 1.4, 0.3, 0.4, 0.4)))
    c.layer(blink_layer([1.15, 2.6]))
    out.append(c)
    return out


# --------------------------------------------------------------------------------------------- zip
def zip_(body):
    L = body.lib
    REST, hips, hand_world, open_hand = L.REST, L.hips, L.hand_world, L.open_hand
    rw = L.rest_wrists(body)
    lip = V(*LIP) - V(ZIP[0], ZIP[1], 0)                        # the hologram's lip, in his frame
    # the marker's nib from his wrist: his grip_R is 0.102 along the fingers and 0.055 out of the palm, and the
    # marker (held at its middle) reaches 0.105 on along the fingers
    along, out_ = 0.207, 0.055
    T = 3.6
    c = Clip(f"{NAME}/draw", T, frames=108)
    c.key(0.0, REST)
    care = REST.copy()
    care.set("head", -8, -18, 4)
    care.set("chest", 4, -10, 0)
    care.face = {"smirk_L": 0.8, "grin": 0.4}
    giggle = REST.copy()
    giggle.set("head", 10, 0, 0)
    giggle.set("chest", 10, 0, 0)
    giggle.face = {"grin": 1.0}
    c.key(0.5, care, "inout")
    c.key(DRAW[1] + 0.2, care, "linear")
    c.key(2.6, giggle, "inout")
    c.key(T - 0.3, giggle, "linear")
    c.key(T, REST, "inout")
    fingers = V(-0.5, -0.35, 0.8).normalized()                 # the marker pointing up and across at it

    def solve(t, p, skel):
        reach = pulse(t, 0.3, 0.6, DRAW[1] - 0.9 + 0.1, 0.4)
        toes = pulse(t, 0.3, 0.5, DRAW[1] - 0.8, 0.4)
        hips(body, p, dz=0.05 * toes, dx=-0.08 * reach, roll=6 * reach)
        stroke = smooth(DRAW[0], DRAW[1], t)
        x = 0.06 * math.sin(math.tau * stroke)                  # out to one side and the other
        tip = lip + V(x, -0.01, -0.01 * abs(x) / 0.06)
        hr = hand_world(fingers, (0.6, 0.0, 0.8))
        wrist = tip - fingers * along - hr.col[2] * out_
        body.hand_to(p, -1, rw[-1].lerp(wrist, reach), elbow=(0.5, 0.2, -0.5), hand_rot=hr if reach > 0.5 else None)
        L.fist(p, -1, 0.9)
        # the giggle: his left hand over his mouth, shoulders going
        g = pulse(t, 2.4, 0.25, 0.7, 0.3)
        if g > 0.01:
            body.hand_to(p, 1, rw[1].lerp(V(0.06, -0.3, 1.33), g), elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((-0.2, 0, 1), (0, 1, 0)) if g > 0.5 else None)
            open_hand(p, 1, 4 * g)
            p.both("shoulder", z=4 * g * math.sin(math.tau * 6 * t), add=True)
        body.plant(p, 1, roll=24 * toes)
        body.plant(p, -1, roll=24 * toes)
        return p

    c.solve(solve)
    c.layer(lambda t: look((14 * pulse(t, 0.4, 0.3, 1.5, 0.3), -14 * pulse(t, 0.4, 0.3, 1.5, 0.3))))
    c.layer(lambda t: L.squint(Pose(), pulse(t, 2.4, 0.2, 0.8, 0.3)))
    return [c]
