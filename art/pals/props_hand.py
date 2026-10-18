"""Props a hand holds: the level, the screw, the marker, the flashlight, the microphone, the stamp, the
remotes, the fishing rod, ropes and cables, spotlights, the duck, the potato and the rest. Handheld props are
built upright with the origin at the grip, +Z along the fingers and the front (-Y) away from the palm (see
props.py)."""
from __future__ import annotations

import math
import random

import bmesh
from mathutils import Matrix, Vector

import props_kit as K
from props_kit import V, lerp, prop, wobble
from kit import geo

TAU = math.tau


# ------------------------------------------------------------------------------------------- level
@prop("level", "The leveling dispute; The world needs leveling",
      "floor: under the middle of its bottom edge, length along X, vial facing -Y; 1.0 m long (Archie holds "
      "one end, Zip the other)",
      rig="bubble (slides along X): measure, tip_left, tip_right")
def level(p):
    P = p.P
    L, H, D = 1.0, 0.085, 0.055
    p.add(K.plate("level-body", L, H, D, P["yellow"], (0, 0, H / 2), r=0.012, bevel=0.008, seg=2))
    for s in (1, -1):
        p.add(K.plate(f"level-cap{s}", 0.05, H + 0.012, D + 0.012, P["graphite"], (s * (L / 2 - 0.02), 0, H / 2),
                      r=0.014, bevel=0.006, seg=2))
    yf = -D / 2
    zc = H / 2
    p.add(K.plate("level-bezel", 0.23, 0.066, 0.014, P["graphite"], (0, yf - 0.004, zc), r=0.03, bevel=0.005))
    yv = yf - 0.016
    p.add(K.capsule("level-vial", (-0.078, yv, zc), (0.078, yv, zc), 0.021, P["holo_lime"], segs=12))
    for s in (1, -1):
        p.add(K.box(f"level-tick{s}", (0.0028, 0.003, 0.024), P["graphite"], (s * 0.031, yv - 0.02, zc)))
    for i in range(-8, 9):                                     # ruler marks, clear of the vial
        x = i * 0.05
        if abs(x) < 0.13 or abs(x) > 0.42:
            continue
        ln = 0.02 if i % 2 == 0 else 0.012
        p.add(K.box(f"level-mark{i}", (0.002, 0.0015, ln / 2), P["graphite"], (x, yf - 0.001, H - 0.008 - ln / 2)))
    p.bone("bubble", (0, yv, zc), (0.05, yv, zc))
    p.add(K.capsule("level-bubble", (-0.01, yv - 0.009, zc), (0.01, yv - 0.009, zc), 0.0125, P["white"], segs=10),
          "bubble")

    def at(x):
        return {"bubble": dict(move=(x, 0, 0))}

    def measure(t):
        if t < 0.7:
            x = 0.05 * K.ease("inout", t / 0.7)
        elif t < 1.5:
            x = lerp(0.05, -0.05, K.ease("inout", (t - 0.7) / 0.8))
        else:
            x = -0.05 * (1 - K.ease("out", (t - 1.5) / 0.6)) + wobble(t, 2.1, 0.008, 2.0, 3.0)
        return at(x)

    p.clip("measure", 3.0, measure)
    p.clip("tip_right", 0.8, lambda t: at(0.05 * K.ease("back", t / 0.5)))
    p.clip("tip_left", 0.8, lambda t: at(-0.05 * K.ease("back", t / 0.5)))
    p.display = ("measure", 0.0)


# ------------------------------------------------------------------------------------------- screw
@prop("screw", "The missing screw", "grip: the screw's middle, head up (+Z); 0.08 m long")
def screw(p):
    P = p.P
    L, rh, hh, rs = 0.075, 0.021, 0.012, 0.0075
    top = L / 2
    p.add(geo.lathe("screw-head", [(0.0, top + hh), (rh * 0.72, top + hh * 0.93), (rh * 0.95, top + hh * 0.55),
                                   (rh, top + hh * 0.18), (rh * 0.88, top), (0.0, top)], P["steel"], segs=20,
                    caps=False))
    for k in range(2):
        p.add(K.box(f"screw-slot{k}", (rh * 0.62, 0.0026, 0.003), P["graphite"], (0, 0, top + hh * 0.93),
                    rot=Matrix.Rotation(math.pi / 2 * k + math.pi / 4, 3, (0, 0, 1))))
    p.add(geo.lathe("screw-shank", [(0.0, -top), (rs * 0.45, -top + 0.006), (rs, -top + 0.016), (rs, top),
                                    (0.0, top)], P["steel"], segs=12, caps=False))
    pts, radii = [], []
    turns, z0, z1 = 5.0, -top + 0.004, top - 0.006
    n = int(turns * 12)
    for i in range(n + 1):
        t = i / n
        z = lerp(z0, z1, t)
        a = TAU * turns * t
        rr = rs * min(1.0, 0.45 + (z - (-top)) / 0.016 * 0.55) + 0.0012
        pts.append(V(rr * math.cos(a), rr * math.sin(a), z))
        radii.append(0.0022 * min(1.0, 0.2 + 4 * t, 0.2 + 4 * (1 - t)))
    p.add(geo.tube("screw-thread", pts, 0.0022, P["steel"], radii=radii, segs=5))
    p.show = Matrix.Translation((0, 0, top)) @ Matrix.Rotation(math.radians(-70), 4, (1, 0, 0))


# ------------------------------------------------------------------------------------------ marker
@prop("marker", "The glass door (Archie draws the door); The sleepy atlas (Zip draws the mustache)",
      "grip: the barrel's middle, nib up (+Z); 0.21 m long, lime ink")
