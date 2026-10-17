"""The fake crash: Archie's own face shows an error. Brick opens his back panel and finds Zip inside,
operating him with two levers.

Archie is waving hello when he freezes, and a blue screen comes on over his face (the error-face prop). Brick
ambles over, peers at him, knocks on his head twice -- nothing -- and flicks his crest, which spins him round
to face away. Brick steps up and opens the door in his back (his left back plate, on the `hatch` bone): in
the bay behind it, tiny Zip is at a control box, pumping its two levers -- and Archie's raised arm and head
are going with them. Zip freezes, looks back over his shoulder at Brick, and gives a very small wave. Brick
looks at the reader. He shuts the door. A moment later Archie turns round on his own, the screen goes off,
"Rebooted! Good as new." -- and he walks off with a stiff, puppetish walk. Brick raises a brow at the reader.

THE LAYOUT, in metres on the floor (the page's x is a pal's x when he faces the reader; -y is towards the
reader): Archie's root at the origin; Brick's at (D1, 0) for the peer, knock and flick and at (D2, 0) once he
has stepped up, facing the reader -- so his right arm reaches across the page to Archie, in plain view. Archie turns from facing the reader (0) to facing away (SPIN: -pi, so he
spins away from Brick). Tiny Zip, K of his size, stands in the bay on the ledge (archie.py's `bay` bone),
facing screen left, with the control box (props_set.py, BOX of Zip's size) in front of him, SPAN ahead.

Every contact is a fingertip: Brick's right index, on targets in Archie's frame moved into Brick's.

    archie: fake-crash/hello (waves; freezes at CRASH)  frozen (loop)  knocked (with Brick's knock)
            spun (while the page spins him)  door (with Brick's open)  driven (loop: the levers have him)
            held (loop: door open, still)  shut (with Brick's close)  reboot  puppet (a walk, mps WALK)
    brick:  fake-crash/peer  knock  flick  open  stare  close
    zip:    fake-crash/levers (loop, with the box's operate)  caught
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import brows, look
from kit.anim import Clip, Pose, ease, pulse, smooth

NAME = "fake-crash"
CAST = ("archie", "brick", "zip")
D1, D2 = 1.7, 1.6                # Brick's root to the right of Archie's: peering and knocking; at the door
K = 0.09                         # tiny Zip, to Archie's metres
BOX, SPAN = 2.6, 0.44            # the control box at Zip's scale, and its middle ahead of him (his metres)
CRASH = 1.5                      # hello: he freezes
KNOCKS = (0.8, 1.25)             # knock: the tip lands
PINCH, FLICK = 0.75, 1.1         # flick: on the crest; the flick (the page spins him from here, over SPIN_SECS)
SPIN, SPIN_SECS = -math.pi, 0.9
HOOK, OPEN0, OPEN1 = 0.7, 0.8, 1.45          # open: the tip on the door's edge; the swing
OPEN_DEG = 120                   # the door swings round towards his side, out of the bay's way
SHUT0, SHUT1 = 0.55, 1.05        # close: the swing back
LEVER = 1.2                      # the box's `operate` loop (props_set.py: 25 sin(tau t / 1.2) degrees)
DOOR_EDGE = (0.07, 0.165, 1.46)  # the door's free edge, where Brick's finger hooks it (Archie's frame, shut)
KNOCK_AT = (0.13, 0.02, 2.02)    # the top of his head, Brick's side
FACE_AT = (0.0, -0.3, 1.9)       # his face, for Brick to peer at


def V(*a):
    return Vector(a)


def rz(v, a):
    c, s = math.cos(a), math.sin(a)
    return V(c * v[0] - s * v[1], s * v[0] + c * v[1], v[2])


def to_brick(p, theta=0.0, d=D1):
    """A point of Archie's (his frame, him turned `theta`) in Brick's frame, Brick at (d, 0) facing the
    reader."""
    return rz(V(*p), theta) - V(d, 0, 0)


def door_edge(phi_deg, hinge):
    """The door's free edge in Archie's frame, the door `phi_deg` open about its hinge (x, y). (It is on his
    left: it opens turning -z, its free edge swinging back and out.)"""
    e = V(*DOOR_EDGE)
    r = rz(e - V(hinge.x, hinge.y, e.z), -math.radians(phi_deg))
    return V(hinge.x + r.x, hinge.y + r.y, e.z)


def lever(t):
    """The box's levers at t into `operate`: (left, right) degrees."""
    a = 25 * math.sin(math.tau * t / LEVER)
    return a, -a


