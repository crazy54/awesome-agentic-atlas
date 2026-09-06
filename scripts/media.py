"""Embed each screenshot in a workbook once, however many sheets place it.

An `.xlsx` is a ZIP, and openpyxl writes one media part per *placement* rather than per distinct
image: `Image.path` is `/xl/media/image{_id}.{format}` and `_id` is that placement's position in the
writer's list, so a screenshot placed on six sheets becomes six byte-identical parts and six ZIP
entries. That is not an openpyxl bug -- nothing in `Image` identifies two placements as the same
picture -- but this workbook places every repo's screenshot between two and seven times: its list's
own sheet, the Leaderboard, By Category, and up to four platform sheets. Measured at eleven lists that
came to 7,388 placements, against 2,394 entries in those lists and 1,294 distinct repos among them --
so two thirds of the pictures in the file were a picture the file already contained.

Two costs follow, and this module removes both:

  Bytes.   The LIGHT workbook came out near 48 MB from the Linux runner, against a much smaller file
           that had been published by hand -- the hand-made one had been through an Excel COM
           round-trip, which re-deduplicates embedded media on save. Same duplication, seen from the
           other end.
  Entries. A ZIP's central directory counts its entries in a 16-bit field, so the classic format
           tops out at ENTRY_LIMIT. Media parts are ~99% of this workbook's entries, so the entry
           count is essentially the placement count, and the placement count grows with the atlas.

How close that ceiling actually is, because the figure that prompted this module was not right. At
eleven lists the workbook is about 7,570 entries, 12% of the limit. What grows is the cross-list sheets
-- By Category once per repo, plus 2.73 of the four platform sheets per repo, measured from the
published data -- so roughly 3.7 entries per distinct repo, and the ceiling arrives near 16,800 repos.
That is past the 39-list merge (7,980 repos, 50% of the limit) and past that merge with
`TensorBlock/awesome-mcp-servers` folded in even assuming none of its 7,835 rows is a repo the atlas
already has (15,815 repos, 94%). The note that put that last case at about 118% assumed every repo
qualifies for all four platform sheets; Docker reaches 16% of them. Shared, the workbook is one entry
per picture and the ceiling moves out to roughly 65,000 repos. `tests/media_test.py` runs the projection
rather than leaving it to be re-argued.

On the entry ceiling specifically, one thing worth recording because it is easy to assume otherwise:
passing it does not make the file unwritable. `openpyxl.writer.excel.save_workbook` opens its archive
with `allowZip64=True`, and CPython's `zipfile` then quietly writes a ZIP64 end-of-central-directory
record instead of failing -- verified at 65,600 entries. So the failure mode was never a build error;
it was a silently different container format, which no version of Excel here has been tested against.
`save` below therefore opens the archive with `allowZip64=False` *and* checks the count itself, so the
ceiling is a named failure with the numbers in it rather than a format change nobody chose.

The dedup key is the source file, not the shot key. Two shot maps reach the build -- `shots_all.json`
keyed by `shot_key`, and the original pipeline's `shots.json` keyed by `nameWithOwner` -- and they can
name different files for the same repo. Keying on the file that is actually read is right by
construction: same bytes in, same part out.
"""
from __future__ import annotations

import datetime
import os
import zipfile
from io import BytesIO
from pathlib import Path

from openpyxl.drawing.image import Image as XLImage
from openpyxl.writer.excel import ExcelWriter
from PIL import Image as PILImage

# The ZIP central directory records its entry count in two bytes. Every part of the package counts:
# each worksheet, each drawing and its rels, and one per embedded image.
ENTRY_LIMIT = 65_535

# Media parts are named for the pool slot rather than for the writer's placement counter, so the name
# is stable however the sheets are ordered. A distinct stem also means a plain `XLImage` added
# alongside these -- `07_build` does that when it is run on its own -- keeps `image{N}` and cannot
# collide.
PART_STEM = "shot"


class SharedImage(XLImage):
    """One placement of a pooled image: its own anchor, a part name it shares with its siblings.

    Deliberately does not call `XLImage.__init__`. That opens the image with PIL to read its size and
    keeps the buffer it was handed -- and `Image._data` *closes* that buffer once it has read it, so
    two placements genuinely cannot share one `BytesIO`. Everything the writer wants is known once per
    distinct image instead: `Pool` renders it, measures it, and hands each placement the bytes.
    """

    def __init__(self, part: int, data: bytes, size: tuple[int, int], fmt: str):
        self.ref = None  # never read: `_data` is overridden and is the only thing that used it
        self.width, self.height = size
        self.format = fmt
        self._part = part
        self._bytes = data

    @property
    def path(self) -> str:
        # `_id` is still assigned by the writer, as it is for any image, and still ignored here. That
        # is what makes the name independent of write order -- a drawing's relationship Target is
        # resolved while its sheet is written, which for a shared part can be before the placement
        # that "owns" it has been seen at all.
        return f"/xl/media/{PART_STEM}{self._part}.{self.format}"

    def _data(self) -> bytes:
        return self._bytes