def marker(p):
    P = p.P
    r = 0.019
    p.add(K.cyl("marker-barrel", r, (0, 0, -0.07), (0, 0, 0.055), P["graphite"], segs=18))
    p.add(geo.ring("marker-grip", r, 0.004, P["lime"], (0, 0, -0.005), (0, 0, 1), segs=18, sides=6, squash=3.0))
    p.add(geo.lathe("marker-neck", [(r * 0.98, 0.055), (r * 0.85, 0.07), (0.009, 0.083), (0.0075, 0.087),
                                    (0.0, 0.087)], P["ceramic"], segs=18, caps=False))
    p.add(K.capsule("marker-nib", (0, 0, 0.086), (0, 0, 0.098), 0.0058, P["lime"], segs=10, r2=0.0042))
    # the cap, posted on the back end, with its clip
    p.add(K.cyl("marker-cap", r + 0.0025, (0, 0, -0.105), (0, 0, -0.052), P["lime"], segs=18, bevel=0.006))
    p.add(K.box("marker-clip", (0.005, 0.003, 0.022), P["lime"], (0, -(r + 0.0045), -0.07), bevel=0.002))
    p.add(K.text("marker-label", "ARCHIE", 0.012, P["lime"],
                 Matrix.Translation((0, -r - 0.0012, 0.028)) @ K.facing((0, -1, 0), (0, 0, 1)) @
                 Matrix.Rotation(math.pi / 2, 4, (0, 0, 1)), fit=(0.06, 0.014)))
    p.show = Matrix.Rotation(math.radians(-60), 4, (0, 1, 0)) @ Matrix.Rotation(math.radians(20), 4, (1, 0, 0))


# -------------------------------------------------------------------------------------- flashlight
@prop("flashlight", "The tiny inspection (Zip's light under the panel)",
      "grip: the barrel's middle, beam along +Z; 0.2 m long, beam 0.6 m (node `beam`, material holo-beam)")
def flashlight(p):
    P = p.P
    r = 0.022
    p.add(K.cyl("torch-barrel", r, (0, 0, -0.095), (0, 0, 0.05), P["graphite"], segs=18))
    for k, z in enumerate((-0.075, -0.06, -0.045)):
        p.add(geo.ring(f"torch-knurl{k}", r, 0.003, P["brass"], (0, 0, z), (0, 0, 1), segs=18, sides=5))
    p.add(geo.lathe("torch-head", [(r * 0.95, 0.045), (r, 0.05), (0.04, 0.085), (0.042, 0.095), (0.04, 0.1),
                                   (0.035, 0.1)], P["mint"], segs=20, caps=False))
    p.add(K.cyl("torch-lens", 0.036, (0, 0, 0.093), (0, 0, 0.101), P["holo_lamp"], segs=20, bevel=0.002))
    p.add(K.box("torch-switch", (0.007, 0.006, 0.012), P["red"], (0, -r, 0.005), bevel=0.003))
    p.add(K.cyl("torch-tail", r * 0.9, (0, 0, -0.105), (0, 0, -0.09), P["mint"], segs=18))
    p.add(geo.lathe("torch-beam", [(0.034, 0.102), (0.2, 0.7)], P["holo_beam"], segs=24, caps=False), node="beam")
    p.show = Matrix.Rotation(math.radians(-80), 4, (1, 0, 0)) @ Matrix.Rotation(math.radians(-30), 4, (0, 0, 1))
    p.view = dict(az=40, el=28)


# -------------------------------------------------------------------------------------- microphone
@prop("microphone", "The mic drop", "grip: the handle's middle, head up (+Z); 0.17 m tall (tiny)")
def microphone(p):
    P = p.P
    p.add(geo.lathe("mic-handle", [(0.0, -0.065), (0.009, -0.064), (0.0115, -0.058), (0.016, 0.03), (0.0175, 0.04),
                                   (0.0, 0.04)], P["graphite"], segs=16, caps=False))
    p.add(geo.ring("mic-collar", 0.019, 0.0045, P["lime"], (0, 0, 0.043), (0, 0, 1), segs=16, sides=6))
    p.add(K.ball("mic-head", 0.032, P["steel"], (0, 0, 0.074), res=6))
    p.add(geo.ring("mic-band", 0.0322, 0.0028, P["graphite"], (0, 0, 0.074), (0, 0, 1), segs=20, sides=5))
    p.add(K.box("mic-switch", (0.004, 0.003, 0.009), P["lime"], (0, -0.0145, 0.0), bevel=0.0015))
    p.add(K.cyl("mic-tail", 0.004, (0, 0, -0.072), (0, 0, -0.062), P["rubber"], segs=8))


# ------------------------------------------------------------------------------------ rubber stamp
@prop("rubber-stamp", "The inspection scam",
      "grip: the handle; pad faces down (-Z); 0.17 m tall. The head turns on `head` about X: its bottom face "
      "reads QUALITY CHECKED, after `flip` it reads I LICKED THIS",
      rig="head (flips 180 deg about X): flip, flip_back")
