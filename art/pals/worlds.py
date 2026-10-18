"""The miniature worlds the Atlas Core projects, one per part of the site: built, animated and exported from
this script, one small GLB each, which the page projects over the Core (docs/assets/archie-core.js,
archie-stage.js `project()`).

    blender -b --factory-startup --python art/pals/worlds.py -- [--only slug,...] [--out DIR] [--raw DIR]
            [--renders DIR] [--samples N] [--no-render] [--strip]

The GLBs go to docs/assets/pals/worlds/<slug>.glb (`--out`), Blender's raw exports to the scratch folder's
out/worlds-raw (`--raw`, outside the repository), the renders to its renders/worlds (one per world and a
contact sheet). `--strip` adds rows of stills under renders/worlds/strips: <slug>-entrance (appear, idle) and
<slug>-gags (scatter, gather, tilt, level), and holo-bot-clips.

The reference is the right-hand column and the hero of `Archie's unfolding Atlas Core.png` (outside the
repository, with the other sheets): solid low-poly islands with grass tops and rocky undersides, tiny trees,
and cyan hologram structures, arcs and rings, light falling from under the islands to the disc. Each topic's
world adds its family's accent (`worlds_kit.FAMILY`) and a joke you can read at the size of a thumbnail.

UNIT SPACE. A disc of radius 1 at Z = 0 (three.js Y = 0), +Y at the back, the reader in front (three.js +Z).
Every clip but scatter and gather stays inside radius 1 and below 1.3; scatter blows islands up to about 1.25
out.

NODES. The root is `world_<slug>` (hyphens as underscores), then

    stage                 tilt and level turn it, hinged on the disc's rim (worlds_kit.TILT_HINGE)
      island_main         the biggest island (the middle one, in every world that has one)
      island_1 .. n       the others, numbered round from the reader's side (-Y) counter-clockwise seen
                          from above: island_1 is the first one right of straight ahead
      holograms           scatter and gather blink it out and in
        arcs, rings, glints, floating cards ...   the holograms that belong to no island

and everything else rides on its island: bots (`<name>`, with `<name>_arm_L` / `_R`), props, the holograms
standing on it. home's satellites, in that order: island_1 data, island_2 extend, island_3 build, island_4
run, island_5 connect, island_6 trust. Every build prints each world's islands as `ISLANDS slug: new=old`.
Empties named `anchor_*` are spots the page can use: `anchor_centre` in most worlds, `anchor_stage`
(creative-voice-media's clear stage), `anchor_dj`, `anchor_dancefloor`, `anchor_bouncer` (rave), `anchor_gate`
(no-archies).

CLIPS. Six in every world; play the one-shots once, held at their end (as archie-stage.js `play` does):

    appear   0.8 s  the islands pop up from the disc, the holograms flicker on; ends on idle's first frame
    idle     4.0 s  the loop
    scatter  1.0 s  every island blown out from the middle, tumbling, and held there; the holograms go out
    gather   1.2 s  from where scatter ends, back home with a little overshoot, the holograms back on; ends
                    on idle's first frame
    tilt     0.8 s  the whole stage lurches a few degrees off level and stays tipped
    level    0.6 s  from where tilt ends, back down level with a bump; ends on idle's first frame

idle's first frame is also every node's rest pose, so a hard switch between clips never jumps. MATERIALS:
`solid` / `solid_metal` (vertex colours), and the holograms, every one named `holo_*`, which the page draws as
additive light. holo-bot.glb (worlds_holo_bot.py) is a tiny projected agent for the Core's escapee and
rebellion bits.
"""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from mathutils import Matrix

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from kit.geo import TAU, V  # noqa: E402
import worlds_kit as wk  # noqa: E402
from worlds_kit import (IDLE_S, WORLDS, along, arc, arc_pts, ball, beam, blink, bob, bot, box, bush, chain,  # noqa: E402
                        drip, ease, flat_ring, glint, hop, ico, island, isle_node, polar, prism, quad, rock, sat,
                        scatter, shuttle, slab, spin, spire, swing, text, throb, torus, tree, tube, world)
from worlds_topics import rad, rings, rx, ry, rz, smooth01, speaker  # noqa: E402  (and registers the topics)
import worlds_holo_bot  # noqa: E402,F401  (registers holo-bot)

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
SCRATCH = Path("E:/Development Workspaces/Archie and Pals")
SITE = HERE.parent.parent / "docs" / "assets" / "pals" / "worlds"


def opt(flag, default=None):
    if flag in ARGS:
        return ARGS[ARGS.index(flag) + 1]
    return default