def clips(bodies):
    out = {}
    if "archie" in bodies:
        out["archie"] = archie_clips(bodies["archie"])
    if "brick" in bodies:
        out["brick"] = brick_clips(bodies["brick"], bodies.get("archie"))
    if "zip" in bodies:
        out["zip"] = zip_clips(bodies["zip"])
    return out


# ------------------------------------------------------------------------------------------- archie
def archie_clips(body):
    L = body.lib
    REST, hips, hand_world, open_hand = L.REST, L.hips, L.hand_world, L.open_hand
    RW = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    out = []
    WAVE = V(-0.5, -0.12, 1.86)                     # his right wrist, up by his head, waving

    def raised(p, k, wave=0.0, bob=0.0):
        tgt = RW[-1].lerp(WAVE + V(0.07 * wave, 0, bob), k)
        body.hand_to(p, -1, tgt, elbow=(0.5, -0.4, -0.5),          # elbow forward: from behind, clear of the bay
                     hand_rot=hand_world((-0.25 + 0.5 * wave, -0.1, 1), (0, -1, 0)) if k > 0.5 else None)
        open_hand(p, -1, 12 * k)

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    frozen_face = {"grin": 0.6, "open": 0.4}

    # ---- hello: a cheery wave, and, mid-wave, the freeze -----------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/hello", T)
    c.key(0.0, REST)
    hi = REST.copy()
    hi.face = {"grin": 0.6, "open": 0.4}
    c.key(0.5, hi)
    c.key(T, hi, "linear")

    def hello(t, p, skel):
        up = ease("inout", smooth(0.0, 0.5, t))
        live = 1 - smooth(CRASH, CRASH + 0.02, t)
        w = math.sin(math.tau * 2.2 * min(t, CRASH))   # the wave stops where it is
        jolt = pulse(t, CRASH, 0.03, 0.02, 0.12)
        hips(body, p, dz=0.01 * jolt)
        p.add("head", 4 * jolt, 0, -3 * jolt)
        p.add("head", 0, 0, 5 * up * live)
        raised(p, up, wave=w)
        stand(p)
        return p

    c.solve(hello)
    c.layer(lambda t: look((6 * (1 - smooth(CRASH, CRASH + 0.05, t)), 0)))
    out.append(c)
    W_FROZEN = math.sin(math.tau * 2.2 * CRASH)

    def frozen_pose(p, wave_add=0.0, bob=0.0):
        raised(p, 1.0, wave=W_FROZEN + wave_add, bob=bob)

    # ---- frozen: stuck, with a glitch now and then ------------------------------------------------------
    T = 2.4
    c = Clip(f"{NAME}/frozen", T, loop=True)
    held = REST.copy()
    held.face = dict(frozen_face)
    c.key(0.0, held)
    c.key(T, held, "linear")

    def frozen(t, p, skel):
        g = pulse(t, 0.7, 0.03, 0.04, 0.04) - pulse(t, 1.75, 0.03, 0.05, 0.05)
        p.add("head", 2.5 * g, 0, 3 * g)
        frozen_pose(p, wave_add=0.15 * g)
        stand(p)
        return p

    c.solve(frozen)
    out.append(c)

    # ---- knocked: his head nods under each knock --------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/knocked", T)
    c.key(0.0, held)
    c.key(T, held, "linear")

    def knocked(t, p, skel):
        n = sum(pulse(t, k + 0.02, 0.04, 0.0, 0.25) for k in KNOCKS)
        p.add("head", 5 * n, 0, -2 * n)
        p.add("neck", 2 * n, 0, 0)
        frozen_pose(p, bob=-0.01 * n)
        stand(p)
        return p

    c.solve(knocked)
    out.append(c)

    # ---- spun: stiff as a board while the page turns him, a wobble as he stops --------------------------
    T = 1.2
    c = Clip(f"{NAME}/spun", T)
    c.key(0.0, held)
    c.key(T, held, "linear")

    def spun(t, p, skel):
        wob = math.sin(math.tau * 2.4 * t) * math.exp(-3.0 * max(0.0, t - SPIN_SECS)) * smooth(0.6, SPIN_SECS, t)
        hips(body, p, roll=2.0 * wob)
        p.add("head", 0, 0, -3 * wob)
        frozen_pose(p)
        stand(p)
        return p

    c.solve(spun)
    out.append(c)

    # ---- the door: open with Brick's finger, then the levers have him -----------------------------------
    def door_at(p, phi):
        p.set("hatch", 0, -phi, 0)                     # archie.py: the left door opens turning -Y

    T = 1.8
    c = Clip(f"{NAME}/door", T)
    c.key(0.0, held)
    c.key(T, held, "linear")

    def door(t, p, skel):
        door_at(p, OPEN_DEG * ease("inout", smooth(OPEN0, OPEN1, t)))
        frozen_pose(p)
        stand(p)
        return p

    c.solve(door)
    out.append(c)

    c = Clip(f"{NAME}/driven", LEVER, loop=True)
    c.key(0.0, held)
    c.key(LEVER, held, "linear")

    def driven(t, p, skel):
        left, right = lever(t)
        door_at(p, OPEN_DEG)
        p.add("head", 0, 0.3 * left, 0)                # his head turns with the near lever
        frozen_pose(p, wave_add=right / 25 * 0.5, bob=0.03 * right / 25)
        stand(p)
        return p

    c.solve(driven)
    out.append(c)

    c = Clip(f"{NAME}/held", 2.0, loop=True)
    c.key(0.0, held)
    c.key(2.0, held, "linear")

    def held_open(t, p, skel):
        door_at(p, OPEN_DEG)
        frozen_pose(p)
        stand(p)
        return p

    c.solve(held_open)
    out.append(c)

    T = 1.4
    c = Clip(f"{NAME}/shut", T)
    c.key(0.0, held)
    c.key(T, held, "linear")

    def shut(t, p, skel):
        door_at(p, OPEN_DEG * (1 - ease("in", smooth(SHUT0, SHUT1, t))))
        jolt = pulse(t, SHUT1, 0.02, 0.02, 0.15)
        hips(body, p, dy=-0.01 * jolt)
        frozen_pose(p)
        stand(p)
        return p

    c.solve(shut)
    out.append(c)

    # ---- reboot: the arm down, a shake of the head, blink blink, and the grin back -----------------------
    T = 2.6
    c = Clip(f"{NAME}/reboot", T)
    c.key(0.0, held)
    c.key(0.9, held, "linear")
    c.key(1.6, REST)
    c.key(T, REST, "linear")

    def reboot(t, p, skel):
        down = ease("inout", smooth(0.9, 1.6, t))
        jerk = sum(pulse(t, a, 0.03, 0.05, 0.08) for a in (0.3, 0.55))
        p.add("head", 0, 0, 4 * jerk)
        shake = math.sin(math.tau * 4 * t) * pulse(t, 1.6, 0.1, 0.35, 0.2)
        p.add("head", 0, 9 * shake, 0)
        if down < 1:
            raised(p, 1 - down, wave=W_FROZEN * (1 - down))
        stand(p)
        return p

    c.solve(reboot)

    def reboot_face(t):
        p = Pose()
        b = max(pulse(t, 1.15, 0.05, 0.03, 0.06), pulse(t, 1.4, 0.05, 0.03, 0.06), pulse(t, 2.2, 0.06, 0.04, 0.1))
        p.both("lid_up", x=-46 * b)
        p.both("lid_lo", x=40 * b)
        brows(p, 1.0 * pulse(t, 1.9, 0.2, 0.4, 0.3), 1.4 * pulse(t, 1.9, 0.2, 0.4, 0.3), 1.0)
        return p

    c.layer(reboot_face)
    out.append(c)

    # ---- puppet: his walk, but someone else is doing the arms -------------------------------------------
    walk = L.walk(body, name="_walk")
    TW = walk.seconds
    c = Clip(f"{NAME}/puppet", TW, loop=True, frames=walk.frames)
    c.key(0.0, REST)

    def puppet(t, p, skel):
        q = walk.at(t, skel)
        # the arms: straight, swung in jerks (held, then snapped to the next place), not swinging
        u = (t / TW) % 1.0
        step = math.floor(u * 4) / 4 + ease("inout", smooth(0.0, 0.3, (u * 4) % 1.0)) / 4
        sw = math.sin(math.tau * step)
        for sg in (1, -1):
            q.side("upper_arm", sg, x=-28 * sw * sg, z=-50, add=False)
            q.side("forearm", sg, x=4, add=False)
        q.add("head", 0, 6 * math.sin(math.tau * step * 2), 0)
        return q

    c.solve(puppet)
    out.append(c)
    return out


