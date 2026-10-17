"""The leveling dispute: Archie levels the README. Zip, out of sight behind the viewer's far end, nudges the
other end of the level. Archie measures again and fixes it. Twice. The third time he follows the level along
to its far end -- and there is Zip, holding it.

The page stands Archie on the README viewer's top edge, facing the reader, and lays the level (the `level`
prop, scaled LEVEL_SCALE) along the edge on his left (screen right), from LEVEL_NEAR to LEVEL_NEAR +
LEVEL_LEN metres from his root. Zip stands below the edge at the level's far end, the end resting on top of
his head, hidden by the page (his figure is clipped at the edge's line, as if behind the viewer) but for the
tips of his horns, until he rises into view. He nudges the end by going up on his toes.

FORMATION (metres, from Archie's root, x to his left = screen right, z up; the edge is z = 0):
    archie  (0, 0, 0)
    level   from x = LEVEL_NEAR to LEVEL_NEAR + LEVEL_LEN, on the edge
    zip     (ZIP_X, 0, ZIP_Z): below the edge, facing the reader, the level's far end on his head

Pieces (Archie):
    leveling-dispute/hop      he comes up from behind the viewer onto its edge (the page lifts him from
                              below the edge's line over the first HOP_RISE seconds) and lands
    leveling-dispute/set      the level from behind his back, laid on the edge at his left; the page holds
                              it in his left hand until SET_DROP, then lays it down
    leveling-dispute/peer     down on his haunches, one eye shut, squinting along it at the bubble
    leveling-dispute/fix      two firm taps on the level's near end with his left fist (the page levels
                              it on the taps, at FIX_TAPS)
    leveling-dispute/pleased  up, dusts his hands, a smug nod
    leveling-dispute/again    a double take at the level: it has moved
    leveling-dispute/follow   he follows the level along to its far end with his eyes, finds Zip, stares,
                              then turns the same stare on the reader
Pieces (Zip, clips/zip_base.py):
    leveling-dispute/hold     loops: still as a mouse under the end, eyes up
    leveling-dispute/nudge    up on his toes (NUDGE_RISE metres) and held there, stifling a giggle
    leveling-dispute/duck     back down off his toes
    leveling-dispute/caught   the page lifts him up into view; hands up, who, me? a sheepish grin, a wave
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "leveling-dispute"
CAST = ("archie", "zip")
LEVEL_SCALE = 2.0                    # the 1 m prop, drawn 2 m long
LEVEL_NEAR = 0.32                    # its near end, from Archie's root
LEVEL_LEN = 1.0 * LEVEL_SCALE
HOP_RISE = 0.45
SET_GRAB, SET_DROP = 0.35, 1.25      # the level appears in his left hand, and leaves it
FIX_TAPS = (0.75, 1.25)
ZIP_X, ZIP_Z = LEVEL_NEAR + LEVEL_LEN, -1.74     # his dome's top just under the edge
NUDGE_RISE = 0.07


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


def archie_clips(body):
    L = body.lib
    REST, hips, fist, open_hand, hand_world = L.REST, L.hips, L.fist, L.open_hand, L.hand_world
    out = []

    def rest_wrist(sg):
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        return L.wrist_of(body, q, sg)

    RW = {1: rest_wrist(1), -1: rest_wrist(-1)}

    # ---- hop: up from behind the viewer, a landing ---------------------------------------------------
    TH = 1.2
    c = Clip(f"{NAME}/hop", TH)
    up = REST.copy()
    up.both("upper_arm", x=-20, z=60)
    up.both("forearm", x=30)
    open_hand(up, 1, 12)
    open_hand(up, -1, 12)
    up.face = {"wide": 0.6, "grin": 0.4}
    c.key(0.0, up)
    c.key(HOP_RISE, up, "linear")
    c.key(TH, REST, "out")

    def hop_solve(t, p, skel, TH=TH):
        land = pulse(t, HOP_RISE, 0.08, 0.05, 0.45)
        hips(body, p, dz=-0.18 * land, pitch=10 * land)
        p.add("chest", 6 * land, 0, 0)
        p.add("head", -8 * land, 0, 0)
        body.plant(p, 1, lift=0.12 * (1 - smooth(HOP_RISE - 0.1, HOP_RISE, t)))
        body.plant(p, -1, lift=0.08 * (1 - smooth(HOP_RISE - 0.1, HOP_RISE, t)))
        return p

    c.solve(hop_solve)
    c.layer(lambda t: L.crest_follow(t * 8, 2.0 * pulse(t, HOP_RISE, 0.05, 0.1, 0.5)))
    out.append(c)

    # ---- set: the level from behind his back, down on the edge ---------------------------------------
    TS = 2.4
    c = Clip(f"{NAME}/set", TS)
    c.key(0.0, REST)
    look_down = REST.copy()
    look_down.set("head", 12, 16, -6)
    look_down.face = {"grin": 0.5, "flat": 0.3}
    c.key(0.9, look_down)
    c.key(TS - 0.5, look_down, "linear")
    c.key(TS, REST)
    behind = V(0.32, 0.24, 1.0)
    down = V(0.62, -0.12, 0.22)

    def set_solve(t, p, skel, TS=TS):
        crouch = pulse(t, 0.55, 0.5, 0.45, 0.6)
        hips(body, p, dx=0.1 * crouch, dz=-0.55 * crouch, pitch=10 * crouch, roll=-8 * crouch)
        p.add("spine", 6 * crouch, 0, -6 * crouch)
        p.add("chest", 4 * crouch, 8 * crouch, -6 * crouch)
        reach = pulse(t, 0.05, 0.3, TS - 1.0, 0.5)
        if t < SET_GRAB:
            tgt = RW[1].lerp(behind, smooth(0.05, SET_GRAB, t))
        elif t < SET_DROP:
            tgt = behind.lerp(down, ease("inout", (t - SET_GRAB) / (SET_DROP - SET_GRAB)))
        else:
            tgt = down.lerp(RW[1], smooth(SET_DROP + 0.2, TS - 0.2, t))
        hr = hand_world((0.2, -1, -0.2), (0, 0, -1)) if SET_GRAB < t < SET_DROP else None
        body.hand_to(p, 1, RW[1].lerp(tgt, reach) if t < SET_GRAB else tgt, elbow=(0.5, 0.4, -0.4), hand_rot=hr)
        fist(p, 1, 0.8 * pulse(t, SET_GRAB - 0.1, 0.1, SET_DROP - SET_GRAB, 0.15))
        body.plant(p, 1, pos=(0.08 * crouch, 0, 0), knee_out=0.1 * crouch)
        body.plant(p, -1, knee_out=0.06 * crouch)
        return p

    c.solve(set_solve)
    c.layer(blink_layer([0.4, 2.0]))
    out.append(c)

    # ---- peer: on his haunches, one eye shut, squinting along the level ------------------------------
    TP = 2.8
    c = Clip(f"{NAME}/peer", TP)
    c.key(0.0, REST)
    sq = REST.copy()
    sq.set("head", 0, 22, -22)                   # turned to his left, tipped to put his eye along it
    sq.set("neck", 0, 6, -6)
    sq.face = {"flat": 0.6, "smirk_R": 0.5}
    for sg in (1, -1):
        open_hand(sq, sg, 6)
    c.key(0.6, sq)
    c.key(TP - 0.5, sq, "linear")
    c.key(TP, REST)

    def peer_solve(t, p, skel, TP=TP):
        k = pulse(t, 0.0, 0.6, TP - 1.1, 0.5)
        hips(body, p, dx=0.12 * k, dz=-0.62 * k, pitch=8 * k, roll=-8 * k)
        p.add("spine", 4 * k, 0, -8 * k)
        p.add("chest", 0, 8 * k, -8 * k)
        # hands on his knees
        for sg in (1, -1):
            knee = V(sg * 0.22 + 0.08 * k, -0.42, 0.62)
            body.hand_to(p, sg, RW[sg].lerp(knee, k), elbow=(0.6, 0.3, -0.2),
                         hand_rot=hand_world((0, -0.3, -1), (0, -1, 0.2)) if k > 0.5 else None)
        body.plant(p, 1, pos=(0.1 * k, 0, 0), knee_out=0.16 * k)
        body.plant(p, -1, pos=(-0.04 * k, 0, 0), knee_out=0.16 * k)
        return p

    c.solve(peer_solve)

    def peer_face(t, TP=TP):
        p = Pose()
        k = pulse(t, 0.5, 0.2, TP - 1.1, 0.3)
        p.side("lid_up", -1, x=-46 * k)           # the right eye shut
        p.side("lid_lo", -1, x=40 * k)
        p.side("lid_up", 1, x=-18 * k)            # the left one narrowed
        brows(p, -1.0 * k, -0.6 * k, 0.3 * k, side=1)
        brows(p, 1.4 * k, 1.2 * k, 0.6 * k, side=-1)
        bob = math.sin(t * 7) * pulse(t, 0.8, 0.3, 1.0, 0.3)
        p.add("head", 0, 0, 2 * bob)
        return p + look((-8 * k, 22 * k))

    c.layer(peer_face)
    out.append(c)

    # ---- fix: two firm taps on the near end ----------------------------------------------------------
    TF = 2.0
    c = Clip(f"{NAME}/fix", TF)
    c.key(0.0, REST)
    fx = REST.copy()
    fx.set("head", 10, 20, -6)
    fx.face = {"grit": 0.6, "flat": 0.4}
    c.key(0.45, fx)
    c.key(TF - 0.45, fx, "linear")
    c.key(TF, REST)
    end = V(LEVEL_NEAR + 0.1, -0.08, 0.17)

    def fix_solve(t, p, skel, TF=TF):
        k = pulse(t, 0.0, 0.45, TF - 0.9, 0.45)
        hips(body, p, dx=0.1 * k, dz=-0.58 * k, pitch=10 * k, roll=-8 * k)
        p.add("spine", 6 * k, 0, -8 * k)
        p.add("chest", 4 * k, 10 * k, -6 * k)
        tap = max(pulse(t, FIX_TAPS[0] - 0.12, 0.12, 0.02, 0.18), pulse(t, FIX_TAPS[1] - 0.12, 0.12, 0.02, 0.18))
        tgt = end + V(0, 0, 0.16 * (1 - tap))
        body.hand_to(p, 1, RW[1].lerp(tgt, k), elbow=(0.6, 0.4, -0.3),
                     hand_rot=hand_world((0.1, -0.3, -1), (0, -1, 0)) if k > 0.5 else None)
        fist(p, 1, k)
        body.hand_to(p, -1, RW[-1].lerp(V(-0.2, -0.4, 0.62), k), elbow=(0.6, 0.3, -0.2))
        body.plant(p, 1, pos=(0.08 * k, 0, 0), knee_out=0.12 * k)
        body.plant(p, -1, knee_out=0.1 * k)
        return p

    c.solve(fix_solve)
    c.layer(lambda t: look((-14, 18)) + Pose(face={"grin": -0.4 * pulse(t, 0.6, 0.1, 0.8, 0.2)}))
    out.append(c)

    # ---- pleased: up, dust the hands, a smug nod -----------------------------------------------------
    TQ = 1.8
    c = Clip(f"{NAME}/pleased", TQ)
    c.key(0.0, REST)
    pl = REST.copy()
    pl.set("chest", -6, 0, 0)
    pl.set("head", -8, -6, 4)
    pl.face = {"grin": 1.0, "smirk_L": 0.4}
    c.key(0.4, pl)
    c.key(TQ - 0.3, pl, "linear")
    c.key(TQ, REST)

    def pleased_solve(t, p, skel, TQ=TQ):
        k = pulse(t, 0.05, 0.35, 0.7, 0.35)
        brush = math.sin(t * 22) * pulse(t, 0.25, 0.1, 0.5, 0.15)
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.06 + 0.04 * brush * sg, -0.4, 1.12), k), elbow=(0.6, 0.2, -0.6))
            open_hand(p, sg, 6)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(pleased_solve)
    c.layer(lambda t: Pose().add("head", 10 * pulse(t, 1.05, 0.15, 0.05, 0.2), 0, 0) + look((4, -6)))
    c.layer(lambda t: brows(Pose(), 0.6, 1.2 * pulse(t, 0.9, 0.2, 0.5, 0.2), 1.0, side=1))
    out.append(c)

    # ---- again: a double take ------------------------------------------------------------------------
    TA = 1.4
    c = Clip(f"{NAME}/again", TA)
    c.key(0.0, REST)
    dt = REST.copy()
    dt.set("head", 12, 30, -8)
    dt.set("chest", 2, 10, -2)
    dt.face = {"oh": 1.0}
    c.key(0.18, dt, "snap")
    c.key(TA - 0.35, dt, "linear")
    c.key(TA, REST)
    c.layer(lambda t: brows(Pose(), 1.6, 1.8, 1.0) + look((-10, 20)) if t > 0.12 else None)
    c.solve(lambda t, p, skel: (body.plant(p, 1), body.plant(p, -1), p)[-1])
    out.append(c)

    # ---- follow: along the level to its far end, Zip; the stare; the reader --------------------------
    TW = 4.2
    c = Clip(f"{NAME}/follow", TW)
    c.key(0.0, REST)
    near = REST.copy()
    near.set("head", 14, 22, -6)
    near.face = {"flat": 0.6}
    far = REST.copy()
    far.set("head", 2, 44, -4)
    far.set("chest", 0, 16, -4)
    far.set("spine", 0, 8, -6)
    far.face = {"flat": 1.0}
    reader = REST.copy()
    reader.set("head", -2, 0, 6)
    reader.face = {"flat": 1.0}
    c.key(0.5, near)
    c.key(1.7, far, "inout")
    c.key(2.9, far, "linear")
    c.key(3.3, reader, "inout")
    c.key(TW, reader, "linear")

    def follow_layer(t):
        p = Pose()
        u = smooth(0.4, 1.7, t)
        p = p + look((-14 * (1 - u), 18 + 16 * u)) if t < 3.1 else p + look((0, 0))
        s = pulse(t, 1.8, 0.2, 2.4, 0.1)
        brows(p, -1.2 * s, -0.8 * s, 0.4 * s)
        p.both("lid_up", x=-14 * s)
        return p

    c.layer(follow_layer)
    c.layer(blink_layer([2.6]))
    c.solve(lambda t, p, skel: (body.plant(p, 1), body.plant(p, -1), p)[-1])
    out.append(c)
    return out


def zip_clips(body):
    """Zip's pieces: below the edge at the level's far end (ZIP_X, ZIP_Z from Archie's root), facing the
    reader, the end of the level on his head."""
    from bits._moves import loop_clip
    L = body.lib
    RW = L.rest_wrists(body)
    out = []
    still = L.REST.copy()
    still.set("head", -6, 0, 0)
    still.face = {"grin": 0.6, "smirk_L": 0.6}

    TH = 2.0
    c = loop_clip(f"{NAME}/hold", TH)
    c.key(0.0, still)
    c.layer(lambda t: look((18, 6 * math.sin(math.tau * t / TH))) + L.horn_sway(t, TH, 2.0))
    c.solve(L.stand(body))
    out.append(c)

    def tiptoe(p, k):
        L.hips(body, p, dz=NUDGE_RISE * k)
        body.plant(p, 1, roll=30 * k)
        body.plant(p, -1, roll=30 * k)
        return p

    TN = 0.9
    c = Clip(f"{NAME}/nudge", TN)
    c.key(0.0, still)
    gig = still.copy()
    gig.face = {"grin": 1.0}
    c.key(0.4, gig)
    c.key(TN, gig, "linear")
    c.solve(lambda t, p, skel: tiptoe(p, ease("inout", t / 0.35)))
    c.layer(lambda t: L.squint(Pose(), pulse(t, 0.3, 0.1, 0.4, 0.1))
            + Pose().add("chest", 0, 0, 3 * math.sin(t * 30) * pulse(t, 0.35, 0.05, 0.3, 0.1)) + look((18, 0)))
    out.append(c)

    TD = 0.6
    c = Clip(f"{NAME}/duck", TD)
    c.key(0.0, gig)
    c.key(TD, still, "linear")
    c.solve(lambda t, p, skel: tiptoe(p, 1 - ease("inout", t / 0.4)))
    c.layer(lambda t: look((18, 0)))
    out.append(c)

    TC = 2.8
    c = Clip(f"{NAME}/caught", TC)
    c.key(0.0, still)
    who = L.REST.copy()
    who.face = {"grin": 1.0, "wide": 0.4}
    c.key(0.5, who)
    c.key(TC - 0.4, who, "linear")
    c.key(TC, L.REST)

    def caught_solve(t, p, skel):
        k = pulse(t, 0.3, 0.3, TC - 1.0, 0.4)
        wave = pulse(t, 1.5, 0.2, 0.6, 0.3)
        for sg in (1, -1):
            up = Vector((sg * 0.42, -0.25, 1.35 + 0.15 * (wave if sg < 0 else 0)))
            body.hand_to(p, sg, RW[sg].lerp(up, k), elbow=(0.6, 0.3, -0.2),
                         hand_rot=L.hand_world((sg * 0.1, -0.1, 1), (0, -1, 0)) if k > 0.5 else None)
            L.open_hand(p, sg, 14)
        p.side("hand", -1, z=30 * math.sin(t * 14) * wave, add=True)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(caught_solve)
    c.layer(lambda t: brows(Pose(), 1.2, 1.6, 1.0) + look((0, 30 * smooth(0.2, 0.5, t) * (1 - smooth(1.2, 1.5, t))))
            + L.horn_sway(t, TC, 5.0))
    out.append(c)
    return out
