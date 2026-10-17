"""The emergency backup: Archie reaches for the Atlas Core and it isn't there. While he pats himself down,
Zip runs up with a potato with continents drawn on it and offers it, beaming. Archie stares at it, and takes
it. Brick plugs a cable into it. It lights up -- the continents glow and it projects the page's world, a little
crooked -- and Archie is furious.

FORMATION (metres from Archie's root, x to his left = screen right, y back, z up; everyone faces the reader):
    archie  (0, 0, 0)
    zip     (ZIP_X, ZIP_Y, 0) while he offers the potato
    brick   (BRICK_X, BRICK_Y, 0) while he plugs it in
Zip and Brick stand nearer the reader than Archie (the page's `depth`, -y times the px to the metre): that is
how their hands reach the potato in front of him, and who is drawn in front of whom.

The potato (the `potato` prop at POTATO times its size, kept level on the page: continents to the reader, its
socket on its +X end, screen right) rides a palm-up hand, upright, LIFT over the grip bone. The hand-offs meet
at shared points, which each pal's pieces put the grip itself on (`grip_to`): OFFER_AT, Zip's right grip
holding it out, where Archie's left grip takes it at TAKE_AT (at TAKE_GRIP, ARCHIE_DX along: he holds it by
its right half); HELD_AT, Archie's left grip holding it up the way he holds the Core; and PLUG_AT, Brick's
right grip holding the cable's plug (the `cable` prop at CABLE times, PLUG_OUT ahead of his grip) into the
socket at PLUG_IN.

    emergency-backup/search    archie  REST -> REST: his left hand to the Core's dock; nothing; he pats himself
                                       down and looks about him
    emergency-backup/stare     archie  REST -> REST: down at what Zip is holding out; a flat look, a slow blink
    emergency-backup/take      archie  REST -> HELD: his left hand out to the potato (the page moves it from
                                       Zip's hand to his at TAKE_AT) and up to HELD_AT
    emergency-backup/hold      archie  HELD, looping: holding it as he would the Core, eyes on it
    emergency-backup/furious   archie  HELD -> HELD: stamping, his right fist shaking, glaring at it
    emergency-backup/offer     zip     REST -> OFFER: the potato (in his right hand since he ran in) held out to
                                       Archie at OFFER_AT, beaming
    emergency-backup/offer-hold zip    OFFER, looping: up on his toes, bouncing
    emergency-backup/let-go    zip     OFFER -> REST: his hand back, empty (once Archie has it)
    emergency-backup/plug      brick   REST -> REST: the plug, held in his right hand, to the socket (PLUG_IN: the
                                       page leaves it there), a push, his hand back
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import blink_layer, brows, look
from kit.anim import Clip, Pose, pulse, smooth

NAME = "emergency-backup"
CAST = ("archie", "zip", "brick")
ZIP_X, ZIP_Y = 1.0, -0.5
BRICK_X, BRICK_Y = 1.75, -0.35
POTATO, CABLE = 2.4, 1.8                   # the props' scales on the page (a potato you can see from the back row)
LIFT = 0.07                                # the potato's middle, above a palm-up grip
OFFER_AT = Vector((0.56, -0.55, 1.06))     # Zip's right grip, holding it out (Archie's frame)
ARCHIE_DX = 0.08                           # Archie's grip, this far to the right of its middle (screen left)
TAKE_GRIP = OFFER_AT - Vector((ARCHIE_DX, 0, 0))   # ... where his left grip takes it from Zip's hand
HELD_AT = Vector((0.1, -0.58, 1.32))       # his left grip holding it up (where the Core would be)
POTATO_HELD = HELD_AT + Vector((ARCHIE_DX, 0, LIFT))
SOCKET = 0.08 * POTATO                     # the socket, from the potato's middle (its +X end)
PLUGGED = SOCKET + 0.035 * CABLE           # the plug's grip point, in the socket
PLUG_OUT = 0.05                            # the plug, that far ahead of Brick's grip (towards the socket)
PLUG_AT = POTATO_HELD + Vector((PLUGGED + PLUG_OUT, 0, 0))   # Brick's right grip holding the plug in
TAKE_AT = 0.75                             # take: Archie's grip reaches it, and the page hands it over
PLUG_IN = 1.05                             # plug: the plug goes in
GLOW = 0.25                                # ... and the potato lights up this long after


def V(*a):
    return Vector(a)


def grip_to(body, p, side, target, elbow, hand_rot):
    """Put the hand's grip bone (not the wrist) on `target`: hand_to aims the wrist, so solve, see where the
    grip landed, and aim again by the miss."""
    s = "_L" if side > 0 else "_R"
    target = Vector(target)
    aim = target.copy()
    for _ in range(3):
        body.hand_to(p, side, aim, elbow=elbow, hand_rot=hand_rot)
        g = body.skel.fk(p, f"grip{s}")[f"grip{s}"].translation
        aim = aim + (target - g)
    return p


def rest_wrist(body, side):
    q = body.lib.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    return body.lib.wrist_of(body, q, side)


def rest_grip(body, side):
    q = body.lib.REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    s = "_L" if side > 0 else "_R"
    return body.skel.fk(q, f"grip{s}")[f"grip{s}"].translation.copy()


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"])
    return out


# --------------------------------------------------------------------------------------------- Archie
def archie_clips(body):
    L = body.lib
    REST, hips, open_hand, hand_world, fist = L.REST, L.hips, L.open_hand, L.hand_world, L.fist
    n = lambda piece: f"{NAME}/{piece}"
    rw = {1: rest_wrist(body, 1), -1: rest_wrist(body, -1)}
    PALM_UP = hand_world((-0.35, -0.9, 0.05), (0, 0, 1))
    ELBOW = (0.55, 0.35, -0.5)
    DOCK = V(0.12, -0.22, 1.205)                       # where his left hand takes the Core from (_corekit)
    out = []

    def held(p, at=HELD_AT):
        grip_to(body, p, 1, at, ELBOW, PALM_UP)
        p.fingers(1, 30, spread=6, thumb=20)

    HOLD = REST.copy()
    HOLD.set("head", 10, 6, -3)
    HOLD.set("chest", 2, 4, 0)
    eyes_on = lambda k: look((-18 * k, 14 * k))

    # ---- search: the dock is empty ----------------------------------------------------------------------
    T = 3.2
    c = Clip(n("search"), T)
    c.key(0.0, REST)
    down = REST.copy()
    down.set("head", 24, 0, 0)
    down.set("chest", 8, 0, 0)
    down.face = {"flat": 0.6}
    panic = REST.copy()
    panic.set("head", -4, 0, 0)
    panic.face = {"wide": 1.0, "oh": 0.6}
    c.key(0.5, down, "inout")
    c.key(1.7, down, "linear")
    c.key(2.0, panic, "snap")
    c.key(T - 0.4, panic, "linear")
    c.key(T, REST, "inout")

    def search_solve(t, p, skel, T=T):
        hips(body, p, dz=-0.03 * pulse(t, 0.3, 0.3, 1.2, 0.3))
        k = pulse(t, 0.0, 0.45, 0.35, 0.3)              # his left hand to the dock, and away: nothing
        if k > 0.01:
            body.hand_to(p, 1, rw[1].lerp(DOCK, k), elbow=ELBOW, hand_rot=hand_world((-0.3, -0.2, -1), (-1, 0, 0)))
        pat = pulse(t, 1.05, 0.2, 0.5, 0.25)            # both hands patting his belly, twice
        if pat > 0.01:
            tap = 0.04 * abs(math.sin(math.tau * (t - 1.05) / 0.3))
            for sg in (1, -1):
                body.hand_to(p, sg, rw[sg].lerp(V(0.2 * sg, -0.3 - tap, 1.1), pat), elbow=(0.5, 0.3, -0.6),
                             hand_rot=hand_world((-sg * 0.4, -0.2, -0.9), (-sg, -0.4, 0)) if pat > 0.5 else None)
                open_hand(p, sg, 6)
        up = pulse(t, 2.0, 0.15, T - 2.6, 0.4)          # hands up: gone!
        if up > 0.01:
            for sg in (1, -1):
                body.hand_to(p, sg, rw[sg].lerp(V(0.55 * sg, -0.3, 1.55), up), elbow=(0.6, 0.4, -0.4),
                             hand_rot=hand_world((0, -0.1, 1), (0, -1, 0)) if up > 0.5 else None)
                open_hand(p, sg, 14)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(search_solve)
    c.layer(lambda t: look((0, 30 * math.sin(math.tau * (t - 2.0) / 1.0) * pulse(t, 2.0, 0.1, 0.8, 0.2))))
    out.append(c)

    # ---- stare: down at the thing Zip is holding out ----------------------------------------------------
    T = 2.2
    c = Clip(n("stare"), T)
    c.key(0.0, REST)
    at_it = REST.copy()
    at_it.set("head", 16, 18, 4)
    at_it.face = {"flat": 1.0}
    c.key(0.45, at_it, "inout")
    c.key(T - 0.4, at_it, "linear")
    c.key(T, REST, "inout")
    c.solve(lambda t, p, skel: (body.plant(p, 1), body.plant(p, -1), p)[-1])

    def stare_face(t, T=T):
        p = Pose()
        b = pulse(t, 1.0, 0.25, 0.25, 0.35)              # the slow blink
        p.both("lid_up", x=-46 * b - 10 * (1 - b) * pulse(t, 0.4, 0.3, T - 1.0, 0.3))
        return p + look((-16 * pulse(t, 0.3, 0.3, T - 0.9, 0.3), 24 * pulse(t, 0.3, 0.3, T - 0.9, 0.3)))

    c.layer(stare_face)
    out.append(c)

    # ---- take: his left hand out to the potato, and up -------------------------------------------------
    T = 1.7
    c = Clip(n("take"), T)
    c.key(0.0, REST)
    c.key(0.6, at_it, "inout")
    c.key(T, HOLD, "inout")
    take_rot = hand_world((-0.1, -0.6, -0.1), (0, 0, 1))

    g0 = rest_grip(body, 1)

    def take_solve(t, p, skel, T=T):
        if t < TAKE_AT:
            k = smooth(0.05, TAKE_AT, t)
            if k > 0.01:
                grip_to(body, p, 1, g0.lerp(TAKE_GRIP, k), (0.6, 0.3, -0.5), take_rot if k > 0.4 else None)
        else:
            k = smooth(TAKE_AT, T - 0.1, t)
            grip_to(body, p, 1, TAKE_GRIP.lerp(HELD_AT, k), ELBOW if k > 0.5 else (0.6, 0.3, -0.5),
                    PALM_UP if k > 0.5 else take_rot)
        p.fingers(1, 30, spread=6, thumb=20)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(take_solve)
    c.layer(lambda t, T=T: look((-16 * (1 - smooth(1.0, T, t)), 24 * (1 - smooth(1.0, T, t)))) + eyes_on(smooth(1.0, T, t)))
    c.layer(lambda t: Pose(face={"flat": 1.0, "grin": -1.0}))
    out.append(c)

    # ---- hold ------------------------------------------------------------------------------------------
    T = 4.0
    c = Clip(n("hold"), T, frames=120)
    c.key(0.0, HOLD)

    def hold_solve(t, p, skel, T=T):
        held(p, HELD_AT + V(0, 0, 0.008 * math.sin(math.tau * t / T)))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(hold_solve)
    c.layer(lambda t: eyes_on(1.0) + Pose(face={"flat": 0.8, "grin": -0.8}))
    c.layer(blink_layer([1.6]))
    out.append(c)

    # ---- furious ---------------------------------------------------------------------------------------
    T = 3.2
    c = Clip(n("furious"), T)
    c.key(0.0, HOLD)
    rage = HOLD.copy()
    rage.set("head", 6, 4, 0)
    rage.set("chest", 8, 0, 0)
    rage.face = {"grit": 1.0, "frown": 0.8, "grin": -1.0}
    c.key(0.3, rage, "snap")
    c.key(T - 0.4, rage, "linear")
    c.key(T, HOLD, "inout")
    stamps = (0.45, 1.05)

    def furious_solve(t, p, skel, T=T):
        e = pulse(t, 0.15, 0.25, T - 0.75, 0.35)
        shake = math.sin(math.tau * t * 7) * e
        stamp = max(pulse(t, s - 0.15, 0.15, 0.0, 0.1) for s in stamps)
        hips(body, p, dz=-0.03 * e + 0.03 * stamp, pitch=4 * e)
        p.add("chest", 3 * shake, 0, 0)
        held(p)                                         # (on the hips and chest, so the potato stays put)
        if e > 0.01:
            body.hand_to(p, -1, rw[-1].lerp(V(-0.42, -0.42, 1.45 + 0.04 * shake), e), elbow=(0.5, 0.2, -0.6),
                         hand_rot=hand_world((0.1, -0.3, 1), (1, 0, 0)) if e > 0.5 else None)
            fist(p, -1, e)
        body.plant(p, 1)
        body.plant(p, -1, lift=0.12 * stamp)
        return p

    c.solve(furious_solve)

    def furious_face(t, T=T):
        p = Pose()
        e = pulse(t, 0.15, 0.2, T - 0.7, 0.35)
        brows(p, -1.8 * e, -0.8 * e, 0.6 * e)
        return p + eyes_on(1.0)

    c.layer(furious_face)
    out.append(c)
    return out


# ------------------------------------------------------------------------------------------------ Zip
def zip_clips(body):
    L = body.lib
    REST, hand_world = L.REST, L.hand_world
    n = lambda piece: f"{NAME}/{piece}"
    g0 = rest_grip(body, -1)
    at = OFFER_AT - V(ZIP_X, ZIP_Y, 0)               # the potato, in his own frame: out to his right
    rot = hand_world((-0.55, -0.8, 0.0), (0, 0, 1))  # palm up, fingers out to Archie
    elbow = (0.5, 0.2, -0.6)
    OFFER = REST.copy()
    OFFER.set("head", 6, -14, -4)
    OFFER.set("chest", -2, -8, 0)
    OFFER.face = {"grin": 1.0, "wide": 0.4}

    def offer_arm(p, k):
        if k > 0.01:
            grip_to(body, p, -1, g0.lerp(at, k), elbow, rot if k > 0.3 else None)
        p.fingers(-1, 26, spread=6, thumb=18)

    T = 1.2
    c = Clip(n("offer"), T)
    c.key(0.0, REST)
    c.key(T, OFFER, "back")

    def offer_solve(t, p, skel, T=T):
        L.hips(body, p, dz=0.03 * pulse(t, 0.7, 0.2, 0.0, 0.3))
        offer_arm(p, smooth(0.0, T - 0.15, t))
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(offer_solve)
    c.layer(lambda t, T=T: look((-10 * smooth(0.4, T, t), -20 * smooth(0.4, T, t))))
    out = [c]

    T = 1.2
    c = L.looped(n("offer-hold"), T)
    c.key(0.0, OFFER)

    def hold_solve(t, p, skel, T=T):
        bob = 0.5 - 0.5 * math.cos(math.tau * t / (T / 2))
        L.hips(body, p, dz=0.035 * bob)
        offer_arm(p, 1.0)
        body.plant(p, 1, roll=18 * bob)
        body.plant(p, -1, roll=18 * bob)
        return p

    c.solve(hold_solve)
    c.layer(lambda t, T=T: look((-10, -20)) + L.horn_sway(t, T / 2, 3.0))
    out.append(c)

    T = 0.8
    c = Clip(n("let-go"), T)
    c.key(0.0, OFFER)
    c.key(T, REST, "inout")

    def let_go_solve(t, p, skel, T=T):
        k = 1 - smooth(0.0, T, t)
        offer_arm(p, k)
        p.fingers(-1, 26 * k + 18 * (1 - k), spread=6, thumb=18)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(let_go_solve)
    out.append(c)
    return out


# ---------------------------------------------------------------------------------------------- Brick
def brick_clips(body):
    L = body.lib
    REST, hand_world = L.REST, L.hand_world
    n = lambda piece: f"{NAME}/{piece}"
    g0 = rest_grip(body, -1)
    at = PLUG_AT - V(BRICK_X, BRICK_Y, 0)            # the plug in the socket, in his own frame
    rot = hand_world((-1, -0.05, 0.0), (0, 0, -1))   # fingers pointing at the socket, palm down
    T = 2.4
    c = Clip(n("plug"), T)
    c.key(0.0, REST)
    lean = REST.copy()
    lean.set("head", 14, -10, 0)
    lean.set("chest", 10, -8, 0)
    c.key(0.6, lean, "inout")
    c.key(T - 0.5, lean, "linear")
    c.key(T, REST, "inout")

    def plug_solve(t, p, skel, T=T):
        k = pulse(t, 0.1, PLUG_IN - 0.25, 0.55, T - PLUG_IN - 0.45)
        push = 0.04 * (1 - smooth(PLUG_IN - 0.2, PLUG_IN, t)) if t < PLUG_IN + 0.3 else 0.0
        L.hips(body, p, dz=-0.06 * k, pitch=6 * k)
        if k > 0.01:
            grip_to(body, p, -1, g0.lerp(at + V(push, 0, 0), k), (0.8, -0.1, -0.5), rot if k > 0.4 else None)
        p.fingers(-1, 40, spread=0, thumb=30)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(plug_solve)
    c.layer(lambda t: look((-14 * pulse(t, 0.3, 0.4, 1.2, 0.4), -26 * pulse(t, 0.3, 0.4, 1.2, 0.4))))
    return [c]
