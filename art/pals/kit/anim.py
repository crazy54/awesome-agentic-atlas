"""Animation for the pals: poses, timelines, a forward-kinematics model of the skeleton to solve legs and
arms against, and a baker that writes it all straight into actions and NLA tracks for the glTF exporter.

POSES. A pose is a `Pose`: per bone a rotation in the bone's own rest frame (Euler degrees, XYZ) and a
location offset (metres, also in the bone's rest frame), plus face shape-key weights. With the skeleton's
axes (see rig.py) +X is flexion nearly everywhere. Poses are usually written for the left side and mirrored:
`p.both("upper_arm", x, y, z)` sets `_L` as given and `_R` with Y and Z negated, which is what an X-mirror does
to a rotation in a symmetric rig's bone frames.

TIMELINES. A clip is a function of time. `Track` interpolates a value (a number, a tuple, or a Pose) between
keys with an easing per segment ("linear", "in", "out", "inout", "back" with overshoot, "settle" with a
damped wobble, "step" to hold then cut). `Clip` holds a base track of poses and any number of additive
layers (callables of t returning a Pose of offsets), and evaluates to one Pose per frame.

KINEMATICS. `Skeleton` reads the armature's rest matrices once and evaluates poses in plain Python, so a clip
can ask where a hand or a foot is, plant a foot on the floor while the hips move (`leg_ik`), put a hand on a
point (`arm_ik`), or turn the head and eyes towards a target (`look`), without asking Blender to update.

BAKING. `bake()` evaluates a clip at every frame and writes location and quaternion F-curves for the
armature and value F-curves for the face's shape keys, linear between frames, into one action each, pushed
onto NLA tracks named for the clip. The exporter's NLA_TRACK mode turns each name into one glTF animation.
"""
from __future__ import annotations

import math

import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

TAU = math.tau


# ------------------------------------------------------------------------------------------ easing
def ease(kind, t):
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    if kind == "linear":
        return t
    if kind == "in":
        return t * t * t
    if kind == "out":
        u = 1 - t
        return 1 - u * u * u
    if kind == "inout":
        return t * t * (3 - 2 * t)
    if kind == "inout2":
        return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
    if kind == "back":                           # overshoots then comes back
        c = 1.9
        u = t - 1
        return 1 + (c + 1) * u * u * u + c * u * u
    if kind == "settle":                         # arrives, then a damped wobble
        if t >= 1:
            return 1.0
        return 1 - math.exp(-6 * t) * math.cos(t * 13)
    if kind == "step":
        return 0.0 if t < 1 else 1.0
    if kind == "snap":                           # most of the move in the first fifth
        return 1 - (1 - t) ** 6
    raise ValueError(kind)


def smooth(e0, e1, x):
    if e0 == e1:
        return 0.0 if x < e0 else 1.0
    t = (x - e0) / (e1 - e0)
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3 - 2 * t)


def pulse(t, at, rise, hold=0.0, fall=None):
    """0 -> 1 over `rise` starting at `at`, held for `hold`, back to 0 over `fall` (default `rise`)."""
    fall = rise if fall is None else fall
    if t < at:
        return 0.0
    if t < at + rise:
        return smooth(at, at + rise, t)
    if t < at + rise + hold:
        return 1.0
    return 1.0 - smooth(at + rise + hold, at + rise + hold + fall, t)


def wave(t, period, phase=0.0):
    return math.sin(TAU * (t / period + phase))


def noise1(t, seed=0.0):
    """Smooth 1D noise, roughly -1..1, from a sum of incommensurate sines (cheap and deterministic)."""
    return (math.sin(t * 1.7 + seed * 3.1) * 0.5 + math.sin(t * 2.9 + seed * 1.3) * 0.3 +
            math.sin(t * 5.3 + seed * 2.7) * 0.2)


# -------------------------------------------------------------------------------------------- pose
def flip(name):
    if name.endswith("_L"):
        return name[:-2] + "_R"
    if name.endswith("_R"):
        return name[:-2] + "_L"
    return name


