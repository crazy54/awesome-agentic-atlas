"""Props that stand, hang or get built: cones, the wall panel, the harness, the loading bar, the drawn door,
the dust bunny, hard hats, the balcony, chairs, the forbidden button, confetti, the control box, stage and
studio lights, the velvet rope, smoke and the disco ball. See props.py for the conventions."""
from __future__ import annotations

import math
import random

from mathutils import Matrix, Vector

import props_kit as K
from props_kit import V, lerp, prop, wobble
from kit import geo

TAU = math.tau


# ------------------------------------------------------------------------------------------- cones
def _cone(p, H):
    P = p.P
    rb, rt, z0 = 0.2 * H, 0.034 * H, 0.05 * H

    def r(z):
        return lerp(rb, rt, (z - z0) / (0.965 * H - z0))

    p.add(K.box("cone-base", (0.29 * H, 0.29 * H, 0.025 * H), P["graphite"], (0, 0, 0.025 * H), bevel=0.012 * H))
    prof = [(0.0, z0), (rb, z0)] + [(r(z), z) for z in (lerp(z0, 0.93 * H, k / 4) for k in range(1, 5))]
    prof += [(rt * 0.85, 0.975 * H), (rt * 0.45, 0.995 * H), (0.0, H)]
    p.add(geo.lathe("cone-body", prof, P["cone"], segs=20, caps=False))
    e = 0.006 * H
    for i, (a, b) in enumerate(((0.36, 0.47), (0.62, 0.7))):
        za, zb = a * H, b * H
        band = [(r(za) - e, za), (r(za) + e * 0.6, za + e * 0.4), (r(za + e) + e, za + e),
                (r(zb - e) + e, zb - e), (r(zb) + e * 0.6, zb - e * 0.4), (r(zb) - e, zb)]
        p.add(geo.lathe(f"cone-band{i}", band, P["white"], segs=20, caps=False))


@prop("traffic-cone", "The unnecessary crew; The blame button (the thing that falls over)",
      "floor, under the middle; 0.42 m tall")
def traffic_cone(p):
    _cone(p, 0.42)


@prop("traffic-cone-small", "The unnecessary crew", "floor, under the middle; 0.26 m tall")
def traffic_cone_small(p):
    _cone(p, 0.26)


@prop("traffic-cone-large", "The unnecessary crew (Brick's)", "floor, under the middle; 0.62 m tall")
def traffic_cone_large(p):
    _cone(p, 0.62)


@prop("tiny-traffic-cone", "Pocket universe, wrong pocket",
      "floor, under the middle; 0.09 m tall, pocket-sized (fits in a palm)")
def tiny_traffic_cone(p):
    _cone(p, 0.09)


# -------------------------------------------------------------------------------------- wall panel
@prop("wall-panel", "The missing screw (it tilts); The tiny inspection (Zip goes behind it)",
      "its back face on the wall (y = 0) at the panel's middle, front towards -Y; 0.9 x 0.6 m. It hangs on "
      "its one remaining screw, top left; the other three corners are empty holes",
      rig="panel (pivots on the top-left screw): tilt (swings down about the wall's normal), lift (swings "
          "up and out about its top edge)")
def wall_panel(p):
    P = p.P
    W, H, D = 0.9, 0.6, 0.04
    piv = V(-W / 2 + 0.055, -D - 0.004, H / 2 - 0.055)
    p.bone("panel", piv, piv + V(0, -0.06, 0), z=(0, 0, 1))
    p.add(K.plate("panel-body", W, H, D, P["ceramic"], (0, -D / 2, 0), r=0.035, bevel=0.01), "panel")
    rim = [V(u, -D - 0.0015, v) for u, v in K.rrect(W - 0.17, H - 0.17, 0.02, 3)]
    p.add(geo.tube("panel-seam", rim, 0.005, P["graphite"], segs=5, caps=False, closed=True), "panel")
    for k in range(3):                                          # vents
        z = 0.06 - k * 0.06
        p.add(K.capsule(f"panel-vent{k}", (0.03, -D - 0.002, z), (0.22, -D - 0.002, z), 0.012, P["lime"], segs=8,
                        rings=2), "panel")
    p.add(K.text("panel-label", "A&P-07", 0.03, P["graphite"], K.on_front((-0.17, -D - 0.0012, -0.12)),
                 fit=(0.18, 0.035)), "panel")
    for sx, sz in ((1, 1), (1, -1), (-1, -1)):                 # the empty holes
        c = V(sx * (W / 2 - 0.055), -D - 0.001, sz * (H / 2 - 0.055))
        p.add(K.cyl(f"panel-hole{sx}{sz}", 0.013, c + V(0, 0.004, 0), c + V(0, -0.0015, 0), P["rubber"], segs=12),
              "panel")
    # the last screw, which stays in the wall
    p.add(K.cyl("panel-screw", 0.019, piv + V(0, 0.006, 0), piv + V(0, -0.006, 0), P["steel"], segs=14,
                bevel=0.005))
    for a in (45, -45):
        p.add(K.box(f"panel-screw-slot{a}", (0.012, 0.002, 0.0025), P["graphite"], piv + V(0, -0.0065, 0),
                    rot=Matrix.Rotation(math.radians(a), 3, (0, 1, 0))))

    def tilt(t):
        a = 24 * K.ease("settle", t / 1.6) if t < 1.6 else 24
        return {"panel": dict(turn=((0, 1, 0), a))}

    def lift(t):
        return {"panel": dict(turn=((1, 0, 0), -70 * K.ease("back", t / 0.8)))}

    p.clip("tilt", 1.8, tilt)
    p.clip("lift", 1.0, lift)
    p.display = ("tilt", 1.8)
    p.view = dict(az=25, el=10)


# ---------------------------------------------------------------------------------- lifting harness
@prop("lifting-harness", "The unnecessary crew (an oversized harness for one tiny button)",
      "hang point (the top of the crane cable) at the origin, everything below; 2.0 m tall, spreader 1.0 m",
      rig="cable (stretches along its length), hook (the block and hook) > bar (spreader, slings, straps and "
          "cradle): sway, lower")
