"""The fourteen topic worlds, in the taxonomy's order (scripts/taxonomy.py CATEGORIES), each in its family's
accent (scripts/30_v2.py FAMILY_OF). Built from worlds_kit's vocabulary; `worlds.py` runs them.
"""
from __future__ import annotations

import math
import random

from mathutils import Matrix, Vector

from kit.anim import ease, pulse
from kit.geo import TAU, V
from worlds_kit import (along, arc, arc_pts, ball, beam, blink, bob, bot, box, bush, card, chain, disc_ring,
                        drip, flat_ring, frame, glint, glow_cone, hop, ico, isle_node, lathe, pedestal, polar,
                        prism, quad, rock, sat, scatter, shuttle, slab, spin, swing, text, throb, torus, tube,
                        world)
import worlds_kit as wk


def rad(d):
    return math.radians(d)


def rx(deg):
    return Matrix.Rotation(rad(deg), 4, "X")


def ry(deg):
    return Matrix.Rotation(rad(deg), 4, "Y")


def rz(deg):
    return Matrix.Rotation(rad(deg), 4, "Z")


def facing(p, target, toward_reader=0.5):
    """The `face` angle that turns a bot at `p` towards `target`, blended towards the reader (-Y)."""
    d = Vector(target) - Vector(p)
    a = math.degrees(math.atan2(-d.x, -d.y))          # face 0 looks down -Y; +face turns towards +X
    a = (a + 180) % 360 - 180
    return a * (1 - toward_reader)


def rings(W, m, idle=True, r=0.93, dashes=36):
    """The dashed ring round the disc's edge, drifting by one dash a loop."""
    W.node("rings", (0, 0, 0.012), kind="holo", idle=spin(1 / dashes) if idle else None, cyclic=False)
    with W.on("rings"):
        disc_ring(m, r, dashes=dashes)


# ------------------------------------------------------------------------------------- small props
def speaker(p, w=0.075, d=0.065, h=0.15, cones=2):
    p = Vector(p)
    box("black", p + V(0, 0, h / 2), (w, d, h))
    for k in range(cones):
        z = h * (0.3 + 0.42 * k)
        r = w * (0.36 if k == 0 else 0.26)
        prism("metal", p + V(0, -d / 2 + 0.002, z), r, 0.006, n=10, rot=(90, 0, 0), r_top=r * 0.7)
        prism("graphite", p + V(0, -d / 2 - 0.003, z), r * 0.35, 0.004, n=8, rot=(90, 0, 0))


def lamp_post(p, h=0.16, light="holo_white"):
    p = Vector(p)
    prism("graphite", p, 0.006, h, n=5, top=False, bottom=False)
    prism("graphite", p, 0.016, 0.01, n=8)
    ball(light, p + V(0, 0, h + 0.012), 0.016, segs=6, rings=3)
    prism("graphite", p + V(0, 0, h + 0.024), 0.02, 0.012, n=6, r_top=0.004, bottom=False)


def bench(p, face=0.0, w=0.09):
    p = Vector(p)
    R = (0, 0, face)
    M = wk.place(p, R)
    for ob in (box("wood", (0, 0, 0.026), (w, 0.03, 0.008)), box("wood", (0, 0.016, 0.045), (w, 0.006, 0.03)),
               box("graphite", (-w * 0.4, 0, 0.011), (0.006, 0.026, 0.022)),
               box("graphite", (w * 0.4, 0, 0.011), (0.006, 0.026, 0.022))):
        ob.data.transform(M)


def house(p, w, d, h, roof="red", face=0.0, door="wood", window="holo_white"):
    """A cottage facing -Y (turned by `face`): walls, a pitched roof, a door and a lit window."""
    M = wk.place(Vector(p), (0, 0, face))
    obs = [box("cream", (0, 0, h / 2), (w, d, h)),
           slab(roof, (-w / 2 - 0.008, 0, h - 0.002),
                [(-d / 2 - 0.012, 0), (d / 2 + 0.012, 0), (0, h * 0.75)], w + 0.016, rot=(90, 0, 90)),
           box(door, (-w * 0.18, -d / 2 - 0.002, h * 0.28), (w * 0.22, 0.006, h * 0.56)),
           quad(window, (w * 0.2, -d / 2 - 0.004, h * 0.55), w * 0.22, h * 0.24)]
    for ob in obs:
        ob.data.transform(M)


def book(p, thick, depth, h, cover, face=0.0, tilt=0.0, bands="brass"):
    """A book standing on its tail, spine to the reader: covers, a page block, bands round the spine."""
    M = wk.place(Vector(p), (0, tilt, face))
    obs = [box(cover, (0, 0, h / 2), (thick, depth, h)),
           box("paper", (0, 0.006, h / 2 + 0.002), (thick * 0.8, depth - 0.004, h - 0.006)),
           box(bands, (0, -depth / 2 - 0.001, h * 0.82), (thick + 0.002, 0.004, h * 0.035)),
           box(bands, (0, -depth / 2 - 0.001, h * 0.18), (thick + 0.002, 0.004, h * 0.035))]
    for ob in obs:
        ob.data.transform(M)


def gear_pts(teeth, ro, ri, frac=0.45):
    pts = []
    for k in range(teeth):
        a0 = TAU * k / teeth
        da = TAU / teeth
        for a, r in ((a0, ri), (a0 + da * 0.12, ro), (a0 + da * frac, ro), (a0 + da * (frac + 0.12), ri)):
            pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def jigsaw_pts(L, sides=(0, 0, 0, 0)):
    """A jigsaw piece's outline, `L` square, counter-clockwise from the bottom left; `sides` (bottom, right,
    top, left) are 0 flat, 1 a knob out, -1 a socket in."""
    knob = [(0.35, 0.0), (0.39, 0.07), (0.33, 0.16), (0.38, 0.24), (0.5, 0.27), (0.62, 0.24), (0.67, 0.16),
            (0.61, 0.07), (0.65, 0.0)]
    corners = [(0, 0), (L, 0), (L, L), (0, L)]
    pts = []
    for i in range(4):
        a, b = Vector(corners[i]), Vector(corners[(i + 1) % 4])
        d = (b - a) / L
        n = Vector((d.y, -d.x))                        # outward, for a counter-clockwise outline
        pts.append(tuple(a))
        if sides[i]:
            for u, v in knob:
                q = a + d * (u * L) + n * (v * L * sides[i])
                pts.append((q.x, q.y))
    return [(x - L / 2, y - L / 2) for x, y in pts]


def magnifier(p, r=0.05, rot=(0, 0, 0), lens="holo_panel"):
    """A magnifying glass, its lens facing up (turned by `rot`)."""
    M = wk.place(Vector(p), rot)
    obs = [torus("brass", (0, 0, 0), r, r * 0.13, segs=16, sides=4),
           prism(lens, (0, 0, -0.002), r * 0.92, 0.004, n=12),
           tube("wood", [(r * 1.05, 0, 0), (r * 2.3, 0, 0)], r * 0.13, sides=5)]
    for ob in obs:
        ob.data.transform(M)


def check(p, s, m, rot=(0, 0, 0)):
    """A tick, facing -Y."""
    M = wk.place(Vector(p), rot)
    tube(m, [(-s * 0.5, 0, s * 0.05), (-s * 0.12, 0, -s * 0.35), (s * 0.55, 0, s * 0.45)], s * 0.1,
         sides=3).data.transform(M)


def note(p, s, m):
    """A quaver, facing -Y."""
    p = Vector(p)
    ball(m, p, s * 0.28, segs=6, rings=3, scale=(1.3, 0.6, 1.0), rot=(0, -25, 0))
    box(m, p + V(s * 0.3, 0, s * 0.45), (s * 0.08, s * 0.08, s * 0.9))
    box(m, p + V(s * 0.45, 0, s * 0.78), (s * 0.32, s * 0.08, s * 0.1), rot=(0, 30, 0))