# -------------------------------------------------------------------------------------------- brick
def brick_clips(body, archie):
    L = body.lib
    REST, hips, point, hand_world = L.REST, L.hips, L.point, L.hand_world
    RW = {sg: L.wrist_of(body, REST, sg) for sg in (1, -1)}
    TIP = 0.58                                         # wrist to index tip, pointing
    out = []
    crest = V(0.19, -0.212, 2.473)
    hinge = V(0.2506, 0.0647, 1.54)
    if archie is not None:
        crest = archie.where(archie.lib.REST, "crest_3", at="tail")
        hinge = archie.where(archie.lib.REST, "hatch")

    def tip_to(p, k, target, along, palm=(0, -1, 0), elbow=(0.5, 0.6, -0.5)):
        """His right index tip on `target` (his frame), the finger along `along`, eased in by k."""
        hand = hand_world(along, palm)
        wrist = V(*target) - hand.col[1] * TIP
        body.hand_to(p, -1, RW[-1].lerp(wrist, k), elbow=elbow, hand_rot=hand if k > 0.4 else None)
        if k > 0.15:
            point(p, -1)

    def lean_in(p, k, roll=8, dx=-0.08, pitch=4, dz=-0.03):
        """Leaning towards Archie, who is to his right (screen left): over from the hips."""
        hips(body, p, dx=dx * k, dz=dz * k, pitch=pitch * k, roll=roll * 0.4 * k)
        p.add("spine", 2 * k, 0, roll * 0.35 * k)
        p.add("chest", 2 * k, 0, roll * 0.25 * k)

    def stand(p, **feet):
        body.plant(p, 1)
        body.plant(p, -1)

    def head_to(p, target, k, extra=(0, 0, 0)):
        """Turn his head and eyes towards a point of his frame."""
        h = body.where(REST, "head")
        d = V(*target) - h
        yaw = math.degrees(math.atan2(d.x, -d.y))
        pitch = -math.degrees(math.atan2(d.z, math.hypot(d.x, d.y)))
        yaw = max(-75.0, min(75.0, yaw))
        p.add("head", (pitch * 0.6 + extra[0]) * k, (yaw * 0.6 + extra[1]) * k, extra[2] * k)
        p.add("neck", pitch * 0.3 * k, yaw * 0.3 * k, 0)

    # ---- peer: leans in and looks at the blue screen, a brow up ----------------------------------------
    T = 2.6
    c = Clip(f"{NAME}/peer", T)
    c.key(0.0, REST)
    c.key(T, REST)
    face_b = to_brick(FACE_AT)

    def peer(t, p, skel):
        k = pulse(t, 0.2, 0.7, 1.2, 0.5)
        lean_in(p, k, roll=14, dx=-0.12, pitch=8)
        head_to(p, face_b, k, extra=(0, 0, 8 * smooth(0.9, 1.4, t)))
        stand(p)
        return p

    c.solve(peer)
    c.layer(lambda t: L.brows(Pose(), 0, 0.6 * pulse(t, 1.0, 0.3, 0.8, 0.4), 1.2 * pulse(t, 1.0, 0.3, 0.8, 0.4),
                              side=-1))
    out.append(c)

    # ---- knock: two taps on the top of his head ---------------------------------------------------------
    T = 2.0
    c = Clip(f"{NAME}/knock", T)
    c.key(0.0, REST)
    c.key(T, REST)
    knock = to_brick(KNOCK_AT)

    def knock_(t, p, skel):
        k = pulse(t, 0.0, 0.55, 0.95, 0.45)
        lean_in(p, k, roll=6)
        lift = 0.08 * (1 - max(pulse(t, KNOCKS[0] - 0.12, 0.12, 0.0, 0.14), pulse(t, KNOCKS[1] - 0.12, 0.12, 0.0, 0.14)))
        lift = lift if t > KNOCKS[0] - 0.12 else 0.08
        tip_to(p, k, knock + V(0, 0, lift), (-0.5, -0.2, -1), palm=(0, -1, 0.2))
        head_to(p, knock, k)
        stand(p)
        return p

    c.solve(knock_)
    out.append(c)

    # ---- flick: finger and thumb on the crest's tip, and a flick that sends him spinning ----------------
    T = 2.2
    c = Clip(f"{NAME}/flick", T)
    c.key(0.0, REST)
    c.key(T, REST)
    at = to_brick(crest)
    away = to_brick(crest + V(crest.y, -crest.x, 0) * 0.35) - at    # along the spin (turning him -z), briefly

    def flick(t, p, skel):
        k = pulse(t, 0.0, PINCH, FLICK - PINCH + 0.05, 0.9)
        lean_in(p, k, roll=6, pitch=2)
        f = ease("out", smooth(FLICK - 0.02, FLICK + 0.1, t))
        tip_to(p, k, at + away * f, (-1, -0.2, 0.25), palm=(0, 0, -1))
        # the thumb to the finger for the pinch, open for the flick
        p.add("thumb_1_R", 30 * smooth(0.5, PINCH, t) * (1 - f), 0, 0)
        head_to(p, at, k)
        stand(p)
        return p

    c.solve(flick)
    out.append(c)

    # ---- open: a finger hooked on the door's edge, and round it swings ----------------------------------
    T = 1.8
    c = Clip(f"{NAME}/open", T)
    c.key(0.0, REST)
    c.key(T, REST)

    def edge_b(phi):
        return to_brick(door_edge(phi, hinge), SPIN, D2)

    def open_(t, p, skel):
        k = pulse(t, 0.0, HOOK, OPEN1 - HOOK + 0.05, 0.3)
        lean_in(p, k, roll=14, dx=-0.1, pitch=10, dz=-0.08)
        phi = OPEN_DEG * ease("inout", smooth(OPEN0, OPEN1, t))
        tip_to(p, k, edge_b(phi), (-1, -0.3, -0.35), palm=(0, 1, 0), elbow=(0.5, 0.2, -0.6))
        head_to(p, edge_b(phi), k)
        stand(p)
        return p

    c.solve(open_)
    out.append(c)

    # ---- stare: into the bay; then at the reader ---------------------------------------------------------
    T = 3.2
    c = Clip(f"{NAME}/stare", T)
    c.key(0.0, REST)
    c.key(T, REST)
    bay = to_brick(V(0.165, 0.095, 1.4), SPIN, D2)

    def stare(t, p, skel):
        k = pulse(t, 0.0, 0.5, 1.0, 0.4)
        lean_in(p, k, roll=7, dx=-0.05, pitch=6)
        r = pulse(t, 1.9, 0.25, 0.7, 0.3)               # then to the reader, straight ahead
        head_to(p, bay, k * (1 - r))
        stand(p)
        return p

    c.solve(stare)

    def stare_face(t):
        p = Pose()
        r = pulse(t, 1.9, 0.25, 0.7, 0.3)
        p = p + look((0, -16 * (1 - r) * smooth(0.2, 0.6, t)))
        L.brows(p, 0, 0.8 * r, 1.6 * r, side=-1)
        return p

    c.layer(stare_face)
    out.append(c)

    # ---- close: the door pushed shut ---------------------------------------------------------------------
    T = 1.4
    c = Clip(f"{NAME}/close", T)
    c.key(0.0, REST)
    c.key(T, REST)

    def close(t, p, skel):
        k = pulse(t, 0.0, SHUT0, SHUT1 - SHUT0 + 0.05, 0.3)
        lean_in(p, k, roll=14, dx=-0.1, pitch=10, dz=-0.08)
        phi = OPEN_DEG * (1 - ease("in", smooth(SHUT0, SHUT1, t)))
        tip_to(p, k, edge_b(phi) + V(0, -0.04, 0), (-1, 0.3, -0.35), palm=(0, -1, 0), elbow=(0.5, 0.2, -0.6))
        head_to(p, edge_b(phi), k)
        stand(p)
        return p

    c.solve(close)
    out.append(c)
    return out


