"""Subset the two embedded families to what the site draws, as woff2, into docs/assets/fonts/.

Not a pipeline stage: the three files are committed, and this is how they were made, for whoever next needs
a glyph the site does not have yet. It is run by hand, outside CI, against the two upstream releases:

    gh release download v3.5.1 -R ryanoasis/nerd-fonts -p GeistMono.tar.xz      # into <geistmono-dir>
    gh release download v1.7.2 -R vercel/geist-font -p geist-font-v1.7.2.zip     # into <geist-dir>
    python -I scripts/subset_fonts.py <geist-dir> <geistmono-dir> docs/assets/fonts

`-I` because the archives are downloads: their directories should never be on the import path. Needs
fontTools and brotli (`pip install fonttools brotli`), which nothing else in the repository does.

An Octicon added to the build tags has to be added to ICONS here and to `ICON` in docs/assets/atlas-site.js,
and the code point must fall inside the "Atlas Icons" range in scripts/sitewide.py, or it draws as a box.
"""
import sys
from pathlib import Path

from fontTools import subset

geist, mono, out = (Path(a) for a in sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)

# Google Fonts' "latin" range, plus Latin Extended-A for maintainers' names, the arrows and the two
# verdict glyphs the footer legend prints (U+2713, U+2717).
TEXT = ("U+0000-00FF,U+0100-017F,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,"
        "U+0329,U+2000-206F,U+20AC,U+2122,U+2190-21FF,U+2212,U+2215,U+2713,U+2717,U+FEFF,U+FFFD")
# The mono face also draws the build badges, so it keeps box drawing, the geometric shapes and the
# Octicons the badges use: check-circle-fill, x-circle-fill, sync, dot-fill, clock, rocket, database,
# beaker, workflow, mark-github, git-commit, skip, alert, pulse, stopwatch, package.
ICONS = "U+F4A4,U+F530,U+F46A,U+F444,U+F43A,U+F427,U+F472,U+F499,U+F52E,U+F408,U+F417,U+F517,U+F421,U+F469,U+F520,U+F487"
MONO = TEXT + ",U+2500-25FF," + ICONS


def run(src: Path, dst: Path, ranges: str, keep_variations: bool) -> None:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum", "zero", "ss01"]
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.notdef_outline = True
    opts.hinting = False
    opts.desubroutinize = True
    font = subset.load_font(str(src), opts)
    s = subset.Subsetter(opts)
    s.populate(unicodes=subset.parse_unicodes(ranges))
    s.subset(font)
    subset.save_font(font, str(dst), opts)
    print(f"{dst.name:24s} {dst.stat().st_size:>7,d} bytes  ({len(font.getGlyphOrder())} glyphs)"
          f"{'  variable' if keep_variations and 'fvar' in font else ''}")


run(geist / "geist-font/Geist/webfonts/Geist[wght].woff2", out / "geist.woff2", TEXT, True)
run(mono / "GeistMonoNerdFont-Regular.otf", out / "geist-mono.woff2", MONO, False)
run(mono / "GeistMonoNerdFont-SemiBold.otf", out / "geist-mono-600.woff2", MONO, False)