# ================================================================================ orchestrators (run)
@world("orchestrators-multi-agent", "run")
def orchestrators(W):
    """Little agents on islands, each taking a glowing task the conductor on the middle podium sends out
    along an arc (each hops when one lands), and the backlog piled up on an island of its own."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, -0.04, 0.34, 0.3, sides=12, seed=41)
    with W.on("isle_centre"):
        scatter(C, 4, seed=42, avoid=lambda x, y: math.hypot(x - C.x, y - C.y + 0.03) < 0.19, companions=0.0)
        prism("stone", C.at(0, 0, -0.004), 0.12, 0.03, n=12)
        prism("cream", C.at(0, 0, 0.024), 0.088, 0.034, n=12)
        flat_ring(A, C.at(0, 0, 0.059), 0.074, 0.008, segs=16)
    top = C.at(0, 0, 0.058)
    s = 1.4

    def baton(t):                                   # down on the beat, a beat a second
        return rx(-78 + 22 * math.sin(TAU * t / 1.0))

    bot(W, "conductor", top, face=0, s=s, tip=A, parent="isle_centre", idle=swing(5, 2.0, axis="Z"),
        arms=(lambda t: rx(-55) @ ry(-25), baton))
    hand = top + V(-0.042, -0.008, 0.016) * s
    with W.on("conductor_arm_R"):
        tube("graphite", [hand, hand + V(0.0, -0.025, -0.09)], 0.0035, sides=3)
        ball(A, hand + V(0.0, -0.025, -0.094), 0.009, segs=5, rings=2)
    head = top + V(0, 0, 0.27)
    workers = [(150, 0.66, 0.55), (35, 0.66, 0.57), (325, 0.7, 0.36)]
    W.node("arcs", head, kind="holo")
    # the backlog: a pile of tasks still waiting their turn, on an island of their own
    Q = sat(W, "isle_backlog", 215, 0.7, 0.15, 0.34, seed=49, trees=0, drip_m=A, bushes=2, sides=8)
    with W.on("isle_backlog"):
        for j, (dx, dy, dz, rz_) in enumerate([(-0.025, 0.0, 0.0, 10), (0.025, 0.01, 0.0, -15), (0.0, 0.0, 1.0, 30)]):
            box(A, Q.at(dx, dy, 0.022 + dz * 0.045), (0.042, 0.042, 0.042), rot=(0, 0, rz_))
    for k, (a, d, z) in enumerate(workers):
        S = sat(W, f"isle_{k + 1}", a, d, 0.17, z, seed=50 + k, trees=1, clear=0.08, drip_m=A, bushes=0, sides=8)
        with W.on(f"isle_{k + 1}"):
            pp = pedestal(S.at(0, 0), 0.055, glow=A, m="graphite")
        t_arr = (2.0 * (1 - k / 3)) % 2.0
        bot(W, f"agent_{k + 1}", pp, face=facing(pp, C.c, 0.5), s=1.3, tip=A, parent=f"isle_{k + 1}",
            idle=hop(0.035, t_arr, period=2.0))
        b = pp + V(0, 0, 0.27)
        a_ = head + (pp - head).normalized() * 0.02
        h = 0.12 if z > 0.45 else 0.2
        with W.on("arcs"):
            arc(a_, b, h, m=A)
        glint(W, f"task_{k + 1}", arc_pts(a_, b, h, 8), period=2.0, phase=k / 3, m="holo_white", r=0.016,
              shape="cube")
    rings(W, A)
    W.anchor("anchor_centre", top, parent="isle_centre")


# ================================================================================== coding agents (run)
@world("coding-agents", "run")
def coding(W):
    """A coding workshop: an agent at a desk typing into a big hologram of code (and then deleting the
    last line), a crate of spare brackets, a rubber duck on a pond, and a build light that goes green."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.0, 0.38, 0.3, sides=12, seed=61)
    T = C.top
    K = 1.4                                         # the workshop, fitted to its island
    with W.on("isle_centre"), wk.scaled(K, (0, 0, T)):
        # the desk, in front of the agent
        dz = T + 0.075
        box("wood", (0, -0.045, dz), (0.22, 0.1, 0.014))
        for sx in (-1, 1):
            for sy in (-1, 1):
                box("trunk", (sx * 0.095, -0.045 + sy * 0.038, T + 0.034), (0.012, 0.012, 0.075))
        # the laptop: its lid to us, a glowing </> on the back of it
        box("graphite", (0, -0.03, dz + 0.011), (0.1, 0.065, 0.006))
        box("graphite", (0, -0.065, dz + 0.045), (0.1, 0.005, 0.068), rot=(-12, 0, 0))
        text("</>", A, (0, -0.0705, dz + 0.046), 0.03, rot=(78, 0, 0))
        # a mug of coffee
        lathe("cream", (0.075, -0.06, dz + 0.007), [(0.0, 0.0), (0.014, 0.0), (0.015, 0.028), (0.0, 0.028)], 8)
        torus("cream", (0.091, -0.06, dz + 0.021), 0.007, 0.0025, rot=(90, 0, 0), segs=8, sides=4)
        # a stool, mostly hidden
        prism("graphite", (0, 0.05, T), 0.03, 0.05, n=8)
        # the crate of brackets
        cx, cy = 0.15, -0.12
        box("wood", (cx, cy, T + 0.035), (0.13, 0.1, 0.07))
        box("trunk", (cx, cy, T + 0.066), (0.12, 0.09, 0.006))
        box("trunk", (cx, cy - 0.051, T + 0.035), (0.135, 0.004, 0.012))
        box("trunk", (cx, cy + 0.051, T + 0.035), (0.135, 0.004, 0.012))
        for k, (ch, m, dx, dy, r) in enumerate([("{", "yellow", -0.035, 0.0, (80, 0, 15)),
                                                ("}", "violet", 0.0, 0.01, (75, 0, -10)),
                                                ("{", "mint", 0.035, -0.005, (85, 0, 30)),
                                                ("}", "red", -0.01, -0.025, (70, 15, -25))]):
            text(ch, m, (cx + dx, cy + dy, T + 0.085), 0.075, rot=r, extrude=0.006)
        text("}", "yellow", (cx - 0.1, cy - 0.06, T + 0.006), 0.06, rot=(0, 0, 20), extrude=0.005)
    with W.on("isle_centre"):
        scatter(C, 5, seed=62, ring_=(0.72, 0.92), arc=(110, 330),
                avoid=lambda x, y: math.hypot(x, y + 0.03) < 0.22 or math.hypot(x - 0.21, y + 0.17) < 0.13)
        bush(C.at(-0.26, -0.12), 0.026, seed=3)
    # the agent, typing
    seat = V(0, 0.05 * K, T + 0.045 * K)

    def typing(ph):
        return lambda t: rx(-62 + 7 * math.sin(TAU * (t / 0.25 + ph)))

    bot(W, "coder", seat, face=0, s=1.05 * K, tip=A, parent="isle_centre", idle=swing(3, 1.0, axis="Y"),
        arms=(typing(0.0), typing(0.5)))
    # the code: a hologram over the agent's head, to us
    sc = V(0, 0.2, T + 0.5)
    sw, sh = 0.48, 0.28
    W.node("screen", sc, parent="isle_centre", kind="holo", idle=bob(0.008, 2.0))
    with W.on("screen"):
        quad("holo_panel", sc, sw, sh)
        frame("holo_cyan", sc + V(0, -0.001, 0), sw, sh, 0.008)
        rng = random.Random(3)
        indent = [0, 1, 2, 2, 1, 2, 0]
        for k, ind in enumerate(indent[:6]):
            z = sc.z + sh / 2 - 0.04 - k * 0.036
            x0 = sc.x - sw / 2 + 0.035 + ind * 0.035
            w = rng.uniform(0.09, 0.22)
            quad(A if k % 3 else "holo_cyan", (x0 + w / 2, sc.y - 0.002, z), w, 0.014)
        text("{ }", "holo_white", (sc.x + sw / 2 - 0.07, sc.y - 0.003, sc.z + sh / 2 - 0.06), 0.065)
    # the line being typed (and then deleted): it grows from its left end
    z = sc.z + sh / 2 - 0.04 - 6 * 0.036
    x0 = sc.x - sw / 2 + 0.035
    L = 0.27

    def grow(t):
        if t < 2.9:
            u = t / 2.9
        elif t < 3.3:
            u = 1.0
        else:
            u = 1 - ease("inout", (t - 3.3) / 0.7)
        return Matrix.Diagonal((max(0.02, u), 1, 1, 1))

    W.node("typing", (x0, sc.y - 0.002, z), parent="screen", kind="holo", idle=grow)
    with W.on("typing"):
        quad(A, (x0 + L / 2, sc.y - 0.002, z), L, 0.014)

    def cursor(t):
        g = grow(t)[0][0]
        on = 1.0 if (t * 2.5) % 1.0 < 0.6 or g < 0.999 else 0.001
        return Matrix.Translation((L * g + 0.008, 0, 0)) @ Matrix.Scale(on, 4)

    W.node("cursor", (x0, sc.y - 0.003, z), parent="screen", kind="holo", idle=cursor)
    with W.on("cursor"):
        quad("holo_white", (x0, sc.y - 0.003, z), 0.012, 0.024)
    # the rubber duck on its pond
    D = sat(W, "isle_duck", 150, 0.68, 0.18, 0.5, seed=63, trees=2, clear=0.1, drip_m=A)
    with W.on("isle_duck"):
        prism("blue", D.at(0, 0, -0.003), 0.095, 0.006, n=12, ry=0.075)
        rock(D.at(0.09, 0.03), 0.018, seed=4)
    dk = D.at(0, 0, 0.004)
    W.node("duck", dk, parent="isle_duck",
           idle=chain(swing(8, 2.0, axis="X"), bob(0.004, 1.0), swing(20, 4.0, axis="Z")))
    with W.on("duck"), wk.scaled(1.35, dk):
        ball("yellow", dk + V(0, 0, 0.022), 0.035, segs=10, rings=5, scale=(1.0, 1.3, 0.75))
        ball("yellow", dk + V(0, -0.03, 0.06), 0.022, segs=8, rings=4)
        prism("orange", dk + V(0, -0.048, 0.057), 0.009, 0.018, n=6, rot=(90, 0, 0), r_top=0.002)
        ball("black", dk + V(-0.011, -0.046, 0.068), 0.004, segs=5, rings=3)
        ball("black", dk + V(0.011, -0.046, 0.068), 0.004, segs=5, rings=3)
    # the build light
    B = sat(W, "isle_ci", 35, 0.68, 0.16, 0.54, seed=64, trees=2, clear=0.07, drip_m=A)
    bt = B.at(0, 0)
    with W.on("isle_ci"), wk.scaled(1.25, bt):
        prism("graphite", bt, 0.008, 0.16, n=5, top=False, bottom=False)
        box("graphite", bt + V(0, 0, 0.2), (0.05, 0.04, 0.11))
        ball("red", bt + V(0, -0.02, 0.235), 0.012, segs=8, rings=4)
        ball("orange", bt + V(0, -0.02, 0.2), 0.012, segs=8, rings=4)
    gl = bt + V(0, -0.022, 0.165) * 1.25
    W.node("green_light", gl, parent="isle_ci", kind="holo",
           idle=lambda t: Matrix.Identity(4) if t >= 3.0 or t < 0.1 else Matrix.Scale(0.001, 4))
    with W.on("green_light"):
        ball(A, gl, 0.016, segs=8, rings=4)
    # the pull request, sent to the build when the line is done
    a_ = sc + V(sw / 2, 0, 0.02)
    b_ = bt + V(0, 0, 0.27 * 1.25 + 0.02)
    W.node("arcs", a_, kind="holo")
    with W.on("arcs"):
        arc(a_, b_, 0.08, m=A)
    glint(W, "commit", arc_pts(a_, b_, 0.08, 14), period=4.0, phase=0.25, m="holo_white", r=0.012,
          shape="cube", spin_=2)
    rings(W, A)
    W.anchor("anchor_centre", seat, parent="isle_centre")


