"""Archie 'Atlas' Algorithm, in three dimensions, built from nothing but this script.

Run it headless and it writes three files:

    blender --background --factory-startup --python art/archie/archie.py

  * `art/archie/archie.blend`  -- the scene, for anyone who wants to open it and push vertices around.
  * `docs/assets/archie.glb`   -- the animated model the homepage banner loads, with twenty named glTF
                                  animations at 30 fps: `idle` (a four-second loop: sway, foot tap,
                                  blinks), `watch`, `sit`, `sleep`, thirteen Fortnite dances (`floss`,
                                  `take-the-l`, `default-dance`, `orange-justice`, `robot`,
                                  `electro-shuffle`, `hype`, `boogie-down`, `get-griddy`, `billy-bounce`,
                                  `fresh`, `scenario`, `groove-jam`) of fifteen or sixteen seconds each,
                                  `press` (jabbing at a button that won't work), `shrug`, and `walk`,
                                  one stride in place that the page moves across the banner. Every clip
                                  but `idle` and `walk` starts and ends on the idle's first pose, so the
                                  page can play any of them between two idles without a jump.
  * `docs/assets/archie-3d.webp` -- a transparent still of the idle's first frame, for reduced motion, for
                                  narrow screens, and for any browser that cannot or will not run WebGL.

Procedural rather than sculpted, for the reason the rest of this repository prefers generators to hand-made
output: the model is a function of the numbers below, so a change to it is a reviewable diff instead of a
binary nobody can read. The reference is `docs/assets/atlas-byte.png` -- charcoal body, gold accents, a
gold globe for a chest, an orbit ring round the waist, headphone cups, an antenna, pixel shades, one thumb up
and one hand on the hip.

Two liberties, both for the animation. The shades sit a little lower on the visor than in the drawing, so
that there are eyes above them to blink with; and the orbit ring carries its moon round once per loop.

Its surfaces are textured too, and the textures are generated here like everything else: tiling noise and
line work, painted into 1024-pixel normal and roughness/metal maps -- staggered plate seams, rivets and
gold circuit traces on the shell (the traces glow), brushed gold, gritty joints, and relief on the globe's
continents -- and projected onto each part in metres so that a texel is the same size everywhere.

Everything animated is animated at object level -- a hierarchy of pivots with no armature and no skinning --
because that is the cheapest thing glTF can carry and the cheapest thing a browser can play, and a robot is
rigid parts anyway. Each clip is a function of its own phase; the idle's is periodic, so its frame 120
runs straight back into frame 1 with no seam.
"""
from __future__ import annotations

import math
import sys
import zlib
from pathlib import Path

import bmesh
import bpy
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BLEND = HERE / "archie.blend"
GLB = ROOT / "docs" / "assets" / "archie.glb"
POSTER = ROOT / "docs" / "assets" / "archie-3d.webp"

FPS = 30
LOOP = 120                      # four seconds
TAU = math.tau

# `--preview` renders a still and stops, which is the loop for adjusting the model by eye.
PREVIEW = "--preview" in sys.argv


# ------------------------------------------------------------------------------------------------------
# Scene
# ------------------------------------------------------------------------------------------------------

def reset() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start, sc.frame_end = 1, LOOP


def material(name: str, color, metal=0.0, rough=0.5, coat=0.0, glow=None, strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1.0)
    p.inputs["Metallic"].default_value = metal
    p.inputs["Roughness"].default_value = rough
    p.inputs["Coat Weight"].default_value = coat
    if glow:
        p.inputs["Emission Color"].default_value = (*glow, 1.0)
        p.inputs["Emission Strength"].default_value = strength
    return m


def smooth(ob) -> None:
    for poly in ob.data.polygons:
        poly.use_smooth = True


def link(ob, parent, mat=None):
    if parent is not None:
        ob.parent = parent
    if mat is not None:
        ob.data.materials.append(mat)
    return ob


def empty(name: str, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    ob.empty_display_size = 0.05
    bpy.context.collection.objects.link(ob)
    ob.parent = parent
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def ball(name, parent, loc, scale, mat, segs=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=rings, radius=1.0)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    smooth(ob)
    link(ob, parent, mat)
    ob.location = loc
    return ob


def blob(name, parent, loc, scale, mat, level=3):
    """A subdivided cube: the rounded-box shape every shell on this robot is."""
    bpy.ops.mesh.primitive_cube_add(size=2.0)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    ob.modifiers.new("round", "SUBSURF").levels = level
    ob.modifiers["round"].render_levels = level
    smooth(ob)
    link(ob, parent, mat)
    ob.location = loc
    return ob


def ring(name, parent, loc, rot, major, minor, mat):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=40,
                                     minor_segments=8)
    ob = bpy.context.object
    ob.name = name
    smooth(ob)
    link(ob, parent, mat)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


def rod(name, parent, loc, rot, radius, depth, mat, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth)
    ob = bpy.context.object
    ob.name = name
    smooth(ob)
    ob.modifiers.new("edge", "BEVEL").width = min(radius, depth) * 0.25
    ob.modifiers["edge"].segments = 2
    link(ob, parent, mat)
    ob.location = loc
    ob.rotation_euler = rot
    return ob


# ------------------------------------------------------------------------------------------------------
# The globe's texture: gold continents on a gold sea, with a graticule
# ------------------------------------------------------------------------------------------------------

def globe_field(w, h):
    """Equirectangular, and seamless because it is computed on the sphere rather than on the rectangle:
    each pixel's direction is fed to a sum of plane waves, so longitude 0 and 360 are the same point."""
    lon = (np.arange(w) + 0.5) / w * TAU - math.pi
    lat = math.pi / 2 - (np.arange(h) + 0.5) / h * math.pi
    lon, lat = np.meshgrid(lon, lat)
    d = np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], -1)
    rng = np.random.default_rng(54)            # fixed, so the planet is the same on every build
    field = np.zeros((h, w))
    for octave in range(5):
        freq, amp = 2.2 * 1.9 ** octave, 0.55 ** octave
        for _ in range(7):
            k = rng.normal(size=3)
            k /= np.linalg.norm(k)
            field += amp * np.sin(freq * (d @ k) + rng.uniform(0, TAU))
    return field, lon, lat


def globe_image(w=1024, h=512):
    field, lon, lat = globe_field(w, h)
    land = field > np.quantile(field, 0.63)
    sea = np.array([1.00, 0.70, 0.16])
    ground = np.array([0.50, 0.29, 0.04])
    rgb = np.where(land[..., None], ground, sea)
    # Shade the sea toward the coast, the way the drawing's ocean darkens at the land's edge.
    coast = np.clip((field - np.quantile(field, 0.45)) / (np.quantile(field, 0.63) - np.quantile(field, 0.45)),
                    0, 1)
    rgb = np.where(land[..., None], rgb, sea - coast[..., None] * np.array([0.18, 0.16, 0.06]))
    lines = np.zeros((h, w), bool)
    for deg in range(-90, 91, 20):
        lines |= np.abs(np.degrees(lat) - deg) < 0.45
    for deg in range(-180, 181, 20):
        lines |= np.abs(np.degrees(lon) - deg) < 0.45 / np.maximum(np.cos(lat), 0.2)
    rgb = np.where(lines[..., None], rgb * 0.62, rgb)
    img = bpy.data.images.new("globe", w, h, alpha=False)
    px = np.concatenate([rgb[::-1], np.ones((h, w, 1))], -1).astype(np.float32)
    img.pixels.foreach_set(px.ravel())
    img.pack()
    return img


def globe_material():
    m = material("globe", (1, 0.7, 0.2), metal=0.85, rough=0.32)
    nt = m.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = globe_image()
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    # A little of its own light, so the chest reads as the brightest thing on the robot as it does in the
    # drawing, and not only when a light happens to catch it.
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Emission Color"])
    nt.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.5
    # The continents stand proud of the sea, and are rougher than it.
    relief, rough = globe_relief()
    detail(m, normal=relief, orm=rough)
    return m


# ------------------------------------------------------------------------------------------------------
# Surface detail: panel seams, rivets, gold circuit traces, brushing and smudges
# ------------------------------------------------------------------------------------------------------
# Every texture below is computed, tiles seamlessly (each is a sum of whole waves across the tile, or a
# pattern on the tile's own grid), and is fixed by its seed, so the robot is the same on every build. The
# shells are box-projected in metres (`box_uv`), so a seam is the same width on the helmet as on a shin.
#
# At the banner's size he is about 100 CSS pixels a metre, so detail finer than a centimetre never reaches
# the screen: the seams are 8 mm, the traces 5 mm, and 1024 texels across a 60 cm tile is already more than
# a visit's close-up can show.

