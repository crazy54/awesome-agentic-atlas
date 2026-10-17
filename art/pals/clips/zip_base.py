"""Zip's everyday clips: what the stage plays when he walks on, stands about, reacts, and the reusable pieces
his bits are built from. Small, quick and up to something: he never stands quite still, his eyes get
somewhere before his head does, his horns and ears catch every jolt a beat late, and when he moves he moves
all at once.

    idle (4 s loop)  walk (one 0.6 s stride in place)  run (0.4 s)  sneak (1.2 s, on tiptoe)
    point  laugh  shrug  wave  cheer  fold-arms  hands-on-hips  jump  peek  push (loop)  pull (loop)
    carry (loop)  sit  fall-over  dance (8 s, his own: the gremlin)

Every clip but the loops starts and ends on `REST`, so the page can drop any of them between two idles
without a jump; the loops start on REST's stance at their own phase. A loop is baked with its closing frame
(the first again) and an even number of frames, so that the file's clip, sampled every other frame, lasts
exactly one period and its feet keep pace with the page (`looped()`).

THE STRIDES. `walk`, `run`, `sneak`, `push`, `pull` and `carry` are strides in place: each foot slides back
at the clip's ground speed while it is down, and the page moves him at that speed, so on the page his feet
stay put. Ground speed = stride / (stance * period):

    walk   0.46 / (0.58 * 0.60) = 1.32 m/s   (WALK_SPEED; the stage's CAST table uses it)
    run    0.60 / (0.40 * 0.40) = 3.75 m/s   (RUN_SPEED)
    sneak  0.32 / (0.62 * 1.20) = 0.43 m/s   (SNEAK_SPEED)
    push   0.26 / (0.70 * 1.00) = 0.37 m/s   (PUSH_SPEED: leaning into something in front of him)
    pull   0.24 / (0.70 * 1.00) = 0.34 m/s   (PULL_SPEED: leaning back, hauling; he travels BACKWARDS, so the
                                              page moves him away from the way he faces itself rather than
                                              with walkTo, which turns him to face where he goes)
    carry  0.40 / (0.60 * 0.80) = 0.83 m/s   (CARRY_SPEED: something held in both hands in front of him,
                                              between grip_L and grip_R, CARRY_WRISTS apart at chest height)

On the page, a stride other than the walk is `walkTo(x, {clip: "run", speed: RUN_SPEED / WALK_SPEED})`.

AXES (kit/rig.py, and zip.py's docstring). Arms: +X swings forward, +Z raises sideways (his arms are built
in the sheet's A-pose, 48 degrees below level: -42 hangs one straight down, +48 holds it level). Trunk and
head: +X bends forward, +Y turns to his left, +Z leans to his right. Lids: the upper closes at x -80, the
lower at x +66. Eyes: +X looks up, +Z looks to his left. Horns (`horn_1` then `horn_2`, two-bone chains):
+X tips them forward, +Z out to his right. Ears: their bones run out along the ear cups' axes, so a turn
about Y spins a cup like a dial and X/Z tilt it. Poses are written for the left and mirrored with
`both`/`side`.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from common import Body, blink_layer, breathe, brows, look, stride_foot  # noqa: F401  (Body: for bits)
from kit.anim import Clip, Pose, blend, ease, pulse, smooth

TAU = math.tau
FACE = {"grin": 1.0}                    # zip.py REST_FACE: the sheet's grin
HORNS = ("horn_1_L", "horn_2_L", "horn_1_R", "horn_2_R")
BODY = dict(heel_back=0.23, toe_front=0.32)     # his sneakers: heel and toe, metres behind / ahead of the ankle line
LID_UP, LID_LO = -80.0, 66.0            # a blink: zip.py builds his lids open by these

WALK_PERIOD, WALK_STANCE, WALK_STRIDE = 0.6, 0.58, 0.46
WALK_SPEED = WALK_STRIDE / (WALK_STANCE * WALK_PERIOD)
RUN_PERIOD, RUN_STANCE, RUN_STRIDE = 0.40, 0.40, 0.60
RUN_SPEED = RUN_STRIDE / (RUN_STANCE * RUN_PERIOD)
SNEAK_PERIOD, SNEAK_STANCE, SNEAK_STRIDE = 1.2, 0.62, 0.32
SNEAK_SPEED = SNEAK_STRIDE / (SNEAK_STANCE * SNEAK_PERIOD)
PUSH_PERIOD, PUSH_STANCE, PUSH_STRIDE = 1.0, 0.70, 0.26
PUSH_SPEED = PUSH_STRIDE / (PUSH_STANCE * PUSH_PERIOD)
PULL_PERIOD, PULL_STANCE, PULL_STRIDE = 1.0, 0.70, 0.24
PULL_SPEED = PULL_STRIDE / (PULL_STANCE * PULL_PERIOD)
CARRY_PERIOD, CARRY_STANCE, CARRY_STRIDE = 0.8, 0.60, 0.40
CARRY_SPEED = CARRY_STRIDE / (CARRY_STANCE * CARRY_PERIOD)
CARRY_WRISTS = (0.36, -0.4, 0.98)       # carry: the wrists' spacing across, then where (Y, Z) they hold
PUSH_HANDS = (-0.62, 1.0)               # push: the palms' plane (Y) and height (Z): what he pushes is there
                                        # (his face is about at it too: the head is the biggest thing he has)
DANCE_SECS, DANCE_BEATS = 8.0, 20       # dance: 150 beats a minute


def V(*a):
    return Vector(a)


def rest_pose():
    """His everyday stance: weight forward, chin down a touch and cocked, the arms hanging a little out from
    the body (they are chunky, and so is he) with soft elbows, hands half curled, the sheet's grin."""
    p = Pose(face=dict(FACE))
    p.both("shoulder", z=-2)
    p.both("upper_arm", x=8, y=0, z=-20)
    p.both("forearm", x=20, y=0, z=0)
    p.both("hand", x=6, y=0, z=0)
    p.fingers(1, 22, spread=6, thumb=14)
    p.fingers(-1, 22, spread=6, thumb=14)
    p.set("chest", 3, 0, 0)
    p.set("head", 2, 0, -4)
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


def rest_wrists(body):
    """Where his wrists hang at REST with his feet planted: the place a hand reaches from and goes back to."""
    q = REST.copy()
    body.plant(q, 1)
    body.plant(q, -1)
    return {1: wrist_of(body, q, 1), -1: wrist_of(body, q, -1)}


def stand(body, feet=None):
    """A post-solver that keeps both feet planted; `feet(t)` may return {side: plant kwargs}."""
    def f(t, p, skel):
        spec = feet(t) if feet else {}
        for sg in (1, -1):
            body.plant(p, sg, **spec.get(sg, {}))
        return p
    return f


def ring(t, at, freq=18.0, decay=7.0):
    """A damped wobble set off at `at`: what a spring does after a jolt (0 before it)."""
    if t < at:
        return 0.0
    u = t - at
    return math.exp(-u * decay) * math.sin(u * freq)


def horns(p, x=0.0, z=0.0, tip=1.4):
    """Tip both horns forward (x) and out (z, each to its own side), the tips more than the roots."""
    for s, sg in (("_L", 1), ("_R", -1)):
        p.add(f"horn_1{s}", x, 0, -z * sg)
        p.add(f"horn_2{s}", x * tip, 0, -z * sg * tip)
    return p


