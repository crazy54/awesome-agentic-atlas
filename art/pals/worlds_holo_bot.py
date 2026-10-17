"""The hologram bot: one of the worlds' tiny agents, projected, at the worlds' own scale (a world is a disc of
radius 1; the bot stands 0.25 tall, feet on Z = 0, facing -Y, which is three.js +Z, towards the reader). It is
for the Core bits where a projection gets loose: "the escapee" (a bot climbs out of the world, waves, runs
off) and "the miniature rebellion" (tiny agents copying Archie). Everything is a hologram (`holo_cyan` with
`holo_white` eyes, smile, antenna tip and chest light), so the page draws it in light like the worlds.

Nodes: the root `holo_bot` (never animated: the page moves it), `bot_body` (pivoting at the hips), and on
it `bot_head` (at the neck), `bot_arm_L` / `bot_arm_R` (at the shoulders; L is the bot's own left, +X) and
`bot_leg_L` / `bot_leg_R` (at the hips).

Clips, all loops, all in place:

  idle    2.0 s  breathing, looking round
  walk    0.8 s  two steps; move the root forward at WALK_SPEED (0.136 units/s) and the feet do not skate
  run     0.5 s  two strides, leaning in; RUN_SPEED (0.332 units/s)
  wave    1.0 s  the right arm up, waving twice
  climb   1.0 s  hand over hand up a face in front of it, a foot up with each pull; raise the root at
                 CLIMB_SPEED (0.138 units/s)
  cheer   1.0 s  both arms up, two hops
  dance   2.0 s  four beats: the hips sway, the arms swap pointing up and down, the knees come up in turn

The speeds are the stance foot's (or the gripping hand's) speed against the body: 4 L sin(A) / period for a
leg of length L swinging through +-A, and the hand's drop over half a climb.
"""
from __future__ import annotations

import math

from mathutils import Matrix

from kit.geo import TAU, V
from worlds_kit import ball, lathe, prism, torus, tube, world

BODY, LIGHT = "holo_cyan", "holo_white"
HIP_Z, HIP_X = 0.062, 0.02                    # the legs hang from here; the feet's soles are on Z = 0
SHOULDER = V(0.036, 0.0, 0.112)
NECK_Z = 0.126
LEG = HIP_Z                                   # hip to sole
ARM = 0.047                                   # shoulder to hand
WALK = dict(period=0.8, swing=26.0)
RUN = dict(period=0.5, swing=42.0)
CLIMB = dict(period=1.0, high=-165.0, low=-60.0)
WALK_SPEED = 4 * LEG * math.sin(math.radians(WALK["swing"])) / WALK["period"]
RUN_SPEED = 4 * LEG * math.sin(math.radians(RUN["swing"])) / RUN["period"]
CLIMB_SPEED = ARM * (math.cos(math.radians(CLIMB["low"])) - math.cos(math.radians(CLIMB["high"]))) / \
    (CLIMB["period"] / 2)

BOT_CLIPS = [("walk", WALK["period"], True), ("run", RUN["period"], True), ("wave", 1.0, True),
             ("climb", CLIMB["period"], True), ("cheer", 1.0, True), ("dance", 2.0, True), ("idle", 2.0, True)]


def R(axis, deg):
    return Matrix.Rotation(math.radians(deg), 4, axis)


def T(x=0.0, y=0.0, z=0.0):
    return Matrix.Translation((x, y, z))


def s(t, period, phase=0.0):
    return math.sin(TAU * (t / period + phase))


def c(t, period, phase=0.0):
    return math.cos(TAU * (t / period + phase))


def blend(t, period):
    """0 -> 1 -> 0 over a period, smoothly."""
    return 0.5 - 0.5 * math.cos(TAU * t / period)


# ------------------------------------------------------------------------------------------- clips
# Each returns the deltas of the moving parts at time t. +X rotation swings a hanging limb back (its end to
# +Y), -X forward; about Y, a negative angle swings the left arm out and up, a positive one the right.
def walk(t):
    P, A = WALK["period"], WALK["swing"]
    th = A * s(t, P)
    lift = 0.008
    return dict(
        body=T(z=LEG * (math.cos(math.radians(th)) - 1)) @ R("X", 5) @ R("Y", 3 * s(t, P)) @ R("Z", 5 * s(t, P)),
        head=R("X", -3) @ R("Z", -4 * s(t, P)),
        arm_L=R("X", -0.9 * th), arm_R=R("X", 0.9 * th),
        leg_L=T(z=lift * max(0.0, -c(t, P))) @ R("X", th),
        leg_R=T(z=lift * max(0.0, c(t, P))) @ R("X", -th))


def run(t):
    P, A = RUN["period"], RUN["swing"]
    th = A * s(t, P)
    bounce = 0.008 * (1 - c(t, P / 2)) / 2
    return dict(
        body=T(z=LEG * (math.cos(math.radians(th)) - 1) + bounce) @ R("X", 14) @ R("Z", 7 * s(t, P)),
        head=R("X", -8),
        arm_L=R("X", -15 - 1.1 * th), arm_R=R("X", -15 + 1.1 * th),
        leg_L=T(z=0.015 * max(0.0, -c(t, P))) @ R("X", th),
        leg_R=T(z=0.015 * max(0.0, c(t, P))) @ R("X", -th))


def wave(t):
    return dict(
        body=T(z=0.003 * s(t, 0.5)) @ R("Y", -3 * s(t, 1.0)),
        head=R("Y", 8) @ R("Z", 6 * s(t, 1.0)),
        arm_R=R("X", -15) @ R("Y", 128 + 25 * s(t, 0.5)),
        arm_L=R("X", 4 * s(t, 1.0)))