def rubber_stamp(p):
    P = p.P
    zp = -0.04                                   # the head's pivot
    p.add(K.ball("stamp-knob", 0.03, P["lime"], (0, 0, 0.1), res=5, scale=(1, 1, 0.85)))
    p.add(K.cyl("stamp-shaft", 0.012, (0, 0, 0.012), (0, 0, 0.085), P["graphite"], segs=14))
    p.add(K.box("stamp-yoke", (0.078, 0.014, 0.009), P["graphite"], (0, 0, 0.012), bevel=0.004))
    for s in (1, -1):
        p.add(K.box(f"stamp-arm{s}", (0.006, 0.014, 0.03), P["graphite"], (s * 0.074, 0, -0.012), bevel=0.003))
        p.add(K.cyl(f"stamp-pin{s}", 0.009, (s * 0.066, 0, zp), (s * 0.084, 0, zp), P["brass"], segs=12))
    p.bone("head", (0, 0, zp), (0.05, 0, zp))
    p.add(K.box("stamp-block", (0.062, 0.036, 0.018), P["wood"], (0, 0, zp), bevel=0.005), "head")
    for s, body, up in ((-1, "QUALITY\nCHECKED", (0, -1, 0)), (1, "I LICKED\nTHIS", (0, 1, 0))):
        zf = zp + s * 0.0215
        p.add(K.box(f"stamp-pad{s}", (0.058, 0.032, 0.0035), P["cream"], (0, 0, zf), bevel=0.0015), "head")
        p.add(K.text(f"stamp-text{s}", body, 0.02, P["redink"],
                     Matrix.Translation((0, 0, zf + s * 0.0037)) @ K.facing((0, 0, s), up), fit=(0.1, 0.05),
                     line=0.85), "head")

    def flip(t, a=0.0, b=180.0):
        return {"head": dict(turn=((1, 0, 0), lerp(a, b, K.ease("back", t / 0.6))))}

    p.clip("flip", 0.8, flip)
    p.clip("flip_back", 0.8, lambda t: flip(t, 180.0, 360.0))
    p.show = Matrix.Translation((0, 0, 0.1)) @ Matrix.Rotation(math.radians(-115), 4, (1, 0, 0))
    p.view = dict(az=25, el=15)


# ----------------------------------------------------------------------------------------- remotes
def _remote(p, body, face, keys, accent):
    P = p.P
    W, H, D, zc = 0.056, 0.19, 0.024, 0.03
    p.add(K.plate("remote-body", W, H, D, P[body], (0, 0, zc), r=0.024, bevel=0.007))
    yf = -D / 2
    p.add(K.plate("remote-face", W - 0.012, H - 0.03, 0.004, P[face], (0, yf - 0.001, zc - 0.004), r=0.018,
                  bevel=0.0015, steps=1))
    yk = yf - 0.003
    p.add(geo.ring("remote-dpad", 0.016, 0.0045, P[accent], (0, yk, 0.065), (0, -1, 0), segs=18, sides=6))
    p.add(K.cyl("remote-ok", 0.0075, (0, yk + 0.002, 0.065), (0, yk - 0.004, 0.065), P[keys], segs=12))
    for i, z in enumerate((0.022, 0.0, -0.022)):
        for s in (1, -1):
            p.add(K.capsule(f"remote-key{i}{s}", (s * 0.012 - 0.004, yk, z), (s * 0.012 + 0.004, yk, z), 0.0042,
                            P[keys], segs=8, rings=2))
    p.add(K.cyl("remote-ir", 0.009, (0, 0, zc + H / 2 - 0.004), (0, 0, zc + H / 2 + 0.002), P["lens"], segs=12))
    p.bone("power", (0, yk, 0.103), (0, yk - 0.03, 0.103))
    p.add(K.cyl("remote-power", 0.0085, (0, yk + 0.003, 0.103), (0, yk - 0.004, 0.103), P["red"], segs=12),
          "power")

    def click(t):
        return {"power": dict(move=(0, 0.004 * K.pulse(t, 0.05, 0.06, 0.08, 0.12), 0))}

    p.clip("click", 0.5, click)


@prop("remote", "The fake settings panel (Archie's); Contraband inspection (the missing light-switch remote); "
      "Brick hands Zip the remote",
      "grip: the lower middle, IR end up (+Z), buttons facing -Y; 0.19 m long",
      rig="power (the red button, presses in +Y): click")
def remote(p):
    _remote(p, "ceramic", "graphite", "ceramic", "lime")


@prop("remote-zip", "The fake settings panel (the second remote Zip produces)",
      "grip: the lower middle, IR end up (+Z), buttons facing -Y; 0.19 m long",
      rig="power (the red button, presses in +Y): click")
def remote_zip(p):
    _remote(p, "violet", "graphite", "mint", "mint")


# ------------------------------------------------------------------------------------- fishing rod
@prop("fishing-rod", "Cursor fishing",
      "grip: the handle's middle, rod up (+Z, 1.35 m); the line leaves the tip along -Y (0.9 m) with the "
      "horseshoe magnet at its end, poles pointing -Y (held out level with the palm down, the line hangs)",
      rig="rod_1..2 (the rod bends), line_1..5 (the line), magnet rides line_5: dangle, snap")