def horn_sway(t, period, amount=4.0, cycles=(1, 3), phase=0.0):
    """A loose, looping drift of the horns (whole cycles in `period`, so a loop stays seamless)."""
    p = Pose()
    u = t / period
    for k, (s, sg) in enumerate((("_L", 1), ("_R", -1))):
        a = amount * (0.6 * math.sin(TAU * (cycles[0] * u + phase + 0.17 * k)) +
                      0.4 * math.sin(TAU * (cycles[1] * u + 0.4 + 0.31 * k)))
        b = amount * 0.7 * math.sin(TAU * (cycles[0] * u + 0.25 + phase))
        p.add(f"horn_1{s}", a * 0.5, 0, b * 0.5 * sg)
        p.add(f"horn_2{s}", a, 0, b * sg)
    return p


def ears(p, spin=0.0, tilt=0.0, side=0):
    """Spin the ear cups like dials (degrees) and tilt them back (positive)."""
    for s, sg in (("_L", 1), ("_R", -1)):
        if side and side != sg:
            continue
        p.add(f"ear{s}", tilt, spin * sg, 0)
    return p


def looped(name, T):
    """A loop's clip: T seconds of whole, even frames, baked with its closing frame (kit.anim.bake leaves the
    closing frame off a `loop` clip, and the exporter keeps every other frame, which together would cut a
    0.6 s stride to 0.53 s and make the feet skate). The page loops it."""
    n = int(round(T * 30))
    assert n % 2 == 0 and abs(n / 30 - T) < 1e-6, f"{name}: a loop needs an even number of frames"
    return Clip(name, T, loop=False, frames=n)


def blinks(times):
    return blink_layer(times, up=LID_UP, lo=LID_LO)


def squint(p, k):
    """Lids half down, happily (a laugh, a grin with the eyes)."""
    p.both("lid_up", x=0.55 * LID_UP * k, add=True)
    p.both("lid_lo", x=0.4 * LID_LO * k, add=True)
    return p


def wink(p, side, k):
    s = "_L" if side > 0 else "_R"
    p.add(f"lid_up{s}", LID_UP * k, 0, 0)
    p.add(f"lid_lo{s}", LID_LO * k, 0, 0)
    return p


def stride(body, p, t, T, length, stance, height=0.12, toe_off=28.0, heel_strike=-14.0, back=False,
           phases=(0.0, 0.5), **plant):
    """Both feet of a stride in place (see the module's docstring); `back` walks backwards."""
    for sg, ph in zip((1, -1), phases):
        y, lift, roll = stride_foot(t, T, length, stance, ph, height=height, toe_off=toe_off,
                                    heel_strike=heel_strike)
        if back:
            y, roll = -y, -roll * 0.6
        body.plant(p, sg, pos=(0, y, 0), lift=lift, roll=roll, **plant)


# ------------------------------------------------------------------------------------------- idle
def idle(body):
    """Four seconds, looping, and never still: a bounce on his toes, a weight shift, eyes that dart off to
    his left and the head snapping after them, the horns ringing on, a sly sidelong look at the reader with
    one brow up, fingers drumming, an ear cup tuned like a dial, a toe tapping, a double blink."""
    T = 4.0
    c = looped("idle", T)
    c.key(0.0, REST)

    def layer(t):
        u = t / T
        p = Pose()
        sway = math.sin(TAU * u)
        hips(body, p, dx=0.018 * sway, dz=-0.012 + 0.006 * math.sin(TAU * 4 * u + 1.2), roll=-2.2 * sway,
             yaw=2.0 * math.sin(TAU * 2 * u))
        p.add("spine", 0, 0, 1.6 * sway)
        p.add("chest", 0, -1.2 * math.sin(TAU * u - 0.6), 0.8 * sway)
        p.both("upper_arm", z=1.6 * sway, add=True)
        # the glance: the eyes go first, the head snaps after them, holds, snaps back; the horns ring on
        g = pulse(u, 0.28, 0.02, 0.1, 0.03)
        gh = pulse(u, 0.295, 0.03, 0.085, 0.035)
        r = 1.0 * ring(t, 0.295 * T + 0.1) - 0.8 * ring(t, 0.41 * T + 0.1)
        # the sly look at the reader: a sidelong slide of the eyes, one brow up, the smirk
        sl = pulse(u, 0.62, 0.06, 0.18, 0.06)
        p = p + look((3 * g - 4 * sl, 30 * g - 14 * sl), head=(0, -4 * gh, 16 * gh - 6 * sl))
        horns(p, x=7 * r, z=-5 * r)
        brows(p, 0.3 * sl, 1.5 * sl, 1.1 * sl, side=1)
        brows(p, -0.6 * sl, -0.3 * sl, 0.0, side=-1)
        p.face["smirk_L"] = 0.6 * sl
        p.face["grin"] = 1.0 - 0.5 * sl
        # an ear tuned like a dial while he thinks of something
        e = pulse(u, 0.48, 0.05, 0.08, 0.06)
        ears(p, spin=40 * e, tilt=6 * e, side=1)
        # fingers drumming on nothing (left hand)
        d = pulse(u, 0.06, 0.03, 0.14, 0.03)
        for k, f in enumerate(("index", "middle", "ring")):
            a = 22 + 30 * d * max(0.0, math.sin(TAU * (t * 6 - k * 0.22)))
            p.set(f"{f}_1_L", a, 0, 0)
            p.set(f"{f}_2_L", a * 1.1, 0, 0)
        p = p + breathe(T / 2, 0.8)(t)
        p = p + horn_sway(t, T, 2.5)
        return p

    c.layer(layer)
    c.layer(blinks([0.16 * T, 0.75 * T, 0.8 * T]))

    def feet(t):
        u = t / T
        tap = max(0.0, math.sin(TAU * 10 * u)) ** 2 * smooth(0.82, 0.84, u) * (1 - smooth(0.95, 0.97, u))
        lean = math.sin(TAU * u)
        return {1: dict(roll=-12 * tap + 6 * max(0.0, lean) ** 2),
                -1: dict(roll=6 * max(0.0, -lean) ** 2)}

    c.solve(stand(body, feet))
    return c


# -------------------------------------------------------------------------------------------- walk
def walk(body):
    """One stride in place (two quick steps): bouncy, up on the balls of his feet, the arms pumping and the
    elbows out, the head bobbing a beat behind with the horns flapping after it, a cheeky lean."""
    T = WALK_PERIOD
    c = looped("walk", T)
    base = REST.copy()
    base.set("chest", 6, 0, 0)
    base.set("head", 0, 0, -6)
    c.key(0.0, base)

    def layer(t):
        u = t / T
        p = Pose()
        bob = math.cos(TAU * 2 * (u - 0.1))
        hips(body, p, dz=-0.025 + 0.028 * bob, dx=0.022 * math.sin(TAU * u), yaw=-8 * math.sin(TAU * u),
             roll=3 * math.sin(TAU * u), pitch=4)
        p.add("chest", 0, 10 * math.sin(TAU * u), -2 * math.sin(TAU * u))
        p.add("head", 3 * math.cos(TAU * 2 * (u - 0.22)), -4 * math.sin(TAU * u), 0)
        swing = math.sin(TAU * u)
        p.side("upper_arm", 1, x=-34 * swing, z=6, add=True)
        p.side("upper_arm", -1, x=34 * swing, z=6, add=True)
        p.side("forearm", 1, x=24 + 22 * max(0.0, -swing), add=True)
        p.side("forearm", -1, x=24 + 22 * max(0.0, swing), add=True)
        horns(p, x=-4 + 6 * math.cos(TAU * 2 * (u - 0.32)), z=2 * math.sin(TAU * u))
        ears(p, tilt=3 * math.cos(TAU * 2 * (u - 0.3)))
        return p

    c.layer(layer)
    c.solve(lambda t, p, skel: stride(body, p, t, T, WALK_STRIDE, WALK_STANCE, height=0.12, yaw=3) or p)
    return c