def lifting_harness(p):
    P = p.P
    zc, zh, zr = -0.6, -0.95, -1.0
    p.bone("cable", (0, 0, 0), (0, 0, zc), z=(0, -1, 0))
    p.bone("hook", (0, 0, zc), (0, 0, zh), z=(0, -1, 0))
    p.bone("bar", (0, 0, zr), (0, 0, -1.5), parent="hook", z=(0, -1, 0))
    p.add(geo.tube("harness-cable", [V(0, 0, 0), V(0, 0, zc - 0.02)], 0.011, P["steel"], segs=8), "cable")
    p.add(K.box("harness-block", (0.075, 0.06, 0.1), P["graphite"], (0, 0, zc - 0.1), bevel=0.02), "hook")
    for s in (1, -1):
        p.add(K.plate(f"harness-cheek{s}", 0.14, 0.18, 0.012, P["yellow"], (0, s * 0.066, zc - 0.1), r=0.06,
                      bevel=0.004, rot=Matrix.Rotation(math.pi / 2 * (1 - s), 3, (0, 0, 1))), "hook")
    p.add(K.cyl("harness-sheave", 0.05, (0, -0.075, zc - 0.07), (0, 0.075, zc - 0.07), P["steel"], segs=16), "hook")
    hk = [V(0, 0, zc - 0.19), V(0, 0, zc - 0.28)]
    hk += [V(0.06 - 0.06 * math.cos(a), 0, zc - 0.28 - 0.07 * math.sin(a)) for a in
           (math.pi * k / 8 for k in range(1, 9))]
    hk += [V(0.12, 0, zc - 0.24)]
    p.add(geo.tube("harness-hook", hk, 0.02, P["steel"], radii=[0.022] * (len(hk) - 1) + [0.011], segs=10), "hook")
    p.add(K.box("harness-latch", (0.004, 0.012, 0.045), P["lime"], (0.075, 0, zc - 0.215), bevel=0.003,
                rot=Matrix.Rotation(math.radians(-35), 3, (0, 1, 0))), "hook")
    # the master ring through the hook, slings down to the spreader bar
    p.add(geo.ring("harness-ring", 0.06, 0.014, P["steel"], (0.03, 0, zr + 0.03), (0, 1, 0), segs=20, sides=6),
          "bar")
    zb = -1.3
    for s in (1, -1):
        p.add(geo.sweep(f"harness-sling{s}", [V(0.03 + s * 0.03, 0, zr - 0.02), V(s * 0.46, 0, zb + 0.04)], 0.03,
                        0.005, P["yellow"], segs=8, up=(0, -1, 0)), "bar")
    p.add(K.box("harness-bar", (0.5, 0.045, 0.045), P["orange"], (0, 0, zb), bevel=0.014), "bar")
    for s in (1, -1):
        p.add(K.box(f"harness-bar-cap{s}", (0.035, 0.055, 0.055), P["graphite"], (s * 0.5, 0, zb), bevel=0.012),
              "bar")
    p.add(K.text("harness-wll", "WLL 40 T", 0.05, P["graphite"], K.on_front((0, -0.0465, zb)), fit=(0.3, 0.05)),
          "bar")
    zcr = -1.95
    for sx in (1, -1):
        for sy in (1, -1):
            a, b = V(sx * 0.46, sy * 0.03, zb - 0.04), V(sx * 0.3, sy * 0.19, zcr + 0.03)
            p.add(geo.sweep(f"harness-strap{sx}{sy}", [a, b], 0.03, 0.005, P["yellow"], segs=8,
                            up=(0, -sy, 0)), "bar")
            p.add(K.box(f"harness-buckle{sx}{sy}", (0.036, 0.012, 0.02), P["steel"], a.lerp(b, 0.45), bevel=0.004),
                  "bar")
    p.add(K.plate("harness-cradle", 0.66, 0.44, 0.05, P["graphite"], (0, 0, zcr), r=0.08, bevel=0.015,
                  rot=Matrix.Rotation(math.pi / 2, 3, (1, 0, 0))), "bar")
    rim = [V(u, v, zcr + 0.027) for u, v in K.rrect(0.6, 0.38, 0.06, 3)]
    p.add(geo.tube("harness-cradle-rim", rim, 0.008, P["lime"], segs=5, caps=False, closed=True), "bar")

    def sway(t):
        return {"hook": dict(turn=((1, 0, 0), 2.5 * math.sin(TAU * t / 3.0))),
                "bar": dict(turn=[((1, 0, 0), 3.5 * math.sin(TAU * t / 3.0 - 0.9)),
                                  ((0, 1, 0), 2.0 * math.sin(TAU * t / 3.0 + 0.6))])}

    def lower(t):
        k = K.ease("settle", t / 1.4) if t < 1.4 else 1.0
        drop = 0.8 * k
        return {"cable": dict(scale=(1, 1 + drop / abs(zc), 1)), "hook": dict(move=(0, 0, -drop))}

    p.clip("sway", 3.0, sway, loop=True)
    p.clip("lower", 1.6, lower)
    p.view = dict(az=30, el=12)


# ------------------------------------------------------------------------------------- loading bar
@prop("loading-bar", "The loading-bar tow truck (decorative: shows during a real wait, never reports it)",
      "floor, under its middle, front facing -Y, towed towards +X (the tow ring); 1.5 m long",
      rig="fill (the lime fill, scales from its left end), wheel_front, wheel_back (roll about Y), brake (the "
          "hand-brake lever, pivots about Y): fill, roll, brake_release")
def loading_bar(p):
    P = p.P
    L, H, D, wr = 1.4, 0.26, 0.22, 0.085
    zc = 0.17 + H / 2
    p.add(K.plate("bar-body", L, H, D, P["ceramic"], (0, 0, zc), r=H / 2 - 0.002, bevel=0.03, seg=4))
    p.add(K.plate("bar-track", L - 0.07, H - 0.07, D + 0.012, P["graphite"], (0, 0, zc), r=(H - 0.07) / 2 - 0.002,
                  bevel=0.008, seg=4, steps=1))
    x0 = -L / 2 + 0.06
    p.bone("fill", (x0, 0, zc), (x0 + 0.3, 0, zc), z=(0, 0, 1))
    fl = L - 0.12
    p.add(K.plate("bar-fill", fl, H - 0.12, D + 0.022, P["lime"], (x0 + fl / 2, 0, zc), r=(H - 0.12) / 2 - 0.002,
                  bevel=0.01, seg=4, steps=1), "fill")
    p.add(K.box("bar-chassis", (L * 0.4, 0.07, 0.035), P["graphite"], (0, 0, 0.15), bevel=0.012))
    for name, x in (("wheel_front", 0.45), ("wheel_back", -0.45)):
        p.bone(name, (x, -0.13, wr), (x, -0.23, wr), z=(0, 0, 1))
        for s in (1, -1):
            y = s * (D / 2 + 0.035)
            p.add(K.cyl(f"{name}-tyre{s}", wr, (x, y - 0.03, wr), (x, y + 0.03, wr), P["rubber"], segs=14,
                        bevel=0.02, steps=1), name)
            p.add(K.cyl(f"{name}-hub{s}", 0.042, (x, y + s * 0.025, wr), (x, y + s * 0.037, wr), P["lime"], segs=10,
                        bevel=0.005, steps=1), name)
            p.add(K.box(f"{name}-spoke{s}", (0.036, 0.004, 0.008), P["graphite"], (x, y + s * 0.037, wr)), name)
        p.add(K.cyl(f"{name}-axle", 0.014, (x, -D / 2 - 0.02, wr), (x, D / 2 + 0.02, wr), P["graphite"], segs=8))
    p.add(geo.ring("bar-tow-ring", 0.045, 0.011, P["graphite"], (L / 2 + 0.05, 0, zc - 0.03), (0, 0, 1), segs=16,
                   sides=6))
    p.add(K.box("bar-tow-mount", (0.03, 0.025, 0.02), P["graphite"], (L / 2 + 0.005, 0, zc - 0.03), bevel=0.006))
    # the beacon on the roof, and the hand brake at the back
    p.add(K.cyl("bar-beacon-base", 0.05, (0.35, 0, zc + H / 2 - 0.01), (0.35, 0, zc + H / 2 + 0.02), P["graphite"],
                segs=14))
    p.add(geo.lathe("bar-beacon", [(0.04, 0.0), (0.04, 0.04), (0.03, 0.065), (0.0, 0.075)], P["holo_amber"],
                    (0.35, 0, zc + H / 2 + 0.02), segs=14, caps=False))
    bz = zc + H / 2 - 0.005
    bx = -L / 2 + 0.2
    p.add(K.box("bar-brake-base", (0.04, 0.035, 0.02), P["graphite"], (bx, 0, bz), bevel=0.008))
    p.bone("brake", (bx, 0, bz + 0.01), (bx, 0, bz + 0.2), z=(0, -1, 0))
    tilt = Matrix.Rotation(math.radians(-25), 3, (0, 1, 0))
    top = V(bx, 0, bz) + tilt @ V(0, 0, 0.2)
    p.add(geo.tube("bar-brake-lever", [V(bx, 0, bz + 0.01), top], 0.011, P["graphite"], segs=8), "brake")
    p.add(K.ball("bar-brake-knob", 0.026, P["red"], top, res=4), "brake")

    def fill(t):
        keys = ((0.0, 0.0), (0.6, 0.35), (1.4, 0.38), (1.7, 0.8), (3.0, 0.82), (3.4, 1.0))
        v = keys[-1][1]
        for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
            if t <= t1:
                v = lerp(v0, v1, K.ease("inout", (t - t0) / (t1 - t0)))
                break
        g = max(1e-3, min(1.0, v * 30))                     # an empty bar shows no sliver of lime
        return {"fill": dict(scale=(g, max(1e-3, v), g))}

    def roll(t):
        a = -360 * t                                        # one turn a second: 0.53 m/s along +X
        return {"wheel_front": dict(turn=((0, 1, 0), -a)), "wheel_back": dict(turn=((0, 1, 0), -a))}

    def release(t):
        return {"brake": dict(turn=((0, 1, 0), 50 * K.ease("back", t / 0.4)))}

    p.clip("fill", 3.6, fill)
    p.clip("roll", 1.0, roll, loop=True)
    p.clip("brake_release", 0.6, release)
    p.display = ("fill", 2.0)


