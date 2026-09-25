"""The video wall's clips: four seamless eight-second loops, drawn frame by frame here and encoded by Blender.

    python art/rig/wall.py [a b c d]     # all four when none are named
    python art/rig/wall.py --check       # measure them; encode nothing

writes, into `docs/assets/rig/`:

  * `wall-a.webm` / `wall-a.mp4` / `wall-a.webp` -- "tunnel": rings of the blue-hour beam colours flowing out
    of the middle of the wall, with a slow turn of spokes through them.
  * `wall-b.webm` / `wall-b.mp4` / `wall-b.webp` -- "levels": a 24-band LED equaliser in the afterglow colours,
    over its own reflection on the stage floor.
  * `wall-c.webm` / `wall-c.mp4` / `wall-c.webp` -- "archie": Archie himself in silhouette, rim-lit, with the
    ember look's beams swinging through the haze behind him. The silhouette is rendered from `archie.glb` by
    Blender each time this runs, so it is always the Archie the page hangs.
  * `wall-d.webm` / `wall-d.mp4` / `wall-d.webp` -- "field": a grid of dots swelling and shrinking under two
    slow waves, one travelling across the wall and one turning round its middle, in the low-tide colours,
    going ember where the waves meet.

480 x 240, 24 fps, 192 frames, no audio. VP9 in WebM first, H.264 in MP4 for Safari, and a WebP of frame 0
as the poster, which is also what a reader with reduced motion is shown in their place.

TWO MACHINES, ONE FILE. The frames are numpy and PIL, which the system Python has and Blender's does not;
the encoding is Blender's bundled FFmpeg, because this machine has no other. So run under Python this draws
the frames into a temporary folder and then runs Blender on this same file, which finds `bpy`, loads the
frames into the sequencer and renders them out twice. It runs Blender once more first, to render Archie's
silhouette.

SEAMLESS, BY CONSTRUCTION. Every motion is a function of `t` in [0, 1) that is periodic in it: the tunnel
moves exactly four rings a loop and there are four colours, so frame 192 would be frame 0; every equaliser
band, every beam's swing and every wave in the field is a sine of a whole number of cycles a loop. Nothing is
cut or cross-faded.

NOTHING FLASHES (WCAG 2.3.1). The fastest any pixel's light goes up and back is the tunnel's rings passing it,
four times in eight seconds, and the equaliser's quickest band moves at three cycles a loop; the beams and
the waves are slower still. All are far under three a second. No frame is lighter overall than about a
fifth of white, and none is a full-frame change from the last: the wall is a backdrop, and a bright one
would out-shine the rig in front of it. `--check` prints each clip's range of mean luminance, its largest
mean frame-to-frame change and its loop error.

THE COLOURS are the look book's (`docs/assets/rig-show.js`, LOOKS): blue-hour's beams for the tunnel,
afterglow's for the levels, ember's for Archie and low-tide's for the field, so each clip sits in a look.
The page may tint or cross-fade them; they are dark enough to take it.
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "docs" / "assets" / "rig"
ARCHIE_GLB = ROOT / "docs" / "assets" / "archie.glb"
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe")
W, H, FPS, FRAMES = 480, 240, 24, 192
KBPS = 220                                  # 8 s at 220 kbit/s is about 220 KB: under the 300 KB each is allowed
# ...except the field: hundreds of small hard-edged discs are what VP9 is worst at, and at 220 it overshot to
# 304 KB. 170 brings it back under with room, and at this size nobody can see the difference.
KBPS_FOR = {"d": 170}

BLUE_HOUR = ["#6FD3FF", "#4E7BFF", "#9C8CFF", "#3FE0C5"]
AFTERGLOW = ["#2EC4B6", "#FF4FA3", "#FFB000", "#7A5CFF"]
EMBER = ["#FFB347", "#FF7A45", "#FF5E7E", "#FFD27A"]
LOW_TIDE = ["#5F7DFF", "#8A6BFF", "#5CC8FF", "#A0B4FF"]
SIL = {}                                    # "archie": his silhouette's alpha at wall size, once rendered


def blender(*args):
    subprocess.run([BLENDER, "--background", "--factory-startup", "--python-exit-code", "1", "--python",
                    str(Path(__file__)), "--", *map(str, args)], check=True, stdout=subprocess.DEVNULL)


# ---- drawing (system Python) ------------------------------------------------------------------------------
def _rgb(hexes):
    import numpy as np
    return np.array([[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)] for h in hexes], np.float32)


def _blur(a, px):
    import numpy as np
    from PIL import Image, ImageFilter
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(px))
    return np.asarray(im, dtype=np.float32) / 255


def tunnel(t):
    """Rings spaced evenly in log-radius, so they seem to come at you down a tube; four colours, four rings a
    loop. Spokes turn a sixth of a revolution a loop and darken the rings between them."""
    import numpy as np
    P = _rgb(BLUE_HOUR)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    dx, dy = (x - W / 2 + 0.5) / H, (y - H / 2 + 0.5) / H
    r = np.sqrt(dx * dx + dy * dy) + 1e-4
    a = np.arctan2(dy, dx)
    u = 3.0 * np.log(r) - 4.0 * t                       # four rings a loop, outward
    ring = np.floor(u).astype(int) % 4
    f = u - np.floor(u)
    # Each ring is a bright line with a wide glow round it and a wash of its colour filling the ring, so the
    # wall reads as lit video from across the stage and not as a few hairlines on black. (The first cut had
    # the line alone, a mean luminance of 0.05, and on the wall it looked switched off.)
    d = np.abs(f - 0.5)
    line = np.clip(1 - d / 0.2, 0, 1) ** 1.3
    glow = np.exp(-(d / 0.22) ** 2)
    spokes = 0.7 + 0.3 * np.cos(6 * a + 2 * np.pi * t)            # six spokes, one sixth turn a loop
    depth = np.clip(r / 0.14, 0, 1) ** 0.8                         # the far end of the tube is dark
    edge = np.clip(1.4 - r, 0, 1)                                   # and the corners fall away
    lum = (0.95 * line + 0.35 * glow + 0.12) * spokes * depth * edge
    white = np.clip(line - 0.75, 0, 1) * 1.6 * depth                # the hottest part of a line goes toward white
    return P[ring] * lum[..., None] + white[..., None] * 0.5 + np.array([0.02, 0.025, 0.06])


def levels(t):
    """Twenty-four bands of LED blocks. Each band's level is a mix of whole-cycle sines, so the loop closes;
    a peak cap above each falls back to it. Colour runs up the bar through the look's four beam colours."""
    import numpy as np
    P = _rgb(AFTERGLOW)
    rng = np.random.default_rng(7)
    n = 24
    ph = rng.random((n, 3))
    k = np.arange(n) / (n - 1)
    lvl = (0.42 + 0.22 * np.sin(2 * np.pi * (1 * t + ph[:, 0]))
           + 0.14 * np.sin(2 * np.pi * (2 * t + ph[:, 1]))
           + 0.08 * np.sin(2 * np.pi * (3 * t + ph[:, 2])))
    lvl *= 1.0 - 0.35 * (k - 0.35) ** 2                              # a bass-heavy shape across the bands
    img = np.zeros((H, W, 3)) + np.array([0.015, 0.012, 0.03])
    floor = int(H * 0.74)                                             # the stage line; the reflection is below
    rows = 18                                                         # LED blocks a bar
    bw = W / n
    cell = (floor - 8) / rows
    for i in range(n):
        x0, x1 = int(i * bw + bw * 0.18), int((i + 1) * bw - bw * 0.18)
        on = int(round(lvl[i] * rows))
        for j in range(rows):
            y1 = int(floor - 4 - j * cell)
            y0 = int(y1 - cell * 0.72)
            q = j / (rows - 1) * 3
            c = P[int(q)] * (1 - (q % 1)) + P[min(3, int(q) + 1)] * (q % 1)
            img[y0:y1, x0:x1] = c * (0.85 if j < on else 0.07)       # the unlit blocks, just visible
        # A thin cap one block over the level, where the peak hold would sit.
        yc = int(floor - 4 - min(rows - 1, on) * cell - cell * 0.72) - 2
        if yc > 0:
            img[yc - 2:yc, x0:x1] = P[3] * 0.9
    ref = img[floor - (H - floor) * 2:floor][::-2][:H - floor]         # squashed mirror image, faded
    fade = np.linspace(0.28, 0.0, H - floor)[:, None, None]
    img[floor:] = img[floor:] + ref * fade
    img[floor:floor + 1] = np.array([0.16, 0.12, 0.2])                 # the stage edge
    return img