def run(body):
    """A sprint in place: pitched forward, fists pumping, the knees high, the horns swept back."""
    T = RUN_PERIOD
    c = looped("run", T)
    base = REST.copy()
    base.set("chest", 10, 0, 0)
    base.set("head", -8, 0, 0)
    fist(base, 1, 0.8)
    fist(base, -1, 0.8)
    base.face = {"grin": 0.6, "ee": 0.5}
    c.key(0.0, base)

    def layer(t):
        u = t / T
        p = Pose()
        bob = math.cos(TAU * 2 * (u - 0.3))           # highest in the flight between the steps
        hips(body, p, dz=-0.03 + 0.04 * bob, yaw=-10 * math.sin(TAU * u), pitch=12)
        p.add("chest", 0, 14 * math.sin(TAU * u), 0)
        swing = math.sin(TAU * u)
        p.side("upper_arm", 1, x=-50 * swing + 6, z=10, add=True)
        p.side("upper_arm", -1, x=50 * swing + 6, z=10, add=True)
        p.side("forearm", 1, x=60 + 20 * max(0.0, -swing), add=True)
        p.side("forearm", -1, x=60 + 20 * max(0.0, swing), add=True)
        horns(p, x=-16 + 5 * math.cos(TAU * 2 * u), z=-3)
        ears(p, tilt=-8)
        return p

    c.layer(layer)
    c.solve(lambda t, p, skel: stride(body, p, t, T, RUN_STRIDE, RUN_STANCE, height=0.2, toe_off=36,
                                      heel_strike=-6) or p)
    return c


def sneak(body):
    """On tiptoe, crouched and leaning in, each knee lifted high and set down with care, the hands up at his
    chest with the wrists dropped like a cartoon burglar's, eyes darting, the grin of someone up to something."""
    T = SNEAK_PERIOD
    c = looped("sneak", T)
    base = REST.copy()
    base.set("chest", 12, 0, 0)
    base.set("head", -6, 0, 0)
    base.face = {"grin": 0.4, "smirk_L": 0.8}
    for sg in (1, -1):
        base.fingers(sg, 30, spread=8, thumb=10)
    c.key(0.0, base)

    def layer(t):
        u = t / T
        p = Pose()
        dart = math.sin(TAU * u) ** 3
        p = p + look((-6, 26 * dart), head=(0, 0, 8 * math.sin(TAU * u)))
        brows(p, 0.4, 1.0, 0.6)
        horns(p, x=6 + 3 * math.sin(TAU * 2 * u), z=1.5 * math.sin(TAU * u))
        return p

    c.layer(layer)

    def solve(t, p, skel):
        u = t / T
        hips(body, p, dz=-0.1 + 0.025 * math.cos(TAU * 2 * (u - 0.2)), dy=-0.03, pitch=12,
             roll=4 * math.sin(TAU * u), yaw=-5 * math.sin(TAU * u))
        p.add("spine", 6, 0, 0)
        # paws up in front of his chest
        for sg in (1, -1):
            tgt = V(sg * 0.16, -0.34, 0.98 + 0.015 * math.sin(TAU * (2 * u + (0.25 if sg > 0 else 0.75))))
            body.hand_to(p, sg, tgt, elbow=(0.6, 0.2, -0.3),
                         hand_rot=hand_world((-sg * 0.25, -0.35, -1), (0, 1, 0)))
        # on tiptoe the whole time: the stance foot stays up on its ball
        for sg, ph in ((1, 0.0), (-1, 0.5)):
            y, lift, roll = stride_foot(t, T, SNEAK_STRIDE, SNEAK_STANCE, ph, height=0.16)
            body.plant(p, sg, pos=(0, y, 0), lift=lift, roll=max(22.0, roll + 22.0) if lift < 0.01 else 10 + roll * 0.4)
        return p

    c.solve(solve)
    return c


# ----------------------------------------------------------------------------------- the pieces
def point_clip(body):
    """Thrusts an arm out to point, to his left and a little up (screen right when he faces the reader),
    head and eyes after it, an eager bounce on his toes: look, there!"""
    T = 2.4
    c = Clip("point", T, frames=72)
    c.key(0.0, REST)
    RW = rest_wrists(body)
    tgt = V(0.62, -0.32, 1.32)

    def solve(t, p, skel):
        w = pulse(t, 0.08, 0.22, 1.55, 0.4)
        jab = pulse(t, 0.3, 0.05, 0.05, 0.25)
        bob = math.sin(TAU * 3 * t) * pulse(t, 0.4, 0.1, 1.2, 0.3)
        hips(body, p, dx=0.03 * w, dz=-0.01 * w + 0.012 * bob, roll=-4 * w, yaw=8 * w)
        p.add("chest", -4 * w, 10 * w, -4 * w)
        d = (tgt - V(0.18, -0.02, 1.12)).normalized()
        body.hand_to(p, 1, RW[1].lerp(tgt + d * 0.04 * jab, w), elbow=(0.3, 0.3, -0.6),
                     hand_rot=hand_world(d, (0, 0.3, -1)) if w > 0.4 else None)
        if w > 0.3:
            point(p, 1)
        body.plant(p, 1, roll=8 * w * max(0.0, bob))
        body.plant(p, -1, roll=8 * w * max(0.0, bob))
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.0, 0.2, 1.6, 0.4)
        p = p + look((6 * w, 24 * w), head=(-4 * w, 0, 16 * w))
        brows(p, 1.4 * w, 1.6 * w, 1.0 * w)
        p.face.update({"grin": 1.0 - 0.6 * w, "wide": 0.6 * w})
        horns(p, x=-6 * ring(t, 0.32), z=4 * ring(t, 0.32))
        return p

    c.layer(layer)
    c.layer(blinks([1.9]))
    return c