def fishing_rod(p):
    P = p.P
    tip = V(0, 0, 1.35)
    p.add(K.cyl("rod-handle", 0.021, (0, 0, -0.13), (0, 0, 0.12), P["cork"], segs=14, bevel=0.006))
    p.add(K.ball("rod-butt", 0.025, P["violet"], (0, 0, -0.135), res=4))
    p.add(K.cyl("rod-seat", 0.016, (0, 0, 0.0), (0, 0, 0.16), P["mint"], segs=14))
    p.add(K.box("rod-reel-foot", (0.008, 0.024, 0.012), P["mint"], (0, -0.03, 0.08), bevel=0.003))
    p.add(K.cyl("rod-reel", 0.042, (-0.016, -0.065, 0.08), (0.016, -0.065, 0.08), P["mint"], segs=20,
                bevel=0.008))
    p.add(K.cyl("rod-spool", 0.03, (-0.019, -0.065, 0.08), (0.019, -0.065, 0.08), P["violet"], segs=18))
    p.add(K.box("rod-crank", (0.004, 0.004, 0.03), P["violet"], (0.024, -0.065, 0.1), bevel=0.0015))
    p.add(K.ball("rod-crank-knob", 0.009, P["mint"], (0.03, -0.065, 0.128), res=3))
    rod_pts = [V(0, 0, 0.12), V(0, 0, 0.75), tip]
    rods = p.chain("rod", rod_pts)
    blank = geo.tube("rod-blank", K.polyline(rod_pts, 12), 0.014, P["violet"],
                     radii=[lerp(0.015, 0.006, k / 12) for k in range(13)], segs=8)
    p.add(K.skin_chain(blank, rods, rod_pts, blend=0.5))
    for k, z in enumerate((0.55, 0.95, 1.25)):
        g = geo.ring(f"rod-guide{k}", 0.009, 0.0022, P["steel"], (0, -0.015, z), (0, 0, 1), segs=8, sides=4)
        p.add(K.skin_chain(g, rods, rod_pts))
    line_pts = [tip + V(0, -0.9 * k / 5, 0) for k in range(6)]
    lines = p.chain("line", line_pts, parent=rods[-1])
    ln = geo.tube("rod-line", K.polyline(line_pts, 20), 0.004, P["white"], segs=5)
    p.add(K.skin_chain(ln, lines, line_pts, blend=0.5))
    # the horseshoe magnet: its bend at the line's end, poles pointing on down the line (-Y)
    e = line_pts[-1]
    R, leg, w = 0.075, 0.08, 0.028
    c = e + V(0, -R, 0)
    path = [c + V(-R, -leg, 0), c + V(-R, -leg * 0.5, 0)]
    path += [c + V(-R * math.cos(a), R * math.sin(a), 0) for a in (math.pi * k / 8 for k in range(9))]
    path += [c + V(R, -leg * 0.5, 0), c + V(R, -leg, 0)]
    p.add(geo.sweep("magnet-body", path, w, w, P["red"], n=3.0, segs=12, up=(0, 0, 1)), lines[-1])
    for s in (1, -1):
        p.add(K.box(f"magnet-pole{s}", (w + 0.0015, 0.014, w + 0.0015), P["steel"], c + V(s * R, -leg - 0.014, 0),
                    bevel=0.005), lines[-1])
    p.add(geo.ring("magnet-eye", 0.01, 0.0028, P["steel"], e + V(0, -0.004, 0), (0, 0, 1), segs=10, sides=4),
          lines[-1])

    def dangle(t):
        out = {}
        for i, b in enumerate(lines):
            out[b] = dict(turn=[((0, 0, 1), (6 if i == 0 else 2) * math.sin(TAU * (t / 2.0) - i * 0.4)),
                                ((1, 0, 0), (3 if i == 0 else 1) * math.sin(TAU * (t / 2.0) * 2 - i * 0.35))])
        return out

    def snap(t):
        # the magnet locks on and yanks: the line swings out ahead of the rod, the rod bows towards it
        k = K.ease("snap", t / 0.35) if t < 0.9 else 1.0 - 0.3 * K.ease("inout", (t - 0.9) / 0.6)
        out = {}
        for i, b in enumerate(rods):
            out[b] = dict(turn=((1, 0, 0), (9 + 8 * i) * k + wobble(t, 0.35, 3.0, 3.0, 4.0)))
        for i, b in enumerate(lines):
            out[b] = dict(turn=((1, 0, 0), (-55 if i == 0 else -1.5) * k + wobble(t, 0.3, 4.0 if i else 8.0, 2.5,
                                                                                   3.0)))
        return out

    p.clip("dangle", 2.0, dangle, loop=True)
    p.clip("snap", 1.5, snap)
    p.show = Matrix.Rotation(math.radians(90), 4, (0, 0, 1)) @ Matrix.Rotation(math.radians(70), 4, (1, 0, 0))
    p.display = ("dangle", 0.0)
    p.view = dict(az=10, el=8)


# ----------------------------------------------------------------------------------- rope and hook
@prop("rope-hook", "The loading-bar tow truck",
      "grip: the rope's free end (a knot); the rope hangs along -Z for 1.5 m to a steel hook",
      rig="rope_1..6 (the rope), hook rides rope_6: swing, tug")
def rope_hook(p):
    P = p.P
    Lr = 1.5
    pts = [V(0, 0, -Lr * k / 6) for k in range(7)]
    names = p.chain("rope", pts)
    rope = geo.tube("rope", K.polyline(pts, 30), 0.016, P["rope"], segs=8)
    p.add(K.skin_chain(rope, names, pts, blend=0.5))
    # a darker spiral lay so it reads as rope, not a rod
    lay = geo.tube("rope-lay", [q + V(0.0145 * math.cos(q.z * 40), 0.0145 * math.sin(q.z * 40), 0)
                                for q in K.polyline(pts, 90)], 0.004, P["cork"], segs=4)
    p.add(K.skin_chain(lay, names, pts, blend=0.5))
    p.add(K.ball("rope-knot", 0.027, P["rope"], (0, 0, 0.005), res=4, scale=(1, 1, 1.2)), "root")
    e = pts[-1]
    p.add(geo.ring("hook-eye", 0.024, 0.007, P["steel"], e + V(0, 0, -0.024), (0, 1, 0), segs=14, sides=6),
          names[-1])
    hk = [e + V(0, 0, -0.048), e + V(0, 0, -0.15)]
    hk += [e + V(0.06 - 0.06 * math.cos(a), 0, -0.15 - 0.06 * math.sin(a)) for a in
           (math.pi * k / 8 for k in range(1, 9))]
    hk += [e + V(0.12, 0, -0.115)]
    p.add(geo.tube("hook", hk, 0.014, P["steel"], radii=[0.015] * (len(hk) - 1) + [0.008], segs=8), names[-1])

    def swing(t):
        return {b: dict(turn=((0, 1, 0), (5 if i == 0 else 1.5) * math.sin(TAU * t / 2.4 - i * 0.35)))
                for i, b in enumerate(names)}

    def tug(t):
        # a ripple runs down the rope as it is yanked
        return {b: dict(turn=((0, 1, 0), 12 * math.sin(TAU * (t * 2.2 - i / 4)) * K.pulse(t - i * 0.06, 0, 0.1,
                                                                                         0.25, 0.5)))
                for i, b in enumerate(names)}

    p.clip("swing", 2.4, swing, loop=True)
    p.clip("tug", 1.2, tug)
    p.display = ("swing", 0.4)


