"""The fake settings panel: Brick stands guard under the theme switch, arms folded. Archie climbs up from behind
the page, sizes up the switch and Brick, and produces a remote control with a flourish: he aims it. Brick
holds out his hand, palm up. Archie hands it over. Brick folds his arms again. Archie backs off, sulking --
and Zip pops up, and produces another remote. The standoff: Zip aims it, grinning; Brick stares; Archie
begs him not to. Brick's hand comes out again, and Zip hands it over too. The two of them turn to the reader
and point up at the switch -- you do it -- and Brick raises a brow. The page never changes: the switch is
never pressed.

FORMATION (metres; x across the page, from Brick's root, everyone facing the reader): Brick stands under the
switch, which is SW_Z above the floor (the page sizes the cast to make it so). Archie stands at ARCHIE_X, and
backs off to ARCHIE_BACK before Zip comes up at ZIP_X. A remote is held in the left hand (the one nearer
Brick), on `grip_L` (_handkit.GRIP: along the fingers, buttons out of the palm), REMOTE_S times its size; it
comes out from behind his back PRODUCE_AT seconds into `produce`. Handed over, it is at MEET (Brick's frame)
HANDOFF_AT seconds into the giver's `hand-over`, on his grip and on Brick's at once: the page moves it to
Brick's `grip_R` there, keeping it where it is. Brick's `palm-out` holds his hand there.

    archie  fake-settings-panel/hop-up     up from behind the edge (the page lifts him over _moves.HOP_RISE)
            fake-settings-panel/case       REST -> REST: up at the switch, across at Brick, a sly look at us
            fake-settings-panel/produce    REST -> AIM: his left hand behind his back (the remote appears at
                                           PRODUCE_AT), out with a flourish, and aimed up at the switch
            fake-settings-panel/aim        AIM, looping: thumb over the button
            fake-settings-panel/hand-over  AIM -> REST: he sees the hand; a look up at Brick; the remote into
                                           it (HANDOFF_AT); a slump
            fake-settings-panel/sulk       REST -> REST: a pout and a scuff of the foot
            fake-settings-panel/dont       REST -> REST: (at Zip) hands up, a quick shake of the head
            fake-settings-panel/please     REST -> REST: to the reader, pointing up at the switch, hopeful
    zip     fake-settings-panel/hop-up     as Archie's
            fake-settings-panel/psst       REST -> REST: a sly beckon at Archie
            fake-settings-panel/produce    REST -> AIM: as Archie's, with a twirl
            fake-settings-panel/aim        AIM, looping: brows going, thumb twitching
            fake-settings-panel/hand-over  AIM -> REST: as Archie's
            fake-settings-panel/please     REST -> REST: as Archie's
    brick   fake-settings-panel/palm-out   FOLDED -> PALM: his left arm stays folded; his right hand comes out
                                           to MEET, palm up: hand it over
            fake-settings-panel/palm-hold  PALM, looping: the fingers beckon, once
            fake-settings-panel/take       PALM -> FOLDED: the hand closes on it and goes back under his arm
                                           (the page puts the remote away at TAKE_HIDE)
            fake-settings-panel/stare      FOLDED, looping: his eyes on Zip, lids down
            fake-settings-panel/brow       FOLDED -> FOLDED: at the reader, the right brow up
            (everyday: guard-hold; FOLDED is brick_base.guard's folded arms)
"""
from __future__ import annotations

import math

from mathutils import Vector

from . import _corekit as CK
from . import _moves as M
from ._handkit import GRIP, Hand, rest_hands, wrist_for
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "fake-settings-panel"
CAST = ("archie", "zip", "brick")
TAU = math.tau

SW_Z = 3.3                      # the switch above the floor, metres
ARCHIE_X, ARCHIE_BACK, ZIP_X = -2.1, -3.0, -1.85
MEET = (-1.35, -0.3, 1.5)       # Brick's frame: where a remote changes hands (both grips there)
REMOTE_S = 4.5                  # the remotes, drawn this many times their size
PRODUCE_AT = 0.35               # produce: the remote into his hand, behind his back
HANDOFF_AT = 1.55               # hand-over: the remote at MEET
TAKE_HIDE = 1.0                 # take: his hand back under his arm (the page puts the remote away)


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    for pal, fn in (("archie", archie), ("zip", zip_), ("brick", brick)):
        if pal in bodies:
            out[pal] = fn(bodies[pal])
    return out


