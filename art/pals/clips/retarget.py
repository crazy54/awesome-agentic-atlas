"""Archie's clips on the other pals: each of his poses, as a change from his own REST, put on theirs.

The pals share the kit's skeleton (bone names, and each bone's local frame: Y along the bone, X its bend), so
a bone's turn away from his rest pose means the same on Zip or Brick: an elbow bent ninety degrees from
rest is bent ninety degrees. What differs is the rest itself (where each one's arms hang, his eyelids' travel)
and size, so per frame:

  * every bone the two share takes Archie's local turn relative to his REST, on top of the target's REST
    (the lids' travel scaled to the target's: Archie's upper lid closes at -46, Zip's at -80, Brick's at -30);
  * the hips' offsets are scaled by the ratio of the pals' hip heights;
  * and the feet are planted again by the target's own legs, where Archie's are, scaled the same way, turned
    and rolled as his are -- so a smaller or larger pal keeps his feet on the floor and doesn't skate.

Hands go where the arms take them (no contact is kept), which suits a dance: an L on Archie's forehead is an L
near Brick's.

    clip = retarget(archie_clip, archie_body, target_body, name=None)
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

from kit.anim import Clip, Pose

SIDES = ((1, "_L"), (-1, "_R"))
# eyelid travel to closed, upper and lower, per pal (each base module's AXES)
LIDS = {"archie": (-46.0, 40.0), "zip": (-80.0, 66.0), "brick": (-30.0, 38.0)}


def _rest_quats(body, rest):
    return {n: body.skel.local(rest, n)[1] for n in body.skel.order}


def retarget(src_clip: Clip, src, dst, name=None):
    """A clip for `dst` (a common.Body with `.lib` its base module and `.pal` its name) made from `src`'s
    clip, frame for frame."""
    sk_s, sk_d = src.skel, dst.skel
    rest_s, rest_d = src.lib.REST, dst.lib.REST
    q_rs, q_rd = _rest_quats(src, rest_s), _rest_quats(dst, rest_d)
    shared = [n for n in sk_d.order if sk_s.has(n) and n not in ("root",)]
    scale = dst.hip_z / src.hip_z
    lid_s, lid_d = LIDS[src.pal], LIDS[dst.pal]
    lid_k = {"lid_up": lid_d[0] / lid_s[0], "lid_lo": lid_d[1] / lid_s[1]}
    # where Archie's ankles and feet are at rest, in his own frame
    fk_rest = sk_s.fk(rest_s)
    ank_rest = {sg: fk_rest[f"foot{s}"].translation.copy() for sg, s in SIDES}
    rot_rest = {sg: fk_rest[f"foot{s}"].to_3x3() for sg, s in SIDES}
    c = Clip(name or src_clip.name, src_clip.seconds, fps=src_clip.fps, loop=src_clip.loop, frames=src_clip.frames)
    c.key(0.0, rest_d)

    def solve(t, p0, skel):
        ps = src_clip.at(t, sk_s)
        p = Pose(face=dict(ps.face))
        for n in shared:
            _, q, loc = sk_s.local(ps, n)
            delta = q_rs[n].inverted() @ q
            base = n.rsplit("_", 1)[0] if n.endswith(("_L", "_R")) else n
            if base in lid_k:
                ang = delta.to_euler("XYZ")
                k = lid_k[base]
                delta = Matrix.Rotation(ang.x * k, 4, "X").to_quaternion() @ \
                    Matrix.Rotation(ang.y, 4, "Y").to_quaternion() @ Matrix.Rotation(ang.z, 4, "Z").to_quaternion()
            p.quat[n] = q_rd[n] @ delta
            if loc and n == "hips":
                p.loc[n] = tuple(v * scale for v in loc)
            elif loc:
                p.loc[n] = tuple(loc)
        # the feet: where his are, scaled, turned and rolled as his are
        fk = sk_s.fk(ps)
        for sg, s in SIDES:
            ank = fk[f"foot{s}"].translation
            R = fk[f"foot{s}"].to_3x3() @ rot_rest[sg].inverted()
            e = R.to_euler("ZYX")
            yaw, bank, roll = math.degrees(e.z) * sg, math.degrees(e.y) * sg, math.degrees(e.x)
            # the ankle's offset beyond what the foot's own roll about its ball (or heel) moves it
            rolled, _, _ = src.foot_at(sg, (0, 0, 0), yaw=yaw, roll=roll, bank=bank)
            off = (ank - rolled) * scale
            dst.plant(p, sg, pos=(off.x, off.y, 0.0), lift=max(0.0, off.z), yaw=yaw, roll=roll, bank=bank)
        return p

    c.solve(solve)
    return c