# ------------------------------------------------------------------------------------------ cables
def _plug(p, base, axis, bone, body="lime"):
    """A chunky plug at `base` pointing along `axis` (+Z or similar): body, band and two brass prongs."""
    P = p.P
    a = V(*axis).normalized()
    side = a.orthogonal().normalized()
    p.add(K.cyl("plug-body", 0.022, base - a * 0.035, base + a * 0.012, P[body], segs=14, bevel=0.007), bone)
    p.add(geo.ring("plug-band", 0.022, 0.004, P["graphite"], base - a * 0.012, a, segs=14, sides=5), bone)
    for s in (1, -1):
        p.add(K.cyl(f"plug-prong{s}", 0.0035, base + a * 0.01 + side * s * 0.009, base + a * 0.04 + side * s * 0.009,
                    P["brass"], segs=8), bone)


@prop("cable", "Pocket universe, wrong pocket; The emergency backup (Brick plugs it into the potato)",
      "grip: the plug's body, prongs up (+Z); the cable hangs along -Z for 0.9 m",
      rig="cable_1..4: dangle")
def cable(p):
    P = p.P
    pts = [V(0, 0, -0.035 - 0.9 * k / 4) for k in range(5)]
    names = p.chain("cable", pts)
    _plug(p, V(0, 0, 0), (0, 0, 1), "root")
    p.add(geo.lathe("cable-relief", [(0.014, -0.034), (0.0085, -0.07), (0.0, -0.07)], P["graphite"], segs=12,
                    caps=False))
    c = geo.tube("cable", K.polyline(pts, 20), 0.009, P["graphite"], segs=8)
    p.add(K.skin_chain(c, names, pts, blend=0.5))

    def dangle(t):
        return {b: dict(turn=[((0, 1, 0), (7 if i == 0 else 3) * math.sin(TAU * t / 1.8 - i * 0.6)),
                              ((1, 0, 0), (4 if i == 0 else 2) * math.sin(TAU * t / 1.8 * 2 - i * 0.5))])
                for i, b in enumerate(names)}

    p.clip("dangle", 1.8, dangle, loop=True)
    p.display = ("dangle", 0.3)


@prop("tether", "The invisible tug-of-war (the end of Archie's own tether)",
      "the end that plugs into Archie (a collar facing -X) at the origin; the cable runs 3 m along +X to the "
      "plug at its far end",
      rig="tether_1..8, plug rides tether_8: slack, tug")
def tether(p):
    P = p.P
    Lt, nb = 3.0, 8
    pts = [V(Lt * k / nb, 0, 0) for k in range(nb + 1)]
    names = p.chain("tether", pts)
    p.add(K.cyl("tether-collar", 0.045, (-0.02, 0, 0), (0.035, 0, 0), P["graphite"], segs=16, bevel=0.01))
    p.add(geo.ring("tether-collar-ring", 0.043, 0.007, P["lime"], (0.0, 0, 0), (1, 0, 0), segs=16, sides=6))
    c = geo.tube("tether", K.polyline(pts, 40), 0.017, P["graphite"], segs=8)
    p.add(K.skin_chain(c, names, pts, blend=0.5))
    stripe = geo.tube("tether-stripe", [q + V(0, 0.015 * math.cos(q.x * 8), 0.015 * math.sin(q.x * 8))
                                        for q in K.polyline(pts, 80)], 0.005, P["lime"], segs=4)
    p.add(K.skin_chain(stripe, names, pts, blend=0.5))
    _plug(p, pts[-1] + V(0.035, 0, 0), (1, 0, 0), names[-1])

    def sag(t, amp):
        out = {}
        for i, b in enumerate(names):
            a = amp * (1 - 2 * i / (nb - 1))
            out[b] = dict(turn=((0, 1, 0), a * (1 + 0.15 * math.sin(TAU * t / 3.0 + i * 0.4))))
        return out

    def tug(t):
        k = K.ease("snap", t / 0.3)
        out = sag(0, 8.0 * (1 - k))
        for i, b in enumerate(names):
            out[b]["turn"] = [out[b]["turn"], ((0, 0, 1), 7 * math.sin(TAU * (t * 2.5 - i / 4)) *
                                               K.pulse(t, 0.1, 0.1, 0.3, 0.6))]
        return out

    p.clip("slack", 3.0, lambda t: sag(t, 8.0), loop=True)
    p.clip("tug", 1.4, tug)
    p.display = ("slack", 0.0)
    p.view = dict(az=20, el=25)


# -------------------------------------------------------------------------------------- spotlights
def _spot_head(p, scale, bone, at, beam_len):
    """A stage can-light pointing -Y from `at`: graphite can, mint bezel, glowing lens, and its beam."""
    P = p.P
    s = scale
    c = V(*at)
    p.add(K.cyl("spot-can", 0.09 * s, c + V(0, 0.11 * s, 0), c + V(0, -0.09 * s, 0), P["graphite"], segs=18,
                bevel=0.02 * s), bone)
    p.add(geo.ring("spot-bezel", 0.092 * s, 0.014 * s, P["mint"], c + V(0, -0.09 * s, 0), (0, -1, 0), segs=18,
                   sides=5), bone)
    p.add(K.cyl("spot-lens", 0.078 * s, c + V(0, -0.088 * s, 0), c + V(0, -0.098 * s, 0), P["holo_lamp"], segs=18,
                bevel=0.003 * s, steps=1), bone)
    for k in range(2):
        p.add(geo.ring(f"spot-fin{k}", 0.091 * s, 0.007 * s, P["graphite"], c + V(0, (0.025 + 0.04 * k) * s, 0),
                       (0, 1, 0), segs=18, sides=4), bone)
    for sx in (1, -1):                                          # barn doors
        p.add(K.box(f"spot-door{sx}", (0.004 * s, 0.04 * s, 0.08 * s), P["graphite"],
                    c + V(sx * 0.1 * s, -0.12 * s, 0), bevel=0.002 * s,
                    rot=Matrix.Rotation(math.radians(sx * 25), 3, (0, 0, 1))), bone)
    beam = geo.lathe("spot-beam", [(0.075 * s, 0.0), (0.45 * s * beam_len / 1.8, beam_len)], P["holo_beam"], segs=24,
                     caps=False)
    geo.transform(beam, Matrix.Translation(c + V(0, -0.1 * s, 0)) @ geo.basis((0, -1, 0)).to_4x4())
    p.add(beam, bone, node="beam")