class Pool:
    """Every image embedded in one workbook, rendered once and placed as often as asked.

    One pool per workbook, not per sheet and not per run: the rendering is theme-dependent -- each
    screenshot is padded onto a canvas in the theme's background colour -- so the DARK and LIGHT
    workbooks share no bytes and must not share a pool.
    """

    def __init__(self, render):
        # `render(src) -> BytesIO`, i.e. `07_build.pad_shot` bound to one theme's background.
        self._render = render
        self._parts: dict[str, SharedImage] = {}
        self.placements = 0

    @property
    def parts(self) -> int:
        """Distinct images embedded. `placements` is how many cells show one of them."""
        return len(self._parts)

    def place(self, ws, src: Path, anchor) -> None:
        """Draw `src` on `ws` at `anchor`, embedding its bytes only if this is the first sighting."""
        # Normalised, because one file can arrive spelled two ways: `shots_all.json` stores basenames
        # that the build joins onto `cache/shots`, while the original pipeline's `shots.json` stores
        # whole paths it wrote itself -- and on Windows those can also differ only in case. A missed
        # match would cost an extra copy of the picture, not a wrong one, but the copy is the point.
        key = os.path.normcase(os.path.abspath(src))
        owner = self._parts.get(key)
        if owner is None:
            buf = self._render(src)
            data = buf.getvalue() if isinstance(buf, BytesIO) else buf.read()
            owner = self._parts[key] = SharedImage(len(self._parts) + 1, data, *_measure(data))
        # A new object per placement, sharing the same `bytes`. Adding one `SharedImage` to several
        # sheets instead would give every placement of it the last anchor assigned, because the anchor
        # is an attribute of the image -- and openpyxl would then write its one part under the last
        # `_id` it was given while the earlier sheets' relationships still pointed at the earlier
        # names, so most of the pictures would reference a part that is not in the file.
        img = SharedImage(owner._part, owner._bytes, (owner.width, owner.height), owner.format)
        img.anchor = anchor
        ws.add_image(img)
        self.placements += 1


def _measure(data: bytes) -> tuple[tuple[int, int], str]:
    """Size and format, read once per distinct image instead of once per placement."""
    with PILImage.open(BytesIO(data)) as im:
        return im.size, (im.format or "PNG").lower()


class Report:
    """What one saved workbook cost, for the build to print and CI's log to keep."""

    def __init__(self, path: Path, entries: int, parts: int, placements: int):
        self.path, self.entries, self.parts, self.placements = path, entries, parts, placements

    @property
    def headroom(self) -> int:
        return ENTRY_LIMIT - self.entries

    def __str__(self) -> str:
        return (f"{self.placements:,} placements from {self.parts:,} images  ·  "
                f"{self.entries:,} of {ENTRY_LIMIT:,} ZIP entries "
                f"({self.entries / ENTRY_LIMIT:.0%}, {self.headroom:,} spare)")


class _DedupingWriter(ExcelWriter):
    """`ExcelWriter`, writing each media part once rather than once per placement."""

    media_parts = media_placements = 0

    def _write_images(self) -> None:
        # The base class is `for img in self._images: writestr(img.path[1:], img._data())`. Pooled
        # placements share a path, so the only change needed is to skip a name already written; the
        # relationships that point at it are per-drawing and are unaffected. Several relationships
        # resolving to one part is ordinary OPC -- it is what a picture reused on one sheet has always
        # produced.
        written: set[str] = set()
        for img in self._images:
            name = img.path[1:]
            if name in written:
                continue
            written.add(name)
            self._archive.writestr(name, img._data())
        self.media_parts, self.media_placements = len(written), len(self._images)


def _abandon(archive: zipfile.ZipFile, path: Path) -> None:
    """Drop a part-written archive without finishing it.

    Not `archive.close()`: closing is what writes the central directory, and with `allowZip64=False`
    that is the very call that would raise on an over-full package -- with a worse message than the
    caller's, and late enough to replace it. Clearing `fp` is what stops `ZipFile.__del__` trying
    again during interpreter shutdown, where the traceback would be printed and ignored.
    """
    archive.fp.close()
    archive.fp = None
    path.unlink(missing_ok=True)


def save(wb, path: Path, pool: Pool | None = None) -> Report:
    """`wb.save(path)`, deduplicating embedded media and reporting what the package cost.

    Mirrors `openpyxl.writer.excel.save_workbook`, with two deliberate differences: the deduping
    writer, and `allowZip64=False`. See the module docstring for why silently writing ZIP64 is the
    wrong failure -- the count is checked here as well, so the error names the ceiling and the numbers
    rather than leaving `zipfile` to say "Files count would require ZIP64 extensions". Refusing ZIP64
    also caps the archive at 4 GB, which is two orders of magnitude past where this file has ever been.
    """
    archive = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, allowZip64=False)
    wb.properties.modified = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None)
    writer = _DedupingWriter(wb, archive)
    writer.write_data()
    entries = len(archive.namelist())
    parts, placements = writer.media_parts, writer.media_placements
    if entries > ENTRY_LIMIT:
        _abandon(archive, path)
        raise SystemExit(
            f"{path.name}: {entries:,} ZIP entries, and the classic ZIP central directory holds "
            f"{ENTRY_LIMIT:,}. {parts:,} of them are embedded images ({placements:,} placements "
            f"across the sheets). The images are already shared, so nothing is left to squeeze out "
            f"here: the fix is fewer distinct images, or fewer sheets that carry them.")
    # A postcondition, not paranoia. The dedup rides on openpyxl internals -- `ExcelWriter._images`
    # and `Image._data` -- and CI installs openpyxl unpinned, so a rename upstream would quietly put
    # the base class's per-placement `_write_images` back in charge with nothing to say so. The
    # archive is the one witness that cannot be fooled.
    if pool is not None and pool.parts != parts:
        _abandon(archive, path)
        raise SystemExit(
            f"{path.name}: the pool holds {pool.parts:,} distinct images but the package has "
            f"{parts:,} media parts, so media deduplication is not happening. Check openpyxl's "
            f"ExcelWriter._write_images against scripts/media.py.")
    archive.close()
    return Report(path, entries, parts, placements)
