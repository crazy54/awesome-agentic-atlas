"""Every prop the pals' gags use (`Bit What happens.md`), each its own small GLB, built from this script.

    blender -b --factory-startup --python art/pals/props.py -- [--only name,name] [--out DIR]
            [--renders DIR] [--samples N] [--res N] [--no-render] [--strips] [--list]

Builders live in props_hand.py (things a hand holds), props_paper.py (signs, sheets, cards, screens),
props_set.py (things that stand, hang or get built), props_holo.py (the Core's holograms, on Archie's own
skeleton) and props_holo_pals.py (holo-zip and holo-brick, on Zip's and Brick's own skeletons); props_kit.py holds the palette, the `Prop` builder, text
and chains. Output: `<out>/<name>.glb`, by default docs/assets/pals/props/, where the stage's `s.prop(name)`
fetches it (compressed with kit.export.compress; the exporter's raw file and the run's manifest stay outside
the repository, in <PALS_HOME>/out/props/), a 600 px Cycles render of each in `<renders>/<name>.png`, and
`<renders>/contact-sheet.png`.
`--strips` also renders each clip of each moving prop at 0, 1/4 .. 4/4 of its length into
`<renders>/strips/<name>.png`, one row per clip, one camera for all of them.

The props are decorative copies: the page's real cursor, buttons and ratings are never touched.

CONVENTIONS (in Blender's frame; the GLB is the same in three.js's Y-up frame: Blender +Z is three.js +Y,
Blender -Y, the front, is three.js +Z).

  * Standing props: origin on the floor under the middle, front facing -Y (towards the page's camera).
  * Hanging props: origin at the hang point (the hook, the string's top), the prop below it.
  * Handheld props: origin at the grip point, built upright: the prop's +Z runs along the fingers and its
    front (-Y) faces away from the palm. Parented to a pal's `grip_L`/`grip_R` bone with an identity
    transform (three.js: `grip.add(prop)`), it sits in the hand pointing where the fingers point. A fist
    closing round a handle (the fishing rod, the stamp, the marker) reads better turned 90 degrees about
    the grip's Z first, so the handle lies across the palm.
  * Moving props are armatures with a `root` bone at the origin; moving parts ride their own bones, named
    with underscores. Clips are glTF animations; each builder's `@prop(rig=...)` names its bones and clips.
    (`PROPS_PARTS=1` prints each prop's heaviest parts, for keeping triangle counts down.)
  * Materials come from one palette (props_kit.SWATCHES). Anything glowing or beam-like is `holo-*` (the
    page may draw it additively); `card-face` and `screen-face` carry placeholder textures and UVs that fill
    the face 0..1, for the page to swap.
  * Rigid moving parts are either parented to their bone (a mesh node per bone, named `<prop>-<bone>`) or
    skinned into one `<prop>-body` mesh, whichever makes the smaller file; a part the page reaches by name
    (a spotlight's `beam`) is its own node either way.

Each builder's `@prop(...)` records the gags it serves, where its origin is and what moves. A run writes
<PALS_HOME>/out/props/props.json (per prop: file, bits, origin, bones, clips with their lengths, node and material names,
triangles, kilobytes) and `--list` prints the same as a Markdown table.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import props_kit as K  # noqa: E402
import props_hand  # noqa: E402,F401  (registers builders)
import props_paper  # noqa: E402,F401
import props_set  # noqa: E402,F401
import props_holo  # noqa: E402,F401
import props_holo_pals  # noqa: E402,F401
from kit import geo  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(flag, default=None):
    if flag in ARGS:
        return ARGS[ARGS.index(flag) + 1]
    return default


def build(name):
    geo.reset()
    p = K.Prop(name)
    K.REGISTRY[name]["fn"](p)
    p.finish()
    return p


def table(manifest):
    """The registry and the last run's manifest as a Markdown table."""
    out = ["| prop | bits | origin / orientation | bones / nodes : clips | tris | KB |", "|---|---|---|---|---|---|"]
    for n, r in K.REGISTRY.items():
        m = manifest.get(n, {})
        nodes = [x for x in m.get("nodes", []) if x != n]
        rig = r.get("rig") or (("nodes: " + ", ".join(nodes)) if nodes else "static")
        out.append(f"| `{n}` | {r['bits']} | {r['origin']} | {rig} | {m.get('tris', '')} | {m.get('kb', '')} |")
    return "\n".join(out)


def main():
    names = list(K.REGISTRY)
    only = opt("--only")
    if only:
        want = [n.strip() for n in only.split(",") if n.strip()]
        bad = [n for n in want if n not in K.REGISTRY]
        if bad:
            raise SystemExit(f"unknown props: {bad}; known: {names}")
        names = want
    out = Path(opt("--out", str(K.SITE_PROPS))).resolve()
    scratch = K.HOME / "out" / "props"                 # outside the repository: the raw exports, the manifest
    mpath = scratch / "props.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    if "--list" in ARGS:
        print(table(manifest))
        return
    renders = Path(opt("--renders", str(K.HOME / "renders/props"))).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (scratch / "raw").mkdir(parents=True, exist_ok=True)
    renders.mkdir(parents=True, exist_ok=True)
    samples = int(opt("--samples", "32"))
    res = int(opt("--res", "600"))
    for n in names:
        t0 = time.time()
        p = build(n)
        bones = [b.name for b in p.R.ob.data.bones] if p.R else []
        dst = p.export(out, scratch / "raw")
        kb = round(dst.stat().st_size / 1024, 1)
        r = K.REGISTRY[n]
        manifest[n] = dict(file=dst.name, bits=r["bits"], origin=r["origin"], rig=r.get("rig", ""), bones=bones,
                           clips={c[0]: dict(seconds=c[1], loop=c[3]) for c in p.clips},
                           nodes=[o.name for o in p.objs],
                           materials=sorted({m.name for o in p.objs if o.type == "MESH" for m in o.data.materials}),
                           tris=p.tris(), kb=kb)
        print(f"PROP {n}: tris={p.tris()} size={kb}KB bones={bones} clips={list(manifest[n]['clips'])}")
        if "--no-render" not in ARGS:
            p.render(renders / f"{n}.png", samples=samples, res=res)
        if "--strips" in ARGS and p.clips:
            frames = renders / "strips" / "frames"
            frames.mkdir(parents=True, exist_ok=True)
            K.strip_sheet(build(n).strip(frames), renders / "strips" / f"{n}.png")
        print(f"PROP {n} done in {time.time() - t0:.1f}s")
    manifest = {n: manifest[n] for n in K.REGISTRY if n in manifest}
    mpath.write_text(json.dumps(manifest, indent=1))
    if "--no-render" not in ARGS:
        K.contact_sheet([renders / f"{n}.png" for n in K.REGISTRY if (renders / f"{n}.png").exists()],
                        renders / "contact-sheet.png")
    print("SUMMARY")
    for n in names:
        m = manifest[n]
        print(f"  {n:22s} {m['tris']:6d} tris {m['kb']:6.1f} KB  bones={','.join(m['bones']) or '-'}  "
              f"clips={','.join(m['clips']) or '-'}")


if __name__ == "__main__":
    main()
