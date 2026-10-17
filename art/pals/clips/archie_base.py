"""Archie's everyday clips: the twenty-two the homepage director already knows by name (art/archie/archie.py
made the first set; docs/assets/archie.js plays them), re-made for his new skeleton, plus `moonwalk`.

    idle (4 s loop)  watch  sit  sleep  press  shrug  walk (one 0.8 s stride in place)  moonwalk (ditto)
    floss  take-the-l  default-dance  orange-justice  robot  electro-shuffle  hype  boogie-down
    get-griddy  billy-bounce  fresh  scenario  groove-jam  headbang  the-drop

Durations and beat counts are the old ones, because the page's light show counts beats (`BEATS` in
archie.js). Every clip but `idle`, `walk` and `moonwalk` starts and ends on the idle's first pose, `REST`, so
the page can drop any of them between two idles without a jump.

THE WALK. `walk` is a stride in place: each foot slides back at WALK_SPEED while it is down, and the page
moves the view at that speed, so on the page his feet stay put. WALK_SPEED = stride / (stance * period) =
0.60 / (0.62 * 0.8) = 1.21 m/s. archie.js must use the same number.

AXES (see kit/rig.py). Arms: +X swings forward (90 points straight ahead), +Z raises sideways (-53 hangs
straight down, +37 is a T). Trunk and head: +X bends forward, +Y turns to his left, +Z leans to his right.
Lids: the upper closes at x -46, the lower at x +40. Eyes: +X looks up, +Z looks to his left (both eyes the
same sign). Poses are written for the left and mirrored with `both`/`side`.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import Body, blink_at, blink_layer, breathe, brows, look, stride_foot, wobble
from kit.anim import Clip, Pose, blend, ease, noise1, pulse, smooth

TAU = math.tau
FACE = {"grin": 1.0}
CREST = ("crest_1", "crest_2", "crest_3")
WALK_PERIOD, WALK_STANCE, WALK_STRIDE = 0.8, 0.62, 0.60
WALK_SPEED = WALK_STRIDE / (WALK_STANCE * WALK_PERIOD)
MOON_PERIOD = 1.0                       # the ball foot holds the floor half a period: 0.60 / 0.5 = 1.2 m/s


def V(*a):
    return Vector(a)


def rest_pose():
    """His everyday stance: chest up, chin up, arms easy at his sides with the elbows soft and the hands
    half curled, the sheet's smirk."""
    p = Pose(face=dict(FACE))
    p.both("shoulder", z=-2)
    p.both("upper_arm", x=6, y=0, z=-44)
    p.both("forearm", x=16, y=0, z=0)
    p.both("hand", x=4, y=0, z=0)
    p.fingers(1, 18, spread=4, thumb=12)
    p.fingers(-1, 18, spread=4, thumb=12)
    p.set("chest", -3, 0, 0)
    p.set("head", -3, 0, 3)
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
    return p.fingers(side, 88 * k, spread=0, thumb=55 * k)


def point(p, side):
    """Index straight, the others curled, thumb tucked."""
    s = "_L" if side > 0 else "_R"
    p.fingers(side, 90, thumb=50)
    for i in (1, 2, 3):
        p.set(f"index_{i}{s}", 0, 0, 0)
    return p


def open_hand(p, side, spread=10):
    return p.fingers(side, 2, spread=spread, thumb=0)


def stand(body, feet=None, w=None):
    """A post-solver that keeps both feet planted. `feet(t)` may return {side: plant kwargs}; `w(t)` blends
    the spec from rest (0) to full (1)."""
    def f(t, p, skel):
        spec = feet(t) if feet else {}
        k = w(t) if w else 1.0
        for sg in (1, -1):
            s = dict(spec.get(sg, {}))
            if k < 1 and s:
                for key in ("pos",):
                    if key in s:
                        s[key] = tuple(v * k for v in s[key])
                for key in ("yaw", "roll", "lift", "bank", "knee_out"):
                    if key in s:
                        s[key] = s[key] * k
            body.plant(p, sg, **s)
        return p
    return f


def crest_follow(t, amp=1.0, speed=1.0):
    return wobble(CREST, t, 2.5 * amp, speed, 0.3)


def blend_hand(body, p, side, rest_wrist, target, w, elbow=(0.5, 0.4, -0.6), hand_rot=None):
    tgt = rest_wrist.lerp(target, w)
    body.hand_to(p, side, tgt, elbow=elbow, hand_rot=hand_rot)


def wrist_of(body, pose, side):
    s = "_L" if side > 0 else "_R"
    return body.where(pose, f"hand{s}")


def hand_world(*cols):
    """A hand orientation from its Y (along the fingers) and Z (out of the palm) in world space."""
    y = Vector(cols[0]).normalized()
    z = Vector(cols[1])
    z = (z - y * z.dot(y)).normalized()
    x = y.cross(z)
    return Matrix((x, y, z)).transposed()


# ------------------------------------------------------------------------------------------- idle
def idle(body):
    """Four seconds, looping: a slow weight shift, a toe tap, breathing, a glance off and back, a brow
    that can't help itself, blinks (one double)."""
    T = 4.0
    c = Clip("idle", T, loop=True, frames=120)
    c.key(0.0, REST)

    def layer(t):
        u = t / T
        sway = math.sin(TAU * u)
        p = Pose()
        hips(body, p, dx=0.022 * sway, dz=-0.006 - 0.004 * math.cos(TAU * 2 * u), roll=-1.6 * sway,
             yaw=1.2 * math.sin(TAU * u - 0.6))
        p.add("spine", 0, 0, 1.2 * sway)
        p.add("chest", 0, -0.8 * math.sin(TAU * u - 0.6), 0.6 * sway)
        p.both("upper_arm", z=1.2 * sway, add=True)
        # the glance: off to his left and back
        g = pulse(u, 0.44, 0.08, 0.16, 0.1)
        p = p + look((2 * g, 18 * g), head=(0, -2 * g, 7 * g))
        # the brow
        b = pulse(u, 0.62, 0.05, 0.12, 0.08)
        brows(p, 0.4 * b, 1.4 * b, 1.0 * b, side=1)
        p.face["smirk_L"] = 0.35 * b
        p.face["grin"] = -0.3 * b
        p = p + breathe(T / 2, 1.0)(t)
        p = p + crest_follow(t * TAU / T * 0.8, 0.7)
        return p

    c.layer(layer)
    c.layer(blink_layer([0.31 * T, 0.83 * T, 0.9 * T]))

    def feet(t):
        u = t / T
        tap = max(0.0, math.sin(TAU * 4 * u)) ** 2 * smooth(0.0, 0.05, u) * (1 - smooth(0.4, 0.45, u))
        tap2 = max(0.0, math.sin(TAU * 4 * u)) ** 2 * smooth(0.55, 0.6, u) * (1 - smooth(0.95, 1.0, u))
        return {1: dict(roll=-14 * (tap + tap2))}

    c.solve(stand(body, feet))
    return c