# ============================================================================================== home
@world("home")
def home(W):
    """The whole atlas: the hero of the sheet. A crystal city on the central island, a satellite for each
    family with a beacon in its accent, arcs of light from the city out to every one."""
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.4, 0.36, depth=0.27, sides=13, seed=3)
    with W.on("isle_centre"):
        prism("stone", C.at(0, 0, -0.004), 0.2, 0.022, n=12)
        scatter(C, 5, seed=4, avoid=lambda x, y: math.hypot(x - C.x, y - C.y) < 0.24, companions=0.25)
        bush(C.at(0.26, -0.22), seed=5)
    base = C.at(0, 0, 0.018)
    W.node("city", base, parent="isle_centre", kind="holo")
    with W.on("city"):
        spire("holo_cyan", base, 0.046, 0.74, tip=0.2)
        rng = random.Random(8)
        for k, (a, d, h, r) in enumerate([(20, 0.085, 0.42, 0.03), (150, 0.08, 0.36, 0.028),
                                          (260, 0.09, 0.3, 0.027), (80, 0.1, 0.26, 0.024),
                                          (330, 0.14, 0.2, 0.022), (205, 0.14, 0.22, 0.022),
                                          (110, 0.15, 0.16, 0.02), (290, 0.155, 0.15, 0.02)]):
            spire("holo_cyan", base + polar(a, d), r, h, n=6 if k % 2 else 4, tip=rng.uniform(0.15, 0.3))
        beam(C, r=0.05)
    W.node("halo", C.at(0, 0, 0.56), parent="isle_centre", kind="holo", idle=chain(bob(0.04, 4.0), spin(1)))
    with W.on("halo"):
        flat_ring("holo_lime", C.at(0, 0, 0.56), 0.11, 0.008, segs=24, dashes=12, duty=0.7)
    order = [("run", 120, 0.6), ("build", 60, 0.6), ("extend", 0, 0.46), ("data", 300, 0.34),
             ("trust", 240, 0.34), ("connect", 180, 0.46)]
    W.node("arcs", (0, 0, 0.006), kind="holo")
    with W.on("arcs"):
        flat_ring("holo_lime", (0, 0, 0.006), 0.56, 0.006, segs=48)
    for k, (fam, a, z) in enumerate(order):
        p = polar(a, 0.75)
        S = isle_node(W, f"isle_{fam}", p.x, p.y, 0.16, z, depth=0.2, sides=9, seed=20 + k)
        with W.on(f"isle_{fam}"):
            scatter(S, 2, seed=30 + k, ring_=(0.5, 0.8), h=(0.06, 0.09),
                    avoid=lambda x, y, S=S: math.hypot(x - S.x, y - S.y) < 0.05)
            spire(wk.accent(fam), S.at(0, 0, 0.016), 0.024, 0.2, tip=0.3)
            flat_ring(wk.accent(fam), S.at(0, 0, 0.02), 0.045, 0.006, segs=16)
            drip(S, 2, seed=k, m=wk.accent(fam), length=0.06)
        a_ = base + (p - C.at()).normalized() * 0.05 + V(0, 0, 0.36)
        b_ = S.at(0, 0, 0.15)
        h = 0.16 + 0.05 * (z < 0.4)
        with W.on("arcs"):
            arc(a_, b_, h)
        glint(W, f"glint_{fam}", arc_pts(a_, b_, h, 8), period=2.0, phase=k / 6)
    W.node("rings", (0, 0, 0.012), kind="holo", idle=spin(2 / 36), cyclic=False)
    with W.on("rings"):
        flat_ring("holo_lime", (0, 0, 0.012), 0.95, 0.008, dashes=36, duty=0.55)
    W.anchor("anchor_centre", C.at(0, 0, 0.02), parent="isle_centre")