def aim_dir(body, at_x):
    """From his left shoulder towards the switch (his frame), a little towards the reader."""
    sh = body.skel.bones["upper_arm_L"]["rest"].translation
    d = V(-at_x, 0, SW_Z + 0.3) - sh
    d = V(d.x, -0.2 * d.length, d.z).normalized()
    return sh, d


def remote_hand(body, pal, at_x, reach):
    """The left hand's states round a remote: at rest, behind his back, out showing it, aimed at the switch,
    and offering it at MEET."""
    L = body.lib
    rest = rest_hands(body)
    rw, rr = rest[1]
    s = body.hip_z / 1.0
    sh, d = aim_dir(body, at_x)
    aim_rot = L.hand_world(d, (0, -1, 0.3))
    offer_rot = L.hand_world((1, 0, 0), (0, 0, 1))
    meet = V(MEET[0] - at_x, MEET[1], MEET[2])
    show = V(0.3, -0.45, 1.25) * s
    E = (0.5, 0.4, -0.6)
    hold = (70, 0, 10)                       # round the remote, the thumb on the buttons
    return Hand(body, 1, {
        "rest": (lambda p: V(*rw), rr, E, (18, 4, 12)),
        "behind": (lambda p: rw + V(-0.08, 0.3, 0.12) * s, L.hand_world((0.1, 0.5, -1), (1, 0, 0)), (0.5, 0.6, -0.6),
                   hold),
        "show": (lambda p: show, L.hand_world((0.4, -1, 0.5), (0, -0.3, 1)), (0.6, 0.2, -0.6), hold),
        "aim": (lambda p: sh + d * reach, aim_rot, (0.4, 0.5, -0.6), hold),
        "offer": (lambda p: wrist_for(meet, offer_rot, GRIP[pal]), offer_rot, (0.6, 0.2, -0.6), (40, 4, 20)),
    })