# ------------------------------------------------------------------------------------------- watch
def watch(body):
    """Raises his left wrist, looks down at it, taps a foot, looks up at the reader: well?"""
    T = 5.0
    c = Clip("watch", T, frames=150)
    up = REST.copy()
    up.set("head", 14, 6, -6)
    up.set("chest", 2, 6, 0)
    up.face.update({"grin": 0.0, "flat": 1.0})
    stare = up.copy()
    stare.set("head", -4, 2, 6)
    stare.face.update({"flat": 0.0, "smirk_R": 0.8})
    c.key(0.0, REST)
    c.key(0.75, up, "back")
    c.key(2.45, up, "linear")
    c.key(2.75, stare, "snap")
    c.key(3.75, stare, "linear")
    c.key(4.55, REST, "inout")
    c.key(5.0, REST, "linear")

    def layer(t):
        p = Pose()
        down = pulse(t, 0.6, 0.25, 1.6, 0.2)
        p = p + look((-22 * down, -10 * down))
        s = pulse(t, 2.7, 0.08, 1.0, 0.25)
        brows(p, 0.2 * s, 1.6 * s, 1.0 * s, side=-1)
        brows(p, -0.6 * s, -0.4 * s, 0.0, side=1)
        tap = max(0.0, math.sin(TAU * 2.6 * t)) ** 2 * pulse(t, 0.9, 0.1, 1.4, 0.1)
        p.add("head", 2 * tap, 0, 0)
        return p

    c.layer(layer)
    c.layer(blink_layer([1.9, 3.9]))
    rest_w = None

    def solve(t, p, skel):
        nonlocal rest_w
        if rest_w is None:
            q = REST.copy()
            body.plant(q, 1)
            body.plant(q, -1)
            rest_w = wrist_of(body, q, 1)
        w = pulse(t, 0.0, 0.75, 2.95, 0.8)
        target = V(0.1, -0.44, 1.42)
        hr = hand_world((-1, -0.15, 0.1), (0, 0.2, 1))        # fingers across his chest, back of wrist up
        if w > 0.001:
            body.hand_to(p, 1, rest_w.lerp(target, w), elbow=(0.55, 0.3, -0.25),
                         hand_rot=None if w < 0.5 else hr)
        tap = max(0.0, math.sin(TAU * 2.6 * t)) ** 2 * pulse(t, 0.9, 0.1, 1.4, 0.1)
        body.plant(p, 1)
        body.plant(p, -1, roll=-16 * tap)
        return p

    c.solve(solve)
    return c


# --------------------------------------------------------------------------------------------- sit
SIT_HIPS = V(0, 0.16, 0.30)            # where the hips end up, seated on the floor, relative to rest


def seated(p, body, k, lean=0.0):
    """Blend k of the way from standing to sitting on the floor, knees up, hands on the floor behind."""
    hz = body.hip_z
    d = V(0, SIT_HIPS.y, SIT_HIPS.z - hz) * k
    hips(body, p, d.x, d.y, d.z, pitch=-14 * k + lean)
    p.add("spine", 12 * k, 0, 0)
    p.add("chest", 6 * k, 0, 0)
    p.add("head", -6 * k, 0, 0)
    return p


def sit_feet(k):
    return {1: dict(pos=(0.04 * k, -0.42 * k, 0), yaw=12 * k), -1: dict(pos=(-0.04 * k, -0.42 * k, 0), yaw=12 * k)}


def sit(body):
    """Sits down on the floor with his knees up, leans back on his hands, rests, and gets back up."""
    T = 6.0
    c = Clip("sit", T, frames=180)
    c.key(0.0, REST)

    def k_of(t):
        # down: a little rise first, then down with a bump; up: a lean forward and a push
        if t < 0.3:
            return -0.04 * smooth(0, 0.3, t)
        if t < 1.45:
            return -0.04 + 1.04 * ease("inout", (t - 0.3) / 1.15)
        if t < 4.35:
            return 1.0
        if t < 5.6:
            return 1.0 - ease("inout", (t - 4.35) / 1.25)
        return 0.0

    def solve(t, p, skel):
        k = max(0.0, k_of(t))
        lean = 10 * pulse(t, 4.2, 0.35, 0.3, 0.6)
        seated(p, body, k, lean=lean)
        if k_of(t) < 0:
            hips(body, p, dz=-0.03 * smooth(0, 0.3, t))
        # rest: breathe, look round, a contented eye-close
        r = pulse(t, 1.5, 0.3, 2.4, 0.3)
        p.add("head", 4 * r * math.sin(TAU * t / 2.8), 10 * r * math.sin(TAU * (t - 1.5) / 3.0), 0)
        f = sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])
        # hands back to the floor behind him
        hk = smooth(0.7, 1.4, t) * (1 - smooth(4.2, 4.8, t))
        if hk > 0:
            for sg in (1, -1):
                rest_w = wrist_of(body, REST.copy(), sg)
                tgt = V(sg * 0.42, 0.42, 0.14)
                body.hand_to(p, sg, rest_w.lerp(tgt, hk), elbow=(0.4, 0.6, 0.0),
                             hand_rot=hand_world((sg * 0.2, 0.3, -1), (0, 0, -1)) if hk > 0.6 else None)
        # pushing up off the knees on the way up
        uk = pulse(t, 4.35, 0.3, 0.5, 0.4)
        if uk > 0:
            for sg in (1, -1):
                knee = body.where(p, f"shin{'_L' if sg > 0 else '_R'}")
                cur = wrist_of(body, p, sg)
                body.hand_to(p, sg, cur.lerp(knee + V(0, -0.05, 0.08), uk), elbow=(0.6, 0.2, -0.4))
        return p

    def face(t):
        p = Pose()
        r = pulse(t, 1.8, 0.4, 1.8, 0.3)
        p.both("lid_up", x=-28 * r)
        p.face["smile"] = r
        p.face["grin"] = -r
        e = pulse(t, 4.3, 0.15, 0.6, 0.3)
        p.face["grit"] = e
        p.face["grin"] += -e
        brows(p, -0.5 * e, -0.2 * e, 0.3 * e)
        return p

    c.layer(face)
    c.layer(blink_layer([0.9, 4.0, 5.7]))
    c.layer(lambda t: breathe(3.0, 1.0 + pulse(t, 1.5, 0.3, 2.4, 0.3))(t))
    c.solve(solve)
    return c