# ======================================================================= assistants & domain agents (run)
@world("assistants-domain-agents", "run")
def assistants(W):
    """A town square: a help kiosk with an agent at the counter, chat bubbles drifting up, a visitor
    strolling round, and the houses and shops of the domains it serves."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.0, 0.42, 0.3, sides=13, seed=71)
    T = C.top
    with W.on("isle_centre"):
        scatter(C, 5, seed=72, ring_=(0.78, 0.92))
        prism("stone", C.at(0, 0, -0.004), 0.25, 0.014, n=14)
    ky = 0.08
    KK = 1.3
    with W.on("isle_centre"), wk.scaled(KK, (0, ky, T)):
        # the kiosk
        box("cream", (0, ky - 0.03, T + 0.045), (0.2, 0.06, 0.09))
        box("mint", (0, ky - 0.061, T + 0.06), (0.2, 0.004, 0.022))
        for sx in (-1, 1):
            box("graphite", (sx * 0.095, ky + 0.04, T + 0.11), (0.012, 0.012, 0.22))
            box("graphite", (sx * 0.095, ky - 0.055, T + 0.11), (0.01, 0.01, 0.13))
        for k in range(6):
            x = -0.1 + 0.2 * (k + 0.5) / 6
            box("mint" if k % 2 else "white", (x, ky - 0.015, T + 0.215), (0.2 / 6, 0.15, 0.008), rot=(-18, 0, 0))
        box("cream", (0, ky + 0.045, T + 0.27), (0.12, 0.012, 0.06))
        text("HELP", "graphite", (0, ky + 0.038, T + 0.27), 0.036)
    with W.on("isle_centre"):
        # benches, a lamp
        bench(C.at(-0.25, 0.0), face=-70)
        bench(C.at(0.25, 0.0), face=70)
        lamp_post(C.at(-0.12, -0.19), 0.17)
        lamp_post(C.at(0.14, -0.19), 0.17)
    bot(W, "helper", V(0, ky + 0.01 * KK, T + 0.012 * KK), face=0, s=KK, tip=A, parent="isle_centre",
        idle=bob(0.004, 1.0), arms=(lambda t: rx(-10), lambda t: ry(150 + 25 * math.sin(TAU * t / 1.0))))
    # a visitor walking round the square
    path = [C.at(0.17 * math.cos(a), -0.1 + 0.07 * math.sin(a)) for a in
            [TAU * k / 16 for k in range(16)]]
    W.node("visitor", path[0], parent="isle_centre", idle=along(path, path[0], 4.0, face=True))
    bot(W, "visitor_bot", path[0], face=0, s=0.9, body="cream", tip="holo_cyan", parent="visitor",
        idle=hop(0.006, 0.0, period=0.5, dur=0.25))
    # chat bubbles
    for k, (x, y, z, m, ph) in enumerate([(-0.2, 0.0, 0.4, "holo_cyan", 0.0), (0.21, 0.04, 0.47, A, 0.33),
                                          (0.02, -0.08, 0.6, "holo_white", 0.66)]):
        p = V(x, y, T + z)
        W.node(f"bubble_{k + 1}", p, kind="holo", idle=chain(bob(0.02, 2.0, ph), swing(6, 4.0, ph, axis="Z")))
        with W.on(f"bubble_{k + 1}"), wk.scaled(1.35, p):
            prism(m, p + V(0, 0.006, 0), 0.065, 0.012, n=10, ry=0.042, rot=(90, 0, 0))
            prism(m, p + V(-0.03 + 0.06 * (k % 2), 0.006, -0.036), 0.016, 0.012, n=3, rot=(90, 0, 0),
                  a0=-math.pi / 2)
            for j in (-1, 0, 1):
                ball("holo_white" if m != "holo_white" else "holo_cyan", p + V(j * 0.025, -0.009, 0), 0.008,
                     segs=6, rings=3)
    # the domains: a cottage and a shop
    H = sat(W, "isle_home", 145, 0.68, 0.17, 0.5, seed=73, trees=2, clear=0.09, drip_m=A)
    with W.on("isle_home"), wk.scaled(1.3, H.c):
        house(H.at(0.0, 0.0), 0.11, 0.09, 0.08, roof="red", face=facing(H.c, C.c, 0.4))
    S = sat(W, "isle_shop", 35, 0.68, 0.17, 0.52, seed=74, trees=2, clear=0.09, drip_m=A)
    with W.on("isle_shop"), wk.scaled(1.3, S.c):
        house(S.at(0.0, 0.0), 0.12, 0.09, 0.07, roof="blue", face=facing(S.c, C.c, 0.4), window="holo_cyan")
        text("$", "holo_white", S.at(0.0, -0.05, 0.13), 0.06)
    W.node("arcs", C.c, kind="holo")
    for k, I in enumerate((H, S)):
        a_ = V(0, ky + 0.045 * KK, T + 0.31 * KK)
        b_ = I.at(0, 0, 0.21)
        with W.on("arcs"):
            arc(a_, b_, 0.12, m=A)
        glint(W, f"message_{k + 1}", arc_pts(a_, b_, 0.12, 14), period=2.0, phase=k * 0.5, r=0.011)
    rings(W, A)
    W.anchor("anchor_centre", C.at(0, -0.02, 0.01), parent="isle_centre")


# ========================================================================== research & data agents (run)
@world("research-data-agents", "run")
def research(W):
    """An observatory on an island of books: a telescope sweeping a constellation of data, and a
    magnifying glass going over the bars of a chart."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.02, -0.02, 0.4, 0.3, sides=12, seed=81)
    T = C.top
    o = V(-0.06, 0.06, T)
    KO = 1.25
    with W.on("isle_centre"):
        scatter(C, 7, seed=82, ring_=(0.7, 0.92), avoid=lambda x, y: math.hypot(x - o.x, y - o.y) < 0.2 or
                math.hypot(x - 0.2, y + 0.14) < 0.1)
    with W.on("isle_centre"), wk.scaled(KO, o):
        prism("cream", o - V(0, 0, 0.004), 0.12, 0.11, n=14)
        box("wood", o + V(0, -0.121, 0.04), (0.04, 0.006, 0.07))
        for k, (m, w, rz_) in enumerate([("red", 0.1, 5), ("blue", 0.09, -8), ("yellow", 0.095, 12),
                                         ("mint", 0.08, -4)]):
            z = T + 0.012 + k * 0.022
            box(m, (0.2, -0.14, z), (w, 0.07, 0.02), rot=(0, 0, rz_))
            box("paper", (0.2 + 0.004, -0.14, z), (w - 0.006, 0.066, 0.016), rot=(0, 0, rz_))
    # the dome turns, and the telescope with it
    W.node("dome", o + V(0, 0, 0.106 * KO), parent="isle_centre", idle=swing(28, 4.0, axis="Z", bias=10))
    with W.on("dome"), wk.scaled(KO, o):
        dc = o + V(0, 0, 0.106)
        lathe("metal", dc, [(0.12, 0.0), (0.112, 0.04), (0.088, 0.08), (0.05, 0.108), (0.0, 0.12)], 14)
        box("graphite", dc + V(0.05, 0.03, 0.085), (0.13, 0.035, 0.02), rot=(0, -45, 30))
        tip = dc + V(0.14, 0.07, 0.17)
        tube("brass", [dc + V(0.02, 0.0, 0.06), tip], 0.017, sides=8)
        torus("graphite", tip, 0.018, 0.004, rot=(0, 65, 25), segs=10, sides=4)
        glow_cone(A, tip, tip + V(0.06, 0.04, 0.16), 0.05, n=8)
    # the constellation: a little graph of stars
    cc = V(0.14, 0.18, T + 0.7)
    W.node("stars", cc, kind="holo", idle=chain(swing(14, 4.0, axis="Z"), throb(0.04, 1.0)))
    with W.on("stars"):
        pts = [cc + V(*q) for q in [(-0.16, 0, 0.02), (-0.07, 0.02, 0.1), (0.03, -0.02, 0.05),
                                   (0.12, 0.01, 0.13), (0.17, 0.0, 0.0), (0.04, 0.03, -0.07),
                                   (-0.09, -0.01, -0.06)]]
        for i, j in [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 0), (1, 3)]:
            tube(A, [pts[i], pts[j]], 0.0035, sides=3)
        for k, p in enumerate(pts):
            ball("holo_white", p, 0.016 if k % 3 else 0.022, segs=6, rings=3)
    # a chart under a magnifying glass
    S = sat(W, "isle_chart", 330, 0.68, 0.18, 0.38, seed=83, trees=1, clear=0.12, drip_m=A)
    with W.on("isle_chart"):
        for k, (h, m) in enumerate([(0.07, "blue"), (0.13, "mint"), (0.1, "yellow"), (0.16, "red")]):
            box(m, S.at(-0.06 + k * 0.04, 0.0, h / 2), (0.03, 0.03, h))
    mc = S.at(0.0, -0.02, 0.2)
    circle_ = [mc + V(0.05 * math.cos(a), 0.03 * math.sin(a), 0.01 * math.sin(2 * a)) for a in
               [TAU * k / 12 for k in range(12)]]
    W.node("magnifier", mc, parent="isle_chart", idle=along(circle_, mc, 4.0))
    with W.on("magnifier"):
        magnifier(mc, 0.075, rot=(-35, 0, -30))
    # the stacks
    L = sat(W, "isle_stacks", 150, 0.68, 0.17, 0.52, seed=84, trees=2, clear=0.09, drip_m=A)
    with W.on("isle_stacks"):
        for k, (m, h) in enumerate([("violet", 0.12), ("red", 0.15), ("blue", 0.1), ("yellow", 0.13)]):
            book(L.at(-0.05 + k * 0.03, 0.0), 0.026, 0.08, h, m, face=-20, tilt=(-6 if k == 3 else 0))
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.1, -0.1, 0.01), parent="isle_centre")


