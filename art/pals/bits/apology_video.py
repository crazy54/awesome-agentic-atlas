"""The apology video: after a prank, Archie sits on a chair under a softbox, a video camera trained on him,
looking remorseful. Zip, beside the camera, holds up a cue card -- I AM SO SORRY -- and Archie reads it out,
far too cheerfully, and finishes with a thumbs-up. Brick, the director, arms folded, unfolds them, raises a
card of his own and turns it round: LOOK SADDER. Archie goes all the way: lip wobbling, hands clasped, the back
of his hand to his brow, sobbing. Zip, holding the card, has to wipe an eye. Brick nods; the camera stops; and
Archie is up at once with finger guns. Brick raises a brow at the reader.

FORMATION (metres; x across the page from the chair's origin, z towards the reader): the `folding-chair` at
CHAIR_S times, turned AIM radians towards the page's right, where the camera is; Archie's root SEAT_FROM in
front of the chair's origin along that turn, facing the same way (the page stands him there and turns him).
Seated, his hips are SEAT (his frame: back, up) from his root, over the seat. Zip and Brick stand to the
right holding their cards up in their right hands, the wrist at CARD[pal]; the page keeps each card on the
grip, upright, facing where the pal faces (cheated round towards the reader as much as towards Archie).

    archie  apology-video/sit-down  REST -> SAD: down onto the chair, a sigh, hands clasped between his knees
            apology-video/sad       SAD, looping: hunched, a slow breath, a guilty look up and away
            apology-video/apology   SAD -> CHEESY: a glance at Zip's card, then the lines to the camera (SAY_AT),
                                    a hand on his heart -- but the grin breaks through and he gives it a
                                    thumbs-up
            apology-video/cheesy    CHEESY, looping: sitting up, grinning, thumbs-up
            apology-video/sadder    CHEESY -> WEEP: he turns to read Brick's card (READ_AT), the grin drops, a
                                    breath, and then the works: hands clasped under his chin, lip wobbling,
                                    then the back of his right hand to his brow and his head back (SOB_AT)
            apology-video/weep      WEEP, looping: sobbing, shoulders heaving, the lip going
            apology-video/perk-up   WEEP -> REST: the camera stops; upright at once, finger guns at it and a
                                    wink (GUNS_AT), and up off the chair
    zip     apology-video/card-up   REST -> CARD: his right hand behind his hip and up (the page puts the card
                                    in it at CARD_SHOW), holding it up beside his head
            apology-video/card-hold CARD, looping
            apology-video/moved     CARD -> CARD: his lip goes, and he wipes an eye with his free hand
            apology-video/card-down CARD -> REST (the page takes the card at CARD_HIDE)
    brick   apology-video/card-up   REST -> CARD: as Zip's, from behind his back (CARD_SHOW), the card's back
                                    to the room
            apology-video/card-turn CARD -> CARD: held out a little, and turned round (the page plays the card's
                                    own `turn` at TURN_AT); a pointed look over it
            apology-video/card-hold CARD, looping
            apology-video/card-down CARD -> REST (CARD_HIDE), with a slow nod: that'll do
            (everyday: guard-hold, guard-off, raise-brow)
"""
from __future__ import annotations

import math

from mathutils import Vector

from . import _corekit as CK
from ._handkit import Hand, rest_hands
from common import blink_layer, brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "apology-video"
CAST = ("archie", "zip", "brick")
TAU = math.tau

AIM = 0.5                       # radians: Archie and his chair turned towards the camera (the page's right)
CHAIR_S = 1.2                   # the folding chair's scale (it is Zip-sized)
SEAT_FROM = 0.33                # Archie's root in front of the chair's origin
SEAT = (0.34, 0.70)             # seated: his hips this far back from his root, and this high
SAY_AT = 1.0                    # apology: he starts the lines
READ_AT = 0.5                   # sadder: his eyes on Brick's card
SOB_AT = 2.75                   # sadder: the big sob
GUNS_AT = 0.45                  # perk-up: the finger guns are out
CARD_SHOW = {"zip": 0.22, "brick": 0.4}     # card-up: the card into his hand (behind him)
CARD_HIDE = {"zip": 0.45, "brick": 0.65}    # card-down: ... and out of it
TURN_AT = 0.35                  # card-turn: the card's own `turn` starts
CARD = {"zip": (-0.4, -0.1, 1.5), "brick": (-1.05, -0.4, 2.3)}   # the right wrist, holding a card up