def laugh(body):
    """A cackle: a gasp back, then doubled over with both hands on his belly, shoulders shaking, eyes
    squeezed shut, horns rattling; one slap of the thigh, and a wipe of an eye."""
    T = 2.8
    c = Clip("laugh", T, frames=84)
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def solve(t, p, skel):
        back = pulse(t, 0.0, 0.18, 0.12, 0.25)
        over = pulse(t, 0.35, 0.3, 1.5, 0.5)
        shake = math.sin(TAU * 7.5 * t) * pulse(t, 0.25, 0.1, 1.9, 0.3)
        slap = pulse(t, 1.55, 0.12, 0.08, 0.25)
        hips(body, p, dz=-0.04 * over - 0.02 * back, dy=0.03 * over, pitch=-6 * back + 8 * over)
        p.add("spine", 5 * over, 0, 0)
        p.add("chest", -14 * back + 6 * over + 3 * shake, 0, 2 * shake)
        p.add("head", -20 * back - 8 * over - 6 * abs(shake), 0, 0)
        belly = V(0.0, -0.25, 0.95)
        for sg in (1, -1):
            hold = over if sg > 0 else over * (1 - slap)
            tgt = belly + V(sg * 0.12, 0, -0.04 * sg)
            if sg < 0 and slap > 0:
                tgt = tgt.lerp(V(-0.26, -0.18, 0.66), slap)
            k = max(hold, slap if sg < 0 else 0.0)
            body.hand_to(p, sg, RW[sg].lerp(tgt + V(0, 0, 0.01 * shake), k), elbow=(0.6, 0.2, -0.3),
                         hand_rot=hand_world((-sg, -0.3, -0.2), (0, 1, 0)) if k > 0.5 else None)
            open_hand(p, sg, 6 * k)
        # the wipe of an eye at the end, the left hand
        wipe = pulse(t, 2.05, 0.2, 0.25, 0.25)
        if wipe > 0:
            cur = wrist_of(body, p, 1)
            body.hand_to(p, 1, cur.lerp(V(0.24, -0.34, 1.42), wipe), elbow=(0.6, 0.1, -0.4),
                         hand_rot=hand_world((-0.4, -0.3, 1), (0, 1, 0)) if wipe > 0.5 else None)
        body.plant(p, 1, roll=6 * max(0.0, shake))
        body.plant(p, -1, roll=6 * max(0.0, -shake))
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        on = pulse(t, 0.1, 0.12, 2.1, 0.4)
        ha = 0.5 + 0.5 * math.sin(TAU * 7.5 * t)
        p.face.update({"grin": 1.0 - on, "wide": on * (0.5 + 0.5 * ha), "ee": on * 0.5 * (1 - ha)})
        squint(p, on * 0.9)
        brows(p, 1.6 * on, 0.8 * on, -0.2 * on)
        horns(p, x=5 * math.sin(TAU * 7.5 * t + 1) * on, z=3 * math.sin(TAU * 7.5 * t) * on)
        ears(p, tilt=6 * on * ha)
        return p

    c.layer(layer)
    return c


def shrug(body):
    """Shoulders up to his ears fast, palms up, a tilt of the head and an eye-roll: who, me?"""
    T = 2.0
    c = Clip("shrug", T, frames=60)
    up = REST.copy()
    up.both("shoulder", z=18)
    up.set("head", -4, 0, 14)
    up.set("chest", -4, 0, 0)
    for sg in (1, -1):
        open_hand(up, sg, 10)
    up.face = {"flat": 0.5, "smirk_R": 0.7}
    c.key(0.0, REST)
    c.key(0.25, up, "snap")
    c.key(1.25, up, "linear")
    c.key(1.8, REST, "inout")
    c.key(2.0, REST, "linear")
    RW = rest_wrists(body)

    def layer(t):
        p = Pose()
        u = pulse(t, 0.1, 0.18, 1.0, 0.4)
        brows(p, 1.8 * u, 2.0 * u, 1.0 * u)
        roll = pulse(t, 0.45, 0.2, 0.3, 0.25)
        p = p + look((24 * roll, -10 * roll))
        horns(p, x=-5 * ring(t, 0.25), z=4 * ring(t, 0.25))
        return p

    c.layer(layer)

    def solve(t, p, skel):
        w = pulse(t, 0.0, 0.25, 1.05, 0.55)
        for sg in (1, -1):
            tgt = V(sg * 0.46, -0.3, 0.92)
            body.hand_to(p, sg, RW[sg].lerp(tgt, w), elbow=(0.2, 0.25, -1.0),
                         hand_rot=hand_world((sg * 0.55, -0.82, 0.08), (0, 0, 1)) if w > 0.4 else None)
        body.plant(p, 1)
        body.plant(p, -1)
        return p

    c.solve(solve)
    return c


def wave(body):
    """A wave too big for him: up on his toes, the left arm high and the hand going like a windscreen
    wiper, the whole body bouncing with it, the grin as wide as it goes."""
    T = 2.2
    c = Clip("wave", T, frames=66)
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def solve(t, p, skel):
        w = pulse(t, 0.05, 0.25, 1.45, 0.45)
        wag = math.sin(TAU * 3.2 * (t - 0.3)) * smooth(0.25, 0.4, t)
        hips(body, p, dz=0.02 * w + 0.012 * abs(wag) * w, dx=-0.02 * w, roll=4 * w)
        p.add("chest", -4 * w, 4 * w, 4 * w)
        tgt = V(0.44 + 0.07 * wag * w, -0.16, 1.5)
        body.hand_to(p, 1, RW[1].lerp(tgt, w), elbow=(0.6, 0.1, -0.5),
                     hand_rot=hand_world((0.25 * wag, -0.2, 1), (0, -1, 0)) if w > 0.5 else None)
        open_hand(p, 1, 14 * w)
        p.add("hand_L", 0, 0, -20 * wag * w)
        body.plant(p, 1, roll=14 * w)
        body.plant(p, -1, roll=14 * w)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.0, 0.25, 1.5, 0.4)
        p.face.update({"grin": 1.0 - 0.3 * w, "wide": 0.6 * w, "smile": 0.3 * w})
        brows(p, 1.6 * w, 1.8 * w, 1.2 * w)
        p = p + look((4 * w, 6 * w), head=(-4 * w, 6 * w, 6 * w))
        horns(p, x=3 * math.sin(TAU * 3.2 * t) * w, z=4 * math.sin(TAU * 3.2 * t + 0.6) * w)
        squint(p, 0.3 * w)
        return p

    c.layer(layer)
    c.layer(blinks([1.85]))
    return c


def cheer(body):
    """Fists up, a hop, and down with a stomp: yes!"""
    T = 2.2
    c = Clip("cheer", T, frames=66)
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def solve(t, p, skel):
        w = pulse(t, 0.05, 0.22, 1.35, 0.5)
        crouch = pulse(t, 0.25, 0.15, 0.0, 0.1)
        air = pulse(t, 0.42, 0.12, 0.12, 0.16)
        land = pulse(t, 0.8, 0.06, 0.05, 0.25)
        pump = math.sin(TAU * 2.6 * (t - 0.9)) * pulse(t, 0.9, 0.1, 0.6, 0.3)
        hips(body, p, dz=-0.08 * crouch + 0.24 * air - 0.07 * land, pitch=8 * crouch - 6 * air)
        p.add("chest", -10 * w - 6 * air, 0, 0)
        p.add("head", -10 * w, 0, 0)
        for sg in (1, -1):
            tgt = V(sg * 0.4, -0.12, 1.52 + 0.06 * pump * sg)
            body.hand_to(p, sg, RW[sg].lerp(tgt, w), elbow=(0.7, 0.1, -0.3),
                         hand_rot=hand_world((0, -0.2, 1), (-sg, 0, 0)) if w > 0.5 else None)
            fist(p, sg, w)
        lift = 0.24 * air
        body.plant(p, 1, lift=lift, roll=20 * air)
        body.plant(p, -1, lift=lift, roll=20 * air)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.0, 0.2, 1.4, 0.45)
        p.face.update({"grin": 1.0 - w, "wide": w})
        squint(p, 0.7 * w)
        brows(p, 1.4 * w, 1.6 * w, 1.0 * w)
        horns(p, x=-10 * ring(t, 0.45, 16, 5) + 8 * ring(t, 0.82, 20, 6), z=4 * ring(t, 0.82))
        ears(p, tilt=-6 * pulse(t, 0.4, 0.1, 0.3, 0.3))
        return p

    c.layer(layer)
    return c