def archie(t):
    """Archie's silhouette, dark against the haze, with five of the ember look's beams swinging behind him
    from above the wall and a rim of light round his edge whose colour drifts through the look."""
    import numpy as np
    P = _rgb(EMBER)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    haze = 0.05 + 0.1 * (y / H) ** 1.5                                # thicker toward the floor
    img = haze[..., None] * np.array([0.9, 0.55, 0.45], np.float32)
    for i in range(5):
        ox = W * (0.1 + 0.2 * i)
        ang = 0.38 * np.sin(2 * np.pi * (t + i / 5)) * (1 if i % 2 else -1)   # one swing a loop, alternate ways
        th = np.arctan2(x - ox, y + 30)                               # each pixel's angle from the source's down
        beam = np.exp(-((th - ang) / 0.075) ** 2) * (0.35 + 0.65 * (y / H))
        img += beam[..., None] * P[i % 4] * 0.55
    a = SIL["archie"]
    rim = np.clip(_blur(np.clip((a - _blur(a, 2.2)) * 3, 0, 1), 0.8), 0, 1)   # his edge, where the backlight catches
    k = (np.sin(2 * np.pi * t) + 1) / 2                               # rim colour drifts gold to coral and back
    rc = P[3] * (1 - k) + P[2] * k
    img = img * (1 - a[..., None]) + np.array([0.035, 0.03, 0.04]) * a[..., None]
    img += rim[..., None] * rc * 0.9
    img += (_blur(a, 14) * (1 - a) * 0.35)[..., None] * rc             # the glow the haze makes behind him
    return img