def V(*a):
    return Vector(a)


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_(bodies["zip"])
    if "brick" in bodies:
        out["brick"] = brick(bodies["brick"])
    return out


def wobble(t, rate=6.0):
    """A lip going: two near frequencies, so it never quite repeats."""
    return 0.5 * math.sin(TAU * rate * t) + 0.5 * math.sin(TAU * rate * 1.37 * t + 1.1)


# ------------------------------------------------------------------------------------------ archie
def archie(body):
    L = body.lib
    REST, hips, hw = L.REST, L.hips, L.hand_world
    rest = rest_hands(body)
    out = []

    def sit(p, k, hunch=0.0, back=0.0, bob=0.0):
        """k of the way down onto the chair; `hunch` rounds him over his knees, `back` throws him back."""
        hips(body, p, dy=SEAT[0] * k, dz=(SEAT[1] - body.hip_z) * k + bob, pitch=-12 * k + 4 * hunch + 6 * back)
        p.add("spine", 8 * k + 10 * hunch - 8 * back, 0, 0)
        p.add("chest", 4 * k + 10 * hunch - 10 * back, 0, 0)
        p.add("head", 12 * hunch - 14 * back, 0, 0)

    def feet(p, k):
        for sg in (1, -1):
            body.plant(p, sg, pos=(sg * 0.03 * k, -0.04 * k, 0), yaw=6 * k)

    def at(bone, off):
        return lambda p: body.where(p, bone) + V(*off)

    def between_knees(sg):
        def f(p):
            kn = (body.where(p, "shin_L") + body.where(p, "shin_R")) / 2
            return kn + V(sg * 0.075, -0.04, 0.05)
        return f

    def on_knee(sg):
        return lambda p: body.where(p, "shin_L" if sg > 0 else "shin_R") + V(sg * 0.02, -0.02, 0.1)

    relaxed, cupped = (18, 4, 12), (30, 4, 20)
    E = (0.5, 0.4, -0.6)
    states = {sg: {
        "rest": (lambda p, sg=sg: V(*rest[sg][0]), rest[sg][1], E, relaxed),
        "clasp": (between_knees(sg), hw((-sg * 0.35, -0.25, -1), (-sg, 0, 0)), (0.35, -0.25, -0.7), (52, 0, 32)),
        "knee": (on_knee(sg), hw((sg * 0.1, -1, -0.5), (0, 0, 1)), (0.6, 0.2, -0.5), cupped),
        "plead": (at("head", (sg * 0.05, -0.42, -0.42)), hw((-sg * 0.25, -0.15, 1), (-sg, 0, 0)), (0.5, 0.2, -0.7),
                  (30, 0, 20)),
        "gun": (at("chest", (sg * 0.24 + 0.1, -0.55, 0.0)), hw((0.45 - 0.2 * sg, -1, 0.05), (sg * 0.2, 0, 1)),
                (0.6, 0.2, -0.6), ((0, 90, 90), 0, -20)),
    } for sg in (1, -1)}
    # his left hand on his heart; his right with a thumbs-up, and the back of it to his brow
    states[1]["heart"] = (at("chest", (0.1, -0.36, 0.1)), hw((-0.7, -0.1, 0.7), (0, 1, 0)), (0.55, 0.1, -0.6),
                          (14, 4, 10))
    states[-1]["thumb"] = (at("chest", (-0.36, -0.5, 0.15)), hw((0.05, -1, 0.35), (1, 0, 0)), (0.6, 0.2, -0.6),
                           (88, 0, -8))
    states[-1]["brow"] = (at("head", (-0.22, -0.2, 0.46)), hw((1, 0.1, 0.15), (0, -1, 0.1)), (0.7, 0.1, 0.1),
                          (12, 8, 6))
    left, right = Hand(body, 1, states[1]), Hand(body, -1, states[-1])

    # ---- faces ----
    def sad_face(k):
        p = Pose()
        p.face.update({"grin": -1.0 * k, "frown": 0.7 * k, "flat": 0.3 * k})
        brows(p, 1.4 * k, 0.4 * k, -0.6 * k)
        p.both("lid_up", x=-10 * k)
        return p

    def cheesy_face(k):
        p = Pose(face={"ee": 0.7 * k})
        brows(p, 0.8 * k, 1.2 * k, 0.8 * k)
        return p

    def weep_face(k, t):
        w = wobble(t)
        p = Pose(face={"grin": -1.0 * k, "frown": (0.9 + 0.15 * w) * k, "open": (0.3 + 0.12 * w) * k})
        brows(p, 2.6 * k, 0.6 * k, -1.0 * k)
        return p

    # the camera, a little round to his left of where AIM points him; the cards, further round and up
    CAM = ((-4, 16), (0, 0, 10))
    ZIP_CARD = ((14, 26), (-6, 0, 30))
    BRICK_CARD = ((16, 30), (-8, 4, 46))
    TEARFUL = ((24, 8), (0, 10, 0))                               # eyes to the ceiling, head to one side

    def gaze(g, k):
        (ey, el), (nod, tilt, turn) = g
        return look((ey * k, el * k), head=(nod * k, tilt * k, turn * k))

    # ---- sit-down: REST -> SAD --------------------------------------------------------------------------
    T = 1.6
    c = Clip(f"{NAME}/sit-down", T)
    c.key(0.0, REST)

    def sitdown_solve(t, p, skel):
        k = ease("inout", smooth(0.15, 1.1, t)) + 0.04 * pulse(t, 1.05, 0.08, 0.0, 0.3)   # the chair gives
        sit(p, k, hunch=ease("inout", smooth(0.8, 1.5, t)))
        for h in (left, right):
            h(p, t, ["rest", (0.6, 1.45, "clasp", "inout")])
        feet(p, min(1.0, k))
        return p

    c.solve(sitdown_solve)
    c.layer(lambda t: sad_face(smooth(0.3, 1.2, t)) + Pose(face={"open": 0.3 * pulse(t, 1.0, 0.2, 0.2, 0.4)}) +
            look((-14 * smooth(0.9, 1.4, t), 0)))
    out.append(c)

    # ---- sad (loop) -------------------------------------------------------------------------------------
    T = 4.0
    c = CK.loop_clip(f"{NAME}/sad", T)
    c.key(0.0, REST)

    def sad_solve(t, p, skel, T=T):
        sit(p, 1.0, hunch=1.0 + 0.08 * math.sin(TAU * t / T))
        for h in (left, right):
            h(p, t, ["clasp"])
        feet(p, 1.0)
        return p

    c.solve(sad_solve)

    def sad_layer(t, T=T):
        g = pulse(t, 1.4, 0.3, 0.9, 0.4)                       # a guilty look up at the camera, and down
        p = sad_face(1.0) + look((-14 + 22 * g, 12 * g), head=(0, 0, 6 * g))
        p.both("shoulder", z=1.5 * math.sin(TAU * t / T), add=True)
        return p

    c.layer(sad_layer)
    c.layer(blink_layer([0.6, 3.3]))
    out.append(c)

    # ---- apology: SAD -> CHEESY --------------------------------------------------------------------------
    T = 3.6
    c = Clip(f"{NAME}/apology", T)
    c.key(0.0, REST)

    def apology_solve(t, p, skel):
        up = ease("inout", smooth(0.5, 1.0, t))                  # sits up to say it
        sit(p, 1.0, hunch=1.0 - 0.8 * up - 0.2 * smooth(2.2, 2.6, t))
        left(p, t, ["clasp", (0.7, 1.15, "heart", "inout"), (2.1, 2.5, "knee", "inout")])
        right(p, t, ["clasp", (2.15, 2.6, "thumb", "back")])
        feet(p, 1.0)
        return p

    c.solve(apology_solve)

    def apology_layer(t):
        sad = 1 - smooth(2.0, 2.3, t)
        p = sad_face(sad * (0.55 + 0.45 * (1 - smooth(0.5, 1.0, t)))) + cheesy_face(smooth(2.0, 2.4, t))
        talk = pulse(t, SAY_AT, 0.05, 1.0, 0.1)                   # the lines: four syllables or so
        p.face["open"] = p.face.get("open", 0.0) + 0.35 * talk * max(0.0, math.sin(TAU * 2.1 * (t - SAY_AT)))
        card = pulse(t, 0.1, 0.25, 0.35, 0.25)                   # a glance at Zip's card, then the camera
        p = p + gaze(ZIP_CARD, card) + gaze(CAM, smooth(0.8, 1.05, t) * (1 - card))
        p.add("head", 0, 0, -6 * smooth(2.25, 2.6, t))           # a cocky tilt with the thumbs-up
        return p

    c.layer(apology_layer)
    c.layer(blink_layer([0.75, 3.1]))
    out.append(c)

    # ---- cheesy (loop) -----------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/cheesy", T)
    c.key(0.0, REST)

    def cheesy_solve(t, p, skel, T=T):
        sit(p, 1.0, bob=0.006 * math.sin(TAU * 2 * t / T))
        left(p, t, ["knee"])
        right(p, t, ["thumb"])
        feet(p, 1.0)
        return p

    c.solve(cheesy_solve)
    c.layer(lambda t: cheesy_face(1.0) + gaze(CAM, 1.0) + Pose(rot={"head": (0, 0, -6)}))
    c.layer(blink_layer([1.2]))
    out.append(c)

    # ---- sadder: CHEESY -> WEEP ------------------------------------------------------------------------
    T = 4.6
    c = Clip(f"{NAME}/sadder", T)
    c.key(0.0, REST)
    W0, W1 = READ_AT + 0.3, READ_AT + 0.9                         # the thumbs-up wilting

    def sadder_solve(t, p, skel):
        plead = ease("inout", smooth(1.3, 1.75, t)) * (1 - smooth(2.45, 2.8, t))
        back = ease("out", smooth(2.45, 2.85, t))
        sob = pulse(t, SOB_AT, 0.1, 0.1, 0.5)
        sit(p, 1.0, hunch=0.25 * smooth(W0, W1, t) + 0.25 * plead - 0.25 * back, back=back * (1 + 0.15 * sob))
        left(p, t, ["knee", (1.3, 1.75, "plead", "inout"), (2.45, 2.85, "heart", "out")])
        right(p, t, ["thumb", (W0, W1, "knee", "inout"), (1.3, 1.75, "plead", "inout"), (2.45, 2.85, "brow", "out")])
        feet(p, 1.0)
        return p

    c.solve(sadder_solve)

    def sadder_layer(t):
        read = pulse(t, READ_AT - 0.3, 0.3, 0.5, 0.35)
        drop = smooth(W0, W0 + 0.4, t)
        works = smooth(1.2, 1.7, t)
        p = cheesy_face(1 - drop) + sad_face(0.6 * drop * (1 - works)) + weep_face(works, t)
        p = p + gaze(BRICK_CARD, read)
        cam = smooth(1.0, 1.4, t) * (1 - smooth(2.4, 2.7, t))   # pleading at the camera, then the ceiling
        p = p + gaze(CAM, cam) + gaze(TEARFUL, smooth(2.4, 2.8, t))
        p.add("head", 0, 0, 6 * (1 - drop))                     # (the cocky tilt, going)
        p.add("chest", -5 * pulse(t, 0.95, 0.3, 0.1, 0.3), 0, 0)   # a big breath in before the works
        sob = pulse(t, SOB_AT, 0.1, 0.1, 0.5)
        p.both("shoulder", z=6 * sob, add=True)
        p.face["open"] = p.face.get("open", 0.0) + 0.5 * sob
        return p

    c.layer(sadder_layer)
    c.layer(blink_layer([READ_AT + 0.05, 1.95]))
    out.append(c)

    # ---- weep (loop) -------------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/weep", T)
    c.key(0.0, REST)

    def weep_solve(t, p, skel, T=T):
        h = 0.5 + 0.5 * math.sin(TAU * 2 * t / T)
        sit(p, 1.0, back=1.0 + 0.04 * h)
        left(p, t, ["heart"])
        right(p, t, ["brow"])
        feet(p, 1.0)
        return p

    c.solve(weep_solve)

    def weep_layer(t, T=T):
        h = 0.5 + 0.5 * math.sin(TAU * 2 * t / T)
        p = weep_face(1.0, t) + gaze(TEARFUL, 1.0)
        p.both("shoulder", z=4 * h, add=True)
        return p

    c.layer(weep_layer)
    out.append(c)

    # ---- perk-up: WEEP -> REST ---------------------------------------------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/perk-up", T)
    c.key(0.0, REST)
    UP0, UP1 = 1.55, 2.35                                         # up off the chair

    def perk_solve(t, p, skel):
        snap = ease("snap", smooth(0.05, 0.4, t))
        k = 1 - ease("inout", smooth(UP0, UP1, t))
        sit(p, k, back=(1 - snap) * k, bob=0.03 * pulse(t, GUNS_AT, 0.08, 0.05, 0.2) - 0.03 * pulse(t, UP0, 0.2, 0, 0.3))
        left(p, t, ["heart", (0.05, 0.4, "gun", "snap"), (1.35, 2.0, "rest", "inout")])
        right(p, t, ["brow", (0.05, 0.4, "gun", "snap"), (1.35, 2.0, "rest", "inout")])
        feet(p, k)
        return p

    c.solve(perk_solve)

    def perk_layer(t):
        snap = smooth(0.05, 0.3, t)
        home = smooth(1.9, 2.5, t)
        p = weep_face(1 - snap, t) + cheesy_face(snap * (1 - home)) + gaze(TEARFUL, 1 - snap)
        p.face["grin"] = p.face.get("grin", 0.0) + 1.0 * snap        # (weep_face took it away)
        p = p + gaze(CAM, snap * (1 - smooth(1.6, 2.2, t)))
        wk = pulse(t, GUNS_AT, 0.08, 0.25, 0.15)                     # a wink with the guns
        p.side("lid_up", -1, x=-46 * wk, add=True)
        p.side("lid_lo", -1, x=40 * wk, add=True)
        return p

    c.layer(perk_layer)
    out.append(c)
    return out