# ------------------------------------------------------------------------------------------ archie
def archie(body):
    L = body.lib
    REST = L.REST
    out = [M.hop_up(body, f"{NAME}/hop-up")]
    hand = remote_hand(body, "archie", ARCHIE_X, 0.66)
    rest = rest_hands(body)
    right = Hand(body, -1, {
        "rest": (lambda p: V(*rest[-1][0]), rest[-1][1], (0.5, 0.4, -0.6), (18, 4, 12)),
        "hip": (lambda p: V(-0.42, -0.02, 1.02), L.hand_world((0.3, 0.3, -1), (1, 0, 0)), (0.7, 0.2, -0.3), (30, 4, 20)),
        "up": (lambda p: V(-0.38, -0.3, 1.55), L.hand_world((0.1, -0.1, 1), (0, -1, 0)), (0.6, 0.2, -0.6), (4, 12, 0)),
    })
    SWITCH = ((22, 26), (-10, 0, 14))             # eyes and head (nod, tilt, turn) up at the switch
    BRICK = ((18, 30), (-6, 0, 20))               # ... and up at Brick's face

    def gaze(g, k):
        (ey, el), (nod, tilt, turn) = g
        return look((ey * k, el * k), head=(nod * k, tilt * k, turn * k))

    def stand(p, **kw):
        body.plant(p, 1, **kw)
        body.plant(p, -1, **kw)

    # ---- case the joint -----------------------------------------------------------------------------
    T = 1.9
    c = Clip(f"{NAME}/case", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: stand(p) or p)

    def case_layer(t):
        up = pulse(t, 0.1, 0.25, 0.35, 0.2)
        at_b = pulse(t, 0.8, 0.2, 0.25, 0.2)
        us = pulse(t, 1.35, 0.15, 0.3, 0.1)
        p = gaze(SWITCH, up) + gaze(BRICK, at_b) + look((0, -6 * us), head=(0, 6 * us, -4 * us))
        p.face.update({"grin": -0.6 * us, "smirk_L": 1.0 * us})
        brows(p, 0.4 * us, 1.2 * us, 0.8 * us, side=1)
        return p

    c.layer(case_layer)
    c.layer(blink_layer([0.65]))
    out.append(c)

    # ---- produce: REST -> AIM -------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/produce", T)
    c.key(0.0, REST)

    def produce_solve(t, p, skel):
        L.hips(body, p, roll=-3 * pulse(t, 0.3, 0.3, 0.2, 0.5))
        p.add("chest", -4 * smooth(0.9, 1.3, t), 0, 3 * smooth(0.9, 1.3, t))
        hand(p, t, ["rest", (0.0, PRODUCE_AT, "behind", "inout"), (0.4, 0.75, "show", "back"),
                    (0.95, 1.35, "aim", "inout")])
        right(p, t, ["rest", (0.85, 1.3, "hip", "inout")])
        stand(p)
        return p

    c.solve(produce_solve)

    def produce_layer(t):
        sm = smooth(0.4, 0.7, t)
        p = Pose(face={"grin": -0.4 * sm, "smirk_L": 0.9 * sm})
        brows(p, 0.6 * sm, 1.0 * sm, 0.6 * sm)
        p = p + look((6 * pulse(t, 0.4, 0.15, 0.3, 0.2), 10 * pulse(t, 0.4, 0.15, 0.3, 0.2)))   # a look at it
        p = p + gaze(SWITCH, 0.8 * smooth(0.9, 1.3, t))
        return p

    c.layer(produce_layer)
    out.append(c)

    def aim_face(k=1.0, t=0.0):
        p = Pose(face={"grin": -0.4 * k, "smirk_L": 0.9 * k})
        brows(p, 0.6 * k, 1.0 * k, 0.6 * k)
        return p + gaze(SWITCH, 0.8 * k)

    # ---- aim (loop) -----------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/aim", T)
    c.key(0.0, REST)

    def aim_solve(t, p, skel, T=T):
        p.add("chest", -4, 0, 3)
        hand(p, t, ["aim"])
        right(p, t, ["hip"])
        p.side("thumb_2", 1, x=8 * max(0.0, math.sin(TAU * 2 * t / T)), add=True)   # hovering over it
        stand(p)
        return p

    c.solve(aim_solve)
    c.layer(lambda t: aim_face())
    c.layer(blink_layer([1.3]))
    out.append(c)

    # ---- hand-over: AIM -> REST ------------------------------------------------------------------------
    T = 2.8
    c = Clip(f"{NAME}/hand-over", T)
    c.key(0.0, REST)

    def handover_solve(t, p, skel):
        slump = smooth(1.9, 2.5, t)
        p.add("chest", -4 * (1 - smooth(0.3, 0.8, t)) + 8 * slump, 0, 3 * (1 - smooth(0.3, 0.8, t)))
        p.add("spine", 4 * slump, 0, 0)
        p.both("shoulder", z=-5 * slump, add=True)
        hand(p, t, ["aim", (0.8, HANDOFF_AT, "offer", "inout"), (1.85, 2.5, "rest", "inout")])
        right(p, t, ["hip", (0.3, 0.8, "rest", "inout")])
        stand(p)
        return p

    c.solve(handover_solve)

    def handover_layer(t):
        k = 1 - smooth(0.0, 0.3, t)
        p = aim_face(k)
        sees = pulse(t, 0.15, 0.2, 0.5, 0.3)                    # down at the hand
        up = pulse(t, 0.95, 0.25, 0.55, 0.3)                     # up at Brick: really?
        p = p + look((-16 * sees, 26 * sees), head=(10 * sees, 0, 10 * sees)) + gaze(BRICK, up)
        sad = smooth(1.0, 1.5, t)
        p.face.update({"grin": p.face.get("grin", 0.0) - 1.0 * sad, "frown": 0.7 * sad})
        brows(p, 1.4 * sad, 0.4 * sad, -0.5 * sad)
        p.add("head", 10 * smooth(2.0, 2.5, t), 0, 0)
        return p

    c.layer(handover_layer)
    c.layer(blink_layer([0.35, 2.2]))
    out.append(c)

    # ---- sulk -----------------------------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/sulk", T)
    c.key(0.0, REST)
    pout = REST.copy()
    pout.face = {"frown": 0.9}
    pout.set("head", 12, 0, -4)
    pout.set("chest", 6, 0, 0)
    pout.both("shoulder", z=-5)
    c.key(0.3, pout)
    c.key(T - 0.3, pout, "linear")
    c.key(T, REST)

    def sulk_solve(t, p, skel):
        scuff = pulse(t, 0.45, 0.18, 0.05, 0.25)
        body.plant(p, 1)
        body.plant(p, -1, pos=(0, -0.12 * scuff, 0), lift=0.04 * scuff, roll=-10 * scuff)
        return p

    c.solve(sulk_solve)
    c.layer(lambda t: brows(Pose(), 1.0 * pulse(t, 0.2, 0.3, 0.6, 0.3), 0, -0.6 * pulse(t, 0.2, 0.3, 0.6, 0.3)))
    out.append(c)

    # ---- dont: at Zip -- hands up, a quick no -------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/dont", T)
    c.key(0.0, REST)
    up_rot = {sg: L.hand_world((sg * 0.2, -0.1, 1), (0, -1, 0)) for sg in (1, -1)}
    rw = {sg: rest[sg][0] for sg in (1, -1)}

    def dont_solve(t, p, skel):
        k = pulse(t, 0.05, 0.25, 0.9, 0.35)
        for sg in (1, -1):
            body.hand_to(p, sg, rw[sg].lerp(V(sg * 0.42, -0.35, 1.5), k), elbow=(0.6, 0.2, -0.6),
                         hand_rot=up_rot[sg] if k > 0.5 else rest[sg][1])
            p.fingers(sg, 18 - 14 * k, spread=4 + 10 * k, thumb=12 - 12 * k)
        stand(p)
        return p

    c.solve(dont_solve)

    def dont_layer(t):
        k = pulse(t, 0.05, 0.25, 0.9, 0.35)
        p = look((0, 30 * k), head=(0, 0, 14 * k + 10 * math.sin(TAU * 3 * t) * pulse(t, 0.3, 0.1, 0.6, 0.2)))
        p.face.update({"grin": -1.0 * k, "grit": 0.8 * k})
        brows(p, 1.8 * k, 1.4 * k, 0.8 * k)
        return p

    c.layer(dont_layer)
    out.append(c)

    # ---- please: to the reader, pointing up at the switch -------------------------------------------------
    out.append(please(body, aim_dir(body, ARCHIE_X), (18, 4, 12), rest))
    return out