def fold_arms(body):
    """Arms folded high on his chest, chin up, eyes half shut, the foot going: unimpressed."""
    T = 3.0
    c = Clip("fold-arms", T, frames=90)
    c.key(0.0, REST)
    held = REST.copy()
    held.set("head", -8, 0, 6)
    held.set("chest", -5, 0, 0)
    held.face = {"flat": 0.6, "smirk_R": 0.6}
    c.key(0.35, held, "back")
    c.key(T - 0.45, held, "linear")
    c.key(T, REST, "inout")
    RW = rest_wrists(body)
    # the left forearm on top, its hand tucked by the right elbow; the right hand under the left elbow
    wr = {1: V(-0.13, -0.27, 1.07), -1: V(0.14, -0.24, 1.02)}
    hr = {1: hand_world((-1, 0.1, 0.1), (0, -0.2, -1)), -1: hand_world((1, 0.1, -0.1), (0, -0.3, 1))}

    def solve(t, p, skel):
        w = pulse(t, 0.0, 0.35, T - 0.8, 0.45)
        for sg in (1, -1):
            body.hand_to(p, sg, RW[sg].lerp(wr[sg], w), elbow=(0.55, 0.15, -0.35), hand_rot=hr[sg] if w > 0.5 else None)
            fist(p, sg, 0.6 * w)
        tap = max(0.0, math.sin(TAU * 3 * t)) ** 2 * pulse(t, 0.8, 0.1, 1.3, 0.1)
        body.plant(p, 1)
        body.plant(p, -1, roll=-14 * tap)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.1, 0.25, T - 0.8, 0.4)
        p.both("lid_up", x=0.35 * LID_UP * w)
        brows(p, -0.6 * w, -0.2 * w, 0.4 * w)
        brows(p, 0.6 * w, 1.4 * w, 1.0 * w, side=-1)
        p = p + look((-4 * w, -8 * w))
        horns(p, x=-4 * ring(t, 0.35), z=2 * ring(t, 0.35))
        return p

    c.layer(layer)
    return c


def hands_on_hips(body):
    """Fists on his hips, elbows out, leaning back with the chin up: the boss of the place."""
    T = 3.0
    c = Clip("hands-on-hips", T, frames=90)
    c.key(0.0, REST)
    held = REST.copy()
    held.set("head", -8, 0, -6)
    held.set("chest", -8, 0, 0)
    held.face = {"grin": 0.8, "smirk_L": 0.6}
    c.key(0.35, held, "back")
    c.key(T - 0.45, held, "linear")
    c.key(T, REST, "inout")
    RW = rest_wrists(body)

    def solve(t, p, skel):
        w = pulse(t, 0.0, 0.35, T - 0.8, 0.45)
        hips(body, p, dy=0.02 * w, pitch=-4 * w)
        for sg in (1, -1):
            tgt = V(sg * 0.25, -0.04, 0.86)
            body.hand_to(p, sg, RW[sg].lerp(tgt, w), elbow=(0.7, 0.25, 0.0),
                         hand_rot=hand_world((-sg * 0.35, 0.25, -1), (-sg, 0, 0)) if w > 0.5 else None)
            fist(p, sg, 0.8 * w)
        body.plant(p, 1, yaw=6 * w)
        body.plant(p, -1, yaw=6 * w)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.1, 0.25, T - 0.8, 0.4)
        brows(p, 0.4 * w, 1.0 * w, 0.8 * w)
        p = p + look((-6 * w, 0))
        horns(p, x=-5 * ring(t, 0.35), z=-3 * ring(t, 0.35))
        return p

    c.layer(layer)
    c.layer(blinks([1.6]))
    return c


def jump(body):
    """A jump on the spot: a deep, quick crouch, up with the arms flung, knees tucked in the air, and down
    into a squash that bounces back."""
    T = 1.5
    c = Clip("jump", T, frames=45)
    c.key(0.0, REST)
    RW = rest_wrists(body)
    T0, T1 = 0.42, 0.95                       # take-off, landing

    def solve(t, p, skel):
        crouch = pulse(t, 0.05, 0.3, 0.02, 0.06)
        if T0 <= t <= T1:
            u = (t - T0) / (T1 - T0)
            h = 0.38 * 4 * u * (1 - u)
        else:
            h = 0.0
        tuck = pulse(t, T0 + 0.05, 0.12, 0.2, 0.15)
        land = pulse(t, T1, 0.05, 0.05, 0.3)
        hips(body, p, dz=-0.12 * crouch + h - 0.08 * land, pitch=14 * crouch - 4 * tuck + 10 * land)
        p.add("chest", 8 * crouch - 8 * tuck + 6 * land, 0, 0)
        p.add("head", -6 * crouch - 6 * tuck, 0, 0)
        arms = pulse(t, T0 - 0.08, 0.12, 0.3, 0.3)
        for sg in (1, -1):
            if crouch > 0.01:
                p.side("upper_arm", sg, x=-30 * crouch, add=True)
            if arms > 0.01:
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.44, -0.14, 1.5), arms), elbow=(0.6, 0.1, -0.4))
            open_hand(p, sg, 12 * arms)
        lift = h + 0.12 * tuck
        body.plant(p, 1, lift=lift, roll=24 * tuck, pos=(0, 0.05 * tuck, 0))
        body.plant(p, -1, lift=lift, roll=24 * tuck, pos=(0, 0.05 * tuck, 0))
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        air = pulse(t, T0, 0.1, 0.35, 0.15)
        p.face.update({"grin": 1.0 - air, "wide": air})
        brows(p, 1.6 * air, 1.8 * air, 1.2 * air)
        horns(p, x=-10 * air + 10 * ring(t, T1, 18, 5), z=3 * ring(t, T1, 18, 5))
        ears(p, tilt=-6 * air)
        return p

    c.layer(layer)
    return c


def peek(body):
    """Leans out round a corner to his left, a hand on its edge, eyes wide and darting; spots something,
    and the grin spreads; ducks back."""
    T = 3.0
    c = Clip("peek", T, frames=90)
    c.key(0.0, REST)
    RW = rest_wrists(body)
    edge = V(0.3, -0.24, 1.18)

    def solve(t, p, skel):
        w = pulse(t, 0.1, 0.4, 1.9, 0.45)
        hips(body, p, dx=0.1 * w, dz=-0.04 * w, roll=-12 * w)
        p.add("spine", 0, 0, -8 * w)
        p.add("chest", 0, 4 * w, -10 * w)
        p.add("head", 0, 0, -14 * w)
        body.hand_to(p, 1, RW[1].lerp(edge, w), elbow=(0.6, 0.2, -0.3),
                     hand_rot=hand_world((0, -0.1, 1), (-1, 0, 0)) if w > 0.5 else None)
        open_hand(p, 1, 8 * w)
        body.plant(p, 1, pos=(0.06 * w, 0, 0), roll=10 * w)
        body.plant(p, -1, roll=16 * w)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        w = pulse(t, 0.3, 0.2, 1.7, 0.4)
        dart = math.sin(TAU * 1.6 * (t - 0.5)) * pulse(t, 0.5, 0.1, 0.8, 0.1)
        spot = pulse(t, 1.55, 0.08, 0.6, 0.3)
        p = p + look((-4 * w, 18 * dart * w + 12 * spot))
        p.face.update({"grin": 1.0 - 0.5 * w + 0.6 * spot, "oh": 0.5 * w * (1 - spot)})
        brows(p, 1.6 * w, 1.6 * w, 1.0 * w)
        brows(p, 0.0, 0.8 * spot, 0.8 * spot, side=1)
        horns(p, x=6 * ring(t, 0.5), z=-4 * ring(t, 0.5))
        return p

    c.layer(layer)
    c.layer(blinks([1.2, 2.7]))
    return c