# ------------------------------------------------------------------------------------- zip and brick
def card_hand(body, wrist, elbow, side=-1):
    """A pal's right hand and its states for holding a card up: hanging at rest, behind his hip (where a
    card comes from and goes), and up at `wrist`, the fist round the card's bottom edge."""
    L = body.lib
    rest = rest_hands(body)
    r_w, r_rot = rest[side]
    s = body.hip_z / 0.8
    back = r_w + V(-side * 0.05 * s, 0.3 * s, 0.1 * s)
    E = (0.5, 0.4, -0.6)
    fist = (80, 0, 44)
    return Hand(body, side, {
        "rest": (lambda p: V(*r_w), r_rot, E, (22, 4, 14)),
        "behind": (lambda p: back, L.hand_world((side * 0.2, 0.6, -1), (side, 0, 0)), (0.5, 0.6, -0.6), fist),
        "card": (lambda p: V(*wrist), L.hand_world((side * 0.15, -0.1, 1), (0, -1, 0)), elbow, fist),
    })


def zip_(body):
    L = body.lib
    REST = L.REST
    out = []
    W = CARD["zip"]
    hand = card_hand(body, W, (0.6, 0.1, -0.5))

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    # ---- card-up --------------------------------------------------------------------------------------
    T = 0.9
    c = Clip(f"{NAME}/card-up", T)
    c.key(0.0, REST)

    def up_solve(t, p, skel):
        L.hips(body, p, dz=0.03 * pulse(t, 0.3, 0.2, 0.0, 0.4))
        hand(p, t, ["rest", (0.0, 0.2, "behind", "inout"), (0.25, 0.75, "card", "back")])
        stand(p)
        return p

    c.solve(up_solve)
    c.layer(lambda t: look((10 * smooth(0.3, 0.8, t), 14 * smooth(0.3, 0.8, t))))
    out.append(c)

    # ---- card-hold (loop) --------------------------------------------------------------------------------
    T = 2.0
    c = CK.loop_clip(f"{NAME}/card-hold", T)
    c.key(0.0, REST)

    def hold_solve(t, p, skel, T=T):
        L.hips(body, p, dz=0.008 * math.sin(TAU * t / T))
        hand(p, t, ["card"])
        stand(p)
        return p

    c.solve(hold_solve)
    c.layer(lambda t, T=T: look((10, 14 + 3 * math.sin(TAU * t / T))) + L.horn_sway(t, T, 2.0))
    c.layer(blink_layer([1.3], up=L.LID_UP, lo=L.LID_LO))
    out.append(c)

    # ---- moved: a wobbly lip, and an eye wiped with his free hand ------------------------------------------
    T = 3.0
    c = Clip(f"{NAME}/moved", T)
    c.key(0.0, REST)
    rest = rest_hands(body)
    now = [0.0]

    def at_eye(p):
        # the knuckles at his eye, the wrist working to and fro
        rub = 0.03 * math.sin(TAU * 2.2 * (now[0] - 1.25)) * pulse(now[0], 1.25, 0.1, 1.0, 0.1)
        return body.where(p, "eye_L") + V(0.07 + rub, -0.14, -0.03 + 0.5 * rub)

    free = Hand(body, 1, {
        "rest": (lambda p: V(*rest[1][0]), rest[1][1], (0.5, 0.4, -0.6), (22, 4, 14)),
        "wipe": (at_eye, L.hand_world((-0.35, -0.3, 1), (-0.3, -1, -0.1)), (0.5, 0.0, -0.6), (60, 0, 30)),
    })

    def moved_solve(t, p, skel):
        now[0] = t
        sob = math.sin(TAU * 3.0 * t) * pulse(t, 0.3, 0.3, 2.0, 0.3)
        p.add("chest", 2 * sob, 0, 0)
        p.add("head", 8 * pulse(t, 0.4, 0.4, 1.8, 0.4), 0, 0)
        hand(p, t, ["card"])
        free(p, t, ["rest", (0.9, 1.25, "wipe", "inout"), (2.45, 2.9, "rest", "inout")])
        stand(p)
        return p

    c.solve(moved_solve)

    def moved_face(t):
        k = pulse(t, 0.3, 0.35, 2.0, 0.35)
        w = wobble(t, 5.0)
        p = Pose(face={"grin": -1.0 * k, "frown": (0.8 + 0.2 * w) * k, "open": 0.15 * k})
        brows(p, 2.0 * k, 0.6 * k, -0.8 * k)
        L.squint(p, 0.5 * pulse(t, 0.9, 0.3, 1.2, 0.4))
        return p + look((10 * (1 - k), 14 * (1 - k)))

    c.layer(moved_face)
    out.append(c)

    # ---- card-down ----------------------------------------------------------------------------------------
    T = 0.8
    c = Clip(f"{NAME}/card-down", T)
    c.key(0.0, REST)

    def down_solve(t, p, skel):
        hand(p, t, ["card", (0.0, 0.4, "behind", "inout"), (0.5, 0.8, "rest", "inout")])
        stand(p)
        return p

    c.solve(down_solve)
    out.append(c)
    return out