# ================================================================================ agent skills (extend)
@world("agent-skills", "extend")
def skills(W):
    """A training dojo beside a glowing skill tree whose tiers light up one after another, a sparring
    agent at its dummy, and scrolls of technique floating over the island."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.0, 0.41, 0.3, sides=12, seed=91)
    T = C.top
    W.preview_t = 3.0
    d = V(-0.15, 0.1, T)
    with W.on("isle_centre"):
        scatter(C, 7, seed=92, kinds=("round", "round", "pine"), ring_=(0.7, 0.92),
                avoid=lambda x, y: math.hypot(x - d.x, y - d.y) < 0.21 or math.hypot(x - 0.14, y + 0.08) < 0.17)
    with W.on("isle_centre"), wk.scaled(1.15, d):
        box("wood", d + V(0, 0, 0.012), (0.24, 0.2, 0.03))
        for sx in (-1, 1):
            for sy in (-1, 1):
                box("red", d + V(sx * 0.1, sy * 0.08, 0.075), (0.016, 0.016, 0.11))
        box("paper", d + V(0, 0.08, 0.075), (0.18, 0.008, 0.1))
        box("paper", d + V(-0.1, 0, 0.075), (0.008, 0.15, 0.1))
        box("paper", d + V(0.1, 0, 0.075), (0.008, 0.15, 0.1))
        prism("graphite", d + V(0, 0, 0.13), 0.2, 0.05, n=4, r_top=0.1, ry=0.17)
        prism("red", d + V(0, 0, 0.18), 0.1, 0.012, n=4, ry=0.085)
        prism("graphite", d + V(0, 0, 0.192), 0.12, 0.04, n=4, r_top=0.02, ry=0.1)
        box("violet", d + V(0, -0.101, 0.1), (0.05, 0.004, 0.06))
    # the skill tree, facing us: a trunk, branches, and three tiers of nodes, each tier a badge
    t0 = V(0.14, -0.08, T)
    tiers = [[V(0, 0, 0.2)], [V(-0.1, 0, 0.35), V(0.1, 0, 0.35)],
             [V(-0.15, 0, 0.5), V(-0.05, 0, 0.5), V(0.05, 0, 0.5), V(0.15, 0, 0.5)]]
    W.node("tree", t0, parent="isle_centre", kind="holo")
    with W.on("tree"):
        tube(A, [t0, t0 + tiers[0][0]], 0.011, sides=4)
        for p in tiers[1]:
            tube(A, [t0 + tiers[0][0], t0 + p], 0.007, sides=3)
        for k, p in enumerate(tiers[2]):
            tube(A, [t0 + tiers[1][k // 2], t0 + p], 0.006, sides=3)
        flat_ring(A, t0 + V(0, 0, 0.003), 0.08, 0.01, segs=16)
        for tier in tiers:                          # the badges' rims, always there
            for p in tier:
                flat_ring(A, t0 + p + V(0, -0.004, 0), 0.036, 0.007, segs=6, rot=(90, 0, 0))
    for i, tier in enumerate(tiers):
        lit = 0.6 + i * 0.9                            # each tier lights a little after the last
        W.node(f"tier_{i + 1}", t0 + tier[0], parent="tree", kind="holo",
               idle=lambda t, lit=lit: Matrix.Identity(4) if lit <= t <= 3.6 else Matrix.Scale(0.001, 4))
        with W.on(f"tier_{i + 1}"):
            for p in tier:
                prism("holo_white", t0 + p + V(0, 0.004, 0), 0.026, 0.01, n=6, rot=(90, 0, 0))
                ball(A, t0 + p + V(0, -0.006, 0), 0.012, segs=5, rings=2)
    # sparring
    S = sat(W, "isle_dojo", 35, 0.68, 0.18, 0.52, seed=93, trees=1, clear=0.12, drip_m=A, kinds=("round",))
    dm = S.at(0.04, 0.03)
    with W.on("isle_dojo"), wk.scaled(1.3, dm):
        prism("wood", dm, 0.012, 0.13, n=6)
        box("wood", dm + V(0, 0, 0.1), (0.1, 0.014, 0.014))
        ball("sand", dm + V(0, 0, 0.15), 0.025, segs=8, rings=4)
        prism("red", dm + V(0, 0, 0.06), 0.022, 0.03, n=8)
    bp = S.at(-0.07, -0.05)
    bot(W, "student", bp, face=facing(bp, dm, 0.0), s=1.25, tip=A, parent="isle_dojo",
        arms=(lambda t: rx(-80 * ease("snap", min(1, (t % 1.0) / 0.15)) * (1 - smooth01((t % 1.0 - 0.3) / 0.5))),
              lambda t: rx(-30) @ ry(20)))
    # scrolls
    P = sat(W, "isle_scrolls", 150, 0.68, 0.16, 0.5, seed=94, trees=2, clear=0.06, drip_m=A,
            kinds=("round",))
    sp = P.at(0, 0, 0.2)
    W.node("scrolls", sp, parent="isle_scrolls", idle=chain(bob(0.015, 2.0), swing(10, 4.0, axis="Z")))
    with W.on("scrolls"), wk.scaled(1.5, sp):
        for k, (dx, dz, a) in enumerate([(-0.04, 0.0, 15), (0.04, 0.05, -20), (0.0, -0.06, 70)]):
            c = sp + V(dx, 0, dz)
            prism("paper", c + V(-0.045, 0, 0), 0.016, 0.09, n=8, rot=(0, 90, a))
            for e in (-1, 1):
                ball("wood", c + V(e * 0.05 * math.cos(rad(a)), e * 0.05 * math.sin(rad(a)), 0), 0.009,
                     segs=6, rings=3)
            prism("violet", c + V(-0.004 * math.cos(rad(a)), -0.004 * math.sin(rad(a)), 0), 0.017, 0.008,
                  n=8, rot=(0, 90, a))
    W.node("arcs", sp, kind="holo")
    a_, b_ = sp + V(0.04, -0.02, 0.07), t0 + tiers[2][0] + V(-0.03, 0, 0.0)
    with W.on("arcs"):
        arc(a_, b_, 0.1, m=A)
    glint(W, "lesson", arc_pts(a_, b_, 0.1, 14), period=2.0, r=0.011)
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.18, 0.01), parent="isle_centre")


def smooth01(u):
    u = 0.0 if u < 0 else 1.0 if u > 1 else u
    return u * u * (3 - 2 * u)


# ================================================================== plugins, themes & clients (extend)
@world("plugins-themes-clients", "extend")
def plugins(W):
    """Giant jigsaw pieces clicking together, a plug finding its socket, and a fan of colour swatches."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.0, 0.4, 0.3, sides=12, seed=101)
    T = C.top
    W.preview_t = 2.0
    L = 0.24
    pa = V(-0.14, 0.05, T + L / 2 + 0.002)
    with W.on("isle_centre"):
        scatter(C, 6, seed=102, ring_=(0.7, 0.92), arc=(20, 340), avoid=lambda x, y: abs(y - 0.05) < 0.09
                and abs(x) < 0.34 or math.hypot(x - 0.05, y + 0.2) < 0.1)
        slab("violet", pa + V(0, 0.02, 0), jigsaw_pts(L, (0, 1, 0, 0)), 0.04, rot=(90, 0, 0))
        slab("yellow", C.at(0.05, -0.2, 0.0), jigsaw_pts(0.13, (1, 0, -1, 1)), 0.03, rot=(0, 0, 12))
    # piece B slides in, clicks, holds, and pulls away again
    pb = V(pa.x + L, pa.y, pa.z)

    def slide(t):
        if t < 1.1:
            u = ease("inout", t / 1.1)
        elif t < 3.0:
            u = 1.0
        else:
            u = 1 - ease("inout", (t - 3.0) / 1.0)
        bump = 0.006 * pulse(t, 1.1, 0.05, 0.0, 0.2)
        return Matrix.Translation((0.12 * (1 - u), 0, bump))

    W.node("piece", pb, parent="isle_centre", idle=slide)
    with W.on("piece"):
        slab("mint", pb + V(0, 0.02, 0), jigsaw_pts(L, (0, 0, 0, -1)), 0.04, rot=(90, 0, 0))
    jp = V(pa.x + L / 2, pa.y - 0.03, pa.z)

    def spark(t):
        k = pulse(t, 1.08, 0.06, 0.05, 0.3)
        return Matrix.Scale(max(0.001, k * (1 + 0.6 * smooth01((t - 1.08) / 0.4))), 4)

    W.node("click", jp, parent="isle_centre", kind="holo", idle=spark)
    with W.on("click"):
        for k in range(8):
            a = TAU * k / 8
            d = V(math.cos(a), 0, math.sin(a))
            tube(A, [jp + d * 0.03, jp + d * 0.07], 0.004, sides=3)
    # plug and socket, side-on to us
    S = sat(W, "isle_socket", 330, 0.68, 0.18, 0.38, seed=103, trees=1, clear=0.13, drip_m=A)
    so = S.at(0.07, 0.0)
    K = 1.5
    with W.on("isle_socket"), wk.scaled(K, so):
        box("cream", so + V(0, 0, 0.05), (0.05, 0.08, 0.1))
        for dy in (-0.017, 0.017):
            box("graphite", so + V(-0.026, dy, 0.055), (0.004, 0.008, 0.022))
    pl = so + V(-0.065, 0, 0.055) * K

    def plug(t):
        if t < 0.6:
            u = 0.0
        elif t < 1.0:
            u = ease("in", (t - 0.6) / 0.4)
        elif t < 2.8:
            u = 1.0
        else:
            u = 1 - ease("inout", min(1.0, (t - 2.8) / 0.6))
        return Matrix.Translation(((0.06 * u - 0.03) * K, 0, 0))

    W.node("plug", pl, parent="isle_socket", idle=plug)
    with W.on("plug"), wk.scaled(K, pl):
        box("graphite", pl + V(-0.02, 0, 0), (0.04, 0.05, 0.04))
        for dy in (-0.017, 0.017):
            box("brass", pl + V(0.01, dy, 0), (0.026, 0.006, 0.016))
        tube("graphite", [pl + V(-0.04, 0, 0), pl + V(-0.07, 0, -0.01), pl + V(-0.09, -0.02, -0.04),
                          pl + V(-0.1, -0.05, -0.052)], 0.008, sides=5)
    W.node("socket_glow", so + V(0, 0, 0.11 * K), parent="isle_socket", kind="holo",
           idle=lambda t: Matrix.Identity(4) if 1.0 <= t < 2.8 else Matrix.Scale(0.001, 4))
    with W.on("socket_glow"):
        ball(A, so + V(0, 0, 0.12 * K), 0.016, segs=6, rings=3)
        flat_ring(A, so + V(0, 0, 0.101 * K), 0.04, 0.008, segs=12)
    # swatches
    P = sat(W, "isle_swatches", 150, 0.68, 0.17, 0.52, seed=104, trees=2, clear=0.08, drip_m=A)
    pin = P.at(0, 0, 0.03)
    W.node("swatches", pin, parent="isle_swatches", idle=swing(10, 2.0, axis="Y"))
    with W.on("swatches"), wk.scaled(1.4, pin):
        for k, m in enumerate(["red", "orange", "yellow", "mint", "blue", "violet"]):
            a = -50 + 20 * k
            box(m, pin + V(math.sin(rad(a)) * 0.07, 0.003 * k, math.cos(rad(a)) * 0.07), (0.035, 0.004, 0.14),
                rot=(0, a, 0))
        ball("brass", pin + V(0, -0.012, 0), 0.008, segs=6, rings=3)
    W.node("arcs", jp, kind="holo")
    for k, I in enumerate((S, P)):
        a_, b_ = jp + V(0, 0, 0.14), I.at(0, 0, 0.22)
        with W.on("arcs"):
            arc(a_, b_, 0.12, m=A)
        glint(W, f"link_{k + 1}", arc_pts(a_, b_, 0.12, 14), period=2.0, phase=k * 0.5, r=0.011)
    rings(W, A)
    W.anchor("anchor_centre", C.at(0, -0.15, 0.01), parent="isle_centre")