# ========================================================================================== discover
@world("discover")
def discover(W):
    """Today's picks: cards riding a Ferris wheel over the central island, coming round in turn, and a
    ticket booth on the island next door."""
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.36, 0.3, sides=12, seed=191)
    ax = C.at(0, 0.0, 0.45)
    R = 0.27
    with W.on("isle_centre"):
        scatter(C, 6, seed=192, ring_=(0.7, 0.9))
        for sy in (-1, 1):
            for sx in (-1, 1):
                tube("metal", [C.at(sx * 0.17, sy * 0.06), ax + V(0, sy * 0.025, 0)], 0.008, sides=5)
            box("metal", C.at(0, sy * 0.06, 0.12), (0.2, 0.008, 0.008))
        prism("stone", C.at(0, 0, -0.004), 0.22, 0.014, n=12, ry=0.12)
    W.node("wheel", ax, parent="isle_centre", kind="holo", idle=lambda t: ry(-180 * t / IDLE_S), cyclic=False)
    with W.on("wheel"):
        torus("holo_lime", ax, R, 0.006, rot=(90, 0, 0), segs=32, sides=4)
        torus("holo_cyan", ax, R * 0.55, 0.004, rot=(90, 0, 0), segs=24, sides=3)
        for k in range(8):
            a = TAU * k / 8
            tube("holo_cyan", [ax, ax + V(R * math.cos(a), 0, R * math.sin(a))], 0.003, sides=3)
        ball("graphite", ax, 0.02, segs=8, rings=4)
    colours = ["mint", "blue", "yellow", "red"]           # the pattern repeats every 4, so half a turn loops
    for k in range(8):
        a = TAU * k / 8
        pv = ax + V(R * math.cos(a), -0.02, R * math.sin(a))
        W.node(f"card_{k + 1}", pv, parent="wheel", idle=lambda t: ry(180 * t / IDLE_S), cyclic=False)
        with W.on(f"card_{k + 1}"):
            box("graphite", pv + V(0, 0, -0.012), (0.006, 0.006, 0.024))
            c = pv + V(0, -0.004, -0.07)
            box("paper", c, (0.075, 0.006, 0.095))
            box(colours[k % 4], c + V(0, -0.0035, 0.032), (0.065, 0.002, 0.022))
            for j in range(2):
                box("stone", c + V(-0.008 * j, -0.0035, -0.002 - 0.02 * j), (0.05 - 0.016 * j, 0.002, 0.007))
            box("yellow", c + V(0.026, -0.0035, -0.034), (0.012, 0.002, 0.012), rot=(0, 45, 0))
    # the ticket booth
    S = sat(W, "isle_booth", 330, 0.7, 0.17, 0.36, seed=193, trees=1, clear=0.1, drip_m="holo_lime")
    bb = S.at(0.0, 0.0)
    with W.on("isle_booth"):
        box("cream", bb + V(0, 0, 0.045), (0.09, 0.07, 0.09))
        for k in range(5):
            box("red" if k % 2 else "white", bb + V(-0.045 + 0.09 * (k + 0.5) / 5, -0.01, 0.1), (0.018, 0.1, 0.008),
                rot=(-15, 0, 0))
        box("graphite", bb + V(0, -0.036, 0.05), (0.05, 0.004, 0.035))
        box("cream", bb + V(0, -0.02, 0.15), (0.11, 0.008, 0.04))
        text("TODAY", "red", bb + V(0, -0.025, 0.15), 0.026)
    P = sat(W, "isle_grove", 150, 0.68, 0.16, 0.54, seed=194, trees=3, drip_m="holo_lime")
    sp = P.at(0, 0, 0.2)
    W.node("star", sp, parent="isle_grove", kind="holo", idle=chain(bob(0.015, 2.0), spin(1)))
    with W.on("star"):
        pts = []
        for k in range(10):
            r = 0.045 if k % 2 == 0 else 0.018
            a = math.pi / 2 + TAU * k / 10
            pts.append((r * math.cos(a), r * math.sin(a)))
        slab("holo_lime", sp + V(0, 0.005, 0), pts, 0.01, rot=(90, 0, 0))
    rings(W, "holo_lime")
    W.anchor("anchor_centre", C.at(0, -0.2, 0.01), parent="isle_centre")


