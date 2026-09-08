"""The five platform marks, drawn once and used by every surface that names a platform.

Four generators print the words Windows, WSL2, macOS, Linux and Docker: the index (filter chips and a row
of five verdicts per project), the 156 facet pages, the 1,294 detail pages and the curated collections.
Replacing those words with marks is only an improvement if all four draw the *same* mark for the same
platform, so the geometry lives here and nowhere else -- there is no second copy to drift, which is the
failure mode `tests/theme_test.py` exists to catch for the palette.

FOUR DECISIONS, because each one is a thing a reader could lose:

  The mark never replaces the accessible name. Every use carries the word in a `title` and, where it is
  the whole of a control's label, in a visually-hidden span. A filter chip reading "Windows" to a screen
  reader before this change must still read "Windows" after it, or this is a regression dressed as a
  polish. An icon is a shorthand for people who can see it and nothing at all to anyone else.

  Order is checked, not assumed. `data.json`'s `os` column is a five-character verdict string and the
  labels are a parallel array, so the icons are matched to platforms by position -- and a mark paired with
  the wrong column is a page that states a falsehood about which platforms a project runs on. `check()`
  raises on any disagreement rather than letting a reordered `OS_LABELS` publish quietly.

  Solid silhouettes, `currentColor`, no interior knock-outs. These are drawn at 13-16px beside an 11.5px
  verdict glyph and inherit the verdict's colour, which is green, amber or grey depending on the answer
  and different again in each theme. An outline at that size fills in; a knocked-out highlight needs a
  known background colour, and there isn't one.

  One sprite per document, referenced by `<use>`. Five inline SVGs per row across 1,294 rows would be
  ~400 KB of repeated path data on the index alone. The sprite is ~1.4 KB once and each use is ~70 bytes.
  The wrapper is `display:none`, which is the ordinary way to do this: a `<symbol>` is never drawn where
  it is defined, so hiding its container costs nothing and keeps it out of the layout.

Markdown and the workbook keep the words. GitHub strips `<svg>` from rendered Markdown, and a spreadsheet
cell has no document to reference a symbol in -- so `mega-list/**` and the xlsx stay textual, and so does
the index's own Markdown export. That is not an omission; it is the same reason those surfaces print the
verdict as a glyph rather than as a colour.
"""
from __future__ import annotations

# Positional, and the position is load-bearing: index k of every one of these lists describes character k
# of a row's `os` string. `check()` is the guard.
LABELS = ["Windows", "WSL2", "macOS", "Linux", "Docker"]
IDS = ["oi-windows", "oi-wsl2", "oi-macos", "oi-linux", "oi-docker"]

# What hovering says. Longer than the label where the label is an abbreviation nobody should have to
# already know -- "WSL2" is the one platform here whose mark cannot be recognised on sight.
TITLES = {
    "Windows": "Windows",
    "WSL2": "WSL2 — Windows Subsystem for Linux 2",
    "macOS": "macOS",
    "Linux": "Linux",
    "Docker": "Docker",
}