# ==================================================================================== frameworks (build)
@world("frameworks-sdks", "build")
def frameworks(W):
    """A building going up: a steel frame in scaffolding, a tower crane swinging a beam over it, the
    blueprint glowing on the grass, and an agent in a hard hat."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.02, 0.42, 0.3, sides=12, seed=111)
    T = C.top
    f0 = V(0.06, 0.08, T)
    fw, fd, fh = 0.22, 0.16, 0.12
    with W.on("isle_centre"):
        scatter(C, 4, seed=112, ring_=(0.75, 0.9), arc=(150, 330))
        box("stone", f0 + V(0, 0, 0.006), (fw + 0.04, fd + 0.04, 0.014))
        xs, ys = (-fw / 2, 0, fw / 2), (-fd / 2, fd / 2)
        for x in xs:
            for y in ys:
                box("blue", f0 + V(x, y, 0.012 + fh * 1.5), (0.012, 0.012, fh * 3))
        for lv in (1, 2, 3):
            z = 0.012 + fh * lv
            for y in ys:
                box("blue", f0 + V(0, y, z), (fw + 0.012, 0.012, 0.012))
            for x in xs:
                box("blue", f0 + V(x, 0, z), (0.012, fd, 0.012))
        box("stone", f0 + V(0, 0, 0.012 + fh + 0.008), (fw, fd, 0.006))
        # scaffolding on its front
        for x in (-fw / 2 - 0.01, 0, fw / 2 + 0.01):
            box("yellow", f0 + V(x, -fd / 2 - 0.04, 0.012 + fh), (0.006, 0.006, fh * 2))
        for lv in (0.6, 1.4):
            box("wood", f0 + V(0, -fd / 2 - 0.04, 0.012 + fh * lv), (fw + 0.03, 0.03, 0.006))
        # the crane's mast
        m0 = V(-0.22, 0.12, T)
        box("graphite", m0 + V(0, 0, 0.01), (0.06, 0.06, 0.02))
        box("yellow", m0 + V(0, 0, 0.32), (0.03, 0.03, 0.6))
        for k in range(6):
            box("orange", m0 + V(0, -0.016, 0.06 + 0.1 * k), (0.03, 0.003, 0.004), rot=(0, 45, 0))
        # the blueprint on the grass
    bp = C.at(-0.1, -0.2, 0.004)
    W.node("blueprint", bp, parent="isle_centre", kind="holo")
    with W.on("blueprint"):
        flat_ring(A, bp, 0.1, 0.006, segs=4, rot=(0, 0, 45))
        for k in range(-2, 3):
            box(A, bp + V(k * 0.028, 0, 0), (0.003, 0.11, 0.001))
            box(A, bp + V(0, k * 0.022, 0), (0.11, 0.003, 0.001))
        box(A, bp + V(0, 0, 0.12), (0.06, 0.002, 0.07), rot=(0, 0, 0))
        frame(A, bp + V(0, 0, 0.12), 0.08, 0.09, 0.005)
    # the jib swings about the mast, the hook rides on it
    jt = m0 + V(0, 0, 0.62)
    W.node("jib", jt, parent="isle_centre", idle=swing(22, 4.0, axis="Z", bias=-8))
    with W.on("jib"):
        box("yellow", jt + V(0.17, 0, 0.015), (0.42, 0.025, 0.025))
        box("yellow", jt + V(-0.07, 0, 0.015), (0.14, 0.025, 0.02))
        box("graphite", jt + V(-0.12, 0, -0.01), (0.05, 0.035, 0.04))
        box("cream", jt + V(0.0, -0.025, -0.02), (0.04, 0.03, 0.035))
        prism("yellow", jt + V(0, 0, 0.03), 0.012, 0.06, n=4, r_top=0.002)
        tube("graphite", [jt + V(0, 0, 0.09), jt + V(0.36, 0, 0.03)], 0.0015, sides=3)
        tube("graphite", [jt + V(0, 0, 0.09), jt + V(-0.13, 0, 0.03)], 0.0015, sides=3)
    hk = jt + V(0.28, 0, 0.0)

    def hoist(t):
        return Matrix.Translation((0, 0, -0.03 - 0.03 * math.cos(TAU * t / 4.0))) @ rx(4 * math.sin(TAU * t / 2.0))

    W.node("hook", hk, parent="jib", idle=hoist)
    with W.on("hook"):
        tube("graphite", [hk, hk + V(0, 0, -0.16)], 0.0018, sides=3)
        box("graphite", hk + V(0, 0, -0.165), (0.012, 0.012, 0.012))
        box("blue", hk + V(0, 0, -0.18), (0.16, 0.014, 0.014))
    # an agent in a hard hat, and the site's stock
    S = sat(W, "isle_yard", 330, 0.7, 0.18, 0.36, seed=113, trees=1, clear=0.12, drip_m=A)
    with W.on("isle_yard"):
        for k in range(3):
            box("blue", S.at(0.03, 0.06 - 0.005 * k, 0.008 + 0.014 * k), (0.15, 0.014, 0.014), rot=(0, 0, 8 * k))
        cone = S.at(0.08, -0.05)
        prism("orange", cone, 0.028, 0.085, n=8, r_top=0.005)
        prism("white", cone + V(0, 0, 0.034), 0.019, 0.017, n=8, r_top=0.015)
        box("orange", cone + V(0, 0, 0.002), (0.07, 0.07, 0.005))
    hb = S.at(-0.05, -0.04)
    bot(W, "builder", hb, face=facing(hb, C.c, 0.5), s=1.3, tip=A, parent="isle_yard",
        idle=swing(8, 2.0, axis="Z"))
    with W.on("builder"), wk.scaled(1.3, hb):
        lathe("yellow", hb + V(0, 0, 0.142), [(0.052, 0.0), (0.05, 0.012), (0.042, 0.03), (0.024, 0.045),
                                              (0.0, 0.05)], 10)
    P = sat(W, "isle_bricks", 150, 0.68, 0.16, 0.52, seed=114, trees=2, clear=0.07, drip_m=A)
    with W.on("isle_bricks"):
        for k in range(6):
            box("red", P.at(-0.025 + 0.03 * (k % 3), 0.0, 0.01 + 0.02 * (k // 3)), (0.028, 0.05, 0.018))
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.18, 0.01), parent="isle_centre")


# ======================================================================== harnesses & runtime (build)
@world("harnesses-runtime-infra", "build")
def harnesses(W):
    """The engine room: a turbine tower with a spinning fan, pipes to its tanks, gauges whose needles
    twitch, steam from the stack, meshing gears and a rack of blinking lights."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.02, 0.4, 0.3, sides=12, seed=121)
    T = C.top
    tw = V(0.0, 0.1, T)
    with W.on("isle_centre"):
        scatter(C, 4, seed=122, ring_=(0.78, 0.92), arc=(190, 350))
        prism("stone", tw - V(0, 0, 0.004), 0.13, 0.02, n=12)
        prism("metal", tw, 0.1, 0.36, n=12)
        for z in (0.06, 0.34):
            prism("graphite", tw + V(0, 0, z), 0.104, 0.018, n=12)
        lathe("metal", tw + V(0, 0, 0.36), [(0.1, 0.0), (0.085, 0.03), (0.0, 0.045)], 12)
        prism("graphite", tw + V(0.04, 0.03, 0.38), 0.022, 0.12, n=8)
        for sx in (-1, 1):
            tk = V(sx * 0.24, 0.0, T)
            lathe("cream", tk, [(0.0, 0.0), (0.05, 0.0), (0.06, 0.03), (0.06, 0.13), (0.045, 0.16),
                                (0.0, 0.17)], 10)
            tube("brass", [tk + V(-sx * 0.055, 0, 0.09), tk + V(-sx * 0.1, 0.0, 0.09),
                           tw + V(sx * 0.098, 0.0, 0.09)], 0.011, sides=6)
            tube("brass", [tk + V(-sx * 0.04, 0, 0.03), tw + V(sx * 0.07, -0.07, 0.03)], 0.008, sides=6)
        # gauges on posts
        for k, gx in enumerate((-0.13, 0.13)):
            gp = V(gx, -0.13, T)
            prism("graphite", gp, 0.006, 0.12, n=5, top=False, bottom=False)
            prism("cream", gp + V(0, 0.006, 0.14), 0.035, 0.012, n=14, rot=(90, 0, 0))
            torus("graphite", gp + V(0, -0.006, 0.14), 0.035, 0.004, rot=(90, 0, 0), segs=14, sides=4)
            flat_ring("mint", gp + V(0, -0.0065, 0.14), 0.026, 0.006, segs=6, rot=(90, -90, 0), arc=TAU / 4)
            flat_ring("red", gp + V(0, -0.0065, 0.14), 0.026, 0.006, segs=4, rot=(90, 0, 0), arc=TAU / 8)
    for k, gx in enumerate((-0.13, 0.13)):
        gc = V(gx, -0.13 - 0.008, T + 0.14)

        def needle(t, k=k):
            base = 20 if k == 0 else -10
            return Matrix.Rotation(rad(base + 30 * math.sin(TAU * t / 2.0 + k) + 6 * math.sin(TAU * t / 0.25)),
                                   4, "Y")

        W.node(f"needle_{k + 1}", gc, parent="isle_centre", idle=needle)
        with W.on(f"needle_{k + 1}"):
            box("red", gc + V(0, 0, 0.012), (0.004, 0.003, 0.026))
            ball("graphite", gc, 0.005, segs=6, rings=3)
    # the turbine on the tower's face
    tc = tw + V(0, -0.11, 0.2)
    with W.on("isle_centre"):
        torus("graphite", tc, 0.08, 0.008, rot=(90, 0, 0), segs=16, sides=4)
        tube("graphite", [tc + V(0, 0.01, 0), tc + V(0, 0.03, 0)], 0.012, sides=6)
    W.node("turbine", tc, parent="isle_centre", idle=spin(2, "Y"))
    with W.on("turbine"):
        prism("metal", tc + V(0, 0.004, 0), 0.016, 0.022, n=8, rot=(90, 0, 0), r_top=0.004)
        for k in range(5):
            a = 360 * k / 5
            M = wk.place(tc, (0, a, 0))
            box("cream", (0.04, 0, 0), (0.06, 0.004, 0.022), rot=(25, 0, 0)).data.transform(M)
    # steam from the stack
    st = tw + V(0.04, 0.03, 0.47)
    for k in range(2):
        def puff(t, k=k):
            u = ((t / 2.0) + k * 0.5 + 0.25) % 1.0
            s = 0.4 + 1.2 * u
            return Matrix.Translation((0.04 * u, 0.02 * u, 0.24 * u)) @ Matrix.Scale(max(0.001, s * (1 - u ** 4)), 4)

        W.node(f"steam_{k + 1}", st, parent="isle_centre", kind="holo", idle=puff)
        with W.on(f"steam_{k + 1}"):
            ico("holo_white", st, 0.05, seed=k, subdiv=1)
    # gears
    G = sat(W, "isle_gears", 35, 0.68, 0.18, 0.52, seed=123, trees=1, clear=0.12, drip_m=A)
    g1, g2 = G.at(-0.04, 0.0, 0.085), G.at(0.074, 0.0, 0.06)
    with W.on("isle_gears"):
        prism("graphite", G.at(-0.04, 0.012), 0.006, 0.08, n=4, top=False, bottom=False)
        prism("graphite", G.at(0.074, 0.012), 0.006, 0.055, n=4, top=False, bottom=False)
    W.node("gear_1", g1, parent="isle_gears", idle=spin(3 / 10, "Y"), cyclic=False)
    with W.on("gear_1"):
        slab("metal", g1 + V(0, 0.01, 0), gear_pts(10, 0.07, 0.056), 0.02, rot=(90, 0, 0))
        prism("graphite", g1 + V(0, -0.012, 0), 0.016, 0.006, n=10, rot=(90, 0, 0))   # (its turn's symmetry)
    W.node("gear_2", g2, parent="isle_gears", idle=spin(-3 / 7, "Y", phase=0.5 / 7), cyclic=False)
    with W.on("gear_2"):
        slab("brass", g2 + V(0, 0.01, 0), gear_pts(7, 0.05, 0.037), 0.02, rot=(90, 0, 0))
        prism("graphite", g2 + V(0, -0.012, 0), 0.012, 0.006, n=7, rot=(90, 0, 0))
    # the rack
    R = sat(W, "isle_rack", 150, 0.68, 0.16, 0.5, seed=124, trees=2, clear=0.07, drip_m=A)
    rk = R.at(0, 0)
    with W.on("isle_rack"):
        box("graphite", rk + V(0, 0, 0.08), (0.08, 0.06, 0.16))
        for k in range(4):
            box("black", rk + V(0, -0.031, 0.025 + 0.035 * k), (0.068, 0.003, 0.026))
    for k in range(2):
        W.node(f"leds_{k + 1}", rk + V(0, -0.034, 0.08), parent="isle_rack", kind="holo",
               idle=blink(0.5, k * 0.5, 0.5))
        with W.on(f"leds_{k + 1}"):
            for j in range(4):
                ball(A if (j + k) % 2 else "holo_white", rk + V(-0.022 + 0.014 * k, -0.034, 0.03 + 0.035 * j),
                     0.005, segs=5, rings=3)
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.2, 0.01), parent="isle_centre")