# ======================================================================================= collections
@world("collections")
def collections(W):
    """A shelf island: cubbies of labelled kits, one box coming in to land in the empty slot, and an agent
    carrying another one over."""
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.42, 0.3, sides=12, seed=201)
    sh = C.at(0.0, 0.1)
    w, h, d, t = 0.44, 0.34, 0.11, 0.014
    cols, rows = 3, 2
    cw, chh = (w - t) / cols, (h - t) / rows
    with W.on("isle_centre"):
        scatter(C, 5, seed=202, ring_=(0.78, 0.93), arc=(190, 350))
        box("trunk", sh + V(0, d / 2 - 0.004, h / 2), (w, 0.008, h))
        for k in range(cols + 1):
            box("wood", sh + V(-w / 2 + t / 2 + k * cw, 0, h / 2), (t, d, h))
        for k in range(rows + 1):
            box("wood", sh + V(0, 0, t / 2 + k * chh), (w, d, t))
        labels = ["mint", "blue", "violet", "yellow", "red", None]
        for k, lab in enumerate(labels):
            if lab is None:
                continue
            cx = sh.x - w / 2 + t + cw * (k % cols + 0.5) - t / 2
            cz = sh.z + t + chh * (k // cols) + 0.003
            bw, bh = cw * 0.78, chh * 0.7
            box("cardboard", V(cx, sh.y - 0.005, cz + bh / 2), (bw, d * 0.8, bh))
            box("sand", V(cx, sh.y - 0.005, cz + bh + 0.001), (bw * 0.25, d * 0.8, 0.003))
            box(lab, V(cx, sh.y - d * 0.4 - 0.006, cz + bh * 0.55), (bw * 0.6, 0.003, bh * 0.35))
        text("KITS", "graphite", sh + V(0, -d / 2 - 0.003, h + 0.04), 0.05)
        box("cream", sh + V(0, -d / 2 + 0.002, h + 0.04), (0.16, 0.006, 0.06))
    # the last box, coming in to land in the empty cubby
    cx = sh.x - w / 2 + t + cw * (2 + 0.5) - t / 2
    cz = sh.z + t + chh + 0.003
    bw, bh = cw * 0.78, chh * 0.7
    home = V(cx, sh.y - 0.005, cz + bh / 2)
    away = [home + V(0.0, -0.3, 0.2), home + V(0, -0.22, 0.02), home]
    W.node("incoming", away[0], parent="isle_centre", idle=shuttle(away, away[0], (0.3, 1.6), (2.9, 3.8)))
    with W.on("incoming"):
        box("cardboard", away[0], (bw, d * 0.8, bh))
        box("sand", away[0] + V(0, 0, bh / 2 + 0.001), (bw * 0.25, d * 0.8, 0.003))
        box("mint", away[0] + V(0, -d * 0.4 - 0.002, bh * 0.05), (bw * 0.6, 0.003, bh * 0.35))
    W.node("tag", away[0] + V(0, 0, bh / 2 + 0.05), parent="incoming", kind="holo", idle=bob(0.008, 1.0))
    with W.on("tag"):
        text("NEW", "holo_lime", away[0] + V(0, 0, bh / 2 + 0.05), 0.03)
    # the stack and the courier
    S = sat(W, "isle_stack", 330, 0.7, 0.18, 0.36, seed=203, trees=1, clear=0.12, drip_m="holo_lime")
    with W.on("isle_stack"):
        for k, (dx, dy, m) in enumerate([(-0.04, 0.02, "red"), (0.03, 0.03, "blue"), (0.0, 0.01, "yellow")]):
            z = 0.025 if k < 2 else 0.075
            b = S.at(dx, dy, z)
            box("cardboard", b, (0.06, 0.06, 0.05), rot=(0, 0, 10 * k))
            box(m, b + wk.rot3((0, 0, 10 * k)) @ V(0, -0.031, 0.0), (0.035, 0.003, 0.02), rot=(0, 0, 10 * k))
    P = sat(W, "isle_courier", 150, 0.68, 0.17, 0.52, seed=204, trees=2, clear=0.1, drip_m="holo_lime")
    route = [P.at(-0.06, -0.02), P.at(0.06, -0.03)]
    W.node("courier", route[0], parent="isle_courier",
           idle=chain(shuttle(route, route[0], (0.2, 1.8), (2.2, 3.8)), hop(0.006, 0.0, 0.4, 0.2)))
    bot(W, "courier_bot", route[0], face=60, s=0.9, tip="holo_lime", parent="courier",
        arms=(lambda t: rx(-80), lambda t: rx(-80)))
    with W.on("courier_bot"):
        b = route[0] + wk.rot3((0, 0, 60)) @ V(0, -0.06, 0.07)
        box("cardboard", b, (0.06, 0.05, 0.045), rot=(0, 0, 60))
        box("violet", b + wk.rot3((0, 0, 60)) @ V(0, -0.026, 0), (0.035, 0.003, 0.018), rot=(0, 0, 60))
    rings(W, "holo_lime")
    W.anchor("anchor_centre", C.at(0, -0.15, 0.01), parent="isle_centre")


# ============================================================================================== lost
@world("lost")
def lost(W):
    """The 404 page: one small island, adrift, with a signpost whose every arrow says `?` (one says 404),
    and a little agent turning round and round, scratching its head."""
    loop = [V(0.06 * math.cos(a), 0.04 * math.sin(a), 0.42 + 0.015 * math.sin(2 * a)) for a in
            [TAU * k / 16 for k in range(16)]]
    W.node("isle", loop[0], kind="island", idle=chain(along(loop, loop[0], 4.0),
                                                       lambda t: rx(3 * math.sin(TAU * t / 4.0)) @
                                                       ry(4 * math.cos(TAU * t / 4.0))))
    with W.on("isle"):
        I = island(loop[0].x, loop[0].y, 0.32, loop[0].z, depth=0.32, sides=11, seed=211)
        drip(I, 3, seed=5, m="holo_cyan", length=0.12)
        tree(I.at(0.19, 0.1), 0.15, "round", seed=3)
        tree(I.at(-0.2, 0.12), 0.11, "pine", seed=4)
        bush(I.at(-0.2, -0.04), 0.026, seed=2)
        rock(I.at(0.15, -0.16), 0.03, seed=3)
        rock(I.at(-0.22, -0.12), 0.022, seed=4)
        sp = I.at(-0.05, 0.05)
    with W.on("isle"), wk.scaled(1.35, sp):
        prism("wood", sp, 0.01, 0.3, n=6)
        for k, (hd, z, word) in enumerate([(-20, 0.27, "?"), (200, 0.225, "?"), (35, 0.18, "404"),
                                           (150, 0.135, "?")]):
            M = wk.place(sp + V(0, 0, z), (0, 0, hd))
            ob = slab("cream", (0, 0, 0), [(0.0, -0.02), (0.1, -0.02), (0.125, 0.0), (0.1, 0.02), (0.0, 0.02)],
                      0.008, rot=(90, 0, 0))
            ob.data.transform(Matrix.Translation((0, 0.004, 0)))
            ob.data.transform(M)
            # the lettering goes on whichever face looks at the reader
            front = (wk.rot3((0, 0, hd)) @ V(0, -1, 0)).y < 0
            tr = wk.place(V(0.06, -0.0045 if front else 0.0045, 0), (90, 0, 0 if front else 180))
            tx = text(word, "graphite", (0, 0, 0), 0.03 if word == "?" else 0.022, rot=(0, 0, 0))
            tx.data.transform(M @ tr)
    W.node("agent_spin", I.at(0.09, -0.09), parent="isle", idle=lambda t: Matrix.Rotation(
        rad(60 * math.sin(TAU * t / 4.0)), 4, "Z"))
    bot(W, "agent", I.at(0.09, -0.09), face=-20, s=1.3, parent="agent_spin",
        arms=(lambda t: rx(-150 + 12 * math.sin(TAU * t / 0.5)) @ ry(-30), lambda t: rx(-10)))
    W.node("marks", I.at(0, 0, 0.52), parent="isle", kind="holo", idle=spin(1))
    with W.on("marks"):
        for k in range(3):
            a = TAU * k / 3
            p = I.at(0.0, 0.0, 0.52) + V(0.17 * math.cos(a), 0.17 * math.sin(a), 0.04 * (k - 1))
            text("?", "holo_cyan", p, 0.11, rot=(90, 0, math.degrees(a) + 90), extrude=0.008)
    rings(W, "holo_cyan", dashes=24)
    W.anchor("anchor_centre", I.at(0.0, -0.15, 0.01), parent="isle")


# ============================================================================================== rave
@world("rave")
def rave(W):
    """Zip's nightclub inside the Core: a dance floor of tiles that flash, a DJ booth with spinning decks,
    speaker stacks, laser fans, a disco ball, and a velvet rope at the door for Brick to mind."""
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.46, 0.3, sides=13, seed=221)
    fl = C.at(0, -0.02, 0.0)
    with W.on("isle_centre"):
        scatter(C, 4, seed=222, ring_=(0.86, 0.96), arc=(120, 420))
        prism("black", fl - V(0, 0, 0.004), 0.42, 0.022, n=4, a0=math.pi / 4)
        # the booth
        db = C.at(0, 0.17, 0.018)
        box("graphite", db + V(0, 0, 0.045), (0.26, 0.08, 0.09))
        box("black", db + V(0, 0.0, 0.092), (0.27, 0.09, 0.006))
        # the rope
        for sx in (-1, 1):
            rp = C.at(sx * 0.1, -0.33)
            prism("brass", rp, 0.006, 0.07, n=6)
            prism("brass", rp, 0.016, 0.006, n=8)
            ball("brass", rp + V(0, 0, 0.075), 0.01, segs=6, rings=3)
        rope = [C.at(-0.1 + 0.2 * k / 6, -0.33, 0.07 - 0.03 * math.sin(math.pi * k / 6)) for k in range(7)]
        tube("velvet", rope, 0.0055, sides=5)
        box("velvet", C.at(0.0, -0.4, 0.002), (0.12, 0.08, 0.004))
    W.node("booth_glow", db, parent="isle_centre", kind="holo")
    with W.on("booth_glow"):
        quad("holo_magenta", db + V(0, -0.0415, 0.05), 0.24, 0.012)
        quad("holo_cyan", db + V(0, -0.0415, 0.025), 0.24, 0.006)
        text("RAVE", "holo_magenta", db + V(0, 0.06, 0.28), 0.09, extrude=0.006)
        box("holo_cyan", db + V(0, 0.06, 0.28), (0.26, 0.004, 0.006))
    for k, sx in enumerate((-1, 1)):
        tt = db + V(sx * 0.065, 0, 0.096)
        W.node(f"deck_{k + 1}", tt, parent="isle_centre", idle=spin(3 if k else -3))
        with W.on(f"deck_{k + 1}"):
            prism("black", tt, 0.04, 0.006, n=12)
            prism("metal", tt + V(0, 0, 0.006), 0.006, 0.004, n=6)
            box("red", tt + V(0.022, 0, 0.0065), (0.012, 0.004, 0.001))
        sp = C.at(sx * 0.32, 0.1)
        W.node(f"speaker_{k + 1}", sp, parent="isle_centre", idle=throb(0.06, 0.5, k * 0.5, (1, 1, 0.5)))
        with W.on(f"speaker_{k + 1}"):
            speaker(sp, 0.1, 0.08, 0.18)
            speaker(sp + V(0, 0, 0.18), 0.08, 0.07, 0.11, cones=1)
    # the dance floor: two sets of tiles that flash in turn
    n, ts = 4, 0.068
    for g in range(2):
        W.node(f"tiles_{g + 1}", fl + V(0, 0, 0.019), parent="isle_centre", kind="holo",
               idle=blink(0.5, g * 0.5, 0.5))
        with W.on(f"tiles_{g + 1}"):
            for i in range(n):
                for j in range(n):
                    if (i + j) % 2 != g:
                        continue
                    m = ["holo_magenta", "holo_cyan", "holo_lime", "holo_extend"][(i * 3 + j * 2 + g) % 4]
                    c = fl + V((i - (n - 1) / 2) * ts, (j - (n - 1) / 2) * ts - 0.06, 0.02)
                    box(m, c, (ts - 0.008, ts - 0.008, 0.003))
    # lasers fanning from the back corners
    for k, sx in enumerate((-1, 1)):
        em = C.at(sx * 0.3, 0.3, 0.3)
        with W.on("isle_centre"):
            prism("graphite", C.at(sx * 0.3, 0.3), 0.006, 0.3, n=5, top=False, bottom=False)
        W.node(f"laser_{k + 1}", em, parent="isle_centre", kind="holo",
               idle=lambda t, sx=sx: rz(sx * 25 * math.sin(TAU * t / 2.0)) @ Matrix.Rotation(
                   rad(10 * math.sin(TAU * t / 1.0)), 4, "X"))
        with W.on(f"laser_{k + 1}"):
            box("graphite", em, (0.03, 0.03, 0.03))
            for j in range(5):
                a = rad(-30 + 15 * j)
                d = V(-sx * 0.5 * math.cos(a) * 0.6, -0.5 * math.cos(a), 0.25 * math.sin(a) + 0.05)
                tube("holo_magenta" if j % 2 else "holo_lime", [em, em + d * 0.9], 0.0025, sides=3, caps=False)
    db2 = C.at(0, -0.06, 0.62)
    W.node("disco", db2, parent="isle_centre", idle=spin(1))
    with W.on("disco"):
        ico("mirror", db2, 0.06, seed=1, subdiv=2, jitter=0.0)
        tube("graphite", [db2, db2 + V(0, 0, 0.1)], 0.002, sides=3)
    rings(W, "holo_magenta")
    W.anchor("anchor_dancefloor", fl + V(0, -0.06, 0.022), parent="isle_centre")
    W.anchor("anchor_dj", C.at(0, 0.25, 0.018), parent="isle_centre")
    W.anchor("anchor_bouncer", C.at(0.17, -0.36, 0.0), parent="isle_centre")


