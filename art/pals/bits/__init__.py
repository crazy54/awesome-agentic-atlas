"""The bits: the pals' gags, as clips. One module per bit, each with

    NAME = "heavy-readme"            # the bit's name, as archie-bits.js knows it
    CAST = ("archie", "brick")       # who is in it
    def clips(bodies) -> {pal: [Clip, ...]}

`bodies` maps each pal of the cast to its `clips.common.Body` (and `bodies[pal].lib` to that pal's base clip
module, for its REST pose and helpers). Every clip is named "<bit>/<segment>" and is a piece the page
strings together: the page walks the pals between the places a bit happens (the README's edge, the theme
switch), and plays these pieces where they stand. A piece that two pals play together is written for both in
the same space, with each pal's root where the page will stand him (the bit's `FORMATION`, metres, x across
and y towards the back, from the bit's origin), so a hand-off lines up.

Pieces start and end on the pal's REST pose unless they say otherwise; a held piece (`.../hold`) loops.

`build_bits.py` bakes every bit into docs/assets/pals/bits/<bit>@<pal>.glb: the pal's skeleton and face
with only that bit's clips, fetched by the page when the bit is about to play.
"""
import importlib
import pkgutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def all_bits():
    out = {}
    for m in pkgutil.iter_modules([str(HERE)]):
        if m.name.startswith("_"):
            continue
        mod = importlib.import_module(f"bits.{m.name}")
        if hasattr(mod, "NAME"):
            out[mod.NAME] = mod
    return out