class Pose:
    """Bone rotations (Euler degrees in the bone's rest frame) and offsets, and face weights."""

    __slots__ = ("rot", "loc", "face", "quat")

    def __init__(self, rot=None, loc=None, face=None):
        self.rot = dict(rot or {})          # name -> (x, y, z) degrees
        self.loc = dict(loc or {})          # name -> (x, y, z) metres, bone frame
        self.face = dict(face or {})        # shape key -> weight
        self.quat = {}                      # name -> Quaternion, overriding rot (set by solvers)

    def copy(self):
        p = Pose(self.rot, self.loc, self.face)
        p.quat = dict(self.quat)
        return p

    # ---- writing ----
    def set(self, name, x=0.0, y=0.0, z=0.0):
        self.rot[name] = (x, y, z)
        return self

    def add(self, name, x=0.0, y=0.0, z=0.0):
        a = self.rot.get(name, (0.0, 0.0, 0.0))
        self.rot[name] = (a[0] + x, a[1] + y, a[2] + z)
        return self

    def move(self, name, x=0.0, y=0.0, z=0.0):
        a = self.loc.get(name, (0.0, 0.0, 0.0))
        self.loc[name] = (a[0] + x, a[1] + y, a[2] + z)
        return self

    def both(self, base, x=0.0, y=0.0, z=0.0, add=False):
        f = self.add if add else self.set
        f(base + "_L", x, y, z)
        f(base + "_R", x, -y, -z)
        return self

    def side(self, base, side, x=0.0, y=0.0, z=0.0, add=False):
        """`side` is +1 for the left, -1 for the right; values are written as for the left."""
        f = self.add if add else self.set
        if side > 0:
            f(base + "_L", x, y, z)
        else:
            f(base + "_R", x, -y, -z)
        return self

    def mirrored(self):
        p = Pose()
        for k, (x, y, z) in self.rot.items():
            p.rot[flip(k)] = (x, -y, -z) if k != flip(k) else (x, -y, -z)
        for k, (x, y, z) in self.loc.items():
            p.loc[flip(k)] = (-x, y, z) if k == flip(k) else (x, y, z)
        for k, v in self.face.items():
            p.face[flip(k)] = v
        return p

    def fingers(self, side, curl, spread=0.0, thumb=None, which=("index", "middle", "ring")):
        """Curl each finger by `curl` degrees per joint (a fist is about 80), fanning them by `spread`."""
        sfx = "_L" if side > 0 else "_R"
        sg = 1 if side > 0 else -1
        for k, f in enumerate(which):
            fan = spread * (k - 1)
            c = curl if not isinstance(curl, (tuple, list)) else curl[k]
            self.set(f"{f}_1{sfx}", c, 0.0, fan * sg)
            self.set(f"{f}_2{sfx}", c * 1.1, 0.0, 0.0)
            self.set(f"{f}_3{sfx}", c * 0.9, 0.0, 0.0)
        t = curl * 0.5 if thumb is None else thumb
        self.set(f"thumb_1{sfx}", t * 0.4, 0.0, 0.0)
        self.set(f"thumb_2{sfx}", t, 0.0, 0.0)
        self.set(f"thumb_3{sfx}", t, 0.0, 0.0)
        return self

    # ---- combining ----
    def __add__(self, o):
        p = self.copy()
        for k, v in o.rot.items():
            a = p.rot.get(k, (0.0, 0.0, 0.0))
            p.rot[k] = (a[0] + v[0], a[1] + v[1], a[2] + v[2])
        for k, v in o.loc.items():
            a = p.loc.get(k, (0.0, 0.0, 0.0))
            p.loc[k] = (a[0] + v[0], a[1] + v[1], a[2] + v[2])
        for k, v in o.face.items():
            p.face[k] = p.face.get(k, 0.0) + v
        p.quat.update(o.quat)
        return p

    def scaled(self, w):
        p = Pose({k: (v[0] * w, v[1] * w, v[2] * w) for k, v in self.rot.items()},
                 {k: (v[0] * w, v[1] * w, v[2] * w) for k, v in self.loc.items()},
                 {k: v * w for k, v in self.face.items()})
        return p