# ------------------------------------------------------------------------------------- drawn door
@prop("drawn-door", "The glass door (Archie draws a door on the invisible wall and exits through it)",
      "floor, at the middle of the doorway, facing -Y; 1.0 x 2.3 m in lime marker. The rest pose is fully "
      "drawn: hold frame 0 of `draw` (all strokes at zero) until he starts drawing",
      rig="stroke_left, stroke_top, stroke_right (each grows along itself), leaf (hinged on the left, turns "
          "about Z) > leaf_fill (the door face, wipes in from the hinge), knob: draw, open")
def drawn_door(p):
    P = p.P
    W, H, r = 1.0, 2.3, 0.02
    rng = random.Random(3)

    def wobbly(a, b, n=14, amp=0.008):
        a, b = V(*a), V(*b)
        d = (b - a)
        side = d.cross(V(0, 1, 0)).normalized()
        ph = rng.uniform(0, TAU)
        return [a.lerp(b, k / n) + side * amp * math.sin(ph + k * 0.9) * math.sin(math.pi * k / n)
                for k in range(n + 1)]

    corners = [V(-W / 2, -0.01, 0.0), V(-W / 2, -0.01, H), V(W / 2, -0.01, H), V(W / 2, -0.01, 0.0)]
    for name, a, b in (("stroke_left", corners[0], corners[1]), ("stroke_top", corners[1], corners[2]),
                       ("stroke_right", corners[2], corners[3])):
        p.bone(name, a, b, z=(0, -1, 0))
        pts = wobbly(a, b)
        p.add(geo.tube(name.replace("_", "-"), pts, r, P["lime"], radii=[r * 0.8] + [r] * (len(pts) - 2) + [r * 0.8],
                       segs=8), name)
    hx = -W / 2 + 0.05
    p.bone("leaf", (hx, -0.01, 0.0), (hx, -0.01, H - 0.05), z=(0, -1, 0))
    p.bone("leaf_fill", (hx, -0.01, 0.0), (hx + 0.3, -0.01, 0.0), parent="leaf", z=(0, 0, 1))
    lw, lh = W - 0.1, H - 0.05
    p.add(K.plate("door-face", lw, lh, 0.012, P["holo_door"], (hx + lw / 2, -0.01, lh / 2), r=0.01, bevel=0.003,
                  steps=1), "leaf_fill")
    edge = [V(hx + lw / 2 + u, -0.018, lh / 2 + v) for u, v in K.rrect(lw - 0.03, lh - 0.03, 0.01, 1)]
    p.add(geo.tube("door-edge", edge, 0.007, P["lime"], segs=5, caps=False, closed=True), "leaf_fill")
    kc = V(W / 2 - 0.14, -0.024, 1.05)
    p.bone("knob", kc, kc + V(0, -0.06, 0), parent="leaf", z=(0, 0, 1))
    p.add(geo.ring("door-knob", 0.045, 0.011, P["lime"], kc, (0, -1, 0), segs=18, sides=6), "knob")
    p.add(K.ball("door-knob-dot", 0.016, P["lime"], kc + V(0, -0.004, 0), res=3, scale=(1, 0.5, 1)), "knob")

    def grow(t, t0, t1):
        return max(1e-3, K.ease("inout", (t - t0) / (t1 - t0)))

    def line(k):
        """A stroke `k` of the way drawn: its length grows, its girth pops in over the first touch."""
        g = min(1.0, k * 20)
        return dict(scale=(max(1e-3, g), k, max(1e-3, g)))

    def draw(t):
        fill = grow(t, 1.65, 2.05)
        return {"stroke_left": line(grow(t, 0.0, 0.5)), "stroke_top": line(grow(t, 0.5, 0.85)),
                "stroke_right": line(grow(t, 0.85, 1.35)),
                "knob": dict(scale=(max(1e-3, K.ease("back", (t - 1.4) / 0.25)),) * 3),
                "leaf_fill": dict(scale=(max(1e-3, min(1.0, fill * 20)), fill, 1))}

    def open_(t):
        return {"leaf": dict(turn=((0, 0, 1), -100 * K.ease("inout", t / 0.9)))}

    p.clip("draw", 2.2, draw)
    p.clip("open", 1.0, open_)
    p.display = ("open", 0.45)
    p.view = dict(az=30, el=8)


# ------------------------------------------------------------------------------------- dust bunny
@prop("dust-bunny", "The tiny inspection (Zip emerges wearing it)",
      "floor (or the top of Zip's head), under its middle, eyes towards -Y; 0.95 m across",
      rig="body (squashes and stretches about its base): jiggle")