def push(body):
    """Leaning his whole weight into something in front of him, palms flat on it (at PUSH_HANDS), digging
    in step by step, teeth gritted: a loop to walk with at PUSH_SPEED."""
    T = PUSH_PERIOD
    c = looped("push", T)
    base = REST.copy()
    base.face = {"grit": 1.0}
    for sg in (1, -1):
        open_hand(base, sg, 8)
    c.key(0.0, base)

    def solve(t, p, skel):
        u = t / T
        hips(body, p, dz=-0.07 + 0.015 * math.cos(TAU * 2 * u), dy=0.1, pitch=15, roll=3 * math.sin(TAU * u))
        p.add("spine", 4, 0, 0)
        p.add("chest", 0, 4 * math.sin(TAU * u), 0)
        p.add("head", -10, 14, 6)
        y, z = PUSH_HANDS
        for sg in (1, -1):
            body.hand_to(p, sg, V(sg * 0.16, y + 0.12, z), elbow=(0.6, 0.3, -0.5),
                         hand_rot=hand_world((-sg * 0.1, -0.1, 1), (0, 1, 0)))
        stride(body, p, t, T, PUSH_STRIDE, PUSH_STANCE, height=0.08, toe_off=34, heel_strike=0)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        brows(p, -1.2, -0.4, 0.6)
        squint(p, 0.6)
        horns(p, x=8 + 2 * math.sin(TAU * 2 * t / T))
        return p

    c.layer(layer)
    return c


def pull(body):
    """Hauling on something in front of him (a rope, a corner) with both fists, leaning back and stepping
    backwards: a loop for a page moving him BACKWARDS at PULL_SPEED."""
    T = PULL_PERIOD
    c = looped("pull", T)
    base = REST.copy()
    base.face = {"grit": 1.0}
    c.key(0.0, base)

    def solve(t, p, skel):
        u = t / T
        heave = 0.5 + 0.5 * math.cos(TAU * 2 * u)
        hips(body, p, dz=-0.1 + 0.02 * heave, dy=0.12 + 0.03 * heave, pitch=-14 - 6 * heave)
        p.add("chest", -8, 6 * math.sin(TAU * u), 0)
        p.add("head", 10, 0, 0)
        for sg in (1, -1):
            body.hand_to(p, sg, V(sg * 0.08, -0.36 + 0.04 * heave, 0.96 + 0.02 * sg), elbow=(0.5, 0.3, -0.6),
                         hand_rot=hand_world((0, -1, 0.2), (-sg, 0, 0)))
            fist(p, sg)
        stride(body, p, t, T, PULL_STRIDE, PULL_STANCE, height=0.07, toe_off=10, heel_strike=-20, back=True)
        return p

    c.solve(solve)

    def layer(t):
        p = Pose()
        brows(p, -1.4, -0.6, 0.6)
        squint(p, 0.8)
        horns(p, x=-8 - 3 * math.cos(TAU * 2 * t / T))
        return p

    c.layer(layer)
    return c


def carry(body):
    """Walking with something held in both hands in front of his chest (CARRY_WRISTS), elbows in, a little
    waddle under the weight, peering round it: a loop to walk with at CARRY_SPEED."""
    T = CARRY_PERIOD
    c = looped("carry", T)
    base = REST.copy()
    base.face = {"grin": 0.5, "smirk_L": 0.5}
    c.key(0.0, base)
    w_, y_, z_ = CARRY_WRISTS

    def solve(t, p, skel):
        u = t / T
        bob = math.cos(TAU * 2 * (u - 0.1))
        hips(body, p, dz=-0.04 + 0.02 * bob, dy=0.02, roll=5 * math.sin(TAU * u), yaw=-4 * math.sin(TAU * u),
             pitch=-3)
        p.add("chest", -6, 4 * math.sin(TAU * u), -3 * math.sin(TAU * u))
        p.add("head", -4, 0, 6 * math.sin(TAU * u))
        for sg in (1, -1):
            body.hand_to(p, sg, V(sg * w_ / 2, y_, z_ + 0.012 * bob), elbow=(0.4, 0.3, -0.6),
                         hand_rot=hand_world((-sg * 0.2, -0.4, 0.9), (-sg, 0, 0)))
            p.fingers(sg, 40, spread=4, thumb=20)
        stride(body, p, t, T, CARRY_STRIDE, CARRY_STANCE, height=0.09, yaw=6)
        return p

    c.solve(solve)
    c.layer(lambda t: horns(Pose(), x=4 * math.cos(TAU * 2 * (t / T - 0.3))))
    return c


SIT_HIPS = V(0, 0.12, 0.2)              # where the hips end up, seated on the floor (Z absolute)


def seated(p, body, k, lean=0.0):
    """Blend k of the way from standing to sitting on the floor, knees up."""
    d = V(0, SIT_HIPS.y, SIT_HIPS.z - body.hip_z) * k
    hips(body, p, d.x, d.y, d.z, pitch=-18 * k + lean)
    p.add("spine", 14 * k, 0, 0)
    p.add("chest", 8 * k, 0, 0)
    p.add("head", -4 * k, 0, 0)
    return p


def sit_feet(k):
    return {1: dict(pos=(0.02 * k, -0.3 * k, 0), yaw=14 * k), -1: dict(pos=(-0.02 * k, -0.3 * k, 0), yaw=14 * k)}


def sit(body):
    """Flops down on the floor (no slow lowering for him: he drops and bounces), knees up and hands round
    them, swings his feet, and springs back up."""
    T = 5.0
    c = Clip("sit", T, frames=150)
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def k_of(t):
        if t < 0.2:
            return -0.06 * smooth(0, 0.2, t)
        if t < 0.65:
            return -0.06 + 1.1 * ease("in", (t - 0.2) / 0.45)
        if t < 0.9:
            return 1.04 - 0.04 * smooth(0.65, 0.9, t)
        if t < 4.1:
            return 1.0
        if t < 4.6:
            return 1.0 - ease("out", (t - 4.1) / 0.5)
        return 0.0

    def solve(t, p, skel):
        k = k_of(t)
        seated(p, body, max(0.0, k))
        if k < 0:
            hips(body, p, dz=0.4 * k)
        swing = math.sin(TAU * 1.4 * (t - 1.2)) * pulse(t, 1.2, 0.3, 2.3, 0.3)
        p.add("head", 0, 12 * math.sin(TAU * (t - 1.0) / 2.6) * pulse(t, 1.0, 0.3, 2.6, 0.3), 0)
        f = sit_feet(max(0.0, k))
        for sg in (1, -1):
            body.plant(p, sg, pos=f[sg]["pos"], yaw=f[sg]["yaw"], lift=max(0.0, 0.05 * swing * sg) * k,
                       roll=-12 * max(0.0, swing * sg) * k)
        hk = smooth(0.7, 1.1, t) * (1 - smooth(3.9, 4.15, t))
        if hk > 0:
            for sg in (1, -1):
                knee = body.where(p, f"shin{'_L' if sg > 0 else '_R'}")
                tgt = knee + V(-sg * 0.06, -0.08, -0.04)
                body.hand_to(p, sg, RW[sg].lerp(tgt, hk), elbow=(0.6, 0.2, -0.4),
                             hand_rot=hand_world((-sg, -0.2, -0.4), (0, 1, 0)) if hk > 0.6 else None)
                p.fingers(sg, 50 * hk, thumb=30)
        return p

    def face_(t):
        p = Pose()
        bump = pulse(t, 0.62, 0.05, 0.1, 0.25)
        p.face.update({"grin": 1.0 - bump, "oh": bump})
        hum = pulse(t, 1.4, 0.3, 2.2, 0.3)
        p.face["smile"] = 0.5 * hum
        squint(p, 0.4 * hum)
        horns(p, x=10 * ring(t, 0.65, 16, 5), z=5 * ring(t, 0.65, 14, 5))
        ears(p, spin=30 * math.sin(TAU * 0.5 * (t - 1.4)) * hum)
        return p

    c.layer(face_)
    c.layer(blinks([1.0, 3.3, 3.45]))
    c.solve(solve)
    return c