# The geometry, on a 24x24 grid. Kept as the inner markup of each `<symbol>` rather than as bare path data
# because two of the five are clearer as primitives than as one heroic path, and a `<symbol>` may hold as
# many shapes as it likes.
SHAPES = {
    # Four panes. The one mark in this set that is exactly itself at any size.
    "oi-windows": '<path d="M3 3h8v8H3zm10 0h8v8h-8zM3 13h8v8H3zm10 0h8v8h-8z"/>',
    # A window frame with a shell prompt inside it, which is what WSL2 is. `evenodd` cuts the frame open:
    # the ring is two same-wound rectangles, and the chevron and underscore sit in the hole at winding 3,
    # so they fill while the hole around them does not.
    "oi-wsl2": '<path fill-rule="evenodd" d="M2 3.5h20v17H2zm2 2v13h16v-13zm3.4 3.7L8.8 7.9 12.6 12l-3.8 '
               '4.1-1.4-1.3L9.9 12zm6 5.4h4.2v1.6h-4.2z"/>',
    # Two lobes with a dip between them, a wide body under both, and a leaf. The dip is what makes it an
    # apple rather than a cloud, so the lobes have to sit higher than the body's top.
    "oi-macos": '<circle cx="8.8" cy="11.2" r="4.2"/><circle cx="15.2" cy="11.2" r="4.2"/>'
                '<ellipse cx="12" cy="14.8" rx="7" ry="5.4"/>'
                '<path d="M12.5 7.4c-.3-1.5.2-2.9 1.2-3.9 1-1 2.4-1.5 3.6-1.5.1 1.4-.4 2.8-1.4 3.8-1 '
                '1-2.3 1.5-3.4 1.6z"/>',
    # Tux as a silhouette: round head, tall body, two flippers and two feet splayed out at the bottom.
    # The feet are the part that reads as a penguin at 13px, so they are wider than they are subtle.
    "oi-linux": '<circle cx="12" cy="6.2" r="3.7"/><ellipse cx="12" cy="14" rx="5.5" ry="6.3"/>'
                '<ellipse cx="8.2" cy="20.2" rx="2.9" ry="1.5"/>'
                '<ellipse cx="15.8" cy="20.2" rx="2.9" ry="1.5"/>'
                '<path d="M6.6 10.3c-1.8 1-3 2.9-3 4.9 0 1.1.5 1.9 1.2 1.9.9 0 1.8-1.5 2.4-3.4z"/>'
                '<path d="M17.4 10.3c1.8 1 3 2.9 3 4.9 0 1.1-.5 1.9-1.2 1.9-.9 0-1.8-1.5-2.4-3.4z"/>',
    # A hull with a stack of containers on its back. Docker's whale also has a tail and a spout; both are
    # under two pixels wide here and read as noise, so they are left out.
    "oi-docker": '<rect x="6.4" y="9.6" width="3.2" height="3.2" rx=".5"/>'
                 '<rect x="10.2" y="9.6" width="3.2" height="3.2" rx=".5"/>'
                 '<rect x="14" y="9.6" width="3.2" height="3.2" rx=".5"/>'
                 '<rect x="10.2" y="5.8" width="3.2" height="3.2" rx=".5"/>'
                 '<path d="M2.4 13.6h19.2c.4 0 .7.4.6.8-.5 2.4-2 4.3-4.1 5.3-1.7.8-3.7 1.2-6 1.2-4.1 '
                 '0-7.5-1.2-9.4-3.2-1-1.1-1.6-2.3-1.6-3.4 0-.4.3-.7.7-.7z"/>',
}

# One per document, immediately after `<body>`. `aria-hidden` because a definition block is not content,
# and `display:none` rather than a clipped 1px box because nothing in here is ever drawn in place.
SPRITE = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
          + "".join(f'<symbol id="{i}" viewBox="0 0 24 24">{SHAPES[i]}</symbol>' for i in IDS)
          + "</svg>")

# The base rule, shared by all three stylesheets. Sizing is per-surface and stays with the surface: a chip
# wants a mark slightly larger than its text, a row of verdicts wants one that does not out-weigh the
# glyph beside it. `em` so both track whatever font-size the context set.
CSS = """/* The five platform marks -- scripts/osicons.py owns the geometry; these are the only rules that
   apply to all of them. `fill:currentColor` is the whole reason they can sit inside a coloured verdict:
   a green Y and a grey dash get a green and a grey mark without either being named here. */
.oi{width:1.15em;height:1.15em;fill:currentColor;vertical-align:-.19em;flex:none}
/* A mark and its word, when both are shown, should not be separable by a line break. */
.oiw{white-space:nowrap}
/* The legend -- see `legend()` for why a `title` is not enough. Sized and coloured like the caption it is,
   and it wraps, because five pairs do not fit on one line at 335px. */
.oikey{display:flex;flex-wrap:wrap;gap:4px 14px;margin:0 0 12px;font-size:12.5px;color:var(--muted)}"""