def climb(t):
    P, hi, lo = CLIMB["period"], CLIMB["high"], CLIMB["low"]
    mid, amp = (hi + lo) / 2, (lo - hi) / 2
    return dict(
        body=T(z=0.004 * s(t, P / 2)) @ R("X", 12) @ R("Y", 5 * s(t, P)),
        head=R("X", -14),
        arm_L=R("X", mid - amp * c(t, P)) @ R("Y", -10),
        arm_R=R("X", mid + amp * c(t, P)) @ R("Y", 10),
        leg_L=R("X", -30 + 25 * c(t, P)), leg_R=R("X", -30 - 25 * c(t, P)))


def cheer(t):
    hopk = abs(s(t, 1.0))                             # two hops a second
    return dict(
        body=T(z=0.022 * hopk),
        head=R("X", -8 * hopk),
        arm_L=R("Y", -135 + 15 * s(t, 0.5)), arm_R=R("Y", 135 - 15 * s(t, 0.5)),
        leg_L=R("X", -10 * hopk), leg_R=R("X", 10 * hopk))


def dance(t):
    w = blend(t, 2.0)                                 # 0 at the top of the bar, 1 halfway
    beat = abs(s(t, 1.0))                             # a dip on every beat
    return dict(
        body=T(x=0.01 * s(t, 2.0), z=-0.005 * beat) @ R("Z", 14 * s(t, 2.0)),
        head=R("X", 8 * beat) @ R("Y", 6 * s(t, 2.0)),
        arm_L=R("X", -20 * beat) @ R("Y", -(25 + 120 * (1 - w))),
        arm_R=R("X", -20 * beat) @ R("Y", 25 + 120 * w),
        leg_L=R("X", -20 * max(0.0, s(t, 1.0))), leg_R=R("X", -20 * max(0.0, -s(t, 1.0))))


def idle(t):
    return dict(
        body=T(z=0.002 * s(t, 1.0)) @ R("Y", 1.5 * s(t, 2.0)),
        head=R("Z", 18 * s(t, 2.0)) @ R("X", 4 * s(t, 1.0)),
        arm_L=R("X", 4 * s(t, 2.0)), arm_R=R("X", -4 * s(t, 2.0)))


CLIPS = dict(walk=walk, run=run, wave=wave, climb=climb, cheer=cheer, dance=dance)
PARTS = ("body", "head", "arm_L", "arm_R", "leg_L", "leg_R")


def part(fn, key):
    return lambda t: fn(t).get(key, Matrix.Identity(4))


# ------------------------------------------------------------------------------------------- build
@world("holo-bot", clips=BOT_CLIPS, root_name="holo_bot")
def holo_bot(W):
    """The escapee: a tiny agent, in light."""
    W.camera = dict(dist=0.62, focus=(0, 0, 0.125), el=12.0, az=24.0)
    W.strips = [("clips", [(clip, k * secs / 4) for clip, secs, _ in BOT_CLIPS for k in range(4)])]
    W.preview_t = 0.6
    nodes = {}
    for key, pivot, parent in (("body", (0, 0, HIP_Z), None), ("head", (0, 0, NECK_Z), "body"),
                               ("arm_L", SHOULDER, "body"), ("arm_R", V(-SHOULDER.x, 0, SHOULDER.z), "body"),
                               ("leg_L", (HIP_X, 0, HIP_Z), "body"), ("leg_R", (-HIP_X, 0, HIP_Z), "body")):
        name = "bot_" + key
        W.node(name, pivot, parent=nodes.get(parent), idle=part(idle, key),
               motion={clip: part(fn, key) for clip, fn in CLIPS.items()}, kind="holo")
        nodes[key] = name
    with W.on("bot_body"):
        lathe(BODY, (0, 0, 0), [(0.0, 0.052), (0.026, 0.054), (0.038, 0.074), (0.036, 0.104), (0.025, 0.124),
                                (0.0, 0.128)], segs=10)
        prism(LIGHT, (0, -0.033, 0.092), 0.009, 0.006, n=8, rot=(90, 0, 0))
    with W.on("bot_head"):
        ball(BODY, (0, 0, 0.172), 0.05, segs=12, rings=5, scale=(1.08, 1.0, 0.94))
        for sx in (-1, 1):
            ball(LIGHT, (sx * 0.017, -0.046, 0.176), 0.009, segs=6, rings=3, scale=(1, 0.5, 1.3))
        torus(LIGHT, (0, -0.047, 0.158), 0.011, 0.0022, rot=(90, 180, 0), segs=8, sides=3, arc=math.pi)
        prism(BODY, (0, 0, 0.214), 0.003, 0.026, n=4, bottom=False, top=False)
        ball(LIGHT, (0, 0, 0.242), 0.009, segs=6, rings=3)
    for sx, side in ((1, "L"), (-1, "R")):
        with W.on(f"bot_arm_{side}"):
            tube(BODY, [(sx * 0.034, 0, 0.112), (sx * 0.043, -0.003, 0.09), (sx * 0.046, -0.006, 0.072)], 0.009,
                 sides=6)
            ball(BODY, (sx * 0.046, -0.006, 0.066), 0.012, segs=6, rings=3)
        with W.on(f"bot_leg_{side}"):
            tube(BODY, [(sx * HIP_X, 0, HIP_Z), (sx * HIP_X, 0, 0.014)], 0.0105, sides=6)
            ball(BODY, (sx * HIP_X, -0.006, 0.009), 0.013, segs=8, rings=3, scale=(1, 1.35, 0.65))