def please(body, aim, relaxed, rest):
    """Turned to the reader, his left hand pointing up at the switch, brows up: you do it."""
    L = body.lib
    sh, d = aim
    B = body.skel.bones
    reach = 0.85 * (B["upper_arm_L"]["length"] + B["forearm_L"]["length"])
    T = 2.4
    c = Clip(f"{NAME}/please", T)
    c.key(0.0, L.REST)
    hand = Hand(body, 1, {
        "rest": (lambda p: V(*rest[1][0]), rest[1][1], (0.5, 0.4, -0.6), relaxed),
        "point": (lambda p: sh + (d * 0.85 + V(0, -0.3, 0)).normalized() * reach,
                  L.hand_world(d, (0, -1, 0)), (0.4, 0.4, -0.6), ((0, 90, 90), 0, 50)),
    })

    def solve(t, p, skel):
        hand(p, t, ["rest", (0.1, 0.45, "point", "back"), (1.9, 2.35, "rest", "inout")])
        L.hips(body, p, dz=0.02 * math.sin(TAU * 2 * t) * pulse(t, 0.5, 0.1, 1.2, 0.2))   # a hopeful bounce
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)

    def layer(t):
        k = pulse(t, 0.1, 0.3, 1.5, 0.4)
        p = Pose(face={"grin": 0.3 * k, "wide": 0.3 * k})
        brows(p, 1.6 * k, 1.8 * k, 1.2 * k)
        return p + look((6 * k, 0))

    c.layer(layer)
    return c