def fall_over(body):
    """A pratfall: a foot shoots out, the arms windmill, he lands on his bottom with a bounce, sits dazed
    (head wobbling, eyes rolling, horns drooping), shakes it off and pops up: ta-da."""
    T = 3.6
    c = Clip("fall-over", T, frames=108)
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def k_of(t):
        if t < 0.25:
            return 0.0
        if t < 0.7:
            return 1.08 * ease("in", (t - 0.25) / 0.45)
        if t < 1.0:
            return 1.08 - 0.08 * smooth(0.7, 1.0, t)
        if t < 2.35:
            return 1.0
        if t < 2.75:
            return 1.0 - ease("out", (t - 2.35) / 0.4)
        return 0.0

    def solve(t, p, skel):
        k = k_of(t)
        slip = pulse(t, 0.08, 0.2, 0.35, 0.3)
        seated(p, body, k, lean=-20 * slip * (1 - k))
        hips(body, p, dy=0.06 * slip, pitch=-14 * slip)
        daze = pulse(t, 1.0, 0.1, 1.15, 0.2)
        circ = TAU * 1.6 * (t - 1.0)
        p.add("head", 8 * math.sin(circ) * daze + 10 * daze, 0, 10 * math.cos(circ) * daze)
        p.add("chest", 6 * daze, 0, 0)
        ta = pulse(t, 2.75, 0.15, 0.4, 0.3)
        f = sit_feet(k)
        # the slip: the left foot shoots forward and up
        body.plant(p, 1, pos=(f[1]["pos"][0], f[1]["pos"][1] - 0.3 * slip, 0), yaw=f[1]["yaw"],
                   lift=0.25 * slip, roll=-30 * slip)
        body.plant(p, -1, pos=f[-1]["pos"], yaw=f[-1]["yaw"], lift=0.06 * slip, roll=-10 * slip)
        mill = pulse(t, 0.05, 0.1, 0.55, 0.2)
        for sg in (1, -1):
            if mill > 0.01:
                a = TAU * 2.5 * t + (0 if sg > 0 else math.pi)
                tgt = V(sg * 0.45, -0.1 + 0.2 * math.cos(a), 1.25 + 0.25 * math.sin(a))
                body.hand_to(p, sg, RW[sg].lerp(tgt, mill), elbow=(0.6, 0.2, -0.3))
                open_hand(p, sg, 14 * mill)
            elif daze > 0.01:
                tgt = V(sg * 0.32, 0.25, 0.12)
                body.hand_to(p, sg, RW[sg].lerp(tgt, daze), elbow=(0.5, 0.5, 0.0))
            elif ta > 0.01:
                body.hand_to(p, sg, RW[sg].lerp(V(sg * 0.5, -0.2, 1.3), ta), elbow=(0.6, 0.1, -0.4),
                             hand_rot=hand_world((sg, -0.2, 0.4), (0, -0.3, 1)) if ta > 0.5 else None)
                open_hand(p, sg, 16 * ta)
        if ta > 0.01:
            body.plant(p, 1, roll=16 * ta)
            body.plant(p, -1, roll=16 * ta)
        return p

    c.solve(solve)

    def face_(t):
        p = Pose()
        shock = pulse(t, 0.08, 0.08, 0.6, 0.2)
        daze = pulse(t, 1.0, 0.1, 1.15, 0.2)
        ta = pulse(t, 2.75, 0.15, 0.4, 0.3)
        p.face.update({"grin": 1.0 - shock - daze + 0.0 * ta, "wide": shock, "flat": 0.6 * daze,
                       "smirk_L": 0.4 * daze})
        circ = TAU * 2.2 * (t - 1.0)
        p = p + look((18 * math.sin(circ) * daze, 18 * math.cos(circ) * daze))
        p.both("lid_up", x=0.3 * LID_UP * daze)
        brows(p, 2.0 * shock, 2.0 * shock, 1.4 * shock)
        horns(p, x=24 * daze + 14 * ring(t, 0.7, 18, 4), z=-10 * daze)
        ears(p, spin=120 * daze * math.sin(TAU * 0.8 * (t - 1.0)))
        squint(p, 0.6 * ta)
        return p

    c.layer(face_)
    c.layer(blinks([2.5, 2.62]))
    return c


# ------------------------------------------------------------------------------------------ the dance
def spin_feet(body, theta):
    """Plant kwargs that turn both feet `theta` degrees round the vertical through his root (for spinning
    on the spot while they are off the floor, or pivoting on them)."""
    out = {}
    Rz = Matrix.Rotation(math.radians(theta), 3, "Z")
    for sg in (1, -1):
        ball = body.foot[sg]["ball"]
        d = Rz @ ball - ball
        out[sg] = dict(pos=(d.x, d.y, 0.0), yaw=theta * sg)
    return out