# ========================================================================================= no archies
@world("no-archies")
def no_archies(W):
    """The tiny agents' takeover: a fortress with a NO ARCHIES sign at its gate (a no-entry ring over a
    little Archie head), lookouts on the walls, flags flying, and a catapult on the island next door. The
    `gate` (hinged on its left post) and the `sign` (pivoting at its foot) are nodes of their own, for the
    hostile takeover bit to swing and to swap for the agents' own sign."""
    C = isle_node(W, "isle_centre", 0.0, 0.06, 0.44, 0.3, sides=13, seed=231)
    fc = C.at(0, 0.06)
    hw, wh, wt = 0.2, 0.12, 0.03
    with W.on("isle_centre"):
        scatter(C, 4, seed=232, ring_=(0.86, 0.96), arc=(110, 430))
        prism("stone", fc - V(0, 0, 0.004), 0.06, 0.008, n=4, a0=math.pi / 4, r_top=0.06)
        for k in range(4):
            a = 90 * k
            R3 = wk.rot3((0, 0, a))
            mid = fc + R3 @ V(0, -hw, 0)
            if k == 0:
                for s_ in (-1, 1):
                    box("stone", mid + V(s_ * (hw + 0.045) / 2, 0, wh / 2), (hw - 0.045, wt, wh))
                box("stone", mid + V(0, 0, wh + 0.015), (0.09, wt, 0.03))
                gate = mid
            else:
                box("stone", mid + V(0, 0, wh / 2), (2 * hw, wt, wh), rot=(0, 0, a))
            for j in range(-3, 4):
                if k == 0 and abs(j) <= 0:
                    continue
                box("stone", mid + R3 @ V(j * 0.055, 0, wh + 0.012), (0.028, wt + 0.004, 0.024), rot=(0, 0, a))
        for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            tp = fc + V(dx * hw, dy * hw, 0)
            prism("stone", tp, 0.048, wh + 0.08, n=8)
            prism("red", tp + V(0, 0, wh + 0.08), 0.058, 0.08, n=8, r_top=0.0)
    # the gate: its own node, hinged on its left post, so a bit can swing it open (about Z, +90 opens it inwards)
    hinge = gate + V(-0.04, -0.004, 0)
    W.node("gate", hinge, parent="isle_centre")
    with W.on("gate"):
        box("wood", gate + V(0, -0.004, wh * 0.42), (0.08, wt * 0.6, wh * 0.84))
        box("graphite", gate + V(0.03, -wt * 0.32, wh * 0.42), (0.008, 0.002, 0.012))
    # the sign at the gate: its own node too (pivot at its foot), so a bit can take it down or put it up
    sg = fc + V(0, -hw - 0.13, 0)
    W.node("sign", sg, parent="isle_centre")
    with W.on("sign"), wk.scaled(1.0, sg, rot=(-14, 0, 0)):
        for s_ in (-1, 1):
            box("wood", sg + V(s_ * 0.15, 0, 0.06), (0.014, 0.014, 0.12))
        box("cream", sg + V(0, 0, 0.125), (0.34, 0.014, 0.085))
        box("red", sg + V(0, 0, 0.125), (0.35, 0.01, 0.092))
        text("NO ARCHIES", "red", sg + V(0, -0.0078, 0.125), 0.05)
    # the no-entry sign over a little Archie head, over the gate
    ns = fc + V(0, -hw - 0.02, wh + 0.15)
    W.node("no_entry", ns, parent="isle_centre", kind="holo", idle=chain(bob(0.01, 2.0), throb(0.05, 1.0)))
    with W.on("no_entry"), wk.scaled(1.45, ns):
        ball("cream", ns + V(0, 0.01, -0.004), 0.034, segs=10, rings=5, scale=(0.85, 0.85, 1.05))
        slab("graphite", ns + V(0, 0.01, 0.025), [(-0.03, 0.0), (0.0, 0.006), (0.05, -0.014), (0.012, 0.018),
                                                   (-0.024, 0.014)], 0.012, rot=(90, 0, 0))
        tube("lime", [ns + V(-0.02, 0.005, 0.035), ns + V(0.01, 0.0, 0.05), ns + V(0.04, -0.01, 0.04)], 0.005,
             sides=4)
        for sx in (-1, 1):
            ball("black", ns + V(sx * 0.012, -0.022, 0.0), 0.006, segs=5, rings=3)
        torus("holo_trust", ns, 0.06, 0.007, rot=(90, 0, 0), segs=20, sides=4)
        box("holo_trust", ns + V(0, -0.006, 0), (0.12, 0.006, 0.013), rot=(0, 45, 0))
    # lookouts on the walls
    for k, (x0, x1) in enumerate([(-0.17, -0.06), (0.06, 0.17)]):
        route = [fc + V(x0, -hw, wh), fc + V(x1, -hw, wh)]
        W.node(f"lookout_{k + 1}", route[0], parent="isle_centre",
               idle=shuttle(route, route[0], (0.2 + k, 1.6 + k), (2.2 + k * 0.4, 3.6 + k * 0.1)))
        bot(W, f"lookout_bot_{k + 1}", route[0], face=0, s=0.6, tip="holo_trust", parent=f"lookout_{k + 1}",
            idle=hop(0.006, 0.0, 0.5, 0.25))
    bot(W, "lookout_bot_3", fc + V(0.1, hw, wh), face=-10, s=0.55, tip="holo_trust",
        parent="isle_centre", arms=(lambda t: ry(-150 + 25 * math.sin(TAU * t / 1.0)), lambda t: rx(-10)))
    for k, (dx, dy) in enumerate(((-1, -1), (1, -1), (-1, 1))):
        fp = fc + V(dx * hw, dy * hw, wh + 0.16)
        with W.on("isle_centre"):
            prism("graphite", fp, 0.003, 0.09, n=4, top=False, bottom=False)
        W.node(f"flag_{k + 1}", fp + V(0, 0, 0.09), parent="isle_centre",
               idle=swing(18, 1.0, k / 3, axis="Z"))
        with W.on(f"flag_{k + 1}"):
            slab("red" if k != 1 else "yellow", fp + V(0, 0.002, 0.09),
                 [(0.0, -0.035), (0.06, -0.025), (0.05, -0.0125), (0.06, 0.0), (0.0, 0.0)], 0.004, rot=(90, 0, 0))
    # the catapult, aimed at the reader
    S = sat(W, "isle_catapult", 330, 0.72, 0.17, 0.36, seed=233, trees=1, clear=0.1, drip_m="holo_trust")
    cp = S.at(0.0, 0.01)
    with W.on("isle_catapult"):
        box("wood", cp + V(0, 0, 0.012), (0.08, 0.12, 0.016))
        for sx in (-1, 1):
            box("wood", cp + V(sx * 0.034, 0.0, 0.045), (0.01, 0.01, 0.07))
            ball("graphite", cp + V(sx * 0.044, -0.045, 0.01), 0.012, segs=6, rings=3)
            ball("graphite", cp + V(sx * 0.044, 0.045, 0.01), 0.012, segs=6, rings=3)
        box("wood", cp + V(0, 0.0, 0.08), (0.078, 0.01, 0.01))
    piv = cp + V(0, 0.0, 0.03)

    def fling(t):
        u = t % 4.0
        a = -60 + 85 * ease("snap", (u - 2.5) / 0.2) if 2.5 <= u < 2.7 else 25 * (1 - smooth01((u - 2.7) / 1.0)) \
            if 2.7 <= u < 3.7 else -60 * smooth01(u / 2.5) if u < 2.5 else 0.0
        return rx(a)

    W.node("arm", piv, parent="isle_catapult", idle=fling)
    with W.on("arm"):
        box("wood", piv + V(0, 0.05, 0.0), (0.012, 0.12, 0.01))
        prism("wood", piv + V(0, 0.11, 0.004), 0.018, 0.014, n=8, r_top=0.022)
        ball("lime", piv + V(0, 0.11, 0.022), 0.012, segs=6, rings=3)
    rings(W, "holo_trust")
    W.anchor("anchor_gate", fc + V(0, -hw - 0.05, 0.0), parent="isle_centre")