def blend(a: Pose, b: Pose, w: float) -> Pose:
    p = Pose()
    z = (0.0, 0.0, 0.0)
    for k in set(a.rot) | set(b.rot):
        x, y = a.rot.get(k, z), b.rot.get(k, z)
        p.rot[k] = (x[0] + (y[0] - x[0]) * w, x[1] + (y[1] - x[1]) * w, x[2] + (y[2] - x[2]) * w)
    for k in set(a.loc) | set(b.loc):
        x, y = a.loc.get(k, z), b.loc.get(k, z)
        p.loc[k] = (x[0] + (y[0] - x[0]) * w, x[1] + (y[1] - x[1]) * w, x[2] + (y[2] - x[2]) * w)
    for k in set(a.face) | set(b.face):
        x, y = a.face.get(k, 0.0), b.face.get(k, 0.0)
        p.face[k] = x + (y - x) * w
    return p


def _lerp(a, b, w):
    if isinstance(a, Pose):
        return blend(a, b, w)
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * w for x, y in zip(a, b))
    return a + (b - a) * w


class Track:
    """Keys (time, value, easing into it). Evaluated between neighbouring keys."""

    def __init__(self, keys=None):
        self.keys = []
        for k in keys or []:
            self.key(*k)

    def key(self, t, value, how="inout"):
        self.keys.append((t, value, how))
        self.keys.sort(key=lambda k: k[0])
        return self

    def __call__(self, t):
        ks = self.keys
        if not ks:
            return None
        if t <= ks[0][0]:
            return ks[0][1]
        for (t0, v0, _), (t1, v1, how) in zip(ks, ks[1:]):
            if t <= t1:
                w = ease(how, (t - t0) / (t1 - t0) if t1 > t0 else 1.0)
                return _lerp(v0, v1, w)
        return ks[-1][1]


class Clip:
    """A named clip of `seconds` (at `fps`): a base track of poses plus additive layers."""

    def __init__(self, name, seconds, fps=30, loop=False, frames=None):
        self.name = name
        self.fps = fps
        self.frames = frames if frames is not None else int(round(seconds * fps))
        self.seconds = self.frames / fps
        self.loop = loop
        self.base = Track()
        self.layers = []
        self.post = []                       # callables (t, pose, skel) -> pose, run after layers (IK etc.)
        self.props = {}                      # object name -> callable t -> Matrix (armature space) or None

    def key(self, t, pose, how="inout"):
        self.base.key(t, pose, how)
        return self

    def layer(self, fn):
        self.layers.append(fn)
        return self

    def solve(self, fn):
        self.post.append(fn)
        return self

    def at(self, t, skel=None):
        p = self.base(t)
        p = p.copy() if p is not None else Pose()
        for fn in self.layers:
            d = fn(t)
            if d is not None:
                p = p + d
        for fn in self.post:
            p = fn(t, p, skel) or p
        return p