def dust_bunny(p):
    P = p.P
    rng = random.Random(11)
    jit = {}

    lobes = [(V(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.4, 1)).normalized(), rng.uniform(0.12, 0.22))
             for _ in range(9)]

    def fluff(q, u):
        key = (round(u.x, 3), round(u.y, 3), round(u.z, 3))
        if key not in jit:
            jit[key] = rng.uniform(-1.0, 1.0)
        n = u.normalized()
        k = 0.95 + 0.5 * sum(a * max(0.0, n.dot(d)) ** 5 for d, a in lobes)
        k += 0.03 * math.sin(13 * n.x + 11 * n.y) + 0.065 * jit[key]
        if u.z < -0.2:
            k *= lerp(1.0, 0.8, min(1.0, (-u.z - 0.2) / 0.8))
        return q * k

    zc = 0.36
    p.bone("body", (0, 0, 0), (0, 0, 0.7), z=(0, -1, 0))
    blob = geo.superquad("bunny", (0.42, 0.38, 0.34), P["fluff"], (0, 0, zc), n=2.0, shape=fluff, res=9)
    p.add(blob, "body")
    surf = geo.Surface(blob)
    for k in range(52):                                          # curly wisps of fluff
        d = V(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.3, 1)).normalized()
        hit = surf.toward(V(0, 0, zc) + d * 1.5, (0, 0, zc), offset=-0.012)
        if hit is None:
            continue
        ln = rng.uniform(0.05, 0.11)
        side = d.orthogonal().normalized()
        side = Matrix.Rotation(rng.uniform(0, TAU), 3, d) @ side
        pts = [hit + d * ln * t + side * ln * 0.45 * math.sin(t * 2.6) * t for t in (0.0, 0.35, 0.7, 1.0)]
        p.add(geo.tube(f"bunny-wisp{k}", pts, 0.01, P["fluff"],
                       radii=[0.012, 0.007, 0.004, 0.0008], segs=3, caps=False), "body")
    for s in (1, -1):
        hit = surf.front(s * 0.12, zc + 0.07, offset=-0.022)
        p.add(K.ball(f"bunny-eye{s}", 0.08, P["white"], hit, res=4, scale=(1, 0.8, 1.1)), "body")
        p.add(K.ball(f"bunny-pupil{s}", 0.045, P["black"], hit + V(-s * 0.01, -0.052, -0.01), res=3,
                     scale=(1, 0.6, 1.1)), "body")
        p.add(K.ball(f"bunny-glint{s}", 0.013, P["white"], hit + V(-s * 0.026, -0.078, 0.012), res=2), "body")

    def jiggle(t):
        sq = 0.06 * math.sin(TAU * t / 0.8)
        return {"body": dict(scale=(1 + sq * 0.5, 1 + sq * 0.5, 1 - sq))}

    p.clip("jiggle", 1.6, jiggle, loop=True)


# ---------------------------------------------------------------------------------------- hard hats
def _hard_hat(p, color, W, letter):
    P = p.P
    D, Hd = W * 1.12, W * 0.46

    def dome_shape(q, u):
        z = q.z if u.z > 0 else q.z * 0.02
        return V(q.x, q.y, z)

    dome = geo.superquad("hat-dome", (W / 2, D / 2, Hd), P[color], (0, 0, 0.012), n=2.15, shape=dome_shape, res=7)
    p.add(dome)
    ridge = [V(0, D * 0.42 * math.cos(a), 0.012 + Hd * math.sin(a) * 1.0) for a in
             (math.pi * (0.12 + 0.76 * k / 12) for k in range(13))]
    p.add(geo.sweep("hat-ridge", ridge, W * 0.06, W * 0.035, P[color], n=2.6, segs=8, up=(0, 0, 1)))
    p.add(geo.ring("hat-rim", 1.0, 0.018 / W, P[color], (0, 0, 0.014), (0, 0, 1), segs=32, sides=4, squash=0.7))
    geo.transform(p.parts[-1], Matrix.Translation((0, 0, 0.014)) @ Matrix.Diagonal((W / 2 + 0.008, D / 2 + 0.008,
                                                                                     W, 1.0))
                  @ Matrix.Translation((0, 0, -0.014)))
    p.add(geo.superquad("hat-peak", (W * 0.3, W * 0.15, W * 0.013), P[color], (0, -D / 2 + W * 0.02, 0.02),
                        n=(2.4, 2.2, 2.0), res=3, rot=Matrix.Rotation(math.radians(7), 3, (1, 0, 0))))
    surf = geo.Surface(dome)
    c = surf.front(W * 0.2, Hd * 0.42, offset=0.002)
    n = surf.normal_at(c)
    disc = geo.disc("hat-badge", W * 0.1, 0.006, P["white"], c, n, segs=20)
    p.add(disc)
    p.add(K.text("hat-letter", letter, W * 0.12, P["graphite"],
                 Matrix.Translation(c + n * 0.0045) @ K.facing(n, (0, 0, 1)), fit=(W * 0.12, W * 0.12)))
    p.view = dict(az=30, el=22)


@prop("hard-hat-lime", "The unauthorized renovation (Archie's)",
      "the middle of its opening, front (peak) towards -Y; 0.5 m wide, for Archie's 0.5 m head (rim about "
      "0.1 m above the head's centre; his crest pokes through)")
def hard_hat_lime(p):
    _hard_hat(p, "lime", 0.5, "A")


@prop("hard-hat-violet", "The unauthorized renovation (Zip's)",
      "the middle of its opening, front (peak) towards -Y; 0.66 m wide, for Zip's 0.65 m dome (rim about "
      "0.1 m above the dome's centre; his horns poke through)")
def hard_hat_violet(p):
    _hard_hat(p, "violet", 0.66, "Z")


@prop("hard-hat-orange", "The unauthorized renovation (Brick's)",
      "the middle of its opening, front (peak) towards -Y; 0.68 m wide, for Brick's 0.67 m head (rim about "
      "0.08 m above the head's centre)")
def hard_hat_orange(p):
    _hard_hat(p, "orange", 0.68, "B")


# ------------------------------------------------------------------------------------------ balcony
@prop("balcony", "The unauthorized renovation (a tiny balcony on the README frame)",
      "the middle of the platform's back edge, on its top surface (where it meets the wall), the platform "
      "sticking out towards -Y; 1.4 x 0.6 m, railing 0.55 m",
      rig="platform, bracket_L, bracket_R, rail (each pops in): build")
def balcony(p):
    P = p.P
    W, Dp, T = 1.4, 0.6, 0.07
    p.bone("platform", (0, -Dp / 2, -T / 2), (0, -Dp / 2, 0.1), z=(0, -1, 0))
    for k in range(5):
        y = -Dp * (k + 0.5) / 5
        p.add(K.box(f"balcony-plank{k}", (W / 2, Dp / 10 - 0.005, T / 2), P["wood"], (0, y, -T / 2), bevel=0.008),
              "platform")
    for s, side in ((1, "_L"), (-1, "_R")):
        bn = p.bone("bracket" + side, (s * 0.52, 0, -T), (s * 0.52, 0, -T - 0.3), z=(0, -1, 0))
        tri = [(0.0, 0.0), (-Dp * 0.85, 0.0), (0.0, -0.42)]
        ob = K.poly_mesh(f"balcony-bracket{side}", tri, 0.04, P["graphite"], bevel=0.008)
        geo.transform(ob, Matrix.Translation((s * 0.52, 0, -T)) @ Matrix.Rotation(math.pi / 2, 4, (0, 0, 1)))
        p.add(ob, bn)
    p.bone("rail", (0, -Dp + 0.03, 0), (0, -Dp + 0.03, 0.55), z=(0, -1, 0))
    yf, ys, zr = -Dp + 0.03, -0.03, 0.55
    posts = [V(x, yf, 0) for x in (-0.67, -0.335, 0.0, 0.335, 0.67)] + [V(sx * 0.67, -0.31, 0) for sx in (1, -1)]
    for k, b in enumerate(posts):
        p.add(K.cyl(f"balcony-post{k}", 0.017, b, b + V(0, 0, zr), P["graphite"], segs=10), "rail")
    for k, (a, b) in enumerate(((V(-0.69, yf, zr), V(0.69, yf, zr)), (V(0.67, yf, zr), V(0.67, ys, zr)),
                                (V(-0.67, yf, zr), V(-0.67, ys, zr)))):
        p.add(K.capsule(f"balcony-rail{k}", a, b, 0.03, P["lime"], segs=10, rings=2), "rail")
        m = (a + V(0, 0, -zr * 0.5), b + V(0, 0, -zr * 0.5))
        p.add(K.capsule(f"balcony-mid{k}", m[0], m[1], 0.012, P["graphite"], segs=8, rings=2), "rail")

    def pop(t, t0, d=0.3):
        return max(1e-3, K.ease("back", (t - t0) / d))

    def build(t):
        return {"bracket_L": dict(scale=(pop(t, 0.0),) * 3), "bracket_R": dict(scale=(pop(t, 0.15),) * 3),
                "platform": dict(scale=(pop(t, 0.35),) * 3),
                "rail": dict(scale=(min(1.0, pop(t, 0.7, 0.4) * 8), pop(t, 0.7, 0.4), min(1.0, pop(t, 0.7, 0.4) * 8)))}

    p.clip("build", 1.3, build)
    p.view = dict(az=30, el=22)


