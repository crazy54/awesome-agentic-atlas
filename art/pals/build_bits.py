"""Bake the bits: each pal's pieces of each bit, into the small clip files the page fetches before a bit plays.

    blender -b --factory-startup --python art/pals/build_bits.py -- [--only bit,bit] [--pal archie]
            [--out DIR] [--keep-raw]

For every bit module in art/pals/bits/ and every pal in its cast, writes
docs/assets/pals/bits/<bit>@<pal>.glb: the pal's skeleton and face mesh (the face carries the shape keys the
clips animate) and only that bit's clips, meshopt-compressed. The models themselves are not in these files;
the page plays the clips on the models it already has, by bone name.
"""
from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "clips"))
from kit import anim, export, geo, proxy  # noqa: E402
import bits as B  # noqa: E402
import common  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    return ARGS[ARGS.index(flag) + 1] if flag in ARGS else default


OUT = Path(opt("--out", str(ROOT / "docs" / "assets" / "pals" / "bits")))


def clear_tracks(*ids):
    for idb in ids:
        if idb is not None and idb.animation_data:
            for tr in list(idb.animation_data.nla_tracks):
                idb.animation_data.nla_tracks.remove(tr)
            idb.animation_data.action = None


def main():
    t0 = time.time()
    bits = B.all_bits()
    only = opt("--only")
    if only:
        bits = {k: v for k, v in bits.items() if k in only.split(",")}
    pals = sorted({p for b in bits.values() for p in b.CAST})
    if opt("--pal"):
        pals = [p for p in pals if p == opt("--pal")]
    OUT.mkdir(parents=True, exist_ok=True)
    for pal in pals:
        geo.reset()
        mod = importlib.import_module(pal)
        R, parts, M = mod.build()
        meshes = R.finalize(parts)
        skel = anim.Skeleton(R.ob)
        lib = importlib.import_module(f"{pal}_base")
        body = common.Body(skel, **getattr(lib, "BODY", {}))
        body.lib = lib
        face = meshes.get("face")
        for name, bit in bits.items():
            if pal not in bit.CAST:
                continue
            bodies = {pal: body}
            made = bit.clips(bodies).get(pal, [])
            if not made:
                continue
            clear_tracks(R.ob)
            stand = proxy.StandIn(face) if face else None
            for c in made:
                anim.bake(c, skel, stand.ob if stand else None)
            for ob in (R.ob, stand.ob if stand else None):
                if ob is not None and ob.animation_data:
                    ob.animation_data.action = None
            dest = OUT / f"{name}@{pal}.glb"
            raw = dest.with_suffix(".raw.glb")
            export.glb(raw, [R.ob] + ([stand.ob] if stand else []), frame_step=2)
            if stand:
                stand.restore()
            export.compress(raw, dest, tolerance=0.001)
            if "--keep-raw" not in ARGS:
                raw.unlink()
            print(f"BIT {name}@{pal}: {len(made)} clips, {dest.stat().st_size:,} bytes")
    print(f"done in {time.time() - t0:.0f}s")


main()
