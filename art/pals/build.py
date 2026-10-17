"""Build a pal for the site: the model, every clip baked onto it, the GLB the page loads, and (for Archie)
the poster the page shows before, or instead of, the live model.

    blender -b --factory-startup --python art/pals/build.py -- archie [--only idle,walk] [--no-poster]
            [--out DIR] [--keep-raw]

Archie writes `docs/assets/archie.glb` and `docs/assets/archie-3d.webp`, the files the homepage's
`archie.js` has always loaded, so the swap needs no new wiring. Zip and Brick write
`docs/assets/pals/<pal>.glb`.

The poster is the idle's first frame through the banner's own camera (archie.js `start()`; Blender's
(0.9, -6.2, 1.55) aimed at z 1.08, a 70 mm lens), square at twice the banner slot's 240 CSS px, so the poster
and the first live frame are the same picture and the swap between them does not jump.
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "clips"))
from kit import anim, export, geo, proxy, studio  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
pal = ARGS[0] if ARGS else "archie"


def opt(flag, default=None):
    return ARGS[ARGS.index(flag) + 1] if flag in ARGS else default


ASSETS = ROOT / "docs" / "assets"
GLB = Path(opt("--out", str(ASSETS))) / ("archie.glb" if pal == "archie" else f"pals/{pal}.glb")
POSTER = ASSETS / "archie-3d.webp"


def clear_tracks(*ids):
    for idb in ids:
        if idb is not None and idb.animation_data:
            for tr in list(idb.animation_data.nla_tracks):
                idb.animation_data.nla_tracks.remove(tr)
            idb.animation_data.action = None


def main():
    t0 = time.time()
    mod = importlib.import_module(pal)
    geo.reset()
    R, parts, M = mod.build()
    meshes = R.finalize(parts)
    skel = anim.Skeleton(R.ob)
    lib = importlib.import_module(f"{pal}_base")
    import common  # noqa: E402
    body = common.Body(skel, **getattr(lib, "BODY", {}))
    clips = lib.clips(body)
    face = meshes.get("face")
    # A pal's clips go out in packs: the first carries the model and its everyday clips; the others carry
    # only the skeleton and the face (whose shape keys the clips animate), for clips fetched when needed.
    packs = getattr(lib, "PACKS", None) or {pal: [n for n in clips if n != "calibrate"]}
    only = opt("--only")
    first = True
    for pack, members in packs.items():
        clear_tracks(R.ob, face.data.shape_keys if face else None)
        names = [n for n in members if not only or n in only.split(",")]
        # The packs after the first carry a stand-in for the face (kit/proxy.py), not the face itself.
        stand = proxy.StandIn(face) if (face and not first) else None
        for n in names:
            t = time.time()
            anim.bake(clips[n], skel, stand.ob if stand else face)
            print(f"baked {n}: {clips[n].frames} frames in {time.time() - t:.1f}s")
        if first and "idle" in clips:
            anim.apply(clips["idle"], skel, 0.0, face)
            if pal == "archie" and "--no-poster" not in ARGS:
                poster()
        for ob in (R.ob, face, stand.ob if stand else None):
            if ob is not None and ob.animation_data:
                ob.animation_data.action = None
        dest = GLB if first else GLB.with_name(f"{pack}.glb")
        raw = dest.with_suffix(".raw.glb")
        objs = [R.ob, *meshes.values()] if first else [R.ob] + ([stand.ob] if stand else [])
        export.glb(raw, objs, frame_step=int(opt("--step", "2")))
        if stand:
            stand.restore()
        export.compress(raw, dest, tolerance=float(opt("--tolerance", "0.001")))
        if "--keep-raw" not in ARGS:
            raw.unlink()
        print(f"BUILT {dest} ({dest.stat().st_size:,} bytes), {len(names)} clips")
        first = False
    print(f"done in {time.time() - t0:.0f}s")


def poster():
    sc = bpy.context.scene
    studio.site_camera()
    studio.site_lights()
    studio.settings(res=(480, 480), samples=64, engine="CYCLES", transparent=True, view="Standard")
    sc.render.image_settings.file_format = "WEBP"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.image_settings.quality = 82
    for ob in list(sc.objects):
        if ob.type == "MESH" and ob.name == "floor":
            bpy.data.objects.remove(ob)
    studio.render(POSTER)
    print("poster", POSTER)


main()