# --------------------------------------------------------------------------------------- deck chair
@prop("deck-chair", "The unauthorized renovation (Archie settles into it on the balcony)",
      "floor, under the middle, the sitter facing -Y; 0.72 m wide, 1.05 m tall (Archie-sized)")
def deck_chair(p):
    P = p.P
    xs = 0.34
    top, front, foot = V(0, 0.32, 0.96), V(0, -0.42, 0.42), V(0, -0.3, 0.03)
    for sd in (1, -1):
        x = sd * xs
        # the long frame, front foot to the top of the back; the seat frame, rear foot to the front rail
        for name, a, b, xo in (("deck-frame", foot, top, 0.0), ("deck-seat", V(0, 0.45, 0.03), front, 0.035)):
            a, b = V(x + sd * xo, a.y, a.z), V(x + sd * xo, b.y, b.z)
            p.add(K.box(f"{name}{sd}", (0.02, 0.028, (b - a).length / 2 + 0.02), P["wood"], (a + b) / 2, bevel=0.008,
                        rot=geo.basis(b - a, (0, 1, 0))))
    for a, b, r in ((V(-xs, top.y, top.z), V(xs, top.y, top.z), 0.022),
                    (V(-xs - 0.035, front.y, front.z), V(xs + 0.035, front.y, front.z), 0.022),
                    (V(-xs, foot.y, foot.z + 0.05), V(xs, foot.y, foot.z + 0.05), 0.018)):
        p.add(K.cyl("deck-bar", r, a + V(-0.03, 0, 0), b + V(0.03, 0, 0), P["wood"], segs=10))
    # the canvas: striped strips hung from the top bar to the front bar, sagging under the sitter
    n = 6
    w = (2 * xs - 0.06) / n
    curve = []
    for k in range(13):
        t = k / 12
        q = top.lerp(front, t)
        q.z -= 0.28 * math.sin(math.pi * t) ** 1.3
        q.y += 0.06 * math.sin(math.pi * t)
        curve.append(q)
    for i in range(n):
        x = -xs + 0.03 + w * (i + 0.5)
        pts = [V(x, q.y, q.z) for q in curve]
        p.add(geo.sweep(f"deck-canvas{i}", pts, w / 2 + 0.001, 0.006, P["lime" if i % 2 == 0 else "canvas"], n=4,
                        segs=4, up=(0, -1, 1)))
    p.view = dict(az=-35, el=18)


# ------------------------------------------------------------------------------------ folding chair
@prop("folding-chair", "The union break (Brick and Zip unfold them)",
      "floor, under the middle, the sitter facing -Y; seat 0.46 m up (Zip-sized; scale 1.4 for Brick)",
      rig="front_legs (fold back about X), seat (folds up about its back edge): unfold, fold")
def folding_chair(p):
    P = p.P
    p.skin = False                     # rigid parts on their bones: a page can clone it (a pair of chairs)
    xs = 0.22
    piv = V(0, 0.16, 0.44)
    for s in (1, -1):
        x = s * xs
        p.add(K.capsule(f"fchair-rear{s}", (x, 0.24, 0.015), (x, 0.17, 0.93), 0.014, P["graphite"], segs=8,
                        rings=2))
    p.add(K.plate("fchair-back", 0.46, 0.2, 0.025, P["cream"], (0, 0.18, 0.79), r=0.04, bevel=0.008,
                  rot=Matrix.Rotation(math.radians(-5), 3, (1, 0, 0))))
    p.add(K.capsule("fchair-rear-bar", (-xs, 0.23, 0.12), (xs, 0.23, 0.12), 0.01, P["graphite"], segs=8, rings=2))
    p.bone("front_legs", piv, piv + V(0, -0.2, -0.2), z=(0, 0, 1))
    for s in (1, -1):
        x = s * (xs - 0.025)
        p.add(K.capsule(f"fchair-front{s}", (x, piv.y, piv.z), (x, -0.25, 0.015), 0.013, P["graphite"], segs=8,
                        rings=2), "front_legs")
    p.add(K.capsule("fchair-front-bar", (-xs + 0.025, -0.2, 0.08), (xs - 0.025, -0.2, 0.08), 0.01, P["graphite"],
                    segs=8, rings=2), "front_legs")
    for s in (1, -1):
        p.add(K.ball(f"fchair-foot{s}", 0.018, P["rubber"], (s * (xs - 0.025), -0.25, 0.015), res=2),
              "front_legs")
    sp = V(0, 0.14, 0.465)
    p.bone("seat", sp, sp + V(0, -0.3, 0), z=(0, 0, 1))
    p.add(K.plate("fchair-seat", 0.44, 0.4, 0.035, P["cream"], (0, sp.y - 0.2, sp.z), r=0.06, bevel=0.01,
                  rot=Matrix.Rotation(math.pi / 2, 3, (1, 0, 0))), "seat")
    folded = {"front_legs": dict(turn=((1, 0, 0), 52)), "seat": dict(turn=((1, 0, 0), -84))}

    def at(k):
        return {b: dict(turn=(spec["turn"][0], spec["turn"][1] * k)) for b, spec in folded.items()}

    def unfold(t):
        return at(1 - K.ease("settle", t / 0.9) if t < 0.9 else 0.0)

    def fold(t):
        return at(K.ease("inout", t / 0.7))

    p.clip("unfold", 1.0, unfold)
    p.clip("fold", 0.8, fold)
    p.view = dict(az=-40, el=15)


# ------------------------------------------------------------------------------------- lounge chair
@prop("lounge-chair", "Zip moved in (Zip lounges inside the core)",
      "floor, under the middle, the foot end towards -Y; 1.6 m long (Zip-sized: scale it with him)")
def lounge_chair(p):
    P = p.P
    xs, zs = 0.29, 0.3
    knee, hip, head = V(0, -0.78, zs), V(0, 0.28, zs), V(0, 0.72, 0.78)
    for s in (1, -1):
        x = s * xs
        p.add(K.capsule(f"lounge-rail{s}", (x, knee.y, zs), (x, hip.y, zs), 0.02, P["mint"], segs=8, rings=2))
        p.add(K.capsule(f"lounge-back{s}", (x, hip.y, zs), (x, head.y, head.z), 0.02, P["mint"], segs=8, rings=2))
        for y in (-0.7, 0.2):
            p.add(K.capsule(f"lounge-leg{s}{y}", (x, y, zs), (x, y, 0.02), 0.018, P["mint"], segs=8, rings=2))
    p.add(K.plate("lounge-seat", 0.56, 1.08, 0.07, P["violet"], (0, (knee.y + hip.y) / 2, zs + 0.045), r=0.06,
                  bevel=0.025, rot=Matrix.Rotation(math.pi / 2, 3, (1, 0, 0))))
    ang = math.atan2(head.z - hip.z, head.y - hip.y)
    mid = hip.lerp(head, 0.5)
    p.add(K.plate("lounge-backrest", 0.56, 0.66, 0.07, P["violet"], mid + V(0, -0.03, 0.045), r=0.06, bevel=0.025,
                  rot=Matrix.Rotation(math.pi / 2 + ang, 3, (1, 0, 0))))
    p.add(geo.superquad("lounge-pillow", (0.2, 0.06, 0.08), P["cream"], head + V(0, -0.1, 0.06), n=2.4, res=5,
                        rot=Matrix.Rotation(ang - 0.3, 3, (1, 0, 0))))
    p.view = dict(az=-40, el=22)