def field(t):
    """Dots on a 16 px grid, each one's radius the product of two waves: one crossing the wall on a diagonal
    twice a loop, one turning round the centre once. Where both are high the dot is big and goes ember."""
    import numpy as np
    P, E = _rgb(LOW_TIDE), _rgb(EMBER)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    C = 16
    cx, cy = (np.floor(x / C) + 0.5) * C, (np.floor(y / C) + 0.5) * C   # the centre of each pixel's cell
    u, v = cx / W, cy / H
    w1 = 0.5 + 0.5 * np.sin(2 * np.pi * (1.5 * u + 0.75 * v - 2 * t))
    ang = np.arctan2(cy - H / 2, cx - W / 2)
    rr = np.hypot((cx - W / 2) / H, (cy - H / 2) / H)
    w2 = 0.5 + 0.5 * np.sin(2 * ang - 2 * np.pi * t + 5 * rr)
    lvl = w1 * (0.35 + 0.65 * w2)
    dot = np.clip(1.5 + 6.0 * lvl - np.hypot(x - cx, y - cy) + 0.5, 0, 1)   # an anti-aliased disc
    q = u * 2.999                                                    # low-tide's colours, left to right
    i0 = np.floor(q).astype(int)
    base = P[i0] * (1 - q % 1)[..., None] + P[i0 + 1] * (q % 1)[..., None]
    hot = np.clip((lvl - 0.55) / 0.35, 0, 1)[..., None]
    col = base * (1 - hot) + E[1] * hot
    return np.array([0.02, 0.022, 0.05]) + dot[..., None] * col * (0.35 + 0.65 * lvl[..., None])


FNS = {"a": tunnel, "b": levels, "c": archie, "d": field}


def silhouette():
    """Archie's alpha from `archie.glb`, rendered by Blender and fitted to the wall: 92% of its height,
    standing centred on its bottom edge."""
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "sil.png"
        blender("silhouette", png)
        im = Image.open(png).getchannel("A")
        im.load()
    im = im.crop(im.getbbox())
    h = int(H * 0.92)
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    a = np.zeros((H, W), np.float32)
    x0, y0 = (W - im.width) // 2, H - h - 2
    a[y0:y0 + h, x0:x0 + im.width] = np.asarray(im, np.float32) / 255
    SIL["archie"] = a


def draw(kind, folder: Path):
    import numpy as np
    from PIL import Image
    for i in range(FRAMES):
        im = Image.fromarray((np.clip(FNS[kind](i / FRAMES), 0, 1) * 255 + 0.5).astype("uint8"))
        im.save(folder / f"f{i:04d}.png")
        if i == 0:
            im.save(OUT / f"wall-{kind}.webp", quality=72, method=6)