TILE = 0.6                      # metres of surface one repeat of the shell textures covers
N = 1024


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def waves(n, lo, hi, seed, stretch=1.0):
    """Tiling noise, unit variance: white noise kept to the band of lo..hi cycles a tile. `stretch` > 1
    squeezes the band along x, for streaks that run along y."""
    rng = np.random.default_rng(seed)
    f = np.fft.fft2(rng.normal(size=(n, n)))
    ky, kx = np.meshgrid(np.fft.fftfreq(n) * n, np.fft.fftfreq(n) * n, indexing="ij")
    k = np.hypot(kx * stretch, ky / stretch)
    x = np.real(np.fft.ifft2(f * ((k >= lo) & (k <= hi))))
    return x / (x.std() + 1e-9)


def to_normal(h, strength):
    """A tangent-space normal map (glTF's, +Y up) from a height field whose rows run bottom to top."""
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength
    v = np.stack([-gx, -gy, np.ones_like(h)], -1)
    return v / np.linalg.norm(v, axis=-1, keepdims=True) * 0.5 + 0.5


def image(name, rgb, colour=False):
    """Pack an (h, w, 3) array, rows bottom to top, as a Blender image. Data maps are Non-Color."""
    h, w = rgb.shape[:2]
    img = bpy.data.images.new(name, w, h, alpha=False)
    img.colorspace_settings.name = "sRGB" if colour else "Non-Color"
    img.pixels.foreach_set(np.concatenate([rgb, np.ones((h, w, 1))], -1).astype(np.float32).ravel())
    img.pack()
    return img


def orm(rough, metal):
    """glTF's metallic-roughness packing: roughness in green, metalness in blue."""
    return np.stack([np.ones_like(rough), rough, np.broadcast_to(metal, rough.shape)], -1)