# ======================================================================= context, memory & rag (data)
@world("context-memory-rag", "data")
def memory(W):
    """The sheet's MEMORY / RETRIEVE: cards of memory floating over stepped islands, a filing cabinet, and
    a glowing path that runs up from the reader and fetches one card down."""
    A = W.accent
    I1 = isle_node(W, "isle_low", -0.36, -0.26, 0.24, 0.22, sides=11, seed=131)
    I2 = isle_node(W, "isle_mid", 0.06, 0.06, 0.32, 0.36, sides=12, seed=132)
    I3 = isle_node(W, "isle_high", 0.48, 0.4, 0.2, 0.52, sides=10, seed=133)
    with W.on("isle_low"):
        scatter(I1, 3, seed=134, avoid=lambda x, y: math.hypot(x - I1.x - 0.04, y - I1.y - 0.02) < 0.11)
        drip(I1, 2, seed=1, m=A, length=0.08)
        cb = I1.at(0.04, 0.03)
    KC = 1.35
    with W.on("isle_low"), wk.scaled(KC, cb):
        box("cream", cb + V(0, 0, 0.065), (0.08, 0.07, 0.13))
        for k in range(2):
            box("stone", cb + V(0, -0.036, 0.03 + 0.042 * k), (0.068, 0.004, 0.034))
    dr = cb + V(0, -0.036, 0.114) * KC
    W.node("drawer", dr, parent="isle_low", idle=shuttle([dr, dr + V(0, -0.05, 0)], dr, (0.2, 0.6), (2.6, 3.0)))
    with W.on("drawer"), wk.scaled(KC, cb):
        box("stone", cb + V(0, -0.04, 0.114), (0.068, 0.012, 0.034))
        box("brass", cb + V(0, -0.048, 0.114), (0.024, 0.006, 0.006))
        quad("paper", cb + V(0, -0.03, 0.135), 0.05, 0.02)
    with W.on("isle_mid"):
        scatter(I2, 6, seed=135, ring_=(0.65, 0.9), arc=(-70, 210))
        drip(I2, 2, seed=2, m=A, length=0.1)
    with W.on("isle_high"):
        scatter(I3, 2, seed=136)
        drip(I3, 2, seed=3, m=A, length=0.08)
    # the cards, fanned over the middle island and one over the high one
    st = V(0.06, 0.16, 0.66)
    W.node("cards", st, kind="holo", idle=bob(0.012, 2.0))
    with W.on("cards"):
        for k, (dx, dy, dz, rz_) in enumerate([(-0.17, 0.04, -0.02, 18), (-0.06, 0.02, 0.03, 6),
                                               (0.06, 0.03, 0.06, -6), (0.17, 0.05, 0.0, -18)]):
            card(st + V(dx * 1.2, dy, dz), 0.145, 0.18, rot=(-10, 0, rz_), lines=3, head=A if k % 2 else None,
                 seed=k)
        card(I3.at(0, 0, 0.22), 0.12, 0.15, rot=(-10, 0, -30), lines=3, seed=9)
        card(I1.at(-0.08, -0.02, 0.2), 0.11, 0.14, rot=(-10, 0, 25), lines=2, seed=7)
    # the path, from the disc's front edge up through the islands to the cards
    path = [V(0.24, -0.86, 0.014), V(0.24, -0.5, 0.014), V(0.24, -0.27, I2.top + 0.006),
            V(0.02, -0.06, I2.top + 0.006), V(0.02, 0.1, 0.5), V(0.0, 0.135, 0.56)]
    W.node("path", path[0], kind="holo")
    with W.on("path"):
        tube(A, path, 0.008, sides=4)
        flat_ring(A, path[0], 0.03, 0.008, segs=12)
    glint(W, "pulse", path, period=2.0, m="holo_white", r=0.013)
    # the retrieved card: out of the stack, down the path to the reader, and back
    rc = st + V(0.0, -0.02, -0.05)
    route = [rc, V(0.02, -0.06, I2.top + 0.14), V(0.24, -0.3, I2.top + 0.12)]
    W.node("recall", rc, kind="holo", idle=shuttle(route, rc, (0.4, 1.6), (2.8, 3.8)))
    with W.on("recall"):
        card(rc, 0.12, 0.15, rot=(-12, 0, 0), lines=3, head=A, seed=4, ml="holo_white")
    rings(W, A)
    W.anchor("anchor_centre", I2.at(0.0, -0.1, 0.01), parent="isle_mid")


# ========================================================================= creative, voice & media (data)
@world("creative-voice-media", "data")
def creative(W):
    """A little media stage: speakers that thump, spotlights crossing, a disco ball throwing specks, a mic
    at the front, sound rings, notes, and a clapperboard. The stage's middle is left clear for a dance."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.46, 0.28, sides=13, seed=141)
    sc = C.at(0, 0.0)
    with W.on("isle_centre"):
        scatter(C, 4, seed=142, ring_=(0.84, 0.95), arc=(200, 340))
        prism("black", sc - V(0, 0, 0.004), 0.3, 0.04, n=16)
        prism("graphite", sc - V(0, 0.27, 0.004), 0.12, 0.02, n=4, ry=0.07)
        mic = sc + V(-0.12, -0.19, 0.036)
        prism("graphite", mic, 0.028, 0.008, n=8)
        tube("graphite", [mic, mic + V(0, 0, 0.16), mic + V(0.016, -0.026, 0.2)], 0.004, sides=4)
        ball("metal", mic + V(0.021, -0.034, 0.21), 0.017, segs=6, rings=4, scale=(1, 1, 1.3))
        for sx in (-1, 1):
            lp = sc + V(sx * 0.17, 0.25, 0.036)
            prism("graphite", lp, 0.007, 0.3, n=5, top=False, bottom=False)
            prism("graphite", lp, 0.02, 0.008, n=8)
    W.node("rim", sc + V(0, 0, 0.037), parent="isle_centre", kind="holo")
    with W.on("rim"):
        flat_ring(A, sc + V(0, 0, 0.037), 0.285, 0.012, segs=32)
    for k, sx in enumerate((-1, 1)):
        sp = sc + V(sx * 0.33, 0.06, 0.0)
        W.node(f"speaker_{k + 1}", sp, parent="isle_centre", idle=throb(0.05, 0.5, k * 0.5, (1, 1, 0.6)))
        with W.on(f"speaker_{k + 1}"):
            speaker(sp, 0.09, 0.075, 0.17)
            speaker(sp + V(0, 0, 0.17), 0.075, 0.065, 0.1, cones=1)
        rp = sp + V(0, -0.045, 0.09)

        def ring_out(t, k=k):
            u = ((t / 1.0) + k * 0.5 + 0.25) % 1.0        # (no ring is born on the loop's seam)
            return Matrix.Scale(max(0.001, (0.4 + 1.4 * u) * (1 - u ** 6)), 4)

        W.node(f"sound_{k + 1}", rp, parent="isle_centre", kind="holo", idle=ring_out)
        with W.on(f"sound_{k + 1}"):
            flat_ring(A, rp, 0.06, 0.006, segs=20, rot=(90, 0, 0))
            flat_ring(A, rp, 0.09, 0.004, segs=20, rot=(90, 0, 0))
        lamp = sc + V(sx * 0.17, 0.25, 0.35)

        def sweep(t, sx=sx):
            return rz(sx * 14 * math.sin(TAU * t / 4.0))

        W.node(f"spot_{k + 1}", lamp, parent="isle_centre", idle=sweep)
        with W.on(f"spot_{k + 1}"):
            d = (sc + V(-sx * 0.03, -0.02, 0.04) - lamp).normalized()
            prism("graphite", lamp - d * 0.02, 0.022, 0.05, n=8, rot=wk.geo.basis(d), r_top=0.028)
            glow_cone(A, lamp + d * 0.03, sc + V(-sx * 0.03, -0.02, 0.04), 0.085, n=10)
    # the disco ball, over the clear middle
    db = sc + V(0, 0.02, 0.62)
    W.node("disco", db, parent="isle_centre", idle=spin(1))
    with W.on("disco"):
        ico("mirror", db, 0.065, seed=1, subdiv=2, jitter=0.0)
        tube("graphite", [db, db + V(0, 0, 0.12)], 0.002, sides=3)
    W.node("specks", sc + V(0, 0, 0.037), parent="isle_centre", kind="holo", idle=spin(-1 / 8), cyclic=False)
    with W.on("specks"):
        for k in range(16):
            a = TAU * k / 16
            r = 0.11 + 0.1 * (k % 2)
            prism("holo_white", sc + V(r * math.cos(a), r * math.sin(a), 0.039), 0.009, 0.001, n=8)
    # notes rising
    for k in range(2):
        n0 = sc + V((-1) ** k * 0.36, 0.0, 0.25)

        def rise(t, k=k):
            u = ((t / 2.0) + k * 0.5 + 0.25) % 1.0
            return Matrix.Translation((0.02 * math.sin(TAU * u), 0, 0.3 * u)) @ \
                Matrix.Scale(max(0.001, smooth01(u / 0.15) * (1 - smooth01((u - 0.8) / 0.2))), 4)

        W.node(f"note_{k + 1}", n0, parent="isle_centre", kind="holo", idle=rise)
        with W.on(f"note_{k + 1}"):
            note(n0, 0.06, A)
    # the clapperboard
    S = sat(W, "isle_film", 215, 0.72, 0.17, 0.33, seed=143, trees=1, clear=0.1, drip_m=A, depth=0.22)
    cp = S.at(0.0, 0.0)
    KF = 1.5
    with W.on("isle_film"), wk.scaled(KF, cp):
        box("black", cp + V(0, 0, 0.05), (0.12, 0.012, 0.09), rot=(0, 0, 20))
        for k in range(3):
            box("white", cp + V(-0.03 + 0.03 * k, -0.007, 0.07), (0.012, 0.002, 0.02), rot=(0, 0, 20))
    hinge = cp + V(-0.056, -0.02, 0.097) * KF
    def clap(t):
        u = t % 2.0
        a = 28 * smooth01(u / 1.2) if u < 1.6 else 28 * (1 - ease("snap", min(1.0, (u - 1.6) / 0.08)))
        return Matrix.Rotation(rad(a), 4, Vector((-math.sin(rad(20)), math.cos(rad(20)), 0)))

    W.node("clapper", hinge, parent="isle_film", idle=clap)
    with W.on("clapper"), wk.scaled(KF, hinge):
        box("black", hinge + wk.rot3((0, 0, 20)) @ V(0.06, 0.0, 0.008), (0.12, 0.012, 0.016), rot=(0, 0, 20))
        for k in range(4):
            box("white", hinge + wk.rot3((0, 0, 20)) @ V(0.015 + 0.03 * k, -0.007, 0.008), (0.012, 0.002, 0.016),
                rot=(0, -30, 20))
    rings(W, A)
    W.anchor("anchor_stage", sc + V(0, 0, 0.036), parent="isle_centre")


# ======================================================================= docs, learning & lists (data)
@world("docs-learning-lists", "data")
def docs(W):
    """A library island whose buildings are giant books, lights on in their windows, a checklist unrolling
    and ticking itself off, and a mortarboard floating over a pencil."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.04, 0.42, 0.3, sides=12, seed=151)
    books = [(-0.26, 0.1, 0.06, 0.26, "red", -10), (-0.17, 0.14, 0.07, 0.34, "blue", -4),
             (-0.07, 0.16, 0.055, 0.29, "mint", 0), (0.02, 0.15, 0.075, 0.38, "violet", 3),
             (0.12, 0.13, 0.06, 0.24, "yellow", 8)]
    with W.on("isle_centre"):
        scatter(C, 5, seed=152, ring_=(0.78, 0.94), arc=(150, 380),
                avoid=lambda x, y: math.hypot(x - 0.21, y + 0.13) < 0.12)
        for x, y, th, h, m, f in books:
            book(C.at(x, y, -0.002), th, 0.14, h, m, face=f)
        # one lying flat, one open like a tent
        box("orange", C.at(0.24, 0.02, 0.012), (0.1, 0.15, 0.024), rot=(0, 0, -20))
        box("paper", C.at(0.244, 0.02, 0.013), (0.094, 0.142, 0.02), rot=(0, 0, -20))
        for s_ in (-1, 1):
            box("pink", C.at(-0.14 + s_ * 0.032, -0.14, 0.04), (0.07, 0.11, 0.006), rot=(0, s_ * 55, 10))
        tube("graphite", [C.at(-0.14, -0.2, 0.068), C.at(-0.14, -0.08, 0.068)], 0.003, sides=3)
    W.node("windows", C.c, parent="isle_centre", kind="holo", idle=blink(2.0, 0.0, 0.85))
    with W.on("windows"):
        rng = random.Random(5)
        for x, y, th, h, m, f in books:
            for k in range(2):
                z = h * (0.38 + 0.24 * k)
                p = C.at(x, y, z) + wk.rot3((0, 0, f)) @ V(0, -0.072, 0)
                quad("holo_white" if rng.random() < 0.6 else A, p, th * 0.4, 0.022, rot=(0, 0, f))
    # the checklist: a roller in the air, a sheet that unrolls, ticks that land as it does
    W.preview_t = 2.8
    rl = C.at(0.21, -0.17, 0.44)
    KS = 1.4
    W.node("roller", rl, parent="isle_centre", kind="solid", idle=bob(0.01, 4.0))
    with W.on("roller"), wk.scaled(KS, rl):
        prism("paper", rl + V(-0.07, 0, 0), 0.016, 0.14, n=8, rot=(0, 90, 0))
        for e in (-1, 1):
            ball("wood", rl + V(e * 0.077, 0, 0), 0.011, segs=6, rings=3)

    def unroll(t):
        if t < 2.4:
            u = ease("out", t / 2.4)
        elif t < 3.3:
            u = 1.0
        else:
            u = 1 - ease("inout", (t - 3.3) / 0.7)
        return Matrix.Diagonal((1, 1, max(0.05, u), 1))

    W.node("sheet", rl, parent="roller", idle=unroll)
    with W.on("sheet"), wk.scaled(KS, rl):
        quad("paper", rl + V(0, -0.012, -0.12), 0.13, 0.24)
        quad("paper", rl + V(0, -0.0115, -0.12), 0.13, 0.24, rot=(0, 0, 180))
        for k in range(3):
            z = -0.05 - k * 0.065
            box("graphite", rl + V(-0.04, -0.014, z), (0.02, 0.003, 0.02))
            box("stone", rl + V(0.02, -0.014, z), (0.07, 0.002, 0.008))
    for k in range(3):
        at = 0.9 + 0.55 * k
        W.node(f"tick_{k + 1}", rl + V(-0.04, -0.02, -0.05 - k * 0.065) * KS, parent="roller", kind="holo",
               idle=lambda t, at=at: Matrix.Scale(1.0 if at <= t < 3.3 else 0.001, 4) @
               Matrix.Scale(1 + 0.4 * pulse(t, at, 0.05, 0.0, 0.2), 4))
        with W.on(f"tick_{k + 1}"), wk.scaled(KS, rl):
            check(rl + V(-0.038, -0.02, -0.048 - k * 0.065), 0.036, A)
    # the pencil, and the cap over it
    S = sat(W, "isle_pencil", 35, 0.68, 0.17, 0.52, seed=153, trees=2, clear=0.1, drip_m=A)
    pp = S.at(-0.02, 0.0)
    with W.on("isle_pencil"):
        M = wk.place(pp, (0, 30, 20), 1.3)
        for ob in (prism("yellow", (0, 0, 0.03), 0.017, 0.16, n=6), prism("wood", (0, 0, 0.19), 0.017, 0.03, n=6,
                                                                        r_top=0.005),
                   prism("graphite", (0, 0, 0.22), 0.005, 0.008, n=6, r_top=0.0),
                   prism("metal", (0, 0, 0.012), 0.018, 0.018, n=8), prism("pink", (0, 0, -0.012), 0.017, 0.024, n=8)):
            ob.data.transform(M)
    cap = S.at(0.02, 0.0, 0.32)
    W.node("cap", cap, parent="isle_pencil", idle=chain(bob(0.02, 2.0), swing(12, 4.0, axis="Z")))
    with W.on("cap"), wk.scaled(1.4, cap):
        prism("black", cap, 0.04, 0.03, n=10)
        box("black", cap + V(0, 0, 0.032), (0.11, 0.11, 0.006), rot=(0, 0, 45))
        tube(A, [cap + V(0, 0, 0.036), cap + V(0.05, -0.03, 0.033), cap + V(0.06, -0.035, -0.01)], 0.003, sides=3)
        ball(A, cap + V(0.06, -0.035, -0.016), 0.008, segs=6, rings=3)
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.16, 0.01), parent="isle_centre")