# ============================================================================================== main
ORDER = ["home", "orchestrators-multi-agent", "coding-agents", "agent-skills", "mcp-servers", "frameworks-sdks",
         "harnesses-runtime-infra", "context-memory-rag", "sandbox-security-governance", "observability-evals",
         "plugins-themes-clients", "research-data-agents", "creative-voice-media", "assistants-domain-agents",
         "docs-learning-lists", "discover", "collections", "lost", "rave", "no-archies", "holo-bot"]


def main():
    only = opt("--only")
    known = [s for s in ORDER if s in WORLDS] + [s for s in WORLDS if s not in ORDER]
    slugs = only.split(",") if only else known
    unknown = [s for s in slugs if s not in WORLDS]
    if unknown:
        raise SystemExit(f"unknown worlds: {unknown}; known: {list(WORLDS)}")
    out = Path(opt("--out", str(SITE))).resolve()
    raw = Path(opt("--raw", str(SCRATCH / "out" / "worlds-raw"))).resolve()
    renders = Path(opt("--renders", str(SCRATCH / "renders" / "worlds"))).resolve()
    samples = int(opt("--samples", "40"))
    for d in (out, raw):
        d.mkdir(parents=True, exist_ok=True)
    rows = []
    for slug in slugs:
        wk.reset()
        fn, fam, kw = WORLDS[slug]
        W = wk.World(slug, fam, **kw)
        fn(W)
        W.finalize()
        W.bake()
        info = W.check()
        path = wk.export(W, out / f"{slug}.glb", raw)
        g = wk.inspect(path)
        ok = info["radius"] <= wk.RADIUS and info["zmin"] >= -0.001 and info["zmax"] <= wk.HEIGHT
        rows.append((slug, g["bytes"], g["tris"], info, g, ok))
        print(f"WORLD {slug}: {g['bytes'] / 1024:.1f} KB tris={g['tris']} nodes={info['nodes']} "
              f"r={info['radius']} z=[{info['zmin']}, {info['zmax']}] {'ok' if ok else 'OUT OF BOUNDS'} "
              f"scattered={info.get('scattered')} anims={g['animations']} mats={g['materials']}")
        if W.islands:
            print(f"  ISLANDS {slug}: " + ", ".join(f"{new}={old}" for old, new in W.renamed.items()))
        if "--no-render" not in ARGS:
            renders.mkdir(parents=True, exist_ok=True)
            wk.stage(samples=samples, **W.camera)
            wk.render(renders / f"{slug}.png", W, "idle", W.preview_t)
            if "--strip" in ARGS:
                strips = W.strips or [
                    ("entrance", [("appear", t) for t in (0.1, 0.25, 0.4, 0.6)] +
                     [("idle", t) for t in (0.5, 1.5, 2.5, 3.5)]),
                    ("gags", [("scatter", t) for t in (0.1, 0.3, 0.6, 1.0)] +
                     [("gather", t) for t in (0.3, 0.7, 1.0, 1.2)] +
                     [("tilt", t) for t in (0.15, 0.35, 0.55, 0.8)] +
                     [("level", t) for t in (0.1, 0.25, 0.4, 0.6)])]
                for label, moments in strips:
                    # the motion, as rows of stills, four to a clip
                    shots = [wk.render(renders / "strips" / f"{slug}@{clip}-{t:.3f}.png", W, clip, t, res=360,
                                       samples=16) for clip, t in moments]
                    if wk.contact_sheet(shots, renders / "strips" / f"{slug}-{label}.png", cols=4, tile=360,
                                        labels=[f"{c} {t:.2f}s" for c, t in moments]):
                        for shot in shots:
                            Path(shot).unlink()
    if "--no-render" not in ARGS:
        done = [renders / f"{s}.png" for s in known if (renders / f"{s}.png").exists()]
        wk.contact_sheet(done, renders / "contact-sheet.png")
    print("\nSUMMARY")
    for slug, b, tris, info, g, ok in rows:
        print(f"  {slug:30s} {b / 1024:6.1f} KB {tris:5d} tris  r {info['radius']:.3f}  z {info['zmax']:.3f}"
              f"  {'ok' if ok and b <= 60 * 1024 else 'CHECK'}")


if __name__ == "__main__":
    main()