# ---------------------------------------------------------------------------------- the forbidden button
@prop("do-not-press", "The forbidden button",
      "floor, under the pedestal, label facing -Y; 1.0 m tall (decorative: no real control is behind it)",
      rig="button (presses down along the console's slope): press")
def do_not_press(p):
    P = p.P
    p.add(K.cyl("dnp-base", 0.2, (0, 0, 0), (0, 0, 0.06), P["graphite"], segs=24, bevel=0.02))
    p.add(K.cyl("dnp-column", 0.1, (0, 0, 0.05), (0, 0, 0.84), P["graphite"], segs=20))
    for z in (0.08, 0.8):
        p.add(geo.ring(f"dnp-trim{z}", 0.1, 0.008, P["lime"], (0, 0, z), (0, 0, 1), segs=20, sides=6))
    tilt = Matrix.Rotation(math.radians(22), 3, (1, 0, 0))
    top = V(0, 0, 0.9)
    p.add(K.box("dnp-console", (0.18, 0.15, 0.04), P["graphite"], top, bevel=0.015, rot=tilt))
    n = tilt @ V(0, 0, 1)
    face = top + n * 0.04
    p.add(geo.lathe("dnp-collar", [(0.085, 0.0), (0.085, 0.012), (0.072, 0.02), (0.0, 0.02)], P["yellow"], face, n,
                    segs=20, caps=False))
    for k in range(6):                                           # hazard stripes on the collar
        a = TAU * k / 6
        side = (tilt @ V(math.cos(a), math.sin(a), 0)) * 0.078
        p.add(K.box(f"dnp-stripe{k}", (0.012, 0.004, 0.006), P["black"], face + side + n * 0.011, bevel=0.002,
                    rot=tilt @ Matrix.Rotation(a + math.pi / 4, 3, (0, 0, 1))))
    p.bone("button", face + n * 0.02, face + n * 0.12, z=(0, -1, 0))
    p.add(geo.lathe("dnp-button", [(0.06, 0.0), (0.06, 0.02), (0.052, 0.04), (0.03, 0.052), (0.0, 0.056)], P["red"],
                    face + n * 0.012, n, segs=22, caps=False), "button")
    p.add(K.plate("dnp-sign", 0.27, 0.15, 0.012, P["white"], (0, -0.106, 0.55), r=0.02, bevel=0.003))
    p.add(K.text("dnp-text", "DO NOT\nPRESS", 0.05, P["red"], K.on_front((0, -0.1135, 0.55)), fit=(0.23, 0.12),
                 line=0.88))

    def press(t):
        k = K.pulse(t, 0.05, 0.08, 0.2, 0.25)
        return {"button": dict(move=tuple(-n * 0.026 * k))}

    p.clip("press", 0.7, press)
    p.view = dict(az=30, el=18)


# ------------------------------------------------------------------------------------------ confetti
@prop("confetti", "The forbidden button (confetti hits only Archie)",
      "the burst point (the pieces fly up and rain down round it); about 1.2 m across at its widest",
      rig="bit_01..10 (one per piece): burst")
def confetti(p):
    P = p.P
    p.skin = True                                  # one mesh: each piece its own bone, all one draw call each
    rng = random.Random(21)
    cols = ["lime", "violet", "mint", "orange", "yellow"]
    pieces = []
    N = 10
    for i in range(N):
        v = V(rng.uniform(-1, 1), rng.uniform(-1, 1), 0)
        v = v.normalized() * rng.uniform(0.4, 1.5) + V(0, 0, rng.uniform(2.6, 3.6))
        axis = V(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)).normalized()
        spin = rng.uniform(180, 360) * rng.choice((1, -1))
        pieces.append((v, axis, spin, rng.uniform(0, TAU)))

    def where(i, t):
        v, axis, spin, ph = pieces[i]
        drag = 1.8
        k = (1 - math.exp(-drag * t)) / drag                   # drag-damped launch
        g = 3.2
        pos = V(v.x * k, v.y * k, v.z * k - g * (t / drag - k / drag))
        pos += V(math.sin(t * 6 + ph), math.cos(t * 5 + ph), 0) * 0.04 * min(1.0, t)
        return pos

    show_t = 0.75
    for i in range(N):
        c = where(i, show_t)
        b = p.bone(f"bit_{i + 1:02d}", c, c + V(0, 0, 0.04), z=(0, -1, 0))
        m = P[cols[i % len(cols)]]
        if i % 3 == 2:
            pts = [c + V(0.022 * math.cos(a), 0.022 * math.sin(a), 0.01 * a) for a in
                   (TAU * 1.2 * k / 10 for k in range(11))]
            ob = geo.tube(f"confetti-curl{i}", pts, 0.007, m, segs=5)
        else:
            ob = K.box(f"confetti-bit{i}", (0.03, 0.003, 0.019), m, c,
                       rot=Matrix.Rotation(rng.uniform(0, TAU), 3, V(rng.uniform(-1, 1), 1, rng.uniform(-1, 1))))
        p.add(ob, b)

    def burst(t):
        out = {}
        for i in range(N):
            _, axis, spin, _ = pieces[i]
            off = where(i, t) - where(i, show_t)
            out[f"bit_{i + 1:02d}"] = dict(move=tuple(off), turn=(tuple(axis), spin * t))
        return out

    p.clip("burst", 2.0, burst)
    p.view = dict(az=30, el=12)


# -------------------------------------------------------------------------------------- control box
@prop("control-box", "The fake crash (Zip inside Archie, operating him with two levers)",
      "floor, under the box, front facing -Y; 0.34 m wide, levers 0.35 m up",
      rig="lever_L, lever_R (tip forward and back about X): operate, panic")
