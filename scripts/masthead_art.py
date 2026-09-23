"""The homepage masthead's artwork: this repository's own git history and source, as a lit screen of code.

Run by hand, not by any workflow. The two images it writes, `docs/assets/masthead-dark.webp` and
`masthead-light.webp`, are committed, and nothing in the build reads this file. They are artwork, and
redrawing artwork on every daily run would change the page's bytes, re-version the service worker and
re-download a banner for every reader, all to move a commit subject nobody can read at that size.

What is on the screen is real. The left pane is `git log --oneline` for this checkout, prefixed with the
commands that produced it. The right panes are actual lines from `scripts/`, chosen with a fixed seed. The
point is that the picture is of this project, rather than of the stock-photo JavaScript it is modelled on.

The fade is baked into the alpha channel, not left to a CSS mask, so the image is seamless wherever it is
drawn:
  * the top is opaque;
  * each side reaches 0 at the edge;
  * from half-way down, opacity falls to 0 at the bottom edge.
So all three edges that touch the page are fully transparent. Only the top, which sits against the
browser's chrome, is not.

Run: python scripts/masthead_art.py
"""
from __future__ import annotations

import random
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets"

W, H = 2400, 760
# The flat sheet the code is typeset on, before the perspective warp folds it into W x H. Larger than the
# output so the warp has something to pull in from beyond the edges.
SW, SH = 3400, 1500
SEED = 5417

FONTS = ["DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
         "C:/Windows/Fonts/consola.ttf", "Menlo.ttc"]

# Two palettes, one per mode. `bg` is close to the page's own surface in that mode, so the fade meets a
# colour it nearly already is. The rest is the syntax palette: the accent family the site's cards use.
PALETTES = {
    "dark": {"bg": (9, 13, 24), "plain": (150, 170, 205), "dim": (70, 86, 118), "kw": (179, 166, 255),
             "str": (242, 184, 75), "fn": (111, 227, 196), "num": (255, 155, 210), "cmd": (124, 196, 255),
             "prompt": (111, 227, 196), "hash": (242, 184, 75), "glow": 0.85},
    "light": {"bg": (238, 242, 249), "plain": (74, 88, 118), "dim": (160, 172, 196), "kw": (86, 70, 190),
              "str": (160, 98, 0), "fn": (11, 110, 122), "num": (154, 44, 126), "cmd": (29, 94, 158),
              "prompt": (11, 110, 122), "hash": (160, 98, 0), "glow": 0.0},
}

KEYWORDS = {"def", "return", "for", "in", "if", "else", "elif", "import", "from", "const", "let", "await",
            "async", "function", "class", "with", "as", "not", "and", "or", "True", "False", "None",
            "assert", "try", "except", "raise", "while", "new", "=>"}
TOKEN = re.compile(r'(#.*$|//.*$)|("[^"]*"|\'[^\']*\'|`[^`]*`)|(\b\d[\d_.,]*\b)|([A-Za-z_][\w]*)(?=\()|'
                   r'([A-Za-z_]\w*|=>)|(\s+|.)')


def font(size: int) -> ImageFont.FreeTypeFont:
    for f in FONTS:
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    raise SystemExit("no monospace font found; tried " + ", ".join(FONTS))


