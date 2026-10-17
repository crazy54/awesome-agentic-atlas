"""The dance party: all three pals doing Archie's dances side by side, rendered to video (Eevee).

    blender -b --factory-startup --python art/pals/clips/party.py -- [--dances floss,robot] [--secs 8]
            [--res 1280x720] [--out DIR] [--stills]

Archie dances his own clips (clips/archie_base.py); Zip and Brick dance the same ones put onto them by
clips/retarget.py. Zip is on Archie's right (the camera's left), Brick on his left, all facing the camera,
each dance from its start for `--secs` (all of it with --secs 0). Writes <out>/party-<dance>.mp4, or with
--stills one PNG a dance, a third of the way in.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "clips"))
from kit import anim, geo, mat, studio  # noqa: E402
import common  # noqa: E402
from retarget import retarget  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    return ARGS[ARGS.index(flag) + 1] if flag in ARGS else default


OUT = Path(opt("--out", "E:/Development Workspaces/Archie and Pals/renders/party")).resolve()
OUT.mkdir(parents=True, exist_ok=True)
RES = tuple(int(v) for v in opt("--res", "1280x720").split("x"))
SECS = float(opt("--secs", "8"))
PLACES = {"zip": -2.05, "archie": 0.0, "brick": 2.55}          # metres across, camera's left to right

geo.reset()
pals = {}
for pal in ("archie", "zip", "brick"):
    mod = importlib.import_module(pal)
    R, parts, M = mod.build()
    meshes = R.finalize(parts)
    skel = anim.Skeleton(R.ob)
    lib = importlib.import_module(f"{pal}_base")
    body = common.Body(skel, **getattr(lib, "BODY", {}))
    body.lib, body.pal = lib, pal
    R.ob.location.x = PLACES[pal]
    pals[pal] = dict(R=R, skel=skel, body=body, face=meshes.get("face"))

archie = pals["archie"]
CLIPS = archie["body"].lib.clips(archie["body"])
names = opt("--dances", ",".join(archie["body"].lib.DANCES)).split(",")

focus = Vector((0.25, 0, 1.3))
studio.sheet_lights(focus, 1.6)
fl = studio.floor(0.0)
fl.is_shadow_catcher = False
fl.data.materials.append(mat.principled("floor", "#77787c", rough=0.8))
studio.settings(res=RES, samples=16, engine="EEVEE", view="Standard", exposure=-0.9)
studio.camera("cam", focus, 0, 11.5, lens=50)


def clear(ob):
    if ob is not None and ob.animation_data:
        for tr in list(ob.animation_data.nla_tracks):
            ob.animation_data.nla_tracks.remove(tr)
        ob.animation_data.action = None


sc = bpy.context.scene
for name in names:
    src = CLIPS[name]
    longest = 0
    for pal, P in pals.items():
        clip = src if pal == "archie" else retarget(src, archie["body"], P["body"])
        clear(P["R"].ob)
        clear(P["face"].data.shape_keys if P["face"] is not None and P["face"].data.shape_keys else None)
        if "--stills" in ARGS:
            anim.apply(clip, P["skel"], src.seconds / 3, P["face"])
        else:
            anim.bake(clip, P["skel"], P["face"])
        longest = max(longest, clip.frames)
    if "--stills" in ARGS:
        studio.render(OUT / f"party-{name}.png")
        print("STILL", name)
        continue
    sc.render.fps = src.fps
    if hasattr(sc.render.image_settings, "media_type"):
        sc.render.image_settings.media_type = "VIDEO"
    sc.render.image_settings.file_format = "FFMPEG"
    sc.render.ffmpeg.format = "MPEG4"
    sc.render.ffmpeg.codec = "H264"
    sc.render.ffmpeg.constant_rate_factor = "HIGH"
    sc.frame_start = 1
    sc.frame_end = longest if SECS <= 0 else min(longest, int(SECS * src.fps))
    sc.render.filepath = str(OUT / f"party-{name}.mp4")
    bpy.ops.render.render(animation=True)
    print("VIDEO", name, OUT / f"party-{name}.mp4")