def brick(body):
    L = body.lib
    REST = L.REST
    out = []
    W = CARD["brick"]
    hand = card_hand(body, W, (0.9, 0.2, -0.7))
    hand.states["out"] = (lambda p: V(W[0] - 0.06, W[1] - 0.12, W[2] + 0.04), hand.states["card"][1],
                          (0.9, 0.2, -0.7), hand.states["card"][3])

    def stand(p):
        body.plant(p, 1, yaw=L.STANCE)
        body.plant(p, -1, yaw=L.STANCE)

    def deadpan(k=1.0):
        p = Pose(face={"smile": -0.5 * k, "flat": 0.5 * k})
        L.lids(p, 0.2 * k)
        return p

    # ---- card-up: from behind his back ------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/card-up", T)
    c.key(0.0, REST)

    def up_solve(t, p, skel):
        p.add("chest", 0, 4 * smooth(0.4, 1.2, t), 0)
        hand(p, t, ["rest", (0.0, 0.35, "behind", "inout"), (0.45, 1.25, "card", "inout")])
        stand(p)
        return p

    c.solve(up_solve)
    c.layer(lambda t: look((0, 16 * smooth(0.5, 1.2, t))) + deadpan(smooth(0.3, 1.0, t)))
    out.append(c)

    # ---- card-turn ---------------------------------------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/card-turn", T)
    c.key(0.0, REST)

    def turn_solve(t, p, skel):
        p.add("chest", 0, 4, 0)
        hand(p, t, ["card", (0.1, 0.4, "out", "inout"), (1.3, 1.75, "card", "inout")])
        stand(p)
        return p

    c.solve(turn_solve)

    def turn_face(t):
        k = pulse(t, TURN_AT + 0.4, 0.3, 0.6, 0.4)
        p = deadpan(1.0) + look((-4 * k, 16))
        p.add("head", 6 * k, 6 * k, -4 * k)                    # chin down: a pointed look over the card
        L.brows(p, -0.6 * k, -0.4 * k, 0.2 * k)
        return p

    c.layer(turn_face)
    out.append(c)

    # ---- card-hold (loop) --------------------------------------------------------------------------------
    T = 3.0
    c = CK.loop_clip(f"{NAME}/card-hold", T)
    c.key(0.0, REST)

    def hold_solve(t, p, skel, T=T):
        p.add("chest", -0.8 * math.sin(TAU * t / T), 4, 0)
        hand(p, t, ["card"])
        stand(p)
        return p

    c.solve(hold_solve)
    c.layer(lambda t: deadpan(1.0) + look((0, 16)))
    c.layer(L.blinks([1.6]))
    out.append(c)

    # ---- card-down, with a slow nod: that'll do -----------------------------------------------------------
    T = 1.8
    c = Clip(f"{NAME}/card-down", T)
    c.key(0.0, REST)

    def down_solve(t, p, skel):
        p.add("chest", 0, 4 * (1 - smooth(0.0, 0.6, t)), 0)
        hand(p, t, ["card", (0.0, 0.6, "behind", "inout"), (0.75, 1.3, "rest", "inout")])
        stand(p)
        return p

    c.solve(down_solve)

    def down_face(t):
        n = pulse(t, 0.7, 0.45, 0.15, 0.5)
        p = deadpan(1 - smooth(1.2, 1.7, t)) + look((0, 16 * (1 - smooth(1.2, 1.7, t))))
        p.add("head", 14 * n, 0, 0)
        p.add("neck", 4 * n, 0, 0)
        L.lids(p, 0.3 * n)
        return p

    c.layer(down_face)
    out.append(c)
    return out