# ---------------------------------------------------------------------------------------------- zip
def zip_clips(body):
    L = body.lib
    REST, hips, fist, hand_world = L.REST, L.hips, L.fist, L.hand_world
    out = []

    def knob(side, a):
        """A lever's knob (props_set.py control_box: the pivot 0.176 up at x +-0.08, the knob 0.17 above
        it, tipping forward for a positive angle), in Zip's frame: the box SPAN ahead of him, BOX his size."""
        return V(side * 0.08 * BOX, -SPAN + BOX * (-0.17 * math.sin(math.radians(a))),
                 BOX * (0.176 + 0.17 * math.cos(math.radians(a))))

    def on_levers(p, t, k=1.0, let_go=0.0):
        left, right = lever(t)
        hips(body, p, dy=-0.05, pitch=18)
        p.add("spine", 6, 0, 0)
        for sg, a in ((1, left), (-1, right)):
            if sg > 0 and let_go > 0:
                continue
            tgt = knob(sg, a) + V(0, 0.07, 0.015)
            body.hand_to(p, sg, tgt, elbow=(0.3, 0.4, -0.5), hand_rot=hand_world((0, -0.6, 1), (sg * -1, 0, 0)))
            fist(p, sg)

    def stand(p):
        body.plant(p, 1)
        body.plant(p, -1)

    # ---- levers: at work, putting his back into it ------------------------------------------------------
    c = Clip(f"{NAME}/levers", LEVER, loop=True)
    busy = REST.copy()
    busy.face = {"grit": 0.6, "grin": 0.4}
    c.key(0.0, busy)
    c.key(LEVER, busy, "linear")

    def levers(t, p, skel):
        left, _ = lever(t)
        p.add("chest", 0, 0.25 * left, 0)
        p.add("head", 0, -0.2 * left, 0)
        on_levers(p, t)
        stand(p)
        return p

    c.solve(levers)
    out.append(c)

    # ---- caught: freezes; looks back over his shoulder; a very small wave --------------------------------
    T = 3.0
    c = Clip(f"{NAME}/caught", T)
    c.key(0.0, busy)
    caught = REST.copy()
    caught.face = {"grin": 0.7, "wide": 0.3}
    c.key(0.3, caught, "snap")
    c.key(T, caught, "linear")

    def caught_(t, p, skel):
        back = ease("inout", smooth(0.5, 1.1, t))       # head round, over his left shoulder, to the light
        p.add("head", -10 * back, 70 * back, 0)
        p.add("neck", 0, 20 * back, 0)
        p.add("chest", 0, 10 * back, 0)
        wave = pulse(t, 1.4, 0.25, 0.9, 0.3)
        on_levers(p, 0.0, let_go=wave)
        if wave > 0:
            up = V(0.36, 0.05, 1.18 + 0.03 * math.sin(math.tau * 3.5 * t))
            wrist = L.wrist_of(body, REST, 1).lerp(up, wave)
            body.hand_to(p, 1, wrist, elbow=(0.4, 0.2, -0.6), hand_rot=hand_world((0, 0.1, 1), (1, 0, 0)))
            L.open_hand(p, 1, 10)
        stand(p)
        return p

    c.solve(caught_)
    c.layer(lambda t: look((10 * smooth(0.5, 1.0, t), 30 * smooth(0.5, 1.0, t))))
    out.append(c)
    return out