# ============================================================== sandbox, security & governance (trust)
@world("sandbox-security-governance", "trust")
def sandbox(W):
    """An agent playing in a literal sandbox, inside a fenced yard, under a hexagonal shield, behind a
    padlocked gate; a watchtower's searchlight sweeps, and a gavel keeps order."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.02, 0.42, 0.3, sides=12, seed=161)
    yc = C.at(0, 0.02)
    hw = 0.2
    with W.on("isle_centre"):
        scatter(C, 4, seed=162, ring_=(0.82, 0.95))
        # the fence: posts and two rails, a gap at the front for the gate
        corners = [V(-hw, -hw, 0), V(hw, -hw, 0), V(hw, hw, 0), V(-hw, hw, 0)]
        for i in range(4):
            a, b = corners[i], corners[(i + 1) % 4]
            n = 5
            for k in range(n):
                p = a.lerp(b, k / n)
                if i == 0 and abs(p.x) < 0.05:
                    continue
                box("wood", yc + p + V(0, 0, 0.035), (0.012, 0.012, 0.07))
            for z in (0.025, 0.055):
                if i == 0:
                    for s_ in (-1, 1):
                        box("wood", yc + V(s_ * (hw + 0.05) / 2, -hw, z), (hw - 0.05, 0.006, 0.01))
                else:
                    box("wood", yc + (a + b) / 2 + V(0, 0, z), ((b - a).length if i % 2 == 0 else 0.006,
                                                             (b - a).length if i % 2 else 0.006, 0.01))
        for s_ in (-1, 1):
            box("stone", yc + V(s_ * 0.05, -hw, 0.045), (0.02, 0.02, 0.09))
            ball("stone", yc + V(s_ * 0.05, -hw, 0.095), 0.013, segs=6, rings=3)
        box("wood", yc + V(0, -hw, 0.04), (0.08, 0.01, 0.06))
        # the sandbox, its castle, its bucket and spade
        sb = yc + V(0.02, 0.04, 0)
        for k in range(4):
            a = 90 * k
            box("wood", sb + wk.rot3((0, 0, a)) @ V(0, -0.08, 0.012), (0.17, 0.014, 0.024), rot=(0, 0, a))
        box("sand", sb + V(0, 0, 0.012), (0.15, 0.15, 0.018))
        ca = sb + V(0.03, 0.03, 0.02)
        box("sand", ca + V(0, 0, 0.018), (0.05, 0.05, 0.036))
        for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            prism("sand", ca + V(dx * 0.025, dy * 0.025, 0), 0.01, 0.05, n=6)
            prism("sand", ca + V(dx * 0.025, dy * 0.025, 0.05), 0.012, 0.018, n=6, r_top=0.0)
        prism("red", sb + V(-0.05, 0.045, 0.02), 0.014, 0.03, n=8, r_top=0.019)
        box("metal", sb + V(-0.05, -0.04, 0.025), (0.016, 0.006, 0.02), rot=(30, 0, 30))
        tube("wood", [sb + V(-0.05, -0.04, 0.03), sb + V(-0.03, -0.075, 0.07)], 0.003, sides=4)
    bp = yc + V(-0.03, 0.02, 0.022)
    bot(W, "sandboxed", bp, face=-30, s=1.05, tip=A, parent="isle_centre", idle=hop(0.01, 0.0, 1.0, 0.3),
        arms=(lambda t: rx(-30 - 30 * max(0.0, math.sin(TAU * t))), lambda t: rx(-20)))
    # the padlock on the gate
    lk = yc + V(0, -hw - 0.016, 0.07)
    W.node("padlock", lk, parent="isle_centre", idle=swing(10, 2.0, axis="Y"))
    with W.on("padlock"), wk.scaled(1.9, lk):
        torus("metal", lk + V(0, 0, -0.005), 0.016, 0.004, rot=(90, 0, 0), segs=10, sides=4, arc=math.pi)
        box("brass", lk + V(0, 0, -0.025), (0.042, 0.016, 0.034))
        ball("black", lk + V(0, -0.009, -0.022), 0.005, segs=5, rings=3)
    # the shield: hexagonal tiles on a dome
    R = 0.36
    dc = yc + V(0, 0, 0.0)
    W.node("shield", dc, parent="isle_centre", kind="holo", idle=throb(0.015, 2.0))
    with W.on("shield"):
        cell = 0.105
        g = wk.Mesh()
        for qq in range(-5, 6):
            for rr in range(-5, 6):
                cx = cell * math.sqrt(3) * (qq + rr / 2)
                cy = cell * 1.5 * rr
                rho = math.hypot(cx, cy)
                if rho > R * math.pi / 2 * 0.98:
                    continue

                def onto(x, y):
                    rh = math.hypot(x, y)
                    th = min(rh / R, math.pi / 2)
                    ph = math.atan2(y, x)
                    return dc + V(R * math.sin(th) * math.cos(ph), R * math.sin(th) * math.sin(ph),
                                  R * math.cos(th) * 0.92)

                ring_ = [onto(cx + cell * 0.82 * math.cos(TAU * j / 6 + math.pi / 6),
                              cy + cell * 0.82 * math.sin(TAU * j / 6 + math.pi / 6)) for j in range(6)]
                if min(p.z for p in ring_) < dc.z + 0.01:
                    continue
                idx = g.ring(ring_)
                g.fan(idx, g.add(onto(cx, cy)), A)
        g.build("shield")
        flat_ring(A, dc + V(0, 0, 0.004), R * 1.0, 0.01, segs=36)
    # the watchtower and its searchlight
    S = sat(W, "isle_tower", 35, 0.68, 0.17, 0.52, seed=163, trees=1, clear=0.1, drip_m=A)
    tw = S.at(0, 0)
    KT = 1.3
    with W.on("isle_tower"), wk.scaled(KT, tw):
        for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            tube("wood", [tw + V(dx * 0.04, dy * 0.04, 0), tw + V(dx * 0.025, dy * 0.025, 0.16)], 0.005, sides=4)
        box("wood", tw + V(0, 0, 0.17), (0.08, 0.08, 0.012))
        box("cream", tw + V(0, 0, 0.2), (0.07, 0.07, 0.05))
        prism("red", tw + V(0, 0, 0.225), 0.065, 0.045, n=4, r_top=0.0)
    lt = tw + V(0, -0.04, 0.21) * KT
    W.node("searchlight", lt, parent="isle_tower", idle=swing(40, 4.0, axis="Z", bias=-25))
    with W.on("searchlight"):
        prism("graphite", lt, 0.015, 0.025, n=8, rot=(110, 0, 0))
        glow_cone(A, lt + V(0, -0.02, -0.006), lt + V(0, -0.3, -0.12), 0.06, n=8)
    # the gavel
    G = sat(W, "isle_court", 150, 0.68, 0.16, 0.5, seed=164, trees=2, clear=0.07, drip_m=A)
    gb = G.at(0, 0)
    KG = 1.6
    with W.on("isle_court"), wk.scaled(KG, gb):
        prism("wood", gb, 0.04, 0.016, n=10)
        box("red", gb + V(0.06, 0.02, 0.012), (0.05, 0.07, 0.024), rot=(0, 0, 10))
    pv = gb + V(-0.06, 0.0, 0.03) * KG

    def tap(t):
        u = t % 1.0
        a = -35 * smooth01(u / 0.6) if u < 0.6 else -35 * (1 - ease("in", (u - 0.6) / 0.15)) if u < 0.75 else 0
        return ry(a)

    W.node("gavel", pv, parent="isle_court", idle=tap)
    with W.on("gavel"), wk.scaled(KG, pv):
        tube("wood", [pv, pv + V(0.07, 0, 0.0)], 0.004, sides=4)
        prism("wood", pv + V(0.07, -0.024, 0.0), 0.014, 0.048, n=8, rot=(-90, 0, 0))
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.26, 0.01), parent="isle_centre")


# ========================================================================= observability & evals (trust)
@world("observability-evals", "trust")
def observability(W):
    """Dashboards: a live line graph on a floating panel, bars rising and falling, a gauge, a radar sweep,
    and a magnifying glass following a bug round its island."""
    A = W.accent
    C = isle_node(W, "isle_centre", 0.0, 0.02, 0.41, 0.3, sides=12, seed=171)
    with W.on("isle_centre"):
        scatter(C, 4, seed=172, ring_=(0.8, 0.94), arc=(200, 340))
        box("graphite", C.at(-0.12, -0.08, 0.008), (0.25, 0.08, 0.016))
        for sx in (-1, 1):
            tube("graphite", [C.at(sx * 0.18, 0.18), C.at(sx * 0.18, 0.18, 0.2)], 0.005, sides=4)
    gp = C.at(0.19, -0.1)
    KG = 1.4
    with W.on("isle_centre"), wk.scaled(KG, gp):
        prism("graphite", gp, 0.006, 0.12, n=5, top=False, bottom=False)
        prism("cream", gp + V(0, 0.006, 0.15), 0.05, 0.012, n=14, rot=(90, 0, 0))
        torus("graphite", gp + V(0, -0.006, 0.15), 0.05, 0.005, rot=(90, 0, 0), segs=14, sides=4)
        flat_ring("mint", gp + V(0, -0.0065, 0.15), 0.038, 0.008, segs=4, rot=(90, -120, 0), arc=rad(60))
        flat_ring("yellow", gp + V(0, -0.0065, 0.15), 0.038, 0.008, segs=3, rot=(90, -60, 0), arc=rad(60))
        flat_ring("red", gp + V(0, -0.0065, 0.15), 0.038, 0.008, segs=3, rot=(90, 0, 0), arc=rad(60))
    gc = gp + V(0, -0.008, 0.15) * KG
    W.node("needle", gc, parent="isle_centre",
           idle=lambda t: ry(-10 + 35 * math.sin(TAU * t / 4.0) + 4 * math.sin(TAU * t / 0.2)))
    with W.on("needle"), wk.scaled(KG, gc):
        box("graphite", gc + V(0, 0, 0.018), (0.005, 0.003, 0.036))
        ball("red", gc, 0.007, segs=6, rings=3)
    for k, (m, h, ph) in enumerate([("red", 0.14, 0.0), ("yellow", 0.21, 0.25), ("mint", 0.1, 0.5),
                                    ("blue", 0.17, 0.75)]):
        bb = C.at(-0.21 + 0.058 * k, -0.08, 0.016)
        W.node(f"bar_{k + 1}", bb, parent="isle_centre",
               idle=lambda t, ph=ph: Matrix.Diagonal((1, 1, 0.75 + 0.3 * math.sin(TAU * (t / 2.0 + ph)), 1)))
        with W.on(f"bar_{k + 1}"):
            box(m, bb + V(0, 0, h / 2), (0.042, 0.05, h))
    # the panel and its live graph
    pc = C.at(0, 0.18, 0.32)
    pw, ph_ = 0.4, 0.22
    W.node("panel", pc, parent="isle_centre", kind="holo", idle=bob(0.006, 2.0))
    with W.on("panel"):
        quad("holo_panel", pc, pw, ph_)
        frame("holo_cyan", pc + V(0, -0.001, 0), pw, ph_, 0.007)
        for k in range(1, 4):
            quad("holo_cyan", pc + V(0, -0.0015, -ph_ / 2 + k * ph_ / 4), pw - 0.03, 0.0025)
    graph = [pc + V(-pw / 2 + 0.02 + (pw - 0.04) * k / 9, -0.003, -ph_ / 2 + 0.03 + h) for k, h in
             enumerate([0.03, 0.07, 0.05, 0.11, 0.08, 0.13, 0.09, 0.16, 0.12, 0.17])]
    with W.on("panel"):
        tube(A, graph, 0.005, sides=3)
    glint(W, "live", graph, period=2.0, m="holo_white", r=0.012, parent="panel")
    # the radar
    S = sat(W, "isle_radar", 35, 0.68, 0.18, 0.52, seed=173, trees=1, clear=0.13, drip_m=A)
    rc = S.at(0, 0, 0.03)
    with W.on("isle_radar"):
        prism("graphite", S.at(0, 0, -0.002), 0.12, 0.03, n=14)
    W.node("scope", rc, parent="isle_radar", kind="holo")
    with W.on("scope"):
        for r in (0.04, 0.075, 0.11):
            flat_ring(A, rc + V(0, 0, 0.002), r, 0.004, segs=24)
        box(A, rc + V(0, 0, 0.002), (0.22, 0.003, 0.001))
        box(A, rc + V(0, 0, 0.002), (0.003, 0.22, 0.001))
    W.node("sweep", rc, parent="isle_radar", kind="holo", idle=spin(-2))
    with W.on("sweep"):
        g = wk.Mesh()
        idx = g.ring([rc + V(0.11 * math.cos(-a), 0.11 * math.sin(-a), 0.004) for a in
                      [rad(50) * k / 6 for k in range(7)]])
        c0 = g.add(rc + V(0, 0, 0.004))
        for k in range(6):
            g.face((c0, idx[k + 1], idx[k]), A)
        g.build("sweep")
    W.node("blips", rc, parent="isle_radar", kind="holo", idle=blink(1.0, 0.3, 0.4))
    with W.on("blips"):
        for a, r in ((30, 0.06), (160, 0.09), (250, 0.035)):
            ball("holo_white", rc + polar(a, r, 0.006), 0.009, segs=5, rings=3)
    # the bug and the glass that follows it
    B = sat(W, "isle_bug", 150, 0.68, 0.17, 0.5, seed=174, trees=2, clear=0.1, drip_m=A)
    bc = B.at(0, 0, 0.0)
    loop = [bc + V(0.07 * math.cos(a), 0.05 * math.sin(a), 0) for a in [TAU * k / 12 for k in range(12)]]
    W.node("bug", loop[0], parent="isle_bug", idle=along(loop, loop[0], 4.0, face=True))
    b0 = loop[0]
    with W.on("bug"), wk.scaled(1.6, b0):
        ball("red", b0 + V(0, 0, 0.014), 0.02, segs=8, rings=4, scale=(0.9, 1.25, 0.6))
        box("black", b0 + V(0, 0, 0.022), (0.002, 0.045, 0.002))
        ball("black", b0 + V(0, -0.027, 0.012), 0.011, segs=6, rings=3)
        for sx in (-1, 1):
            for k, dy in enumerate((-0.012, 0.0, 0.012)):
                tube("black", [b0 + V(sx * 0.014, dy, 0.01), b0 + V(sx * 0.03, dy * 1.6, 0.0)], 0.0022, sides=3)
            tube("black", [b0 + V(sx * 0.004, -0.035, 0.016), b0 + V(sx * 0.014, -0.05, 0.03)], 0.0018, sides=3)
        for sx, sy in ((-1, 1), (1, -1), (1, 1)):
            ball("black", b0 + V(sx * 0.008, sy * 0.008, 0.024), 0.004, segs=5, rings=3)
    mg = bc + V(0, 0, 0.19)
    loop2 = [mg + V(0.07 * math.cos(a), 0.05 * math.sin(a), 0.01 * math.sin(2 * a)) for a in
             [TAU * k / 12 - 0.35 for k in range(12)]]
    W.node("magnifier", loop2[0], parent="isle_bug", idle=along(loop2, loop2[0], 4.0))
    with W.on("magnifier"):
        magnifier(loop2[0], 0.07, rot=(-20, 0, 40))
    rings(W, A)
    W.anchor("anchor_centre", C.at(0.0, -0.22, 0.01), parent="isle_centre")


# ==================================================================================== mcp servers (connect)
def connector(p, s, m="holo_cyan"):
    """The sheet's connector cube: a glowing cube with dark caps and a socket on its face."""
    p = Vector(p)
    box(m, p, (s, s, s * 0.84))
    box("graphite", p + V(0, 0, s * 0.47), (s * 1.06, s * 1.06, s * 0.1))
    box("graphite", p - V(0, 0, s * 0.47), (s * 1.06, s * 1.06, s * 0.1))
    for dx in (-1, 1):
        box("graphite", p + V(dx * s * 0.17, -s * 0.5, s * 0.05), (s * 0.11, s * 0.04, s * 0.3))