@prop("spotlight", "The stolen spotlight; Contraband inspection (the stolen spotlight falls out)",
      "grip: the pistol handle below the can; beam along -Y (away from the palm), 1.8 m long (node `beam`, "
      "material holo-beam)")
def spotlight(p):
    P = p.P
    _spot_head(p, 1.0, "root", (0, 0, 0.13), 1.8)
    p.add(K.cyl("spot-grip", 0.022, (0, 0.01, -0.06), (0, 0.0, 0.07), P["rubber"], segs=14, bevel=0.008))
    p.add(K.box("spot-trigger", (0.006, 0.012, 0.018), P["red"], (0, -0.026, 0.04), bevel=0.003))
    p.view = dict(az=-50, el=20)


@prop("spotlight-stand", "The stolen spotlight (the stage light Zip turns on himself; Brick's third light); "
      "The dramatic entrance",
      "floor, under the tripod; head 1.6 m up, beam along -Y 3 m (node `beam`, holo-beam)",
      rig="pan (turns about Z) > tilt (about X): sweep, swing_to_zip")
def spotlight_stand(p):
    P = p.P
    p.skin = False                     # rigid parts on their bones: a page can clone it (a third spotlight)
    H = 1.6
    for k in range(3):
        a = TAU * k / 3 + math.pi / 2
        foot = V(0.42 * math.cos(a), 0.42 * math.sin(a), 0.0)
        p.add(geo.tube(f"stand-leg{k}", [V(0, 0, 0.55), foot + V(0, 0, 0.02)], 0.014, P["graphite"], segs=8))
        p.add(K.ball(f"stand-foot{k}", 0.028, P["rubber"], foot + V(0, 0, 0.02), res=3, scale=(1, 1, 0.6)))
    p.add(K.cyl("stand-pole", 0.022, (0, 0, 0.4), (0, 0, H - 0.18), P["graphite"], segs=12))
    p.add(K.cyl("stand-clamp", 0.03, (0, 0, 0.52), (0, 0, 0.6), P["mint"], segs=12))
    p.bone("pan", (0, 0, H - 0.18), (0, 0, H - 0.05), z=(0, -1, 0))
    p.bone("tilt", (0, 0, H), (0.2, 0, H), parent="pan", z=(0, 0, 1))
    p.add(K.cyl("stand-swivel", 0.035, (0, 0, H - 0.2), (0, 0, H - 0.15), P["mint"], segs=14), "pan")
    yoke = [V(-0.15, 0, H), V(-0.15, 0, H - 0.16), V(0.15, 0, H - 0.16), V(0.15, 0, H)]
    p.add(geo.tube("stand-yoke", yoke, 0.014, P["mint"], segs=8), "pan")
    _spot_head(p, 1.3, "tilt", (0, 0, H), 3.0)

    def sweep(t):
        return {"pan": dict(turn=((0, 0, 1), 35 * math.sin(TAU * t / 4.0))),
                "tilt": dict(turn=((1, 0, 0), 12 + 6 * math.sin(TAU * t / 2.0)))}

    def swing_to_zip(t):
        k = K.ease("back", t / 0.5)
        return {"pan": dict(turn=((0, 0, 1), 55 * k)), "tilt": dict(turn=((1, 0, 0), 14 * k))}

    p.clip("sweep", 4.0, sweep, loop=True)
    p.clip("swing_to_zip", 0.8, swing_to_zip)
    p.display = ("sweep", 0.0)
    p.view = dict(az=-40, el=15)


# --------------------------------------------------------------------------------------- rubber duck
@prop("rubber-duck", "Pocket universe, wrong pocket", "floor, under its middle, facing -Y; 0.15 m long")
def rubber_duck(p):
    P = p.P

    def body_shape(q, u):
        z = q.z
        if u.z < 0:
            z *= 0.6
        if u.y > 0.3:                                          # the tail, swept up
            z += 0.035 * (u.y - 0.3) / 0.7 * max(0.0, u.z + 0.3)
        return V(q.x, q.y, z)

    p.add(geo.superquad("duck-body", (0.058, 0.075, 0.045), P["yellow"], (0, 0.005, 0.042), n=2.2,
                        shape=body_shape, res=5))
    p.add(K.ball("duck-head", 0.039, P["yellow"], (0, -0.04, 0.108), res=5))
    p.add(geo.superquad("duck-beak", (0.026, 0.024, 0.01), P["orange"], (0, -0.078, 0.1), n=2.2, res=4))
    for s in (1, -1):
        p.add(K.ball(f"duck-eye{s}", 0.0075, P["graphite"], (s * 0.019, -0.07, 0.122), res=3))
        p.add(K.ball(f"duck-glint{s}", 0.0024, P["white"], (s * 0.019 - 0.002, -0.0765, 0.1255), res=2))
        p.add(geo.superquad(f"duck-wing{s}", (0.012, 0.04, 0.022), P["yellow"], (s * 0.054, 0.012, 0.055), n=2.2,
                            res=3, rot=Matrix.Rotation(math.radians(s * -12), 3, (0, 1, 0))))