# --------------------------------------------------------------------------------------------- zip
def zip_(body):
    L = body.lib
    REST = L.REST
    out = [M.hop_up(body, f"{NAME}/hop-up")]
    hand = remote_hand(body, "zip", ZIP_X, 0.44)
    rest = rest_hands(body)
    right = Hand(body, -1, {
        "rest": (lambda p: V(*rest[-1][0]), rest[-1][1], (0.5, 0.4, -0.6), (22, 4, 14)),
        "hip": (lambda p: V(-0.3, -0.02, 0.8), L.hand_world((0.3, 0.3, -1), (1, 0, 0)), (0.7, 0.2, -0.3), (40, 4, 20)),
        "beckon": (lambda p: V(-0.3, -0.32, 1.05), L.hand_world((0.3, -0.5, 1), (0.3, -1, 0)), (0.6, 0.2, -0.6),
                   (40, 0, 20)),
    })
    SWITCH = ((24, 24), (-10, 0, 12))

    def gaze(g, k):
        (ey, el), (nod, tilt, turn) = g
        return look((ey * k, el * k), head=(nod * k, tilt * k, turn * k))

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    # ---- psst: a sly beckon at Archie, off to his right ---------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/psst", T)
    c.key(0.0, REST)

    def psst_solve(t, p, skel):
        right(p, t, ["rest", (0.05, 0.3, "beckon", "inout"), (1.0, 1.35, "rest", "inout")])
        crook = max(0.0, math.sin(TAU * 2.5 * (t - 0.3))) * pulse(t, 0.3, 0.05, 0.6, 0.1)
        p.fingers(-1, (40 + 50 * crook, 70, 70), spread=0, thumb=30)
        stand(p)
        return p

    c.solve(psst_solve)

    def psst_layer(t):
        k = pulse(t, 0.05, 0.2, 0.9, 0.25)
        p = look((0, -28 * k), head=(4 * k, -6 * k, -18 * k))
        p.face.update({"grin": -0.5 * k, "smirk_R": 1.0 * k})
        brows(p, 0.4 * k, 1.4 * k, 1.0 * k)
        return p

    c.layer(psst_layer)
    out.append(c)

    # ---- produce: with a twirl -----------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/produce", T)
    c.key(0.0, REST)

    def produce_solve(t, p, skel):
        L.hips(body, p, dz=0.03 * pulse(t, 0.4, 0.15, 0.0, 0.3))
        hand(p, t, ["rest", (0.0, PRODUCE_AT, "behind", "inout"), (0.4, 0.7, "show", "back"),
                    (0.95, 1.35, "aim", "inout")])
        right(p, t, ["rest", (0.85, 1.3, "hip", "inout")])
        stand(p)
        return p

    c.solve(produce_solve)

    def aim_face(k, t=0.0):
        waggle = max(0.0, math.sin(TAU * 1.0 * t)) ** 2
        p = Pose(face={"grin": 0.2 * k})
        brows(p, (0.6 + 1.2 * waggle) * k, (1.0 + 1.4 * waggle) * k, (0.8 + 1.0 * waggle) * k)
        L.squint(p, 0.3 * k)
        return p + gaze(SWITCH, 0.8 * k)

    c.layer(lambda t: aim_face(smooth(0.9, 1.3, t)) + L.horn_sway(t, T, 3.0))
    out.append(c)

    # ---- aim (loop) -----------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/aim", T)
    c.key(0.0, REST)

    def aim_solve(t, p, skel, T=T):
        hand(p, t, ["aim"])
        right(p, t, ["hip"])
        p.side("thumb_2", 1, x=12 * max(0.0, math.sin(TAU * 3 * t / T)), add=True)
        stand(p)
        return p

    c.solve(aim_solve)
    c.layer(lambda t, T=T: aim_face(1.0, t) + L.horn_sway(t, T, 2.0))
    out.append(c)

    # ---- hand-over ------------------------------------------------------------------------------------
    T = 2.8
    c = Clip(f"{NAME}/hand-over", T)
    c.key(0.0, REST)

    def handover_solve(t, p, skel):
        tip = pulse(t, 1.2, 0.3, 0.3, 0.4)                       # up on his toes to reach
        L.hips(body, p, dz=0.05 * tip)
        hand(p, t, ["aim", (0.8, HANDOFF_AT, "offer", "inout"), (1.85, 2.5, "rest", "inout")])
        right(p, t, ["hip", (0.3, 0.8, "rest", "inout")])
        for sg in (1, -1):
            body.plant(p, sg, roll=24 * tip)
        return p

    c.solve(handover_solve)

    def handover_layer(t):
        p = aim_face(1 - smooth(0.0, 0.3, t))
        sees = pulse(t, 0.15, 0.2, 0.5, 0.3)
        up = pulse(t, 0.95, 0.25, 0.55, 0.3)
        p = p + look((-10 * sees + 26 * up, 28 * sees + 24 * up), head=(8 * sees - 10 * up, 0, 8 * sees + 10 * up))
        sad = smooth(1.0, 1.5, t)
        p.face.update({"grin": p.face.get("grin", 0.0) - 1.0 * sad, "frown": 0.8 * sad})
        brows(p, 1.6 * sad, 0.4 * sad, -0.6 * sad)
        p.add("head", 10 * smooth(2.0, 2.5, t), 0, 0)
        return p

    c.layer(handover_layer)
    c.layer(blink_layer([0.35, 2.2], up=L.LID_UP, lo=L.LID_LO))
    out.append(c)

    out.append(please(body, aim_dir(body, ZIP_X), (22, 4, 14), rest))
    return out