def hull():
    """The shells' tile: four rows of plates, each row cut at its own places so the seams stagger like
    brickwork; a rivet either side of every cut; and in a few plates a gold trace, a line with one right-
    angle turn that ends in a pad. Returns height, roughness and the traces' glow."""
    n = N
    y, x = np.mgrid[0:n, 0:n] + 0.5
    rng = np.random.default_rng(33)
    rows, rh = 4, n / 4
    per = lambda d: np.abs((d + n / 2) % n - n / 2)          # distance on the tile's torus
    dist = np.abs((y + rh / 2) % rh - rh / 2)                # to the nearest row seam
    row = (y // rh).astype(int)
    rivets, plates = [], []
    for r in range(rows):
        cuts = np.sort(rng.uniform(0, n, rng.integers(2, 4)))
        band = row == r
        for c in cuts:
            dist = np.where(band, np.minimum(dist, per(x - c)), dist)
            for side in (-1, 1):
                rivets.append((c + side * 22, r * rh + rh / 2))
        for a, b in zip(cuts, np.r_[cuts[1:], cuts[0] + n]):
            plates.append((a, b, r * rh, (r + 1) * rh))
    w = 7                                                    # the seam's half width, texels: 8 mm
    groove = smoothstep(w, w * 0.35, dist)
    h = -groove
    for cx, cy in rivets:
        d = np.hypot(per(x - cx), per(y - cy))
        h += 0.7 * np.sqrt(np.clip(1 - (d / 7) ** 2, 0, 1))
    trace = np.zeros((n, n))

    def segment(ax, ay, bx, by, r):
        px, py = (x - ax + n / 2) % n - n / 2, (y - ay + n / 2) % n - n / 2      # signed, on the torus
        vx, vy = bx - ax, by - ay
        t = np.clip((px * vx + py * vy) / (vx * vx + vy * vy + 1e-9), 0, 1)
        return np.hypot(px - t * vx, py - t * vy) - r

    for a, b, lo, hi in plates:
        if rng.random() > 0.45 or b - a < 120:
            continue
        # From one end of the plate, along it, then turning up or down to a pad, all inside the plate.
        sx = a + 40 if rng.random() < 0.5 else b - 40
        sy = rng.uniform(lo + 45, hi - 45)
        ex = sx + (1 if sx < (a + b) / 2 else -1) * rng.uniform(0.35, 0.7) * (b - a - 80)
        ey = np.clip(sy + rng.choice([-1, 1]) * rng.uniform(40, 90), lo + 35, hi - 35)
        d = np.minimum(segment(sx, sy, ex, sy, 2.5), segment(ex, sy, ex, ey, 2.5))
        d = np.minimum(d, segment(ex, ey, ex, ey, 8.0))       # the pad
        d = np.minimum(d, segment(sx, sy, sx, sy, 5.0))
        trace = np.maximum(trace, smoothstep(1.2, -0.6, d))
    h += 0.25 * trace + 0.04 * waves(n, 40, 160, 5)
    smudge = waves(n, 1, 4, 8)
    rough = np.clip(0.24 + 0.06 * smudge + 0.25 * groove - 0.08 * trace, 0.08, 0.9)
    return h, rough, trace


def brushed():
    """Gold's tile: streaks along one direction, in the roughness and a little in the surface."""
    s = waves(N // 2, 20, 200, 12, stretch=8.0)
    return 0.03 * s, np.clip(0.2 + 0.05 * s + 0.04 * waves(N // 2, 1, 4, 13), 0.08, 0.6)


def grit():
    """The joints' and the visor's tile: fine grain in the surface and broad smudges in the roughness."""
    return 0.05 * waves(N // 2, 60, 200, 21), waves(N // 2, 1, 5, 22)


def globe_relief(w=1024, h=512):
    """The globe's land as a height field, from the same field `globe_image` thresholds."""
    field, _, _ = globe_field(w, h)
    land = smoothstep(np.quantile(field, 0.6), np.quantile(field, 0.66), field)
    return to_normal(land[::-1] * 6.0, 1.0), orm(0.22 + 0.25 * land[::-1], 0.85)


def detail(m, normal=None, orm=None, glow=None, glow_colour=(1.0, 0.55, 0.1), glow_strength=0.0):
    """Wire a material's maps: a normal map, a packed roughness-metal map and an emission mask."""
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    if normal is not None:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image(f"{m.name}-normal", normal)
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(tex.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
    if orm is not None:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image(f"{m.name}-orm", orm)
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tex.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Green"], p.inputs["Roughness"])
        nt.links.new(sep.outputs["Blue"], p.inputs["Metallic"])
    if glow is not None:
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = image(f"{m.name}-glow", glow[..., None] * np.array(glow_colour), colour=True)
        nt.links.new(tex.outputs["Color"], p.inputs["Emission Color"])
        p.inputs["Emission Strength"].default_value = glow_strength
    m["textured"] = True
    return m


def box_uv(ob) -> None:
    """UVs by box projection in metres, one tile every `TILE`, shifted per part so seams don't line up."""
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    uv = bm.loops.layers.uv.verify()
    s = ob.scale
    off = zlib.crc32(ob.name.encode()) % 997 / 997.0
    for f in bm.faces:
        ax = max(range(3), key=lambda i: abs(f.normal[i] * s[i]))
        for lp in f.loops:
            q = (lp.vert.co.x * s.x, lp.vert.co.y * s.y, lp.vert.co.z * s.z)
            u, v = [q[i] for i in range(3) if i != ax]
            lp[uv].uv = (u / TILE + off, v / TILE + off * 0.61)
    bm.to_mesh(me)
    bm.free()

# Each lens, drawn left to right as the viewer sees it; B black, W white glint, space nothing. Both lenses
# use the same strings unmirrored, so both glints sit toward the upper left of their lens, as drawn.
SHADES = [
    "BBBBBBB",
    "BWBWBBB",
    "BBWBWBB",
    "BBBBBBB",
    " BBBBB ",
]


def pixel_shades(parent, black, white, p=0.05):
    """The pixel sunglasses, as actual pixels: one cube per cell, both lenses and the bridge in a single
    mesh per colour so the glTF carries two primitives rather than seventy."""
    cells = {"B": [], "W": []}
    lens_w = len(SHADES[0])
    for side in (-1, 1):
        left = -p - lens_w * p if side < 0 else p          # the lens's left edge; the bridge is -p..p
        for r, row in enumerate(SHADES):
            for c, ch in enumerate(row):
                if ch != " ":
                    cells[ch].append((left + c * p + p / 2, -r * p))
    for c in (-1, 0):                                      # the bridge: two pixels on the top row
        cells["B"].append((c * p + p / 2, 0.0))
    obs = []
    for key, mat in (("B", black), ("W", white)):
        verts, faces = [], []
        for x, z in cells[key]:
            base = len(verts)
            h = p / 2
            for dx in (-h, h):
                for dy in (-h * 0.9, h * 0.9):
                    for dz in (-h, h):
                        verts.append((x + dx, dy - (0.004 if key == "W" else 0), z + dz))
            faces += [(base + a, base + b, base + c, base + d) for a, b, c, d in
                      ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3))]
        me = bpy.data.meshes.new(f"shades-{key}")
        me.from_pydata(verts, [], faces)
        ob = bpy.data.objects.new(f"shades-{key}", me)
        bpy.context.collection.objects.link(ob)
        link(ob, parent, mat)
        obs.append(ob)
    return obs


def build():
    # Near-black shells under a full clear coat: the body reads as darker than the drawing's charcoal and the
    # highlights stay sharp, so the gold has more to stand out against.
    body = material("body", (0.009, 0.010, 0.013), metal=0.6, rough=0.22, coat=1.0)
    joint = material("joint", (0.004, 0.004, 0.005), metal=0.4, rough=0.5)
    visor = material("visor", (0.004, 0.005, 0.009), metal=0.2, rough=0.04, coat=1.0)
    gold = material("gold", (1.0, 0.62, 0.10), metal=1.0, rough=0.18)
    # Emission kept low enough that no channel but red clips, so the rings read as gold light, not yellow.
    glow = material("glow", (1.0, 0.5, 0.04), metal=0.5, rough=0.3, glow=(1.0, 0.36, 0.0), strength=1.25)
    eyes = material("eyes", (1.0, 0.7, 0.2), glow=(1.0, 0.55, 0.08), strength=1.8)
    # Matte, with no specular at all: a glossy black pixel reflects the key light and reads as grey.
    black = material("pixel-black", (0.002, 0.002, 0.002), rough=1.0)
    black.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = 0.0
    white = material("pixel-white", (0.95, 0.95, 0.95), rough=0.35, glow=(1, 1, 1), strength=0.4)
    orbit = material("orbit", (0.95, 0.85, 0.6), metal=0.8, rough=0.2, glow=(1.0, 0.7, 0.3), strength=0.5)
    globe = globe_material()
    # The surface detail. The shells get the plates, rivets and gold traces; the coat is thinner than it
    # was, so the seams show through it as well as in it.
    h, rough, trace = hull()
    body.node_tree.nodes["Principled BSDF"].inputs["Coat Weight"].default_value = 0.6
    detail(body, normal=to_normal(h, 2.2), orm=orm(rough, 0.6), glow=trace, glow_strength=1.6)
    bh, br = brushed()
    detail(gold, normal=to_normal(bh, 2.0), orm=orm(br, 1.0))
    gh, gs = grit()
    detail(joint, normal=to_normal(gh, 2.0), orm=orm(np.clip(0.5 + 0.08 * gs, 0.2, 0.9), 0.4))
    detail(visor, orm=orm(np.clip(0.05 + 0.03 * np.maximum(gs, 0), 0.02, 0.3), 0.2))

    P = {}                                               # every pivot the animation drives
    root = P["root"] = empty("archie")

    # Hips and legs. The hips carry the sway, so the body leans from the waist and the feet stay put.
    hips = P["hips"] = empty("hips", root, (0, 0, 0.6))
    blob("pelvis", hips, (0, 0, 0.02), (0.22, 0.17, 0.1), joint)
    for side, name in ((-1, "right"), (1, "left")):
        leg = P[f"leg-{name}"] = empty(f"leg-{name}", hips, (side * 0.15, 0, -0.03))
        rod(f"thigh-{name}", leg, (0, 0, -0.1), (0, 0, 0), 0.085, 0.2, body)
        knee = P[f"knee-{name}"] = empty(f"knee-{name}", leg, (0, 0, -0.21))
        ball(f"kneecap-{name}", knee, (0, 0, 0), (0.1, 0.1, 0.07), joint)
        ring(f"knee-glow-{name}", knee, (0, -0.07, 0), (math.pi / 2, 0, 0), 0.06, 0.014, glow)
        rod(f"shin-{name}", knee, (0, 0, -0.12), (0, 0, 0), 0.095, 0.2, body)
        # The heel is the tap's hinge: the boot hangs off an empty at its back edge.
        heel = P[f"heel-{name}"] = empty(f"heel-{name}", knee, (0, 0.13, -0.27))
        blob(f"boot-{name}", heel, (side * 0.01, -0.18, 0.0), (0.16, 0.25, 0.11), body)
        blob(f"sole-{name}", heel, (side * 0.01, -0.18, -0.1), (0.165, 0.255, 0.025), joint, level=2)
        ring(f"ankle-{name}", heel, (side * 0.165, -0.15, 0.02), (0, math.pi / 2, 0), 0.06, 0.013, glow)

    # Torso: a rounded shell with the globe set into its chest and the orbit ring round its waist.
    torso = P["torso"] = empty("torso", hips, (0, 0, 0.08))
    blob("chest", torso, (0, 0.02, 0.33), (0.42, 0.32, 0.37), body)
    ball("globe", torso, (0, -0.1, 0.32), (0.3, 0.3, 0.3), globe, segs=48, rings=24).rotation_euler = (
        0, 0, math.radians(-100))
    ring("globe-rim", torso, (0, -0.16, 0.32), (math.pi / 2, 0, 0), 0.285, 0.02, gold)
    # A torus lies flat by default, so the tilt is a few degrees, not ninety.
    tilt = empty("orbit-tilt", torso, (0, 0, 0.2), (math.radians(14), math.radians(-10), 0))
    ring("orbit-ring", tilt, (0, 0, 0), (0, 0, 0), 0.66, 0.007, orbit)
    spin = P["orbit"] = empty("orbit-spin", tilt)
    ball("moon", spin, (0.66, 0, 0), (0.045, 0.045, 0.045), glow)
    rod("neck", torso, (0, 0.03, 0.72), (0, 0, 0), 0.13, 0.12, joint)

    # Arms. Robot's right is -X (it faces -Y), which is the viewer's left: the thumb, as drawn.
    for side, name in ((-1, "right"), (1, "left")):
        sh = P[f"shoulder-{name}"] = empty(f"shoulder-{name}", torso, (side * 0.45, 0.03, 0.54))
        ball(f"deltoid-{name}", sh, (0, 0, 0), (0.12, 0.12, 0.12), body)
        ring(f"shoulder-glow-{name}", sh, (side * 0.1, 0, 0), (0, math.pi / 2, 0), 0.075, 0.016, glow)
        upper = P[f"upper-{name}"] = empty(f"upper-{name}", sh, (side * 0.04, 0, -0.04))
        rod(f"bicep-{name}", upper, (0, 0, -0.12), (0, 0, 0), 0.07, 0.2, body)
        elbow = P[f"elbow-{name}"] = empty(f"elbow-{name}", upper, (0, 0, -0.25))
        ball(f"elbow-ball-{name}", elbow, (0, 0, 0), (0.08, 0.08, 0.08), joint)
        ring(f"elbow-glow-{name}", elbow, (0, 0, 0), (0, math.pi / 2, 0), 0.07, 0.014, glow)
        rod(f"forearm-{name}", elbow, (0, 0, -0.12), (0, 0, 0), 0.08, 0.2, body)
        hand = P[f"hand-{name}"] = empty(f"hand-{name}", elbow, (0, 0, -0.28))
        ball(f"fist-{name}", hand, (0, 0, 0), (0.1, 0.095, 0.1), body)
        for i in range(3):                                           # knuckles, on the fist's front
            ball(f"knuckle-{name}-{i}", hand, (0, -0.075, 0.045 - i * 0.045), (0.05, 0.035, 0.028), body)
    # Thumb on the right fist, pointing along the forearm's continuation -- which the pose turns skyward.
    ball("thumb", P["hand-right"], (0, -0.02, -0.12), (0.035, 0.035, 0.07), body)
    # The watch, on the left wrist, for the clip that looks at it.
    ring("watch-band", P["elbow-left"], (0, 0, -0.2), (0, 0, 0), 0.085, 0.02, gold)
    rod("watch-face", P["elbow-left"], (0, -0.09, -0.2), (math.pi / 2, 0, 0), 0.045, 0.02, glow, 24)

    # Head: helmet, visor, headphone cups, antenna, eyes and shades.
    head = P["head"] = empty("head", torso, (0, 0.02, 0.74))
    blob("helmet", head, (0, 0, 0.34), (0.46, 0.42, 0.42), body)
    blob("visor", head, (0, -0.1, 0.31), (0.38, 0.34, 0.3), visor)
    for side in (-1, 1):
        rod(f"cup-{side}", head, (side * 0.45, 0.02, 0.31), (0, math.pi / 2, 0), 0.16, 0.12, joint, 32)
        ring(f"cup-glow-{side}", head, (side * 0.515, 0.02, 0.31), (0, math.pi / 2, 0), 0.115, 0.022, glow)
    ant = P["antenna"] = empty("antenna", head, (0.16, 0.05, 0.7), (0, math.radians(16), 0))
    rod("antenna-rod", ant, (0, 0, 0.14), (0, 0, 0), 0.012, 0.28, joint, 12)
    ball("antenna-tip", ant, (0, 0, 0.3), (0.045, 0.045, 0.045), glow)
    eyes_pivot = P["eyes"] = empty("eyes", head, (0, -0.415, 0.42))
    for side in (-1, 1):
        ball(f"eye-{side}", eyes_pivot, (side * 0.15, 0, 0), (0.07, 0.02, 0.042), eyes, segs=24, rings=12)
    shades = empty("shades", head, (0, -0.445, 0.36))
    pixel_shades(shades, black, white)
    for side in (-1, 1):
        rod(f"temple-{side}", shades, (side * 0.39, 0.2, 0.0), (math.pi / 2, 0, 0), 0.016, 0.4, black, 8)
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob.name != "globe" and ob.data.materials and ob.data.materials[0].get("textured"):
            box_uv(ob)
    return P


# ------------------------------------------------------------------------------------------------------
# The poses. Everything is Euler degrees on a named pivot, relative to the pivot's built rotation.
# ------------------------------------------------------------------------------------------------------

# The resting stance every clip starts and ends on, so the page can play any clip after any other.
REST = {
    "upper-right": (0, 30, 0), "elbow-right": (-25, 140, 0),       # thumbs up
    "upper-left": (0, -35, 0), "elbow-left": (0, 80, 0),           # hand on hip
}

# Straight arms, for the floss.
DOWN = {"upper-right": (0, 8, 0), "elbow-right": (0, 0, 0), "upper-left": (0, -8, 0), "elbow-left": (0, 0, 0)}


def smooth01(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


# `(R, T)` while a dance is being posed as one of R repeats of its pattern, T being the phase of the whole
# repeated clip; `None` otherwise. See `pose_at`.
LONG: tuple | None = None


def envelope(t: float, a: float, b: float, c: float, d: float) -> float:
    """0 before a, easing to 1 by b, holding until c, easing back to 0 by d.

    While `LONG` is set, the envelope is taken over the whole repeated clip instead of the one pattern `t`
    is the phase of, with the ramps kept the same length in frames. So a dance eases in from `REST` once at
    the start and out once at the end, and it doesn't dip back to rest between repeats."""
    if LONG:
        r, t = LONG
        a, b, c, d = a / r, b / r, 1 - (1 - c) / r, 1 - (1 - d) / r
    return smooth01((t - a) / (b - a)) * (1 - smooth01((t - c) / (d - c)))


def blink(t: float, at: float, width=0.035) -> float:
    """1 while open, dipping to 0.08 over `width` of the clip centred on `at`."""
    d = min(abs(t - at), 1 - abs(t - at))
    return 1.0 - 0.92 * max(0.0, 1.0 - d / (width / 2)) ** 1.5


def mix(a: dict, b: dict, w: float) -> dict:
    keys = set(a) | set(b)
    z = (0, 0, 0)
    return {k: tuple(x + (y - x) * w for x, y in zip(a.get(k, z), b.get(k, z))) for k in keys}


def add(pose: dict, name: str, dx=0.0, dy=0.0, dz=0.0) -> None:
    x, y, z = pose.get(name, (0, 0, 0))
    pose[name] = (x + dx, y + dy, z + dz)


# Each clip is (frames, function of phase t in [0,1) -> (rotations, locations, eye scale)). `idle` is a true
# loop; the others start and end on `REST` so that any of them can be dropped between two idles.

def idle(t):
    pose = dict(REST)
    tap = max(0.0, math.sin(TAU * 4 * t)) ** 2          # four taps a loop, one a second
    sway = math.sin(TAU * 2 * t)
    lag = math.sin(TAU * 2 * t - 0.9)
    add(pose, "hips", dy=3.5 * sway, dz=4 * math.sin(TAU * t))
    for s in ("right", "left"):
        add(pose, f"leg-{s}", dy=-3.5 * sway)
    add(pose, "heel-left", dx=-20 * tap)
    add(pose, "torso", dy=1.5 * lag)
    add(pose, "head", dx=3 * tap, dy=5 * lag, dz=3 * math.sin(TAU * t))
    add(pose, "antenna", dy=9 * math.sin(TAU * 2 * t - 1.8))
    add(pose, "upper-right", dx=4 * tap)
    add(pose, "orbit", dz=-360 * t)
    return pose, {"hips": (0, 0, 0.012 * tap)}, blink(t, 0.31) * blink(t, 0.83) * blink(t, 0.9)


def watch(t):
    """Raises the left wrist, looks down at it, taps a foot impatiently, looks up at the viewer."""
    up = envelope(t, 0.05, 0.22, 0.72, 0.9)
    look = {
        "upper-left": (-55, -20, 0), "elbow-left": (-10, 20, -95),
        "head": (-16, 0, 14), "torso": (0, 0, 6),
    }
    pose = mix(REST, {**REST, **look}, up)
    tap = max(0.0, math.sin(TAU * 7 * t)) ** 2 * envelope(t, 0.3, 0.36, 0.66, 0.72)
    add(pose, "heel-right", dx=-22 * tap)
    add(pose, "head", dy=4 * math.sin(TAU * 3 * t) * up)
    add(pose, "orbit", dz=-360 * t)
    return pose, {}, blink(t, 0.5) * blink(t, 0.95)


def floss(t):
    """The floss: straight arms swung together side to side, crossing in front and then behind, with the
    hips going the other way."""
    on = envelope(t, 0.0, 0.1, 0.9, 1.0)
    beats = 6
    swing = math.sin(TAU * beats * t)
    front = math.cos(TAU * beats * t)                    # alternates the arms crossing in front / behind
    pose = mix(REST, DOWN, on)
    for s, sign in (("right", -1), ("left", 1)):
        add(pose, f"upper-{s}", dx=-28 * front * on, dy=38 * swing * on)
    add(pose, "hips", dy=-9 * swing * on, dz=-6 * swing * on)
    for s in ("right", "left"):
        add(pose, f"leg-{s}", dy=9 * swing * on)
    add(pose, "head", dy=8 * swing * on, dx=-4 * abs(swing) * on)
    add(pose, "antenna", dy=-14 * swing * on)
    add(pose, "orbit", dz=-720 * t)
    bounce = 0.03 * abs(math.sin(TAU * beats * t)) * on
    return pose, {"hips": (0, 0, bounce)}, blink(t, 0.45)


def sit(t):
    """Sits on the ground with the knees up, rests, and gets back up."""
    down = envelope(t, 0.05, 0.28, 0.7, 0.92)
    seated = {
        **REST,
        "leg-right": (-85, 0, -6), "leg-left": (-85, 0, 6),
        "knee-right": (95, 0, 0), "knee-left": (95, 0, 0),
        "heel-right": (-10, 0, 0), "heel-left": (-10, 0, 0),
        "torso": (-6, 0, 0), "head": (6, 0, -8),
        "upper-left": (20, -35, 0),
    }
    pose = mix(REST, seated, down)
    rest_t = envelope(t, 0.3, 0.36, 0.64, 0.7)
    add(pose, "head", dy=6 * math.sin(TAU * 2 * t) * rest_t)
    add(pose, "orbit", dz=-360 * t)
    # Turned a third of the way to profile while down: seen square-on, knees raised toward the camera
    # foreshorten to nothing and the pose reads as "shorter", not "sitting".
    add(pose, "root", dz=-35 * down)
    return pose, {"hips": (0, 0.03 * down, -0.35 * down)}, blink(t, 0.4) * blink(t, 0.6)


def sleep(t):
    """Leans on the side of the banner's window, nods off, snores a little, and wakes with a start."""
    lean = envelope(t, 0.03, 0.16, 0.86, 0.96)
    doze = envelope(t, 0.22, 0.34, 0.84, 0.86)            # the eyes; the wake at 0.84 is sudden on purpose
    leaning = {**REST, "root": (0, 11, 0), "leg-left": (0, -6, 0), "heel-left": (0, 0, 0),
               "upper-left": (0, -70, 0), "elbow-left": (0, 60, 0), "head": (6, 12, 0)}
    pose = mix(REST, leaning, lean)
    breathe = math.sin(TAU * 5 * t) * doze
    add(pose, "head", dx=10 * doze + 3 * breathe, dy=6 * doze)
    add(pose, "torso", dx=1.5 * breathe)
    add(pose, "antenna", dy=-20 * doze)
    add(pose, "orbit", dz=-180 * t)
    startle = envelope(t, 0.84, 0.86, 0.87, 0.93)
    add(pose, "head", dx=-8 * startle)
    return pose, {"hips": (0, 0, 0.03 * startle)}, 1.0 - 0.93 * doze


def walk(t):
    """One stride of each leg, in place: `archie.js` moves the model across the banner while this plays,
    at the speed the stride covers, and plays it backwards for the moonwalk back in. Arms down and swinging
    against the legs, so it reads as a walk and not as the idle's pose sliding."""
    s = math.sin(TAU * t)
    pose = dict(DOWN)
    for side, sign in (("right", 1), ("left", -1)):
        swing = sign * s                                # +1: this leg forward
        add(pose, f"leg-{side}", dx=-STRIDE * swing)
        # The knee bends through the swing, while the foot is off the ground and coming forward.
        lift = max(0.0, math.sin(TAU * t + (0 if sign > 0 else math.pi) + math.pi / 2))
        add(pose, f"knee-{side}", dx=38 * lift)
        add(pose, f"heel-{side}", dx=-12 * lift + 10 * max(0.0, swing))
        add(pose, f"upper-{side}", dx=24 * swing)
        add(pose, f"elbow-{side}", dx=-18 - 10 * max(0.0, swing))
    add(pose, "hips", dz=5 * s)
    add(pose, "torso", dx=-4, dz=-3 * s)
    add(pose, "head", dx=3, dz=2 * s)
    add(pose, "antenna", dx=-10 * abs(math.cos(TAU * t)))
    add(pose, "orbit", dz=-360 * t)
    return pose, {"hips": (0, 0, 0.025 * abs(math.cos(TAU * t)) - 0.02)}, 1.0


def take_the_l(t):
    """Take the L: one hand an L on the forehead, the other arm swinging, hopping from foot to foot with the
    free leg kicked out to the side."""
    on = envelope(t, 0.0, 0.08, 0.92, 1.0)
    beats = 8
    hop = math.sin(TAU * beats / 2 * t)                 # +1 on the left foot, -1 on the right
    pose = mix(REST, {**DOWN, "upper-right": (-130, 20, 0), "elbow-right": (100, 0, 0),
                      "hand-right": (0, 0, 0), "head": (-6, 0, 0)}, on)
    for side, sign in (("right", 1), ("left", -1)):
        kick = max(0.0, sign * hop)                     # this leg is the one kicked out
        add(pose, f"leg-{side}", dy=sign * 38 * kick * on, dx=-10 * kick * on)
        add(pose, f"knee-{side}", dx=28 * kick * on)
    add(pose, "upper-left", dx=-40 * hop * on, dy=-10 * on)
    add(pose, "elbow-left", dy=40 * on)
    add(pose, "hips", dy=-8 * hop * on)
    add(pose, "head", dy=10 * hop * on)
    add(pose, "orbit", dz=-720 * t)
    bounce = 0.05 * abs(math.sin(TAU * beats / 2 * t)) * on
    return pose, {"hips": (0.03 * hop * on, 0, bounce)}, 1.0


def default_dance(t):
    """The Default Dance, as the game's default emote goes: arms pumping down across the body in time with
    a side step, then both arms thrown up and over, twice through."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    pose = mix(REST, DOWN, on)
    beats = 8
    b = math.sin(TAU * beats * t)
    half = (t * 2) % 1                                  # each half: pumping, then the overhead swing
    # The pumping comes back in as the arms come down from overhead, so each half ends on the pose the next
    # one starts from.
    over = smooth01((half - 0.55) / 0.1) * (1 - smooth01((half - 0.92) / 0.08))
    pump = 1 - over
    for side, sign in (("right", 1), ("left", -1)):
        beat = max(0.0, sign * b)
        add(pose, f"upper-{side}", dx=(-55 - 25 * beat) * pump * on, dy=sign * -20 * beat * pump * on)
        add(pose, f"elbow-{side}", dx=-70 * pump * on)
        add(pose, f"upper-{side}", dx=-160 * over * on, dy=sign * 30 * math.sin(TAU * 4 * t) * over * on)
        add(pose, f"leg-{side}", dy=sign * 10 * beat * on)
        add(pose, f"knee-{side}", dx=20 * beat * on)
    add(pose, "hips", dy=-6 * b * on)
    add(pose, "head", dy=8 * b * on, dx=-5 * over * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0.05 * b * on, 0, 0.03 * abs(b) * on - 0.03 * on)}, blink(t, 0.5)


def orange_justice(t):
    """Orange Justice: both arms swung like pendulums, forward and back, while the knees knock in and out
    and the whole body pumps up and down."""
    on = envelope(t, 0.0, 0.08, 0.92, 1.0)
    beats = 6
    a = math.sin(TAU * beats * t)
    k = math.sin(TAU * beats * 2 * t)
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        add(pose, f"upper-{side}", dx=-60 * a * on, dy=sign * 15 * on)
        add(pose, f"elbow-{side}", dx=-35 * on)
        add(pose, f"leg-{side}", dz=sign * 25 * k * on, dx=-15 * on)
        add(pose, f"knee-{side}", dx=30 * on + 10 * k * on)
    add(pose, "torso", dx=8 * a * on)
    add(pose, "head", dx=-6 * a * on, dz=10 * k * on)
    add(pose, "antenna", dx=16 * a * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0, 0, (-0.08 + 0.04 * abs(k)) * on)}, 1.0


# The rest of the dances all run at 120 beats a minute -- fifteen frames a beat -- and count their beats as
# `n * t`, so the light rig in `archie.js` can flash on them. `BEATS` there must agree with the `n` here.

def goal(side: str, up: float) -> dict:
    """An arm held out to the side at shoulder height with the forearm bent square: `up` 1 points the forearm
    at the sky, -1 at the ground -- the robot's own 'goalpost'."""
    sign = 1 if side == "right" else -1
    return {f"upper-{side}": (0, sign * 85, 0), f"elbow-{side}": (0, sign * 90 * up, 0)}


def held(poses: list, p: float, snap=0.22):
    """Pose `floor(p)` of `poses`, popped into from the one before in the first `snap` of the beat and then
    held dead still: the Robot's stop-start."""
    i = math.floor(p)
    f = smooth01((p - i) / snap)
    return mix(poses[(i - 1) % len(poses)], poses[i % len(poses)], f), f


def robot(t):
    """The Robot: arms locked in right angles, snapping from one pose to the next on the beat and holding
    it, with the head ticking round and the chest popping on each hit."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 8
    p = n * t
    A = {**goal("right", 1), **goal("left", -1), "head": (0, 0, -25), "torso": (0, -4, 0)}
    B = {**goal("right", -1), **goal("left", 1), "head": (0, 0, 25), "torso": (0, 4, 0)}
    C = {**goal("right", 1), **goal("left", 1), "head": (-8, 0, 0)}
    D = {"upper-right": (0, 90, 0), "upper-left": (0, -90, 0), "elbow-right": (0, 0, 0),
         "elbow-left": (0, 0, 0), "head": (6, 12, 0)}
    E = {"upper-right": (0, 90, 0), "elbow-right": (0, 0, 0), **goal("left", 1), "head": (0, -14, -20),
         "torso": (0, 6, 12)}
    pose, f = held([A, B, A, B, C, D, E, C], p)
    pose = mix(REST, pose, on)
    hit = (1 - f) * on                                   # the jolt as each pose lands
    add(pose, "torso", dx=5 * hit)
    add(pose, "antenna", dy=25 * hit * (1 if math.floor(p) % 2 else -1))
    for side in ("right", "left"):
        add(pose, f"knee-{side}", dx=14 * on)
        add(pose, f"leg-{side}", dx=-7 * on)
    add(pose, "orbit", dz=-90 * math.floor(p) - 90 * f)  # the moon ticks round a quarter a beat
    return pose, {"hips": (0, 0, (-0.03 - 0.015 * hit) * on)}, blink(t, 0.62)


def electro_shuffle(t):
    """The Electro Shuffle: both feet twisting heel and toe out to the sides and back, one leg kicking out on
    each beat, fists pumping at the chest."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 10
    p = n * t
    twist = math.sin(math.pi * p)                        # swaps direction every beat
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        kick = max(0.0, sign * math.sin(math.pi * p)) ** 1.5       # right on even beats, left on odd
        add(pose, f"leg-{side}", dy=sign * 30 * kick * on, dz=35 * twist * on, dx=-8 * kick * on)
        add(pose, f"knee-{side}", dx=(18 + 22 * kick) * on)
        add(pose, f"heel-{side}", dx=-15 * kick * on)
        pump = math.sin(TAU * p / 2 + (0 if sign > 0 else math.pi))
        add(pose, f"upper-{side}", dx=(-45 - 30 * pump) * on, dy=sign * 30 * on)
        add(pose, f"elbow-{side}", dx=-85 * on, dy=-sign * 35 * on)
    add(pose, "hips", dy=-8 * twist * on, dz=-12 * twist * on)
    add(pose, "torso", dz=10 * twist * on)
    add(pose, "head", dy=6 * twist * on, dx=-4 * on)
    add(pose, "orbit", dz=-720 * t)
    bounce = abs(math.sin(math.pi * p))
    return pose, {"hips": (0.04 * twist * on, 0, (-0.05 + 0.03 * bounce) * on)}, blink(t, 0.5)


def hype(t):
    """Hype: both fists punched to the sky and pulled back down to the shoulders on every beat, knees
    bouncing, then arms crossed in an X over the chest for the last two beats, thrown open to the sky again
    as the pattern starts over."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 8
    p = n * t
    cross = smooth01((p - 5.8) / 0.4) * (1 - smooth01((p - 7.4) / 0.6))
    pull = 0.5 - 0.5 * math.cos(TAU * p)                 # 0: fists up; 1: pulled down, on the beat
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        up = {f"upper-{side}": (0, sign * 165, 0), f"elbow-{side}": (0, sign * 5, 0)}
        down = goal(side, 1)
        x = {f"upper-{side}": (-75, -sign * 30, 0), f"elbow-{side}": (-35, -sign * 25, 0)}
        arm = mix(mix(up, down, pull), x, cross)
        for k, v in arm.items():
            add(pose, k, *(c * on for c in v))
    bounce = pull * (1 - cross)
    for side in ("right", "left"):
        add(pose, f"knee-{side}", dx=30 * bounce * on)
        add(pose, f"leg-{side}", dx=-15 * bounce * on)
        add(pose, f"heel-{side}", dx=-10 * bounce * on)
    add(pose, "head", dx=(10 * bounce - 12 * cross) * on)
    add(pose, "torso", dx=6 * bounce * on)
    add(pose, "antenna", dx=-18 * bounce * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0, 0, -0.07 * bounce * on)}, blink(t, 0.3)


def boogie_down(t):
    """Boogie Down: the disco point -- right arm stabbing up at the sky, then down across the body at the
    opposite hip, on alternate beats -- with the hips rolling from side to side and the left hand on the
    hip."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 10
    p = n * t
    pt = 0.5 - 0.5 * math.cos(math.pi * p)             # 0: up, 1: down, swapping every beat
    pt = smooth01(pt * 1.4 - 0.2)                        # snap, so each point reads as a hit
    up = {"upper-right": (-30, 150, 0), "elbow-right": (0, 0, 0)}
    down = {"upper-right": (-45, -40, 0), "elbow-right": (0, -15, 0)}
    pose = mix(REST, {**REST, **mix(up, down, pt), "upper-left": (0, -45, 0), "elbow-left": (0, 95, 0)}, on)
    roll = math.sin(math.pi * p)
    add(pose, "hips", dy=10 * roll * on, dz=8 * math.cos(math.pi * p) * on)
    for side in ("right", "left"):
        add(pose, f"leg-{side}", dy=-10 * roll * on)
    add(pose, "knee-right", dx=25 * max(0.0, roll) * on)
    add(pose, "knee-left", dx=25 * max(0.0, -roll) * on)
    add(pose, "torso", dy=-14 * roll * on)
    add(pose, "head", dx=(-14 + 26 * pt) * on, dz=(-15 + 25 * pt) * on, dy=6 * roll * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0.05 * roll * on, 0, -0.04 * on)}, blink(t, 0.7)


def get_griddy(t):
    """The Griddy: hands up at the face making goggles, elbows out, while the feet walk in place, each heel
    tapping down in front with the toe up and the body leaning back into it."""
    on = envelope(t, 0.0, 0.08, 0.92, 1.0)
    n = 8
    p = n * t
    # The head is too big for the hands to reach the eyes, so the goggles are held up beside the visor:
    # upper arms raised forward past horizontal, forearms straight up and leaning in.
    pose = mix(REST, {**DOWN, "upper-right": (-120, 22, 0), "elbow-right": (-60, -28, 0),
                      "upper-left": (-120, -22, 0), "elbow-left": (-60, 28, 0), "head": (-6, 0, 0)}, on)
    step = math.sin(math.pi * p)                          # +1: the right heel is out in front
    for side, sign in (("right", 1), ("left", -1)):
        out = max(0.0, sign * step)
        add(pose, f"leg-{side}", dx=-38 * out * on)
        add(pose, f"knee-{side}", dx=(12 - 8 * out) * on)
        add(pose, f"heel-{side}", dx=-38 * out * on)
        add(pose, f"elbow-{side}", dy=sign * 12 * out * on)   # the goggles wobble with the steps
    add(pose, "torso", dx=-8 * abs(step) * on)
    add(pose, "head", dy=8 * step * on, dx=4 * abs(step) * on)
    add(pose, "hips", dz=-10 * step * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0, 0.04 * abs(step) * on, (-0.04 + 0.03 * abs(step)) * on)}, blink(t, 0.45)


def billy_bounce(t):
    """The Billy Bounce: a bouncy step to one side and then the other, knees high, arms hanging loose and
    swinging with the body."""
    on = envelope(t, 0.0, 0.08, 0.92, 1.0)
    n = 8
    p = n * t
    side_of = math.sin(math.pi * p / 2)                  # two beats each way
    bounce = abs(math.sin(math.pi * p))
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        lift = max(0.0, math.sin(math.pi * p + (0 if sign > 0 else math.pi)))
        add(pose, f"leg-{side}", dx=-30 * lift * on, dy=-sign * 8 * side_of * on)
        add(pose, f"knee-{side}", dx=55 * lift * on)
        add(pose, f"heel-{side}", dx=-10 * lift * on)
        swing = math.sin(math.pi * p + (math.pi / 2 if sign > 0 else -math.pi / 2))
        add(pose, f"upper-{side}", dx=-35 * swing * on, dy=sign * (15 + 10 * bounce) * on)
        add(pose, f"elbow-{side}", dx=(-25 - 20 * max(0.0, swing)) * on)
    add(pose, "torso", dy=-8 * side_of * on, dx=4 * bounce * on)
    add(pose, "head", dy=12 * side_of * on, dx=8 * (1 - bounce) * on)
    add(pose, "antenna", dy=-20 * side_of * on, dx=-12 * bounce * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0.12 * side_of * on, 0, (-0.03 + 0.05 * bounce) * on)}, blink(t, 0.55)


def fresh(t):
    """Fresh, the Carlton as Fortnite has it: both arms swung together from one side of the body to the
    other in front of the hips, with a step-touch and the head turned the other way."""
    on = envelope(t, 0.0, 0.08, 0.92, 1.0)
    n = 8
    p = n * t
    s = math.sin(math.pi * p)                            # +1: arms over to the robot's left, screen right
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        add(pose, f"upper-{side}", dx=-30 * on, dy=(-62 * s + sign * 14) * on)
        add(pose, f"elbow-{side}", dx=-55 * on, dy=-35 * s * on)
        touch = max(0.0, -sign * s)                      # the leg on the side the arms swing from
        add(pose, f"leg-{side}", dy=sign * 18 * touch * on)
        add(pose, f"knee-{side}", dx=20 * touch * on)
        add(pose, f"heel-{side}", dx=-15 * touch * on)
    add(pose, "hips", dy=6 * s * on, dz=-10 * s * on)
    add(pose, "torso", dz=-12 * s * on)
    add(pose, "head", dz=22 * s * on, dy=-6 * s * on)
    add(pose, "orbit", dz=-720 * t)
    bounce = abs(math.sin(math.pi * p))
    return pose, {"hips": (-0.07 * s * on, 0, (0.02 * bounce - 0.03) * on)}, blink(t, 0.35)


def scenario(t):
    """Scenario: one arm then the other thrown straight up at the sky on every beat, the hips bouncing and
    kicking out to the side of the raised arm."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 8
    p = n * t
    which = math.sin(math.pi * p)                        # +1: right arm up
    bounce = abs(which)
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        raise_ = max(0.0, sign * which) ** 0.7
        # Raised by abduction alone: with any forward swing in it the Euler order points the arm at the
        # camera, and a raised arm seen end-on is invisible.
        add(pose, f"upper-{side}", dx=-10 * raise_ * on, dy=sign * (10 + 155 * raise_) * on)
        add(pose, f"elbow-{side}", dx=-40 * (1 - raise_) * on)
        add(pose, f"knee-{side}", dx=(10 + 30 * raise_) * on)
        add(pose, f"heel-{side}", dx=-12 * raise_ * on)
    add(pose, "hips", dy=12 * which * on)
    for side in ("right", "left"):
        add(pose, f"leg-{side}", dy=-12 * which * on)
    add(pose, "torso", dy=-10 * which * on)
    add(pose, "head", dx=-12 * bounce * on, dy=10 * which * on)
    add(pose, "antenna", dy=-22 * which * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (-0.06 * which * on, 0, (-0.05 + 0.04 * bounce) * on)}, blink(t, 0.6)


def groove_jam(t):
    """Groove Jam: a side step out and back, shoulders bouncing on every beat, both forearms up in front
    swinging side to side like a pair of pendulums the wrong way up."""
    on = envelope(t, 0.0, 0.06, 0.94, 1.0)
    n = 8                                                # a whole number of four-beat steps, so it repeats
    p = n * t
    step = math.sin(math.pi * p / 2)                     # two beats each way
    swing = math.sin(math.pi * p)
    bounce = abs(swing)
    pose = mix(REST, DOWN, on)
    for side, sign in (("right", 1), ("left", -1)):
        add(pose, f"upper-{side}", dx=-30 * on, dy=(sign * 28 - 18 * swing) * on)
        add(pose, f"elbow-{side}", dx=-100 * on, dy=-30 * swing * on)
        add(pose, f"shoulder-{side}", dx=-6 * bounce * on)
        out = max(0.0, sign * step)
        add(pose, f"leg-{side}", dy=sign * 20 * out * on)
        add(pose, f"knee-{side}", dx=(15 + 15 * bounce) * on)
    add(pose, "torso", dy=-6 * step * on, dx=5 * bounce * on)
    add(pose, "head", dx=8 * bounce * on, dy=10 * step * on)
    add(pose, "antenna", dx=-15 * bounce * on)
    add(pose, "orbit", dz=-720 * t)
    return pose, {"hips": (0.08 * step * on, 0, (-0.06 + 0.035 * (1 - bounce)) * on)}, blink(t, 0.4)


def pulse(s: float, at: float, rise: float, hold: float, fall: float) -> float:
    """0, easing up to 1 over `rise` seconds ending at `at`, held for `hold`, easing back down over `fall`."""
    if s < at:
        return smooth01((s - at + rise) / rise)
    return 1 - smooth01((s - at - hold) / fall)


# The right arm's two links, pivot to elbow and elbow to wrist, for reaching along a line.
BICEP, FOREARM = 0.25, 0.28


def reach(angle: float, d: float) -> dict:
    """The right arm with its wrist `d` metres from the shoulder along a line `angle` degrees forward of
    straight down, the elbow dropping below the line as the arm pulls back: two-link IK in the arm's plane."""
    d = min(d, BICEP + FOREARM - 1e-4)
    inner = math.degrees(math.acos((BICEP ** 2 + FOREARM ** 2 - d * d) / (2 * BICEP * FOREARM)))
    lift = math.degrees(math.asin(FOREARM * math.sin(math.radians(inner)) / d))
    return {"upper-right": (-(angle - lift), 0, 0), "elbow-right": (-(180 - inner), 0, 0)}


PRESS = 135                     # four and a half seconds
PRESS_ANGLE = 100               # the jab's line: 10 degrees above horizontal, straight ahead; any higher
                                # and the fist is lost against the head, seen from the side
# The frames (from 0) each jab reaches full stretch on. Even, because the export keeps every other frame and
# a peak between two kept frames would be cut short.
PRESS_STEADY = (30, 46, 62)
PRESS_CROSS = (94, 102, 110)


def press(t):
    """Tries to push a button in front of him that doesn't work: the right arm comes up to point straight
    ahead and a little up, jabs three times on a steady beat, and holds still while he tilts his head at
    the hand. Then three quicker, crosser jabs with the body leaning in, and the arm goes back down. The
    jab is in the arm's own plane, so it reads best from the side, which is how the page shows it."""
    s = t * PRESS / FPS
    up = envelope(t, 0.1 * FPS / PRESS, 0.7 * FPS / PRESS, 3.8 * FPS / PRESS, 4.4 * FPS / PRESS)
    steady = max(pulse(s, c / FPS, 0.12, 0.07, 0.22) for c in PRESS_STEADY)
    cross = max(pulse(s, c / FPS, 0.07, 0.07, 0.12) for c in PRESS_CROSS)
    ext = max(steady, cross)
    arm = reach(PRESS_ANGLE, 0.34 + (BICEP + FOREARM - 0.34) * ext)
    pose = mix(REST, {**REST, **arm, "head": (8, 0, -6)}, up)
    look = envelope(s, 2.15, 2.45, 2.85, 3.05)
    add(pose, "head", dx=10 * look, dy=16 * look, dz=-12 * look)
    add(pose, "torso", dx=4 * steady * up + 7 * cross * up, dz=-4 * up)
    add(pose, "head", dx=3 * steady * up - 4 * cross * up)
    add(pose, "heel-right", dx=-18 * cross)                  # a stamp with each cross jab
    add(pose, "antenna", dx=-14 * ext * up + 10 * look)
    add(pose, "orbit", dz=-360 * t)
    lean = {"shoulder-right": (0, -0.03 * ext * up, 0)}
    return pose, lean, blink(t, 2.5 / 4.5) * blink(t, 2.75 / 4.5)


def shrug(t):
    """The shrug: forearms out in front with the hands turned palm up, shoulders hunched up to the ears and
    the head cocked, then back to rest."""
    up = envelope(t, 0.03, 0.25, 0.72, 0.97)
    bob = up * (0.8 + 0.2 * math.sin(math.pi * smooth01((t - 0.25) / 0.47)))
    pose = mix(REST, {
        "upper-right": (-15, 28, 0), "elbow-right": (-80, 35, 0), "hand-right": (0, 0, 120),
        "upper-left": (-15, -28, 0), "elbow-left": (-80, -35, 0), "hand-left": (0, 0, -120),
        "head": (-6, 16, 0), "torso": (-3, 0, 0),
    }, up)
    add(pose, "antenna", dy=-18 * up)
    add(pose, "orbit", dz=-180 * t)
    lift = 0.06 * bob
    return pose, {"shoulder-right": (0, 0, lift), "shoulder-left": (0, 0, lift)}, blink(t, 0.5)


# How far each leg swings in the walk, in degrees, and the loop's length. `archie.js` moves the model at the
# speed these two give -- `WALK_SPEED` there -- so the feet do not slide. Change one and change it there.
STRIDE = 32
WALK = 24

CLIPS = {"idle": (120, idle), "watch": (150, watch), "floss": (120, floss), "sit": (180, sit),
         "sleep": (270, sleep), "walk": (WALK, walk), "take-the-l": (120, take_the_l),
         "default-dance": (150, default_dance), "orange-justice": (120, orange_justice),
         "robot": (120, robot), "electro-shuffle": (150, electro_shuffle), "hype": (120, hype),
         "boogie-down": (150, boogie_down), "get-griddy": (120, get_griddy),
         "billy-bounce": (120, billy_bounce), "fresh": (120, fresh), "scenario": (120, scenario),
         "groove-jam": (120, groove_jam), "press": (PRESS, press), "shrug": (60, shrug)}

# Each dance is baked as this many repeats of its pattern above, easing in and out once (see `envelope`), so
# it lasts fifteen or sixteen seconds. The beats the page counts, `BEATS` in `archie.js`, are `n` times this.
REPEAT = {"floss": 4, "take-the-l": 4, "default-dance": 3, "orange-justice": 4, "robot": 4,
          "electro-shuffle": 3, "hype": 4, "boogie-down": 3, "get-griddy": 4, "billy-bounce": 4, "fresh": 4,
          "scenario": 4, "groove-jam": 4}


def frames_of(clip: str) -> int:
    return CLIPS[clip][0] * REPEAT.get(clip, 1)


def pose_at(clip: str, T: float):
    """The clip's pose at phase T of the clip as baked: for a dance, of all its repeats together."""
    global LONG
    fn, r = CLIPS[clip][1], REPEAT.get(clip, 1)
    if r == 1:
        return fn(T)
    LONG = (r, T)
    try:
        return fn(T * r % 1.0)
    finally:
        LONG = None


def _fcurves(action):
    """F-curves across both action layouts: Blender 4.4+ keeps them in layered channelbags."""
    out = list(getattr(action, "fcurves", []) or [])
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in strip.channelbags:
                out += list(bag.fcurves)
    return out


def apply_pose(P, base_rot, base_loc, t, clip):
    rots, locs, eye = pose_at(clip, t)
    for name, ob in P.items():
        r = rots.get(name, (0, 0, 0))
        ob.rotation_euler = tuple(b + math.radians(d) for b, d in zip(base_rot[name], r))
        l = locs.get(name, (0, 0, 0))
        ob.location = tuple(b + d for b, d in zip(base_loc[name], l))
    P["eyes"].scale = (1.0, 1.0, eye)


def animate(P) -> None:
    """One NLA track per clip, named for it; the glTF exporter turns each track into one animation."""
    base_rot = {k: tuple(v.rotation_euler) for k, v in P.items()}
    base_loc = {k: tuple(v.location) for k, v in P.items()}
    for clip in CLIPS:
        frames = frames_of(clip)
        for f in range(1, frames + 1):
            apply_pose(P, base_rot, base_loc, (f - 1) / frames, clip)
            for ob in P.values():
                ob.keyframe_insert("rotation_euler", frame=f)
                ob.keyframe_insert("location", frame=f)
            P["eyes"].keyframe_insert("scale", frame=f)
        for ob in P.values():
            act = ob.animation_data.action
            act.name = f"{clip}-{ob.name}"
            for fc in _fcurves(act):
                for k in fc.keyframe_points:
                    k.interpolation = "LINEAR"
            track = ob.animation_data.nla_tracks.new()
            track.name = clip
            strip = track.strips.new(clip, 1, act)
            strip.name = clip
            ob.animation_data.action = None
    apply_pose(P, base_rot, base_loc, 0.0, "idle")


# ------------------------------------------------------------------------------------------------------
# Light, camera, render, export
# ------------------------------------------------------------------------------------------------------

def aim(ob, target) -> None:
    d = np.array(target) - np.array(ob.location)
    ob.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)


def stage() -> None:
    sc = bpy.context.scene
    world = bpy.data.worlds.new("world")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.022, 0.03, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
    sc.world = world

    def area(name, loc, energy, color, size):
        li = bpy.data.lights.new(name, "AREA")
        li.energy, li.color, li.size = energy, color, size
        ob = bpy.data.objects.new(name, li)
        sc.collection.objects.link(ob)
        ob.location = loc
        aim(ob, (0, 0, 1.1))

    area("key", (-2.2, -3.0, 3.0), 900, (1.0, 0.95, 0.88), 2.5)
    area("fill", (2.8, -2.2, 1.4), 260, (0.75, 0.82, 1.0), 3.0)
    area("rim", (0.6, 3.0, 2.8), 700, (1.0, 0.75, 0.4), 1.5)

    cam = bpy.data.cameras.new("cam")
    cam.lens = 70
    ob = bpy.data.objects.new("cam", cam)
    sc.collection.objects.link(ob)
    ob.location = (0.9, -6.2, 1.55)
    aim(ob, (0, 0, 1.08))
    sc.camera = ob

    for engine in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = engine
            break
        except TypeError:
            continue
    sc.render.film_transparent = True
    # Square, at twice the banner slot's 240 CSS px, and framed exactly as `docs/assets/archie.js` frames the
    # live model -- same camera, same aim, same 28.8-degree field -- so the poster and the first rendered
    # frame are the same picture and the swap between them does not jump.
    sc.render.resolution_x, sc.render.resolution_y = 480, 480
    # `--zoom 3` renders previews at three times the size, for looking at the surface detail.
    if "--zoom" in sys.argv:
        sc.render.resolution_percentage = int(100 * float(sys.argv[sys.argv.index("--zoom") + 1]))
    sc.render.image_settings.file_format = "PNG" if PREVIEW else "WEBP"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.image_settings.quality = 82
    # Standard, not AgX: AgX rolls every emitter toward cream, and the gold is the brand. The browser does its
    # own tone mapping on the GLB anyway, so this only decides the poster.
    sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"


def render(path: Path, clip="idle", t=0.0) -> None:
    pivots = PIVOTS
    for ob in pivots.values():
        if ob.animation_data:
            ob.animation_data.use_nla = False
    apply_pose(pivots, BASE_ROT, BASE_LOC, t, clip)
    sc = bpy.context.scene
    sc.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    for ob in pivots.values():
        if ob.animation_data:
            ob.animation_data.use_nla = True


def export() -> None:
    """The GLB the banner loads, kept small because it is fetched on every desktop visit: a mesh whose
    material has no textures loses its UVs (they were an eighth of the file), the textures go as WebP, and
    the clips are sampled every other frame -- 15 a second, linear between -- which the slowest motion here
    does not need more of."""
    GLB.parent.mkdir(parents=True, exist_ok=True)
    for ob in bpy.data.objects:
        if ob.type == "MESH" and not (ob.data.materials and ob.data.materials[0].get("textured")):
            while ob.data.uv_layers:
                ob.data.uv_layers.remove(ob.data.uv_layers[0])
    bpy.ops.export_scene.gltf(
        filepath=str(GLB), export_format="GLB", export_apply=True, export_yup=True,
        export_animations=True, export_animation_mode="NLA_TRACKS", export_force_sampling=True,
        export_optimize_animation_size=True, export_cameras=False, export_lights=False,
        export_extras=False, export_image_format="WEBP", export_image_quality=88, export_frame_step=2)


PIVOTS: dict = {}
BASE_ROT: dict = {}
BASE_LOC: dict = {}


def main() -> None:
    reset()
    P = build()
    PIVOTS.update(P)
    BASE_ROT.update({k: tuple(v.rotation_euler) for k, v in P.items()})
    BASE_LOC.update({k: tuple(v.location) for k, v in P.items()})
    stage()
    if PREVIEW:
        # `--preview <clip> <t> ...` renders stills of each clip at phase t, without animating.
        args = sys.argv[sys.argv.index("--preview") + 1:]
        for clip, t in zip(args[::2], args[1::2]):
            render(HERE / f"preview-{clip}-{float(t):.2f}.png", clip, float(t))
        return
    animate(P)
    render(POSTER, "idle", 0.0)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND), compress=True)
    export()
    print(f"wrote {BLEND}, {GLB} ({GLB.stat().st_size:,} bytes), {POSTER}")


main()