# ------------------------------------------------------------------------------------------- sleep
def sleep(body):
    """Sits down, nods off, sleeps (deep breaths, a snore), jerks awake, checks nobody saw, gets up."""
    T = 9.0
    c = Clip("sleep", T, frames=270)
    c.key(0.0, REST)

    def k_of(t):
        if t < 1.3:
            return ease("inout", t / 1.3)
        if t < 7.4:
            return 1.0
        if t < 8.6:
            return 1.0 - ease("inout", (t - 7.4) / 1.2)
        return 0.0

    def solve(t, p, skel):
        k = k_of(t)
        seated(p, body, k)
        asleep = smooth(1.8, 3.0, t) * (1 - smooth(6.55, 6.65, t))
        snore = 0.5 + 0.5 * math.sin(TAU * (t - 2.5) / 2.2)
        # the head droops, nodding with the breath, and lolls to his right
        p.add("head", 26 * asleep + 4 * asleep * snore, 0, 12 * asleep)
        p.add("neck", 8 * asleep, 0, 4 * asleep)
        p.add("chest", 4 * asleep * snore, 0, 0)
        # the startle: a jolt upright
        j = pulse(t, 6.6, 0.06, 0.25, 0.4)
        p.add("head", -10 * j, 0, 0)
        p.add("chest", -6 * j, 0, 0)
        # checking nobody saw: a look left, a look right
        lk = math.sin(TAU * (t - 6.9) / 0.9) * pulse(t, 6.9, 0.1, 0.7, 0.2)
        p.add("head", 0, 22 * lk, 0)
        f = sit_feet(k)
        body.plant(p, 1, **f[1])
        body.plant(p, -1, **f[-1])
        hk = smooth(0.6, 1.3, t) * (1 - smooth(7.2, 7.8, t))
        if hk > 0:
            for sg in (1, -1):
                rest_w = wrist_of(body, REST.copy(), sg)
                knee = body.where(p, f"shin{'_L' if sg > 0 else '_R'}")
                tgt = knee + V(-sg * 0.02, -0.06, 0.04)          # hands resting on his knees
                body.hand_to(p, sg, rest_w.lerp(tgt, hk), elbow=(0.6, 0.2, -0.4))
        return p

    def face(t):
        p = Pose()
        heavy = smooth(1.2, 2.2, t) * 0.55 + smooth(2.2, 2.9, t) * 0.45
        asleep = heavy * (1 - smooth(6.55, 6.62, t))
        p.both("lid_up", x=-48 * asleep)
        p.both("lid_lo", x=36 * asleep)
        snore = max(0.0, math.sin(TAU * (t - 2.5) / 2.2)) * smooth(2.6, 3.0, t) * (1 - smooth(6.5, 6.6, t))
        p.face["grin"] = -asleep
        p.face["oh"] = 0.8 * snore
        p.face["flat"] = asleep * (1 - snore)
        j = pulse(t, 6.6, 0.05, 0.5, 0.6)
        p.face["wide"] = j
        p.face["flat"] -= 0.0
        brows(p, 2.0 * j, 2.2 * j, 1.6 * j)
        p = p + look((6 * j, 0))
        sheepish = pulse(t, 7.3, 0.2, 0.8, 0.3)
        p.face["smirk_R"] = sheepish
        p.face["grin"] -= sheepish * 0.5
        return p

    c.layer(face)
    c.layer(lambda t: breathe(2.2, 1.0 + 1.5 * smooth(1.8, 3.0, t) * (1 - smooth(6.5, 6.6, t)))(t))
    c.layer(blink_layer([0.6, 7.6, 8.4]))
    c.solve(solve)
    return c