def control_box(p):
    P = p.P
    W, Dd, H = 0.34, 0.22, 0.17
    p.add(K.box("ctrl-box", (W / 2, Dd / 2, H / 2), P["violet"], (0, 0, H / 2), bevel=0.025))
    p.add(K.box("ctrl-top", (W / 2 - 0.03, Dd / 2 - 0.03, 0.006), P["graphite"], (0, 0, H), bevel=0.004))
    for k, (x, m) in enumerate(((-0.1, "holo_red"), (-0.04, "holo_lime"), (0.02, "holo_lamp"))):
        p.add(K.ball(f"ctrl-light{k}", 0.012, P[m], (x, -Dd / 2 - 0.002, H * 0.62), res=3, scale=(1, 0.6, 1)))
    p.add(K.text("ctrl-label", "ARCHIE", 0.03, P["mint"], K.on_front((0.0, -Dd / 2 - 0.0015, H * 0.3)),
                 fit=(0.2, 0.035)))
    for s, side, knob in ((1, "_L", "lime"), (-1, "_R", "red")):
        b0 = V(s * 0.08, 0, H + 0.006)
        p.add(geo.lathe(f"ctrl-boot{side}", [(0.03, 0.0), (0.022, 0.02), (0.012, 0.03), (0.0, 0.03)], P["rubber"], b0,
                        segs=12, caps=False))
        bn = p.bone("lever" + side, b0, b0 + V(0, 0, 0.17), z=(0, -1, 0))
        p.add(K.cyl(f"ctrl-stick{side}", 0.009, b0, b0 + V(0, 0, 0.16), P["steel"], segs=8), bn)
        p.add(K.ball(f"ctrl-knob{side}", 0.026, P[knob], b0 + V(0, 0, 0.17), res=4), bn)

    def operate(t):
        a = 25 * math.sin(TAU * t / 1.2)
        return {"lever_L": dict(turn=((1, 0, 0), a)), "lever_R": dict(turn=((1, 0, 0), -a))}

    def panic(t):
        return {"lever_L": dict(turn=((1, 0, 0), 30 * math.sin(TAU * t * 5))),
                "lever_R": dict(turn=[((1, 0, 0), 28 * math.sin(TAU * t * 6 + 1)), ((0, 1, 0), 8 * math.sin(TAU * t * 4))])}

    p.clip("operate", 1.2, operate, loop=True)
    p.clip("panic", 1.0, panic, loop=True)
    p.display = ("operate", 0.3)


# ------------------------------------------------------------------------------------------ softbox
@prop("softbox", "The apology video (the soft lighting)",
      "floor, under the stand, diffuser facing -Y; 1.75 m tall (the diffuser is holo-soft)")
def softbox(p):
    P = p.P
    for k in range(3):
        a = TAU * k / 3 + math.pi / 2
        foot = V(0.4 * math.cos(a), 0.4 * math.sin(a), 0.02)
        p.add(geo.tube(f"soft-leg{k}", [V(0, 0, 0.55), foot], 0.013, P["graphite"], segs=6))
        p.add(K.ball(f"soft-foot{k}", 0.024, P["rubber"], foot, res=2, scale=(1, 1, 0.6)))
    p.add(K.cyl("soft-pole", 0.02, (0, 0, 0.4), (0, 0, 1.38), P["graphite"], segs=10))
    c = V(0, 0.05, 1.45)
    tilt = Matrix.Rotation(math.radians(12), 4, (1, 0, 0))
    M = Matrix.Translation(c) @ tilt
    body = geo.lathe("soft-body", [(0.08, -0.3), (0.08, -0.24), (0.48, 0.08), (0.48, 0.12)], P["graphite"], segs=4,
                     caps=True, axis=(0, -1, 0), y_hint=(0, 0, 1))
    geo.transform(body, M @ Matrix.Rotation(math.pi / 4, 4, (0, 1, 0)))
    for f in body.data.polygons:
        f.use_smooth = False
    p.add(body)
    p.add(K.plate("soft-diffuser", 0.64, 0.64, 0.012, P["holo_soft"], (0, 0, 0), r=0.015, bevel=0.003, steps=1,
                  rot=None))
    geo.transform(p.parts[-1], M @ Matrix.Translation((0, -0.118, 0)))
    rim = [V(u, -0.126, v) for u, v in K.rrect(0.66, 0.66, 0.02, 1)]
    ob = geo.tube("soft-rim", rim, 0.012, P["lime"], segs=5, caps=False, closed=True)
    p.add(geo.transform(ob, M))
    p.add(K.box("soft-mount", (0.03, 0.06, 0.05), P["graphite"], (0, 0.08, 1.4), bevel=0.01))
    p.view = dict(az=60, el=12)


# -------------------------------------------------------------------------------------- velvet rope
@prop("velvet-rope", "The pocket rave (Brick is the bouncer); The hostile takeover",
      "floor, midway between the two stanchions, the rope across X; 1.3 m wide, 0.95 m tall",
      rig="rope_1..6 (hung between the posts): unhook (the right end drops and swings), sway")
def velvet_rope(p):
    P = p.P
    xs, H = 0.62, 0.92
    for s in (1, -1):
        x = s * xs
        p.add(geo.lathe(f"velvet-base{s}", [(0.0, 0.0), (0.15, 0.0), (0.15, 0.02), (0.11, 0.05), (0.04, 0.07),
                                            (0.0, 0.07)], P["brass"], (x, 0, 0), segs=20, caps=False))
        p.add(K.cyl(f"velvet-post{s}", 0.024, (x, 0, 0.06), (x, 0, H), P["brass"], segs=12))
        p.add(K.ball(f"velvet-finial{s}", 0.042, P["brass"], (x, 0, H + 0.03), res=4))
        p.add(geo.ring(f"velvet-hook{s}", 0.02, 0.006, P["brass"], (x - s * 0.035, 0, H - 0.05), (0, 1, 0), segs=12,
                       sides=4))
    a, b = V(-xs + 0.05, 0, H - 0.07), V(xs - 0.05, 0, H - 0.07)
    nb = 6
    sag = 0.2
    pts = [a.lerp(b, k / nb) - V(0, 0, sag * (1 - (2 * k / nb - 1) ** 2)) for k in range(nb + 1)]
    names = p.chain("rope", pts)
    curve = K.polyline(pts, 30)
    rope = geo.tube("velvet-rope", curve, 0.026, P["velvet"], segs=10)
    p.add(K.skin_chain(rope, names, pts, blend=0.5))
    for i, (q, bn) in enumerate(((pts[0], names[0]), (pts[-1], names[-1]))):
        p.add(K.cyl(f"velvet-clip{i}", 0.03, q + V(-0.02 if i == 0 else 0.02, 0, 0),
                    q + V(0.04 if i == 0 else -0.04, 0, 0), P["brass"], segs=12, bevel=0.008), bn)
    # each link's rest angle below the horizontal, so `unhook` can hang it straight down
    phi = [math.degrees(math.atan2(-(q1.z - q0.z), q1.x - q0.x)) for q0, q1 in zip(pts, pts[1:])]

    def hang(k, swing):
        out, prev = {}, 0.0
        for i, bn in enumerate(names):
            target = (90 - phi[i]) * k + swing * (1 + 0.3 * i)
            out[bn] = dict(turn=((0, 1, 0), target - prev))
            prev = target
        return out

    def unhook(t):
        k = K.ease("in", t / 0.45) if t < 0.45 else 1.0
        return hang(k, wobble(t, 0.45, 14.0, 0.9, 1.6))

    def sway(t):
        return {bn: dict(turn=((1, 0, 0), 3 * math.sin(TAU * t / 2.5) * (1 - abs(2 * i / (nb - 1) - 1))))
                for i, bn in enumerate(names)}

    p.clip("unhook", 2.4, unhook)
    p.clip("sway", 2.5, sway, loop=True)


# ------------------------------------------------------------------------------------------ smoke
@prop("smoke-machine", "The dramatic entrance",
      "floor, under the middle, label facing -Y, nozzle blowing along +X; 0.52 m long")