# ------------------------------------------------------------------------------------------- potato
@prop("potato", "The emergency backup (Zip's stand-in Atlas Core)",
      "grip: its middle, length along X, continents facing -Y; 0.16 m long. Continents are holo-land (the "
      "page lights them when the cable goes in); the socket is on its +X end")
def potato(p):
    P = p.P
    rng = random.Random(5)
    bumps = [(V(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)).normalized(), rng.uniform(0.05, 0.13))
             for _ in range(14)]

    def lumpy(q, u):
        k = 1.0
        n = u.normalized()
        for d, a in bumps:
            k += a * max(0.0, n.dot(d)) ** 4
        return q * k

    spud = geo.superquad("potato-body", (0.078, 0.052, 0.046), P["potato"], (0, 0, 0), n=2.0, shape=lumpy, res=7)
    p.add(spud)
    surf = geo.Surface(spud)
    for k in range(9):                                          # eyes (little dark dimples)
        d = V(rng.uniform(-1, 1), rng.uniform(-0.2, 1), rng.uniform(-1, 1)).normalized()
        hit = surf.toward(d * 0.2, (0, 0, 0), offset=-0.001)
        if hit:
            p.add(K.ball(f"potato-eye{k}", 0.0035, P["ink"], hit, res=2))
    land = [((-0.034, 0.01), 0.026, 1), ((0.024, -0.006), 0.03, 2), ((0.056, 0.022), 0.012, 3),
            ((-0.008, -0.03), 0.013, 4)]
    nv = 22
    for i, ((cx, cz), rad, seed) in enumerate(land):
        r2 = random.Random(seed)
        ph = [r2.uniform(0, TAU) for _ in range(4)]
        ring_ = []
        for j in range(nv):
            a = TAU * j / nv
            k = (1 + 0.3 * math.sin(2 * a + ph[0]) + 0.18 * math.sin(3 * a + ph[1]) + 0.12 * math.sin(5 * a + ph[2])
                 + 0.07 * math.sin(7 * a + ph[3]))
            ring_.append((cx + rad * k * math.cos(a), cz + rad * k * 0.8 * math.sin(a)))
        grid = [[surf.front(cx + (x - cx) * f, cz + (z - cz) * f, offset=0.0012) for x, z in ring_]
                for f in (0.35, 0.7, 1.0)]
        mid = surf.front(cx, cz, offset=0.0012)
        if mid is None or any(q is None for row in grid for q in row):
            continue
        p.add(K.patch_rings(f"potato-land{i}", mid, grid, P["holo_land"], (0, -1, 0)))
        edge = [surf.front(x, z, offset=0.0016) for x, z in ring_]
        p.add(geo.tube(f"potato-coast{i}", edge, 0.0011, P["ink"], segs=3, caps=False, closed=True))
    # the socket the cable plugs into, on the +X end
    hit = surf.side(0.0, 0.0, s=1, offset=-0.004)
    p.add(K.cyl("potato-socket", 0.018, hit + V(-0.006, 0, 0), hit + V(0.008, 0, 0), P["graphite"], segs=14))
    p.add(geo.ring("potato-socket-ring", 0.016, 0.003, P["brass"], hit + V(0.008, 0, 0), (1, 0, 0), segs=14,
                   sides=5))
    for s in (1, -1):
        p.add(K.box(f"potato-slot{s}", (0.0015, 0.0025, 0.005), P["rubber"], hit + V(0.0085, s * 0.006, 0)))


# --------------------------------------------------------------------------------------------- star
@prop("star", "The souvenir theft (spills from behind Zip's back); Contraband inspection (three fall out)",
      "its middle, face towards -Y; 0.22 m across (decorative: the page's real ratings are untouched)")
def star(p):
    p.add(K.pillow("star", K.star_radius(0.11, 0.05), 0.06, p.P["gold"], n=60, rings=5, power=3.0))


# -------------------------------------------------------------------------------------------- drink
@prop("drink", "Zip moved in (the drink with an umbrella)",
      "floor, under the glass; 0.2 m tall with the umbrella (Zip-sized: scale it with him)")
def drink(p):
    P = p.P
    glass = [(0.0, 0.0), (0.03, 0.0), (0.032, 0.006), (0.024, 0.02), (0.022, 0.05), (0.034, 0.085), (0.041, 0.12),
             (0.037, 0.12), (0.03, 0.085), (0.018, 0.05), (0.02, 0.021), (0.0, 0.016)]
    p.add(geo.lathe("drink-glass", glass, P["glass"], segs=20, caps=False))
    p.add(geo.lathe("drink-juice", [(0.0, 0.017), (0.019, 0.022), (0.017, 0.05), (0.028, 0.085), (0.034, 0.108),
                                    (0.0, 0.108)], P["juice"], segs=18, caps=False))
    p.add(geo.tube("drink-straw", [V(-0.01, 0, 0.03), V(-0.012, 0.004, 0.13), V(-0.024, 0.01, 0.155)], 0.0035,
                   P["lime"], segs=6))
    p.add(geo.disc("drink-slice", 0.022, 0.006, P["yellow"], (0.036, -0.012, 0.118), (0.8, -0.6, 0.0), segs=14))
    # the umbrella: a stick and an eight-panel canopy in alternating colours
    top = V(0.012, -0.004, 0.19)
    p.add(geo.tube("drink-stick", [V(0.006, 0.0, 0.06), top + V(0, 0, 0.004)], 0.0018, P["wood"], segs=5))
    up = V(-0.25, 0.1, 1).normalized()
    can = geo.lathe("drink-canopy", [(0.0, 0.004), (0.058, -0.02), (0.056, -0.024), (0.0, 0.0)], P["mint"],
                    top, up, segs=8, caps=False)
    can.data.materials.append(P["pink"])
    side = up.orthogonal().normalized()
    for f in can.data.polygons:
        c = f.center - top
        a = math.atan2(c.dot(up.cross(side)), c.dot(side))
        f.material_index = int(((a + TAU) % TAU) / (TAU / 8)) % 2
        f.use_smooth = False
    p.add(can)