# ------------------------------------------------------------------------------------------- press
def press(body):
    """Jabs at a button off to his left that won't work: a careful press, two harder ones, a flurry, then a
    look at the reader. The button is the page's (a picture of one); his finger meets it at the jabs."""
    T = 4.5
    c = Clip("press", T, frames=135)
    aim = REST.copy()
    aim.set("head", 2, 14, -2)
    aim.set("chest", 0, 10, -2)
    point(aim, 1)
    aim.face.update({"grin": 0.3, "smirk_L": 0.6})
    cross = aim.copy()
    cross.face = {"grit": 1.0}
    after = REST.copy()
    after.set("head", -3, -6, 8)
    after.face = {"flat": 1.0}
    c.key(0.0, REST)
    c.key(0.7, aim, "inout")
    c.key(2.9, cross, "linear")
    c.key(3.45, cross, "linear")
    c.key(3.75, after, "snap")
    c.key(4.4, REST, "inout")
    c.key(4.5, REST, "linear")
    button = V(0.86, -0.46, 1.44)
    # (start, depth) of each jab: one careful, two harder, a flurry of three
    jabs = [(1.0, 0.6), (1.55, 1.0), (2.05, 1.0), (3.0, 1.0), (3.17, 1.0), (3.34, 1.0)]

    def jab(t):
        v = 0.0
        for a, d in jabs:
            v = max(v, d * pulse(t, a, 0.06 if a < 2.9 else 0.035, 0.05, 0.1 if a < 2.9 else 0.05))
        return v

    def layer(t):
        p = Pose()
        j = jab(t)
        p.add("chest", 0, 0, -2 * j)
        p.add("head", 0, 0, 2 * j)
        f = pulse(t, 2.15, 0.1, 0.5, 0.2)
        brows(p, -1.2 * f, -0.6 * f, 0.4 * f)
        s = pulse(t, 3.7, 0.1, 0.5, 0.25)
        brows(p, 0.0, 1.5 * s, 1.2 * s, side=1)
        p = p + look((0, 20 * pulse(t, 0.4, 0.3, 2.9, 0.2)))
        return p

    c.layer(layer)
    c.layer(blink_layer([0.5, 2.5, 3.9]))

    def solve(t, p, skel):
        w = pulse(t, 0.2, 0.55, 2.85, 0.45)
        if w > 0.001:
            q = REST.copy()
            body.plant(q, 1)
            body.plant(q, -1)
            rw = wrist_of(body, q, 1)
            d = (button - V(0.33, 0, 1.5)).normalized()
            ready = button - d * 0.42                     # wrist, finger a hand's length short of the button
            tgt = ready + d * 0.13 * jab(t)
            hr = hand_world(d, (0, 0.2, -1))
            body.hand_to(p, 1, rw.lerp(tgt, w), elbow=(0.3, 0.5, -0.5), hand_rot=hr if w > 0.5 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    return c


# ------------------------------------------------------------------------------------------- shrug
def shrug(body):
    """Shoulders up, palms up, head on one side: what can you do."""
    T = 2.0
    c = Clip("shrug", T, frames=60)
    up = REST.copy()
    up.both("shoulder", z=14)
    up.set("head", -4, 0, 12)
    up.set("chest", -4, 0, 0)
    for sg in (1, -1):
        open_hand(up, sg, 8)
    up.face = {"flat": 0.6, "smirk_L": 0.5}
    c.key(0.0, REST)
    c.key(0.45, up, "back")
    c.key(1.25, up, "linear")
    c.key(1.85, REST, "inout")
    c.key(2.0, REST, "linear")

    def layer(t):
        p = Pose()
        u = pulse(t, 0.2, 0.25, 0.8, 0.4)
        brows(p, 1.6 * u, 1.8 * u, 0.8 * u)
        return p

    c.layer(layer)

    def solve(t, p, skel):
        w = pulse(t, 0.0, 0.45, 0.8, 0.6)
        if w > 0.001:
            for sg in (1, -1):
                q = REST.copy()
                body.plant(q, 1)
                body.plant(q, -1)
                rw = wrist_of(body, q, sg)
                tgt = V(sg * 0.5, -0.36, 1.16)
                hr = hand_world((sg * 0.55, -0.82, 0.08), (0, 0, 1))  # palm up, fingers forward and out
                body.hand_to(p, sg, rw.lerp(tgt, w), elbow=(0.15, 0.25, -1.0), hand_rot=hr if w > 0.4 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    return c


# -------------------------------------------------------------------------------------------- walk
def walk(body, name="walk", back=False):
    """One stride in place (two steps), a strut: a bounce in it, the shoulders rolling against the hips,
    the arms swinging, the chin up and the crest bouncing a beat behind. `back` makes the moonwalk: the
    feet slide forward while the page moves him backwards, the toe of the back foot up on its ball."""
    T = WALK_PERIOD if not back else MOON_PERIOD
    c = Clip(name, T, loop=True, frames=int(round(T * 30)))
    base = REST.copy()
    base.set("chest", -5, 0, 0)
    base.set("head", -6, 0, 0)
    c.key(0.0, base)

    def layer(t):
        u = t / T
        p = Pose()
        # two bounces a stride: lowest just after each heel strike
        bob = math.cos(TAU * 2 * (u - 0.08))
        hips(body, p, dz=-0.03 + 0.022 * bob, dx=0.018 * math.sin(TAU * u), yaw=-6 * math.sin(TAU * u),
             roll=2.5 * math.sin(TAU * u))
        p.add("spine", 2, 0, 0)
        p.add("chest", 0, 9 * math.sin(TAU * u), -1.5 * math.sin(TAU * u))
        p.add("head", 1.5 * bob, -3 * math.sin(TAU * u), 0)
        swing = math.sin(TAU * u)
        p.side("upper_arm", 1, x=-24 * swing, z=4, add=True)
        p.side("upper_arm", -1, x=24 * swing, z=4, add=True)
        p.side("forearm", 1, x=18 + 14 * max(0.0, -swing), add=True)
        p.side("forearm", -1, x=18 + 14 * max(0.0, swing), add=True)
        p = p + crest_follow(t * 6, 1.2, 1.0)
        p.add("crest_1", 3 * bob, 0, 0)
        p.add("crest_2", 4 * math.cos(TAU * 2 * (u - 0.2)), 0, 0)
        return p

    c.layer(layer)

    def solve(t, p, skel):
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            if not back:
                y, lift, roll = stride_foot(t, T, WALK_STRIDE, WALK_STANCE, ph, height=0.14)
            else:
                # moonwalk: one foot up on its ball holds the floor while he glides back over it, so it
                # moves forward under him; the other, flat, slides back past it; at the swap the heels trade.
                u = (t / T + ph) % 1.0
                swap = 0.12
                if u < 0.5:
                    y = WALK_STRIDE / 2 - WALK_STRIDE * (u / 0.5)
                    roll = 30 * smooth(0.0, swap, u) * (1 - smooth(0.5 - swap * 0.4, 0.5, u))
                else:
                    y = -WALK_STRIDE / 2 + WALK_STRIDE * ((u - 0.5) / 0.5)
                    roll = 0.0
                lift = 0.0
            body.plant(p, sg, pos=(0, y, 0), roll=roll, lift=lift, yaw=4)
        return p

    c.solve(solve)
    return c


# ------------------------------------------------------------------------------------------ dances
class Dance:
    """A dance as a function of the beat: `move(b, p, feet, hands)` writes the pattern's pose for beat
    position b (0.. beats) into `p`, foot plants into `feet` and hand targets into `hands`. It eases in
    from REST over the first half second and out over the last."""

    def __init__(self, body, name, frames, beats, move, ramp=0.5):
        self.body, self.name, self.frames, self.beats, self.move, self.ramp = body, name, frames, beats, move, ramp

    def clip(self):
        body = self.body
        T = self.frames / 30
        c = Clip(self.name, T, frames=self.frames)
        beat = T / self.beats
        c.key(0.0, REST)
        q = REST.copy()
        body.plant(q, 1)
        body.plant(q, -1)
        rest_wrists = {sg: wrist_of(body, q, sg) for sg in (1, -1)}

        def solve(t, p0, skel):
            w = env(t, T, self.ramp, self.ramp)
            d = REST.copy()
            feet, hands = {}, {}
            self.move(t / beat, d, feet, hands)
            p = blend(REST, d, w)
            p.quat = {}
            # hips movements the move asked for live in d.loc["hips"], blended above
            for sg in (1, -1):
                s = dict(feet.get(sg, {}))
                for key in ("pos",):
                    if key in s:
                        s[key] = tuple(v * w for v in s[key])
                for key in ("yaw", "roll", "lift", "bank", "knee_out"):
                    if key in s:
                        s[key] = s[key] * w
                body.plant(p, sg, **s)
            for sg, h in hands.items():
                tgt, elbow, hr = h
                body.hand_to(p, sg, rest_wrists[sg].lerp(tgt, w), elbow=elbow, hand_rot=hr if w > 0.6 else None)
            return p

        c.solve(solve)
        c.layer(blink_layer([T * 0.21, T * 0.47, T * 0.73, T * 0.93]))
        return c


def hop(b, period=1.0, height=0.05, phase=0.0):
    """Hips up and down once per `period` beats, a sharp landing."""
    u = (b / period + phase) % 1.0
    return height * math.sin(math.pi * u) ** 1.5


def bounce(b, depth=0.035, phase=0.0):
    """A knee bounce on every beat: down on the beat."""
    u = (b + phase) % 1.0
    return -depth * (0.5 + 0.5 * math.cos(TAU * u))


def beat_side(b):
    """+1 / -1 alternating each beat, eased through the change (the swing of a two-beat pattern)."""
    s = math.sin(math.pi * (b - 0.5))
    return math.copysign(abs(s) ** 0.55, s)


def dances(body):
    D = {}

    def mv_hips(p, dx=0.0, dy=0.0, dz=0.0, pitch=0.0, yaw=0.0, roll=0.0):
        hips(body, p, dx, dy, dz, pitch, yaw, roll)

    # ---- floss: straight arms swung together side to side, one in front and one behind, hips opposite --
    def floss(b, p, feet, hands):
        s = beat_side(b)                                # +1: arms out to his left
        for sg in (1, -1):
            # the arm on the side the arms swing to goes out and behind; the other crosses in front
            out = s * sg
            p.side("upper_arm", sg, x=-38 * out + 4, y=0, z=-50 + 42 * out)
            p.side("forearm", sg, x=4, y=0, z=0)
            fist(p, sg)
        mv_hips(p, dx=-0.11 * s, dz=bounce(b, 0.02), roll=9 * s)
        p.add("spine", 0, 0, -8 * s)
        p.add("chest", 0, 6 * s, -5 * s)
        p.add("head", 4 * abs(s), 0, 4 * s)
        p.face.update({"grin": 0.6, "smirk_L": 0.5})
        p.both("lid_up", x=-12)
        feet[1] = dict(pos=(0.05, 0, 0))
        feet[-1] = dict(pos=(-0.05, 0, 0))

    D["floss"] = Dance(body, "floss", 480, 48, floss)

    # ---- take the L: an L on his forehead, hopping foot to foot, the free leg kicked out --------------
    def take_l(b, p, feet, hands):
        k = int(b) % 2                                  # which foot he's on this beat
        u = b % 1.0
        on = 1 if k == 0 else -1                        # standing side
        kick = math.sin(math.pi * u)
        mv_hips(p, dx=0.06 * on, dz=hop(b, 1.0, 0.07) - 0.02, roll=-5 * on, pitch=4)
        p.add("chest", 0, -6 * on, 4 * on)
        p.add("head", 4, 0, -6 * on)
        feet[on] = dict(pos=(0, 0, 0), lift=hop(b, 1.0, 0.07) * 0.5)
        feet[-on] = dict(pos=(-on * 0.22 * kick, -0.05, 0), lift=0.22 * kick, roll=-20 * kick, yaw=20)
        # the L: right hand at his brow, thumb and index out
        sx = -1
        hands[sx] = (V(-0.05, -0.38, 2.12), (0.5, 0.2, -0.3), hand_world((0.1, -0.2, 1), (0, -1, 0)))
        point(p, sx)
        p.set("thumb_1_R", 0, 0, 0); p.set("thumb_2_R", 0, 0, 0); p.set("thumb_3_R", 0, 0, 0)
        # left hand on his hip
        hands[1] = (V(0.3, -0.04, 1.08), (0.6, 0.3, 0.0), hand_world((-0.6, -0.2, -1), (-1, 0, 0)))
        fist(p, 1, 0.7)
        p.face.update({"grin": 0.2, "smirk_R": 0.9})
        p.both("lid_up", x=-14)
        brows(p, 0.8, 1.6, 1.2)

    D["take-the-l"] = Dance(body, "take-the-l", 480, 32, take_l)

    # ---- default dance: kicks forward with the opposite punch, a lean back every eight beats ---------
    def default(b, p, feet, hands):
        bar = int(b // 8) % 2
        u = b % 1.0
        k = int(b) % 2
        side = 1 if k == 0 else -1
        if bar == 0:
            kick = math.sin(math.pi * u) ** 1.3
            feet[side] = dict(pos=(0, -0.3 * kick, 0), lift=0.16 * kick, roll=-25 * kick)
            feet[-side] = dict()
            mv_hips(p, dz=bounce(b, 0.04) - 0.015, pitch=-6 * kick, yaw=-6 * side)
            for sg in (1, -1):
                punch = kick if sg == -side else 0.0
                p.side("upper_arm", sg, x=30 + 55 * punch, z=-35 + 10 * punch)
                p.side("forearm", sg, x=85 - 70 * punch)
                fist(p, sg)
            p.add("chest", 0, 8 * side, 0)
        else:
            # pumping both fists down on the beat, knees bouncing, leaning back on the last two beats
            pump = 0.5 + 0.5 * math.cos(TAU * u)
            lb = smooth(6, 6.5, b % 8) * (1 - smooth(7.6, 8.0, b % 8))
            mv_hips(p, dz=bounce(b, 0.05), pitch=-10 * lb, dy=0.04 * lb)
            for sg in (1, -1):
                p.side("upper_arm", sg, x=40 + 15 * pump, z=-30 + 20 * lb)
                p.side("forearm", sg, x=70 + 25 * pump - 40 * lb)
                fist(p, sg)
            p.add("chest", -10 * lb, 0, 0)
            p.add("head", -8 * lb + 4 * pump, 0, 0)
            feet[1] = dict(pos=(0.03, 0, 0))
            feet[-1] = dict(pos=(-0.03, 0, 0))
        p.face.update({"grin": 1.0})
        brows(p, 0.6, 0.8, 0.6)

    D["default-dance"] = Dance(body, "default-dance", 450, 48, default)

    # ---- orange justice: both arms swung low across the body, the legs kicking out in turn -----------
    def orange(b, p, feet, hands):
        s = beat_side(b)
        swing = math.sin(math.pi * b)
        for sg in (1, -1):
            out = s * sg
            p.side("upper_arm", sg, x=35 - 10 * out, z=-45 + 32 * out)
            p.side("forearm", sg, x=30 + 20 * (1 - abs(s)))
            open_hand(p, sg, 6)
        k = int(b) % 2
        side = 1 if k == 0 else -1
        u = b % 1.0
        kk = math.sin(math.pi * u)
        feet[side] = dict(pos=(side * 0.12 * kk, -0.08 * kk, 0), lift=0.12 * kk, roll=-15 * kk, yaw=-20 * kk)
        feet[-side] = dict(roll=10 * kk)
        mv_hips(p, dx=0.05 * s, dz=bounce(b, 0.04), roll=-5 * s, yaw=8 * s)
        p.add("chest", 0, -10 * s, 3 * s)
        p.add("head", 5 * abs(swing), 0, -5 * s)
        p.face.update({"wide": 0.6, "grin": 0.4})
        brows(p, 1.0, 1.4, 1.0)

    D["orange-justice"] = Dance(body, "orange-justice", 480, 48, orange)

    # ---- the robot: stiff snaps between held poses, a buzz on each arrival ---------------------------
    robo = []
    for la, lf, ra, rf, hd, ch in [(0, 90, 0, 0, 25, 0), (0, 0, 0, 90, -25, 0), (60, 90, 60, 90, 0, 20),
                                   (90, 0, -10, 90, 0, -20), (-10, 90, 90, 0, 20, 0), (30, 120, 30, 120, -20, 0),
                                   (80, 10, 80, 10, 0, 0), (0, 90, 0, 90, 0, 0)]:
        robo.append((la, lf, ra, rf, hd, ch))

    def robot(b, p, feet, hands):
        i = int(b) % len(robo)
        j = (i + 1) % len(robo)
        u = b % 1.0
        k = ease("snap", smooth(0.0, 0.25, u))         # snap at the start of the beat, then hold
        buzz = math.exp(-u * 18) * math.sin(u * 140) * 1.5
        A, B = robo[i - 1] if i else robo[-1], robo[i]
        la, lf, ra, rf, hd, ch = [x + (y - x) * k for x, y in zip(A, B)]
        p.side("upper_arm", 1, x=la, z=-40)
        p.side("forearm", 1, x=lf + buzz)
        p.side("upper_arm", -1, x=ra, z=-40)
        p.side("forearm", -1, x=rf - buzz)
        p.both("hand", x=0)
        for sg in (1, -1):
            open_hand(p, sg, 0)
        p.add("head", 0, hd, 0)
        p.add("chest", 0, ch, 0)
        mv_hips(p, dz=-0.03 - 0.02 * (int(b) % 2))
        feet[1] = dict(pos=(0.05, 0, 0))
        feet[-1] = dict(pos=(-0.05, 0, 0))
        p.face.update({"grin": 0.0, "flat": 1.0})
        p.both("lid_up", x=-8)

    D["robot"] = Dance(body, "robot", 480, 32, robot)

    # ---- electro shuffle: heel-toe shuffles side to side, fists pumping down -------------------------
    def shuffle(b, p, feet, hands):
        u = b % 1.0
        k = int(b) % 4
        travel = [0, 1, 0, -1][k]
        heel = math.sin(math.pi * u)
        for sg in (1, -1):
            tw = 25 * heel * (1 if (int(b) % 2 == 0) else -1)
            feet[sg] = dict(pos=(sg * 0.04 + 0.05 * travel * heel, 0, 0), yaw=tw * sg, roll=8 * heel)
        mv_hips(p, dz=bounce(b, 0.05), dx=0.03 * travel * heel)
        pump = 0.5 + 0.5 * math.cos(TAU * u)
        side = 1 if int(b) % 2 == 0 else -1
        for sg in (1, -1):
            a = pump if sg == side else 1 - pump
            p.side("upper_arm", sg, x=20 + 10 * a, z=-30 + 15 * a)
            p.side("forearm", sg, x=40 + 50 * a)
            fist(p, sg)
        p.add("chest", 6, 0, 3 * side)
        p.add("head", 6 * pump, 0, 0)
        p.face.update({"grin": 0.8, "ee": 0.3})

    D["electro-shuffle"] = Dance(body, "electro-shuffle", 450, 30, shuffle)

    # ---- hype: fists swung side to side at the chest, knees pumping, a hip pop ------------------------
    def hype(b, p, feet, hands):
        s = beat_side(b)
        for sg in (1, -1):
            p.side("upper_arm", sg, x=45 + 15 * s * sg, z=-20 + 15 * s * sg)
            p.side("forearm", sg, x=95 - 20 * s * sg)
            fist(p, sg)
        k = int(b) % 2
        side = 1 if k == 0 else -1
        u = b % 1.0
        step = math.sin(math.pi * u)
        feet[side] = dict(lift=0.08 * step, roll=-10 * step)
        feet[-side] = dict()
        mv_hips(p, dx=0.04 * s, dz=bounce(b, 0.05), roll=-4 * s, yaw=6 * s)
        p.add("chest", 0, 12 * s, 0)
        p.add("head", 6 * (0.5 + 0.5 * math.cos(TAU * u)), -5 * s, 0)
        p.face.update({"wide": 0.4, "grin": 0.6})
        brows(p, 1.2, 1.4, 1.0)

    D["hype"] = Dance(body, "hype", 480, 32, hype)

    # ---- boogie down: the disco point, up across and down to the hip, hips swaying -------------------
    def boogie(b, p, feet, hands):
        u = b % 2.0 / 2.0
        up = 0.5 - 0.5 * math.cos(TAU * u)               # 0 down at the hip, 1 up and across
        # right arm points up to his left, then down to his right hip
        tgt = V(-0.45, -0.25, 1.0).lerp(V(0.25, -0.35, 2.55), up)
        hands[-1] = (tgt, (0.4, 0.3, -0.4), hand_world((tgt - V(-0.3, 0, 1.55)).normalized(), (0, -1, 0)))
        point(p, -1)
        hands[1] = (V(0.3, -0.04, 1.08), (0.6, 0.3, 0.0), hand_world((-0.6, -0.2, -1), (-1, 0, 0)))
        fist(p, 1, 0.7)
        sway = math.sin(math.pi * b)
        mv_hips(p, dx=0.06 * sway, dz=bounce(b, 0.03), roll=-5 * sway)
        p.add("chest", 0, -8 * up, 6 * up)
        p.add("head", -6 * up, -12 * up, 0)
        feet[1] = dict(pos=(0.06, 0, 0), roll=6 * max(0.0, sway))
        feet[-1] = dict(pos=(-0.06, 0, 0), roll=6 * max(0.0, -sway))
        p.face.update({"grin": 0.5, "oh": 0.4 * up, "smirk_L": 0.4})
        brows(p, 1.0 * up, 1.4 * up, 1.0 * up)

    D["boogie-down"] = Dance(body, "boogie-down", 450, 30, boogie)

    # ---- get griddy: heel taps forward in turn, arms swinging, goggles every fourth bar --------------
    def griddy(b, p, feet, hands):
        k = int(b) % 2
        side = 1 if k == 0 else -1
        u = b % 1.0
        tap = math.sin(math.pi * u)
        feet[side] = dict(pos=(0, -0.28 * tap, 0), lift=0.05 * tap, roll=-28 * tap)
        feet[-side] = dict(pos=(0, 0.04, 0), roll=10 * tap)
        mv_hips(p, dz=-0.07 + bounce(b, 0.03), pitch=10, dy=0.03)
        goggles = (int(b) // 4) % 4 == 3
        if goggles:
            for sg in (1, -1):
                eye = V(sg * 0.11, -0.42, 1.95)
                hands[sg] = (eye + V(sg * 0.06, -0.06, -0.08), (0.5, 0.0, -0.3),
                             hand_world((-sg * 0.3, 0, 1), (0, 1, 0)))
                point(p, sg)
            p.face.update({"grin": 0.0, "oh": 0.6, "wide": 0.3})
        else:
            for sg in (1, -1):
                sw = (1 if sg == side else -1) * tap
                p.side("upper_arm", sg, x=30 * sw + 10, z=-40 + 12 * abs(sw))
                p.side("forearm", sg, x=50 + 30 * abs(sw))
                fist(p, sg, 0.8)
            p.face.update({"grin": 1.0})
        p.add("chest", 8, 8 * side, 0)
        p.add("head", -8, 0, 4 * side)

    D["get-griddy"] = Dance(body, "get-griddy", 480, 32, griddy)

    # ---- billy bounce: bouncing on the spot, forearms up and down in turn, shoulders shimmying -------
    def billy(b, p, feet, hands):
        u = b % 1.0
        side = 1 if int(b) % 2 == 0 else -1
        lift = math.sin(math.pi * u)
        for sg in (1, -1):
            a = lift if sg == side else 0.0
            p.side("upper_arm", sg, x=40 + 20 * a, z=-35)
            p.side("forearm", sg, x=70 + 40 * a)
            open_hand(p, sg, 4)
            p.side("hand", sg, x=-30 * a)
        step = (b % 4) / 4
        lat = math.sin(TAU * step) * 0.08
        mv_hips(p, dx=lat, dz=hop(b, 1.0, 0.045) - 0.03)
        p.both("shoulder", z=5 * math.sin(TAU * b * 2), add=True)
        feet[1] = dict(pos=(lat, 0, 0), lift=hop(b, 1.0, 0.045) * 0.6, roll=8 * lift)
        feet[-1] = dict(pos=(lat, 0, 0), lift=hop(b, 1.0, 0.045) * 0.6, roll=8 * lift)
        p.add("head", 5 * lift, 0, -4 * side)
        p.face.update({"grin": 0.7, "smile": 0.3})

    D["billy-bounce"] = Dance(body, "billy-bounce", 480, 32, billy)

    # ---- fresh: the Carlton: arms swinging across, a side step each way, a snap at the end ------------
    def fresh(b, p, feet, hands):
        s = beat_side(b)
        for sg in (1, -1):
            out = s * sg
            p.side("upper_arm", sg, x=40 + 20 * out, z=-45 + 25 * out)
            p.side("forearm", sg, x=50 + 30 * (1 - out) / 2)
            open_hand(p, sg, 3)
        k = int(b) % 2
        side = 1 if k == 0 else -1
        u = b % 1.0
        st = math.sin(math.pi * u)
        feet[side] = dict(pos=(side * 0.1 * st, 0, 0), lift=0.06 * st)
        feet[-side] = dict(roll=8 * st)
        mv_hips(p, dx=0.06 * s, dz=bounce(b, 0.03), roll=-5 * s)
        p.add("chest", 0, -14 * s, 0)
        p.add("head", 0, 14 * s, -6 * s)
        p.face.update({"grin": 0.6, "ee": 0.5})
        brows(p, 0.8, 1.2, 0.8)

    D["fresh"] = Dance(body, "fresh", 480, 32, fresh)

    # ---- scenario: hopping, knees up in turn, arms rolling over each other in front ------------------
    def scenario(b, p, feet, hands):
        u = b % 1.0
        side = 1 if int(b) % 2 == 0 else -1
        knee = math.sin(math.pi * u)
        feet[side] = dict(pos=(0, -0.12 * knee, 0), lift=0.26 * knee, roll=-10 * knee)
        feet[-side] = dict(lift=hop(b, 1.0, 0.06) * 0.6)
        mv_hips(p, dz=hop(b, 1.0, 0.06) - 0.03, pitch=4)
        roll_ = TAU * b * 0.5
        for sg in (1, -1):
            ph = roll_ + (0 if sg > 0 else math.pi)
            p.side("upper_arm", sg, x=55 + 15 * math.sin(ph), z=-30)
            p.side("forearm", sg, x=80 + 25 * math.cos(ph))
            fist(p, sg)
        p.add("chest", 6, 6 * side, 0)
        p.add("head", 4 * knee, 0, 0)
        p.face.update({"grin": 0.5, "wide": 0.5})
        brows(p, 1.5, 1.6, 1.2)

    D["scenario"] = Dance(body, "scenario", 480, 32, scenario)

    # ---- groove jam: shoulder rolls, a step touch, a clap on two and four ----------------------------
    def groove(b, p, feet, hands):
        u = b % 1.0
        side = 1 if int(b) % 2 == 0 else -1
        st = math.sin(math.pi * u)
        feet[side] = dict(pos=(side * 0.16 * st, 0, 0), lift=0.05 * st, roll=-6 * st)
        feet[-side] = dict()
        mv_hips(p, dx=0.07 * side * st, dz=bounce(b, 0.03), roll=-4 * side * st)
        clap = int(b) % 2 == 1
        if clap:
            cl = pulse(u, 0.0, 0.2, 0.1, 0.3)
            for sg in (1, -1):
                hands[sg] = (V(sg * (0.06 + 0.15 * (1 - cl)), -0.45, 1.5), (0.6, 0.4, -0.4),
                             hand_world((0, -0.2, 1), (-sg, 0, 0)))
                open_hand(p, sg, 0)
        else:
            for sg in (1, -1):
                p.side("upper_arm", sg, x=25, z=-35)
                p.side("forearm", sg, x=70)
                p.fingers(sg, 30, thumb=20)
        roll_ = TAU * b * 0.5
        p.side("shoulder", 1, z=6 * math.sin(roll_), add=True)
        p.side("shoulder", -1, z=6 * math.sin(roll_ + math.pi), add=True)
        p.add("head", 4 * st, 6 * side * st, 0)
        p.face.update({"smile": 0.6, "grin": 0.4})
        p.both("lid_up", x=-16)

    D["groove-jam"] = Dance(body, "groove-jam", 480, 32, groove)

    # ---- headbang: wide stance, knees bent, the head (and crest) slamming on the beat, fist pumps ------
    def headbang(b, p, feet, hands):
        u = b % 1.0
        bang = math.exp(-u * 6) * (1 - math.exp(-u * 60))
        mv_hips(p, dz=-0.11 - 0.03 * bang, pitch=8)
        feet[1] = dict(pos=(0.14, 0, 0), yaw=14)
        feet[-1] = dict(pos=(-0.14, 0, 0), yaw=14)
        p.add("spine", 6 + 10 * bang, 0, 0)
        p.add("chest", 4 + 14 * bang, 0, 0)
        p.add("neck", 10 * bang, 0, 0)
        p.add("head", -6 + 28 * bang, 0, 0)
        p.add("crest_1", -14 * bang, 0, 0)
        p.add("crest_2", -18 * bang, 0, 0)
        p.add("crest_3", -20 * bang, 0, 0)
        side = 1 if int(b) % 2 == 0 else -1
        for sg in (1, -1):
            pump = bang if sg == side else 0.2
            p.side("upper_arm", sg, x=40 + 60 * pump, z=-10 + 30 * pump)
            p.side("forearm", sg, x=90 - 50 * pump)
            fist(p, sg)
        p.face.update({"grit": 0.6, "wide": 0.4 * bang})
        p.both("lid_up", x=-30)
        brows(p, -1.0, -0.4, 0.4)

    D["headbang"] = Dance(body, "headbang", 480, 32, headbang)

    # ---- the drop: a build-up crouch, lower and lower, fists shaking; the drop; jumping wild ----------
    def drop(b, p, feet, hands):
        if b < 15:
            k = b / 15
            shake = math.sin(TAU * b * 4) * (0.3 + 0.7 * k)
            mv_hips(p, dz=-0.05 - 0.22 * k, pitch=10 * k)
            p.add("spine", 10 * k, 0, 0)
            p.add("chest", 8 * k + 2 * shake, 0, 0)
            p.add("head", -10 * k, 0, 0)
            for sg in (1, -1):
                p.side("upper_arm", sg, x=30 + 20 * k, z=-30 + 3 * shake)
                p.side("forearm", sg, x=100 + 4 * shake)
                fist(p, sg)
            feet[1] = dict(pos=(0.1 * k, 0, 0), yaw=10 * k)
            feet[-1] = dict(pos=(-0.1 * k, 0, 0), yaw=10 * k)
            p.face.update({"grin": 0.0, "grit": k, "oh": 0.0})
            brows(p, -1.2 * k, -0.6 * k, 0.4 * k)
            p.both("lid_up", x=-20 * k)
        elif b < 16:
            # the drop: explode upwards, arms flung up
            u = b - 15
            jump = math.sin(math.pi * u)
            mv_hips(p, dz=-0.27 + 0.5 * jump)
            for sg in (1, -1):
                p.side("upper_arm", sg, x=10, z=-30 + 140 * ease("snap", u))
                p.side("forearm", sg, x=10)
                open_hand(p, sg, 14)
            feet[1] = dict(pos=(0.1, 0, 0), lift=0.32 * jump, roll=-10 * jump)
            feet[-1] = dict(pos=(-0.1, 0, 0), lift=0.32 * jump, roll=-10 * jump)
            p.face.update({"wide": 1.0})
            brows(p, 2.2, 2.4, 1.8)
        else:
            u = b % 1.0
            jump = math.sin(math.pi * u) ** 1.2
            side = 1 if int(b) % 2 == 0 else -1
            mv_hips(p, dz=-0.05 + 0.18 * jump, dx=0.03 * side)
            for sg in (1, -1):
                pump = jump if sg == side else 0.6
                p.side("upper_arm", sg, x=20, z=40 + 70 * pump)
                p.side("forearm", sg, x=20 + 40 * (1 - pump))
                fist(p, sg)
            p.add("head", -8 * jump, 0, 8 * side)
            feet[1] = dict(pos=(0.08, 0, 0), lift=0.14 * jump)
            feet[-1] = dict(pos=(-0.08, 0, 0), lift=0.14 * jump)
            p.face.update({"wide": 0.8, "grin": 0.4})
            brows(p, 1.6, 1.8, 1.4)

    D["the-drop"] = Dance(body, "the-drop", 480, 32, drop)
    return {k: v.clip() for k, v in D.items()}


EVERYDAY = ["idle", "watch", "sit", "sleep", "press", "shrug", "walk", "moonwalk", "core-show"]
DANCES = ["floss", "take-the-l", "default-dance", "orange-justice", "robot", "electro-shuffle", "hype",
          "boogie-down", "get-griddy", "billy-bounce", "fresh", "scenario", "groove-jam", "headbang", "the-drop"]
# archie.glb carries the model and the everyday clips; archie-dances.glb the dances, fetched in idle time.
PACKS = {"archie": EVERYDAY, "archie-dances": DANCES}

# -------------------------------------------------------------------------------------------- core
# The Atlas Core act: he takes the Core out of the dock in his belly, holds it up palm up, it unfolds and
# projects the world of the page the reader is on, he presents it, and it folds and goes back. The page
# moves the Core between his `core` bone and his `grip_L` at the two hand-offs, and plays the Core's own
# clips (art/pals/core.py) at these times:
CORE_GRAB, CORE_UNFOLD, CORE_FOLD, CORE_DOCK, CORE_SECS = 0.62, 1.35, 6.05, 7.5, 8.6
CORE_HOLD = (0.14, -0.46, 1.42)         # his left wrist while he holds it up


def core_show(body):
    T = CORE_SECS
    c = Clip("core-show", T, frames=int(round(T * 30)))
    c.key(0.0, REST)
    look_down = REST.copy()
    look_down.set("head", 18, 6, -4)
    look_down.set("chest", 6, 4, 0)
    proud = REST.copy()
    proud.set("head", -4, 10, 4)
    proud.set("chest", -6, 6, 0)
    proud.face = {"grin": 1.0}
    c.key(0.45, look_down, "inout")
    c.key(1.1, proud, "back")
    c.key(5.9, proud, "linear")
    c.key(6.6, look_down, "inout")
    c.key(7.7, look_down, "linear")
    c.key(T, REST, "inout")
    dock = V(0.0, -0.2, 1.225)              # in front of the dock (art/pals/archie.py dock_c)
    hold = V(*CORE_HOLD)
    palm_up = hand_world((-0.35, -0.9, 0.05), (0, 0, 1))
    palm_in = hand_world((-0.3, -0.2, -1), (-1, 0, 0))

    def solve(t, p, skel):
        rw = wrist_of(body, REST, 1)
        # left hand: to the dock (0.15-0.6), out and up holding it (0.62-1.1), held, back down (6.9-7.5),
        # away (7.5-8.2)
        if t < CORE_GRAB:
            k = smooth(0.15, CORE_GRAB, t)
            tgt, hr = rw.lerp(dock + V(0.12, -0.02, -0.02), k), palm_in if k > 0.5 else None
        elif t < 6.9:
            k = ease("back", min(1.0, (t - CORE_GRAB) / 0.5))
            bob = 0.012 * math.sin(math.tau * (t - 1.2) / 2.2) * smooth(1.2, 1.8, t)
            tgt, hr = (dock + V(0.12, -0.02, -0.02)).lerp(hold, k) + V(0, 0, bob), palm_up if k > 0.3 else palm_in
        elif t < CORE_DOCK:
            k = smooth(6.9, CORE_DOCK, t)
            tgt, hr = hold.lerp(dock + V(0.12, -0.02, -0.02), k), palm_in if k > 0.6 else palm_up
        else:
            k = smooth(CORE_DOCK, CORE_DOCK + 0.7, t)
            tgt, hr = (dock + V(0.12, -0.02, -0.02)).lerp(rw, k), palm_in if k < 0.5 else None
        body.hand_to(p, 1, tgt, elbow=(0.55, 0.35, -0.5), hand_rot=hr)
        p.fingers(1, 30 if t > CORE_GRAB else 55 * smooth(0.4, CORE_GRAB, t), spread=6, thumb=20)
        # right hand: the presenter's sweep, palm up towards it, on the unfold, and a point at the reader
        ta = pulse(t, CORE_UNFOLD + 0.1, 0.45, 2.1, 0.5)
        if ta > 0.01:
            tgt_r = rw_r.lerp(V(-0.36, -0.5, 1.4), ta)
            body.hand_to(p, -1, tgt_r, elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((0.7, -0.6, 0.2), (0, 0, 1)) if ta > 0.5 else None)
            open_hand(p, -1, 10 * ta)
        pt = pulse(t, 4.3, 0.25, 0.9, 0.35)
        if pt > 0.01:
            cur = wrist_of(body, p, -1)
            body.hand_to(p, -1, cur.lerp(V(-0.3, -0.62, 1.55), pt), elbow=(0.5, 0.3, -0.5),
                         hand_rot=hand_world((0.1, -1, 0.15), (0, 0, 1)) if pt > 0.5 else None)
            point(p, -1)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    rw_r = wrist_of(body, REST, -1)

    def face(t):
        p = Pose()
        at_core = pulse(t, 1.2, 0.3, 1.6, 0.3) + pulse(t, 6.0, 0.3, 0.8, 0.3)
        p = p + look((-18 * at_core, 14 * at_core))
        w = pulse(t, 1.5, 0.2, 0.5, 0.4)
        brows(p, 1.4 * w, 1.6 * w, 1.0 * w)
        p.face["wide"] = 0.6 * w
        p.face["grin"] = -0.6 * w
        sm = pulse(t, 4.2, 0.2, 1.1, 0.3)
        brows(p, 0.0, 1.4 * sm, 1.0 * sm, side=1)
        p.face["smirk_L"] = 0.7 * sm
        return p

    c.layer(face)
    c.layer(blink_layer([0.9, 3.4, 5.6, 7.9]))
    c.solve(solve)
    return c


BEATS = {"floss": 48, "take-the-l": 32, "default-dance": 48, "orange-justice": 48, "robot": 32,
         "electro-shuffle": 30, "hype": 32, "boogie-down": 30, "get-griddy": 32, "billy-bounce": 32,
         "fresh": 32, "scenario": 32, "groove-jam": 32, "headbang": 32, "the-drop": 32}


def clips(body: Body):
    out = {
        "idle": idle(body),
        "watch": watch(body),
        "sit": sit(body),
        "sleep": sleep(body),
        "press": press(body),
        "shrug": shrug(body),
        "walk": walk(body),
        "moonwalk": walk(body, "moonwalk", back=True),
        "core-show": core_show(body),
    }
    out.update(dances(body))
    out["calibrate"] = calibrate(body)
    return out


def calibrate(body):
    """Not for the page: one test pose a second, to check the skeleton's axes by eye."""
    c = Clip("calibrate", 8.0)
    tests = [REST.copy(), REST.copy().both("forearm", x=16, y=60, z=0), REST.copy().both("forearm", x=16, y=-60, z=0),
             REST.copy().both("lid_up", x=-46).both("lid_lo", x=40)]
    p = REST.copy() + look((12, 25))
    brows(p, 1.5, 1.5, 1.0)
    tests += [p, REST.copy()]
    p = REST.copy()
    p.fingers(1, 85, thumb=60)
    p.fingers(-1, 85, thumb=60)
    tests += [p, REST.copy()]
    for i, q in enumerate(tests):
        c.key(float(i), q, "step")
        c.key(i + 0.999, q, "step")

    def solve(t, p, skel):
        if 5 <= t < 6:
            body.move_world(p, "hips", 0, 0, -0.06)
            body.plant(p, 1, pos=(0, -0.2, 0), roll=-20)
            body.plant(p, -1, pos=(0, 0.15, 0), roll=25)
        else:
            if 7 <= t < 8:
                body.hand_to(p, 1, V(0.22, -0.4, 1.35))
            body.plant(p, 1)
            body.plant(p, -1)
        return p

    c.solve(solve)
    return c
