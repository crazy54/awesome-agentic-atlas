"""End-to-end check of the pipeline on Archie: build, skin, bake a test clip (arm raise, wave, blink, mouth,
look), export a GLB, compress it, and report what came out.

    blender -b --factory-startup --python art/pals/tests/pipeline.py -- <out.glb>
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import archie  # noqa: E402
from kit import anim, export, geo  # noqa: E402
from kit.anim import Clip, Pose  # noqa: E402

out = Path(sys.argv[sys.argv.index("--") + 1])
geo.reset()
R, parts, M = archie.build()
meshes = R.finalize(parts)
skel = anim.Skeleton(R.ob)

rest = Pose(face={"grin": 1.0})
c = Clip("wave", 3.0)
c.key(0.0, rest)
up = rest.copy().side("upper_arm", 1, x=-10, z=95).side("forearm", 1, x=70).side("hand", 1, z=0)
c.key(0.6, up, "back")
c.key(2.3, up, "linear")
c.key(3.0, rest, "inout")
c.layer(lambda t: Pose().side("forearm", 1, z=25 * math.sin(t * 9) * anim.pulse(t, 0.6, 0.2, 1.4, 0.3)))
c.layer(lambda t: Pose().both("lid_up", x=-36 * anim.pulse(t, 1.2, 0.06, 0.04, 0.08)))
c.layer(lambda t: Pose(face={"grin": -anim.pulse(t, 0.8, 0.3, 0.8, 0.3), "oh": anim.pulse(t, 0.8, 0.3, 0.8, 0.3)}))
c.layer(lambda t: Pose().both("eye", z=0).set("eye_L", 0, 0, 18 * anim.pulse(t, 1.6, 0.15, 0.5, 0.2))
        .set("eye_R", 0, 0, 18 * anim.pulse(t, 1.6, 0.15, 0.5, 0.2)))
idle = Clip("idle", 4.0, loop=True)
idle.key(0.0, rest)
idle.layer(lambda t: Pose().set("spine", 2 * math.sin(t * math.tau / 4), 0, 0).set("head", 0, 0, 4 * math.sin(t * math.tau / 4)))
anim.bake(c, skel, meshes["face"])
anim.bake(idle, skel, meshes["face"])
raw = export.glb(out.with_suffix(".raw.glb"), [R.ob, *meshes.values()])
export.compress(raw, out)
print("RAW", raw.stat().st_size, "COMPRESSED", out.stat().st_size)
