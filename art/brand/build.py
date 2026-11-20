"""Every raster of Archie the site serves, cut from the two renders of the current Archie in `.github/readme/`.

    python art/brand/build.py

Run by hand when the art changes, like the Blender scripts beside it; the pipeline never runs it, because it
needs Pillow and the pipeline is stdlib. Its outputs are committed:

| Output | From | Used by |
|---|---|---|
| `docs/assets/archie-head.webp` (96 px) | `archie.png` | the top-left logo on every page (`scripts/mark.py`), seated in a raised disc by CSS |
| `docs/assets/archie-mark.webp` (96 px) | `icon.png` | the v2 beta's rail mark (`scripts/30_v2.py`) |
| `docs/assets/archie-bust.webp` (256 px wide) | `archie.png` | the catalogue's upper-right mascot (`scripts/19_pages.py`) |
| `docs/favicon.svg` | `icon.png` at 64 px, embedded | every page's `<link rel="icon">` |
| `art/brand/icon-192.png`, `icon-512.png`, `icon-maskable-512.png`, `apple-touch-icon.png`, `favicon.ico` | `icon.png` | copied into `docs/` by `scripts/24_pwa.py` on every build |

The app icons live here rather than in `docs/` because both workflows require a generator to rewrite each
tracked file under `docs/` that is not under `docs/assets/`; `24_pwa.py` does that by copying them.

These replace the first Archie -- the black robot with pixel shades and a gold globe (`atlas-byte.png`, and the
globe-and-shades vector the old `favicon.svg`, `mark.py` and `24_pwa.icon()` drew). The source renders are the
owner's (commit 5635fcc989, "README: the new Archie and his icon"). `icon.png` is 256 px, so the two 512 px
icons are upscaled from it; a larger render of the same tile is the fix if they look soft on a launcher.
"""
from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / ".github" / "readme"
HERE = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

# The tile's own plate, sampled from `icon.png` (it is also the old mark's `PLATE`, which is why
# `24_pwa.SURFACE` did not move).
PLATE = (0x09, 0x0A, 0x0D, 255)


def tile() -> Image.Image:
    return Image.open(SRC / "icon.png").convert("RGBA")


def sized(im: Image.Image, px: int) -> Image.Image:
    return im.resize((px, px), Image.Resampling.LANCZOS)


def png_bytes(im: Image.Image) -> bytes:
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def opaque(px: int, inset: float) -> Image.Image:
    """The head on a square, full-bleed plate: the OS rounds or masks it.

    The tile's own rounded rim is cropped away (`inset` of the edge on each side), and what is left is the
    plate and the head, scaled so the plate fills the square. Android's maskable icon also needs the head
    inside the middle 80%, so it shrinks the interior onto a plate-coloured square instead.
    """
    t = tile()
    edge = t.size[0]
    # Everything outside a rounded rectangle just inside the rim becomes plate, so neither the rim nor the
    # transparent corners survive; then the rim's band is cropped off.
    cut = round(edge * 0.045)
    keep = Image.new("L", t.size, 0)
    ImageDraw.Draw(keep).rounded_rectangle((cut, cut, edge - 1 - cut, edge - 1 - cut),
                                           radius=round(edge * 0.25), fill=255)
    flat = Image.new("RGBA", t.size, PLATE)
    flat.paste(t, (0, 0), keep)
    inner = flat.crop((cut, cut, edge - cut, edge - cut))
    out = Image.new("RGBA", (px, px), PLATE)
    face = px - 2 * round(px * inset)
    out.alpha_composite(sized(inner, face), ((px - face) // 2, (px - face) // 2))
    return out


def ico(images: list[bytes], sizes: list[int]) -> bytes:
    """An ICO of PNG entries (the same layout `24_pwa.ico()` used to write)."""
    import struct
    head = struct.pack("<HHH", 0, 1, len(images))
    at = len(head) + 16 * len(images)
    entries, body = b"", b""
    for size, data in zip(sizes, images):
        entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), at + len(body))
        body += data
    return head + entries + body


def main() -> None:
    t = tile()

    # The logo. 96 px for a 30 px slot, so a 3x screen still gets real pixels.
    sized(t, 96).save(DOCS / "assets" / "archie-mark.webp", "WEBP", quality=90, method=6)

    # The logo: his head alone, transparent, from the render. The site's soft UI seats it in a raised disc of
    # the page's own colour, so it needs no plate of its own. Cut square around the head, above the neck.
    render = Image.open(SRC / "archie.png").convert("RGBA")
    head_box = render.getchannel("A").crop((0, 0, render.width, 207)).getbbox()
    if head_box is None:
        raise SystemExit(".github/readme/archie.png has no opaque pixels; it is not the render this expects.")
    hl, ht, hr, hb = head_box
    side = max(hr - hl, hb - ht) + 8
    cx, cy = (hl + hr) // 2, (ht + hb) // 2
    x0, y0 = cx - side // 2, cy - side // 2
    head = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    part = render.crop((max(x0, 0), max(y0, 0), min(x0 + side, render.width), min(y0 + side, 207)))
    head.alpha_composite(part, (max(x0, 0) - x0, max(y0, 0) - y0))
    sized(head, 96).save(DOCS / "assets" / "archie-head.webp", "WEBP", quality=90, method=6)

    # The catalogue's mascot: head and shoulders, trimmed to the render's opaque box, and cut to the first
    # Archie's 512:532 so the catalogue's masthead column keeps its exact height at every width.
    bust = Image.open(SRC / "archie.png").convert("RGBA")
    box = bust.getchannel("A").getbbox()
    if box is None:
        raise SystemExit(".github/readme/archie.png has no opaque pixels; it is not the render this expects.")
    l, t_, r, _ = box
    w = r - l
    bust = bust.crop((l, t_, r, t_ + round(w * 532 / 512)))
    bust = bust.resize((256, 266), Image.Resampling.LANCZOS)
    bust.save(DOCS / "assets" / "archie-bust.webp", "WEBP", quality=90, method=6)
    print("archie-bust.webp", bust.size)

    # The tab icon. An SVG wrapper rather than a PNG link, because ~12,800 pages already name
    # `favicon.svg`; a data: image inside an SVG used as an image is allowed (no external fetch).
    b64 = base64.b64encode(png_bytes(sized(t, 64))).decode("ascii")
    (DOCS / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        "  <title>Archie 'Atlas' Algorithm</title>\n"
        f'  <image width="64" height="64" href="data:image/png;base64,{b64}"/>\n'
        "</svg>\n", encoding="utf-8", newline="\n")

    # The installed-app icons, copied into `docs/` by `scripts/24_pwa.py`.
    (HERE / "icon-192.png").write_bytes(png_bytes(sized(t, 192)))
    (HERE / "icon-512.png").write_bytes(png_bytes(sized(t, 512)))
    (HERE / "icon-maskable-512.png").write_bytes(png_bytes(opaque(512, 0.10)))
    (HERE / "apple-touch-icon.png").write_bytes(png_bytes(opaque(180, 0.0)))
    sizes = [16, 32, 48]
    (HERE / "favicon.ico").write_bytes(ico([png_bytes(sized(t, s)) for s in sizes], sizes))

    for p in [DOCS / "assets" / "archie-head.webp", DOCS / "assets" / "archie-mark.webp", DOCS / "assets" / "archie-bust.webp", DOCS / "favicon.svg",
              *sorted(HERE.glob("*.png")), HERE / "favicon.ico"]:
        print(f"{p.relative_to(ROOT).as_posix():40s} {p.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