# The ids as a JavaScript array literal, for the index's client script. Emitted rather than retyped, so
# the page and the sprite in it cannot disagree about a name.
JS_IDS = "[" + ",".join(f'"{i}"' for i in IDS) + "]"

# And the hover texts, in the same order and for the same reason. The index builds its five filter chips in
# the browser, and those chips are a mark with no word on them -- so this array is the only thing standing
# between a reader and an unlabelled square, which is the whole of WSL2's problem. No escaping beyond the
# quotes: every value is a plain-text literal above, with no quote character and no backslash in any of them.
JS_TITLES = "[" + ",".join(f'"{TITLES[lab]}"' for lab in LABELS) + "]"


def check(os_labels: list[str]) -> None:
    """Refuse to draw if the caller's platform order is not the one these marks were paired with.

    Called by every generator against whatever it is about to iterate -- `OS_LABELS` in 19_pages.py,
    `data["os"]` everywhere downstream. The marks are matched by position and nothing else, so a reordered
    or renamed column would silently publish a Docker mark over a Windows verdict. There is no honest
    fallback for that, and a wrong answer about which platforms a project runs on is the specific thing a
    reader comes here for.
    """
    if list(os_labels) != LABELS:
        raise SystemExit(
            "scripts/osicons.py draws the five platform marks in this order:\n"
            f"  {LABELS}\n"
            "and the caller is about to iterate:\n"
            f"  {list(os_labels)}\n\n"
            "The marks are paired with platforms by position, so publishing this would put some other "
            "platform's mark beside each verdict. Update LABELS, IDS, TITLES and SHAPES in "
            "scripts/osicons.py together -- they are four parallel lists and changing one is never right.")


def use(k: int, cls: str = "oi") -> str:
    """One mark, by platform index. `aria-hidden` because the word is always supplied beside it."""
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#{IDS[k]}"></use></svg>'


def use_terse(k: int, cls: str = "oi") -> str:
    """The same mark, spelled as short as HTML allows, for a surface that draws hundreds of them.

    44 bytes against `use()`'s 87, and the difference is two attributes rather than anything about the
    picture. `focusable="false"` is an IE11 attribute; no browser in support reads it. `aria-hidden` is
    load-bearing, so dropping it is only safe where the marks sit inside a container that carries the
    accessible name for the whole group -- `role="img"` with an `aria-label`, which makes the children
    presentational and gives a screen reader one sentence about the row instead of five fragments. A
    caller with no such container wants `use()`; the two forms are not interchangeable.

    `href="#..."` keeps its quotes. Unquoted, the `/` that closes the tag is swallowed into the attribute
    value and the element never closes -- which is a whole document lost to save one byte.

    Why the terse form exists at all: `20_landing.py` draws 505 of these on its biggest facet page and
    there are 156 pages. The 43 bytes that say nothing are 3.3 MB of committed HTML, and `docs/` is
    committed verbatim.
    """
    return f'<svg class="{cls}"><use href="#{IDS[k]}"/></svg>'


def legend(cls: str = "oikey") -> str:
    """All five marks with their words, once per page, for the reader who has never seen them.

    A `title` answers "which platform is the penguin" on a desktop and answers nothing at all on a phone,
    where there is no hover and a long-press is a text selection. Every surface that prints a mark instead
    of a word therefore needs the pairing stated somewhere in the page, visibly, in text -- otherwise the
    marks are a private notation and the row of five verdicts is unreadable to anybody arriving cold.

    The index does not need this: its "Runs on" filter row is five labelled controls sitting directly
    above the table, which is a legend that also does something. Everywhere else -- the facet pages, the
    collections -- this is the legend.
    """
    return (f'<p class="{cls}">Runs on: '
            + " ".join(f'<span class="oiw">{use(k)} {LABELS[k]}</span>' for k in range(len(LABELS)))
            + "</p>")


def title(k: int) -> str:
    """The hover text for platform `k`, without the surrounding attribute."""
    return TITLES[LABELS[k]]
