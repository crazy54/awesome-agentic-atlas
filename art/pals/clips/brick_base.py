"""Brick's everyday clips, and the pieces his bits are made of. He is the big, calm, deliberate one: every
move is slow and sure, his face mostly deadpan (the sheet's small closed smile), and he does the one useful
thing in the scene without fuss.

    idle (4 s loop)  walk (one 1.3 s stride in place)  carry (the walk, holding something in front)
    lift  lift-hold  set-down                 two hands: up from the floor to his chest, held, put down
    lift-one-finger  finger-hold  finger-down one enormous index finger, raised overhead (it bears the weight)
    finger-point  finger-point-hold  finger-point-off   one finger on a point beside his head (a light switch)
    guard  guard-hold  guard-off              arms folded, feet set: nobody is getting past
    bouncer (4 s loop)                        hands clasped at the belt, chin up, scanning the room
    catch  slow-clap  raise-brow  shake-head  nod  shrug  push  pull
    much-better                               his signature move: smooth, and much better than yours

Every clip but the loops and the `-hold`s starts and ends on `REST`, so the page can chain them with no
jump; `lift` ends holding (`lift-hold` then loops and `set-down` starts from there), as do `lift-one-finger`,
`finger-point` and `guard`.

THE WALK. `walk` is a stride in place: each foot slides back at WALK_SPEED while it is down, and the page
moves him at that speed, so on the page his feet stay put. WALK_SPEED = stride / (stance * period) =
0.75 / (0.64 * 1.3) = 0.90 m/s: a long, slow, heavy stride. `carry` is the same stride.

AXES (kit/rig.py; his arms already hang about 20 degrees out at rest, so `z` 0 is the sheet's hang). Arms:
+X swings forward (90 points straight ahead), +Z raises sideways (+70 is a T). Trunk and head: +X bends
forward, +Y turns to his left, +Z leans to his right. Lids: the upper closes at x -30, the lower at x +38.
Eyes: +X looks up, +Z looks to his left. Poses are written for the left and mirrored with `both`/`side`.

PLACES (his frame at rest, metres: x to his left, y back, z up; the page's x is his x when he faces the
reader). Wrists hang at (+-1.17, 0.34, 1.10); the shoulders pivot at (+-0.84, 0.30, 2.05). FINGER_TIP is
where `finger-point` holds his right index tip; ONE_FINGER where `lift-one-finger` holds his right index tip;
HOLD the middle of whatever `lift` holds between his hands.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import Body, breathe, look, stride_foot
from kit.anim import Clip, Pose, ease, pulse, smooth

TAU = math.tau
FACE = {"smile": 1.0}
BODY = dict(heel_back=0.56, toe_front=0.54)
STANCE = 8.0                            # toe out, degrees, standing
WALK_PERIOD, WALK_STANCE, WALK_STRIDE = 1.3, 0.64, 0.75
WALK_SPEED = WALK_STRIDE / (WALK_STANCE * WALK_PERIOD)
LID_UP, LID_LO = -30.0, 38.0            # the lids shut
BROW = 0.015                            # a brow unit, metres
FINGER_TIP = (-0.62, -0.62, 2.28)       # finger-point: his right index tip, beside and above his head
ONE_FINGER = (-0.55, -0.55, 3.0)        # lift-one-finger: his right index tip, overhead
HOLD = (0.0, -0.95, 1.5)                # lift: between his hands, in front of his chest


def V(*a):
    return Vector(a)


def rest_pose():
    """His everyday stance: as built (the sheet's hang of the arms), the hands loosely curled, the head a
    touch down and the small closed smile."""
    p = Pose(face=dict(FACE))
    p.fingers(1, (22, 24, 26), spread=3, thumb=14)
    p.fingers(-1, (22, 24, 26), spread=3, thumb=14)
    p.set("head", 3, 0, 0)
    return p


REST = rest_pose()


# --------------------------------------------------------------------------------------------- tools
def env(t, T, a=0.5, b=0.5):
    """0 at both ends of a clip of T seconds, 1 between, easing over `a` in and `b` out."""
    return smooth(0, a, t) * (1 - smooth(T - b, T, t))


def hips(body, p, dx=0.0, dy=0.0, dz=0.0, pitch=0.0, yaw=0.0, roll=0.0):
    """Move the hips by a world offset and turn them (pitch forward, yaw left, roll right), additively."""
    body.move_world(p, "hips", dx, dy, dz)
    p.add("hips", pitch, yaw, roll)
    return p


def fist(p, side, k=1.0):
    return p.fingers(side, 86 * k, spread=0, thumb=55 * k)


def point(p, side):
    """Index straight, the others curled, thumb tucked."""
    s = "_L" if side > 0 else "_R"
    p.fingers(side, 88, thumb=55, which=("middle", "ring"))
    for i in (1, 2, 3):
        p.set(f"index_{i}{s}", 0, 0, 0)
    return p


def open_hand(p, side, spread=10):
    return p.fingers(side, 3, spread=spread, thumb=0)


def wrist_of(body, pose, side):
    return body.where(pose, f"hand{'_L' if side > 0 else '_R'}")


def tip_of(body, pose, side, finger="index"):
    return body.where(pose, f"{finger}_3{'_L' if side > 0 else '_R'}", at="tail")


def hand_world(*cols):
    """A hand orientation from its Y (along the fingers) and Z (out of the palm) in world space."""
    y = Vector(cols[0]).normalized()
    z = Vector(cols[1])
    z = (z - y * z.dot(y)).normalized()
    x = y.cross(z)
    return Matrix((x, y, z)).transposed()


def feet_spec(spec, k):
    s = dict(spec)
    if "pos" in s:
        s["pos"] = tuple(v * k for v in s["pos"])
    for key in ("roll", "lift", "bank", "knee_out"):
        if key in s:
            s[key] = s[key] * k
    if "yaw" in s:
        s["yaw"] = STANCE + (s["yaw"] - STANCE) * k
    return s


def stand(body, feet=None, w=None):
    """A post-solver that keeps both feet planted, toes out. `feet(t)` may return {side: plant kwargs};
    `w(t)` blends that spec from his stance (0) to full (1)."""
    def f(t, p, skel):
        spec = feet(t) if feet else {}
        k = w(t) if w else 1.0
        for sg in (1, -1):
            s = dict(spec.get(sg, {}))
            s.setdefault("yaw", STANCE)
            body.plant(p, sg, **feet_spec(s, k))
        return p
    return f


def planted(body, pose=None):
    q = (pose or REST).copy()
    body.plant(q, 1, yaw=STANCE)
    body.plant(q, -1, yaw=STANCE)
    return q


def rest_wrists(body):
    q = planted(body)
    return {1: wrist_of(body, q, 1), -1: wrist_of(body, q, -1)}


def blink_at(t, times, close=0.12, hold=0.07, open_=0.2):
    """His blinks are slow: 1 at the bottom of each, 0 with the eyes open."""
    return max((pulse(t, a, close, hold, open_) for a in times), default=0.0)


def blinks(times, **kw):
    def f(t):
        b = blink_at(t, times, **kw)
        if b <= 0:
            return None
        p = Pose()
        p.both("lid_up", x=LID_UP * b)
        p.both("lid_lo", x=LID_LO * b)
        return p
    return f


def brows(p, inner=0.0, mid=0.0, outer=0.0, side=0):
    """Raise his brows by about 1.5 cm a unit: `side` 0 both, +1 left only, -1 right only."""
    for sg, s in ((1, "_L"), (-1, "_R")):
        if side and side != sg:
            continue
        p.move(f"brow_in{s}", 0, inner * BROW, 0)
        p.move(f"brow_mid{s}", 0, mid * BROW, 0)
        p.move(f"brow_out{s}", 0, outer * BROW, 0)
    return p


def lids(p, k):
    """Heavier lids (k 0..1 of the way shut), the deadpan look."""
    p.both("lid_up", x=LID_UP * k, add=True)
    return p


# ------------------------------------------------------------------------------------------- idle
def idle(body):
    """Four seconds, looping: one slow breath, the weight easing from foot to foot, two slow blinks, and
    now and then the right brow goes up on its own."""
    T = 4.0
    c = Clip("idle", T, loop=True, frames=120)
    c.key(0.0, REST)

    def layer(t):
        u = t / T
        sway = math.sin(TAU * u)
        p = Pose()
        hips(body, p, dx=0.014 * sway, dz=-0.004 * (1 - math.cos(TAU * u)), roll=-0.8 * sway)
        p.add("spine", 0, 0, 0.6 * sway)
        p.add("head", 0, 1.5 * math.sin(TAU * u + 0.9), -1.4 * math.sin(TAU * u + 0.4))
        p.both("upper_arm", z=0.8 * sway, add=True)
        p = p + breathe(T, 1.5)(t)
        b = pulse(u, 0.52, 0.07, 0.16, 0.1)
        brows(p, 0.5 * b, 1.4 * b, 1.0 * b, side=-1)
        p = p + look((2 * b, -4 * b))
        return p

    c.layer(layer)
    c.layer(blinks([1.05, 3.05]))
    c.solve(stand(body))
    return c


# -------------------------------------------------------------------------------------------- walk
def walk(body, name="walk", carry=False):
    """One stride in place: long, slow and heavy, the weight rolling over onto each foot in turn, a dip
    as each heel lands, the arms barely swinging. `carry` holds both hands out in front, round something."""
    T = WALK_PERIOD
    c = Clip(name, T, loop=True, frames=int(round(T * 30)))
    base = REST.copy()
    base.set("chest", 3, 0, 0)
    c.key(0.0, base)
    rw = rest_wrists(body)

    def layer(t):
        u = t / T
        p = Pose()
        dip = math.cos(TAU * 2 * (u - 0.1))
        hips(body, p, dz=-0.045 + 0.028 * dip, dx=0.055 * math.sin(TAU * (u - 0.07)),
             roll=-3.0 * math.sin(TAU * (u - 0.07)), yaw=-4 * math.sin(TAU * u))
        p.add("chest", 0, 5 * math.sin(TAU * u), 1.5 * math.sin(TAU * (u - 0.07)))
        p.add("head", 1.2 * dip, -3 * math.sin(TAU * u), -1.5 * math.sin(TAU * (u - 0.07)))
        if not carry:
            swing = math.sin(TAU * u)
            p.side("upper_arm", 1, x=-12 * swing, add=True)
            p.side("upper_arm", -1, x=12 * swing, add=True)
            p.side("forearm", 1, x=8 + 8 * max(0.0, -swing), add=True)
            p.side("forearm", -1, x=8 + 8 * max(0.0, swing), add=True)
        return p

    c.layer(layer)

    def solve(t, p, skel):
        if carry:
            u = t / T
            bob = 0.015 * math.cos(TAU * 2 * (u - 0.1))
            for sg in (1, -1):
                tgt = V(sg * 0.5, -0.85, 1.48 + bob)
                body.hand_to(p, sg, tgt, elbow=(0.7, 0.3, -0.6), hand_rot=hand_world((-sg * 0.45, -0.75, 0.2),
                                                                                       (-sg, 0.1, 0.25)))
                p.fingers(sg, 34, spread=2, thumb=20)
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, WALK_STRIDE, WALK_STANCE, ph, height=0.12, toe_off=20.0,
                                        heel_strike=-10.0)
            body.plant(p, sg, pos=(0, y, 0), roll=roll, lift=lift, yaw=4)
        return p

    c.solve(solve)
    return c


# -------------------------------------------------------------------------------- lifting, two hands
def lift_pose(body, p, k, sink):
    """Hands on whatever is in front of him at HOLD, `k` of the way from his sides, the knees `sink` bent."""
    hips(body, p, dz=-0.16 * sink, dy=0.06 * sink, pitch=10 * sink)
    p.add("spine", 8 * sink, 0, 0)
    p.add("chest", 4 * sink - 4 * k * (1 - sink), 0, 0)
    p.add("head", -6 * sink, 0, 0)


def lift(body):
    """Bends at the knees, takes something off the floor in front of him in both hands, and straightens
    with it at his chest. Ends holding (HOLD between his hands): `lift-hold` loops from there."""
    T = 2.6
    c = Clip("lift", T, frames=78)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    low, hold = V(0, -0.9, 0.62), V(*HOLD)

    def solve(t, p, skel):
        sink = pulse(t, 0.1, 0.7, 0.35, 0.9)
        reach = smooth(0.1, 0.8, t)
        up = smooth(1.15, 2.2, t)
        mid = low.lerp(hold, ease("inout", up))
        lift_pose(body, p, reach, sink)
        for sg in (1, -1):
            tgt = rw[sg].lerp(mid + V(sg * 0.6, 0.05, -0.02), reach)
            body.hand_to(p, sg, tgt, elbow=(0.8, 0.3, -0.5),
                         hand_rot=hand_world((-sg * 0.5, -0.7, 0.2), (-sg, 0.1, 0.3)) if reach > 0.5 else None)
            p.fingers(sg, 22 + 14 * reach, spread=2, thumb=14 + 8 * reach)
        body.plant(p, 1, yaw=STANCE, knee_out=0.1 * sink)
        body.plant(p, -1, yaw=STANCE, knee_out=0.1 * sink)
        return p

    def face(t):
        p = Pose()
        e = pulse(t, 0.9, 0.3, 0.6, 0.4)
        p.face.update({"smile": -0.6 * e, "flat": 0.6 * e})
        brows(p, -0.3 * e, 0.0, 0.2 * e)
        p = p + look((-14 * pulse(t, 0.2, 0.4, 0.6, 0.6), 0))
        return p

    c.solve(solve)
    c.layer(face)
    c.layer(blinks([0.4]))
    return c


def held(body, p, t, bob=0.012):
    hold = V(*HOLD) + V(0, 0, bob * math.sin(TAU * t / 2.0))
    for sg in (1, -1):
        body.hand_to(p, sg, hold + V(sg * 0.6, 0.05, -0.02), elbow=(0.8, 0.3, -0.5),
                     hand_rot=hand_world((-sg * 0.5, -0.7, 0.2), (-sg, 0.1, 0.3)))
        p.fingers(sg, 36, spread=2, thumb=22)


def lift_hold(body):
    T = 2.0
    c = Clip("lift-hold", T, loop=True, frames=60)
    c.key(0.0, REST)
    c.layer(lambda t: breathe(T, 1.0)(t))

    def solve(t, p, skel):
        held(body, p, t)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    return c


def set_down(body):
    """From `lift-hold`: bends, sets it on the floor in front of him, lets go, straightens."""
    T = 2.4
    c = Clip("set-down", T, frames=72)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    low, hold = V(0, -0.9, 0.62), V(*HOLD)

    def solve(t, p, skel):
        down = smooth(0.0, 1.0, t)
        sink = pulse(t, 0.2, 0.8, 0.3, 1.0)
        let = smooth(1.3, 2.3, t)
        mid = hold.lerp(low, ease("inout", down))
        lift_pose(body, p, 1 - let, sink)
        for sg in (1, -1):
            tgt = (mid + V(sg * 0.6, 0.05, -0.02)).lerp(rw[sg], let)
            body.hand_to(p, sg, tgt, elbow=(0.8, 0.3, -0.5),
                         hand_rot=hand_world((-sg * 0.5, -0.7, 0.2), (-sg, 0.1, 0.3)) if let < 0.5 else None)
            p.fingers(sg, 36 - 14 * let, spread=2, thumb=22 - 8 * let)
        body.plant(p, 1, yaw=STANCE, knee_out=0.1 * sink)
        body.plant(p, -1, yaw=STANCE, knee_out=0.1 * sink)
        return p

    c.solve(solve)
    c.layer(blinks([1.6]))
    return c


def carry(body):
    return walk(body, "carry", carry=True)


# ---------------------------------------------------------------------------------- one finger
def one_finger_at(body, p, k, rw, target, side=-1):
    """His `side` index tip on `target` (world), the hand turned so the finger points up at it."""
    up = hand_world((side * 0.15, -0.2, 1), (side * 0.9, 0.2, 0.2))
    wrist = target - up.col[1] * 0.58
    body.hand_to(p, side, rw[side].lerp(wrist, k), elbow=(0.6, 0.6, -0.4), hand_rot=up if k > 0.45 else None)
    if k > 0.2:
        point(p, side)


def lift_one_finger(body):
    """Raises his right hand overhead, index finger up, as if whatever is on it weighed nothing. Ends
    holding the tip at ONE_FINGER: `finger-hold` loops, `finger-down` puts it back."""
    T = 1.8
    c = Clip("lift-one-finger", T, frames=54)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*ONE_FINGER)

    def solve(t, p, skel):
        k = ease("inout", smooth(0.15, 1.5, t))
        p.add("chest", -3 * k, 0, 2 * k)
        p.add("head", -6 * k, 0, 0)
        one_finger_at(body, p, k, rw, tip)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    c.layer(lambda t: look((10 * smooth(0.3, 1.2, t), -6 * smooth(0.3, 1.2, t))))
    c.layer(blinks([1.4]))
    return c


def finger_hold(body):
    T = 3.0
    c = Clip("finger-hold", T, loop=True, frames=90)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*ONE_FINGER)

    def solve(t, p, skel):
        p.add("chest", -3, 0, 2)
        p.add("head", -6, 0, 0)
        one_finger_at(body, p, 1.0, rw, tip + V(0, 0, 0.008 * math.sin(TAU * t / T)))
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    c.layer(lambda t: breathe(T, 1.0)(t) + look((10, -6)))
    c.layer(blinks([1.8]))
    return c


def finger_down(body):
    T = 1.4
    c = Clip("finger-down", T, frames=42)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*ONE_FINGER)

    def solve(t, p, skel):
        k = 1 - ease("inout", smooth(0.0, 1.2, t))
        p.add("chest", -3 * k, 0, 2 * k)
        p.add("head", -6 * k, 0, 0)
        one_finger_at(body, p, k, rw, tip)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    return c


# ------------------------------------------------------------------------------- finger on a point
def finger_point(body):
    """Reaches up beside his head and puts one enormous index finger on a point (FINGER_TIP), pressing it
    flat to the glass. Ends holding it there: `finger-point-hold` loops, `finger-point-off` takes it away."""
    T = 1.6
    c = Clip("finger-point", T, frames=48)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*FINGER_TIP)

    def solve(t, p, skel):
        k = ease("inout", smooth(0.1, 1.3, t))
        press = pulse(t, 1.2, 0.12, 0.3, 0.2) * 0.04
        p.add("chest", 0, -6 * k, 3 * k)
        p.add("head", 0, -10 * k, 0)
        one_finger_at(body, p, k, rw, tip + V(0, -press, 0))
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    c.layer(lambda t: look((10 * smooth(0.2, 1.0, t), -14 * smooth(0.2, 1.0, t))))
    return c


def finger_point_hold(body):
    T = 4.0
    c = Clip("finger-point-hold", T, loop=True, frames=120)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*FINGER_TIP)

    def solve(t, p, skel):
        p.add("chest", 0, -6, 3)
        p.add("head", 0, -10, 0)
        one_finger_at(body, p, 1.0, rw, tip)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)

    def face(t):
        p = breathe(T, 1.0)(t)
        # he looks back at the reader, and the right brow goes up a little
        k = pulse(t, 0.8, 0.5, 2.0, 0.6)
        p = p + look((4 - 4 * k, -14 + 14 * k))
        brows(p, 0.3 * k, 0.9 * k, 0.6 * k, side=-1)
        return p

    c.layer(face)
    c.layer(blinks([2.4]))
    return c


def finger_point_off(body):
    T = 1.3
    c = Clip("finger-point-off", T, frames=39)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    tip = V(*FINGER_TIP)

    def solve(t, p, skel):
        k = 1 - ease("inout", smooth(0.0, 1.1, t))
        p.add("chest", 0, -6 * k, 3 * k)
        p.add("head", 0, -10 * k, 0)
        one_finger_at(body, p, k, rw, tip + V(0, 0, 0))
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    c.solve(solve)
    return c


# -------------------------------------------------------------------------------------- arms folded
FOLD = {1: V(-0.34, -0.88, 1.56), -1: V(0.38, -0.98, 1.48)}       # wrists, folded: left over right


def folded(body, p, k, rw):
    p.add("chest", -4 * k, 0, 0)
    p.add("head", -4 * k, 0, 0)
    for sg in (1, -1):
        tgt = rw[sg].lerp(FOLD[sg], k)
        body.hand_to(p, sg, tgt, elbow=(1.0, -0.2, -0.3),
                     hand_rot=hand_world((-sg * 1, -0.1, 0.1), (0, 0.3 * sg, -1)) if k > 0.5 else None)
        p.fingers(sg, 22 + 40 * k, spread=0, thumb=14 + 20 * k)


def guard(body):
    """Folds his arms across his chest and sets his feet a little wider: nobody is getting past. Ends
    folded: `guard-hold` loops, `guard-off` unfolds."""
    T = 1.4
    c = Clip("guard", T, frames=42)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        k = ease("inout", smooth(0.1, 1.2, t))
        folded(body, p, k, rw)
        body.plant(p, 1, pos=(0.06 * k, 0, 0), yaw=STANCE + 4 * k)
        body.plant(p, -1, pos=(-0.06 * k, 0, 0), yaw=STANCE + 4 * k)
        return p

    def face(t):
        p = Pose()
        k = smooth(0.3, 1.2, t)
        p.face.update({"smile": -0.5 * k, "flat": 0.5 * k})
        lids(p, 0.2 * k)
        return p

    c.solve(solve)
    c.layer(face)
    return c


def guard_hold(body):
    T = 4.0
    c = Clip("guard-hold", T, loop=True, frames=120)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        folded(body, p, 1.0, rw)
        body.plant(p, 1, pos=(0.06, 0, 0), yaw=STANCE + 4)
        body.plant(p, -1, pos=(-0.06, 0, 0), yaw=STANCE + 4)
        return p

    def face(t):
        p = breathe(T, 1.2)(t)
        p.face.update({"smile": -0.5, "flat": 0.5})
        lids(p, 0.2)
        g = math.sin(TAU * t / T)
        p = p + look((0, 8 * g))
        return p

    c.solve(solve)
    c.layer(face)
    c.layer(blinks([1.4, 3.3]))
    return c


def guard_off(body):
    T = 1.2
    c = Clip("guard-off", T, frames=36)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        k = 1 - ease("inout", smooth(0.0, 1.05, t))
        folded(body, p, k, rw)
        body.plant(p, 1, pos=(0.06 * k, 0, 0), yaw=STANCE + 4 * k)
        body.plant(p, -1, pos=(-0.06 * k, 0, 0), yaw=STANCE + 4 * k)
        return p

    def face(t):
        p = Pose()
        k = 1 - smooth(0.0, 1.0, t)
        p.face.update({"smile": -0.5 * k, "flat": 0.5 * k})
        lids(p, 0.2 * k)
        return p

    c.solve(solve)
    c.layer(face)
    return c


# ------------------------------------------------------------------------------------------ bouncer
def bouncer(body):
    """Four seconds, looping: feet wide, hands clasped at the belt, chin up, scanning the room slowly."""
    T = 4.0
    c = Clip("bouncer", T, loop=True, frames=120)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        p.add("chest", -5, 0, 0)
        p.add("head", -6, 10 * math.sin(TAU * t / T), 0)
        for sg in (1, -1):
            body.hand_to(p, sg, V(sg * 0.2, -0.86, 1.06), elbow=(1.0, 0.2, -0.2),
                         hand_rot=hand_world((-sg * 0.8, -0.3, -0.4), (0, 0.4 * sg, 1)))
            p.fingers(sg, 55, spread=0, thumb=40)
        body.plant(p, 1, pos=(0.1, 0, 0), yaw=STANCE + 6)
        body.plant(p, -1, pos=(-0.1, 0, 0), yaw=STANCE + 6)
        return p

    def face(t):
        p = breathe(T, 1.3)(t)
        p.face.update({"smile": -0.7, "flat": 0.7})
        lids(p, 0.25)
        p = p + look((0, 14 * math.sin(TAU * t / T - 0.4)))
        return p

    c.solve(solve)
    c.layer(face)
    c.layer(blinks([0.6, 2.6]))
    return c


# --------------------------------------------------------------------------------------- gestures
def catch(body):
    """A sudden, surprisingly quick dip: his right hand cups under something falling in front of him, just
    above the floor, and brings it up to look at it, then back to his side."""
    T = 2.4
    c = Clip("catch", T, frames=72)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    low, look_at = V(-0.42, -0.95, 0.42), V(-0.25, -0.8, 1.55)

    def solve(t, p, skel):
        dive = smooth(0.0, 0.3, t)
        up = smooth(0.55, 1.2, t)
        back = smooth(1.75, 2.35, t)
        sink = dive * (1 - up)
        hips(body, p, dz=-0.3 * sink, dy=0.05 * sink, pitch=18 * sink, yaw=-8 * sink)
        p.add("spine", 12 * sink, 0, 0)
        p.add("chest", 8 * sink, -6 * sink, 0)
        p.add("head", 10 * sink, 0, 0)
        cup = low.lerp(look_at, ease("inout", up))
        tgt = rw[-1].lerp(cup, dive * (1 - back))
        palm_up = hand_world((0.2, -1, 0.15), (0, 0, 1))
        body.hand_to(p, -1, tgt, elbow=(0.6, 0.5, -0.4), hand_rot=palm_up if dive * (1 - back) > 0.4 else None)
        p.fingers(-1, 30 + 10 * dive * (1 - back), spread=4, thumb=20)
        body.plant(p, 1, yaw=STANCE, knee_out=0.12 * sink)
        body.plant(p, -1, pos=(0, -0.12 * sink, 0), yaw=STANCE, knee_out=0.12 * sink)
        return p

    def face(t):
        p = Pose()
        a = pulse(t, 0.05, 0.1, 0.4, 0.3)
        brows(p, 1.0 * a, 1.2 * a, 0.8 * a)
        k = pulse(t, 0.9, 0.2, 0.8, 0.3)
        p = p + look((-10 * k - 20 * pulse(t, 0.0, 0.2, 0.4, 0.3), -8 * k))
        return p

    c.solve(solve)
    c.layer(face)
    return c


def slow_clap(body):
    """Four slow claps in front of his chest, utterly deadpan."""
    T = 4.6
    c = Clip("slow-clap", T, frames=138)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    claps = [1.0, 1.85, 2.7, 3.55]

    def solve(t, p, skel):
        k = pulse(t, 0.1, 0.65, 3.25, 0.6)
        gap = 1.0
        for a in claps:
            gap = min(gap, 1 - pulse(t, a - 0.32, 0.32, 0.02, 0.4))
        for sg in (1, -1):
            tgt = V(sg * (0.13 + 0.17 * gap), -0.9, 1.45)
            body.hand_to(p, sg, rw[sg].lerp(tgt, k), elbow=(0.9, 0.3, -0.4),
                         hand_rot=hand_world((-sg * 0.3, -0.9, 0.35), (-sg, 0, 0)) if k > 0.5 else None)
            open_hand(p, sg, 2)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    def face(t):
        p = Pose()
        k = pulse(t, 0.2, 0.4, 3.6, 0.4)
        p.face.update({"smile": -0.8 * k, "flat": 0.8 * k})
        lids(p, 0.3 * k)
        for a in claps:
            p.add("head", 1.5 * pulse(t, a, 0.04, 0.02, 0.2), 0, 0)
        return p

    c.solve(solve)
    c.layer(face)
    c.layer(blinks([2.2]))
    return c


def raise_brow(body):
    """The right brow goes up, slowly, and stays up a moment. The rest of him does not move."""
    T = 2.0
    c = Clip("raise-brow", T, frames=60)
    c.key(0.0, REST)

    def layer(t):
        p = Pose()
        k = pulse(t, 0.15, 0.4, 0.9, 0.45)
        brows(p, 0.6 * k, 1.9 * k, 1.5 * k, side=-1)
        brows(p, -0.3 * k, -0.4 * k, -0.2 * k, side=1)
        p.add("head", -2 * k, 0, -3 * k)
        p.face.update({"smile": -0.4 * k, "flat": 0.4 * k})
        return p

    c.layer(layer)
    c.solve(stand(body))
    return c


def shake_head(body):
    """A slow no, twice, the eyes shutting on the second."""
    T = 2.4
    c = Clip("shake-head", T, frames=72)
    c.key(0.0, REST)

    def layer(t):
        p = Pose()
        k = pulse(t, 0.1, 0.25, 1.8, 0.25)
        p.add("head", 4 * k, 14 * k * math.sin(TAU * (t - 0.15) / 1.0), 0)
        p.add("neck", 0, 5 * k * math.sin(TAU * (t - 0.15) / 1.0), 0)
        p.face.update({"smile": -0.9 * k, "frown": 0.4 * k, "flat": 0.5 * k})
        brows(p, 0.6 * k, 0.2 * k, -0.3 * k)
        sh = pulse(t, 1.15, 0.15, 0.5, 0.25)
        p.both("lid_up", x=LID_UP * 0.9 * sh)
        p.both("lid_lo", x=LID_LO * 0.9 * sh)
        return p

    c.layer(layer)
    c.solve(stand(body))
    return c


def nod(body):
    """One slow, approving nod."""
    T = 1.6
    c = Clip("nod", T, frames=48)
    c.key(0.0, REST)

    def layer(t):
        p = Pose()
        k = pulse(t, 0.1, 0.45, 0.15, 0.6)
        p.add("head", 14 * k, 0, 0)
        p.add("neck", 4 * k, 0, 0)
        p.face.update({"smile": 0.3 * k})
        lids(p, 0.3 * k)
        return p

    c.layer(layer)
    c.solve(stand(body))
    return c


def shrug(body):
    """Big shoulders up, palms up, head to one side: what did you expect."""
    T = 2.2
    c = Clip("shrug", T, frames=66)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        k = pulse(t, 0.1, 0.45, 0.8, 0.6)
        p.both("shoulder", z=10 * k, add=True)
        p.add("head", -3 * k, 0, 10 * k)
        for sg in (1, -1):
            tgt = rw[sg].lerp(V(sg * 0.95, -0.55, 1.25), k)
            body.hand_to(p, sg, tgt, elbow=(0.3, 0.4, -1.0),
                         hand_rot=hand_world((sg * 0.5, -0.85, 0.1), (0, 0, 1)) if k > 0.4 else None)
            p.fingers(sg, 22 - 18 * k, spread=8 * k, thumb=14 - 14 * k)
        body.plant(p, 1, yaw=STANCE)
        body.plant(p, -1, yaw=STANCE)
        return p

    def face(t):
        p = Pose()
        k = pulse(t, 0.2, 0.4, 0.8, 0.5)
        brows(p, 1.2 * k, 1.5 * k, 0.8 * k)
        p.face.update({"smile": -0.6 * k, "flat": 0.6 * k})
        return p

    c.solve(solve)
    c.layer(face)
    return c


def push(body):
    """Both palms to something in front of him, a lean, and a slow, steady push."""
    T = 3.0
    c = Clip("push", T, frames=90)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        k = pulse(t, 0.1, 0.6, 1.8, 0.5)
        shove = pulse(t, 0.9, 0.9, 0.3, 0.5)
        hips(body, p, dy=-0.12 * shove * k, dz=-0.06 * k, pitch=6 * k + 8 * shove)
        p.add("chest", 6 * k, 0, 0)
        for sg in (1, -1):
            tgt = rw[sg].lerp(V(sg * 0.5, -1.15 - 0.22 * shove, 1.45), k)
            body.hand_to(p, sg, tgt, elbow=(0.9, 0.4, -0.4),
                         hand_rot=hand_world((-sg * 0.1, -0.2, 1), (0, -1, 0)) if k > 0.5 else None)
            open_hand(p, sg, 6 * k)
        body.plant(p, 1, pos=(0, -0.1 * k, 0), yaw=STANCE)
        body.plant(p, -1, pos=(0, 0.28 * k, 0), yaw=STANCE, roll=12 * shove)
        return p

    def face(t):
        p = Pose()
        k = pulse(t, 0.7, 0.4, 1.2, 0.4)
        p.face.update({"smile": -0.7 * k, "flat": 0.7 * k})
        brows(p, -0.4 * k, 0.0, 0.3 * k)
        return p

    c.solve(solve)
    c.layer(face)
    return c


def pull(body):
    """Takes hold of something in front of him, leans back, and hauls it in, hand over hand once."""
    T = 3.0
    c = Clip("pull", T, frames=90)
    c.key(0.0, REST)
    rw = rest_wrists(body)

    def solve(t, p, skel):
        k = pulse(t, 0.1, 0.55, 1.9, 0.45)
        haul = smooth(0.9, 2.0, t) * (1 - smooth(2.3, 2.6, t))
        hips(body, p, dy=0.12 * haul * k, dz=-0.08 * k, pitch=-8 * haul * k)
        p.add("chest", -6 * haul * k, 0, 0)
        for sg in (1, -1):
            reach = V(sg * 0.22, -1.25, 1.25)
            tgt = rw[sg].lerp(reach.lerp(V(sg * 0.4, -0.55, 1.3), haul), k)
            body.hand_to(p, sg, tgt, elbow=(0.8, 0.5, -0.5),
                         hand_rot=hand_world((-sg * 0.3, -1, 0), (-sg, 0, 0.4)) if k > 0.5 else None)
            fist(p, sg, 0.9 * k)
        body.plant(p, 1, pos=(0, -0.22 * k, 0), yaw=STANCE)
        body.plant(p, -1, pos=(0, 0.1 * k, 0), yaw=STANCE, roll=-14 * haul * k)
        return p

    def face(t):
        p = Pose()
        k = pulse(t, 0.8, 0.4, 1.2, 0.4)
        p.face.update({"smile": -0.8 * k, "grit": 0.5 * k})
        brows(p, -0.6 * k, -0.2 * k, 0.3 * k)
        return p

    c.solve(solve)
    c.layer(face)
    return c


# ----------------------------------------------------------------------------------- much better
def much_better(body):
    """His signature move, seven and a half seconds of it, smooth as anything: a cool touch to the brow; a
    hip sway with slow finger snaps; a body wave rolling down him from the head to the knees; a glide, the
    feet sliding apart and back as if the floor were ice; the lean -- thirty-five degrees forward from the
    ankles, held, impossible (turn him side on for it: B.face(+-1) at 4.75 s, back at 6.75); and up again, a point at the reader. Ends on REST."""
    T = 7.6
    c = Clip("much-better", T, frames=228)
    c.key(0.0, REST)
    rw = rest_wrists(body)
    beat = 0.5                                   # 120 bpm: the sway and the snaps
    W0, W1 = 2.7, 3.9                            # the wave
    G0, G1 = 3.9, 5.0                            # the glide
    L0, L1 = 5.0, 6.7                            # the lean

    def solve(t, p, skel):
        e = env(t, T, 0.4, 0.5)
        # ---- the touch to the brow (0.1-0.9): right fingers to the eyebrow and away
        tb = pulse(t, 0.1, 0.3, 0.15, 0.35)
        # ---- the sway (0.8-2.8) and snaps
        sway_k = pulse(t, 0.7, 0.3, 1.7, 0.3)
        b = t / beat
        sway = math.sin(math.pi * b) * sway_k
        snap = sway_k * max(0.0, math.cos(math.pi * b)) ** 8
        hips(body, p, dx=0.07 * sway, dz=-0.04 * sway_k, roll=-4 * sway, yaw=5 * sway)
        p.add("chest", 0, -6 * sway, 3 * sway)
        p.add("head", 2 * sway_k, 6 * sway, -3 * sway)
        p.both("shoulder", z=4 * sway, add=True)
        # ---- the wave (W0-W1): a roll travelling from the head down
        wv = smooth(W0, W1, t) if W0 < t < W1 + 0.4 else 0.0
        if 0 < wv < 1:
            for bone, at, amp in (("head", 0.0, 12), ("neck", 0.1, 8), ("chest", 0.25, 12), ("spine", 0.4, 12),
                                  ("hips", 0.55, -10)):
                u = (wv - at) / 0.45
                if 0 < u < 1:
                    p.add(bone, amp * math.sin(TAU * u), 0, 0)
            knee = math.sin(math.pi * smooth(0.6, 1.0, wv))
            hips(body, p, dz=-0.1 * knee, dy=-0.04 * math.sin(TAU * smooth(0.3, 0.9, wv)))
        # ---- the glide (G0-G1): the feet slide apart and together, the body floating level
        gl = smooth(G0, G1, t) if G0 <= t <= G1 else 0.0
        glide = math.sin(TAU * gl) * (1 if G0 <= t <= G1 else 0)
        hips(body, p, dx=0.12 * glide, dz=-0.03 * abs(glide))
        p.add("chest", 0, 0, -4 * glide)
        # ---- the lean (L0-L1): the whole of him tips forward about the ankles, held, and back
        ln = pulse(t, L0, 0.55, 0.6, 0.55)
        ang = math.radians(35 * ln)
        hz = body.hip_z
        hips(body, p, dy=-hz * math.sin(ang), dz=-hz * (1 - math.cos(ang)), pitch=35 * ln)
        p.add("head", -14 * ln, 0, 0)
        # ---- the arms
        for sg in (1, -1):
            if sg < 0 and tb > 0.01:
                brow = V(-0.27, -0.52, 2.62)
                body.hand_to(p, -1, rw[-1].lerp(brow, tb), elbow=(0.5, 0.2, -0.6),
                             hand_rot=hand_world((0.4, -0.3, 1), (0.2, -1, 0)) if tb > 0.5 else None)
                point(p, -1)
                p.set("middle_1_R", 0, 0, 0); p.set("middle_2_R", 0, 0, 0); p.set("middle_3_R", 0, 0, 0)
                continue
            if sway_k > 0.01:
                tgt = rw[sg].lerp(V(sg * 1.0, -0.4 - 0.1 * sway * sg, 1.25 + 0.08 * sway * sg), sway_k)
                body.hand_to(p, sg, tgt, elbow=(0.4, 0.4, -0.8),
                             hand_rot=hand_world((sg * 0.3, -0.6, 0.7), (0, -1, 0)) if sway_k > 0.5 else None)
                p.fingers(sg, 40 + 40 * snap, spread=0, thumb=10 + 50 * snap)
                p.set(f"middle_1{'_L' if sg > 0 else '_R'}", 30 * snap, 0, 0)
            if gl > 0:
                fl = math.sin(math.pi * gl)
                p.side("upper_arm", sg, x=12 * fl, z=30 * fl, add=True)
                p.side("forearm", sg, x=20 * fl, add=True)
                open_hand(p, sg, 8 * fl)
            if ln > 0.01:
                p.side("upper_arm", sg, x=-30 * ln, z=-6 * ln, add=True)
        # the point at the reader (6.75-7.3), left hand
        pt = pulse(t, 6.75, 0.25, 0.3, 0.3)
        if pt > 0.01:
            cur = wrist_of(body, p, 1)
            body.hand_to(p, 1, cur.lerp(V(0.55, -1.3, 1.75), pt), elbow=(0.6, 0.3, -0.5),
                         hand_rot=hand_world((-0.1, -1, 0.1), (-1, 0, 0)) if pt > 0.5 else None)
            point(p, 1)
        # ---- the feet: the glide slides them; the lean pins them flat
        gx = 0.16 * max(0.0, glide)
        gy = 0.16 * max(0.0, -glide)
        body.plant(p, 1, pos=(gx, 0, 0), yaw=STANCE - 10 * max(0.0, glide), roll=0)
        body.plant(p, -1, pos=(-gy, 0, 0), yaw=STANCE - 10 * max(0.0, -glide), roll=0)
        return p

    def face(t):
        p = Pose()
        cool = pulse(t, 0.3, 0.4, 6.4, 0.4)
        p.face.update({"smile": -0.4 * cool, "smirk_R": 0.8 * cool})
        lids(p, 0.35 * cool)
        brows(p, 0.4 * cool, 1.0 * cool, 0.8 * cool, side=-1)
        ln = pulse(t, L0, 0.55, 0.6, 0.55)
        p = p + look((12 * ln, 0))
        wink = pulse(t, 6.85, 0.08, 0.15, 0.15)
        p.set("lid_up_L", LID_UP * wink, 0, 0)
        p.set("lid_lo_L", LID_LO * wink, 0, 0)
        return p

    c.solve(solve)
    c.layer(face)
    return c


# ----------------------------------------------------------------------------------------- the lot
EVERYDAY = ["idle", "walk", "carry", "lift", "lift-hold", "set-down", "lift-one-finger", "finger-hold",
            "finger-down", "finger-point", "finger-point-hold", "finger-point-off", "guard", "guard-hold",
            "guard-off", "bouncer", "catch", "slow-clap", "raise-brow", "shake-head", "nod", "shrug", "push",
            "pull", "much-better"]
PACKS = {"brick": EVERYDAY}


def clips(body: Body):
    out = {
        "idle": idle(body), "walk": walk(body), "carry": carry(body),
        "lift": lift(body), "lift-hold": lift_hold(body), "set-down": set_down(body),
        "lift-one-finger": lift_one_finger(body), "finger-hold": finger_hold(body), "finger-down": finger_down(body),
        "finger-point": finger_point(body), "finger-point-hold": finger_point_hold(body),
        "finger-point-off": finger_point_off(body),
        "guard": guard(body), "guard-hold": guard_hold(body), "guard-off": guard_off(body),
        "bouncer": bouncer(body), "catch": catch(body), "slow-clap": slow_clap(body),
        "raise-brow": raise_brow(body), "shake-head": shake_head(body), "nod": nod(body), "shrug": shrug(body),
        "push": push(body), "pull": pull(body), "much-better": much_better(body),
    }
    out["calibrate"] = calibrate(body)
    return out


def calibrate(body):
    """Not for the page: one test pose a second, to check the skeleton's axes by eye."""
    c = Clip("calibrate", 8.0)
    tests = [REST.copy(), REST.copy().both("upper_arm", x=60), REST.copy().both("upper_arm", z=70),
             REST.copy().both("forearm", x=80), REST.copy().both("lid_up", x=LID_UP).both("lid_lo", x=LID_LO)]
    p = REST.copy() + look((12, 25))
    brows(p, 1.5, 1.5, 1.0)
    tests += [p]
    p = REST.copy()
    point(p, 1)
    fist(p, -1)
    tests += [p, REST.copy().set("head", 0, 30, 0)]
    for i, q in enumerate(tests):
        c.key(float(i), q, "step")
        c.key(i + 0.999, q, "step")
    c.solve(stand(body))
    return c