def check():
    """Each clip's range of mean luminance, its biggest mean frame-to-frame change, and frame 192 against 0."""
    import numpy as np
    Y = np.array([0.2126, 0.7152, 0.0722], np.float32)
    for kind, fn in FNS.items():
        L = [np.clip(fn(i / FRAMES), 0, 1) @ Y for i in range(FRAMES + 1)]
        m = [l.mean() for l in L]
        step = max(np.abs(L[i + 1] - L[i]).mean() for i in range(FRAMES))
        print(f"wall-{kind}: mean luminance {min(m):.3f}..{max(m):.3f}, largest step {step:.4f}, "
              f"loop error {np.abs(L[FRAMES] - L[0]).max():.6f}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    silhouette()
    if "--check" in sys.argv:
        return check()
    for kind in [a for a in sys.argv[1:] if a in FNS] or list(FNS):
        with tempfile.TemporaryDirectory() as tmp:
            draw(kind, Path(tmp))
            for ext in ("webm", "mp4"):
                blender("encode", tmp, ext, OUT / f"wall-{kind}.{ext}", KBPS_FOR.get(kind, KBPS))
        for ext in ("webm", "mp4", "webp"):
            p = OUT / f"wall-{kind}.{ext}"
            print(f"{p.name:14s} {p.stat().st_size:>9,} bytes")


# ---- in Blender ----------------------------------------------------------------------------------------------
def encode(folder: str, ext: str, dest: str, kbps: str):
    import bpy
    s = bpy.context.scene
    s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = W, H, 100
    s.render.fps, s.frame_start, s.frame_end = FPS, 1, FRAMES
    s.view_settings.view_transform = "Standard"                    # the frames' colours, not a film curve's
    ed = s.sequence_editor_create()
    strips = ed.strips if hasattr(ed, "strips") else ed.sequences      # renamed in Blender 4.4
    names = sorted(n for n in os.listdir(folder) if n.endswith(".png"))
    st = strips.new_image(name="wall", filepath=os.path.join(folder, names[0]), channel=1, frame_start=1)
    for n in names[1:]:
        st.elements.append(n)
    ims = s.render.image_settings
    if hasattr(ims, "media_type"):
        ims.media_type = "VIDEO"
    ims.file_format = "FFMPEG"
    f = s.render.ffmpeg
    f.format, f.codec = ("WEBM", "WEBM") if ext == "webm" else ("MPEG4", "H264")
    f.audio_codec = "NONE"
    f.constant_rate_factor = "NONE"                                 # a bitrate, so the size is predictable
    f.video_bitrate, f.maxrate, f.minrate = int(kbps), int(kbps) * 2, 0
    f.gopsize = FPS * 2
    f.ffmpeg_preset = "BEST"
    s.render.filepath = os.path.join(folder, "out_")
    bpy.ops.render.render(animation=True)
    made = [p for p in os.listdir(folder) if p.startswith("out_")]
    shutil.move(os.path.join(folder, made[0]), dest)


def render_silhouette(dest: str):
    """Archie from the front, orthographic, as alpha only: the workbench engine on a transparent film."""
    import bpy
    from mathutils import Vector
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(ARCHIE_GLB))
    s = bpy.context.scene
    pts = [o.matrix_world @ Vector(c) for o in s.objects if o.type == "MESH" for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
    s.collection.objects.link(cam)
    s.camera = cam
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = (hi.z - lo.z) * 1.08
    c = (lo + hi) / 2
    cam.location = (c.x, lo.y - 5, c.z)                            # glTF +Z (his front) is Blender -Y
    cam.rotation_euler = (math.pi / 2, 0, 0)
    s.render.engine = "BLENDER_WORKBENCH"
    s.render.film_transparent = True
    s.render.resolution_x = s.render.resolution_y = 720
    s.render.filepath = dest
    bpy.ops.render.render(write_still=True)


try:
    import bpy  # noqa: F401
except ImportError:
    if __name__ == "__main__":
        main()
else:
    _a = sys.argv[sys.argv.index("--") + 1:]
    {"encode": encode, "silhouette": render_silhouette}[_a[0]](*_a[1:])