def git(*args: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def code_only(lines: list[str]) -> list[str | None]:
    """Each line, or None where it is prose: comments, docstrings, and the insides of long strings."""
    out, inside = [], False
    for ln in lines:
        q = ln.count('"""') + ln.count("'''")
        if inside or q:
            out.append(None)
            if q % 2:
                inside = not inside
            continue
        st = ln.strip()
        out.append(None if st.startswith("#") or not st else ln.rstrip())
    return out


def source_lines(rng: random.Random, n: int, width: int) -> list[str]:
    """`n` lines of real code from `scripts/`, in runs of consecutive code, with a blank between runs."""
    files = sorted((ROOT / "scripts").glob("*.py"))
    out: list[str] = []
    while len(out) < n:
        lines = code_only(files[rng.randrange(len(files))].read_text(encoding="utf-8").splitlines())
        start = rng.randrange(max(1, len(lines) - 40))
        run: list[str] = []
        for ln in lines[start:]:
            if ln is None or len(ln) > width or ln.count("f'") + ln.count('f"') > 1:
                if len(run) >= 5:
                    break
                run = []
                continue
            run.append(ln)
            if len(run) >= rng.randint(7, 14):
                break
        if len(run) >= 5:
            # Dedent the run to its own left margin, the way a pane scrolled to the middle of a file shows it.
            pad = min(len(r) - len(r.lstrip()) for r in run)
            out += [r[pad:] for r in run] + [""]
    return out[:n]


def history_lines() -> list[str]:
    log = git("log", "--oneline", "--no-decorate", "-n", "44")
    branch = (git("rev-parse", "--abbrev-ref", "HEAD") or ["latest_branch"])[0]
    return ([f"$ git checkout -b {branch} origin/latest_branch", "$ python scripts/31_home.py",
             "$ python scripts/24_pwa.py", "$ node tests/run.mjs", "$ git log --oneline", ""]
            + [ln[:57] for ln in log]
            + ["", "$ git push -u origin HEAD", "$ gh pr checks"])


def paint_line(d: ImageDraw.ImageDraw, x: int, y: int, text: str, f, pal: dict, lit: float) -> None:
    """One line, tokenised just well enough to colour like an editor would."""
    def col(c):
        return tuple(int(v * lit + pal["bg"][i] * (1 - lit)) for i, v in enumerate(c))
    if text.startswith("$ "):
        d.text((x, y), "$", font=f, fill=col(pal["prompt"]))
        d.text((x + f.getlength("$ "), y), text[2:], font=f, fill=col(pal["cmd"]))
        return
    m = re.match(r"^([0-9a-f]{7,9}) (.*)$", text)
    if m:
        d.text((x, y), m.group(1), font=f, fill=col(pal["hash"]))
        d.text((x + f.getlength(m.group(1) + " "), y), m.group(2), font=f, fill=col(pal["plain"]))
        return
    cx = x
    for t in TOKEN.finditer(text):
        s = t.group(0)
        if t.group(1):
            c = pal["dim"]
        elif t.group(2):
            c = pal["str"]
        elif t.group(3):
            c = pal["num"]
        elif t.group(4):
            c = pal["fn"]
        elif t.group(5):
            c = pal["kw"] if s in KEYWORDS else pal["plain"]
        else:
            c = pal["plain"]
        if s.strip():
            d.text((cx, y), s, font=f, fill=col(c))
        cx += f.getlength(s)


def sheet(pal: dict, rng: random.Random) -> Image.Image:
    """The flat screen: three panes of code with line numbers, the way an editor lays them out."""
    img = Image.new("RGB", (SW, SH), pal["bg"])
    d = ImageDraw.Draw(img)
    f = font(30)
    lh = 44
    panes = [(60, history_lines()), (1180, source_lines(rng, 40, 56)), (2330, source_lines(rng, 40, 56))]
    for px, lines in panes:
        for i, text in enumerate(lines[: (SH - 150) // lh]):
            y = 150 + i * lh
            # Brighter towards the middle rows, where the focal band will be after the warp.
            lit = 0.55 + 0.45 * max(0.0, 1 - abs(y - SH * 0.42) / (SH * 0.55))
            d.text((px, y), f"{i + 1:>3}", font=f, fill=tuple(int(v * 0.8) for v in pal["dim"]))
            paint_line(d, px + 90, y, text, f, pal, lit)
    return img


def perspective(img: Image.Image, bg: tuple) -> Image.Image:
    """Tilt the sheet away to the right, as if photographed at an angle across a monitor.

    `Image.transform(PERSPECTIVE)` wants the eight coefficients mapping *output* pixels back to *input*
    ones, so they are solved from four corner pairs rather than written by hand."""
    src = [(0, 0), (SW, 0), (SW, SH), (0, SH)]
    # Output corners: the left edge is near and tall, the right edge far and short.
    dst = [(-30, -70), (W + 40, 120), (W + 40, H - 20), (-30, H + 170)]
    import numpy as np  # local: only this function needs it
    a, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        a += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    coef = np.linalg.solve(np.array(a, float), np.array(b, float))
    return img.transform((W, H), Image.Transform.PERSPECTIVE, tuple(coef), Image.Resampling.BICUBIC,
                         fillcolor=bg)


def depth_of_field(img: Image.Image) -> Image.Image:
    """Sharp in a band left of centre, softening towards the far right and the near left."""
    soft = img.filter(ImageFilter.GaussianBlur(5))
    softer = img.filter(ImageFilter.GaussianBlur(11))
    focus = Image.new("L", (W, H))
    far = Image.new("L", (W, H))
    fp, rp = focus.load(), far.load()
    for x in range(W):
        t = x / W
        sharp = max(0.0, 1 - abs(t - 0.40) / 0.30)
        blur2 = min(1.0, max(0.0, (t - 0.72) / 0.28))
        for y in range(0, H):
            fp[x, y] = int(255 * sharp)
            rp[x, y] = int(255 * blur2)
    out = Image.composite(img, soft, focus)
    return Image.composite(softer, out, far)


def glow(img: Image.Image, strength: float) -> Image.Image:
    """The screen's own light: a halo off the glyphs, and two soft washes of the accent colours."""
    if not strength:
        return img
    halo = img.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * strength))
    wash = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(wash)
    for (cx, cy, r, c) in [(W * 0.30, H * 0.25, 560, (20, 70, 90)), (W * 0.78, H * 0.35, 640, (48, 30, 92))]:
        d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=c)
    wash = wash.filter(ImageFilter.GaussianBlur(160))
    return ImageChops.add(ImageChops.add(img, halo), wash)


def fade_mask() -> Image.Image:
    """Opaque at the top, transparent on both sides and along the bottom, with smooth ramps.

    Horizontal: 0 at each edge, 1 from 22% in. Vertical: 1 down to half the height, then 0 at the bottom.
    The two multiply, so a bottom corner is transparent from both directions at once."""
    def smooth(t: float) -> float:
        t = min(1.0, max(0.0, t))
        return t * t * (3 - 2 * t)
    m = Image.new("L", (W, H))
    px = m.load()
    hs = [smooth(min(x, W - 1 - x) / (W * 0.22)) for x in range(W)]
    vs = [1.0 if y < H * 0.5 else smooth((H - 1 - y) / (H * 0.5)) for y in range(H)]
    for y in range(H):
        v = vs[y]
        for x in range(W):
            px[x, y] = int(255 * hs[x] * v + 0.5)
    return m


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mask = fade_mask()
    for mode, pal in PALETTES.items():
        rng = random.Random(SEED)
        art = glow(depth_of_field(perspective(sheet(pal, rng), pal["bg"])), pal["glow"])
        art = art.convert("RGBA")
        art.putalpha(mask)
        dest = OUT / f"masthead-{mode}.webp"
        art.save(dest, "WEBP", quality=72, method=6)
        print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size / 1024:.1f} KB  {W}x{H}")


if __name__ == "__main__":
    main()
