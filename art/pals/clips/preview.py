"""Contact strips of a pal's clips, for checking poses and timing by eye (Eevee, quick).

    blender -b --factory-startup --python art/pals/clips/preview.py -- <pal> <clip>[,<clip>...]
            [--times 0,0.5,1.0 | --every 0.25] [--out DIR] [--res 360x480] [--view three|front|side|back]
            [--video]  (an MP4 of each clip instead of a strip)

`<pal>` is a module in art/pals (archie, zip, brick) and its clips come from `clips/<pal>_base.py`'s
`clips(body)` (and `clips/bits_*.py` once they exist).
"""
from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "clips"))
from kit import anim, geo, studio  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:]
pal, names = ARGS[0], ARGS[1].split(",")


def opt(flag, default=None):
    return ARGS[ARGS.index(flag) + 1] if flag in ARGS else default


out = Path(opt("--out", rf"E:/Development Workspaces/Archie and Pals/renders/clips/{pal}")).resolve()
out.mkdir(parents=True, exist_ok=True)
res = tuple(int(v) for v in opt("--res", "360x480").split("x"))
view = opt("--view", "three")

mod = importlib.import_module(pal)
geo.reset()
R, parts, M = mod.build()
meshes = R.finalize(parts)
skel = anim.Skeleton(R.ob)
lib = importlib.import_module(f"{pal}_base")
import common  # noqa: E402

body = common.Body(skel, **getattr(lib, "BODY", {}))
body.lib = lib
CLIPS = lib.clips(body)
# A bit's pieces, by "<bit>/<piece>": load that bit's module and add its clips for this pal.
import bits as _bits  # noqa: E402
_all = None
for n in names:
    if "/" in n and n not in CLIPS:
        _all = _all or _bits.all_bits()
        mod = _all[n.split("/")[0]]
        for c in mod.clips({pal: body}).get(pal, []):
            CLIPS[c.name] = c

H = {"archie": 2.4, "zip": 2.0, "brick": 2.8}.get(pal, 2.4)
focus = Vector((0, 0, H * 0.5))
studio.sheet_lights(focus, 1.0)
fl = studio.floor(0.0)
fl.is_shadow_catcher = False                  # Eevee has no shadow catcher: a plain grey floor instead
from kit import mat  # noqa: E402
fl.data.materials.append(mat.principled("floor", "#77787c", rough=0.8))
studio.settings(res=res, samples=16, engine="EEVEE", view="Standard", exposure=-0.9)
if view == "face":
    hz = {"archie": 1.98, "zip": 1.45, "brick": 2.45}.get(pal, 1.98)
    cam = studio.camera("cam", Vector((0, 0, hz)), 8, H * 1.1, lens=85)
else:
    ang = {"three": 30, "front": 0, "side": -90, "back": 180, "left": 90}[view]
    cam = studio.camera("cam", focus, ang, H * 2.5, lens=50)

face = meshes.get("face")
for name in names:
    c = CLIPS[name]
    if "--video" in ARGS:
        sc = bpy.context.scene
        sc.render.fps = c.fps
        if hasattr(sc.render.image_settings, "media_type"):
            sc.render.image_settings.media_type = "VIDEO"     # Blender 5: video is a media type, then FFMPEG
        sc.render.image_settings.file_format = "FFMPEG"
        sc.render.ffmpeg.format = "MPEG4"
        sc.render.ffmpeg.codec = "H264"
        sc.render.ffmpeg.constant_rate_factor = "MEDIUM"
        anim.bake(c, skel, face)
        sc.frame_start, sc.frame_end = 1, c.frames
        sc.render.filepath = str(out / f"{name.replace('/', '__')}.mp4")
        bpy.ops.render.render(animation=True)
        print("VIDEO", out / f"{name}.mp4")
        continue
    if opt("--times"):
        times = [float(x) for x in opt("--times").split(",")]
    else:
        step = float(opt("--every", str(max(0.2, round(c.seconds / 8, 2)))))
        times = [round(i * step, 3) for i in range(int(c.seconds / step) + 1)]
    files = []
    for t in times:
        anim.apply(c, skel, t, face)
        f = out / f"{name.replace('/', '__')}-{t:06.2f}.png"
        studio.render(f)
        files.append(str(f))
    print("STRIP", name, "|".join(files))