# -------------------------------------------------------------------------------------- balloon dog
@prop("balloon-dog", "The fake cursor (Archie bends the decoy pointer into one)",
      "floor, between its feet, nose towards -Y; 0.45 m tall, cursor-white")
def balloon_dog(p):
    P = p.P
    m = P["white"]
    r = 0.032
    segs = [((0, 0.11, 0.2), (0, -0.07, 0.21)),                          # body
            ((0, -0.08, 0.22), (0, -0.1, 0.33)),                         # neck
            ((0, -0.12, 0.36), (0, -0.21, 0.35)),                        # snout
            ((0, 0.12, 0.22), (0, 0.17, 0.33))]                          # tail
    for i, (a, b) in enumerate(segs):
        p.add(K.capsule(f"dog-seg{i}", a, b, r if i != 3 else r * 0.8, m, segs=10, rings=3,
                        r2=None if i != 3 else r * 0.45))
    for s in (1, -1):
        p.add(K.capsule(f"dog-ear{s}", (s * 0.02, -0.1, 0.36), (s * 0.06, -0.07, 0.41), r * 0.85, m, segs=10))
        p.add(K.capsule(f"dog-front-leg{s}", (s * 0.03, -0.07, 0.19), (s * 0.06, -0.08, 0.04), r * 0.9, m, segs=10))
        p.add(K.capsule(f"dog-back-leg{s}", (s * 0.03, 0.11, 0.19), (s * 0.06, 0.12, 0.04), r * 0.9, m, segs=10))
    p.add(K.ball("dog-nose", 0.012, P["graphite"], (0, -0.245, 0.352), res=3))
    for s in (1, -1):
        p.add(K.ball(f"dog-eye{s}", 0.007, P["graphite"], (s * 0.026, -0.15, 0.375), res=2))
    p.add(K.ball("dog-knot", 0.009, m, (0, 0.17, 0.345), res=2))


# ------------------------------------------------------------------------------------- fake cursor
CURSOR = [(0.0, 0.0), (0.0, -16.0), (3.9, -12.4), (6.6, -18.6), (9.4, -17.4), (6.8, -11.3), (11.6, -11.3)]


@prop("fake-cursor", "The fake cursor (Zip's theatrical decoy pointer; the real cursor is untouched)",
      "its hotspot (the arrow's tip) at the origin, the arrow pointing up-left as on screen, face towards -Y; "
      "0.55 m tall",
      rig="cursor_1..4 (from the tip down the stem; it bends): poke, bend, wobble")
def fake_cursor(p):
    P = p.P
    k = 0.55 / 18.6
    pts = K.ccw([(x * k, y * k) for x, y in CURSOR])
    outline = K.offset_poly(pts, 0.014)
    body = K.poly_mesh("cursor-outline", outline, 0.05, P["black"], bevel=0.008, steps=2, sharp=50)
    face = K.poly_mesh("cursor-face", pts, 0.058, P["white"], bevel=0.008, steps=2, sharp=50)
    # the chain: from the tip, down the arrow's middle and out along the stem
    axis = [V(0.0, 0, 0.0), V(0.05, 0, -0.14), V(0.1, 0, -0.27), V(0.15, 0, -0.39), V(0.235, 0, -0.53)]
    names = p.chain("cursor", axis, z=(0, -1, 0))
    for ob in (body, face):
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        d = (axis[-1] - axis[0]).normalized()
        for j in range(1, 12):
            c = axis[0] + d * (0.6 * j / 12)
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=c, plane_no=d)
        bm.to_mesh(ob.data)
        bm.free()
        p.add(K.skin_chain(ob, names, axis, blend=0.5))

    def poke(t):
        k_ = K.ease("snap", t / 0.18) if t < 0.3 else 1 - K.ease("inout", (t - 0.3) / 0.4)
        return {names[0]: dict(move=(-0.1 * k_, 0, 0.27 * k_ * 0.5)),
                **{b: dict(turn=((0, 1, 0), wobble(t, 0.18, 6.0, 4.0, 5.0))) for b in names[1:]}}

    def bend(t):
        k_ = K.ease("inout", t / 1.2)
        return {b: dict(turn=((0, 1, 0), -24 * k_)) for b in names[1:]}

    def wob(t):
        return {b: dict(turn=((0, 1, 0), 5 * math.sin(TAU * t / 1.2 - i * 0.7))) for i, b in enumerate(names)}

    p.clip("poke", 0.8, poke)
    p.clip("bend", 1.4, bend)
    p.clip("wobble", 1.2, wob, loop=True)
    p.view = dict(az=25, el=10)


# ------------------------------------------------------------------------------------------- hammer
@prop("hammer", "The unauthorized renovation (building the balcony)",
      "grip: the handle, a third of the way up; head up (+Z), its face towards +X; 0.34 m long")
def hammer(p):
    P = p.P
    p.add(K.cyl("hammer-handle", 0.017, (0, 0, -0.12), (0, 0, 0.2), P["wood"], segs=12, bevel=0.006))
    p.add(K.cyl("hammer-grip", 0.02, (0, 0, -0.12), (0, 0, 0.02), P["lime"], segs=12, bevel=0.006))
    p.add(K.box("hammer-head", (0.07, 0.025, 0.03), P["steel"], (0.0, 0, 0.215), bevel=0.008))
    p.add(K.cyl("hammer-face", 0.03, (0.06, 0, 0.215), (0.1, 0, 0.215), P["steel"], segs=12, bevel=0.006))
    p.add(K.box("hammer-claw", (0.03, 0.02, 0.012), P["steel"], (-0.085, 0, 0.205), bevel=0.005,
                rot=Matrix.Rotation(math.radians(-25), 3, (0, 1, 0))))