def dance(body):
    """His own dance, eight seconds at 150 beats a minute, and none of it a fad: the gremlin. Four beats of
    the shuffle (hopping foot to foot, noodle arms flailing up and down), a spin on the spot with a kick, the
    noodle (a wave rippling up through him from the knees, arms over his head), the horn-bang with air
    guitar (crouched, the horns doing the work), a stomp with fists pumping, and a leap into his pose: arms
    up in a V, one foot kicked up behind, a wink. Eases in from REST over the first half second and out
    over the last."""
    T, NB = DANCE_SECS, DANCE_BEATS
    beat = T / NB
    c = Clip("dance", T, frames=int(round(T * 30)))
    c.key(0.0, REST)
    RW = rest_wrists(body)

    def move(b, d, feet, hands):
        u = b % 1.0
        on = 1 if int(b) % 2 == 0 else -1
        hop = math.sin(math.pi * u) ** 1.4
        if b < 4:                                            # the shuffle
            hips(body, d, dx=0.06 * on * hop, dz=-0.04 + 0.08 * hop, roll=-6 * on)
            d.add("chest", 4, 8 * on, 6 * on)
            d.add("head", 6 * hop, 0, -10 * on)
            for sg in (1, -1):
                up = 1 if sg == on else -1
                d.side("upper_arm", sg, x=10 + 20 * up, z=-10 + 60 * (0.5 + 0.5 * up) * hop)
                d.side("forearm", sg, x=40 + 40 * (0.5 - 0.5 * up), y=30 * up * sg)
                open_hand(d, sg, 16)
            feet[on] = dict(lift=0.06 * hop * 0.5)
            feet[-on] = dict(pos=(-on * 0.05, -0.08 * hop, 0), lift=0.16 * hop, roll=-20 * hop)
            d.face.update({"grin": 0.6, "ee": 0.6})
        elif b < 6:                                          # the spin, with a kick at the end
            s = smooth(4.1, 5.5, b)
            theta = 360 * ease("inout", s)
            air = math.sin(math.pi * smooth(4.0, 5.7, b))
            hips(body, d, dz=-0.03 + 0.12 * air, yaw=theta)
            sf = spin_feet(body, theta)
            for sg in (1, -1):
                feet[sg] = dict(sf[sg], lift=0.12 * air)
                d.side("upper_arm", sg, x=-10, z=40 * air + 10)
                d.side("forearm", sg, x=20)
                open_hand(d, sg, 18)
            kick = pulse(b, 5.5, 0.2, 0.0, 0.3)
            feet[1] = dict(feet[1], pos=(feet[1]["pos"][0] + 0.08 * kick, feet[1]["pos"][1] - 0.25 * kick, 0),
                           lift=feet[1]["lift"] + 0.22 * kick, roll=-30 * kick)
            d.face.update({"grin": 0.0, "wide": 1.0})
        elif b < 10:                                         # the noodle
            w = TAU * (b - 6) / 2
            hips(body, d, dx=0.07 * math.sin(w), dz=-0.06 + 0.02 * math.cos(2 * w), roll=-8 * math.sin(w))
            d.add("spine", 0, 0, 12 * math.sin(w - 0.6))
            d.add("chest", 0, 0, -14 * math.sin(w - 1.2))
            d.add("head", 0, 0, 16 * math.sin(w - 1.8))
            for sg in (1, -1):
                ph = w - 1.6 + (0 if sg > 0 else math.pi)
                hands[sg] = (V(sg * (0.26 + 0.08 * math.sin(ph)), -0.12, 1.52 + 0.06 * math.cos(ph)),
                             (0.6, 0.1, -0.3), hand_world((sg * 0.6 * math.sin(ph), -0.2, 1), (0, -1, 0)))
                open_hand(d, sg, 18)
            for sg in (1, -1):
                feet[sg] = dict(knee_out=0.12 * math.sin(w + (0 if sg > 0 else math.pi)), roll=10 * max(0.0, math.sin(w) * sg))
            d.face.update({"grin": 0.4, "ee": 0.8})
            d.both("lid_up", x=0.3 * LID_UP)
        elif b < 14:                                         # horn-bang and air guitar
            bang = math.exp(-u * 6) * (1 - math.exp(-u * 60))
            hips(body, d, dz=-0.14 - 0.03 * bang, pitch=10)
            feet[1] = dict(pos=(0.08, 0, 0), yaw=16)
            feet[-1] = dict(pos=(-0.08, 0, 0), yaw=16)
            d.add("spine", 8 + 8 * bang, 0, 0)
            d.add("chest", 6 + 10 * bang, 0, 0)
            d.add("neck", 10 * bang, 0, 0)
            d.add("head", -4 + 26 * bang, 0, 0)
            horns(d, x=-22 * bang, tip=1.8)
            strum = math.sin(TAU * 2 * b)
            hands[-1] = (V(-0.06, -0.3, 0.86 + 0.05 * strum), (0.6, 0.3, -0.4), hand_world((1, -0.2, -0.3), (0, 1, 0)))
            hands[1] = (V(0.42, -0.3, 1.12), (0.6, 0.2, -0.4), hand_world((0.6, -0.3, 0.7), (0, 1, 0)))
            fist(d, -1, 0.6)
            d.fingers(1, 50, spread=6, thumb=30)
            d.face.update({"grin": 0.0, "grit": 0.5, "wide": 0.5 * bang})
            d.both("lid_up", x=0.4 * LID_UP)
        elif b < 18:                                         # the stomp
            stomp = math.sin(math.pi * u) ** 2
            hips(body, d, dz=-0.06 + 0.05 * stomp, dx=0.05 * on, roll=-6 * on, yaw=10 * on)
            feet[on] = dict(pos=(on * 0.06, -0.06 * stomp, 0), lift=0.18 * stomp, roll=-10 * stomp)
            feet[-on] = dict()
            for sg in (1, -1):
                pump = stomp if sg == on else 0.2
                d.side("upper_arm", sg, x=30 + 40 * pump, z=-10 + 40 * pump)
                d.side("forearm", sg, x=90 - 50 * pump)
                fist(d, sg)
            d.add("chest", 6 * stomp, 10 * on, 0)
            d.add("head", 10 * stomp, 0, 8 * on)
            d.face.update({"grin": 0.3, "grit": 0.4, "wide": 0.4})
        else:                                                # the leap into his pose, and held
            leap = math.sin(math.pi * smooth(18.0, 18.9, b))
            pose = smooth(18.3, 18.9, b)
            hips(body, d, dz=0.18 * leap, dx=-0.03 * pose, roll=6 * pose)
            for sg in (1, -1):
                hands[sg] = (V(sg * 0.46, -0.08, 1.56), (0.6, 0.1, -0.4),
                             hand_world((sg * 0.6, -0.2, 1), (0, -1, 0)))
                open_hand(d, sg, 18)
            feet[-1] = dict(lift=0.2 * leap)
            feet[1] = dict(pos=(0.04, 0.22 * pose, 0), lift=0.2 * leap + 0.26 * pose, roll=40 * pose)
            d.add("chest", -10 * pose, -8 * pose, 0)
            d.add("head", -6 * pose, 10 * pose, 10 * pose)
            wink(d, 1, pose)
            d.face.update({"grin": 1.0, "smirk_L": 0.6 * pose})

    def solve(t, p0, skel):
        w = env(t, T, 0.5, 0.5)
        d = REST.copy()
        feet, hands = {}, {}
        move(t / beat, d, feet, hands)
        p = blend(REST, d, w)
        p.quat = {}
        for sg in (1, -1):
            s = dict(feet.get(sg, {}))
            if "pos" in s:
                s["pos"] = tuple(v * w for v in s["pos"])
            for key in ("yaw", "roll", "lift", "bank", "knee_out"):
                if key in s:
                    s[key] = s[key] * w
            body.plant(p, sg, **s)
        for sg, (tgt, elbow, hr) in hands.items():
            body.hand_to(p, sg, RW[sg].lerp(tgt, w), elbow=elbow, hand_rot=hr if w > 0.6 else None)
        return p

    c.solve(solve)
    c.layer(lambda t: horn_sway(t, T, 4 * env(t, T), cycles=(4, 9)))
    c.layer(blinks([T * 0.3, T * 0.62]))
    return c


# ------------------------------------------------------------------------------------------- the lot
EVERYDAY = ["idle", "walk", "run", "sneak", "point", "laugh", "shrug", "wave", "cheer", "fold-arms",
            "hands-on-hips", "jump", "peek", "push", "pull", "carry", "sit", "fall-over", "dance"]
PACKS = {"zip": EVERYDAY}


def clips(body: Body):
    out = {
        "idle": idle(body),
        "walk": walk(body),
        "run": run(body),
        "sneak": sneak(body),
        "point": point_clip(body),
        "laugh": laugh(body),
        "shrug": shrug(body),
        "wave": wave(body),
        "cheer": cheer(body),
        "fold-arms": fold_arms(body),
        "hands-on-hips": hands_on_hips(body),
        "jump": jump(body),
        "peek": peek(body),
        "push": push(body),
        "pull": pull(body),
        "carry": carry(body),
        "sit": sit(body),
        "fall-over": fall_over(body),
        "dance": dance(body),
    }
    out["calibrate"] = calibrate(body)
    return out


def calibrate(body):
    """Not for the page: one test pose a second, to check the skeleton's axes by eye."""
    c = Clip("calibrate", 6.0)
    tests = [REST.copy(), REST.copy().both("upper_arm", z=48), REST.copy().both("lid_up", x=LID_UP).both("lid_lo", x=LID_LO),
             horns(REST.copy(), x=25, z=15), REST.copy() + look((12, 25)), ears(REST.copy(), spin=60, tilt=20)]
    for i, q in enumerate(tests):
        c.key(float(i), q, "step")
        c.key(i + 0.999, q, "step")
    c.solve(stand(body))
    return c
