"""The video wall's clips: two seamless eight-second loops, drawn frame by frame here and encoded by Blender.

    python art/rig/wall.py

writes, into `docs/assets/rig/`:

  * `wall-a.webm` / `wall-a.mp4` / `wall-a.webp` -- "tunnel": rings of the blue-hour beam colours flowing out
    of the middle of the wall, with a slow turn of spokes through them.
  * `wall-b.webm` / `wall-b.mp4` / `wall-b.webp` -- "levels": a 24-band LED equaliser in the afterglow colours,
    over its own reflection on the stage floor.

480 x 240, 24 fps, 192 frames, no audio. VP9 in WebM first, H.264 in MP4 for Safari, and a WebP of frame 0
as the poster, which is also what a reader with reduced motion is shown in their place.

TWO MACHINES, ONE FILE. The frames are numpy and PIL, which the system Python has and Blender's does not;
the encoding is Blender's bundled FFmpeg, because this machine has no other. So run under Python this draws
the frames into a temporary folder and then runs Blender on this same file, which finds `bpy`, loads the
frames into the sequencer and renders them out twice.

SEAMLESS, BY CONSTRUCTION. Every motion is a function of `t` in [0, 1) that is periodic in it: the tunnel
moves exactly four rings a loop and there are four colours, so frame 192 would be frame 0; every equaliser
band is a sum of sines of whole numbers of cycles a loop. Nothing is cut or cross-faded.

NOTHING FLASHES (WCAG 2.3.1). The fastest any pixel's light goes up and back is the tunnel's rings passing it,
four times in eight seconds, and the equaliser's quickest band moves at three cycles a loop; both are far
under three a second. No frame is lighter overall than about a fifth of white, and none is a full-frame
change from the last: the wall is a backdrop, and a bright one would out-shine the rig in front of it.

THE COLOURS are the look book's (`docs/assets/rig-show.js`, LOOKS): blue-hour's beams for the tunnel and
afterglow's for the levels, so each clip sits in a look. The page may tint or cross-fade them; they are
dark enough to take it.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / "docs" / "assets" / "rig"
BLENDER = os.environ.get("BLENDER", r"C:/Program Files/Blender Foundation/Blender 5.2/blender.exe")
W, H, FPS, FRAMES = 480, 240, 24, 192
KBPS = 220                                  # 8 s at 220 kbit/s is about 220 KB: under the 300 KB each is allowed

BLUE_HOUR = ["#6FD3FF", "#4E7BFF", "#9C8CFF", "#3FE0C5"]
AFTERGLOW = ["#2EC4B6", "#FF4FA3", "#FFB000", "#7A5CFF"]


# ---- drawing (system Python) ------------------------------------------------------------------------------
def _rgb(hexes):
    import numpy as np
    return np.array([[int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)] for h in hexes])


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
    band = np.clip(1 - np.abs(f - 0.5) / 0.18, 0, 1) ** 1.5      # a soft-edged line in each ring's middle
    spokes = 0.55 + 0.45 * np.cos(6 * a + 2 * np.pi * t)          # six spokes, one sixth turn a loop
    depth = np.clip(r / 0.25, 0, 1) ** 1.2                         # the far end of the tube is dark
    edge = np.clip(1.25 - r, 0, 1)                                  # and the corners fall away
    lum = band * spokes * depth * edge
    img = P[ring] * lum[..., None] * 0.9 + np.array([0.02, 0.025, 0.06]) * (1 - lum[..., None])
    return img


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
    y = np.arange(floor)
    cell = (floor - 8) / rows
    for i in range(n):
        x0, x1 = int(i * bw + bw * 0.18), int((i + 1) * bw - bw * 0.18)
        on = int(round(lvl[i] * rows))
        for j in range(rows):
            y1 = int(floor - 4 - j * cell)
            y0 = int(y1 - cell * 0.72)
            q = j / (rows - 1) * 3
            c = P[int(q)] * (1 - (q % 1)) + P[min(3, int(q) + 1)] * (q % 1)
            if j < on:
                img[y0:y1, x0:x1] = c * 0.85
            else:
                img[y0:y1, x0:x1] = c * 0.07                          # the unlit blocks, just visible
        # A thin cap one block over the level, where the peak hold would sit.
        yc = int(floor - 4 - min(rows - 1, on) * cell - cell * 0.72) - 2
        if yc > 0:
            img[yc - 2:yc, x0:x1] = P[3] * 0.9
    ref = img[floor - (H - floor) * 2:floor][::-2][:H - floor]         # squashed mirror image, faded
    fade = np.linspace(0.28, 0.0, H - floor)[:, None, None]
    img[floor:] = img[floor:] + ref * fade
    img[floor:floor + 1] = np.array([0.16, 0.12, 0.2])                 # the stage edge
    return img


def draw(kind, folder: Path):
    import numpy as np
    from PIL import Image
    fn = {"a": tunnel, "b": levels}[kind]
    for i in range(FRAMES):
        rgb = np.clip(fn(i / FRAMES), 0, 1)
        Image.fromarray((rgb * 255 + 0.5).astype("uint8")).save(folder / f"f{i:04d}.png")
        if i == 0:
            Image.fromarray((rgb * 255 + 0.5).astype("uint8")).save(OUT / f"wall-{kind}.webp", quality=72, method=6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for kind in ("a", "b"):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            draw(kind, tmp)
            for ext in ("webm", "mp4"):
                subprocess.run([BLENDER, "--background", "--factory-startup", "--python-exit-code", "1", "--python", str(Path(__file__)),
                                "--", str(tmp), ext, str(OUT / f"wall-{kind}.{ext}")], check=True,
                               stdout=subprocess.DEVNULL)
        for ext in ("webm", "mp4", "webp"):
            p = OUT / f"wall-{kind}.{ext}"
            print(f"{p.name:14s} {p.stat().st_size:>9,} bytes")


# ---- encoding (Blender) -------------------------------------------------------------------------------------
def encode(folder: str, ext: str, dest: str):
    import bpy
    s = bpy.context.scene
    s.render.resolution_x, s.render.resolution_y, s.render.resolution_percentage = W, H, 100
    s.render.fps, s.frame_start, s.frame_end = FPS, 1, FRAMES
    s.view_settings.view_transform = "Standard"                    # the frames' colours, not a film curve's
    ed = s.sequence_editor_create()
    strips = ed.strips if hasattr(ed, "strips") else ed.sequences      # renamed in Blender 4.4
    names = sorted(os.listdir(folder))
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
    f.video_bitrate, f.maxrate, f.minrate = KBPS, KBPS * 2, 0
    f.gopsize = FPS * 2
    f.ffmpeg_preset = "BEST"
    out = os.path.join(folder, "out_")
    s.render.filepath = out
    bpy.ops.render.render(animation=True)
    made = [p for p in os.listdir(folder) if p.startswith("out_")]
    shutil.move(os.path.join(folder, made[0]), dest)


try:
    import bpy  # noqa: F401
except ImportError:
    if __name__ == "__main__":
        main()
else:
    a = sys.argv[sys.argv.index("--") + 1:]
    encode(*a)
