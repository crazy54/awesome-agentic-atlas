"""What every pal's clips are made of: a `Body` that knows one character's feet, legs and arms well enough to
plant a foot, roll it heel to toe, put a hand on a point, and walk; and the small motions that keep a still
character alive (breathing, blinks, glances, a wobble in whatever is loose on its head).

A clip here is a `kit.anim.Clip` whose base track is key poses and whose layers are the functions below.
Foot and hand placement happens in the clip's `post` stage, after the key poses and layers have set the
hips, so a foot stays where it was put however the body above it moves.

World positions are armature space with the root at rest: metres, Z up, the character facing -Y.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from kit.anim import Pose, ease, noise1, pulse, smooth

TAU = math.tau
SIDES = ((1, "_L"), (-1, "_R"))


def V(*a):
    return Vector(a)


class Body:
    """One character's geometry, read off its skeleton: rest ankle, ball and heel of each foot, hip and
    shoulder heads, and the conversions between world offsets and a bone's own frame."""

    def __init__(self, skel, heel_back=0.19, toe_front=0.49):
        self.skel = skel
        B = skel.bones
        self.rest = {n: b["rest"] for n, b in B.items()}
        self.foot = {}
        for sg, s in SIDES:
            ankle = B[f"foot{s}"]["rest"].translation.copy()
            ball = B[f"toe{s}"]["rest"].translation.copy()
            heel = V(ankle.x, heel_back, 0.0)
            toe = V(ball.x, -toe_front, 0.0)
            self.foot[sg] = dict(ankle=ankle, ball=V(ball.x, ball.y, 0.0), heel=heel, toe=toe,
                                 rot=B[f"foot{s}"]["rest"].to_3x3(), toe_rot=B[f"toe{s}"]["rest"].to_3x3())
        self.hip_z = B["hips"]["rest"].translation.z
        self.leg = {sg: (B[f"thigh{s}"]["length"] + B[f"shin{s}"]["length"]) for sg, s in SIDES}

    # ---- frames ----
    def to_local(self, bone, world_vec):
        """A world offset expressed in `bone`'s rest frame (right for bones whose parents are not turned)."""
        return self.rest[bone].to_3x3().inverted() @ Vector(world_vec)

    def move_world(self, pose, bone, dx=0.0, dy=0.0, dz=0.0):
        l = self.to_local(bone, (dx, dy, dz))
        return pose.move(bone, l.x, l.y, l.z)

    # ---- feet ----
    def foot_at(self, side, pos=(0, 0, 0), yaw=0.0, roll=0.0, lift=0.0, bank=0.0):
        """Where the ankle goes and how the foot is turned for a foot `pos` metres from its rest place on the
        floor, yawed `yaw` degrees (toe out positive on either side), rolled `roll` degrees (heel up about
        the ball when positive, toe up about the heel when negative), `lift` metres off the floor, banked
        `bank` degrees (outer edge up). Returns (ankle, foot world rotation 3x3, toe local roll)."""
        f = self.foot[side]
        pivot = f["ball"] if roll >= 0 else f["heel"]
        R = (Matrix.Rotation(math.radians(yaw * side), 3, "Z") @
             Matrix.Rotation(math.radians(bank * side), 3, "Y") @
             Matrix.Rotation(math.radians(roll), 3, "X"))
        offset = Vector(pos) + V(0, 0, lift)
        ankle = pivot + R @ (f["ankle"] - pivot) + offset
        # turning about the pivot: yaw and bank about the pivot too
        rot = R @ f["rot"]
        return ankle, rot, (-roll if roll > 0 else 0.0)

    def plant(self, pose, side, pos=(0, 0, 0), yaw=0.0, roll=0.0, lift=0.0, bank=0.0, knee_out=0.0):
        """Solve the leg so the foot is where `foot_at` says, the knee pointing forward (and out by
        `knee_out` metres)."""
        s = "_L" if side > 0 else "_R"
        ankle, rot, toe = self.foot_at(side, pos, yaw, roll, lift, bank)
        M = self.skel.fk(pose, "hips")
        hip = (M["hips"] @ self.skel.bones[f"thigh{s}"]["rel"]).translation
        pole = (hip + ankle) / 2 + V(side * knee_out, -1.5, 0.0)
        self.skel.two_bone(pose, f"thigh{s}", f"shin{s}", ankle, pole, end=f"foot{s}", end_world=rot)
        if toe:
            pose.set(f"toe{s}", toe, 0, 0)
        return pose

    def hand_to(self, pose, side, target, elbow=(0.5, 0.4, -0.6), hand_rot=None):
        """Put the wrist on `target` (world), the elbow bending towards `elbow` (an offset from the
        shoulder, x mirrored for the right). `hand_rot` (3x3 world) orients the hand if given."""
        s = "_L" if side > 0 else "_R"
        M = self.skel.fk(pose, f"shoulder{s}")
        sh = (M[f"shoulder{s}"] @ self.skel.bones[f"upper_arm{s}"]["rel"]).translation
        pole = sh + V(elbow[0] * side, elbow[1], elbow[2])
        self.skel.two_bone(pose, f"upper_arm{s}", f"forearm{s}", target, pole,
                           end=f"hand{s}" if hand_rot is not None else None, end_world=hand_rot)
        return pose

    def where(self, pose, bone, at="head"):
        M = self.skel.fk(pose, bone)
        if at == "head":
            return M[bone].translation.copy()
        return (M[bone] @ Vector((0, self.skel.bones[bone]["length"], 0, 1))).to_3d()