def smoke_machine(p):
    P = p.P
    W, Dd, H = 0.5, 0.3, 0.24
    zc = 0.03 + H / 2
    p.add(K.box("fog-body", (W / 2, Dd / 2, H / 2), P["graphite"], (0, 0, zc), bevel=0.03))
    for sx in (1, -1):
        for sy in (1, -1):
            p.add(K.cyl(f"fog-foot{sx}{sy}", 0.022, (sx * 0.19, sy * 0.1, 0.0), (sx * 0.19, sy * 0.1, 0.035),
                        P["rubber"], segs=8))
    p.add(K.plate("fog-label", 0.24, 0.1, 0.008, P["lime"], (-0.08, -Dd / 2 - 0.003, zc + 0.02), r=0.02, bevel=0.002,
                  steps=1))
    p.add(K.text("fog-text", "FOG 3000", 0.045, P["graphite"], K.on_front((-0.08, -Dd / 2 - 0.0085, zc + 0.02)),
                 fit=(0.2, 0.05)))
    p.add(K.ball("fog-light", 0.014, P["holo_red"], (0.14, -Dd / 2 - 0.002, zc + 0.05), res=3, scale=(1, 0.6, 1)))
    p.add(K.cyl("fog-dial", 0.025, (0.14, -Dd / 2, zc - 0.03), (0.14, -Dd / 2 - 0.02, zc - 0.03), P["mint"], segs=12))
    for k in range(4):                                            # vents along the side
        p.add(K.capsule(f"fog-vent{k}", (-0.18 + k * 0.05, -0.08, zc + H / 2 + 0.001), (-0.18 + k * 0.05, 0.08,
                                                                                    zc + H / 2 + 0.001),
                        0.008, P["black"], segs=6, rings=1))
    p.add(K.cyl("fog-nozzle", 0.045, (W / 2 - 0.01, 0, zc - 0.02), (W / 2 + 0.07, 0, zc - 0.02), P["steel"], segs=14,
                bevel=0.008))
    p.add(K.cyl("fog-mouth", 0.03, (W / 2 + 0.06, 0, zc - 0.02), (W / 2 + 0.075, 0, zc - 0.02), P["black"], segs=12))
    p.add(geo.ring("fog-nozzle-ring", 0.046, 0.007, P["lime"], (W / 2 + 0.02, 0, zc - 0.02), (1, 0, 0), segs=14,
                   sides=5))
    p.add(geo.tube("fog-handle", [V(-0.12, 0, zc + H / 2 - 0.01), V(-0.1, 0, zc + H / 2 + 0.07),
                                  V(0.1, 0, zc + H / 2 + 0.07), V(0.12, 0, zc + H / 2 - 0.01)], 0.013, P["mint"],
                   segs=8))


@prop("smoke-puff", "The dramatic entrance (the machine's smoke: clone, scale and fade them)",
      "floor, under the middle of the cloud; 0.7 m across (material smoke, alpha-blended: fade its opacity)",
      rig="puff (billows up from its base): billow")
def smoke_puff(p):
    P = p.P
    p.bone("puff", (0, 0, 0), (0, 0, 0.3), z=(0, -1, 0))
    rng = random.Random(4)
    blobs = [((0, 0, 0.17), 0.17), ((0.17, 0.02, 0.12), 0.13), ((-0.18, -0.01, 0.11), 0.12),
             ((0.07, -0.05, 0.29), 0.12), ((-0.08, 0.04, 0.27), 0.11), ((0.28, 0.0, 0.08), 0.08),
             ((-0.28, 0.02, 0.07), 0.075)]
    for k, (c, r) in enumerate(blobs):
        p.add(K.ball(f"puff{k}", r, P["smoke"], c, res=4 if r > 0.1 else 3,
                     scale=(1.1, 0.9 + 0.2 * rng.random(), 0.95)), "puff")

    def billow(t):
        k = K.ease("out", t / 1.5)
        return {"puff": dict(scale=(0.25 + 0.75 * k,) * 3, move=(0, 0, 0.25 * k))}

    p.clip("billow", 1.6, billow)


# --------------------------------------------------------------------------------------- disco ball
@prop("disco-ball", "The pocket rave (Zip's nightclub inside the core)",
      "hang point (the top of its chain) at the origin, the ball below; 0.32 m across (scale it to the core)",
      rig="ball (spins about Z): spin")
def disco_ball(p):
    P = p.P
    p.bone("ball", (0, 0, -0.1), (0, 0, -0.45), z=(0, -1, 0))
    for k in range(4):
        p.add(geo.ring(f"disco-link{k}", 0.012, 0.0035, P["steel"], (0, 0, -0.012 - 0.022 * k),
                       (1, 0, 0) if k % 2 else (0, 1, 0), segs=10, sides=4))
    rings, segs, R = 14, 28, 0.16
    zc = -0.1 - R
    prof = [(R * math.sin(math.pi * k / rings), R * math.cos(math.pi * k / rings)) for k in range(rings + 1)]
    ball = geo.lathe("disco", prof, P["chrome"], (0, 0, zc), segs=segs, caps=False)
    for f in ball.data.polygons:
        f.use_smooth = False
    p.add(ball, "ball")
    p.add(K.cyl("disco-cap", 0.025, (0, 0, -0.1 + 0.008), (0, 0, -0.1 - 0.012), P["graphite"], segs=10), "ball")

    p.clip("spin", 4.0, lambda t: {"ball": dict(turn=((0, 0, 1), 360 * t / 4.0))}, loop=True)
    p.view = dict(az=30, el=10)


# ------------------------------------------------------------------------------------- video camera
@prop("video-camera", "The apology video (who it is recorded on)",
      "floor, under the tripod, lens facing -Y; 1.25 m tall (the REC light is holo-red)")
def video_camera(p):
    P = p.P
    for k in range(3):
        a = TAU * k / 3 - math.pi / 2
        foot = V(0.35 * math.cos(a), 0.35 * math.sin(a), 0.02)
        p.add(geo.tube(f"cam-leg{k}", [V(0, 0, 0.98), foot], 0.014, P["graphite"], segs=6))
        p.add(K.ball(f"cam-foot{k}", 0.02, P["rubber"], foot, res=2))
    p.add(K.cyl("cam-head", 0.04, (0, 0, 0.96), (0, 0, 1.04), P["graphite"], segs=12))
    c = V(0, 0, 1.12)
    p.add(K.box("cam-body", (0.065, 0.13, 0.07), P["ceramic"], c, bevel=0.025))
    p.add(K.cyl("cam-lens", 0.05, c + V(0, -0.12, 0), c + V(0, -0.21, 0), P["graphite"], segs=16, bevel=0.01))
    p.add(geo.ring("cam-lens-ring", 0.05, 0.008, P["lime"], c + V(0, -0.2, 0), (0, -1, 0), segs=16, sides=5))
    p.add(K.cyl("cam-glass", 0.038, c + V(0, -0.2, 0), c + V(0, -0.215, 0), P["lens"], segs=16))
    p.add(K.box("cam-finder", (0.025, 0.05, 0.022), P["graphite"], c + V(0, 0.11, 0.08), bevel=0.008))
    p.add(K.plate("cam-screen", 0.12, 0.08, 0.012, P["graphite"], c + V(0.075, -0.02, 0.005), r=0.01, bevel=0.003,
                  rot=Matrix.Rotation(math.radians(-70), 3, (0, 0, 1))))
    p.add(K.ball("cam-rec", 0.011, P["holo_red"], c + V(0.04, -0.12, 0.05), res=3))
    p.add(geo.tube("cam-strap", [c + V(-0.066, -0.08, 0.03), c + V(-0.075, 0.0, 0.05), c + V(-0.066, 0.08, 0.03)],
                   0.008, P["lime"], segs=6))
    p.view = dict(az=40, el=14)