@world("mcp-servers", "connect")
def mcp(W):
    """The sheet's MCP / CONNECT: islands with glowing connector cubes on pedestals, joined to the central
    server by arcs that data packets run along; one has its plug in for real."""
    C = isle_node(W, "isle_centre", 0.0, -0.02, 0.36, 0.32, sides=12, seed=181)
    with W.on("isle_centre"):
        scatter(C, 6, seed=182, avoid=lambda x, y: math.hypot(x - C.x, y - C.y) < 0.12)
        pp = pedestal(C.at(0, 0), 0.09, 0.02, glow="holo_cyan")
    W.node("pillar", pp, parent="isle_centre", kind="holo")
    with W.on("pillar"):
        prism("holo_cyan", pp, 0.022, 0.22, n=8, top=False, bottom=False, smooth_=True)
        beam(C, r=0.045)
    hc = pp + V(0, 0, 0.31)
    W.node("hub", hc, parent="isle_centre", kind="holo", idle=bob(0.012, 2.0))
    with W.on("hub"):
        connector(hc, 0.15)
    sats = [(150, 0.68, 0.56), (40, 0.68, 0.58), (335, 0.72, 0.38), (220, 0.72, 0.36)]
    W.node("arcs", hc, kind="holo")
    for k, (a, d, z) in enumerate(sats):
        S = sat(W, f"isle_{k + 1}", a, d, 0.17, z, seed=183 + k, trees=2, clear=0.08, drip_m="holo_cyan")
        with W.on(f"isle_{k + 1}"):
            sp = pedestal(S.at(0, 0), 0.055, 0.016, glow="holo_cyan")
        cc = sp + V(0, 0, 0.07)
        W.node(f"server_{k + 1}", cc, parent=f"isle_{k + 1}", kind="holo", idle=bob(0.01, 2.0, k / 4))
        with W.on(f"server_{k + 1}"):
            connector(cc, 0.09)
        a_ = hc + (cc - hc).normalized() * 0.06 + V(0, 0, 0.04)
        b_ = cc + V(0, 0, 0.055)
        h = 0.1 if z > 0.45 else 0.14
        with W.on("arcs"):
            arc(a_, b_, h, m="holo_lime")
        glint(W, f"packet_{k + 1}", arc_pts(a_, b_, h, 14), period=2.0, phase=k / 4, m="holo_white", r=0.011,
              shape="cube", spin_=2)
        if k == 3:
            with W.on(f"isle_{k + 1}"):
                pl = S.at(-0.03, -0.06, 0.012)
                box("graphite", pl, (0.04, 0.028, 0.024), rot=(0, 0, 30))
                for dy in (-1, 1):
                    box("brass", pl + wk.rot3((0, 0, 30)) @ V(0.028, dy * 0.008, 0), (0.018, 0.004, 0.008),
                        rot=(0, 0, 30))
                tube("graphite", [pl + V(-0.02, -0.012, 0), S.at(-0.09, -0.1, 0.006), S.at(-0.13, -0.08, 0.004),
                                  S.at(-0.16, -0.07, -0.03), S.at(-0.17, -0.07, -0.09)], 0.007, sides=5)
    with W.on("arcs"):
        flat_ring("holo_lime", (0, 0, 0.006), 0.56, 0.006, segs=48)
    rings(W, "holo_lime")
    W.anchor("anchor_centre", hc, parent="isle_centre")