# -------------------------------------------------------------------------------------- kinematics
class Skeleton:
    """Rest matrices of an armature, and forward kinematics over `Pose`s in armature space."""

    def __init__(self, arm_ob):
        self.ob = arm_ob
        self.bones = {}
        self.order = []
        for b in arm_ob.data.bones:
            self.order.append(b.name)
        # parents before children
        done, ordered = set(), []

        def visit(b):
            if b.name in done:
                return
            if b.parent:
                visit(b.parent)
            done.add(b.name)
            ordered.append(b)

        for b in arm_ob.data.bones:
            visit(b)
        for b in ordered:
            rest = b.matrix_local.copy()
            rel = (b.parent.matrix_local.inverted() @ rest) if b.parent else rest
            self.bones[b.name] = dict(parent=b.parent.name if b.parent else None, rest=rest, rel=rel,
                                      length=b.length)
        self.order = [b.name for b in ordered]

    def has(self, name):
        return name in self.bones

    def local(self, pose: Pose, name):
        q = pose.quat.get(name)
        if q is None:
            r = pose.rot.get(name)
            q = Euler([math.radians(a) for a in r], "XYZ").to_quaternion() if r else Quaternion()
        l = pose.loc.get(name)
        return Matrix.Translation(Vector(l) if l else Vector()) @ q.to_matrix().to_4x4(), q, l

    def fk(self, pose: Pose, upto=None):
        """{bone: posed 4x4 in armature space}. `upto` stops once that bone (and its ancestors) are done."""
        out = {}
        need = None
        if upto is not None:
            need = set()
            n = upto
            while n:
                need.add(n)
                n = self.bones[n]["parent"]
        for name in self.order:
            if need is not None and name not in need:
                continue
            b = self.bones[name]
            L, _, _ = self.local(pose, name)
            par = out[b["parent"]] if b["parent"] else Matrix.Identity(4)
            out[name] = par @ b["rel"] @ L
        return out

    def head(self, pose, name, M=None):
        M = M or self.fk(pose, name)
        return M[name].translation.copy()

    def tail(self, pose, name, M=None):
        M = M or self.fk(pose, name)
        return (M[name] @ Vector((0, self.bones[name]["length"], 0, 1))).to_3d()

    def basis_for(self, pose, name, world_rot: Matrix, M=None):
        """The local quaternion that gives bone `name` the armature-space orientation `world_rot` (3x3),
        given its parent as posed."""
        b = self.bones[name]
        M = M or self.fk(pose, b["parent"]) if b["parent"] else {}
        par = M[b["parent"]] if b["parent"] else Matrix.Identity(4)
        base = (par @ b["rel"]).to_3x3()
        return (base.inverted() @ world_rot).to_quaternion()

    # ---- solvers ----
    def two_bone(self, pose, upper, lower, target, pole, end=None, end_world=None, soften=0.0):
        """Point `upper` and `lower` so `lower`'s tail lands on `target`, bending towards `pole` (a point),
        and optionally give `end` the armature-space orientation `end_world`. Writes quaternions into
        `pose.quat` and returns the pose."""
        M = self.fk(pose, self.bones[upper]["parent"]) if self.bones[upper]["parent"] else {}
        par = M.get(self.bones[upper]["parent"], Matrix.Identity(4))
        a = (par @ self.bones[upper]["rel"]).translation.copy()        # upper's head (location offsets
        lu = self.bones[upper]["length"]                                # on upper ignored)
        ll = self.bones[lower]["length"]
        t = Vector(target)
        d = t - a
        dist = d.length
        reach = (lu + ll) * (0.9995 - soften)
        if dist > reach:
            dist = reach
        dist = max(dist, abs(lu - ll) + 1e-4)
        dn = d.normalized()
        # angle at the upper joint between the target line and the upper bone
        cos_a = (lu * lu + dist * dist - ll * ll) / (2 * lu * dist)
        ang = math.acos(max(-1.0, min(1.0, cos_a)))
        pv = Vector(pole) - a
        bend = (pv - dn * pv.dot(dn))
        if bend.length < 1e-6:
            bend = dn.orthogonal()
        bend.normalize()
        u_dir = (dn * math.cos(ang) + bend * math.sin(ang)).normalized()
        knee = a + u_dir * lu
        l_dir = (a + dn * dist - knee).normalized()
        # Each bone's frame: Y along it; X is the hinge, normal to the bend plane, chosen to keep the
        # bone's rest twist (the rest X projected onto the plane's normal, sign kept).
        hinge = u_dir.cross(bend)
        if hinge.length < 1e-8:
            hinge = u_dir.orthogonal()
        hinge.normalize()

        def frame(name, y, M_par):
            rest = (M_par @ self.bones[name]["rel"]).to_3x3()
            rx = rest.col[0]
            x = hinge if rx.dot(hinge) >= 0 else -hinge
            z = x.cross(y).normalized()
            x = y.cross(z).normalized()
            return Matrix((x, y, z)).transposed()

        Wu = frame(upper, u_dir, par)
        pose.quat[upper] = ((par @ self.bones[upper]["rel"]).to_3x3().inverted() @ Wu).to_quaternion()
        M2 = self.fk(pose, upper)
        Pu = M2[upper]
        Wl = frame(lower, l_dir, Pu)
        pose.quat[lower] = ((Pu @ self.bones[lower]["rel"]).to_3x3().inverted() @ Wl).to_quaternion()
        if end is not None and end_world is not None:
            M3 = self.fk(pose, lower)
            Pl = M3[lower]
            pose.quat[end] = ((Pl @ self.bones[end]["rel"]).to_3x3().inverted() @ end_world).to_quaternion()
        return pose

    def aim(self, pose, name, target, up=(0, 0, 1), weight=1.0):
        """Turn `name` so its Y points at `target` (armature space), its Z leaning to `up`; blended by
        `weight` with whatever rotation the pose already gives it."""
        M = self.fk(pose, name)
        P = M[name]
        h = P.translation
        y = (Vector(target) - h)
        if y.length < 1e-6:
            return pose
        y.normalize()
        u = Vector(up)
        z = (u - y * u.dot(y))
        if z.length < 1e-6:
            z = y.orthogonal()
        z.normalize()
        x = y.cross(z)
        W = Matrix((x, y, z)).transposed()
        par = M[self.bones[name]["parent"]] if self.bones[name]["parent"] else Matrix.Identity(4)
        q = ((par @ self.bones[name]["rel"]).to_3x3().inverted() @ W).to_quaternion()
        _, q0, _ = self.local(pose, name)
        pose.quat[name] = q0.slerp(q, weight) if weight < 1 else q
        return pose


