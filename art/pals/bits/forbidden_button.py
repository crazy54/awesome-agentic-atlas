"""The forbidden button: a pedestal rises out of the floor with a big red button on it: DO NOT PRESS. Zip,
delighted, lunges for it -- and Archie, arriving, holds him back by the dome at arm's length, Zip
scrabbling, a finger short. "It says DO NOT PRESS." Zip sulks off, back turned; Archie gives the reader a
responsible nod. Then, alone with it: a look at the button, a long look at the reader, a glance at Zip
(back still turned) -- and he presses it. Confetti, all over Archie, only Archie. Zip spins round and sells
him out: "HE PRESSED IT!" "It was very tempting." And Zip, with a remote from behind his back, clicks it:
the confetti goes off over Archie again.

FORMATION (metres across the page from the pedestal, PEDESTAL_SCALE times the do-not-press prop, its
button BUTTON metres up; everyone on the window's floor):

    zip      ZIP_REACH (reaching for it, facing the reader); restrained by archie at ZIP_REACH + HOLD_GAP
    archie   ARCHIE_PRESS (pressing it, facing the reader, it on his right)
    zip      sulking ZIP_SULK past Archie, his back turned; then facing the reader, clicking a remote at it

Archie's pieces (clips/archie_base.py):

    forbidden-button/restrain    REST -> HOLDING: his right hand out onto Zip's dome (on his right, HOLD_GAP
                                 away), landing at GRIP s
    forbidden-button/holding     HOLDING, looping: holding him off, unbothered, eyes on the reader
    forbidden-button/release     HOLDING -> REST
    forbidden-button/nod         REST -> REST: hands behind his back, chin up, eyes shut, a responsible nod
    forbidden-button/tempt       REST -> PRESSED: a look down at the button, a long look at the reader, a
                                 glance over his left shoulder at Zip, and the jab (PRESS s): ends with his
                                 finger on it
    forbidden-button/confettied  PRESSED -> REST: the burst (BURST s): a flinch, frozen, the hand off it
    forbidden-button/deadpan     REST -> REST: the second burst: no flinch at all, a flat look, a slow blink

Zip's (clips/zip_base.py):

    forbidden-button/delight     REST -> REST: it rises on his right: a double take, a grin, hands rubbed
    forbidden-button/reach       REST -> STRAIN: the lunge for it
    forbidden-button/strain      STRAIN, looping: held back by the dome: feet scrabbling, the right hand
                                 grabbing at the air a finger short of the button, the left arm windmilling
    forbidden-button/deflate     STRAIN -> FOLDED: a huff, the arms folded
    forbidden-button/sulk        FOLDED, looping: head down, a foot tapping (the page turns his back)
    forbidden-button/snitch      FOLDED -> REST: arms flung out of the fold, pointing at Archie on his right,
                                 shouting at the reader, bouncing
    forbidden-button/click       REST -> REST: the right hand behind his back and out with the remote (grip_R
                                 from REMOTE s), aimed at the button on his right, a click (CLICK s), a snicker
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, breathe, brows, look
from kit.anim import Clip, Pose, pulse, smooth
from . import _corekit as K

NAME = "forbidden-button"
CAST = ("archie", "zip")
PEDESTAL_SCALE = 1.35
BUTTON = 0.99 * PEDESTAL_SCALE                 # the button's top, metres up
ZIP_REACH, HOLD_GAP = 0.8, 0.95
ARCHIE_PRESS, ZIP_SULK = 0.65, 0.9
GRIP = 0.45                                     # restrain: his hand on Zip's dome
PRESS = 3.6                                     # tempt: the button goes down
BURST = 0.05                                    # confettied: the confetti goes off over him
REMOTE, CLICK = 0.35, 0.8                       # click: the remote in his hand; the button goes down


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


# ============================================================================================== Archie
def archie_clips(body):
    L = body.lib
    n = lambda piece: f"{NAME}/{piece}"           # noqa: E731
    RW = {sg: K.rest_wrist(body, sg) for sg in (1, -1)}
    out = []

    def lids(p, k):
        p.both("lid_up", x=-46 * k, add=True)
        p.both("lid_lo", x=40 * k, add=True)

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    # his right wrist on Zip's dome (Zip's dome top 1.75 m, HOLD_GAP to his right), palm down
    DOME_W = V(-HOLD_GAP + 0.08, 0.02, 1.84)
    dome_rot = L.hand_world((-0.55, -0.8, -0.1), (0, 0, -1))
    HIP_W = V(0.34, -0.06, 1.12)                 # the left fist on his hip
    hip_rot = L.hand_world((-0.4, -0.2, -1), (-1, 0, 0))
    holding = L.REST.copy()
    holding.set("head", 8, -14, 0)
    holding.set("chest", 0, -6, 0)
    holding.face = {"grin": 0.6, "smirk_R": 0.6}

    def hold_arms(p, k=1.0, jiggle=0.0):
        body.hand_to(p, -1, RW[-1].lerp(DOME_W + V(0.01 * jiggle, 0, 0.006 * jiggle), k), elbow=(0.5, 0.2, -0.3),
                     hand_rot=dome_rot if k > 0.5 else None)
        L.open_hand(p, -1, 6)
        body.hand_to(p, 1, RW[1].lerp(HIP_W, k), elbow=(0.6, 0.1, -0.2), hand_rot=hip_rot if k > 0.5 else None)
        L.fist(p, 1, 0.7 * k)
        L.hips(body, p, dx=0.03 * k, roll=3 * k)

    # ---- restrain ------------------------------------------------------------------------------------
    T = 1.0
    c = Clip(n("restrain"), T)
    c.key(0.0, L.REST)
    c.key(T, holding, "inout")

    def restrain_solve(t, p, skel, T=T):
        hold_arms(p, smooth(0.0, GRIP, t))
        stand(p)
        return p

    c.solve(restrain_solve)
    c.layer(lambda t, T=T: look((-20 * smooth(0.0, 0.4, t), -24 * smooth(0.0, 0.4, t))))
    out.append(c)

    # ---- holding (loop) ------------------------------------------------------------------------------
    T = 2.0
    c = K.loop_clip(n("holding"), T)
    c.key(0.0, holding)

    def holding_solve(t, p, skel, T=T):
        hold_arms(p, 1.0, math.sin(math.tau * 5 * t / T))
        stand(p)
        return p

    c.solve(holding_solve)

    def holding_face(t, T=T):
        u = t / T
        p = look((2, 4 * math.sin(math.tau * u)), head=(0, 0, 14))       # at the reader, over the head turn
        lids(p, 0.15)
        brows(p, 0.0, 0.8, 1.2, side=1)
        return p

    c.layer(holding_face)
    c.layer(blink_layer([1.2]))
    out.append(c)

    # ---- release -------------------------------------------------------------------------------------
    T = 0.8
    c = Clip(n("release"), T)
    c.key(0.0, holding)
    c.key(T, L.REST, "inout")

    def release_solve(t, p, skel, T=T):
        hold_arms(p, 1 - smooth(0.0, T, t))
        stand(p)
        return p

    c.solve(release_solve)
    out.append(c)

    # ---- nod -----------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(n("nod"), T)
    c.key(0.0, L.REST)
    proud = L.REST.copy()
    proud.set("head", -10, 0, 0)
    proud.set("chest", -6, 0, 0)
    proud.face = {"grin": 0.8}
    nod = proud.copy()
    nod.set("head", 14, 0, 0)
    c.key(0.45, proud, "inout")
    c.key(1.0, proud, "linear")
    c.key(1.3, nod, "inout")
    c.key(1.65, proud, "inout")
    c.key(T, L.REST, "inout")
    BACK_W = {1: V(0.12, 0.28, 1.08), -1: V(-0.12, 0.28, 1.1)}       # hands clasped behind his back

    def nod_solve(t, p, skel, T=T):
        k = pulse(t, 0.0, 0.45, T - 0.85, 0.4)
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(BACK_W[sg], k), elbow=(0.5, 0.5, -0.4),
                         hand_rot=L.hand_world((-sg, 0.2, -0.3), (0, 1, 0)) if k > 0.6 else None)
            L.fist(p, sg, 0.5 * k)
        L.hips(body, p, dy=0.02 * k, pitch=-2 * k)
        stand(p)
        return p

    c.solve(nod_solve)

    def nod_face(t, T=T):
        p = Pose()
        shut = pulse(t, 0.5, 0.2, 0.9, 0.3)
        p.both("lid_up", x=-60 * shut)
        p.both("lid_lo", x=30 * shut)
        brows(p, 0.6 * shut, 1.0 * shut, 0.8 * shut)
        return p

    c.layer(nod_face)
    out.append(c)

    # ---- tempt ---------------------------------------------------------------------------------------
    T = 4.2
    c = Clip(n("tempt"), T)
    c.key(0.0, L.REST)
    at_it = L.REST.copy()
    at_it.set("head", 18, -16, 0)
    at_it.face = {"grin": 0.0, "oh": 0.2}
    at_you = L.REST.copy()
    at_you.set("head", 2, -4, 4)
    at_you.face = {"grin": 0.3, "smirk_L": 0.6}
    at_zip = L.REST.copy()
    at_zip.set("head", 0, 40, 0)
    at_zip.set("chest", 0, 10, 0)
    at_zip.face = {"grin": 0.0, "flat": 0.4}
    pressed = L.REST.copy()
    pressed.set("head", 14, -18, 0)
    pressed.set("chest", 6, -8, 0)
    pressed.face = {"grin": 0.0, "wide": 0.5, "oh": 0.4}
    c.key(0.4, at_it, "inout")
    c.key(1.2, at_it, "linear")
    c.key(1.55, at_you, "inout")
    c.key(2.5, at_you, "linear")
    c.key(2.8, at_zip, "inout")
    c.key(3.15, at_zip, "linear")
    c.key(3.4, at_you, "inout")
    c.key(PRESS, pressed, "snap")
    c.key(T, pressed, "linear")
    TIP = V(-ARCHIE_PRESS, -0.05, BUTTON)        # the button, in his frame
    jab = V(-0.5, 0.0, -0.86)                    # his finger pointing down onto it
    PRESS_W = TIP - jab * 0.2
    press_rot = L.hand_world(jab, (-0.3, -1, 0))

    def tempt_solve(t, p, skel, T=T):
        k = smooth(PRESS - 0.2, PRESS, t)
        hover = pulse(t, 1.2, 0.3, 1.1, 0.3) * 0.25          # the hand drifting towards it as he looks at you
        body.hand_to(p, -1, RW[-1].lerp(PRESS_W + V(0, 0, 0.12 * (1 - k)), max(k, hover)), elbow=(0.5, 0.2, -0.5),
                     hand_rot=press_rot if max(k, hover) > 0.2 else None)
        if max(k, hover) > 0.2:
            L.point(p, -1)
        L.hips(body, p, dx=-0.04 * k, roll=4 * k, pitch=4 * k)
        stand(p)
        return p

    c.solve(tempt_solve)

    def tempt_face(t, T=T):
        it = pulse(t, 0.2, 0.3, 0.8, 0.3)
        you = pulse(t, 1.3, 0.3, 0.95, 0.25) + pulse(t, 3.25, 0.15, 0.1, 0.15)
        z = pulse(t, 2.6, 0.25, 0.4, 0.2)
        jabbed = smooth(PRESS - 0.1, PRESS, t)
        p = look((-24 * it - 20 * jabbed, -26 * it + 30 * z - 20 * jabbed))
        lids(p, 0.3 * you)
        brows(p, -0.4 * you, 0.6 * you, 1.6 * you, side=1)
        brows(p, -0.8 * you, -0.4 * you, 0.2 * you, side=-1)
        return p

    c.layer(tempt_face)
    c.layer(blink_layer([0.9, 2.55]))
    out.append(c)

    # ---- confettied ----------------------------------------------------------------------------------
    T = 2.6
    c = Clip(n("confettied"), T)
    c.key(0.0, pressed)
    flinch = pressed.copy()
    flinch.set("head", 20, -10, 0)
    flinch.face = {"grit": 0.8, "grin": 0.0}
    frozen = L.REST.copy()
    frozen.set("head", 4, 0, 0)
    frozen.face = {"flat": 0.9, "grin": 0.0}
    c.key(BURST + 0.12, flinch, "snap")
    c.key(1.2, flinch, "linear")
    c.key(1.9, frozen, "inout")
    c.key(T, frozen, "linear")

    def confettied_solve(t, p, skel, T=T):
        up = pulse(t, BURST, 0.1, 1.0, 0.5)
        p.both("shoulder", z=14 * up)
        k = 1 - smooth(1.2, 2.0, t)
        body.hand_to(p, -1, RW[-1].lerp(PRESS_W + V(0.02, 0, 0.04 * up), k), elbow=(0.5, 0.2, -0.5),
                     hand_rot=press_rot if k > 0.5 else None)
        if k > 0.5:
            L.point(p, -1)
        L.hips(body, p, dx=-0.04 * k, roll=4 * k, pitch=4 * k, dz=-0.03 * up)
        stand(p)
        return p

    c.solve(confettied_solve)

    def confettied_face(t, T=T):
        p = Pose()
        sq = pulse(t, BURST, 0.08, 1.0, 0.4)
        p.both("lid_up", x=-70 * sq)
        p.both("lid_lo", x=40 * sq)
        p.add("crest_2", 14 * sq, 0, 0)
        p.add("crest_3", 18 * sq, 0, 0)
        return p + look((0, 0))

    c.layer(confettied_face)
    out.append(c)

    # ---- deadpan -------------------------------------------------------------------------------------
    T = 2.4
    c = Clip(n("deadpan"), T)
    c.key(0.0, L.REST)
    flat = L.REST.copy()
    flat.set("head", 2, 0, -3)
    flat.face = {"flat": 1.0, "grin": 0.0}
    c.key(0.3, flat, "inout")
    c.key(T - 0.3, flat, "linear")
    c.key(T, L.REST, "inout")

    def deadpan_solve(t, p, skel, T=T):
        p.both("shoulder", z=-6 * pulse(t, 0.4, 0.4, T - 1.2, 0.4))
        stand(p)
        return p

    c.solve(deadpan_solve)

    def deadpan_face(t, T=T):
        p = Pose()
        b = pulse(t, 1.0, 0.3, 0.25, 0.4)
        p.both("lid_up", x=-46 * b - 12 * (1 - b))
        p.both("lid_lo", x=20 * b)
        return p + look((0, 0))

    c.layer(deadpan_face)
    out.append(c)
    return out


# ================================================================================================= Zip
def zip_clips(body):
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    # the button on his right, ZIP_REACH away, BUTTON up: the right hand a finger short of it
    REACH_W = V(-ZIP_REACH + 0.37, -0.12, BUTTON + 0.03)
    reach_rot = L.hand_world((-1, -0.1, 0.05), (0, -0.2, -1))
    strain = L.REST.copy()
    strain.face = {"grin": 0.0, "grit": 1.0}
    folded = L.REST.copy()
    folded.set("head", 14, 0, -6)
    folded.set("chest", -2, 0, 0)
    folded.face = {"grin": 0.0, "flat": 0.6}
    FOLD_W = {1: V(-0.13, -0.27, 1.07), -1: V(0.14, -0.24, 1.02)}   # zip_base.fold_arms
    fold_rot = {1: L.hand_world((-1, 0.1, 0.1), (0, -0.2, -1)), -1: L.hand_world((1, 0.1, -0.1), (0, -0.3, 1))}

    def arms_folded(p, k=1.0):
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(FOLD_W[sg], k), elbow=(0.55, 0.15, -0.35),
                         hand_rot=fold_rot[sg] if k > 0.5 else None)
            L.fist(p, sg, 0.6 * k)

    # ---- delight -------------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/delight", T)
    c.key(0.0, L.REST)

    def delight_solve(t, p, skel, T=T):
        jolt = pulse(t, 0.15, 0.06, 0.1, 0.3)
        L.hips(body, p, dz=0.04 * jolt, roll=-4 * jolt)
        rub = pulse(t, 1.0, 0.2, 0.8, 0.3)
        if rub > 0.01:
            r = 0.02 * math.sin(math.tau * 5 * t)
            for sg in (1, -1):
                body.hand_to(p, sg, RW[sg].lerp(V(sg * (0.06 + r * sg), -0.32, 0.98), rub), elbow=(0.5, 0.3, -0.5),
                             hand_rot=L.hand_world((-sg, -0.3, 0.3), (0, 0, 1) if sg > 0 else (0, 0, -1)) if rub > 0.5 else None)
                L.open_hand(p, sg, 4)
        body.plant(p, 1, lift=0.04 * jolt)
        body.plant(p, -1, lift=0.04 * jolt)
        return p

    c.solve(delight_solve)

    def delight_face(t, T=T):
        at = pulse(t, 0.1, 0.12, 1.6, 0.3)
        wide = pulse(t, 0.15, 0.06, 0.4, 0.3)
        grin = smooth(0.6, 1.1, t)
        p = look((-14 * at, -30 * at), head=(6 * at, 0, -14 * at))
        p.face.update({"wide": 0.8 * wide, "grin": 0.4 + 0.6 * grin, "smirk_L": 0.8 * grin})
        brows(p, 2.0 * wide, 2.0 * wide, 1.4 * wide)
        brows(p, -1.0 * grin, -0.4 * grin, 0.4 * grin, side=-1)
        L.squint(p, 0.4 * grin)
        L.horns(p, x=12 * L.ring(t, 0.15, 20, 5))
        return p

    c.layer(delight_face)
    out.append(c)

    def reaching(p, k=1.0, grab=0.0, mill=0.0, t=0.0):
        L.hips(body, p, dx=-0.02 * k, roll=4 * k, yaw=-14 * k, pitch=4 * k)    # his dome stays under Archie's hand
        p.add("chest", 4 * k, -8 * k, 4 * k)
        body.hand_to(p, -1, RW[-1].lerp(REACH_W + V(-0.03 * grab, 0, 0.02 * grab), k), elbow=(0.3, 0.2, -0.4),
                     hand_rot=reach_rot if k > 0.5 else None)
        p.fingers(-1, 10 + 60 * max(0.0, grab), spread=10, thumb=10)
        if mill:
            a = math.tau * 2.5 * t
            body.hand_to(p, 1, V(0.42 + 0.12 * math.cos(a), -0.1, 1.15 + 0.2 * math.sin(a)), elbow=(0.6, 0.0, -0.3))
            L.open_hand(p, 1, 12)

    # ---- reach ---------------------------------------------------------------------------------------
    T = 0.8
    c = Clip(f"{NAME}/reach", T)
    c.key(0.0, L.REST)
    c.key(T, strain, "inout")

    def reach_solve(t, p, skel, T=T):
        reaching(p, smooth(0.0, 0.45, t))
        body.plant(p, 1)
        body.plant(p, -1, roll=10 * smooth(0.0, 0.4, t))
        return p

    c.solve(reach_solve)
    c.layer(lambda t, T=T: look((-14, -30)))
    out.append(c)

    # ---- strain (loop) -------------------------------------------------------------------------------
    T = 0.8
    c = L.looped(f"{NAME}/strain", T)
    c.key(0.0, strain)

    def strain_solve(t, p, skel, T=T):
        u = t / T
        reaching(p, 1.0, math.sin(math.tau * 2 * u), mill=1.0, t=t)
        # scrabbling: the feet lifting in turn, toes digging
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            s = max(0.0, math.sin(math.tau * (u + ph)))
            body.plant(p, sg, pos=(0, 0.04 * s, 0), lift=0.05 * s, roll=10 + 10 * s)
        return p

    c.solve(strain_solve)

    def strain_face(t, T=T):
        u = t / T
        p = look((-14, -32))
        p.face.update({"grit": 1.0, "grin": 0.0})
        L.squint(p, 0.5)
        brows(p, -1.2, -0.4, 0.8)
        L.horns(p, x=6 + 4 * math.sin(math.tau * 2 * u), z=3 * math.sin(math.tau * u))
        return p

    c.layer(strain_face)
    out.append(c)

    # ---- deflate -------------------------------------------------------------------------------------
    T = 1.2
    c = Clip(f"{NAME}/deflate", T)
    c.key(0.0, strain)
    c.key(T, folded, "inout")

    def deflate_solve(t, p, skel, T=T):
        k = 1 - smooth(0.0, 0.4, t)
        if k > 0.01:
            reaching(p, k)
        f = smooth(0.35, 0.9, t)
        if f > 0.01:
            arms_folded(p, f)
        slump = pulse(t, 0.2, 0.2, 0.3, 0.4)
        L.hips(body, p, dz=-0.04 * slump)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(deflate_solve)

    def deflate_face(t, T=T):
        p = look((-10 * smooth(0.3, 0.8, t), 0))
        p.face.update({"oh": 0.5 * pulse(t, 0.15, 0.1, 0.3, 0.3), "flat": 0.6 * smooth(0.4, 1.0, t)})
        L.horns(p, x=-10 * smooth(0.2, 0.7, t))
        return p

    c.layer(deflate_face)
    out.append(c)

    # ---- sulk (loop) ---------------------------------------------------------------------------------
    T = 2.4
    c = L.looped(f"{NAME}/sulk", T)
    c.key(0.0, folded)

    def sulk_solve(t, p, skel, T=T):
        u = t / T
        arms_folded(p)
        tap = max(0.0, math.sin(math.tau * 3 * u)) ** 2
        body.plant(p, 1)
        body.plant(p, -1, roll=-14 * tap)
        return p

    c.solve(sulk_solve)

    def sulk_face(t, T=T):
        p = look((-10, 0))
        L.horns(p, x=-10)
        L.ears(p, tilt=-10)
        return p

    c.layer(sulk_face)
    out.append(c)

    # ---- snitch --------------------------------------------------------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/snitch", T)
    c.key(0.0, folded)
    c.key(0.3, L.REST, "inout")
    c.key(T, L.REST, "linear")
    POINT_W = V(-0.62, -0.3, 1.3)                # his right arm thrust out at Archie, on his right

    def snitch_solve(t, p, skel, T=T):
        f = 1 - smooth(0.0, 0.25, t)
        if f > 0.01:
            arms_folded(p, f)
        w = pulse(t, 0.12, 0.2, 1.8, 0.4)
        bob = math.sin(math.tau * 3 * t) * pulse(t, 0.4, 0.1, 1.4, 0.3)
        L.hips(body, p, dx=-0.03 * w, dz=0.012 * bob, roll=4 * w, yaw=-8 * w)
        d = (POINT_W - V(-0.18, -0.02, 1.12)).normalized()
        body.hand_to(p, -1, RW[-1].lerp(POINT_W, w), elbow=(0.3, 0.3, -0.6),
                     hand_rot=L.hand_world(d, (0, 0.3, -1)) if w > 0.4 else None)
        if w > 0.3:
            L.point(p, -1)
        up = pulse(t, 0.2, 0.2, 1.6, 0.4)
        body.hand_to(p, 1, RW[1].lerp(V(0.3, -0.36, 1.28), up), elbow=(0.6, 0.2, -0.4),
                     hand_rot=L.hand_world((-0.3, -0.2, 1), (0, -1, 0.2)) if up > 0.5 else None)
        L.open_hand(p, 1, 10)
        body.plant(p, 1, roll=8 * w * max(0.0, bob))
        body.plant(p, -1, roll=8 * w * max(0.0, bob))
        return p

    c.solve(snitch_solve)

    def snitch_face(t, T=T):
        w = pulse(t, 0.1, 0.2, 1.9, 0.4)
        to_him = pulse(t, 0.05, 0.1, 0.35, 0.15)
        p = look((4 * w, -30 * to_him), head=(-6 * w, 0, -18 * to_him))
        brows(p, 2.0 * w, 2.0 * w, 1.4 * w)
        p.face.update({"grin": 0.0, "oh": 0.9 * w, "wide": 0.6 * w})
        L.horns(p, x=-10 * L.ring(t, 0.15, 18, 5), z=6 * L.ring(t, 0.15, 18, 5))
        return p

    c.layer(snitch_face)
    out.append(c)

    # ---- click -------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/click", T)
    c.key(0.0, L.REST)
    c.key(T, L.REST)
    hide_r = V(-0.1, 0.26, 0.88)
    AIM_W = V(-0.42, -0.36, 1.02)                # the remote out at the button, on his right
    aim_rot = L.hand_world((-0.85, -0.45, 0.25), (0, 0, -1))

    def click_solve(t, p, skel, T=T):
        back = pulse(t, 0.0, 0.18, 0.12, 0.1)
        k = pulse(t, REMOTE, 0.3, 0.75, 0.4)
        if t < REMOTE:
            body.hand_to(p, -1, RW[-1].lerp(hide_r, back), elbow=(0.5, 0.6, -0.4))
        else:
            body.hand_to(p, -1, hide_r.lerp(AIM_W, k) if t < 1.0 else RW[-1].lerp(AIM_W, k), elbow=(0.5, 0.2, -0.5),
                         hand_rot=aim_rot if k > 0.5 else None)
        L.fist(p, -1, 0.7 * smooth(0.1, REMOTE, t))
        cl = pulse(t, CLICK - 0.05, 0.05, 0.05, 0.12)
        p.set("thumb_2_R", 20 + 40 * cl, 0, 0)
        p.set("thumb_3_R", 20 + 40 * cl, 0, 0)
        sh = math.sin(math.tau * 8 * t) * pulse(t, CLICK + 0.1, 0.1, 0.6, 0.3)
        p.both("shoulder", z=4 * sh, add=True)
        L.hips(body, p, dz=0.008 * sh, yaw=-8 * k)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(click_solve)

    def click_face(t, T=T):
        sly = pulse(t, 0.0, 0.2, 0.4, 0.2)                 # to the reader first
        at = pulse(t, 0.5, 0.2, 0.9, 0.3)                  # then at it
        p = look((-6 * at, -28 * at), head=(0, 0, -16 * at))
        brows(p, 0.0, 1.6 * sly, 1.2 * sly, side=1)
        p.face.update({"grin": 0.6 + 0.4 * max(sly, at), "smirk_R": 0.8 * at, "smirk_L": 0.8 * sly})
        L.squint(p, 0.4 * sly + 0.5 * smooth(CLICK, CLICK + 0.2, t))
        L.horns(p, x=6 * L.ring(t, CLICK, 18, 6))
        return p

    c.layer(click_face)
    out.append(c)
    return out