# ---------------------------------------------------------------------------------------- walking
def gait(t, period, stance=0.6, phase=0.0):
    """Where one foot is in its stride at time t: (u, swinging, s) with u in 0..1 through the whole step,
    `s` the progress through the current phase (stance or swing)."""
    u = (t / period + phase) % 1.0
    if u < stance:
        return u, False, u / stance
    return u, True, (u - stance) / (1 - stance)


def stride_foot(t, period, stride, stance=0.6, phase=0.0, height=0.13, toe_off=28.0, heel_strike=-14.0):
    """One foot's (y offset, lift, roll) for a walk in place: during stance it slides back from -stride/2
    (in front) to +stride/2 at constant speed (so a page moving the view at stride/(stance*period) keeps it
    planted), rolling up on the toe at the end; during swing it lifts and carries forward, toe up for the
    heel strike."""
    u, swing, s = gait(t, period, stance, phase)
    if not swing:
        y = -stride / 2 + stride * s
        roll = toe_off * smooth(0.72, 1.0, s) ** 1.4 + heel_strike * (1 - smooth(0.0, 0.18, s))
        return y, 0.0, roll
    y = stride / 2 - stride * ease("inout", s)
    lift = height * math.sin(math.pi * s) ** 0.8
    roll = toe_off * (1 - smooth(0.0, 0.35, s)) + heel_strike * smooth(0.55, 1.0, s)
    return y, lift, roll


# --------------------------------------------------------------------------------------- liveliness
def blink_at(t, times, close=0.06, hold=0.03, open_=0.1):
    """1 at the bottom of each blink, 0 with the eyes open."""
    return max((pulse(t, a, close, hold, open_) for a in times), default=0.0)


def blink_layer(times, up=-46.0, lo=40.0, lids=("lid_up", "lid_lo")):
    """Lids close by turning the upper lid down (`up` degrees about its X) and the lower lid up."""
    def f(t):
        b = blink_at(t, times)
        if b <= 0:
            return None
        p = Pose()
        p.both(lids[0], x=up * b)
        p.both(lids[1], x=lo * b)
        return p
    return f


def breathe(period=4.0, amount=1.0, phase=0.0):
    def f(t):
        b = math.sin(TAU * (t / period + phase))
        p = Pose()
        p.add("chest", -1.2 * amount * b, 0, 0)
        p.add("spine", 0.6 * amount * b, 0, 0)
        p.both("shoulder", z=0.8 * amount * b, add=True)
        p.add("head", 0.7 * amount * b, 0, 0)
        return p
    return f


def look(eyes=(0.0, 0.0), head=(0.0, 0.0, 0.0)):
    """Eyes (up, to the character's left) in degrees, and the head (nod down, tilt, turn left)."""
    p = Pose()
    for s in ("_L", "_R"):
        p.set("eye" + s, eyes[0], 0.0, eyes[1])
    if any(head):
        p.add("head", head[0], head[2], head[1])
    return p


def brows(p, inner=0.0, mid=0.0, outer=0.0, side=0, unit=0.012):
    """Raise brows (units of about a centimetre for Archie): `side` 0 both, +1 left only, -1 right only."""
    for sg, s in SIDES:
        if side and side != sg:
            continue
        p.move(f"brow_in{s}", 0, inner * unit, 0)
        p.move(f"brow_mid{s}", 0, mid * unit, 0)
        p.move(f"brow_out{s}", 0, outer * unit, 0)
    return p


def wobble(bones, t, amount=4.0, speed=1.0, seed=0.0):
    """Loose things (a crest, horns) drifting a little."""
    p = Pose()
    for i, b in enumerate(bones):
        p.add(b, amount * noise1(t * speed, seed + i * 0.7), 0, amount * 0.6 * noise1(t * speed * 1.3, seed + 3 + i))
    return p


def follow(bones, accel, gain=6.0):
    """Secondary motion for a chain: each bone tips against `accel` (a world-ish acceleration, metres/s^2,
    of the head), more for the bones further out."""
    p = Pose()
    for i, b in enumerate(bones):
        k = gain * (i + 1) / len(bones)
        p.add(b, -accel[1] * k, 0.0, accel[0] * k)
    return p