# ------------------------------------------------------------------------------------------- brick
def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    palm_rot = L.hand_world((-1, 0, 0), (0, 0, 1))
    # his arms folded as brick_base.guard folds them: left over right
    fold = {sg: (lambda p, sg=sg: V(*L.FOLD[sg]), L.hand_world((-sg * 1, -0.1, 0.1), (0, 0.3 * sg, -1)),
                 (1.0, -0.2, -0.3), (62, 0, 34)) for sg in (1, -1)}
    left = Hand(body, 1, {"fold": fold[1]})
    right = Hand(body, -1, {
        "fold": fold[-1],
        "palm": (lambda p: wrist_for(MEET, palm_rot, GRIP["brick"]), palm_rot, (0.7, 0.3, -0.6), (12, 6, 10)),
        "fist": (lambda p: wrist_for(MEET, palm_rot, GRIP["brick"]), palm_rot, (0.7, 0.3, -0.6), (75, 0, 40)),
    })

    def folded(p, t, path, lean=0.0):
        p.add("chest", -4 + 4 * lean, -6 * lean, 5 * lean)      # leaning a little to his right, to the hand
        p.add("head", -4, 0, 0)
        left(p, t, ["fold"])
        right(p, t, path)
        body.plant(p, 1, pos=(0.06, 0, 0), yaw=L.STANCE + 4)
        body.plant(p, -1, pos=(-0.06, 0, 0), yaw=L.STANCE + 4)
        return p

    def deadpan(k=1.0):
        p = Pose(face={"smile": -0.5 * k, "flat": 0.5 * k})
        L.lids(p, 0.2 * k)
        return p

    AT_HAND = ((-14, -26), (8, 0, -12))           # his eyes down at whoever is at the hand

    def gaze(g, k):
        (ey, el), (nod, tilt, turn) = g
        return look((ey * k, el * k), head=(nod * k, tilt * k, turn * k))

    # ---- palm-out: FOLDED -> PALM, the left arm staying folded ---------------------------------------------
    T = 1.0
    c = Clip(f"{NAME}/palm-out", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: folded(p, t, ["fold", (0.05, 0.85, "palm", "inout")], ease("inout", smooth(0.05, 0.85, t))))
    c.layer(lambda t: deadpan(1.0) + gaze(AT_HAND, smooth(0.0, 0.4, t)))
    out.append(c)

    # ---- palm-hold (loop) -------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/palm-hold", T)
    c.key(0.0, REST)

    def hold_solve(t, p, skel, T=T):
        folded(p, t, ["palm"], 1.0)
        g = pulse(t, 0.5, 0.15, 0.05, 0.2)                     # give: the fingers curl, once
        p.fingers(-1, 12 + 50 * g, spread=6, thumb=10)
        return p

    c.solve(hold_solve)
    c.layer(lambda t: deadpan(1.0) + gaze(AT_HAND, 1.0))
    c.layer(L.blinks([1.4]))
    out.append(c)

    # ---- take: PALM -> FOLDED: the hand closes on it and goes back under his arm ----------------------------
    T = 1.3
    c = Clip(f"{NAME}/take", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: folded(p, t, ["palm", (0.0, 0.2, "fist", "inout"), (0.3, 1.15, "fold", "inout")],
                                      1 - ease("inout", smooth(0.3, 1.15, t))))
    c.layer(lambda t: deadpan(1.0) + gaze(AT_HAND, 1 - smooth(0.4, 1.0, t)))
    out.append(c)

    # ---- stare (loop): at Zip ----------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/stare", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: folded(p, t, ["fold"]))

    def stare_layer(t, T=T):
        p = deadpan(1.0) + gaze(AT_HAND, 0.9)
        L.lids(p, 0.25)
        L.brows(p, -0.8, -0.5, 0.0)
        p.add("chest", -0.8 * math.sin(TAU * t / T), 0, 0)
        return p

    c.layer(stare_layer)
    c.layer(L.blinks([1.5]))
    out.append(c)

    # ---- brow: at the reader ------------------------------------------------------------------------------
    T = 2.2
    c = Clip(f"{NAME}/brow", T)
    c.key(0.0, REST)
    c.solve(lambda t, p, skel: folded(p, t, ["fold"]))

    def brow_layer(t):
        k = pulse(t, 0.15, 0.4, 1.1, 0.45)
        p = deadpan(1.0)
        L.brows(p, 0.6 * k, 1.9 * k, 1.5 * k, side=-1)
        L.brows(p, -0.3 * k, -0.4 * k, -0.2 * k, side=1)
        p.add("head", -2 * k, 0, -3 * k)
        return p

    c.layer(brow_layer)
    out.append(c)
    return out