# ------------------------------------------------------------------------------------------ baking
def _fcurves_for(act, slot):
    layer = act.layers[0] if act.layers else act.layers.new("Layer")
    strip = layer.strips[0] if layer.strips else layer.strips.new(type="KEYFRAME")
    bag = strip.channelbag(slot, ensure=True)
    return bag


def _write(bag, path, index, frames, values, group=None):
    fc = bag.fcurves.new(path, index=index)
    if group:
        g = bag.groups.get(group) or bag.groups.new(group)
        fc.group = g
    n = len(frames)
    fc.keyframe_points.add(n)
    co = [0.0] * (2 * n)
    co[0::2] = frames
    co[1::2] = values
    fc.keyframe_points.foreach_set("co", co)
    fc.keyframe_points.foreach_set("interpolation", [1] * n)       # the enum's LINEAR
    fc.update()
    return fc


def bake(clip: Clip, skel: Skeleton, face_ob=None, start=1, props=None, track_suffix="", quiet_bones=None):
    """Bake `clip` onto the skeleton's armature (and the face's shape keys) as NLA tracks named
    clip.name + track_suffix. Bones whose channels never change are not keyed. `props` maps an object to a
    callable t -> world Matrix, for props baked alongside (each gets its own action on the same track
    name). Returns the actions."""
    arm = skel.ob
    # Every clip is baked through its closing frame, a loop included (its last pose is its first again): the
    # exporter turns the strip's length into the animation's duration, so without it a loop came out a
    # frame short, and sampling every other frame (export.glb's frame_step 2) cut a second frame off an odd
    # count. Loops should have an even frame count for the same reason.
    n = clip.frames + 1
    if clip.loop and clip.frames % 2:
        print(f"anim.bake: loop {clip.name} has an odd frame count ({clip.frames}); sampled every other frame "
              "its last frame is dropped")
    frames = [start + i for i in range(n)]
    poses = [clip.at(i / clip.fps, skel) for i in range(n)]
    name = clip.name + track_suffix

    act = bpy.data.actions.new(f"{name}@{arm.name}")
    slot = act.slots.new(id_type="OBJECT", name=arm.name)
    bag = _fcurves_for(act, slot)
    for bn in skel.order:
        quats, locs = [], []
        for p in poses:
            _, q, l = skel.local(p, bn)
            quats.append(q)
            locs.append(l or (0.0, 0.0, 0.0))
        # keep quaternions on one hemisphere so linear interpolation takes the short way round
        for i in range(1, len(quats)):
            if quats[i].dot(quats[i - 1]) < 0:
                quats[i] = -quats[i]
        q_static = all(abs(q.w - 1) < 1e-7 for q in quats)
        l_static = all(abs(c) < 1e-7 for l in locs for c in l)
        if quiet_bones and bn in quiet_bones:
            continue
        path = f'pose.bones["{bn}"]'
        if not q_static:
            for i in range(4):
                _write(bag, path + ".rotation_quaternion", i, frames, [q[i] for q in quats], bn)
        if not l_static:
            for i in range(3):
                _write(bag, path + ".location", i, frames, [l[i] for l in locs], bn)
    _push(arm, act, slot, name, start)
    acts = [act]

    if face_ob is not None and face_ob.data.shape_keys:
        key = face_ob.data.shape_keys
        names = [kb.name for kb in key.key_blocks[1:]]
        used = set(k for p in poses for k in p.face)
        if used:
            fact = bpy.data.actions.new(f"{name}@{face_ob.name}-keys")
            fslot = fact.slots.new(id_type="KEY", name=key.name)
            fbag = _fcurves_for(fact, fslot)
            for kn in names:
                vals = [max(0.0, min(1.0, p.face.get(kn, 0.0))) for p in poses]
                _write(fbag, f'key_blocks["{kn}"].value', 0, frames, vals)
            _push(key, fact, fslot, name, start)
            acts.append(fact)

    for ob, fn in (props or {}).items():
        pact = bpy.data.actions.new(f"{name}@{ob.name}")
        pslot = pact.slots.new(id_type="OBJECT", name=ob.name)
        pbag = _fcurves_for(pact, pslot)
        ob.rotation_mode = "QUATERNION"
        mats = [fn(i / clip.fps) for i in range(n)]
        locs = [m.to_translation() for m in mats]
        quats = [m.to_quaternion() for m in mats]
        scls = [m.to_scale() for m in mats]
        for i in range(1, len(quats)):
            if quats[i].dot(quats[i - 1]) < 0:
                quats[i] = -quats[i]
        for i in range(3):
            _write(pbag, "location", i, frames, [l[i] for l in locs])
            _write(pbag, "scale", i, frames, [s[i] for s in scls])
        for i in range(4):
            _write(pbag, "rotation_quaternion", i, frames, [q[i] for q in quats])
        _push(ob, pact, pslot, name, start)
        acts.append(pact)
    return acts


def _push(idb, act, slot, track_name, start):
    ad = idb.animation_data or idb.animation_data_create()
    track = ad.nla_tracks.new()
    track.name = track_name
    strip = track.strips.new(track_name, start, act)
    strip.name = track_name
    try:
        strip.action_slot = slot
    except (AttributeError, TypeError):
        pass
    track.mute = False
    ad.action = None
    return track


def apply(clip: Clip, skel: Skeleton, t, face_ob=None):
    """Pose the armature (and face) at time t, for stills and previews."""
    p = clip.at(t, skel)
    arm = skel.ob
    for bn in skel.order:
        pb = arm.pose.bones[bn]
        _, q, l = skel.local(p, bn)
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = q
        pb.location = l or (0, 0, 0)
    if face_ob is not None and face_ob.data.shape_keys:
        for kb in face_ob.data.shape_keys.key_blocks[1:]:
            kb.value = max(0.0, min(1.0, p.face.get(kb.name, 0.0)))
    bpy.context.view_layer.update()
    return p
