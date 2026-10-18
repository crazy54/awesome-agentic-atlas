"""Flat things with words or pictures on them: signs, notes, the README, the app card, the replay screen,
labels and stamps. Text is Geist (the site's face) turned to flat meshes; texturable faces are `card-face`
and `screen-face`, which carry small placeholder textures (and so keep their UVs through slim.mjs's prune)
for the page to swap. See props.py for the conventions."""
from __future__ import annotations

import math

import bpy
import numpy as np
from mathutils import Matrix

import props_kit as K
from props_kit import V, lerp, prop, wobble
from kit import geo, mat

TAU = math.tau


# -------------------------------------------------------------------------------- placeholder images
def _canvas(w, h, hex_):
    return np.ones((h, w, 3), np.float32) * mat._hex01(hex_)


def _rect(img, x0, y0, x1, y1, hex_, r=0.0):
    """Fill a (rounded) rectangle given in 0..1 of the image (y down)."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    u, v = (xx + 0.5) / w, (yy + 0.5) / h
    if r <= 0:
        m = (u >= x0) & (u <= x1) & (v >= y0) & (v <= y1)
    else:
        cx = np.clip(u, x0 + r, x1 - r)
        cy = np.clip(v, y0 + r * w / h, y1 - r * w / h)
        m = ((u - cx) ** 2 + ((v - cy) * h / w) ** 2 <= r * r) & (u >= x0) & (u <= x1) & (v >= y0) & (v <= y1)
    img[m] = mat._hex01(hex_)
    return img


def _face_material(name, img):
    m = mat.principled(name, "#ffffff", rough=0.3, coat=0.5, coat_rough=0.08)
    return mat.textured(m, mat.image(name + "-placeholder", img))


def card_face():
    """A placeholder app card: hero band, title, three lines of text, a row of stars, a lime button."""
    img = _canvas(192, 128, "#f4f1ea")
    _rect(img, 0.0, 0.0, 1.0, 0.42, "#2b2a29")
    _rect(img, 0.06, 0.08, 0.3, 0.34, "#a4c812", r=0.04)
    _rect(img, 0.36, 0.12, 0.86, 0.2, "#efe4d2", r=0.02)
    _rect(img, 0.36, 0.25, 0.7, 0.31, "#8a8580", r=0.02)
    for k, x1 in enumerate((0.9, 0.82, 0.62)):
        _rect(img, 0.06, 0.5 + 0.09 * k, x1, 0.55 + 0.09 * k, "#b8b2a8", r=0.02)
    for k in range(5):
        _rect(img, 0.06 + 0.07 * k, 0.8, 0.11 + 0.07 * k, 0.88, "#f2b630", r=0.025)
    _rect(img, 0.68, 0.78, 0.94, 0.9, "#a4c812", r=0.04)
    return _face_material("card-face", img)


def screen_face():
    """A placeholder replay frame: a dim scene, a big play triangle, a red REC dot."""
    img = _canvas(160, 96, "#1d2430")
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    img *= (0.75 + 0.25 * ((yy // 3) % 2))[..., None]               # scanlines
    _rect(img, 0.0, 0.78, 1.0, 1.0, "#2f3a2a")                       # a floor
    u, v = (xx + 0.5) / w, (yy + 0.5) / h
    tri = (u > 0.43) & (u < 0.6) & (np.abs(v - 0.45) < (0.6 - u) * 1.05 * w / h * 0.6)
    img[tri] = mat._hex01("#f4f1ea")
    dot = (u - 0.08) ** 2 + ((v - 0.12) * h / w) ** 2 < 0.03 ** 2
    img[dot] = mat._hex01("#ff3b30")
    return _face_material("screen-face", img)


# --------------------------------------------------------------------------------------- hanging signs
def _hanging_sign(p, body, w, h, accent):
    """A board on a cord from one hook: the board swings on `sign` about the hook (the origin)."""
    P = p.P
    drop = h * 0.55                                            # hook to the board's top edge
    top = -drop
    p.bone("sign", (0, 0, 0), (0, 0, -drop - h), z=(0, -1, 0))
    d = max(0.014, w * 0.03)
    p.add(K.plate("sign-board", w, h, d, P["ceramic"], (0, 0, top - h / 2), r=h * 0.12, bevel=d * 0.35), "sign")
    rim = [V(u, -d / 2 - 0.001, top - h / 2 + v) for u, v in K.rrect(w * 0.9, h * 0.82, h * 0.09, 3)]
    p.add(geo.tube("sign-rim", rim, max(0.004, w * 0.008), P[accent], segs=5, caps=False, closed=True), "sign")
    p.add(K.text("sign-text", body, h * 0.3, P["graphite"], K.on_front((0, -d / 2 - 0.0015, top - h / 2)),
                 fit=(w * 0.8, h * 0.66), line=0.9), "sign")
    for s in (1, -1):                                          # the cord, from each top corner to the hook
        a = V(s * w * 0.38, 0, top - 0.004)
        p.add(geo.tube(f"sign-cord{s}", [a, a.lerp(V(0, 0, -0.01), 0.5), V(0, 0, -0.01)], max(0.003, w * 0.006),
                       P["graphite"], segs=6), "sign")
        p.add(geo.sphere(f"sign-eyelet{s}", max(0.006, w * 0.014), P["lime"], a + V(0, -d / 2, 0), res=3), "sign")
    hr = max(0.008, w * 0.022)
    p.add(geo.ring("sign-hook", hr, hr * 0.3, P["graphite"], (0, 0, hr * 0.2), (0, 1, 0), segs=14, sides=6))

    def swing(t):
        return {"sign": dict(turn=((0, 1, 0), 9 * math.exp(-0.9 * t) * math.sin(TAU * 0.8 * t)))}

    p.clip("swing", 3.0, swing)
    p.display = ("swing", 0.22)


@prop("sign-back-in-5", "The README hostage situation",
      "hang point (the hook) at the origin, board below, text facing -Y; 0.72 m wide",
      rig="sign (swings about the hook): swing")
def sign_back_in_5(p):
    _hanging_sign(p, "BACK IN\n5 MINUTES", 0.72, 0.4, "lime")


@prop("sign-back-in-4", "The README hostage situation (the smaller one Archie holds underneath)",
      "hang point (the hook) at the origin, board below, text facing -Y; 0.44 m wide",
      rig="sign (swings about the hook): swing")
def sign_back_in_4(p):
    _hanging_sign(p, "BACK IN\n4 MINUTES", 0.44, 0.25, "lime")


# -------------------------------------------------------------------------------------- picket sign
@prop("picket-sign", "The union break",
      "floor, at the foot of its stick, text facing -Y; 1.55 m tall, board 0.95 m wide (grip the stick about "
      "0.7 m up)")
def picket_sign(p):
    P = p.P
    W, H, d, zc = 0.95, 0.64, 0.022, 1.2
    p.add(K.box("picket-stick", (0.02, 0.016, 0.72), P["wood"], (0, d / 2 + 0.016, 0.72), bevel=0.006))
    p.add(K.plate("picket-board", W, H, d, P["cream"], (0, 0, zc), r=0.03, bevel=0.006))
    yf = -d / 2 - 0.0015
    p.add(K.text("picket-text", "YOUR POOR\nPLANNING\nIS NOT OUR", 0.2, P["graphite"],
                 K.on_front((0, yf, zc + 0.07)), fit=(W * 0.86, H * 0.6), line=0.92))
    p.add(K.text("picket-text-red", "EMERGENCY", 0.2, P["redink"], K.on_front((0, yf, zc - 0.225)),
                 fit=(W * 0.88, 0.12)))
    for s in (1, -1):
        p.add(K.ball(f"picket-staple{s}", 0.012, P["steel"], (0, d / 2 + 0.034, zc + s * 0.2), res=2,
                     scale=(1.4, 0.5, 0.5)))


# ---------------------------------------------------------------------------------------- cue cards
def _cue_card(p, front, back):
    P = p.P
    W, H, d = 0.52, 0.36, 0.012
    zc = H / 2
    p.bone("card", (0, 0, 0), (0, 0, H))
    p.add(K.plate("cue-board", W, H, d, P["white"], (0, 0, zc), r=0.025, bevel=0.004), "card")
    rim = [V(u, -d / 2 - 0.001, zc + v) for u, v in K.rrect(W * 0.9, H * 0.84, 0.02, 3)]
    p.add(geo.tube("cue-rim", rim, 0.004, P["mint"], segs=5, caps=False, closed=True), "card")
    p.add(K.text("cue-text", front, 0.1, P["graphite"], K.on_front((0, -d / 2 - 0.0015, zc)),
                 fit=(W * 0.8, H * 0.7), line=0.9), "card")
    p.add(K.text("cue-back", back, 0.035, P["mint"], K.on_back((W * 0.32, d / 2 + 0.0015, zc + H * 0.34)),
                 fit=(0.12, 0.04)), "card")

    def turn(t):
        return {"card": dict(turn=((0, 0, 1), 180 * K.ease("back", t / 0.6)))}

    p.clip("turn", 0.8, turn)


@prop("cue-card", "The apology video (Brick turns it round: LOOK SADDER)",
      "grip: the middle of its bottom edge, LOOK SADDER on the -Y face (the face Archie reads); 0.52 m wide",
      rig="card (turns about Z): turn (180 deg, shows the other face)")
def cue_card(p):
    _cue_card(p, "LOOK\nSADDER", "CUE 3")


@prop("cue-card-sorry", "The apology video (Zip's other cue cards)",
      "grip: the middle of its bottom edge, text on the -Y face; 0.52 m wide",
      rig="card (turns about Z): turn")
def cue_card_sorry(p):
    _cue_card(p, "I AM SO\nSORRY", "CUE 1")


# ------------------------------------------------------------------------------------ no-archies sign
@prop("no-archies-sign", "The hostile takeover (the miniature agents' sign inside the core)",
      "floor, at the foot of its post, facing -Y; 0.42 m tall (scale it to the agents)")
def no_archies_sign(p):
    P = p.P
    W, H, d, zc = 0.32, 0.3, 0.016, 0.27
    p.add(K.box("noarch-post", (0.014, 0.012, 0.15), P["wood"], (0, d / 2 + 0.012, 0.15), bevel=0.004))
    p.add(K.plate("noarch-board", W, H, d, P["white"], (0, 0, zc), r=0.03, bevel=0.005))
    yf = -d / 2
    c = V(0, yf - 0.002, zc + 0.04)
    # a little Archie: an egg of a head with his crest, crossed out
    p.add(geo.superquad("noarch-head", (0.04, 0.008, 0.045), P["ceramic"], c + V(0, 0.0, -0.005), n=2.2, res=3))
    p.add(geo.superquad("noarch-outline", (0.047, 0.006, 0.052), P["graphite"], c + V(0, 0.004, -0.005), n=2.2,
                        res=3))
    for s in (1, -1):
        p.add(K.cyl(f"noarch-ear{s}", 0.017, c + V(s * 0.048, 0.002, -0.005), c + V(s * 0.048, -0.008, -0.005),
                    P["graphite"], segs=12))
    p.add(K.poly_mesh("noarch-crest", [(-0.012, 0.03), (0.0, 0.07), (0.035, 0.085), (0.014, 0.03)], 0.012,
                      P["graphite"], center=c + V(0, 0.001, 0), bevel=0.002))
    for s in (1, -1):
        p.add(K.ball(f"noarch-eye{s}", 0.007, P["lime"], c + V(s * 0.016, -0.007, 0.0), res=2, scale=(1, 0.5, 1)))
    p.add(geo.ring("noarch-ring", 0.07, 0.009, P["red"], c + V(0, -0.006, 0), (0, -1, 0), segs=24, sides=4,
                   squash=0.6))
    p.add(K.box("noarch-slash", (0.068, 0.004, 0.0085), P["red"], c + V(0, -0.008, 0), bevel=0.003,
                rot=Matrix.Rotation(math.radians(-45), 3, (0, 1, 0))))
    p.add(K.text("noarch-text", "NO ARCHIES", 0.05, P["graphite"], K.on_front((0, yf - 0.0015, zc - 0.105)),
                 fit=(W * 0.86, 0.05)))


# ------------------------------------------------------------------------------------- paper sheets
def _paper(p, title, title_ink, lines, footer, W=0.32, H=0.44, extra=None):
    """A sheet that bends: `sheet_1..4` run up it from its bottom edge (the origin, where it is held)."""
    P = p.P
    t = 0.004
    n = 4
    pts = [V(0, 0, H * k / n) for k in range(n + 1)]
    names = p.chain("sheet", pts)
    parts = [K.sheet("paper", W, H, t, P["paper"], nz=12, center=(0, 0, H / 2))]
    yf = -t / 2 - 0.0008
    parts.append(K.text("paper-title", title, 0.05, P[title_ink], K.on_front((0, yf, H * 0.86)),
                        fit=(W * 0.84, H * 0.13), line=0.9))
    z = H * 0.72
    for k, frac in enumerate(lines):
        parts.append(K.box(f"paper-line{k}", (W * 0.4 * frac, 0.0006, 0.0045), P["ink"],
                           (-W * 0.4 * (1 - frac), yf + 0.0002, z)))
        z -= 0.032
    if footer:
        parts.append(K.text("paper-footer", footer, 0.024, P["ink"], K.on_front((W * 0.18, yf, H * 0.1)),
                            fit=(W * 0.5, 0.03)))
    if extra:
        parts += extra(yf)
    for ob in parts:
        p.add(K.skin_chain(ob, names, pts, blend=0.5))

    def flutter(t_):
        return {b: dict(turn=((1, 0, 0), (2.5 + 2 * i) * math.sin(TAU * (t_ / 1.6) - i * 0.8)))
                for i, b in enumerate(names)}

    def curl(t_):
        k = K.ease("inout", t_ / 1.0)
        return {b: dict(turn=((1, 0, 0), -(4 + 9 * i) * k)) for i, b in enumerate(names)}

    p.clip("flutter", 1.6, flutter, loop=True)
    p.clip("curl", 1.2, curl)
    p.display = ("flutter", 0.4)
    p.view = dict(az=30, el=12)
    return names


def _scribble(name, a, w, ink, yf, amp=0.012):
    pts = [V(a[0] + w * k / 24, yf - 0.0004, a[1] + amp * math.sin(k * 1.3) * (1 - abs(k - 12) / 14))
           for k in range(25)]
    return geo.tube(name, pts, 0.0016, ink, segs=4)


@prop("eviction-notice", "The unauthorized renovation (Brick presents it)",
      "grip: the middle of its bottom edge, text on the -Y face; 0.32 x 0.44 m",
      rig="sheet_1..4 (bends up the page): flutter, curl")
def eviction_notice(p):
    P = p.P

    def extra(yf):
        stamp = [geo.tube("evict-stamp-rim", [V(0.07 + u, yf - 0.0008, 0.095 + v) for u, v in
                                              K.rrect(0.11, 0.05, 0.008, 2)], 0.0025, P["redink"], segs=4,
                          caps=False, closed=True),
                 K.text("evict-stamp", "OUT", 0.03, P["redink"], K.on_front((0.07, yf - 0.0009, 0.095)),
                        fit=(0.09, 0.035))]
        for ob in stamp:
            geo.transform(ob, Matrix.Translation((0.07, 0, 0.095)) @ Matrix.Rotation(math.radians(12), 4, (0, 1, 0))
                          @ Matrix.Translation((-0.07, 0, -0.095)))
        return stamp + [_scribble("evict-sign", (-0.13, 0.06), 0.11, P["ink"], yf)]

    _paper(p, "EVICTION\nNOTICE", "redink", (1.0, 0.92, 0.97, 0.6, 1.0, 0.8), None, extra=extra)


@prop("lease", "Zip moved in (Archie checks an imaginary lease)",
      "grip: the middle of its bottom edge, text on the -Y face; 0.32 x 0.44 m",
      rig="sheet_1..4 (bends up the page): flutter, curl")
def lease(p):
    P = p.P

    def extra(yf):
        return [_scribble("lease-sign", (0.02, 0.07), 0.1, P["violet"], yf, amp=0.01),
                K.text("lease-tenant", "TENANT: ZIP", 0.022, P["violet"], K.on_front((-0.07, yf, 0.12)),
                       fit=(0.14, 0.025))]

    _paper(p, "LEASE", "ink", (1.0, 0.95, 0.9, 1.0, 0.7), "(fine print)", extra=extra)


# -------------------------------------------------------------------------------------------- labels
@prop("fragile-label", "The mic drop (Brick points to it)",
      "its back, at the middle (it sticks onto a surface), face towards -Y; 0.22 x 0.1 m")
def fragile_label(p):
    P = p.P
    W, H, d = 0.22, 0.1, 0.003
    p.add(K.plate("fragile", W, H, d, P["red"], (0, d / 2, 0), r=0.012, bevel=0.0012, steps=1))
    yf = -0.0008
    rim = [V(u, yf, v) for u, v in K.rrect(W * 0.92, H * 0.84, 0.009, 2)]
    p.add(geo.tube("fragile-rim", rim, 0.0018, P["white"], segs=4, caps=False, closed=True))
    p.add(K.text("fragile-text", "FRAGILE", 0.04, P["white"], K.on_front((0.022, yf, 0.008)), fit=(0.14, 0.045)))
    p.add(K.text("fragile-sub", "HANDLE WITH CARE", 0.012, P["white"], K.on_front((0.022, yf, -0.026)),
                 fit=(0.14, 0.014)))
    # a wine glass, the fragile sign
    gx = -0.077
    glass = [(gx - 0.016, 0.03), (gx + 0.016, 0.03), (gx + 0.013, 0.008), (gx + 0.003, -0.002), (gx + 0.003, -0.022),
             (gx + 0.012, -0.03), (gx - 0.012, -0.03), (gx - 0.003, -0.022), (gx - 0.003, -0.002), (gx - 0.013, 0.008)]
    p.add(K.poly_mesh("fragile-glass", glass, 0.0016, P["white"], center=(0, yf, 0), bevel=0.0004, steps=1))


def _stamp_mark(p, body, angle):
    P = p.P
    W, H = 0.4, 0.16
    R = Matrix.Rotation(math.radians(angle), 4, (0, 1, 0))
    outer = K.rrect(W, H, 0.02, 3)
    inner = K.rrect(W - 0.024, H - 0.024, 0.012, 3)
    bm_v = [(u, -0.0005, v) for u, v in outer] + [(u, -0.0005, v) for u, v in inner]
    n = len(outer)
    faces = [(j, (j + 1) % n, n + (j + 1) % n, n + j) for j in range(n)]
    me = bpy.data.meshes.new("stamp-rim")
    me.from_pydata(bm_v, [], faces)
    ob = bpy.data.objects.new("stamp-rim", me)
    geo.link(ob)
    me.materials.append(P["redink"])
    for f in me.polygons:
        if f.normal.y > 0:
            f.flip()
    p.add(geo.transform(ob, R))
    p.add(K.text("stamp-mark", body, 0.06, P["redink"], R @ K.on_front((0, -0.001, 0)), fit=(W * 0.84, H * 0.7),
                 line=0.85))


@prop("stamp-mark", "The inspection scam (the ink Archie stamps on the presentation)",
      "its middle, a flat decal facing -Y (single-sided; set it a millimetre off the surface); 0.4 x 0.16 m")
def stamp_mark(p):
    _stamp_mark(p, "QUALITY\nCHECKED", -8)


@prop("stamp-mark-licked", "The inspection scam (what the stamp really printed)",
      "its middle, a flat decal facing -Y (single-sided); 0.4 x 0.16 m")
def stamp_mark_licked(p):
    _stamp_mark(p, "I LICKED\nTHIS", 6)


# ---------------------------------------------------------------------------------------- the README
@prop("readme-slab", "Heavy README; The leveling dispute; The glass door; The README hostage situation; "
      "The unauthorized renovation",
      "floor, under its middle, page facing -Y; 1.9 m long, 0.6 m tall, a scroll-ended slab")
def readme_slab(p):
    P = p.P
    L, H, d = 1.7, 0.56, 0.1
    zc = 0.03 + H / 2
    p.add(K.plate("readme-page", L, H, d, P["paper"], (0, 0, zc), r=0.02, bevel=0.012))
    for s in (1, -1):
        x = s * (L / 2 + 0.035)
        p.add(K.cyl(f"readme-roller{s}", 0.07, (x, 0, 0.0), (x, 0, H + 0.06), P["graphite"], segs=16, bevel=0.015))
        for z in (0.0, H + 0.06):
            p.add(K.cyl(f"readme-cap{s}{z:.1f}", 0.05, (x, 0, z - 0.012), (x, 0, z + 0.012), P["lime"], segs=12,
                        bevel=0.006, steps=1))
    yf = -d / 2 - 0.0015
    x0 = -L / 2 + 0.12
    title = K.text("readme-title", "README.md", 0.15, P["graphite"], None, align="LEFT")
    geo.transform(title, K.on_front((x0, yf, zc + H * 0.32)))
    p.add(title)
    p.add(K.box("readme-rule", (L * 0.42, 0.001, 0.006), P["lime"], (0, yf, zc + H * 0.19)))
    z = zc + H * 0.08
    for k, frac in enumerate((0.95, 0.8, 0.88, 0.5)):
        p.add(K.box(f"readme-line{k}", ((L * 0.5) * frac / 2, 0.001, 0.012), P["ink"],
                    (x0 + (L * 0.5) * frac / 2, yf, z)))
        z -= 0.06
    cx = L * 0.22
    p.add(K.plate("readme-code", L * 0.32, H * 0.5, 0.008, P["graphite"], (cx, -d / 2 - 0.002, zc - H * 0.06),
                  r=0.02, bevel=0.002, steps=1))
    for k, frac in enumerate((0.7, 0.45, 0.85, 0.6)):
        w = L * 0.24 * frac
        p.add(K.box(f"readme-code{k}", (w / 2, 0.001, 0.008), P["lime"] if k % 2 == 0 else P["cream"],
                    (cx - L * 0.12 + w / 2, -d / 2 - 0.0065, zc + H * 0.11 - k * 0.055)))


# --------------------------------------------------------------------------------------- the app card
@prop("app-card", "Wrong way up; The scroll treadmill (Archie rides one); The escapee (he scoops the bot "
      "back with one)",
      "its middle, face towards -Y (material card-face, UVs filling the face, u left to right, v bottom to "
      "top); 1.2 x 0.8 m, 0.05 thick")
def app_card(p):
    P = p.P
    W, H, d = 1.2, 0.8, 0.05
    p.add(K.plate("card", W, H, d, P["ceramic"], (0, 0, 0), r=0.07, bevel=0.012, face=card_face()))
    p.add(K.text("card-back", "ARCHIE & PALS", 0.07, P["lime"], K.on_back((0, d / 2 + 0.0015, 0)), fit=(0.7, 0.08)))
    p.view = dict(az=30, el=10)


# ------------------------------------------------------------------------------------- replay screen
@prop("replay-screen", "The blame button (the replay proving they coordinated it; Archie closes it)",
      "its middle, floating, screen facing -Y (material screen-face, UVs filling it); 0.84 x 0.56 m",
      rig="panel (whole screen; scales) > playhead (slides along X), close_button (presses in +Y): pop_in, "
          "play, close")
def replay_screen(p):
    P = p.P
    W, H, d = 0.84, 0.56, 0.05
    p.bone("panel", (0, 0, 0), (0, 0, 0.2))
    p.add(K.plate("replay-frame", W, H, d, P["graphite"], (0, 0, 0), r=0.04, bevel=0.01), "panel")
    p.add(K.plate("replay-screen", W - 0.07, H - 0.13, 0.006, P["graphite"], (0, -d / 2 - 0.002, 0.025), r=0.015,
                  bevel=0.002, steps=1, face=screen_face()), "panel")
    # REPLAY tab on top, with a glowing red dot
    tab_z = H / 2 + 0.035
    p.add(K.plate("replay-tab", 0.24, 0.07, 0.03, P["red"], (-W / 2 + 0.16, 0, tab_z - 0.01), r=0.035, bevel=0.006),
          "panel")
    p.add(K.ball("replay-dot", 0.012, P["holo_red"], (-W / 2 + 0.07, -0.016, tab_z - 0.01), res=3,
                 scale=(1, 0.5, 1)), "panel")
    p.add(K.text("replay-label", "REPLAY", 0.035, P["white"], K.on_front((-W / 2 + 0.175, -0.0165, tab_z - 0.01)),
                 fit=(0.15, 0.04)), "panel")
    # scrub bar and playhead
    zb = -H / 2 + 0.035
    p.add(K.capsule("replay-track", (-W / 2 + 0.06, -d / 2 - 0.002, zb), (W / 2 - 0.06, -d / 2 - 0.002, zb), 0.006,
                    P["white"], segs=8, rings=2), "panel")
    x0, x1 = -W / 2 + 0.06, W / 2 - 0.06
    p.bone("playhead", (x0, -d / 2 - 0.01, zb), (x0, -d / 2 - 0.05, zb), parent="panel")
    p.add(K.ball("replay-playhead", 0.016, P["lime"], (x0, -d / 2 - 0.006, zb), res=3), "playhead")
    # the close button, top right
    cb = V(W / 2 - 0.02, -d / 2 - 0.004, H / 2 - 0.02)
    p.bone("close_button", cb, cb + V(0, -0.04, 0), parent="panel")
    p.add(K.cyl("replay-close", 0.034, cb + V(0, 0.01, 0), cb + V(0, -0.012, 0), P["red"], segs=16, bevel=0.006),
          "close_button")
    for a in (45, -45):
        p.add(K.box(f"replay-x{a}", (0.018, 0.002, 0.0045), P["white"], cb + V(0, -0.0135, 0), bevel=0.0015,
                    rot=Matrix.Rotation(math.radians(a), 3, (0, 1, 0))), "close_button")

    def pop_in(t):
        k = K.ease("back", t / 0.45)
        return {"panel": dict(scale=(max(k, 1e-3),) * 3)}

    def play(t):
        return {"playhead": dict(move=((x1 - x0) * min(1.0, t / 3.0), 0, 0))}

    def close(t):
        press = K.pulse(t, 0.0, 0.08, 0.06, 0.1)
        k = 1 - K.ease("in", (t - 0.25) / 0.3) if t > 0.25 else 1.0
        return {"close_button": dict(move=(0, 0.008 * press, 0)), "panel": dict(scale=(max(k, 1e-3),) * 3)}

    p.clip("pop_in", 0.6, pop_in)
    p.clip("play", 3.0, play)
    p.clip("close", 0.6, close)
    p.view = dict(az=25, el=8)


# ---------------------------------------------------------------------------------------- error face
@prop("error-face", "The fake crash (Archie's own face shows an error)",
      "the screen's front middle; it curves round a 0.33 m sphere centred 0.33 m behind that point (Archie's "
      "face), screen facing -Y; 0.40 x 0.28 m",
      rig="screen (the whole panel; scales): on (a tube telly coming on: a line that opens), off (closes to a "
          "line and goes)")
def error_face(p):
    import bmesh
    P = p.P
    R, W, H, T = 0.33, 0.40, 0.28, 0.012
    C = V(0, R, 0)                                  # the sphere's centre

    def on_sphere(x, z, out=0.0):
        """The point of the sphere (pushed `out` towards the front) in front of (x, z)."""
        d = V(x, -math.sqrt(max(1e-6, R * R - x * x - z * z)), z).normalized()
        return C + d * (R + out)

    p.bone("screen", (0, 0, 0), (0, 0, 0.12))
    bm = bmesh.new()
    nx, nz, rr = 20, 14, 0.05
    grid = {}
    for i in range(nx + 1):
        for j in range(nz + 1):
            u, v = -W / 2 + W * i / nx, -H / 2 + H * j / nz
            # rounded corners: a grid point past a corner's arc goes onto it
            cx, cz = max(-W / 2 + rr, min(W / 2 - rr, u)), max(-H / 2 + rr, min(H / 2 - rr, v))
            d = math.hypot(u - cx, v - cz)
            if d > rr:
                u, v = cx + (u - cx) * rr / d, cz + (v - cz) * rr / d
            grid[i, j] = bm.verts.new(on_sphere(u, v))
    for i in range(nx):
        for j in range(nz):
            bm.faces.new((grid[i, j], grid[i + 1, j], grid[i + 1, j + 1], grid[i, j + 1]))
    edge = ([grid[i, 0].co.copy() for i in range(nx + 1)] + [grid[nx, j].co.copy() for j in range(1, nz + 1)] +
            [grid[i, nz].co.copy() for i in range(nx - 1, -1, -1)] + [grid[0, j].co.copy() for j in range(nz - 1, 0, -1)])
    panel = geo.mesh_object("error-panel", bm, P["screen_blue"])
    if panel.data.polygons[0].normal.y > 0:                  # its face towards -Y
        panel.data.flip_normals()
    sol = panel.modifiers.new("solidify", "SOLIDIFY")
    sol.thickness, sol.offset, sol.use_rim = T, -1.0, True          # back from its face, so the type sits on it
    p.add(panel, "screen")
    # a graphite bezel round its edge
    ring = [C + (q - C).normalized() * (R + 0.002) for q in edge]
    p.add(geo.tube("error-bezel", ring, 0.008, P["graphite"], segs=6, caps=False, closed=True), "screen")

    def type_(name, body, size, fit, at):
        """Flat type (facing -Y), moved to `at` (x, z) on the screen and laid onto its curve."""
        ob = K.text(name, body, size, P["screen_ink"], K.on_front((0, 0, 0)), fit=fit)
        for v in ob.data.vertices:
            v.co = on_sphere(v.co.x + at[0], v.co.z + at[1], 0.004)
        ob.data.update()
        return p.add(ob, "screen")

    type_("error-sad", ":(", 0.13, (0.16, 0.12), (-0.03, 0.035))
    type_("error-line", "NOT RESPONDING", 0.03, (0.3, 0.03), (0.0, -0.085))

    # (the bone runs up the screen: its scale is (across, up, through))
    def on(t):
        # a line across first, then it opens; a little overshoot
        w = K.ease("out", t / 0.12)
        h = 0.03 + 0.97 * K.ease("back", (t - 0.1) / 0.25) if t > 0.1 else 0.03
        return {"screen": dict(scale=(max(w, 1e-3), max(h, 1e-3), 1))}

    def off(t):
        h = 1 - 0.97 * K.ease("in", t / 0.15)
        w = 1 - K.ease("in", (t - 0.15) / 0.15) if t > 0.15 else 1.0
        return {"screen": dict(scale=(max(w, 1e-3), max(h, 1e-3), 1))}

    p.clip("on", 0.4, on)
    p.clip("off", 0.3, off)
    p.view = dict(az=20, el=6)


# --------------------------------------------------------------------------------------- tiny button
@prop("tiny-button", "The unnecessary crew (the one tiny button)",
      "floor, under the middle of its bottom edge, face towards -Y; 0.15 m wide (decorative: the page's real "
      "buttons are untouched)")
def tiny_button(p):
    P = p.P
    W, H, d = 0.15, 0.056, 0.036
    p.add(K.plate("button", W, H, d, P["lime"], (0, 0, H / 2), r=H / 2 - 0.001, bevel=0.009, seg=5))
    p.add(K.text("button-text", "OK", 0.03, P["graphite"], K.on_front((0, -d / 2 - 0.0012, H / 2)),
                 fit=(0.1, 0.03)))


# ------------------------------------------------------------------------------------------ mustache
@prop("mustache", "The sleepy atlas (Zip draws it on a little hologram of Archie)",
      "its middle, flat, facing -Y; 0.14 m wide (marker ink; scale it to the hologram)",
      rig="curl_L, curl_R (each grows out from the middle): draw")
def mustache(p):
    P = p.P
    # one half's centre line (x out from the middle, z up) and its width along it: full under the nose,
    # sweeping out and down, the tip curling back up
    path = [(0.003, 0.002), (0.016, -0.004), (0.03, -0.01), (0.044, -0.011), (0.056, -0.005), (0.063, 0.006),
            (0.061, 0.016), (0.054, 0.019), (0.049, 0.014)]
    width = [0.013, 0.013, 0.012, 0.01, 0.008, 0.006, 0.0045, 0.0035, 0.0025]
    for s, side in ((1, "_L"), (-1, "_R")):
        pts = [V(s * x, 0, z) for x, z in path]
        fine = K.polyline(pts, 24)
        wf = [width[min(len(width) - 1, int(k / 24 * (len(width) - 1) + 0.5))] for k in range(25)]
        bn = p.bone("curl" + side, (0, 0, 0), (s * 0.06, 0, 0))
        p.add(geo.sweep("mustache" + side, fine, wf, [w * 0.35 for w in wf], P["black"], segs=8, up=(0, -1, 0)), bn)

    def draw(t):
        return {f"curl{sd}": dict(scale=(max(1e-3, K.ease("out", (t - d0) / 0.35)),) * 3)
                for sd, d0 in (("_L", 0.0), ("_R", 0.35))}

    p.clip("draw", 0.9, draw)
    p.view = dict(az=15, el=5)
